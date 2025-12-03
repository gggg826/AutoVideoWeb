#!/bin/bash
###############################################################################
# AutoVideoWeb 一键部署脚本 (CentOS 7/8/9)
# 用途: 在CentOS生产环境上快速部署AutoVideoWeb应用
# 作者: Claude Code
###############################################################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
APP_NAME="AutoVideoWeb"
APP_DIR="/opt/autovideoweb"
DOCKER_COMPOSE_VERSION="2.24.0"
DOMAIN=""  # 留空表示不配置域名/SSL
PORT=8000

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查root权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用root权限运行此脚本"
        log_info "使用: sudo bash $0"
        exit 1
    fi
}

# 检测CentOS版本
detect_os() {
    log_info "检测操作系统版本..."

    if [ -f /etc/redhat-release ]; then
        OS_VERSION=$(cat /etc/redhat-release)
        log_success "检测到系统: $OS_VERSION"

        # 检测CentOS主版本号
        if grep -q "CentOS Linux release 7" /etc/redhat-release; then
            CENTOS_VERSION=7
        elif grep -q "CentOS" /etc/redhat-release && grep -q "release 8" /etc/redhat-release; then
            CENTOS_VERSION=8
        elif grep -q "CentOS Stream" /etc/redhat-release; then
            CENTOS_VERSION=9
        else
            log_warning "未识别的CentOS版本，将尝试继续安装"
            CENTOS_VERSION=7
        fi
    else
        log_error "此脚本仅支持CentOS系统"
        exit 1
    fi
}

# 安装Docker
install_docker() {
    if command -v docker &> /dev/null; then
        log_success "Docker已安装: $(docker --version)"
        return 0
    fi

    log_info "开始安装Docker..."

    # 卸载旧版本
    yum remove -y docker docker-client docker-client-latest docker-common \
        docker-latest docker-latest-logrotate docker-logrotate docker-engine

    # 安装依赖
    yum install -y yum-utils device-mapper-persistent-data lvm2

    # 添加Docker仓库
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

    # 安装Docker
    yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin

    # 启动Docker
    systemctl start docker
    systemctl enable docker

    log_success "Docker安装完成: $(docker --version)"
}

# 安装Docker Compose
install_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        log_success "Docker Compose已安装: $(docker-compose --version)"
        return 0
    fi

    log_info "开始安装Docker Compose..."

    # 下载Docker Compose
    curl -L "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose

    # 添加执行权限
    chmod +x /usr/local/bin/docker-compose

    # 创建软链接
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

    log_success "Docker Compose安装完成: $(docker-compose --version)"
}

# 安装Git
install_git() {
    if command -v git &> /dev/null; then
        log_success "Git已安装: $(git --version)"
        return 0
    fi

    log_info "开始安装Git..."
    yum install -y git
    log_success "Git安装完成: $(git --version)"
}

# 配置防火墙
configure_firewall() {
    log_info "配置防火墙规则..."

    # 检查firewalld状态
    if systemctl is-active --quiet firewalld; then
        firewall-cmd --permanent --add-port=${PORT}/tcp
        firewall-cmd --permanent --add-port=80/tcp
        firewall-cmd --permanent --add-port=443/tcp
        firewall-cmd --reload
        log_success "防火墙规则已配置 (端口: ${PORT}, 80, 443)"
    else
        log_warning "firewalld未运行，跳过防火墙配置"
    fi
}

# 克隆或更新代码
setup_app() {
    log_info "设置应用代码..."

    if [ -d "$APP_DIR/.git" ]; then
        log_info "更新现有代码..."
        cd "$APP_DIR"
        git pull origin master
    else
        log_info "克隆代码仓库..."
        rm -rf "$APP_DIR"
        git clone https://github.com/gggg826/AutoVideoWeb.git "$APP_DIR"
        cd "$APP_DIR"
    fi

    log_success "代码准备完成"
}

# 配置环境变量
configure_env() {
    log_info "配置环境变量..."

    # 生成随机SECRET_KEY
    SECRET_KEY=$(openssl rand -hex 32)

    # 提示用户输入管理员密码
    echo ""
    read -p "设置管理员密码 (留空使用默认: Admin@123): " ADMIN_PASSWORD
    ADMIN_PASSWORD=${ADMIN_PASSWORD:-Admin@123}

    # 更新docker-compose.yml中的环境变量
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/" docker-compose.yml
    sed -i "s/ADMIN_PASSWORD=.*/ADMIN_PASSWORD=${ADMIN_PASSWORD}/" docker-compose.yml

    log_success "环境变量配置完成"
    log_warning "请妥善保管管理员密码: ${ADMIN_PASSWORD}"
}

