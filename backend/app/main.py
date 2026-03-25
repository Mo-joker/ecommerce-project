# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 导入 API v1 路由
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.products import router as products_router
from app.api.v1.orders import router as orders_router

# 创建 FastAPI 实例
app = FastAPI(
    title="电商商城 API",
    description="电商项目后端接口文档",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users_router, prefix="/api/v1/users", tags=["用户"])
app.include_router(products_router, prefix="/api/v1/products", tags=["商品"])
app.include_router(orders_router, prefix="/api/v1/orders", tags=["订单"])

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
        reload=True
    )