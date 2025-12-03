# AutoVideoWeb Windows 部署指南

## 🚀 快速部署 (Windows)

### 前置要求

- **操作系统**: Windows 10/11 (64位)
- **Docker Desktop**: [下载安装](https://www.docker.com/products/docker-desktop)
- **内存**: 至少4GB RAM
- **磁盘**: 至少10GB可用空间

---

## 📦 方式一：一键部署脚本 (推荐)

### 使用批处理脚本 (.bat)

适合不熟悉PowerShell的用户：

```batch
# 1. 克隆代码 (或下载ZIP解压)
git clone https://github.com/gggg826/AutoVideoWeb.git
cd AutoVideoWeb

# 2. 运行部署脚本
Deploy\Windows\deploy.bat
```

### 使用PowerShell脚本 (.ps1)

功能更强大，推荐高级用户使用：

```powershell
# 1. 克隆代码
git clone https://github.com/gggg826/AutoVideoWeb.git
cd AutoVideoWeb

# 2. 允许执行PowerShell脚本 (仅需首次执行)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 3. 以管理员身份运行PowerShell，然后执行：
.\Deploy\Windows\deploy.ps1
```

部署脚本会自动完成：
- ✅ 检查Docker Desktop安装和运行状态
- ✅ 检查项目文件完整性
- ✅ 生成安全密钥
- ✅ 构建Docker镜像
- ✅ 启动容器
- ✅ 健康检查

**部署时间**: 约3-5分钟 (首次构建)

---

## 🛠️ 方式二：手动Docker部署

### 步骤1：安装Docker Desktop

1. 下载：https://www.docker.com/products/docker-desktop
2. 运行安装程序
3. 重启电脑
4. 启动Docker Desktop
5. 等待Docker Desktop完全启动（系统托盘显示Docker图标）

### 步骤2：克隆代码

```batch
# 使用Git
git clone https://github.com/gggg826/AutoVideoWeb.git
cd AutoVideoWeb

# 或直接下载ZIP
# https://github.com/gggg826/AutoVideoWeb/archive/refs/heads/master.zip
```

### 步骤3：配置环境变量 (可选)

编辑 `docker-compose.yml`，修改以下环境变量：

```yaml
environment:
  - SECRET_KEY=your-secret-key-here  # 建议修改
  - ADMIN_PASSWORD=your-password     # 建议修改
```

### 步骤4：启动服务

```batch
# 构建并启动
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 步骤5：访问应用

- **主页**: http://localhost:8000/
- **管理后台**: http://localhost:8000/admin/
- **API文档**: http://localhost:8000/docs

---

## 📋 部署后配置

### 默认管理员账号

- **用户名**: `admin`
- **密码**: `Admin@123` (生产环境请修改！)

### 修改管理员密码

编辑 `docker-compose.yml`:

```yaml
environment:
  - ADMIN_PASSWORD=your-new-password
```

然后重启服务：

```batch
docker-compose down
docker-compose up -d
```

---

## 🔧 常用管理命令

### Docker Compose 命令

```batch
# 查看运行状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 启动服务
docker-compose up -d

# 强制重新构建
docker-compose build --no-cache
docker-compose up -d
```

### 数据管理

```batch
# 数据备份（PowerShell）
Copy-Item .\data\visits.db .\backup\visits_$(Get-Date -Format 'yyyyMMdd').db

# 数据备份（批处理）
copy data\visits.db backup\visits_%date:~0,4%%date:~5,2%%date:~8,2%.db

# 数据恢复
docker-compose down
copy backup\visits_20240101.db data\visits.db
docker-compose up -d
```

### 应用更新

```batch
# 拉取最新代码
git pull origin master

# 重新构建并启动
docker-compose down
docker-compose build
docker-compose up -d

# 查看日志确认
docker-compose logs -f
```

---

## 🌐 网络访问配置

### 局域网访问

默认情况下，应用只能从本机访问。要允许局域网内其他设备访问：

1. **查找本机IP地址**:
   ```batch
   ipconfig
   ```
   找到"IPv4 地址"，例如：`192.168.1.100`

2. **配置防火墙规则** (以管理员身份运行):
   ```batch
   netsh advfirewall firewall add rule name="AutoVideoWeb" dir=in action=allow protocol=TCP localport=8000
   ```

3. **访问地址**:
   - 从其他设备：`http://192.168.1.100:8000/`

### 使用自定义域名 (可选)

编辑 `C:\Windows\System32\drivers\etc\hosts` (需要管理员权限):

```
127.0.0.1 autovideoweb.local
```

然后可以通过 `http://autovideoweb.local:8000/` 访问

---

## 🔒 安全建议

### 1. 修改默认密码

**强烈建议**在生产环境修改默认管理员密码：

```yaml
# docker-compose.yml
environment:
  - ADMIN_PASSWORD=Strong@Password123
```

### 2. 修改密钥

生成新的SECRET_KEY：

```powershell
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

```batch
REM 批处理 - 使用在线生成器
REM https://generate-secret.now.sh/32
```

### 3. 数据目录权限

确保 `data` 目录只有必要的用户可以访问：

```batch
REM 以管理员身份运行
icacls data /inheritance:r
icacls data /grant:r "%USERNAME%:(OI)(CI)F"
```

---

## 📊 性能优化

### Docker Desktop 资源设置

1. 打开Docker Desktop
2. 进入 **Settings** → **Resources**
3. 调整资源分配：
   - **CPU**: 推荐2核以上
   - **Memory**: 推荐2GB以上
   - **Disk**: 至少20GB

### WSL 2 优化 (推荐)

Docker Desktop在Windows上推荐使用WSL 2后端：

1. 安装WSL 2:
   ```batch
   wsl --install
   ```

2. 在Docker Desktop中启用：
   **Settings** → **General** → **Use WSL 2 based engine**

---

## 🐛 故障排查

### Docker Desktop 未启动

**症状**: 运行部署脚本时提示"Docker未安装或未启动"

**解决**:
1. 检查系统托盘是否有Docker图标
2. 手动启动Docker Desktop
3. 等待Docker完全启动（图标变为绿色）
4. 重新运行部署脚本

### 端口被占用

**症状**: 错误信息包含"port is already allocated"

**解决**:
```batch
# 查找占用8000端口的进程
netstat -ano | findstr :8000

# 结束进程 (PID为查询到的进程ID)
taskkill /PID <进程ID> /F

# 或修改端口
# 编辑 docker-compose.yml:
ports:
  - "9000:8000"  # 改为9000端口
```

### 容器无法启动

**症状**: `docker-compose ps` 显示容器状态为 "Exit"

**解决**:
```batch
# 查看详细日志
docker-compose logs

# 删除所有容器和镜像重新构建
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

### 磁盘空间不足

**症状**: 构建失败，提示空间不足

**解决**:
```batch
# 清理未使用的Docker资源
docker system prune -a

# 查看Docker占用空间
docker system df

# 移动Docker数据目录
# 在Docker Desktop中: Settings → Resources → Advanced → Disk image location
```

### 访问被拒绝

**症状**: 浏览器显示"无法访问此网站"

**解决**:
1. 检查容器是否运行: `docker-compose ps`
2. 检查防火墙设置
3. 尝试使用 `http://127.0.0.1:8000` 而不是 `localhost`
4. 检查Docker Desktop的网络设置

---

## 📈 监控和维护

### 查看资源使用

```batch
# 查看容器资源使用
docker stats

# 查看容器详细信息
docker-compose ps
docker inspect autovideoweb
```

### 日志管理

```batch
# 查看实时日志
docker-compose logs -f

# 查看特定时间的日志
docker-compose logs --since 1h

# 导出日志
docker-compose logs > logs\app_%date:~0,4%%date:~5,2%%date:~8,2%.log
```

### 自动备份脚本

创建 `backup.bat`:

```batch
@echo off
SET BACKUP_DIR=backup
SET DATE=%date:~0,4%%date:~5,2%%date:~8,2%

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%
copy data\visits.db %BACKUP_DIR%\visits_%DATE%.db

REM 删除7天前的备份
forfiles /p %BACKUP_DIR% /m visits_*.db /d -7 /c "cmd /c del @path"
```

使用任务计划程序设置每日自动备份：
```batch
schtasks /create /tn "AutoVideoWeb Backup" /tr "C:\path\to\backup.bat" /sc daily /st 02:00
```

---

## 🔄 卸载

### 完全卸载步骤

```batch
# 1. 停止并删除容器
docker-compose down -v

# 2. 删除镜像
docker rmi autovideoweb_web

# 3. 删除项目文件夹
cd ..
rmdir /s /q AutoVideoWeb

# 4. (可选) 卸载Docker Desktop
# 通过Windows设置 → 应用 → Docker Desktop → 卸载
```

---

## 📞 技术支持

- **GitHub仓库**: https://github.com/gggg826/AutoVideoWeb
- **问题反馈**: https://github.com/gggg826/AutoVideoWeb/issues
- **Linux部署**: 查看 [Deploy/Linux/DEPLOYMENT.md](../Linux/DEPLOYMENT.md)

---

## 💡 提示

### Windows特有注意事项

1. **路径分隔符**: Windows使用反斜杠 `\`，命令行中注意路径格式
2. **换行符**: 建议使用支持CRLF的编辑器
3. **权限**: 某些操作需要管理员权限
4. **防火墙**: Windows Defender可能拦截端口，需要手动允许
5. **WSL 2**: 推荐使用WSL 2作为Docker后端，性能更好

### 开发环境

如需在Windows上进行开发：

```batch
# 1. 创建虚拟环境
python -m venv backend\.venv

# 2. 激活虚拟环境
backend\.venv\Scripts\activate

# 3. 安装依赖
pip install -r backend\requirements.txt

# 4. 运行开发服务器
python run.py
```

---

## 📄 许可证

本项目遵循 MIT 许可证。
