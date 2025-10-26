"""
FastAPI主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.core.database import init_db

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    description="AI模拟面试平台后端API"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"启动 {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("初始化数据库...")
    try:
        init_db()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info(f"关闭 {settings.APP_NAME}")


@app.get("/")
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": settings.DOCS_URL,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "app": settings.APP_NAME}
    )


# 导入并注册路由
from app.api.v1 import auth, interviews, questions, answers, evaluations
from app.api.v1 import voice

app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["认证"])
app.include_router(interviews.router, prefix=f"{settings.API_V1_PREFIX}/interviews", tags=["面试管理"])
app.include_router(questions.router, prefix=f"{settings.API_V1_PREFIX}/questions", tags=["问题管理"])
app.include_router(answers.router, prefix=f"{settings.API_V1_PREFIX}/answers", tags=["答案管理"])
app.include_router(evaluations.router, prefix=f"{settings.API_V1_PREFIX}/evaluations", tags=["评价管理"])
app.include_router(voice.router, prefix=f"{settings.API_V1_PREFIX}/voice", tags=["语音"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

