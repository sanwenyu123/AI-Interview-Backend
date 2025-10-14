"""
用户服务
处理用户相关的业务逻辑
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.setting import Setting
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    根据ID获取用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        Optional[User]: 用户对象或None
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    根据用户名获取用户
    
    Args:
        db: 数据库会话
        username: 用户名
        
    Returns:
        Optional[User]: 用户对象或None
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    根据邮箱获取用户
    
    Args:
        db: 数据库会话
        email: 邮箱
        
    Returns:
        Optional[User]: 用户对象或None
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_create: UserCreate) -> Optional[User]:
    """
    创建新用户
    
    Args:
        db: 数据库会话
        user_create: 用户创建数据
        
    Returns:
        Optional[User]: 创建的用户对象或None（如果用户名/邮箱已存在）
    """
    try:
        # 创建用户
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            is_active=True
        )
        db.add(db_user)
        db.flush()  # 获取用户ID
        
        # 创建默认设置
        default_setting = Setting(
            user_id=db_user.id,
            language="zh-CN",
            voice_type="default",
            auto_save=True,
            speech_recognition_quality="high"
        )
        db.add(default_setting)
        
        db.commit()
        db.refresh(db_user)
        return db_user
        
    except IntegrityError:
        db.rollback()
        return None


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    更新用户信息
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        user_update: 用户更新数据
        
    Returns:
        Optional[User]: 更新后的用户对象或None
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    # 更新字段
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None


def delete_user(db: Session, user_id: int) -> bool:
    """
    删除用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        bool: 是否删除成功
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def deactivate_user(db: Session, user_id: int) -> Optional[User]:
    """
    禁用用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        Optional[User]: 禁用后的用户对象或None
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(db: Session, user_id: int) -> Optional[User]:
    """
    激活用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        Optional[User]: 激活后的用户对象或None
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return db_user

