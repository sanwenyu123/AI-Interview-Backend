# Windows 环境安装指南

## ✅ 已完成步骤

1. ✅ 安装了依赖包
2. ✅ 修复了MySQL兼容性问题

## 📋 下一步操作

### 1. 确保MySQL服务正在运行

检查MySQL服务状态：

**方法1：使用服务管理器**
- 按 `Win + R`，输入 `services.msc`
- 查找 MySQL 服务
- 确保状态为"正在运行"

**方法2：使用命令行**
```powershell
# 查看MySQL服务状态
Get-Service -Name MySQL*

# 如果没有运行，启动服务
Start-Service -Name MySQL80  # 或你的MySQL服务名称
```

### 2. 创建数据库

**使用MySQL命令行：**
```powershell
# 登录MySQL（会提示输入密码）
mysql -u root -p

# 在MySQL命令行中执行：
CREATE DATABASE interview_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
EXIT;
```

**或使用图形化工具：**
- MySQL Workbench
- Navicat
- phpMyAdmin

### 3. 配置环境变量

在 `backend` 目录下，复制 `env.example` 为 `.env`：

```powershell
Copy-Item env.example .env
```

然后编辑 `.env` 文件，修改以下配置：

```env
# 数据库配置（修改用户名和密码）
DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/interview_db

# JWT密钥（重要：生产环境必须修改）
SECRET_KEY=your-very-secure-secret-key-12345678

# OpenAI配置（如果要使用AI功能）
OPENAI_API_KEY=sk-your-openai-api-key
```

### 4. 初始化数据库表

```powershell
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

### 5. 启动后端服务

```powershell
# 方式1：使用启动脚本
.\start.bat

# 方式2：直接运行
python -m app.main

# 方式3：使用uvicorn
uvicorn app.main:app --reload
```

启动成功后会显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
启动 AI面试助手 v1.0.0
初始化数据库...
数据库初始化成功
INFO:     Application startup complete.
```

### 6. 测试API

打开浏览器访问：
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **ReDoc文档**: http://localhost:8000/redoc

## 🔧 常见问题

### 问题1：`pip install` 出现警告

**现象**：
```
ERROR: pip's dependency resolver does not currently take into account all the packages...
gradio 5.40.0 requires fastapi<1.0,>=0.115.2, but you have fastapi 0.110.0...
```

**解决**：
这些警告来自你环境中其他项目（gradio, langgraph）的依赖，不影响本项目运行。
如果想消除警告，可以创建独立的虚拟环境：
```powershell
# 创建新的虚拟环境
python -m venv venv_interview

# 激活虚拟环境
.\venv_interview\Scripts\activate

# 重新安装依赖
pip install -r requirements.txt
```

### 问题2：MySQL连接失败

**现象**：
```
OperationalError: (2003, "Can't connect to MySQL server...")
```

**解决**：
1. 确认MySQL服务正在运行
2. 检查 `.env` 中的数据库配置
3. 确认用户名、密码正确
4. 确认端口号（默认3306）

### 问题3：数据库初始化失败

**现象**：
```
sqlalchemy.exc.OperationalError: (1045, "Access denied for user...")
```

**解决**：
1. 确认数据库已创建：`interview_db`
2. 确认MySQL用户权限
3. 检查 `.env` 中的 `DATABASE_URL` 配置

### 问题4：端口被占用

**现象**：
```
OSError: [WinError 10048] 通常每个套接字地址只允许使用一次
```

**解决**：
1. 检查8000端口是否被占用：
```powershell
netstat -ano | findstr :8000
```

2. 修改端口（在 `app/main.py` 最后一行）：
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

## 📝 快速命令参考

```powershell
# 进入后端目录
cd backend

# 激活虚拟环境（如果使用）
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动服务
python -m app.main

# 退出（Ctrl+C）
```

## 🎯 下一步

启动成功后：
1. 访问 http://localhost:8000/docs 查看API文档
2. 使用Swagger UI测试注册和登录API
3. 配置OpenAI API Key启用AI功能
4. 启动前端项目进行联调

## 🔗 相关文档

- [快速开始指南](QUICKSTART.md)
- [API接口文档](API.md)
- [创建数据库说明](CREATE_DATABASE.md)
- [完成报告](COMPLETED.md)

