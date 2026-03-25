# 电商商城项目

## 技术栈

### 后端
- FastAPI
- SQLAlchemy
- MySQL
- JWT

### 前端
- Vue 3
- Pinia
- Vue Router
- Element Plus

## 快速启动

### 1. 启动数据库
```bash
docker-compose up -d mysql
```

### 2. 启动后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. 启动前端
```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173
