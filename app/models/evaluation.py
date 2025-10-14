"""
评价模型
"""
from sqlalchemy import Column, Integer, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Evaluation(Base):
    """评价表"""
    
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)
    overall_score = Column(Integer, nullable=False)
    technical_score = Column(Integer, nullable=False)
    communication_score = Column(Integer, nullable=False)
    experience_score = Column(Integer, nullable=False)
    learning_score = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=False)
    suggestions = Column(JSON, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    
    # 关系
    interview = relationship("Interview", back_populates="evaluation")
    
    def __repr__(self):
        return f"<Evaluation(id={self.id}, interview_id={self.interview_id}, score={self.overall_score})>"

