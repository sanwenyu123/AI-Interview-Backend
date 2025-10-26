"""
语音相关API（短语音ASR 初版）
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Body
from sqlalchemy.orm import Session
import httpx
import asyncio
import uuid
import time
import tos
import logging
from typing import Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.config import settings


router = APIRouter()
logger = logging.getLogger(__name__)


def _map_lang(lang: str) -> str:
    if not lang:
        return settings.VOLC_ASR_LANGUAGE or "zh-CN"
    l = lang.lower()
    if l.startswith("zh"):
        return "zh-CN"
    if l.startswith("en"):
        return "en-US"
    return settings.VOLC_ASR_LANGUAGE or "zh-CN"


def _get_tos_client():
    endpoint = settings.TOS_ENDPOINT if settings.TOS_ENDPOINT.startswith("http") else f"https://{settings.TOS_ENDPOINT}"
    return tos.TosClientV2(settings.TOS_ACCESS_KEY_ID, settings.TOS_SECRET_ACCESS_KEY, endpoint, settings.TOS_REGION)


def _presign_url(client, method: str, bucket: str, object_key: str, expires: int = 600):
    # method: 'GET' or 'PUT'
    method_enum = None
    try:
        # 常见枚举名称
        if method.upper() == 'GET':
            method_enum = getattr(tos.HttpMethodType, 'HTTP_GET', None) or getattr(tos.HttpMethodType, 'Http_Method_Get', None)
        elif method.upper() == 'PUT':
            method_enum = getattr(tos.HttpMethodType, 'HTTP_PUT', None) or getattr(tos.HttpMethodType, 'Http_Method_Put', None)
    except Exception:
        method_enum = None

    try:
        if method_enum is not None:
            pres = client.pre_signed_url(method_enum, bucket, object_key, expires)
        else:
            pres = client.pre_signed_url(method.upper(), bucket, object_key, expires)
    except Exception:
        pres = client.pre_signed_url(method.upper(), bucket, object_key, expires)

    if isinstance(pres, str):
        return pres
    return getattr(pres, 'signed_url', None) or getattr(pres, 'url', None) or getattr(pres, 'presigned_url', None)


async def _auc_submit_and_query(signed_url: str, language: str, fmt: str, user_id: str):
    audio_codec = "opus" if fmt in ("ogg", "webm", "opus") else "raw"
    payload = {
        "user": {"uid": str(user_id)},
        "audio": {
            "format": fmt,
            "codec": audio_codec,
            "rate": 16000,
            "bits": 16,
            "channel": 1,
            "url": signed_url,
        },
        "language": language,
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True,
            "show_utterances": True,
        },
    }

    request_id = str(uuid.uuid4())
    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": settings.VOLC_ASR_APP_ID,
        "X-Api-Access-Key": settings.VOLC_ASR_TOKEN,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": request_id,
        "X-Api-Sequence": "-1",
    }

    try:
        async with httpx.AsyncClient() as client:
            import json as _json
            body = _json.dumps(payload, ensure_ascii=False)
            submit_endpoint = settings.VOLC_ASR_ENDPOINT
            resp = await client.post(submit_endpoint, headers=headers, content=body.encode('utf-8'), timeout=60.0)
            if resp.status_code != 200:
                text = resp.text
                try:
                    j = resp.json()
                    text = j.get('message') or j.get('detail') or text
                except Exception:
                    pass
                raise HTTPException(status_code=resp.status_code, detail=f"ASR请求失败: {text}")

            # derive query endpoint
            try:
                query_endpoint = getattr(settings, 'VOLC_ASR_QUERY_ENDPOINT')
            except Exception:
                query_endpoint = None
            if not query_endpoint:
                se = submit_endpoint.rstrip('/')
                if se.endswith('/submit'):
                    query_endpoint = se[:-len('/submit')] + '/query'
                else:
                    query_endpoint = se + '/query'

            query_headers = {
                "Content-Type": "application/json",
                "X-Api-App-Key": settings.VOLC_ASR_APP_ID,
                "X-Api-Access-Key": settings.VOLC_ASR_TOKEN,
                "X-Api-Resource-Id": "volc.bigasr.auc",
                "X-Api-Request-Id": request_id,
            }

            last_raw_text = None
            last_data = None
            deadline = time.time() + 45.0
            while time.time() < deadline:
                q_resp = await client.post(query_endpoint, headers=query_headers, content=b"{}", timeout=60.0)
                last_raw_text = q_resp.text
                if q_resp.status_code != 200:
                    await asyncio.sleep(1.2)
                    continue
                try:
                    last_data = q_resp.json()
                except Exception:
                    last_data = {}

                parsed_text = None
                try:
                    result_obj = last_data.get("result")
                    if isinstance(result_obj, dict):
                        parsed_text = result_obj.get("text")
                        if not parsed_text:
                            utterances = result_obj.get("utterances") or []
                            if isinstance(utterances, list) and utterances:
                                parsed_text = "".join([u.get("text", "") for u in utterances if isinstance(u, dict)])
                    elif isinstance(result_obj, list) and result_obj:
                        first = result_obj[0]
                        if isinstance(first, dict):
                            parsed_text = first.get("text") or "".join([d.get("text", "") for d in result_obj if isinstance(d, dict)])
                except Exception:
                    parsed_text = None

                if parsed_text:
                    return {"text": parsed_text, "raw": last_data, "raw_text": last_raw_text}

                await asyncio.sleep(1.2)

            return {"text": None, "raw": last_data or {}, "raw_text": last_raw_text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AUC调用异常: {str(e)}")


class SubmitByKeyRequest(BaseModel):
    object_key: str
    language: Optional[str] = None
    fmt: Optional[str] = None


# 简单的连通性检查
@router.get("/ping")
async def ping():
    return {"status": "ok", "service": "voice"}


@router.get("/asr/upload_url")
async def asr_get_upload_url(
    fmt: str = "webm",
    current_user: User = Depends(get_current_user),
):
    if not (settings.TOS_ACCESS_KEY_ID and settings.TOS_SECRET_ACCESS_KEY and settings.TOS_BUCKET and settings.TOS_REGION and settings.TOS_ENDPOINT):
        raise HTTPException(status_code=500, detail="TOS 未配置完整")

    fmt = fmt or settings.VOLC_ASR_FORMAT or "webm"
    object_key = f"voice/{current_user.id}/{int(time.time()*1000)}-{uuid.uuid4().hex}.{fmt}"

    try:
        client = _get_tos_client()
        upload_url = _presign_url(client, 'PUT', settings.TOS_BUCKET, object_key, 600)
        if not upload_url:
            raise HTTPException(status_code=502, detail="获取上传URL失败")
        # 根据 fmt 推导 Content-Type
        content_type = "application/octet-stream"
        if fmt == "webm":
            content_type = "audio/webm"
        elif fmt in ("ogg", "opus"):
            content_type = "audio/ogg"
        return {"upload_url": upload_url, "object_key": object_key, "content_type": content_type}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TOS 预签名异常: {str(e)}")


@router.post("/asr/submit_by_key")
async def asr_submit_by_key(
    body: SubmitByKeyRequest,
    current_user: User = Depends(get_current_user),
):
    if not (settings.TOS_ACCESS_KEY_ID and settings.TOS_SECRET_ACCESS_KEY and settings.TOS_BUCKET and settings.TOS_REGION and settings.VOLC_ASR_ENDPOINT and settings.VOLC_ASR_APP_ID and settings.VOLC_ASR_TOKEN and settings.TOS_ENDPOINT):
        raise HTTPException(status_code=500, detail="TOS/ASR 未配置完整")

    language = _map_lang(body.language or settings.VOLC_ASR_LANGUAGE)
    fmt = body.fmt or settings.VOLC_ASR_FORMAT or "webm"

    try:
        client = _get_tos_client()
        signed_url = _presign_url(client, 'GET', settings.TOS_BUCKET, body.object_key, 600)
        if not signed_url:
            raise HTTPException(status_code=502, detail="获取下载URL失败")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TOS 预签名异常: {str(e)}")

    # 调用 AUC submit + query
    return await _auc_submit_and_query(signed_url, language, fmt, str(current_user.id))

@router.post("/asr/submit")
async def asr_submit(
    audio: UploadFile = File(...),
    language: str = Form(None),
    fmt: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    新版：接收音频，上传到 TOS 生成临时可访问 URL，调用 AUC 录音文件识别接口。
    需要 .env 配置 TOS 与 AUC 相关参数。
    """
    if not (settings.TOS_ACCESS_KEY_ID and settings.TOS_SECRET_ACCESS_KEY and settings.TOS_BUCKET and settings.TOS_REGION and settings.VOLC_ASR_ENDPOINT and settings.VOLC_ASR_APP_ID and settings.VOLC_ASR_TOKEN):
        raise HTTPException(status_code=500, detail="TOS/ASR 未配置完整")


    # 读取音频
    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="音频为空")

    language = _map_lang(language)
    fmt = fmt or settings.VOLC_ASR_FORMAT or "webm"

    # 步骤1：上传到 TOS
    key = f"voice/{current_user.id}/{int(time.time()*1000)}-{uuid.uuid4().hex}.{fmt}"
    try:
        endpoint = settings.TOS_ENDPOINT if settings.TOS_ENDPOINT.startswith("http") else f"https://{settings.TOS_ENDPOINT}"
        client = tos.TosClientV2(settings.TOS_ACCESS_KEY_ID, settings.TOS_SECRET_ACCESS_KEY, endpoint, settings.TOS_REGION)
        # 上传对象
        object_key = key
        content_type = "application/octet-stream"
        if fmt == "webm":
            content_type = "audio/webm"
        elif fmt in ("ogg", "opus"):
            content_type = "audio/ogg"

        put_result = client.put_object(settings.TOS_BUCKET, object_key, content=audio_bytes, content_type=content_type)
        if put_result.status_code not in (200, 204):
            raise HTTPException(status_code=502, detail=f"TOS 上传失败: status={put_result.status_code}")

        # 生成 10 分钟有效期的预签名下载链接
        # 预签名URL：不同 SDK 版本返回值与枚举名可能不同，这里做兼容处理
        method_enum = None
        try:
            # 常见枚举名称
            method_enum = getattr(tos.HttpMethodType, 'HTTP_GET', None) or getattr(tos.HttpMethodType, 'Http_Method_Get', None)
        except Exception:
            method_enum = None

        try:
            if method_enum is not None:
                pres = client.pre_signed_url(method_enum, settings.TOS_BUCKET, object_key, 600)
            else:
                pres = client.pre_signed_url('GET', settings.TOS_BUCKET, object_key, 600)
        except Exception:
            # 最后再退回字符串方式
            pres = client.pre_signed_url('GET', settings.TOS_BUCKET, object_key, 600)

        # 提取字符串 URL
        if isinstance(pres, str):
            signed_url = pres
        else:
            signed_url = getattr(pres, 'signed_url', None) or getattr(pres, 'url', None) or getattr(pres, 'presigned_url', None)
        if not signed_url:
            raise HTTPException(status_code=502, detail="TOS 预签名URL获取失败")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TOS SDK 异常: {str(e)}")
    
    print("signed_url:", signed_url)
    # 步骤2：调用 AUC 接口
    audio_codec = "opus" if fmt in ("ogg", "webm", "opus") else "raw"
    payload = {
        "user": {"uid": str(current_user.id)},
        "audio": {
            "format": fmt,
            "codec": audio_codec,
            "rate": 16000,
            "bits": 16,
            "channel": 1,
            "url": signed_url,
        },
        "language": language,
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True,
            "show_utterances": True,
        },
    }
    request_id = str(uuid.uuid4())
    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": settings.VOLC_ASR_APP_ID,
        "X-Api-Access-Key": settings.VOLC_ASR_TOKEN,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": request_id,
        "X-Api-Sequence": "-1",
    }
    try:
        async with httpx.AsyncClient() as client:
            # 明确以 raw JSON 字符串发送至 submit 接口
            import json as _json
            body = _json.dumps(payload, ensure_ascii=False)
            submit_endpoint = settings.VOLC_ASR_ENDPOINT
            resp = await client.post(submit_endpoint, headers=headers, content=body.encode('utf-8'), timeout=60.0)
            if resp.status_code != 200:
                # 将上游错误透传给前端，方便定位
                text = resp.text
                try:
                    j = resp.json()
                    text = j.get('message') or j.get('detail') or text
                except Exception:
                    pass
                raise HTTPException(status_code=resp.status_code, detail=f"ASR请求失败: {text}")

            # 根据文档：submit 只负责提交，需调用 query 查询结果
            # 推导 query 端点：优先读取配置，其次将 submit 替换为 query
            try:
                query_endpoint = getattr(settings, 'VOLC_ASR_QUERY_ENDPOINT')
            except Exception:
                query_endpoint = None
            if not query_endpoint:
                se = submit_endpoint.rstrip('/')
                if se.endswith('/submit'):
                    query_endpoint = se[:-len('/submit')] + '/query'
                else:
                    query_endpoint = se + '/query'

            # 轮询查询，直至拿到结果或超时
            query_headers = {
                "Content-Type": "application/json",
                "X-Api-App-Key": settings.VOLC_ASR_APP_ID,
                "X-Api-Access-Key": settings.VOLC_ASR_TOKEN,
                "X-Api-Resource-Id": "volc.bigasr.auc",
                "X-Api-Request-Id": request_id,
            }

            last_raw_text = None
            last_data = None
            deadline = time.time() + 45.0
            while time.time() < deadline:
                q_resp = await client.post(query_endpoint, headers=query_headers, content=b"{}", timeout=60.0)
                last_raw_text = q_resp.text
                if q_resp.status_code != 200:
                    # 查询未就绪时，服务可能返回非200或空体，等待重试
                    await asyncio.sleep(1.2)
                    continue
                try:
                    last_data = q_resp.json()
                except Exception:
                    last_data = {}

                # 解析结果：兼容 result 为对象或数组
                parsed_text = None
                try:
                    result_obj = last_data.get("result")
                    if isinstance(result_obj, dict):
                        parsed_text = result_obj.get("text")
                        if not parsed_text:
                            utterances = result_obj.get("utterances") or []
                            if isinstance(utterances, list) and utterances:
                                parsed_text = "".join([u.get("text", "") for u in utterances if isinstance(u, dict)])
                    elif isinstance(result_obj, list) and result_obj:
                        first = result_obj[0]
                        if isinstance(first, dict):
                            parsed_text = first.get("text") or "".join([d.get("text", "") for d in result_obj if isinstance(d, dict)])
                except Exception:
                    parsed_text = None

                if parsed_text:
                    return {"text": parsed_text, "raw": last_data, "raw_text": last_raw_text}

                await asyncio.sleep(1.2)

            # 超时仍无结果
            return {"text": None, "raw": last_data or {}, "raw_text": last_raw_text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AUC调用异常: {str(e)}")

