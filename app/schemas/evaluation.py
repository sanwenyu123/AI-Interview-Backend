"""
评价相关模式
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class EvaluationBase(BaseModel):
    """评价基础模式"""
    overall_score: int = Field(..., ge=0, le=100)
    technical_score: int = Field(..., ge=0, le=100)
    communication_score: int = Field(..., ge=0, le=100)
    experience_score: int = Field(..., ge=0, le=100)
    learning_score: int = Field(..., ge=0, le=100)
    feedback: str = Field(..., min_length=10)
    suggestions: Optional[List[str]] = []
    strengths: Optional[List[str]] = []
    weaknesses: Optional[List[str]] = []


class EvaluationCreate(EvaluationBase):
    """评价创建模式"""
    interview_id: int


class Evaluation(EvaluationBase):
    """评价响应模式"""
    id: int
    interview_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True




