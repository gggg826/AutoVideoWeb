#!/bin/bash

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================================"
echo "   AdAlliance 访问追踪系统 - 启动脚本"
echo "============================================================"
echo ""

# 检查 Python 是否安装
echo "[1/5] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未检测到 Python3！${NC}"
    echo ""
    echo "请先安装 Python 3.10 或更高版本"
    echo "Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi
python3 --version
echo ""

# 检查虚拟环境
echo "[2/5] 检查虚拟环境..."
if [ ! -d "backend/.venv" ]; then
    echo -e "${YELLOW}⚠️  虚拟环境不存在，正在创建...${NC}"
    cd backend
    python3 -m venv .venv
    cd ..
    echo -e "${GREEN}✅ 虚拟环境创建成功${NC}"
else
    echo -e "${GREEN}✅ 虚拟环境已存在${NC}"
fi
echo ""

# 激活虚拟环境
echo "[3/5] 激活虚拟环境..."
source backend/.venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 错误: 无法激活虚拟环境${NC}"
    exit 1
fi
echo -e "${GREEN}✅ 虚拟环境已激活${NC}"
echo ""

# 检查依赖
echo "[4/5] 检查依赖包..."
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  依赖包未安装，正在安装...${NC}"
    pip install -r backend/requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 错误: 依赖包安装失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ 依赖包安装成功${NC}"
else
    echo -e "${GREEN}✅ 依赖包已安装${NC}"
fi
echo ""

# 检查数据库
echo "[5/5] 检查数据库..."
if [ ! -f "data/tracker.db" ]; then
    echo -e "${YELLOW}⚠️  数据库不存在，正在初始化...${NC}"
    python backend/scripts/init_db.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 错误: 数据库初始化失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ 数据库初始化成功${NC}"
else
    echo -e "${GREEN}✅ 数据库已存在${NC}"
fi
echo ""

# 启动服务器
echo "============================================================"
echo "   准备启动服务器..."
echo "============================================================"
echo ""
echo -e "${BLUE}📍 访问地址:${NC}"
echo "   - 主页:     http://localhost:8000/"
echo "   - 测试页面: http://localhost:8000/public/index.html"
echo "   - 管理后台: http://localhost:8000/admin/index.html"
echo "   - API文档:  http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}💡 提示: 按 Ctrl+C 可停止服务器${NC}"
echo "============================================================"
echo ""

# 启动服务器
python run.py

# 如果服务器异常退出
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ 服务器异常退出${NC}"
fi
