################################################################################
# AutoVideoWeb Windows PowerShell 部署脚本
# 用途: 在Windows环境下快速部署AutoVideoWeb应用
# 要求: Docker Desktop for Windows, PowerShell 5.1+
################################################################################

#Requires -RunAsAdministrator

# 设置错误处理
$ErrorActionPreference = "Stop"

# 配置变量
$APP_NAME = "AutoVideoWeb"
$APP_DIR = Get-Location
$PORT = 8000
$DOCKER_COMPOSE_FILE = "docker-compose.yml"

# 颜色函数
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Title {
    param([string]$Message)
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  $Message" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
}

# 检查Docker Desktop
function Test-DockerDesktop {
    Write-Info "检查Docker Desktop..."

    try {
        $dockerVersion = docker --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Docker命令执行失败"
        }

        Write-Success "Docker Desktop已安装: $dockerVersion"

        # 检查Docker是否运行
        docker ps >$null 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Docker Desktop未运行"
            Write-Info "请启动Docker Desktop后重试"
            exit 1
        }

        Write-Success "Docker Desktop正在运行"
        return $true
    }
    catch {
        Write-Error "Docker Desktop未安装或未启动"
        Write-Host "`n请安装Docker Desktop:"
        Write-Host "  1. 访问: https://www.docker.com/products/docker-desktop"
        Write-Host "  2. 下载并安装Docker Desktop for Windows"
        Write-Host "  3. 启动Docker Desktop"
        Write-Host "  4. 确保Docker Desktop正在运行（系统托盘有Docker图标）"
        Write-Host "  5. 以管理员身份重新运行此脚本`n"
        exit 1
    }
}

# 检查Docker Compose
function Test-DockerCompose {
    Write-Info "检查Docker Compose..."

    try {
        $composeVersion = docker-compose --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            # 尝试使用docker compose (v2)
            $composeVersion = docker compose version 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "Docker Compose不可用"
            }
        }

        Write-Success "Docker Compose可用: $composeVersion"
        return $true
    }
    catch {
        Write-Error "Docker Compose未找到"
        Write-Info "请确保Docker Desktop已正确安装"
        exit 1
    }
}

# 检查项目文件
function Test-ProjectFiles {
    Write-Info "检查项目文件..."

    if (-not (Test-Path $DOCKER_COMPOSE_FILE)) {
        Write-Error "未找到 $DOCKER_COMPOSE_FILE 文件"
        Write-Info "请确保在项目根目录下运行此脚本"
        exit 1
    }

    if (-not (Test-Path "Dockerfile")) {
        Write-Error "未找到 Dockerfile 文件"
        exit 1
    }

    Write-Success "项目文件完整"
}

# 配置环境变量
function Set-Environment {
    Write-Info "配置环境变量..."

    # 生成随机SECRET_KEY
    $randomBytes = New-Object byte[] 32
    [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($randomBytes)
    $SECRET_KEY = [BitConverter]::ToString($randomBytes).Replace("-", "").ToLower()

    # 提示输入管理员密码
    $ADMIN_PASSWORD = Read-Host "设置管理员密码（留空使用默认 Admin@123）"
    if ([string]::IsNullOrWhiteSpace($ADMIN_PASSWORD)) {
        $ADMIN_PASSWORD = "Admin@123"
    }

    Write-Success "环境变量配置完成"
    Write-Warning "请妥善保管管理员密码: $ADMIN_PASSWORD"

    return @{
        SecretKey = $SECRET_KEY
        AdminPassword = $ADMIN_PASSWORD
    }
}

# 停止旧容器
function Stop-OldContainers {
    Write-Info "停止旧容器..."

    try {
        docker-compose down 2>&1 | Out-Null
    }
    catch {
        # 忽略错误，可能没有运行的容器
    }
}

# 构建镜像
function Build-DockerImage {
    Write-Info "构建Docker镜像..."
    Write-Info "这可能需要几分钟时间，请耐心等待..."

    docker-compose build

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker镜像构建失败"
        exit 1
    }

    Write-Success "Docker镜像构建完成"
}

