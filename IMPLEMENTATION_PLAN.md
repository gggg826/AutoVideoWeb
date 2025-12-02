# AdAllianceTools 测试网站 - 实施计划

## 1. 项目启动准备

### 1.1 环境准备检查清单

```bash
# Python 环境
□ Python 3.10+ 已安装
□ pip 已更新到最新版本
□ virtualenv 或 venv 可用

# 开发工具
□ Git 已安装并配置
□ VSCode/PyCharm 等 IDE 已安装
□ Postman/Insomnia API 测试工具
□ SQLite 查看器（DB Browser for SQLite）

# 可选工具
□ Docker Desktop（用于容器化部署）
□ Redis（Phase 2 功能）
□ PostgreSQL（Phase 2 功能）
```

### 1.2 依赖文件准备

#### backend/requirements.txt
```txt
# Web 框架
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# 数据库
sqlalchemy==2.0.25
alembic==1.13.1
aiosqlite==0.19.0

# 数据验证
pydantic==2.5.3
pydantic-settings==2.1.0
email-validator==2.1.0

# User-Agent 解析
user-agents==2.2.0

# 安全
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# 工具库
aiofiles==23.2.1
httpx==0.26.0

# 可选：IP 地理位置
# requests==2.31.0

# 可选：Redis 缓存
# redis==5.0.1
# hiredis==2.3.2
```

#### backend/requirements-dev.txt
```txt
-r requirements.txt

# 测试
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
pytest-mock==3.12.0

# 代码质量
black==24.1.1
flake8==7.0.0
mypy==1.8.0
isort==5.13.2

# 性能测试
locust==2.20.0

# 开发工具
ipython==8.20.0
ipdb==0.13.13
```

### 1.3 配置文件准备

#### .env（从 .env.example 复制并修改）
```env
# Application
APP_NAME=AdAllianceTools Test Site
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/tracker.db

# Security
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Admin@123456
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
ALLOWED_METHODS=GET,POST,PUT,DELETE
ALLOWED_HEADERS=*

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=150

# Analytics
CACHE_TTL=300
MAX_EXPORT_ROWS=10000
DATA_RETENTION_DAYS=90

# External APIs (Optional)
IP_API_KEY=
IP_API_PROVIDER=ipapi.co

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=json
LOG_FILE=data/logs/app.log

# WebSocket
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=100
```

## 2. 阶段性实施计划

### Phase 0: 项目初始化（Day 1）

#### 任务清单
```bash
# 1. 创建项目目录结构
mkdir -p backend/app/{core,models,schemas,crud,api/v1,services,utils}
mkdir -p backend/{migrations/versions,scripts,tests/{unit,integration,load}}
mkdir -p frontend/{public,admin,static/{css,js/{tracker,admin,utils},img}}
mkdir -p data/{exports/{csv,json},logs}
mkdir -p docker
mkdir -p docs

# 2. 初始化 Python 虚拟环境
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 3. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 初始化 Git
git init
git add .
git commit -m "Initial project structure"

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置必要的配置
```

#### 验收标准
- ✅ 所有目录结构创建完成
- ✅ Python 虚拟环境激活成功
- ✅ 所有依赖安装无错误
- ✅ Git 仓库初始化完成
- ✅ .env 文件配置完成

### Phase 1: 数据库和核心模型（Day 1-2）

#### 1.1 数据库配置

**文件**: `backend/app/core/database.py`
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# 创建异步会话工厂
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 模型基类
Base = declarative_base()

# 依赖注入：获取数据库会话
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

#### 1.2 配置管理

**文件**: `backend/app/config.py`
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AdAlliance Tracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # Cache
    CACHE_TTL: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

#### 1.3 数据模型

