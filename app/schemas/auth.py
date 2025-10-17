"""
认证相关模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.user import User


class Token(BaseModel):
    """令牌响应模式"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: User  # 添加用户信息


class TokenPayload(BaseModel):
    """令牌负载模式"""
    sub: Optional[int] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    """登录请求模式"""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求模式"""
    refresh_token: str

