# AI面试助手 - 后端API

基于FastAPI的AI模拟面试平台后端服务。

## 技术栈

- **FastAPI** - 高性能Web框架
- **SQLAlchemy** - ORM
- **MySQL** - 数据库
- **JWT** - 认证
- **OpenAI API** - AI功能
- **Python 3.8+**

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env.example` 为 `.env` 并配置：

```bash
cp env.example .env
```

编辑 `.env` 文件，配置：
- 数据库连接
- OpenAI API密钥
- JWT密钥等

### 3. 创建数据库

在MySQL中创建数据库：

```sql
CREATE DATABASE interview_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 启动服务

```bash
# 开发模式
python -m app.main

# 或使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置
│   ├── core/                # 核心功能
│   │   ├── database.py      # 数据库连接
│   │   └── security.py      # 安全功能
│   ├── models/              # 数据库模型
│   ├── schemas/             # Pydantic模式
│   ├── api/                 # API路由
│   ├── services/            # 业务逻辑
│   └── utils/               # 工具函数
├── requirements.txt         # 依赖
└── README.md
```

## API接口

### 认证相关 `/api/v1/auth`
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `POST /refresh` - 刷新token
- `GET /me` - 获取当前用户信息

### 面试相关 `/api/v1/interviews`
- `POST /` - 创建面试
- `GET /` - 获取面试列表
- `GET /{id}` - 获取面试详情
- `POST /{id}/start` - 开始面试
- `POST /{id}/complete` - 完成面试

### 问题生成 `/api/v1/questions`
- `POST /generate` - 生成面试问题

### 评价相关 `/api/v1/evaluations`
- `POST /` - 创建评价
- `GET /interview/{id}` - 获取面试评价

## 数据库表结构

### users (用户表)
- 用户认证信息
- 个人资料

### interviews (面试记录表)
- 面试配置
- 面试状态
- 面试结果

### questions (问题表)
- 面试问题
- 问题顺序

### answers (回答表)
- 用户回答
- 回答类型（文字/语音）

### evaluations (评价表)
- 面试评分
- 评价反馈
- 改进建议

### settings (用户设置表)
- 语言偏好
- 语音设置

## 开发说明

### 添加新的API路由

1. 在 `app/api/v1/` 创建新的路由文件
2. 在 `app/main.py` 中注册路由
3. 使用 FastAPI 的依赖注入系统

### 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
# 初始化迁移
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DATABASE_URL | MySQL连接字符串 | - |
| SECRET_KEY | JWT密钥 | - |
| OPENAI_API_KEY | OpenAI API密钥 | - |
| DEBUG | 调试模式 | True |

## 注意事项

1. **安全性**
   - 生产环境务必修改 SECRET_KEY
   - 使用强密码保护数据库
   - 启用HTTPS

2. **性能**
   - 配置合适的数据库连接池
   - 使用Redis缓存AI响应
   - 异步处理耗时操作

3. **AI调用**
   - OpenAI API有速率限制
   - 建议缓存常见问题
   - 监控API调用成本

## 许可证

MIT License

