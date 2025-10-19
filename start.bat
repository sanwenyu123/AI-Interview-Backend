@echo off
echo 正在启动AI面试助手后端服务...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate

REM 检查是否已安装依赖
if not exist "venv\Lib\site-packages\fastapi" (
    echo 正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查.env文件
if not exist ".env" (
    echo 警告: 未找到.env文件
    echo 请复制env.example为.env并配置
    pause
    exit /b 1
)

echo 启动服务器...
echo API文档: http://localhost:8000/docs
echo.

python -m app.main

pause





