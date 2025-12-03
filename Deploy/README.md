# AutoVideoWeb 部署文件

本目录包含AutoVideoWeb在不同平台上的部署脚本和文档。

## 📁 目录结构

```
Deploy/
├── Linux/              # Linux系统部署
│   ├── deploy.sh       # CentOS一键部署脚本
│   └── DEPLOYMENT.md   # Linux详细部署文档
│
└── Windows/            # Windows系统部署
    ├── deploy.bat      # Windows批处理部署脚本
    ├── deploy.ps1      # Windows PowerShell部署脚本
    └── DEPLOYMENT.md   # Windows详细部署文档
```

## 🚀 快速开始

### Linux (CentOS 7/8/9)

```bash
# 下载并运行部署脚本
wget https://raw.githubusercontent.com/gggg826/AutoVideoWeb/master/Deploy/Linux/deploy.sh
chmod +x deploy.sh
sudo bash deploy.sh
```

**详细文档**: [Linux/DEPLOYMENT.md](Linux/DEPLOYMENT.md)

### Windows (10/11)

```batch
# 克隆代码后运行
git clone https://github.com/gggg826/AutoVideoWeb.git
cd AutoVideoWeb
Deploy\Windows\deploy.bat
```

**详细文档**: [Windows/DEPLOYMENT.md](Windows/DEPLOYMENT.md)

## 📋 部署方式对比

| 特性 | Linux | Windows |
|------|-------|---------|
| **部署方式** | 一键脚本 | 批处理/PowerShell |
| **容器化** | Docker/Docker Compose | Docker Desktop |
| **Web服务器** | 可选Nginx反向代理 | 直接访问或IIS反向代理 |
| **SSL证书** | Let's Encrypt自动配置 | 手动配置或使用反向代理 |
| **进程管理** | systemd | Docker Desktop自动管理 |
| **适用场景** | 生产服务器 | 开发/测试环境 |

## 🔧 部署要求

### 通用要求

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **内存**: 至少1GB (推荐2GB+)
- **磁盘**: 至少10GB可用空间
- **网络**: 需要访问GitHub和Docker Hub

### Linux特定要求

- **系统**: CentOS 7/8/9, Ubuntu 20.04+, Debian 10+
- **权限**: root或sudo权限
- **端口**: 8000 (应用), 80 (HTTP), 443 (HTTPS)

### Windows特定要求

- **系统**: Windows 10 64位 (1903+) 或 Windows 11
- **Docker Desktop**: 最新版本
- **内存**: 至少4GB RAM
- **Hyper-V**: 需要启用或WSL 2

## 🌐 部署后访问

部署完成后，可通过以下地址访问：

- **主页**: http://your-ip:8000/
- **测试页面**: http://your-ip:8000/public/index.html
- **管理后台**: http://your-ip:8000/admin/
- **API文档**: http://your-ip:8000/docs

## 🔐 默认账号

- **用户名**: admin
- **密码**: Admin@123

⚠️ **生产环境请务必修改默认密码！**

## 📊 功能特性

### Linux部署特性

- ✅ 自动检测系统版本
- ✅ 自动安装Docker环境
- ✅ 自动配置防火墙
- ✅ 可选Nginx反向代理
- ✅ 可选SSL证书配置
- ✅ 完整的健康检查
- ✅ 自动重启策略

### Windows部署特性

- ✅ Docker Desktop集成
- ✅ 图形化管理界面
- ✅ 完整的错误提示
- ✅ PowerShell高级功能
- ✅ 批处理简易部署
- ✅ 局域网访问配置

## 🛠️ 常用命令

### 查看状态

```bash
# Linux/Windows通用
docker-compose ps
docker-compose logs -f
```

### 重启服务

```bash
# Linux/Windows通用
cd /opt/autovideoweb  # Linux
cd C:\path\to\AutoVideoWeb  # Windows

docker-compose restart
```

### 更新应用

```bash
# Linux/Windows通用
git pull origin master
docker-compose down
docker-compose build
docker-compose up -d
```

## 🔄 数据备份

### Linux

```bash
# 备份
cp /opt/autovideoweb/data/visits.db /backup/visits_$(date +%Y%m%d).db

# 恢复
docker-compose down
cp /backup/visits_20240101.db /opt/autovideoweb/data/visits.db
docker-compose up -d
```

### Windows

```powershell
# 备份 (PowerShell)
Copy-Item .\data\visits.db .\backup\visits_$(Get-Date -Format 'yyyyMMdd').db

# 恢复
docker-compose down
Copy-Item .\backup\visits_20240101.db .\data\visits.db
docker-compose up -d
```

## 🐛 故障排查

### 常见问题

1. **Docker未安装或未启动**
   - Linux: 运行部署脚本会自动安装
   - Windows: 手动启动Docker Desktop

2. **端口被占用**
   ```bash
   # 修改 docker-compose.yml 中的端口配置
   ports:
     - "9000:8000"  # 改为其他端口
   ```

3. **容器无法启动**
   ```bash
   docker-compose logs  # 查看错误日志
   docker-compose down -v  # 清理后重试
   docker-compose up -d
   ```

### 获取帮助

- 查看详细部署文档：[Linux](Linux/DEPLOYMENT.md) | [Windows](Windows/DEPLOYMENT.md)
- GitHub Issues: https://github.com/gggg826/AutoVideoWeb/issues

## 📄 其他部署方式

### 使用Docker直接部署

```bash
# 构建镜像
docker build -t autovideoweb .

# 运行容器
docker run -d \
  --name autovideoweb \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  autovideoweb
```

### 使用Kubernetes

参考项目根目录的 `k8s/` 文件夹（如有）

### 云平台部署

- **阿里云**: 使用容器镜像服务 + ECS
- **腾讯云**: 使用容器服务 + CVM
- **AWS**: 使用ECS/EKS
- **Azure**: 使用Container Instances

## 📞 技术支持

- **项目主页**: https://github.com/gggg826/AutoVideoWeb
- **问题反馈**: https://github.com/gggg826/AutoVideoWeb/issues
- **项目文档**: https://github.com/gggg826/AutoVideoWeb/blob/master/README.md

---

**提示**: 首次部署建议先阅读对应平台的详细部署文档。
