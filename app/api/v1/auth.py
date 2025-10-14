"""
认证相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.user import UserCreate, User
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.services.user_service import (
    create_user,
    get_user_by_username,
    get_user_by_email,
    get_user_by_id
)
from app.services.auth_service import authenticate_user, generate_tokens
from app.core.security import decode_token
from app.models.user import User as UserModel


router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    用户注册
    
    - **username**: 用户名（3-50字符，唯一）
    - **email**: 邮箱（唯一）
    - **password**: 密码（至少6字符）
    """
    # 检查用户名是否已存在
    if get_user_by_username(db, user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被使用"
        )
    
    # 检查邮箱是否已存在
    if get_user_by_email(db, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被使用"
        )
    
    # 创建用户
    user = create_user(db, user_create)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="用户创建失败"
        )
    
    return user


@router.post("/login", response_model=Token)
async def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    用户登录
    
    - **username**: 用户名
    - **password**: 密码
    
    返回访问令牌和刷新令牌
    """
    # 验证用户
    user = authenticate_user(db, login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成令牌
    tokens = generate_tokens(user.id)
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    刷新访问令牌
    
    - **refresh_token**: 刷新令牌
    
    返回新的访问令牌和刷新令牌
    """
    # 解码刷新令牌
    payload = decode_token(refresh_request.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查令牌类型
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌类型错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证用户是否存在且激活
    user = get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成新令牌
    tokens = generate_tokens(user.id)
    return tokens


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    """
    获取当前登录用户信息
    
    需要在请求头中携带访问令牌：
    Authorization: Bearer <access_token>
    """
    return current_user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_user: UserModel = Depends(get_current_user)
):
    """
    用户登出
    
    注意：由于使用JWT，服务端无需维护会话状态。
    客户端应删除本地存储的token。
    """
    return {
        "message": "登出成功",
        "detail": "请在客户端删除token"
    }