**文件**: `backend/app/models/visit.py`
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(String(64), unique=True, nullable=False, index=True)
    session_id = Column(String(64), index=True)

    # 时间
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # IP 信息
    ip_address = Column(String(45), nullable=False, index=True)
    ip_country = Column(String(2))
    ip_city = Column(String(100))
    is_proxy = Column(Boolean, default=False)
    is_datacenter = Column(Boolean, default=False)

    # 请求信息
    user_agent = Column(Text)
    referrer = Column(Text)
    page_url = Column(String(500), nullable=False)

    # 设备信息
    device_type = Column(String(20), index=True)
    browser = Column(String(50))
    browser_version = Column(String(20))
    os = Column(String(50))
    os_version = Column(String(20))

    # 浏览器指纹
    screen_resolution = Column(String(20))
    timezone = Column(String(50))
    language = Column(String(10))
    platform = Column(String(50))
    canvas_fingerprint = Column(String(64))
    webgl_fingerprint = Column(String(64))
    fonts_hash = Column(String(64))

    # 行为数据
    stay_duration = Column(Integer, default=0)
    scroll_depth = Column(Integer, default=0)
    mouse_movements = Column(Text)

    # 分析字段
    is_bot = Column(Boolean, default=False, index=True)
    authenticity_score = Column(Float, default=0.0, index=True)
    fingerprint_hash = Column(String(64), nullable=False, index=True)

    # 元数据
    raw_data = Column(Text)

    def __repr__(self):
        return f"<Visit {self.visit_id} - {self.ip_address}>"
```

#### 1.4 初始化脚本

**文件**: `backend/scripts/init_db.py`
```python
import asyncio
from app.core.database import engine, Base
from app.models.visit import Visit  # 导入所有模型

async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        # 删除所有表（仅开发环境）
        # await conn.run_sync(Base.metadata.drop_all)

        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
```

#### 验收标准
- ✅ 数据库连接配置正确
- ✅ 模型定义完整
- ✅ 初始化脚本运行成功
- ✅ 数据库表创建成功

### Phase 2: 追踪 API 实现（Day 2-3）

#### 2.1 Pydantic Schema

**文件**: `backend/app/schemas/visit.py`
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class VisitCreate(BaseModel):
    """创建访问记录的请求体"""
    # IP 自动获取
    user_agent: str
    referrer: Optional[str] = None
    page_url: str

    # 浏览器指纹
    screen_resolution: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    platform: Optional[str] = None
    canvas_fingerprint: Optional[str] = None
    webgl_fingerprint: Optional[str] = None
    fonts_hash: Optional[str] = None

    # 其他元数据
    extra_data: Optional[Dict[str, Any]] = None

class BehaviorUpdate(BaseModel):
    """更新行为数据的请求体"""
    visit_id: str
    stay_duration: Optional[int] = None
    scroll_depth: Optional[int] = None
    mouse_movements: Optional[str] = None

class VisitResponse(BaseModel):
    """访问记录响应"""
    visit_id: str
    timestamp: datetime
    ip_address: str
    device_type: Optional[str]
    authenticity_score: float

    class Config:
        from_attributes = True
```

#### 2.2 CRUD 操作

**文件**: `backend/app/crud/visit.py`
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.visit import Visit
from app.schemas.visit import VisitCreate, BehaviorUpdate
from typing import Optional
import uuid

async def create_visit(
    db: AsyncSession,
    visit_data: VisitCreate,
    ip_address: str
) -> Visit:
    """创建访问记录"""
    visit = Visit(
        visit_id=str(uuid.uuid4()),
        ip_address=ip_address,
        **visit_data.dict(exclude={'extra_data'}),
        raw_data=visit_data.json() if visit_data.extra_data else None
    )

    # TODO: 解析 User-Agent
    # TODO: 生成指纹哈希
    # TODO: 计算真实性评分

    db.add(visit)
    await db.commit()
    await db.refresh(visit)
    return visit

async def update_behavior(
    db: AsyncSession,
    behavior_data: BehaviorUpdate
) -> Optional[Visit]:
    """更新行为数据"""
    stmt = select(Visit).where(Visit.visit_id == behavior_data.visit_id)
    result = await db.execute(stmt)
    visit = result.scalar_one_or_none()

    if visit:
        if behavior_data.stay_duration is not None:
            visit.stay_duration = behavior_data.stay_duration
        if behavior_data.scroll_depth is not None:
            visit.scroll_depth = behavior_data.scroll_depth
        if behavior_data.mouse_movements is not None:
            visit.mouse_movements = behavior_data.mouse_movements

        await db.commit()
        await db.refresh(visit)

    return visit
