"""
回答模型
"""
from sqlalchemy import Column, Integer, Text, String, Enum as SQLEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class AnswerTypeEnum(str, enum.Enum):
    """回答类型枚举"""
    TEXT = "text"
    VOICE = "voice"


class Answer(Base):
    """回答表"""
    
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)
    answer_text = Column(Text, nullable=False)
    answer_type = Column(SQLEnum(AnswerTypeEnum), nullable=False, default=AnswerTypeEnum.TEXT)
    audio_url = Column(String(255), nullable=True)
    duration = Column(Integer, nullable=True)  # 秒
    created_at = Column(DateTime, server_default=func.current_timestamp())
    
    # 关系
    question = relationship("Question", back_populates="answer")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, question_id={self.question_id}, type='{self.answer_type}')>"