# 构建并启动应用
start_app() {
    log_info "构建Docker镜像..."
    cd "$APP_DIR"

    # 停止旧容器
    docker-compose down || true

    # 构建镜像
    docker-compose build

    log_info "启动应用容器..."
    docker-compose up -d

    # 等待应用启动
    log_info "等待应用启动..."
    sleep 10

    # 检查健康状态
    if docker-compose ps | grep -q "Up"; then
        log_success "应用启动成功！"
        docker-compose ps
    else
        log_error "应用启动失败，请检查日志"
        docker-compose logs
        exit 1
    fi
}

# 安装Nginx
install_nginx() {
    if command -v nginx &> /dev/null; then
        log_success "Nginx已安装"
        return 0
    fi

    log_info "安装Nginx..."
    yum install -y nginx
    systemctl enable nginx
    log_success "Nginx安装完成"
}

# 配置Nginx反向代理
configure_nginx() {
    log_info "配置Nginx反向代理..."

    if [ -z "$DOMAIN" ]; then
        log_warning "未配置域名，跳过Nginx配置"
        log_info "应用直接运行在端口 ${PORT}"
        return 0
    fi

    # 创建Nginx配置
    cat > /etc/nginx/conf.d/autovideoweb.conf <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    # 限制请求大小
    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:${PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

    # 测试Nginx配置
    nginx -t

    # 重启Nginx
    systemctl restart nginx

    log_success "Nginx配置完成"
}

# 安装SSL证书
install_ssl() {
    if [ -z "$DOMAIN" ]; then
        log_warning "未配置域名，跳过SSL证书安装"
        return 0
    fi

    log_info "安装Let's Encrypt SSL证书..."

    # 安装certbot
    if [ "$CENTOS_VERSION" -eq 7 ]; then
        yum install -y epel-release
        yum install -y certbot python2-certbot-nginx
    else
        yum install -y certbot python3-certbot-nginx
    fi

    # 获取证书
    certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email

    # 设置自动续期
    echo "0 0,12 * * * root python3 -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q" | tee -a /etc/crontab > /dev/null

    log_success "SSL证书安装完成"
}

# 显示部署信息
show_info() {
    echo ""
    echo "=========================================="
    log_success "${APP_NAME} 部署完成！"
    echo "=========================================="
    echo ""
    echo "📋 应用信息:"
    echo "  应用目录: ${APP_DIR}"
    echo "  数据目录: ${APP_DIR}/data"
    echo ""

    if [ -z "$DOMAIN" ]; then
        echo "🌐 访问地址:"
        echo "  主页:     http://$(hostname -I | awk '{print $1}'):${PORT}/"
        echo "  管理后台: http://$(hostname -I | awk '{print $1}'):${PORT}/admin/"
        echo "  API文档:  http://$(hostname -I | awk '{print $1}'):${PORT}/docs"
    else
        echo "🌐 访问地址:"
        echo "  主页:     https://${DOMAIN}/"
        echo "  管理后台: https://${DOMAIN}/admin/"
        echo "  API文档:  https://${DOMAIN}/docs"
    fi

    echo ""
    echo "🔐 管理员账号:"
    echo "  用户名: admin"
    echo "  密码:   ${ADMIN_PASSWORD}"
    echo ""
    echo "📦 Docker管理命令:"
    echo "  查看日志: cd ${APP_DIR} && docker-compose logs -f"
    echo "  重启服务: cd ${APP_DIR} && docker-compose restart"
    echo "  停止服务: cd ${APP_DIR} && docker-compose down"
    echo "  启动服务: cd ${APP_DIR} && docker-compose up -d"
    echo ""
    echo "🔄 更新应用:"
    echo "  cd ${APP_DIR}"
    echo "  git pull origin master"
    echo "  docker-compose down"
    echo "  docker-compose build"
    echo "  docker-compose up -d"
    echo ""
    echo "=========================================="
}

# 主函数
main() {
    echo ""
    echo "=========================================="
    echo "  ${APP_NAME} 一键部署脚本"
    echo "  支持: CentOS 7/8/9"
    echo "=========================================="
    echo ""

    # 询问是否配置域名
    read -p "是否配置域名和SSL证书? (y/N): " SETUP_DOMAIN
    if [[ "$SETUP_DOMAIN" =~ ^[Yy]$ ]]; then
        read -p "请输入域名 (例如: example.com): " DOMAIN
    fi

    echo ""
    log_info "开始部署流程..."
    echo ""

    check_root
    detect_os
    install_docker
    install_docker_compose
    install_git
    configure_firewall
    setup_app
    configure_env
    start_app

    # 如果配置了域名，安装Nginx和SSL
    if [ -n "$DOMAIN" ]; then
        install_nginx
        configure_nginx
        install_ssl
    fi

    show_info

    log_success "部署完成！"
}

# 执行主函数
main "$@"
