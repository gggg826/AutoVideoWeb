# AdAlliance Tracker - 启动脚本 (PowerShell)
# PowerShell 版本对中文支持更好

$Host.UI.RawUI.WindowTitle = "AdAlliance Tracker - 启动服务器"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   AdAlliance 访问追踪系统 - 启动脚本" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 是否安装
Write-Host "[1/5] 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
} catch {
    Write-Host "[错误] 未检测到 Python！" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Python 3.10 或更高版本"
    Write-Host "下载地址: https://www.python.org/downloads/"
    Read-Host "按任意键退出"
    exit 1
}
Write-Host ""

# 检查虚拟环境
Write-Host "[2/5] 检查虚拟环境..." -ForegroundColor Yellow
if (-not (Test-Path "backend\.venv")) {
    Write-Host "[提示] 虚拟环境不存在，正在创建..." -ForegroundColor Yellow
    Push-Location backend
    python -m venv .venv
    Pop-Location
    Write-Host "[成功] 虚拟环境创建成功" -ForegroundColor Green
} else {
    Write-Host "[成功] 虚拟环境已存在" -ForegroundColor Green
}
Write-Host ""

# 激活虚拟环境
Write-Host "[3/5] 激活虚拟环境..." -ForegroundColor Yellow
& "backend\.venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
    Write-Host "[错误] 无法激活虚拟环境" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}
Write-Host "[成功] 虚拟环境已激活" -ForegroundColor Green
Write-Host ""

# 检查依赖
Write-Host "[4/5] 检查依赖包..." -ForegroundColor Yellow
$fastApiInstalled = python -c "import fastapi" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[提示] 依赖包未安装，正在安装..." -ForegroundColor Yellow
    pip install -r backend\requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 依赖包安装失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit 1
    }
    Write-Host "[成功] 依赖包安装成功" -ForegroundColor Green
} else {
    Write-Host "[成功] 依赖包已安装" -ForegroundColor Green
}
Write-Host ""

# 检查数据库
Write-Host "[5/5] 检查数据库..." -ForegroundColor Yellow
if (-not (Test-Path "data\tracker.db")) {
    Write-Host "[提示] 数据库不存在，正在初始化..." -ForegroundColor Yellow
    python backend\scripts\init_db.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 数据库初始化失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit 1
    }
    Write-Host "[成功] 数据库初始化成功" -ForegroundColor Green
} else {
    Write-Host "[成功] 数据库已存在" -ForegroundColor Green
}
Write-Host ""

# 启动服务器
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   准备启动服务器..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址:" -ForegroundColor Magenta
Write-Host "   - 主页:     http://localhost:8000/" -ForegroundColor White
Write-Host "   - 测试页面: http://localhost:8000/public/index.html" -ForegroundColor White
Write-Host "   - 管理后台: http://localhost:8000/admin/index.html" -ForegroundColor White
Write-Host "   - API文档:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "提示: 按 Ctrl+C 可停止服务器" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 启动服务器
python run.py

# 如果服务器异常退出
if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
    Write-Host ""
    Write-Host "[错误] 服务器异常退出" -ForegroundColor Red
    Read-Host "按任意键退出"
}
