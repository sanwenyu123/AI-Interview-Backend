"""
问题模型
"""
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Question(Base):
    """问题表"""
    
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_order = Column(Integer, nullable=False)
    language = Column(String(10), nullable=False, default="zh-CN")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    
    # 关系
    interview = relationship("Interview", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Question(id={self.id}, interview_id={self.interview_id}, order={self.question_order})>"

