# 后端项目结构说明

## 📁 完整目录结构

```
backend/
│
├── 📄 requirements.txt          # Python依赖包列表
├── 📄 env.example               # 环境变量模板
├── 📄 .gitignore               # Git忽略文件
├── 📄 init_db.py               # 数据库初始化脚本
├── 📄 start.bat                # Windows启动脚本
├── 📄 start.sh                 # Linux/Mac启动脚本
├── 📄 README.md                # 项目说明文档
├── 📄 QUICKSTART.md            # 快速开始指南
├── 📄 DEVELOPMENT.md           # 开发进度文档
└── 📄 STRUCTURE.md             # 本文件 - 结构说明
│
├── 📁 app/                     # 主应用目录
│   │
│   ├── 📄 __init__.py          # 应用包初始化
│   ├── 📄 main.py              # ✅ FastAPI应用入口
│   ├── 📄 config.py            # ✅ 全局配置管理
│   ├── 📄 dependencies.py      # 🚧 依赖注入（待创建）
│   │
│   ├── 📁 core/                # 核心功能模块
│   │   ├── 📄 __init__.py
│   │   ├── 📄 database.py      # ✅ 数据库连接和会话
│   │   └── 📄 security.py      # ✅ JWT认证、密码加密
│   │
│   ├── 📁 models/              # SQLAlchemy数据库模型
│   │   ├── 📄 __init__.py      # ✅ 模型导出
│   │   ├── 📄 user.py          # ✅ 用户模型
│   │   ├── 📄 interview.py     # ✅ 面试记录模型
│   │   ├── 📄 question.py      # ✅ 问题模型
│   │   ├── 📄 answer.py        # ✅ 回答模型
│   │   ├── 📄 evaluation.py    # ✅ 评价模型
│   │   └── 📄 setting.py       # ✅ 用户设置模型
│   │
│   ├── 📁 schemas/             # Pydantic数据验证模式
│   │   ├── 📄 __init__.py      # ✅ 模式导出
│   │   ├── 📄 user.py          # ✅ 用户相关模式
│   │   ├── 📄 auth.py          # ✅ 认证相关模式
│   │   ├── 📄 interview.py     # ✅ 面试相关模式
│   │   ├── 📄 question.py      # ✅ 问题相关模式
│   │   ├── 📄 answer.py        # ✅ 回答相关模式
│   │   ├── 📄 evaluation.py    # ✅ 评价相关模式
│   │   └── 📄 setting.py       # ✅ 设置相关模式
│   │
│   ├── 📁 api/                 # API路由（待实现）
│   │   ├── 📄 __init__.py      # 🚧 API包初始化
│   │   └── 📁 v1/              # API v1版本
│   │       ├── 📄 __init__.py  # 🚧 路由汇总
│   │       ├── 📄 auth.py      # 🚧 认证相关API
│   │       ├── 📄 users.py     # 🚧 用户管理API
│   │       ├── 📄 interviews.py # 🚧 面试相关API
│   │       ├── 📄 questions.py  # 🚧 问题生成API
│   │       ├── 📄 answers.py    # 🚧 答案提交API
│   │       ├── 📄 evaluations.py # 🚧 评价API
│   │       ├── 📄 history.py    # 🚧 历史记录API
│   │       └── 📄 settings.py   # 🚧 设置管理API
│   │
│   ├── 📁 services/            # 业务逻辑层（待实现）
│   │   ├── 📄 __init__.py      # 🚧 服务包初始化
│   │   ├── 📄 user_service.py  # 🚧 用户业务逻辑
│   │   ├── 📄 auth_service.py  # 🚧 认证服务
│   │   ├── 📄 ai_service.py    # 🚧 AI服务（OpenAI）
│   │   ├── 📄 interview_service.py # 🚧 面试业务逻辑
│   │   └── 📄 evaluation_service.py # 🚧 评价业务逻辑
│   │
│   └── 📁 utils/               # 工具函数（待实现）
│       ├── 📄 __init__.py      # 🚧 工具包初始化
│       ├── 📄 ai_prompts.py    # 🚧 AI提示词模板
│       └── 📄 helpers.py       # 🚧 辅助函数
│
├── 📁 tests/                   # 测试（待实现）
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py          # 🚧 测试配置
│   ├── 📄 test_auth.py         # 🚧 认证测试
│   ├── 📄 test_interviews.py   # 🚧 面试测试
│   └── 📄 test_ai_service.py   # 🚧 AI服务测试
│
├── 📁 alembic/                 # 数据库迁移（待配置）
│   ├── 📄 alembic.ini          # 🚧 Alembic配置
│   ├── 📄 env.py               # 🚧 迁移环境
│   └── 📁 versions/            # 🚧 迁移脚本
│
├── 📁 logs/                    # 日志文件（运行时生成）
│   └── 📄 app.log
│
└── 📁 uploads/                 # 上传文件（运行时生成）
    └── 📁 audio/               # 语音文件
```

