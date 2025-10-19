# 快速开始指南

## 📋 前置要求

- Python 3.8+
- MySQL 5.7+ 或 8.0+
- pip
- OpenAI API Key（用于AI功能）

## 🚀 快速启动

### 1. 创建MySQL数据库

```sql
CREATE DATABASE interview_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 配置环境变量

复制环境变量模板：

```bash
cd backend
cp env.example .env
```

编辑 `.env` 文件，修改以下配置：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://你的用户名:你的密码@localhost:3306/interview_db

# JWT密钥（生产环境务必修改）
SECRET_KEY=your-very-secure-secret-key-change-this

# OpenAI配置
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. 安装依赖

**Windows:**
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
python init_db.py
```

成功后会显示：
```
✅ 数据库初始化成功！
已创建以下表:
  - users (用户表)
  - interviews (面试记录表)
  - questions (问题表)
  - answers (回答表)
  - evaluations (评价表)
  - settings (设置表)
```

### 5. 启动服务

**方式1：使用启动脚本（推荐）**

Windows:
```bash
start.bat
```

Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

**方式2：直接运行**
```bash
python -m app.main
```

**方式3：使用uvicorn**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问API

启动成功后访问：

- **API根路径**: http://localhost:8000
- **Swagger文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 📝 测试API

### 使用Swagger UI

1. 打开 http://localhost:8000/docs
2. 点击任意API端点
3. 点击 "Try it out"
4. 填写参数
5. 点击 "Execute"

### 使用curl

**健康检查:**
```bash
curl http://localhost:8000/health
```

**注册用户（待实现）:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

## 🛠️ 开发说明

### 项目结构

```
backend/
├── app/
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── core/                # 核心功能
│   │   ├── database.py      # 数据库连接
│   │   └── security.py      # 安全功能(JWT, 密码)
│   ├── models/              # SQLAlchemy模型
│   │   ├── user.py
│   │   ├── interview.py
│   │   ├── question.py
│   │   ├── answer.py
│   │   ├── evaluation.py
│   │   └── setting.py
│   ├── schemas/             # Pydantic模式
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── interview.py
│   │   ├── question.py
│   │   ├── answer.py
│   │   ├── evaluation.py
│   │   └── setting.py
│   ├── api/                 # API路由（待实现）
│   ├── services/            # 业务逻辑（待实现）
│   └── utils/               # 工具函数（待实现）
├── init_db.py               # 数据库初始化脚本
├── requirements.txt         # Python依赖
├── env.example              # 环境变量模板
└── README.md
```

### 下一步开发

已完成：
- ✅ 项目基础架构
- ✅ 数据库模型设计
- ✅ Pydantic数据验证模式
- ✅ 核心安全功能（JWT, 密码加密）
- ✅ 数据库连接管理
- ✅ 主应用配置

待实现（按优先级）：
1. **认证API** (`app/api/v1/auth.py`)
   - 用户注册
   - 用户登录
   - Token刷新
   - 获取当前用户

2. **面试API** (`app/api/v1/interviews.py`)
   - CRUD操作
   - 开始/完成面试

3. **AI服务** (`app/services/ai_service.py`)
   - OpenAI集成
   - 问题生成
   - 答案评价

4. **其他API**
   - 问题管理
   - 评价系统
   - 历史记录
   - 用户设置

## 🐛 常见问题

### 1. 数据库连接失败

**错误**: `Can't connect to MySQL server`

**解决**:
- 检查MySQL服务是否启动
- 检查 `.env` 中的数据库配置
- 确认数据库已创建

### 2. 模块导入错误

**错误**: `ModuleNotFoundError`

**解决**:
```bash
# 确保虚拟环境已激活
pip install -r requirements.txt
```

### 3. JWT密钥警告

**警告**: 使用默认SECRET_KEY

**解决**:
在 `.env` 中设置强密码：
```env
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
```

### 4. OpenAI API错误

**错误**: `OpenAI API key not found`

**解决**:
在 `.env` 中配置：
```env
OPENAI_API_KEY=sk-your-api-key-here
```

## 📚 更多资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Pydantic文档](https://docs.pydantic.dev/)
- [OpenAI API文档](https://platform.openai.com/docs/)

## 💡 提示

1. **开发模式**: 自动重载已启用，修改代码后会自动重启
2. **日志**: 查看控制台输出了解请求日志
3. **调试**: 使用Swagger UI测试API非常方便
4. **数据库**: 使用MySQL Workbench等工具可视化管理数据

## 🔒 安全提示

⚠️ **生产环境部署前务必**:
1. 修改 `SECRET_KEY` 为强随机字符串
2. 设置 `DEBUG=False`
3. 配置HTTPS
4. 限制CORS来源
5. 启用速率限制
6. 定期备份数据库

---

需要帮助？查看 [README.md](README.md) 或提交Issue。





