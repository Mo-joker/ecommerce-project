#!/bin/bash
# build-and-export.sh - 本地构建并导出镜像

echo "🚀 开始构建 Docker 镜像..."

# 1. 构建后端镜像
echo "📦 构建后端镜像..."
docker build -t ecommerce-backend:latest ./backend
if [ $? -ne 0 ]; then
    echo "❌ 后端镜像构建失败！"
    exit 1
fi
echo "✅ 后端镜像构建成功"

# 2. 构建前端镜像
echo "📦 构建前端镜像..."
docker build -t ecommerce-frontend:latest ./frontend
if [ $? -ne 0 ]; then
    echo "❌ 前端镜像构建失败！"
    exit 1
fi
echo "✅ 前端镜像构建成功"

# 3. 创建导出目录
EXPORT_DIR="./ecommerce"
mkdir -p "$EXPORT_DIR"

# 4. 导出镜像为 tar 文件到 ecommerce 目录
echo "💾 导出镜像到 $EXPORT_DIR 目录..."
docker save -o "$EXPORT_DIR/ecommerce-backend.tar" ecommerce-backend:latest
docker save -o "$EXPORT_DIR/ecommerce-frontend.tar" ecommerce-frontend:latest

echo ""
echo "✅ 镜像导出完成！"
echo "📁 生成的文件："
ls -lh "$EXPORT_DIR"/ecommerce-*.tar

echo ""
echo "📋 下一步：将以下文件传输到远程服务器"
echo "   - docker-compose.yml"
echo "   - $EXPORT_DIR/ecommerce-backend.tar"
echo "   - $EXPORT_DIR/ecommerce-frontend.tar"
echo "   - init_config.sh"
