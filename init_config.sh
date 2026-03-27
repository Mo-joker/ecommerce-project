#!/bin/bash
echo "🚀 开始部署电商项目..."
echo "=" * 60

# 检查必要文件是否存在
if [ ! -f "ecommerce-backend.tar" ]; then
    echo "❌ 错误：ecommerce-backend.tar 不存在"
    exit 1
fi

if [ ! -f "ecommerce-frontend.tar" ]; then
    echo "❌ 错误：ecommerce-frontend.tar 不存在"
    exit 1
fi

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 错误：docker-compose.yml 不存在"
    exit 1
fi

# 1. 加载镜像
echo "📦 加载后端镜像..."
docker load -i ecommerce-backend.tar
if [ $? -ne 0 ]; then
    echo "❌ 后端镜像加载失败"
    exit 1
fi

echo "📦 加载前端镜像..."
docker load -i ecommerce-frontend.tar
if [ $? -ne 0 ]; then
    echo "❌ 前端镜像加载失败"
    exit 1
fi

# 2. 停止旧容器
echo "⏹️  停止旧服务..."
docker-compose down

# 3. 启动新服务
echo "▶️  启动服务..."
docker-compose up -d

# 4. 等待启动
echo "⏳ 等待服务启动 (约 15 秒)..."
sleep 15

# 5. 检查容器状态
echo "🔍 检查容器状态..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 6. 初始化数据库
echo ""
echo "📝 初始化数据库..."
docker exec -it ecommerce-backend python init_db.py

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "======================================"
echo ""
echo "📋 访问地址："
echo "  前端：http://localhost"
echo "  后端 API: http://localhost:8000"
echo "  API 文档：http://localhost:8000/docs"
echo ""
echo "🔧 测试账号:"
echo "  普通用户：testuser / 123456"
echo "  管理员：admin / admin123"
echo ""
