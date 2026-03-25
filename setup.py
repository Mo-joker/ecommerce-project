import os
import sys


def create_project_structure():
    """快速创建项目目录结构"""

    # 项目根目录
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义所有需要创建的目录
    directories = [
        # 后端目录
        "backend/app/api/v1",
        "backend/app/core",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/services",
        "backend/app/utils",
        "backend/migrations/versions",
        "backend/tests",

        # 前端目录
        "frontend/src/assets/styles",
        "frontend/src/assets/images",
        "frontend/src/components/common",
        "frontend/src/components/shop",
        "frontend/src/views/auth",
        "frontend/src/views/home",
        "frontend/src/views/products",
        "frontend/src/views/orders",
        "frontend/src/views/cart",
        "frontend/src/router",
        "frontend/src/stores",
        "frontend/src/api",
        "frontend/src/utils",
        "frontend/src/composables",
        "frontend/src/directives",
        "frontend/public",

        # 数据库
        "database",

        # 文档
        "docs",

        # 脚本
        "scripts"
    ]

    # 创建目录
    for directory in directories:
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)
        print(f"✅ 创建目录: {directory}")

    # 创建必要的空文件
    files = {
        # Python 包标识文件
        "backend/app/__init__.py": "# Backend app package\n",
        "backend/app/api/__init__.py": "# API package\n",
        "backend/app/api/v1/__init__.py": "# API v1 package\n",
        "backend/app/core/__init__.py": "# Core package\n",
        "backend/app/models/__init__.py": "# Models package\n",
        "backend/app/schemas/__init__.py": "# Schemas package\n",
        "backend/app/services/__init__.py": "# Services package\n",
        "backend/app/utils/__init__.py": "# Utils package\n",
        "backend/tests/__init__.py": "# Tests package\n",

        # 配置文件
        "backend/.env.example": "# Database\nDATABASE_URL=mysql+aiomysql://user:password@localhost:3306/ecommerce\n\n# JWT\nSECRET_KEY=your-secret-key\nALGORITHM=HS256\nACCESS_TOKEN_EXPIRE_MINUTES=30\n",
        "backend/requirements.txt": "fastapi==0.104.1\nuvicorn[standard]==0.24.0\nsqlalchemy==2.0.23\naiomysql==0.2.0\npydantic==2.5.0\npydantic-settings==2.1.0\npython-jose[cryptography]==3.3.0\npasslib[bcrypt]==1.7.4\npython-multipart==0.0.6\nalembic==1.12.1\n",

        # 前端配置文件
        "frontend/package.json": '{\n  "name": "ecommerce-frontend",\n  "version": "1.0.0",\n  "type": "module",\n  "scripts": {\n    "dev": "vite",\n    "build": "vite build",\n    "preview": "vite preview"\n  },\n  "dependencies": {\n    "vue": "^3.3.8",\n    "vue-router": "^4.2.5",\n    "pinia": "^2.1.7",\n    "axios": "^1.6.2",\n    "element-plus": "^2.4.4"\n  },\n  "devDependencies": {\n    "@vitejs/plugin-vue": "^4.5.0",\n    "vite": "^5.0.0"\n  }\n}\n',

        "frontend/vite.config.js": "import { defineConfig } from 'vite'\nimport vue from '@vitejs/plugin-vue'\n\nexport default defineConfig({\n  plugins: [vue()],\n  server: {\n    port: 5173,\n    proxy: {\n      '/api': {\n        target: 'http://localhost:8000',\n        changeOrigin: true\n      }\n    }\n  }\n})\n",

        "frontend/index.html": '<!DOCTYPE html>\n<html lang="zh-CN">\n  <head>\n    <meta charset="UTF-8">\n    <link rel="icon" type="image/svg+xml" href="/favicon.ico">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>电商商城</title>\n  </head>\n  <body>\n    <div id="app"></div>\n    <script type="module" src="/src/main.js"></script>\n  </body>\n</html>\n',

        "frontend/src/main.js": "import { createApp } from 'vue'\nimport { createPinia } from 'pinia'\nimport ElementPlus from 'element-plus'\nimport 'element-plus/dist/index.css'\nimport App from './App.vue'\nimport router from './router'\n\nconst app = createApp(App)\napp.use(createPinia())\napp.use(router)\napp.use(ElementPlus)\napp.mount('#app')\n",

        "frontend/src/App.vue": '<template>\n  <div id="app">\n    <router-view />\n  </div>\n</template>\n\n<script setup>\n</script>\n\n<style>\n* {\n  margin: 0;\n  padding: 0;\n  box-sizing: border-box;\n}\n\nbody {\n  font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', sans-serif;\n}\n</style>\n',

        # 数据库文件
        "database/init.sql": "-- 初始化数据库脚本\nCREATE DATABASE IF NOT EXISTS ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\nUSE ecommerce;\n\n-- 用户表\nCREATE TABLE IF NOT EXISTS users (\n    id INT PRIMARY KEY AUTO_INCREMENT,\n    email VARCHAR(100) UNIQUE NOT NULL,\n    username VARCHAR(50) UNIQUE NOT NULL,\n    hashed_password VARCHAR(200) NOT NULL,\n    full_name VARCHAR(100),\n    is_active BOOLEAN DEFAULT TRUE,\n    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);\n",

        # Docker 文件
        "docker-compose.yml": "version: '3.8'\n\nservices:\n  mysql:\n    image: mysql:8.0\n    environment:\n      MYSQL_ROOT_PASSWORD: root123\n      MYSQL_DATABASE: ecommerce\n    ports:\n      - \"3306:3306\"\n    volumes:\n      - mysql-data:/var/lib/mysql\n\n  backend:\n    build: ./backend\n    ports:\n      - \"8000:8000\"\n    depends_on:\n      - mysql\n\nvolumes:\n  mysql-data:\n",

        "backend/Dockerfile": "FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . .\n\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n",

        "frontend/Dockerfile": "FROM node:18-alpine AS build\n\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install\nCOPY . .\nRUN npm run build\n\nFROM nginx:alpine\nCOPY --from=build /app/dist /usr/share/nginx/html\nCOPY nginx.conf /etc/nginx/conf.d/default.conf\nEXPOSE 80\n",

        # README
        "README.md": "# 电商商城项目\n\n## 技术栈\n\n### 后端\n- FastAPI\n- SQLAlchemy\n- MySQL\n- JWT\n\n### 前端\n- Vue 3\n- Pinia\n- Vue Router\n- Element Plus\n\n## 快速启动\n\n### 1. 启动数据库\n```bash\ndocker-compose up -d mysql\n```\n\n### 2. 启动后端\n```bash\ncd backend\npip install -r requirements.txt\nuvicorn app.main:app --reload\n```\n\n### 3. 启动前端\n```bash\ncd frontend\nnpm install\nnpm run dev\n```\n\n访问 http://localhost:5173\n"
    }

    for file_path, content in files.items():
        full_path = os.path.join(base_dir, file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建文件: {file_path}")

    print("\n🎉 项目结构创建完成！")
    print("\n下一步：")
    print("1. 在 PyCharm 中打开项目")
    print("2. 配置 Python 解释器")
    print("3. 运行 pip install -r backend/requirements.txt")
    print("4. 运行 npm install (在 frontend 目录)")
    print("5. 启动 MySQL 数据库")
    print("6. 开始开发！")


if __name__ == "__main__":
    create_project_structure()