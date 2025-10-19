"""
回答相关模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AnswerTypeEnum(str, Enum):
    """回答类型枚举"""
    TEXT = "text"
    VOICE = "voice"


class AnswerBase(BaseModel):
    """回答基础模式"""
    answer_text: str = Field(..., min_length=1)
    answer_type: AnswerTypeEnum = AnswerTypeEnum.TEXT
    audio_url: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)


class AnswerCreate(AnswerBase):
    """回答创建模式"""
    question_id: int


class Answer(AnswerBase):
    """回答响应模式"""
    id: int
    question_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True




