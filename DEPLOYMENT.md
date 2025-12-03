# AutoVideoWeb 生产环境部署指南

## 🚀 快速部署 (CentOS)

### 方式一：一键部署脚本

```bash
# 1. 下载部署脚本
wget https://raw.githubusercontent.com/gggg826/AutoVideoWeb/master/deploy.sh

# 2. 赋予执行权限
chmod +x deploy.sh

# 3. 运行部署脚本 (需要root权限)
sudo bash deploy.sh
```

部署脚本会自动完成：
- ✅ 检测系统环境 (CentOS 7/8/9)
- ✅ 安装Docker和Docker Compose
- ✅ 配置防火墙规则 (端口8000, 80, 443)
- ✅ 克隆代码仓库
- ✅ 生成安全密钥
- ✅ 构建并启动Docker容器
- ✅ 配置Nginx反向代理 (可选)
- ✅ 安装Let's Encrypt SSL证书 (可选)

### 方式二：手动Docker部署

```bash
# 1. 安装Docker和Docker Compose
sudo yum install -y docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# 2. 克隆代码
git clone https://github.com/gggg826/AutoVideoWeb.git
cd AutoVideoWeb

# 3. 配置环境变量 (可选)
# 编辑 docker-compose.yml 修改以下变量:
# - SECRET_KEY: 密钥 (建议修改)
# - ADMIN_PASSWORD: 管理员密码 (建议修改)

# 4. 启动服务
docker-compose up -d

# 5. 查看运行状态
docker-compose ps
docker-compose logs -f
```

---

## 📋 部署后配置

### 访问地址

- **主页**: http://your-server-ip:8000/
- **测试页面**: http://your-server-ip:8000/public/index.html
- **管理后台**: http://your-server-ip:8000/admin/
- **API文档**: http://your-server-ip:8000/docs

### 默认管理员账号

- **用户名**: `admin`
- **密码**: `Admin@123` (生产环境请修改！)

---

## 🔧 常用管理命令

### Docker Compose命令

```bash
cd /opt/autovideoweb  # 进入应用目录

# 查看运行状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 启动服务
docker-compose up -d

# 重新构建并启动
docker-compose down
docker-compose build
docker-compose up -d
```

### 数据备份

```bash
# 备份数据库
cp /opt/autovideoweb/data/visits.db /backup/visits_$(date +%Y%m%d).db

# 恢复数据库
docker-compose down
cp /backup/visits_20240101.db /opt/autovideoweb/data/visits.db
docker-compose up -d
```

### 应用更新

```bash
cd /opt/autovideoweb

# 拉取最新代码
git pull origin master

# 重新构建并启动
docker-compose down
docker-compose build
docker-compose up -d

# 查看日志确认启动成功
docker-compose logs -f
```

---

## 🔒 安全加固建议

### 1. 修改默认管理员密码

编辑 `docker-compose.yml`:
```yaml
environment:
  - ADMIN_PASSWORD=your-strong-password-here
```

然后重启：
```bash
docker-compose down
docker-compose up -d
```

### 2. 配置SSL证书 (HTTPS)

#### 使用Let's Encrypt (推荐)

部署脚本会自动配置，或手动执行：

```bash
# 安装certbot
sudo yum install -y certbot python3-certbot-nginx

# 获取证书 (替换your-domain.com为你的域名)
sudo certbot --nginx -d your-domain.com

# 设置自动续期
echo "0 0,12 * * * root certbot renew -q" | sudo tee -a /etc/crontab
```

#### Nginx反向代理配置

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. 配置防火墙

```bash
# 只开放必要端口
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp  # 可选，如果不使用Nginx
sudo firewall-cmd --reload

# 限制8000端口仅本地访问 (使用Nginx时)
sudo firewall-cmd --permanent --remove-port=8000/tcp
sudo firewall-cmd --reload
```

### 4. 设置环境变量

生产环境中，建议使用环境文件管理敏感配置：

创建 `.env` 文件：
```bash
# 应用配置
APP_NAME=AutoVideoWeb
ENVIRONMENT=production
DEBUG=false

# 数据库
DATABASE_URL=sqlite+aiosqlite:///./data/visits.db

# 安全密钥 (务必修改！)
SECRET_KEY=$(openssl rand -hex 32)

# 管理员账号
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password

# JWT令牌过期时间 (分钟)
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

修改 `docker-compose.yml` 使用环境文件：
```yaml
services:
  web:
    env_file:
      - .env
```

---

## 📊 性能优化

### 1. 数据库优化

项目已自动配置以下数据库索引：
- 时间+设备类型索引 (访问列表查询)
- 时间+评分索引 (评分筛选)
- 地理位置索引 (位置统计)
- 机器人检测索引

### 2. IP地理位置缓存

已自动启用24小时内存缓存，减少外部API调用。

### 3. Docker资源限制

编辑 `docker-compose.yml` 添加资源限制：
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          memory: 512M
```

---

## 🐛 故障排查

### 查看日志

```bash
# 查看应用日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100

# 查看特定服务日志
docker-compose logs web
```

### 容器无法启动

```bash
# 检查容器状态
docker-compose ps

# 查看详细错误
docker-compose logs

# 重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 端口被占用

```bash
# 检查8000端口占用
sudo netstat -tulpn | grep 8000

# 修改端口
# 编辑 docker-compose.yml:
ports:
  - "9000:8000"  # 改为9000端口
```

### 数据库权限问题

```bash
# 修复数据目录权限
sudo chown -R 1000:1000 /opt/autovideoweb/data
sudo chmod -R 755 /opt/autovideoweb/data
```

### 健康检查失败

```bash
# 手动检查健康状态
curl http://localhost:8000/health

# 进入容器调试
docker-compose exec web bash
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

---

## 📈 监控和维护

### 日志轮转

创建 `/etc/logrotate.d/autovideoweb`:
```
/opt/autovideoweb/data/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### 自动备份脚本

创建 `/root/backup_autovideoweb.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backup/autovideoweb"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp /opt/autovideoweb/data/visits.db $BACKUP_DIR/visits_$DATE.db

# 保留最近7天的备份
find $BACKUP_DIR -name "visits_*.db" -mtime +7 -delete
```

添加到crontab (每天凌晨2点备份):
```bash
0 2 * * * /bin/bash /root/backup_autovideoweb.sh
```

### 监控磁盘空间

```bash
# 检查数据目录大小
du -sh /opt/autovideoweb/data

# 监控Docker占用空间
docker system df

# 清理未使用的Docker资源
docker system prune -a
```

---

## 🔄 系统要求

### 最低配置
- CPU: 1核
- 内存: 1GB
- 磁盘: 10GB
- 系统: CentOS 7/8/9, Ubuntu 20.04+, Debian 10+

### 推荐配置
- CPU: 2核+
- 内存: 2GB+
- 磁盘: 20GB+
- 系统: CentOS 8/9, Ubuntu 22.04

---

## 📞 技术支持

- **GitHub仓库**: https://github.com/gggg826/AutoVideoWeb
- **问题反馈**: https://github.com/gggg826/AutoVideoWeb/issues
- **文档**: https://github.com/gggg826/AutoVideoWeb/blob/master/README.md

---

## 📄 许可证

本项目遵循 MIT 许可证。
