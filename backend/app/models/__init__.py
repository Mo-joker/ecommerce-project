# backend/app/models/__init__.py
from .users import User
from .product import Product, Category
from .orders import Order, OrderItem, CartItem, OrderStatus

# 确保所有模型都被导入，这样 Base.metadata 才能识别它们
__all__ = ["User", "Product", "Category", "Order", "OrderItem", "CartItem", "OrderStatus"]