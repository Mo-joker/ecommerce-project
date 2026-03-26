# backend/app/api/v1/users.py
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from jose import jwt, JWTError
from ...core.database import get_db
from ...models.users import User
from ...core.config import settings
from pydantic import BaseModel

router = APIRouter()

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar: Optional[str] = None

async def get_current_user_from_token(
    authorization: str | None = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """从 token 获取当前用户"""
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少认证凭证")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(status_code=401, detail="无效的认证格式")
    
    token = parts[1]
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的认证凭证")
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的认证凭证")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return user

@router.get("/me")
async def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """获取当前用户信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active
    }

@router.put("/me")
async def update_user_profile(
    profile: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """更新用户信息"""
    # 只允许更新 full_name 和 avatar
    if profile.full_name is not None:
        current_user.full_name = profile.full_name
    
    if profile.avatar is not None:
        current_user.avatar = profile.avatar
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "更新成功",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "avatar": current_user.avatar,
            "is_admin": current_user.is_admin,
            "is_active": current_user.is_active
        }
    }

@router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name
    }