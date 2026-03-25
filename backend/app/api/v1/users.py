# backend/app/api/v1/users.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...models.users import User
from pydantic import BaseModel

router = APIRouter()

class UserProfile(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None

@router.get("/me")
async def get_user_profile(db: Session = Depends(get_db)):
    """获取当前用户信息"""
    # 临时返回，后续接入认证
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "测试用户"
    }

@router.put("/me")
async def update_user_profile(profile: UserProfile):
    """更新用户信息"""
    return {"message": "更新成功", "data": profile}

@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    """根据ID获取用户信息"""
    return {
        "id": user_id,
        "username": f"user_{user_id}",
        "email": f"user{user_id}@example.com"
    }