#!/bin/bash
# server-jenkins-deploy.sh - 服务器端 Jenkins 部署脚本
# 直接在目标服务器上执行，无需文件传输

set -e  # 遇到错误立即退出

# ==================== 配置区域 ====================
PROJECT_DIR="/path/to/jenkins/workspace"  # Jenkins 工作空间
DEPLOY_DIR="/path/to/deployment"          # 部署目录

# ==================== 颜色输出 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "🚀 开始电商项目自动化部署"
echo "========================================"
echo ""

# 进入项目目录
cd "$PROJECT_DIR"

# ==================== 步骤 1: 停止旧服务 ====================
echo "${YELLOW}🛑 步骤 1: 停止旧服务${NC}"
cd "$DEPLOY_DIR"
docker-compose down || true
echo "✅ 旧服务已停止"
echo ""

# ==================== 步骤 2: 构建 Docker 镜像 ====================
echo "${YELLOW}📦 步骤 2: 构建 Docker 镜像${NC}"
cd "$PROJECT_DIR"

# 构建后端镜像
echo "构建后端镜像..."
docker build -t ecommerce-backend:latest ./backend
if [ $? -ne 0 ]; then
    echo "${RED}❌ 后端镜像构建失败！${NC}"
    exit 1
fi
echo "✅ 后端镜像构建成功"

# 构建前端镜像
echo "构建前端镜像..."
docker build -t ecommerce-frontend:latest ./frontend
if [ $? -ne 0 ]; then
    echo "${RED}❌ 前端镜像构建失败！${NC}"
    exit 1
fi
echo "✅ 前端镜像构建成功"
echo ""

# ==================== 步骤 3: 执行部署 ====================
echo "${YELLOW}🚀 步骤 3: 执行部署${NC}"
cd "$DEPLOY_DIR"

# 确保部署脚本有执行权限
chmod +x init_config.sh

# 修改 init_config.sh，跳过镜像加载步骤（因为已经本地构建了）
# 创建临时部署脚本
cat > deploy_temp.sh << 'EOF'
#!/bin/bash
echo "🚀 开始部署电商项目..."
echo "=" * 60

# 1. 停止旧容器
echo "⏹️  停止旧服务..."
docker-compose down

# 2. 启动新服务
echo "▶️  启动服务..."
docker-compose up -d

# 3. 等待启动
echo "⏳ 等待服务启动 (约 15 秒)..."
sleep 15

# 4. 检查容器状态
echo "🔍 检查容器状态..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 5. 初始化数据库
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
EOF

chmod +x deploy_temp.sh
./deploy_temp.sh

# 清理临时脚本
rm deploy_temp.sh

echo ""
echo "${GREEN}========================================${NC}"
echo "${GREEN}✅ 部署完成！${NC}"
echo "${GREEN}========================================${NC}"
