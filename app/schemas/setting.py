"""
设置相关模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class SpeechQualityEnum(str, Enum):
    """语音识别质量枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SettingBase(BaseModel):
    """设置基础模式"""
    language: str = Field("zh-CN", min_length=2, max_length=10)
    voice_type: str = Field("default", min_length=1, max_length=50)
    auto_save: bool = True
    speech_recognition_quality: SpeechQualityEnum = SpeechQualityEnum.HIGH


class SettingCreate(SettingBase):
    """设置创建模式"""
    pass


class SettingUpdate(BaseModel):
    """设置更新模式"""
    language: Optional[str] = Field(None, min_length=2, max_length=10)
    voice_type: Optional[str] = Field(None, min_length=1, max_length=50)
    auto_save: Optional[bool] = None
    speech_recognition_quality: Optional[SpeechQualityEnum] = None


class Setting(SettingBase):
    """设置响应模式"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

