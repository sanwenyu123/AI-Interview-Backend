"""
用户模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """用户表"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    interviews = relationship("Interview", back_populates="user", cascade="all, delete-orphan")
    setting = relationship("Setting", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

