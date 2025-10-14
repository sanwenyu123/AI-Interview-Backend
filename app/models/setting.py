"""
用户设置模型
"""
from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class SpeechQualityEnum(str, enum.Enum):
    """语音识别质量枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Setting(Base):
    """用户设置表"""
    
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)
    language = Column(String(10), nullable=False, default="zh-CN")
    voice_type = Column(String(50), nullable=False, default="default")
    auto_save = Column(Boolean, nullable=False, default=True)
    speech_recognition_quality = Column(SQLEnum(SpeechQualityEnum), nullable=False, default=SpeechQualityEnum.HIGH)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    user = relationship("User", back_populates="setting")
    
    def __repr__(self):
        return f"<Setting(id={self.id}, user_id={self.user_id}, language='{self.language}')>"

