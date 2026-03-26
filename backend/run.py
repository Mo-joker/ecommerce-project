"""
启动脚本 - 在 backend 目录下运行 python run.py
"""
import uvicorn

if __name__ == "__main__":
    # 禁用 reload 以确保 CORS 配置正确加载
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发环境可以改为 True，但如果 CORS 有问题就设为 False
        log_level="info"
    )