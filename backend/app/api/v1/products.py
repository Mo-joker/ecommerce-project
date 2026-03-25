# backend/app/api/v1/products.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...models.product import Product, Category
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: Optional[int] = None
    images: Optional[List[str]] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    size: int
    pages: int


# backend/app/api/v1/products.py 中的 get_products 函数
@router.get("/")
async def get_products(
        skip: int = Query(0, ge=0),
        limit: int = Query(12, ge=1, le=100),
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """获取商品列表"""
    query = db.query(Product).filter(Product.is_active == True)

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if search:
        query = query.filter(
            Product.name.contains(search) | Product.description.contains(search)
        )

    # 获取总数
    total = query.count()

    # 排序
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.id.desc())

    # 分页
    products = query.offset(skip).limit(limit).all()

    # 返回分页格式
    return {
        "items": products,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取商品详情"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product


@router.get("/categories/")
async def get_categories(db: Session = Depends(get_db)):
    """获取所有分类"""
    categories = db.query(Category).filter(Category.parent_id.is_(None)).all()
    return categories