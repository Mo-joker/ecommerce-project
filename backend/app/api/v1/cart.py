# backend/app/api/v1/cart.py
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import jwt, JWTError
from ...core.database import get_db
from ...models.orders import CartItem
from ...models.product import Product
from ...models.users import User
from ...core.config import settings
from pydantic import BaseModel

router = APIRouter()


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    product_image: Optional[str] = None
    quantity: int

    class Config:
        from_attributes = True


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


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


@router.get("", response_model=List[CartItemResponse])
async def get_cart_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """获取当前用户的购物车列表"""
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    
    # 构建响应数据
    result = []
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product_image = None
            if product.images and isinstance(product.images, list) and len(product.images) > 0:
                product_image = product.images[0]
            
            result.append({
                "id": item.id,
                "product_id": item.product_id,
                "product_name": product.name,
                "product_price": product.price,
                "product_image": product_image,
                "quantity": item.quantity
            })
    
    return result


@router.post("", response_model=CartItemResponse)
async def add_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """添加商品到购物车"""
    # 验证商品是否存在
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    # 检查是否已在购物车中
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item_data.product_id
    ).first()
    
    if cart_item:
        # 已存在则增加数量
        cart_item.quantity += item_data.quantity
    else:
        # 不存在则创建新记录
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    
    # 返回响应数据
    product_image = None
    if product.images and isinstance(product.images, list) and len(product.images) > 0:
        product_image = product.images[0]
    
    return {
        "id": cart_item.id,
        "product_id": cart_item.product_id,
        "product_name": product.name,
        "product_price": product.price,
        "product_image": product_image,
        "quantity": cart_item.quantity
    }


@router.put("/{item_id}")
async def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """更新购物车商品数量"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="购物车记录不存在")
    
    if item_data.quantity <= 0:
        # 数量为 0 或删除操作
        db.delete(cart_item)
        db.commit()
        return {"message": "商品已从购物车移除"}
    
    cart_item.quantity = item_data.quantity
    db.commit()
    db.refresh(cart_item)
    
    return {"message": "更新成功", "quantity": cart_item.quantity}


@router.delete("/{item_id}")
async def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """从购物车移除商品"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="购物车记录不存在")
    
    db.delete(cart_item)
    db.commit()
    
    return {"message": "商品已从购物车移除"}


@router.delete("")
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """清空购物车"""
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    
    return {"message": "购物车已清空"}
