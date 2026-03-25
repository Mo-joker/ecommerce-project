# backend/app/api/v1/__init__.py
"""
API v1 路由
"""
from . import auth
from . import users
from . import products
from . import orders

# 可以在这里统一导出路由
__all__ = ["auth", "users", "products", "orders"]