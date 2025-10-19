"""
面试相关模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DifficultyEnum(str, Enum):
    """难度枚举"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class InterviewTypeEnum(str, Enum):
    """面试类型枚举"""
    TEXT = "text"
    VOICE = "voice"


class InterviewStatusEnum(str, Enum):
    """面试状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InterviewBase(BaseModel):
    """面试基础模式"""
    position: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    skills: Optional[List[str]] = []
    difficulty: DifficultyEnum = DifficultyEnum.MEDIUM
    duration: int = Field(30, ge=15, le=120)
    language: str = Field("zh-CN", min_length=2, max_length=10)
    type: InterviewTypeEnum = InterviewTypeEnum.TEXT


class InterviewCreate(InterviewBase):
    """面试创建模式"""
    pass


class InterviewUpdate(BaseModel):
    """面试更新模式"""
    status: Optional[InterviewStatusEnum] = None
    score: Optional[int] = Field(None, ge=0, le=100)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Interview(InterviewBase):
    """面试响应模式"""
    id: int
    user_id: int
    status: InterviewStatusEnum
    score: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class InterviewWithDetails(Interview):
    """包含详情的面试模式"""
    question_count: int = 0
    answer_count: int = 0
    
    class Config:
        from_attributes = True




