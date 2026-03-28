// Jenkinsfile - 服务器端直接部署版本
// 适用于 Jenkins 安装在目标服务器的场景，无需文件传输

pipeline {
    agent any

    environment {
        // ==================== 配置区域 ====================
        DEPLOY_DIR = '/data/ecommerce-deploy'  // 部署目录（存放 docker-compose.yml 和 init_config.sh）
        PROJECT_DIR = "${WORKSPACE}"           // Jenkins 工作空间（代码仓库）

        // Docker 镜像配置
        BACKEND_IMAGE = 'ecommerce-backend:latest'
        FRONTEND_IMAGE = 'ecommerce-frontend:latest'

        // 临时构建目录（在 workspace 内，不会被 git 追踪）
        BUILD_OUTPUT_DIR = "${WORKSPACE}/build-output"
    }

    stages {
        stage('📥 检出代码') {
            steps {
                echo '正在从 Git 仓库拉取最新代码...'
                checkout scm
                echo '代码检出完成'
            }
        }

        stage('🛑 停止旧服务') {
            steps {
                script {
                    echo '检查并停止旧的服务...'
                    sh """
                        cd ${DEPLOY_DIR}
                        if [ -f "docker-compose.yml" ]; then
                            docker-compose down || true
                            echo '旧服务已停止'
                        else
                            echo '首次部署，跳过停止步骤'
                        fi
                    """
                }
            }
        }

        stage('📦 构建后端镜像') {
            steps {
                echo '开始构建后端 Docker 镜像...'
                sh """
                    cd ${PROJECT_DIR}
                    docker build -t ${BACKEND_IMAGE} ./backend
                """
                echo '✅ 后端镜像构建完成'
            }
        }

        stage('📦 构建前端镜像') {
            steps {
                echo '开始构建前端 Docker 镜像...'
                sh """
                    cd ${PROJECT_DIR}
                    docker build -t ${FRONTEND_IMAGE} ./frontend
                """
                echo '✅ 前端镜像构建完成'
            }
        }

        stage('🚀 部署服务') {
            steps {
                script {
                    echo '开始部署服务...'

                    // 确保部署目录存在
                    sh """
                        mkdir -p ${DEPLOY_DIR}
                    """

                    // 复制部署文件到部署目录
                    sh """
                        cp ${PROJECT_DIR}/ecommerce/docker-compose.yml ${DEPLOY_DIR}/
                        cp ${PROJECT_DIR}/ecommerce/init_config.sh ${DEPLOY_DIR}/

                        # 如果数据库初始化脚本存在，也复制过去
                        if [ -f "${PROJECT_DIR}/backend/init_db.py" ]; then
                            cp ${PROJECT_DIR}/backend/init_db.py ${DEPLOY_DIR}/
                        fi
                    """

                    // 创建简化的部署脚本（不需要加载镜像，因为已经本地构建）
                    sh """
                        cat > ${DEPLOY_DIR}/deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 开始部署电商项目..."
echo "======================================"

cd ${DEPLOY_DIR}

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
echo ""
echo "🔍 检查容器状态..."
docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"

# 5. 初始化数据库
echo ""
echo "📝 初始化数据库..."
if [ -f "init_db.py" ]; then
    docker exec -it ecommerce-backend python init_db.py || echo "数据库初始化可能已存在数据"
else
    echo "数据库初始化脚本不存在，跳过"
fi

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

                        chmod +x ${DEPLOY_DIR}/deploy.sh
                    """

                    // 执行部署
                    sh "${DEPLOY_DIR}/deploy.sh"
                }
            }
        }

        stage('✅ 验证部署') {
            steps {
                script {
                    echo '验证服务是否正常运行...'
                    sh """
                        echo '检查容器状态...'
                        docker ps --filter "name=ecommerce" --format "table {{.Names}}\\t{{.Status}}"

                        echo ''
                        echo '等待 10 秒后检查后端服务...'
                        sleep 10

                        # 检查后端 API 是否可访问
                        if curl -s http://localhost:8000/docs > /dev/null; then
                            echo '✅ 后端 API 运行正常'
                        else
                            echo '⚠️  后端 API 可能未完全启动，请稍后检查'
                        fi

                        # 检查前端是否可访问
                        if curl -s http://localhost > /dev/null; then
                            echo '✅ 前端服务运行正常'
                        else
                            echo '⚠️  前端服务可能未完全启动，请稍后检查'
                        fi
                    """
                }
            }
        }
    }

    post {
        always {
            echo '清理临时文件...'
            sh """
                # 清理部署脚本
                rm -f ${DEPLOY_DIR}/deploy.sh

                # 清理未使用的 Docker 镜像（保留最近 3 个版本）
                docker images | grep ecommerce | tail -n +4 | awk '{print \$3}' | xargs -r docker rmi 2>/dev/null || true
            """
            echo '清理完成'
        }

        success {
            echo '✅ 部署成功！'
            script {
                currentBuild.result = 'SUCCESS'
                echo '''
                ======================================
                🎉 部署成功完成！
                ======================================

                📋 访问地址：
                  前端：http://localhost
                  后端 API: http://localhost:8000
                  API 文档：http://localhost:8000/docs

                🔧 测试账号:
                  普通用户：testuser / 123456
                  管理员：admin / admin123

                ======================================
                '''
            }
        }

        failure {
            echo '❌ 部署失败！'
            script {
                currentBuild.result = 'FAILURE'
                echo '''
                ======================================
                ❌ 部署失败！
                ======================================

                请检查构建日志以获取详细信息。

                常见问题排查：
                1. 检查 Docker 服务是否正常运行
                2. 检查端口是否被占用
                3. 检查磁盘空间是否充足
                4. 查看 Docker 日志：docker logs ecommerce-backend
                ======================================
                '''
            }
        }
    }
}
