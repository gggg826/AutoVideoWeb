@echo off
chcp 65001 >nul
title AdAlliance Tracker - 启动服务器

echo ============================================================
echo    AdAlliance 访问追踪系统 - 启动脚本
echo ============================================================
echo.

:: 检查 Python 是否安装
echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到 Python！
    echo.
    echo 请先安装 Python 3.10 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

:: 检查虚拟环境
echo [2/5] 检查虚拟环境...
if not exist "backend\.venv\" (
    echo ⚠️  虚拟环境不存在，正在创建...
    cd backend
    python -m venv .venv
    cd ..
    echo ✅ 虚拟环境创建成功
) else (
    echo ✅ 虚拟环境已存在
)
echo.

:: 激活虚拟环境
echo [3/5] 激活虚拟环境...
call backend\.venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ 错误: 无法激活虚拟环境
    pause
    exit /b 1
)
echo ✅ 虚拟环境已激活
echo.

:: 检查依赖
echo [4/5] 检查依赖包...
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  依赖包未安装，正在安装...
    pip install -r backend\requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 错误: 依赖包安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖包安装成功
) else (
    echo ✅ 依赖包已安装
)
echo.

:: 检查数据库
echo [5/5] 检查数据库...
if not exist "data\tracker.db" (
    echo ⚠️  数据库不存在，正在初始化...
    python backend\scripts\init_db.py
    if %errorlevel% neq 0 (
        echo ❌ 错误: 数据库初始化失败
        pause
        exit /b 1
    )
    echo ✅ 数据库初始化成功
) else (
    echo ✅ 数据库已存在
)
echo.

:: 启动服务器
echo ============================================================
echo    准备启动服务器...
echo ============================================================
echo.
echo 📍 访问地址:
echo    - 主页:     http://localhost:8000/
echo    - 测试页面: http://localhost:8000/public/index.html
echo    - 管理后台: http://localhost:8000/admin/index.html
echo    - API文档:  http://localhost:8000/docs
echo.
echo 💡 提示: 按 Ctrl+C 可停止服务器
echo ============================================================
echo.

:: 启动服务器
python run.py

:: 如果服务器异常退出
if %errorlevel% neq 0 (
    echo.
    echo ❌ 服务器异常退出
    pause
)
