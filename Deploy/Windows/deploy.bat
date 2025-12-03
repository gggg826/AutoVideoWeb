@echo off
REM ============================================================================
REM AutoVideoWeb Windows 一键部署脚本
REM 用途: 在Windows环境下快速部署AutoVideoWeb应用
REM 要求: Docker Desktop for Windows
REM ============================================================================

SETLOCAL EnableDelayedExpansion

REM 配置变量
SET APP_NAME=AutoVideoWeb
SET APP_DIR=%CD%
SET PORT=8000
SET ADMIN_PASSWORD=Admin@123

REM 颜色设置（需要Windows 10+）
echo [92m========================================[0m
echo [92m  %APP_NAME% Windows 部署脚本[0m
echo [92m========================================[0m
echo.

REM 检查Docker Desktop
echo [94m[1/5] 检查Docker Desktop...[0m
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [91m[错误] Docker Desktop未安装或未启动[0m
    echo.
    echo 请先安装Docker Desktop:
    echo   1. 访问: https://www.docker.com/products/docker-desktop
    echo   2. 下载并安装Docker Desktop for Windows
    echo   3. 启动Docker Desktop
    echo   4. 确保Docker Desktop正在运行（系统托盘有Docker图标）
    echo   5. 重新运行此脚本
    echo.
    pause
    exit /b 1
)
docker --version
echo [92m[成功] Docker Desktop已安装并运行[0m
echo.

REM 检查docker-compose
echo [94m[2/5] 检查Docker Compose...[0m
docker-compose --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [91m[错误] Docker Compose未找到[0m
    echo 请确保Docker Desktop已正确安装
    pause
    exit /b 1
)
docker-compose --version
echo [92m[成功] Docker Compose可用[0m
echo.

REM 检查代码目录
echo [94m[3/5] 检查项目文件...[0m
if not exist "docker-compose.yml" (
    echo [91m[错误] 未找到docker-compose.yml文件[0m
    echo 请确保在项目根目录下运行此脚本
    pause
    exit /b 1
)
echo [92m[成功] 项目文件完整[0m
echo.

REM 配置环境变量
echo [94m[4/5] 配置环境变量...[0m
set /p CUSTOM_PASSWORD="设置管理员密码（留空使用默认 Admin@123）: "
if not "!CUSTOM_PASSWORD!"=="" (
    SET ADMIN_PASSWORD=!CUSTOM_PASSWORD!
)
echo [92m[成功] 环境变量配置完成[0m
echo.

REM 构建并启动
echo [94m[5/5] 构建并启动Docker容器...[0m
echo 正在构建镜像，请稍候...
docker-compose down >nul 2>&1
docker-compose build
if %ERRORLEVEL% NEQ 0 (
    echo [91m[错误] Docker镜像构建失败[0m
    pause
    exit /b 1
)

echo 正在启动容器...
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo [91m[错误] 容器启动失败[0m
    pause
    exit /b 1
)

REM 等待启动
timeout /t 5 /nobreak >nul

REM 检查状态
docker-compose ps

echo.
echo [92m========================================[0m
echo [92m  部署完成！[0m
echo [92m========================================[0m
echo.
echo [93m访问地址:[0m
echo   主页:     http://localhost:%PORT%/
echo   测试页面: http://localhost:%PORT%/public/index.html
echo   管理后台: http://localhost:%PORT%/admin/
echo   API文档:  http://localhost:%PORT%/docs
echo.
echo [93m管理员账号:[0m
echo   用户名: admin
echo   密码:   %ADMIN_PASSWORD%
echo.
echo [93m常用命令:[0m
echo   查看日志: docker-compose logs -f
echo   重启服务: docker-compose restart
echo   停止服务: docker-compose down
echo   启动服务: docker-compose up -d
echo.
echo [93m提示:[0m
echo   - 数据保存在 .\data 目录
echo   - 如需更新，运行: git pull 后重新执行此脚本
echo.
echo [92m========================================[0m
echo.
pause
