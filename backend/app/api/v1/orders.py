# backend/app/api/v1/orders.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...core.database import get_db
from ...models.orders import Order, OrderItem, OrderStatus
from pydantic import BaseModel

router = APIRouter()


# 定义响应模型（这是 Pydantic 模型，不是数据库模型）
class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int
    total_price: float


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


# 临时存储（开发用）
fake_orders = []


@router.post("/", response_model=OrderResponse)
async def create_order(order_data: OrderCreate):
    """创建订单"""
    order_id = len(fake_orders) + 1
    order = {
        "id": order_id,
        "order_number": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{order_id}",
        "user_id": 1,
        "items": order_data.items,
        "total_amount": order_data.total_amount,
        "status": "pending",
        "address": order_data.address,
        "phone": order_data.phone,
        "created_at": datetime.now()
    }
    fake_orders.append(order)
    return order


@router.get("/", response_model=List[OrderResponse])
async def get_orders():
    """获取订单列表"""
    return fake_orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    """获取订单详情"""
    for order in fake_orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="订单不存在")


@router.put("/{order_id}/status")
async def update_order_status(order_id: int, status: str):
    """更新订单状态"""
    for order in fake_orders:
        if order["id"] == order_id:
            order["status"] = status
            return {"message": "订单状态更新成功", "order": order}
    raise HTTPException(status_code=404, detail="订单不存在")