## 📊 文件状态说明

- ✅ **已完成**: 文件已创建并完成基本功能
- 🚧 **待实现**: 文件需要创建或功能需要实现
- 📁 **目录**: 文件夹
- 📄 **文件**: 文件

## 🎯 核心模块说明

### 1️⃣ app/main.py
**作用**: FastAPI应用入口
- 创建FastAPI实例
- 配置CORS
- 注册路由
- 启动/关闭事件

### 2️⃣ app/config.py
**作用**: 全局配置管理
- 数据库配置
- JWT配置
- OpenAI配置
- CORS配置

### 3️⃣ app/core/database.py
**作用**: 数据库连接管理
- 创建数据库引擎
- 会话工厂
- 依赖注入函数
- 初始化表结构

### 4️⃣ app/core/security.py
**作用**: 安全相关功能
- 密码加密/验证
- JWT token生成
- JWT token解码
- 认证依赖

### 5️⃣ app/models/
**作用**: 数据库ORM模型
- User: 用户表
- Interview: 面试记录表
- Question: 问题表
- Answer: 回答表
- Evaluation: 评价表
- Setting: 用户设置表

### 6️⃣ app/schemas/
**作用**: 数据验证和序列化
- 请求体验证
- 响应体序列化
- 类型检查
- 数据转换

### 7️⃣ app/api/v1/
**作用**: API路由端点（待实现）
- 认证相关: 注册、登录、刷新token
- 面试管理: CRUD操作
- 问题生成: AI生成面试问题
- 评价系统: AI评价回答

### 8️⃣ app/services/
**作用**: 业务逻辑层（待实现）
- 用户服务: 用户CRUD
- AI服务: OpenAI集成
- 面试服务: 面试流程管理
- 评价服务: 评分和反馈

### 9️⃣ app/utils/
**作用**: 工具函数（待实现）
- AI提示词模板
- 辅助函数
- 常量定义

## 🔄 数据流向

```
客户端请求
    ↓
API路由 (app/api/v1/)
    ↓
业务逻辑 (app/services/)
    ↓
数据模型 (app/models/)
    ↓
数据库 (MySQL)
```

## 🗃️ 数据库关系

```
User (用户)
  ├── has many → Interview (面试记录)
  └── has one → Setting (设置)

Interview (面试记录)
  ├── belongs to → User
  ├── has many → Question (问题)
  └── has one → Evaluation (评价)

Question (问题)
  ├── belongs to → Interview
  └── has one → Answer (回答)

Answer (回答)
  └── belongs to → Question

Evaluation (评价)
  └── belongs to → Interview

Setting (设置)
  └── belongs to → User
```

## 🚀 开发流程

### 1. 创建新功能的标准流程

1. **定义数据模型** (app/models/)
2. **定义数据模式** (app/schemas/)
3. **创建服务层** (app/services/)
4. **创建API路由** (app/api/v1/)
5. **编写测试** (tests/)
6. **更新文档**

### 2. 添加新API端点

```python
# 1. 在 app/api/v1/ 创建路由文件
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/endpoint")
async def get_something(db: Session = Depends(get_db)):
    # 逻辑实现
    pass

# 2. 在 app/main.py 注册路由
from app.api.v1 import your_router
app.include_router(your_router.router, prefix="/api/v1")
```

## 📦 依赖关系

```
main.py
  └── 依赖 config.py
  └── 依赖 core/database.py
  └── 依赖 api/v1/* (待创建)

api/v1/*
  └── 依赖 schemas/*
  └── 依赖 services/*
  └── 依赖 core/security.py

services/*
  └── 依赖 models/*
  └── 依赖 utils/*

models/*
  └── 依赖 core/database.py
```

## 💡 最佳实践

1. **分层架构**: API → Service → Model
2. **依赖注入**: 使用FastAPI的Depends
3. **类型提示**: 所有函数都添加类型
4. **文档字符串**: 添加详细的docstring
5. **错误处理**: 统一的异常处理
6. **日志记录**: 关键操作记录日志

## 📝 命名规范

- **文件名**: 小写+下划线 (user_service.py)
- **类名**: 大驼峰 (UserService)
- **函数名**: 小写+下划线 (get_user)
- **常量**: 大写+下划线 (MAX_SIZE)
- **模型**: 单数名词 (User, Interview)
- **路由**: 复数名词 (/users, /interviews)

---

这个结构遵循FastAPI最佳实践，清晰分层，便于维护和扩展。




