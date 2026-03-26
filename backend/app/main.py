# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 导入 API v1 路由
from .api.v1.auth import router as auth_router
from .api.v1.users import router as users_router
from .api.v1.products import router as products_router
from .api.v1.orders import router as orders_router
from .api.v1.cart import router as cart_router

# 创建 FastAPI 实例
app = FastAPI(
    title="电商商城 API",
    description="电商项目后端接口文档",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS - 允许所有来源（开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vue 开发服务器
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # 开发环境允许所有来源
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
    expose_headers=["*"]
)

# 注册路由
app.include_router(auth_router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users_router, prefix="/api/v1/users", tags=["用户"])
app.include_router(products_router, prefix="/api/v1/products", tags=["商品"])
app.include_router(orders_router, prefix="/api/v1/orders", tags=["订单"])
app.include_router(cart_router, prefix="/api/v1/cart", tags=["购物车"])

@app.get("/")
async def root():
    return {
        "message": "电商商城 API 服务",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ecommerce-backend"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )