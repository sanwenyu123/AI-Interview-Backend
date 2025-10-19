"""
认证服务
处理用户认证相关的业务逻辑
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.services.user_service import get_user_by_username


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    验证用户凭据

    Args:
        db: 数据库会话
        username: 用户名
        password: 密码

    Returns:
        Optional[User]: 验证成功返回用户对象，否则返回None
    """
    user = get_user_by_username(db, username)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user


def generate_tokens(user_id: int) -> dict:
    """
    为用户生成访问令牌和刷新令牌

    Args:
        user_id: 用户ID

    Returns:
        dict: 包含access_token和refresh_token的字典
    """
    access_token = create_access_token(subject=user_id)
    refresh_token = create_refresh_token(subject=user_id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




