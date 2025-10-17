"""
面试管理API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.interview import InterviewStatusEnum
from app.schemas.interview import Interview, InterviewCreate, InterviewUpdate, InterviewWithDetails
from app.services.interview_service import (
    create_interview,
    get_interview_by_id,
    get_user_interviews,
    update_interview,
    delete_interview,
    start_interview,
    complete_interview,
    cancel_interview,
    get_interview_statistics
)


router = APIRouter()


@router.post("/", response_model=Interview, status_code=status.HTTP_201_CREATED)
async def create_new_interview(
    interview_create: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建新的面试记录

    - **position**: 岗位名称
    - **description**: 岗位描述（可选）
    - **skills**: 技能列表
    - **difficulty**: 难度（easy/medium/hard/expert）
    - **duration**: 面试时长（分钟，15-120）
    - **language**: 语言代码
    - **type**: 面试类型（text/voice）
    """
    interview = create_interview(db, current_user.id, interview_create)
    return interview


@router.get("/", response_model=List[Interview])
async def get_interviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[InterviewStatusEnum] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的面试列表

    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    - **status**: 筛选状态（可选）
    """
    interviews = get_user_interviews(db, current_user.id, skip, limit, status)
    return interviews


@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的面试统计数据

    返回：
    - total_count: 总面试次数
    - completed_count: 已完成次数
    - in_progress_count: 进行中次数
    - average_score: 平均分数
    """
    statistics = get_interview_statistics(db, current_user.id)
    return statistics


@router.get("/{interview_id}", response_model=Interview)
async def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取面试详情

    - **interview_id**: 面试ID
    """
    interview = get_interview_by_id(db, interview_id)

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )

    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此面试记录"
        )

    return interview


@router.put("/{interview_id}", response_model=Interview)
async def update_interview_info(
    interview_id: int,
    interview_update: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新面试记录

    - **interview_id**: 面试ID
    - 可更新字段：status, score, started_at, completed_at
    """
    interview = get_interview_by_id(db, interview_id)

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )

    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此面试记录"
        )

    updated_interview = update_interview(db, interview_id, interview_update)
    return updated_interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interview_record(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除面试记录

    - **interview_id**: 面试ID
    """
    interview = get_interview_by_id(db, interview_id)

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )

    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此面试记录"
        )

    delete_interview(db, interview_id)
    return None


@router.post("/{interview_id}/start", response_model=Interview)
async def start_interview_session(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    开始面试

    - **interview_id**: 面试ID
    - 将状态从 pending 改为 in_progress
    - 记录开始时间
    """
    interview = get_interview_by_id(db, interview_id)

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )

    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此面试记录"
        )

    # 开始面试
    started_interview = start_interview(db, interview_id)
    if not started_interview:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法开始面试，请检查面试状态"
        )

    return started_interview


@router.post("/{interview_id}/complete", response_model=Interview)
async def complete_interview_session(
    interview_id: int,
    score: Optional[int] = Query(None, ge=0, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    完成面试

    - **interview_id**: 面试ID
    - **score**: 面试分数（可选，0-100）
    - 将状态从 in_progress 改为 completed
    - 记录完成时间
    """
    interview = get_interview_by_id(db, interview_id)

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )

    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此面试记录"
        )

    # 完成面试
    completed_interview = complete_interview(db, interview_id, score)
    if not completed_interview:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法完成面试，请检查面试状态"
        )

    return completed_interview


@router.post("/{interview_id}/cancel", response_model=Interview)
async def cancel_interview_session(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    取消面试

    - **interview_id**: 面试ID
    - 将状态改为 cancelled
    """
    interview = get_interview_by_id(db, interview_id)

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )

    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此面试记录"
        )

    # 取消面试
    cancelled_interview = cancel_interview(db, interview_id)
    return cancelled_interview