```

#### 2.3 工具函数

**文件**: `backend/app/utils/ip.py`
```python
from fastapi import Request

def get_client_ip(request: Request) -> str:
    """获取客户端真实 IP"""
    # 优先检查代理头
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # 返回直接连接 IP
    return request.client.host if request.client else "unknown"
```

**文件**: `backend/app/utils/ua.py`
```python
from user_agents import parse

def parse_user_agent(ua_string: str) -> dict:
    """解析 User-Agent"""
    ua = parse(ua_string)

    return {
        "device_type": "mobile" if ua.is_mobile else "tablet" if ua.is_tablet else "pc",
        "browser": ua.browser.family,
        "browser_version": ua.browser.version_string,
        "os": ua.os.family,
        "os_version": ua.os.version_string,
        "is_bot": ua.is_bot,
    }
```

#### 2.4 API 路由

**文件**: `backend/app/api/v1/tracker.py`
```python
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.visit import VisitCreate, BehaviorUpdate, VisitResponse
from app.crud import visit as visit_crud
from app.utils.ip import get_client_ip

router = APIRouter(prefix="/track", tags=["tracker"])

@router.post("/", response_model=VisitResponse)
async def track_visit(
    visit_data: VisitCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """记录访问"""
    ip_address = get_client_ip(request)
    visit = await visit_crud.create_visit(db, visit_data, ip_address)

    return visit

@router.post("/behavior")
async def update_behavior(
    behavior_data: BehaviorUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新行为数据"""
    visit = await visit_crud.update_behavior(db, behavior_data)

    if not visit:
        return {"success": False, "error": "Visit not found"}

    return {"success": True, "message": "Behavior updated"}
```

#### 2.5 主应用

**文件**: `backend/app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api.v1 import tracker

# 创建应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(tracker.router, prefix="/api/v1")

# 静态文件服务
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
app.mount("/public", StaticFiles(directory="../frontend/public"), name="public")
app.mount("/admin", StaticFiles(directory="../frontend/admin"), name="admin")

@app.get("/")
async def root():
    return {"message": "AdAlliance Tracker API", "version": settings.APP_VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### 2.6 启动脚本

**文件**: `run.py`
```python
import uvicorn
from backend.app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
```

#### 验收标准
- ✅ API 启动成功
- ✅ `/api/v1/track` 端点可访问
- ✅ 数据成功写入数据库
- ✅ Swagger 文档可访问 (`/docs`)

### Phase 3: 前端追踪脚本（Day 3-4）

#### 3.1 指纹采集脚本

**文件**: `frontend/static/js/tracker/fingerprint.js`
```javascript
// 浏览器指纹采集
const FingerprintCollector = {
  // Canvas 指纹
  getCanvasFingerprint() {
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = 200;
      canvas.height = 50;

      ctx.textBaseline = 'top';
      ctx.font = '14px Arial';
      ctx.fillStyle = '#f60';
      ctx.fillRect(0, 0, 100, 50);
      ctx.fillStyle = '#069';
      ctx.fillText('AdAlliance 🎨', 2, 15);

      return this.hashCode(canvas.toDataURL());
    } catch (e) {
      return null;
    }
  },

  // WebGL 指纹
  getWebGLFingerprint() {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

      if (!gl) return null;

      const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
      const vendor = debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : '';
      const renderer = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : '';

      return this.hashCode(vendor + renderer);
    } catch (e) {
      return null;
    }
  },

  // 字体检测
  getFontsHash() {
    const baseFonts = ['monospace', 'sans-serif', 'serif'];
    const testFonts = [
      'Arial', 'Verdana', 'Times New Roman', 'Courier New',
      'Georgia', 'Palatino', 'Garamond', 'Comic Sans MS',
      'Trebuchet MS', 'Arial Black', 'Impact'
    ];

    const detectedFonts = [];

    for (const font of testFonts) {
      if (this.isFontAvailable(font, baseFonts)) {
        detectedFonts.push(font);
      }
    }

    return this.hashCode(detectedFonts.join(','));
  },

  isFontAvailable(fontName, baseFonts) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const text = 'mmmmmmmmmmlli';

    ctx.font = '72px ' + baseFonts[0];
    const baseWidth = ctx.measureText(text).width;

    ctx.font = '72px ' + fontName + ', ' + baseFonts[0];
    const testWidth = ctx.measureText(text).width;

    return baseWidth !== testWidth;
  },

  // 简单哈希函数
  hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(16);
  },

  // 收集所有指纹
  async collect() {
    return {
      canvas_fingerprint: this.getCanvasFingerprint(),
      webgl_fingerprint: this.getWebGLFingerprint(),
      fonts_hash: this.getFontsHash(),
      screen_resolution: `${screen.width}x${screen.height}`,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      language: navigator.language,
      platform: navigator.platform,
    };
  }
};
```

#### 3.2 主追踪脚本

**文件**: `frontend/static/js/tracker/tracker.js`
```javascript
// AdAlliance 追踪器
(function() {
  'use strict';

  const API_BASE = window.location.origin + '/api/v1';
  let visitId = null;
  let startTime = Date.now();
  let maxScrollDepth = 0;
  let mouseMoves = [];

  // 初始化
  async function init() {
    try {
      // 采集指纹
      const fingerprint = await FingerprintCollector.collect();

      // 发送初始追踪请求
      const response = await fetch(`${API_BASE}/track/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_agent: navigator.userAgent,
          referrer: document.referrer || null,
          page_url: window.location.href,
          ...fingerprint
        })
      });

      const data = await response.json();
      visitId = data.visit_id;

      // 监听行为事件
      setupEventListeners();

      console.log('✅ AdAlliance Tracker initialized');
    } catch (error) {
      console.error('❌ Tracker initialization failed:', error);
    }
  }

  // 设置事件监听
  function setupEventListeners() {
    // 滚动深度
    let scrollTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const scrolled = window.scrollY;
        const total = document.documentElement.scrollHeight - window.innerHeight;
        const depth = Math.round((scrolled / total) * 100);
        maxScrollDepth = Math.max(maxScrollDepth, depth || 0);
      }, 100);
    });

    // 鼠标移动（采样）
    let mouseTimeout;
    window.addEventListener('mousemove', (e) => {
      clearTimeout(mouseTimeout);
      mouseTimeout = setTimeout(() => {
        mouseMoves.push({ x: e.clientX, y: e.clientY, t: Date.now() - startTime });
        // 限制数组大小
        if (mouseMoves.length > 50) {
          mouseMoves = mouseMoves.slice(-50);
        }
      }, 200);
    });

    // 页面卸载时发送数据
    window.addEventListener('beforeunload', sendBehaviorData);
    window.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        sendBehaviorData();
      }
    });
  }

  // 发送行为数据
  function sendBehaviorData() {
    if (!visitId) return;

    const duration = Math.round((Date.now() - startTime) / 1000);

    const data = {
      visit_id: visitId,
      stay_duration: duration,
      scroll_depth: maxScrollDepth,
      mouse_movements: JSON.stringify(mouseMoves.slice(-20))
    };

    // 使用 sendBeacon 确保数据发送
    if (navigator.sendBeacon) {
      navigator.sendBeacon(
        `${API_BASE}/track/behavior`,
        JSON.stringify(data)
      );
    } else {
      fetch(`${API_BASE}/track/behavior`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        keepalive: true
      });
    }
  }

  // DOM 加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

#### 3.3 测试页面

**文件**: `frontend/public/index.html`
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AdAlliance - 测试主页</title>
    <link rel="stylesheet" href="/static/css/public.css">
</head>
<body>
    <header>
        <h1>🎯 AdAlliance 测试网站</h1>
        <p>用于测试流量生成工具的效果</p>
    </header>

    <main>
        <section class="hero">
            <h2>欢迎访问测试页面</h2>
            <p>此页面用于测试浏览器指纹伪装和行为模拟效果</p>
        </section>

        <section class="content">
            <h3>功能说明</h3>
            <ul>
                <li>自动采集浏览器指纹信息</li>
                <li>记录用户行为数据（滚动、鼠标移动）</li>
                <li>统计页面停留时间</li>
                <li>检测代理和异常访问</li>
            </ul>
        </section>

        <section class="links">
            <h3>其他测试页面</h3>
            <a href="/public/landing.html">着陆页</a>
            <a href="/public/ad-page.html">广告页</a>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 AdAlliance Tools</p>
    </footer>

    <!-- 追踪脚本 -->
    <script src="/static/js/tracker/fingerprint.js"></script>
    <script src="/static/js/tracker/tracker.js"></script>
</body>
</html>
```

#### 验收标准
- ✅ 测试页面可访问
- ✅ tracker.js 自动加载
- ✅ 指纹数据成功采集
- ✅ 行为数据成功上报

## 3. 后续阶段概览

### Week 2: 管理后台（P1）
- 仪表盘页面（实时统计）
- 访问日志列表（DataTables）
- 统计分析 API
- Chart.js 图表集成

### Week 3: 高级功能（P1）
- 异常检测算法
- 真实性评分系统
- 地理分布分析
- 数据导出功能

### Week 4: 优化和部署（P2）
- 性能优化（索引、缓存）
- WebSocket 实时推送
- Docker 容器化
- 负载测试

## 4. 开发规范和最佳实践

### 4.1 代码风格
```bash
# 格式化代码
black backend/

# 检查代码质量
flake8 backend/app
mypy backend/app

# 排序导入
isort backend/app
```

### 4.2 Git 提交规范
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建/工具配置

示例：
feat(tracker): add canvas fingerprint collection
fix(api): handle missing user-agent gracefully
docs: update API documentation
```

### 4.3 测试规范
```python
# 测试文件命名: test_*.py
# 测试类命名: Test*
# 测试函数命名: test_*

# 示例
async def test_create_visit(db_session):
    """测试创建访问记录"""
    visit_data = VisitCreate(
        user_agent="Mozilla/5.0...",
        page_url="https://example.com"
    )
    visit = await create_visit(db_session, visit_data, "1.2.3.4")

    assert visit.visit_id is not None
    assert visit.ip_address == "1.2.3.4"
```

## 5. 常见问题和解决方案

### 5.1 数据库连接问题
```python
# 问题：asyncio event loop closed
# 解决：使用 asyncio.run() 或正确的事件循环管理

# 问题：SQLite 并发写入错误
# 解决：使用连接池或切换到 PostgreSQL
```

### 5.2 CORS 问题
```python
# 问题：前端无法调用 API
# 解决：检查 ALLOWED_ORIGINS 配置
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### 5.3 静态文件 404
```python
# 问题：静态文件路径不正确
# 解决：检查 StaticFiles 目录配置
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
```

## 6. 下一步行动

### 立即开始
1. ✅ 复制此实施计划到本地
2. ✅ 按照 Phase 0 创建项目结构
3. ✅ 安装依赖并初始化数据库
4. ✅ 实现 Phase 1 数据库和模型
5. ✅ 实现 Phase 2 追踪 API
6. ✅ 测试 API 端点
7. ✅ 实现 Phase 3 前端追踪脚本
8. ✅ 端到端测试

### 每日检查
- [ ] 代码已格式化（black）
- [ ] 测试已通过（pytest）
- [ ] 文档已更新
- [ ] Git 提交清晰
- [ ] TASKS.md 已更新进度

---

**文档版本**: 1.0
**创建日期**: 2025-12-02
**适用阶段**: Week 1 - 基础设施搭建
