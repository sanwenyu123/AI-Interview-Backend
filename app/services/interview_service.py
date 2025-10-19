"""
面试服务
处理面试相关的业务逻辑
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.interview import Interview, InterviewStatusEnum
from app.models.question import Question
from app.models.answer import Answer
from app.models.evaluation import Evaluation
from app.schemas.interview import InterviewCreate, InterviewUpdate


def create_interview(db: Session, user_id: int, interview_create: InterviewCreate) -> Interview:
    """
    创建面试记录

    Args:
        db: 数据库会话
        user_id: 用户ID
        interview_create: 面试创建数据

    Returns:
        Interview: 创建的面试对象
    """
    db_interview = Interview(
        user_id=user_id,
        position=interview_create.position,
        description=interview_create.description,
        skills=interview_create.skills,
        difficulty=interview_create.difficulty,
        duration=interview_create.duration,
        language=interview_create.language,
        type=interview_create.type,
        status=InterviewStatusEnum.PENDING
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview


def get_interview_by_id(db: Session, interview_id: int) -> Optional[Interview]:
    """
    根据ID获取面试记录

    Args:
        db: 数据库会话
        interview_id: 面试ID

    Returns:
        Optional[Interview]: 面试对象或None
    """
    return db.query(Interview).filter(Interview.id == interview_id).first()


def get_user_interviews(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[InterviewStatusEnum] = None
) -> List[Interview]:
    """
    获取用户的面试列表

    Args:
        db: 数据库会话
        user_id: 用户ID
        skip: 跳过的记录数
        limit: 返回的最大记录数
        status: 筛选的状态（可选）

    Returns:
        List[Interview]: 面试列表
    """
    query = db.query(Interview).filter(Interview.user_id == user_id)

    if status:
        query = query.filter(Interview.status == status)

    return query.order_by(desc(Interview.created_at)).offset(skip).limit(limit).all()


def update_interview(
    db: Session,
    interview_id: int,
    interview_update: InterviewUpdate
) -> Optional[Interview]:
    """
    更新面试记录

    Args:
        db: 数据库会话
        interview_id: 面试ID
        interview_update: 更新数据

    Returns:
        Optional[Interview]: 更新后的面试对象或None
    """
    db_interview = get_interview_by_id(db, interview_id)
    if not db_interview:
        return None

    # 更新字段
    update_data = interview_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_interview, field, value)

    db.commit()
    db.refresh(db_interview)
    return db_interview


def delete_interview(db: Session, interview_id: int) -> bool:
    """
    删除面试记录

    Args:
        db: 数据库会话
        interview_id: 面试ID

    Returns:
        bool: 是否删除成功
    """
    db_interview = get_interview_by_id(db, interview_id)
    if not db_interview:
        return False

    db.delete(db_interview)
    db.commit()
    return True


def start_interview(db: Session, interview_id: int) -> Optional[Interview]:
    """
    开始面试

    Args:
        db: 数据库会话
        interview_id: 面试ID

    Returns:
        Optional[Interview]: 更新后的面试对象或None
    """
    db_interview = get_interview_by_id(db, interview_id)
    if not db_interview:
        return None

    if db_interview.status != InterviewStatusEnum.PENDING:
        return None

    db_interview.status = InterviewStatusEnum.IN_PROGRESS
    db_interview.started_at = datetime.utcnow()

    db.commit()
    db.refresh(db_interview)
    return db_interview


def complete_interview(db: Session, interview_id: int, score: Optional[int] = None) -> Optional[Interview]:
    """
    完成面试

    Args:
        db: 数据库会话
        interview_id: 面试ID
        score: 面试分数（可选）

    Returns:
        Optional[Interview]: 更新后的面试对象或None
    """
    db_interview = get_interview_by_id(db, interview_id)
    if not db_interview:
        return None

    if db_interview.status != InterviewStatusEnum.IN_PROGRESS:
        return None

    db_interview.status = InterviewStatusEnum.COMPLETED
    db_interview.completed_at = datetime.utcnow()
    if score is not None:
        db_interview.score = score

    db.commit()
    db.refresh(db_interview)
    return db_interview


def cancel_interview(db: Session, interview_id: int) -> Optional[Interview]:
    """
    取消面试

    Args:
        db: 数据库会话
        interview_id: 面试ID

    Returns:
        Optional[Interview]: 更新后的面试对象或None
    """
    db_interview = get_interview_by_id(db, interview_id)
    if not db_interview:
        return None

    db_interview.status = InterviewStatusEnum.CANCELLED

    db.commit()
    db.refresh(db_interview)
    return db_interview


def get_interview_statistics(db: Session, user_id: int) -> dict:
    """
    获取用户的面试统计数据

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        dict: 统计数据
    """
    # 总面试次数
    total_count = db.query(Interview).filter(Interview.user_id == user_id).count()

    # 已完成次数
    completed_count = db.query(Interview).filter(
        Interview.user_id == user_id,
        Interview.status == InterviewStatusEnum.COMPLETED
    ).count()

    # 平均分数
    avg_score_result = db.query(Interview).filter(
        Interview.user_id == user_id,
        Interview.status == InterviewStatusEnum.COMPLETED,
        Interview.score.isnot(None)
    ).all()

    avg_score = 0
    if avg_score_result:
        scores = [interview.score for interview in avg_score_result if interview.score]
        avg_score = sum(scores) / len(scores) if scores else 0

    return {
        "total_count": total_count,
        "completed_count": completed_count,
        "in_progress_count": db.query(Interview).filter(
            Interview.user_id == user_id,
            Interview.status == InterviewStatusEnum.IN_PROGRESS
        ).count(),
        "average_score": round(avg_score, 2)
    }