# 启动容器
function Start-Containers {
    Write-Info "启动Docker容器..."

    docker-compose up -d

    if ($LASTEXITCODE -ne 0) {
        Write-Error "容器启动失败"
        Write-Info "查看日志: docker-compose logs"
        exit 1
    }

    Write-Success "容器启动成功"
}

# 检查健康状态
function Test-Health {
    Write-Info "等待应用启动..."
    Start-Sleep -Seconds 10

    Write-Info "检查容器状态..."
    docker-compose ps

    $containerStatus = docker-compose ps -q | ForEach-Object {
        docker inspect $_ --format='{{.State.Status}}'
    }

    if ($containerStatus -contains "running") {
        Write-Success "应用运行正常"
        return $true
    }
    else {
        Write-Warning "容器可能未正常启动，请检查日志"
        Write-Info "查看日志: docker-compose logs -f"
        return $false
    }
}

# 显示部署信息
function Show-DeploymentInfo {
    param(
        [hashtable]$Config
    )

    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"})[0].IPAddress

    Write-Title "部署完成！"

    Write-Host "📋 应用信息:" -ForegroundColor Cyan
    Write-Host "  应用名称: $APP_NAME"
    Write-Host "  应用目录: $APP_DIR"
    Write-Host "  数据目录: $APP_DIR\data"
    Write-Host ""

    Write-Host "🌐 访问地址:" -ForegroundColor Cyan
    Write-Host "  主页:     http://localhost:$PORT/"
    Write-Host "            http://${localIP}:$PORT/"
    Write-Host "  测试页面: http://localhost:$PORT/public/index.html"
    Write-Host "  管理后台: http://localhost:$PORT/admin/"
    Write-Host "  API文档:  http://localhost:$PORT/docs"
    Write-Host ""

    Write-Host "🔐 管理员账号:" -ForegroundColor Cyan
    Write-Host "  用户名: admin"
    Write-Host "  密码:   $($Config.AdminPassword)"
    Write-Host ""

    Write-Host "📦 Docker管理命令:" -ForegroundColor Cyan
    Write-Host "  查看日志: docker-compose logs -f"
    Write-Host "  查看状态: docker-compose ps"
    Write-Host "  重启服务: docker-compose restart"
    Write-Host "  停止服务: docker-compose down"
    Write-Host "  启动服务: docker-compose up -d"
    Write-Host ""

    Write-Host "🔄 更新应用:" -ForegroundColor Cyan
    Write-Host "  git pull"
    Write-Host "  docker-compose down"
    Write-Host "  docker-compose build"
    Write-Host "  docker-compose up -d"
    Write-Host ""

    Write-Host "💾 数据备份:" -ForegroundColor Cyan
    Write-Host "  备份: Copy-Item .\data\visits.db .\backup\visits_$(Get-Date -Format 'yyyyMMdd').db"
    Write-Host "  恢复: Copy-Item .\backup\visits_20240101.db .\data\visits.db"
    Write-Host ""

    Write-Host "========================================" -ForegroundColor Green
}

# 主函数
function Main {
    Write-Title "$APP_NAME Windows 部署脚本"

    # 检查管理员权限
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Warning "建议以管理员身份运行此脚本"
        $continue = Read-Host "是否继续? (Y/N)"
        if ($continue -ne "Y" -and $continue -ne "y") {
            exit 0
        }
    }

    # 执行部署步骤
    try {
        Test-DockerDesktop
        Test-DockerCompose
        Test-ProjectFiles
        $config = Set-Environment
        Stop-OldContainers
        Build-DockerImage
        Start-Containers
        Test-Health
        Show-DeploymentInfo -Config $config

        Write-Success "部署完成！"
    }
    catch {
        Write-Error "部署失败: $_"
        Write-Info "错误详情: $($_.Exception.Message)"
        exit 1
    }
}

# 执行主函数
Main
