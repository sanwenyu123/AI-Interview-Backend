"""
面试记录模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, Enum as SQLEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class DifficultyEnum(str, enum.Enum):
    """难度枚举"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class InterviewTypeEnum(str, enum.Enum):
    """面试类型枚举"""
    TEXT = "text"
    VOICE = "voice"


class InterviewStatusEnum(str, enum.Enum):
    """面试状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Interview(Base):
    """面试记录表"""
    
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    position = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    skills = Column(JSON, nullable=True)
    difficulty = Column(SQLEnum(DifficultyEnum), nullable=False, default=DifficultyEnum.MEDIUM)
    duration = Column(Integer, nullable=False)  # 分钟
    language = Column(String(10), nullable=False, default="zh-CN")
    type = Column(SQLEnum(InterviewTypeEnum), nullable=False, default=InterviewTypeEnum.TEXT)
    status = Column(SQLEnum(InterviewStatusEnum), nullable=False, default=InterviewStatusEnum.PENDING)
    score = Column(Integer, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    
    # 关系
    user = relationship("User", back_populates="interviews")
    questions = relationship("Question", back_populates="interview", cascade="all, delete-orphan")
    evaluation = relationship("Evaluation", back_populates="interview", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Interview(id={self.id}, position='{self.position}', status='{self.status}')>"

