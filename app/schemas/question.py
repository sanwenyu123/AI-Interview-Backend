"""
问题相关模式
"""
from pydantic import BaseModel, Field
from datetime import datetime


class QuestionBase(BaseModel):
    """问题基础模式"""
    question_text: str = Field(..., min_length=10)
    question_order: int = Field(..., ge=1)
    language: str = Field("zh-CN", min_length=2, max_length=10)


class QuestionCreate(QuestionBase):
    """问题创建模式"""
    interview_id: int


class Question(QuestionBase):
    """问题响应模式"""
    id: int
    interview_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

