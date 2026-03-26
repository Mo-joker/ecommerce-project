# backend/app/api/v1/orders.py
from fastapi import APIRouter, HTTPException, Depends, Header, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from jose import jwt, JWTError
from ...core.database import get_db
from ...models.orders import Order, OrderItem, OrderStatus
from ...models.users import User
from ...models.product import Product
from ...core.config import settings
from pydantic import BaseModel

router = APIRouter()


class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int
    total_price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    items: List[OrderItemResponse]
    total_amount: float
    status: str
    address: str
    phone: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[dict]
    total_amount: float
    address: str
    phone: str


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


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """创建订单"""
    # 生成订单号
    order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{current_user.id}"
    
    # 创建订单
    order = Order(
        order_number=order_number,
        user_id=current_user.id,
        total_amount=order_data.total_amount,
        status="pending",
        address=order_data.address,
        phone=order_data.phone
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # 创建订单项
    for item_data in order_data.items:
        # 验证商品是否存在
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品 {item_data['product_id']} 不存在")
        
        # 计算小计
        item_quantity = item_data.get("quantity", 1)
        item_price = item_data.get("price", product.price)
        item_total = item_price * item_quantity
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["product_id"],
            product_name=product.name,
            product_price=item_price,
            quantity=item_quantity,
            total_price=item_total
        )
        db.add(order_item)
    
    db.commit()
    
    # 重新加载订单和订单项
    db.refresh(order)
    
    # 手动构建响应数据
    items_response = []
    for item in order.items:
        items_response.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "price": item.product_price,
            "quantity": item.quantity,
            "total_price": item.total_price
        })
    
    return {
        "id": order.id,
        "order_number": order.order_number,
        "user_id": order.user_id,
        "items": items_response,
        "total_amount": order.total_amount,
        "status": order.status.value,
        "address": order.address,
        "phone": order.phone,
        "created_at": order.created_at
    }


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    status: Optional[str] = Query(None, description="订单状态筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """获取当前用户的订单列表（支持按状态筛选）"""
    # 基础查询：只查询当前用户的订单
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    # 如果指定了状态，则按状态筛选
    if status:
        print(f"筛选状态：{status}")  # 调试日志
        query = query.filter(Order.status == status)
    
    # 按创建时间倒序
    orders = query.order_by(Order.created_at.desc()).all()
    
    print(f"查询到 {len(orders)} 个订单")  # 调试日志
    
    # 手动转换数据以匹配响应模型
    result = []
    for order in orders:
        items_response = []
        for item in order.items:
            # 确保 price 不为 None
            price = float(item.product_price) if item.product_price else 0.0
            total_price = float(item.total_price) if item.total_price else 0.0
            
            items_response.append({
                "id": item.id,
                "product_id": item.product_id,
                "product_name": str(item.product_name) if item.product_name else "",
                "price": price,
                "quantity": int(item.quantity) if item.quantity else 0,
                "total_price": total_price
            })
        
        result.append({
            "id": order.id,
            "order_number": str(order.order_number),
            "user_id": order.user_id,
            "items": items_response,
            "total_amount": float(order.total_amount) if order.total_amount else 0.0,
            "status": str(order.status.value) if order.status else "pending",
            "address": str(order.address) if order.address else "",
            "phone": str(order.phone) if order.phone else "",
            "created_at": order.created_at
        })
    
    return result


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """获取订单详情（只能查看自己的订单）"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 手动转换数据以匹配响应模型
    items_response = []
    for item in order.items:
        # 确保 price 不为 None
        price = float(item.product_price) if item.product_price else 0.0
        total_price = float(item.total_price) if item.total_price else 0.0
        
        items_response.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": str(item.product_name) if item.product_name else "",
            "price": price,
            "quantity": int(item.quantity) if item.quantity else 0,
            "total_price": total_price
        })
    
    return {
        "id": order.id,
        "order_number": str(order.order_number),
        "user_id": order.user_id,
        "items": items_response,
        "total_amount": float(order.total_amount) if order.total_amount else 0.0,
        "status": str(order.status.value) if order.status else "pending",
        "address": str(order.address) if order.address else "",
        "phone": str(order.phone) if order.phone else "",
        "created_at": order.created_at
    }


@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """更新订单状态（仅管理员）"""
    # 检查是否是管理员
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="只有管理员可以更新订单状态")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    order.status = status
    db.commit()
    db.refresh(order)
    
    # 手动构建响应数据
    items_response = []
    for item in order.items:
        price = float(item.product_price) if item.product_price else 0.0
        total_price = float(item.total_price) if item.total_price else 0.0
        
        items_response.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": str(item.product_name) if item.product_name else "",
            "price": price,
            "quantity": int(item.quantity) if item.quantity else 0,
            "total_price": total_price
        })
    
    return {
        "message": "订单状态更新成功",
        "order": {
            "id": order.id,
            "order_number": str(order.order_number),
            "user_id": order.user_id,
            "items": items_response,
            "total_amount": float(order.total_amount) if order.total_amount else 0.0,
            "status": str(order.status.value) if order.status else "pending",
            "address": str(order.address) if order.address else "",
            "phone": str(order.phone) if order.phone else "",
            "created_at": order.created_at
        }
    }


@router.put("/{order_id}/cancel", response_model=dict)
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """取消订单（用户只能取消自己的待支付订单）"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="只能取消待支付的订单")
    
    order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    
    return {"message": "订单已取消"}


@router.put("/{order_id}/pay", response_model=dict)
async def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """支付订单（用户只能支付自己的待支付订单）"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="只能支付待支付的订单")
    
    order.status = OrderStatus.PAID
    db.commit()
    db.refresh(order)
    
    return {"message": "支付成功"}
