#!/bin/bash

echo "正在启动AI面试助手后端服务..."
echo

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未检测到Python 3，请先安装Python 3.8+"
    exit 1
fi

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f "venv/lib/python*/site-packages/fastapi" ]; then
    echo "正在安装依赖..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到.env文件"
    echo "请复制env.example为.env并配置"
    exit 1
fi

echo "启动服务器..."
echo "API文档: http://localhost:8000/docs"
echo

python -m app.main

