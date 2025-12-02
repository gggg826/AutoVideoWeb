# AdAllianceTools 测试网站 - 架构设计文档

## 1. 项目概述

这是一个用于测试流量生成工具效果的 Web 应用，核心功能包括访问追踪、行为分析和异常检测。

### 1.1 核心目标
- **追踪精度**: 准确记录访问者的完整指纹信息
- **实时性**: 支持实时数据展示和推送
- **高性能**: 支持 1000+ 并发访问
- **可扩展**: 易于添加新的检测指标和分析维度

## 2. 技术栈选择

### 2.1 后端技术栈

| 技术 | 版本 | 选择理由 |
|------|------|----------|
| **Python** | 3.10+ | 丰富的数据处理库，开发效率高 |
| **FastAPI** | 0.109+ | 高性能异步框架，自动生成 API 文档 |
| **SQLite** | 3.40+ | 轻量级，适合初期开发和测试 |
| **SQLAlchemy** | 2.0+ | 强大的 ORM，支持多数据库切换 |
| **Pydantic** | 2.5+ | 数据验证和序列化 |
| **Uvicorn** | 0.27+ | 高性能 ASGI 服务器 |
| **user-agents** | 2.2+ | User-Agent 解析 |
| **aiofiles** | 23.2+ | 异步文件操作 |
| **python-multipart** | 0.0.6+ | 文件上传支持 |

#### 可选依赖
- **Redis**: 缓存和实时推送（Phase 2）
- **PostgreSQL**: 大数据量场景（Phase 2）
- **ipapi**: IP 地理位置查询

### 2.2 前端技术栈

| 技术 | 版本 | 选择理由 |
|------|------|----------|
| **原生 HTML5** | - | 简单直接，无需构建工具 |
| **CSS3** | - | 现代布局特性（Grid/Flexbox） |
| **Vanilla JS** | ES6+ | 轻量，无框架依赖 |
| **Chart.js** | 4.4+ | 轻量级图表库 |
| **DataTables** | 1.13+ | 强大的表格组件 |
| **FingerprintJS** | 4.2+ | 浏览器指纹采集 |

#### CSS 框架选择
**推荐**: Tailwind CSS CDN 或 Bootstrap 5
- Tailwind: 现代、灵活、体积小
- Bootstrap: 组件丰富、上手快

### 2.3 开发工具

| 工具 | 用途 |
|------|------|
| **pytest** | 单元测试和集成测试 |
| **black** | 代码格式化 |
| **flake8** | 代码检查 |
| **mypy** | 类型检查 |
| **Locust** | 性能测试 |

## 3. 优化的目录结构

```
AutoVideoWeb/
├── backend/                          # 后端代码
│   ├── app/
│   │   ├── __init__.py              # 应用工厂
│   │   ├── main.py                  # FastAPI 应用入口
│   │   ├── config.py                # 配置管理（使用 pydantic-settings）
│   │   │
│   │   ├── core/                    # 核心模块
│   │   │   ├── __init__.py
│   │   │   ├── database.py         # 数据库连接和会话管理
│   │   │   ├── security.py         # 认证和授权
│   │   │   └── cache.py            # 缓存管理（内存/Redis）
│   │   │
│   │   ├── models/                  # SQLAlchemy 模型
│   │   │   ├── __init__.py
│   │   │   ├── visit.py            # 访问记录模型
│   │   │   └── analytics.py        # 统计汇总模型
│   │   │
│   │   ├── schemas/                 # Pydantic 模式
│   │   │   ├── __init__.py
│   │   │   ├── visit.py            # 访问记录 Schema
│   │   │   ├── analytics.py        # 统计数据 Schema
│   │   │   └── common.py           # 通用 Schema（分页、响应）
│   │   │
│   │   ├── crud/                    # 数据库操作
│   │   │   ├── __init__.py
│   │   │   ├── visit.py            # 访问记录 CRUD
│   │   │   └── analytics.py        # 统计数据 CRUD
│   │   │
│   │   ├── api/                     # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── deps.py             # 依赖注入（数据库会话、认证）
│   │   │   ├── v1/                 # API v1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tracker.py      # 追踪 API
│   │   │   │   ├── admin.py        # 管理 API
│   │   │   │   ├── analytics.py    # 统计分析 API
│   │   │   │   └── export.py       # 数据导出 API
│   │   │   └── websocket.py        # WebSocket 端点
│   │   │
│   │   ├── services/                # 业务逻辑服务
│   │   │   ├── __init__.py
│   │   │   ├── fingerprint.py      # 指纹处理服务
│   │   │   ├── detection.py        # 异常检测服务
│   │   │   ├── analytics.py        # 统计分析服务
│   │   │   ├── scoring.py          # 真实性评分服务
│   │   │   └── export.py           # 数据导出服务
│   │   │
│   │   └── utils/                   # 工具函数
│   │       ├── __init__.py
│   │       ├── ip.py               # IP 处理工具
│   │       ├── ua.py               # User-Agent 解析
│   │       ├── hash.py             # 哈希计算
│   │       └── datetime.py         # 日期时间工具
│   │
│   ├── migrations/                  # 数据库迁移（Alembic）
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── scripts/                     # 管理脚本
│   │   ├── init_db.py              # 初始化数据库
│   │   ├── seed_data.py            # 填充测试数据
│   │   └── cleanup.py              # 数据清理
│   │
│   ├── requirements.txt             # 生产依赖
│   ├── requirements-dev.txt         # 开发依赖
│   └── pytest.ini                   # pytest 配置
│
├── frontend/                         # 前端代码
│   ├── public/                      # 测试页面（公开访问）
│   │   ├── index.html              # 主页
│   │   ├── landing.html            # 着陆页
│   │   ├── ad-page.html            # 广告页
│   │   ├── page2.html              # 其他测试页面
│   │   └── page3.html
│   │
│   ├── admin/                       # 管理后台（需要认证）
│   │   ├── index.html              # 仪表盘
│   │   ├── logs.html               # 访问日志
│   │   ├── analytics.html          # 统计分析
│   │   ├── detection.html          # 异常检测
│   │   └── settings.html           # 系统设置
│   │
│   ├── static/                      # 静态资源
│   │   ├── css/
│   │   │   ├── common.css          # 通用样式
│   │   │   ├── public.css          # 测试页面样式
│   │   │   └── admin.css           # 管理后台样式
│   │   │
│   │   ├── js/
│   │   │   ├── tracker/            # 追踪脚本
│   │   │   │   ├── tracker.js      # 主追踪脚本
│   │   │   │   ├── fingerprint.js  # 指纹采集
│   │   │   │   └── behavior.js     # 行为记录
│   │   │   │
│   │   │   ├── admin/              # 管理后台脚本
│   │   │   │   ├── api.js          # API 调用封装
│   │   │   │   ├── dashboard.js    # 仪表盘逻辑
│   │   │   │   ├── logs.js         # 日志页面逻辑
│   │   │   │   ├── analytics.js    # 统计页面逻辑
│   │   │   │   └── websocket.js    # WebSocket 客户端
│   │   │   │
│   │   │   └── utils/              # 工具函数
│   │   │       ├── charts.js       # 图表配置
│   │   │       ├── format.js       # 数据格式化
│   │   │       └── auth.js         # 认证处理
│   │   │
│   │   └── img/                    # 图片资源
│   │       ├── logo.png
│   │       └── icons/
│
├── data/                            # 数据目录
│   ├── tracker.db                  # SQLite 数据库
│   ├── exports/                    # 导出文件
│   │   ├── csv/
│   │   └── json/
│   └── logs/                       # 应用日志
│       ├── app.log
│       └── error.log
│
├── tests/                           # 测试代码
│   ├── __init__.py
│   ├── conftest.py                 # pytest 配置和 fixtures
│   │
│   ├── unit/                       # 单元测试
│   │   ├── test_fingerprint.py
│   │   ├── test_detection.py
│   │   └── test_scoring.py
│   │
│   ├── integration/                # 集成测试
│   │   ├── test_tracker_api.py
│   │   ├── test_admin_api.py
│   │   └── test_websocket.py
│   │
│   └── load/                       # 性能测试
│       ├── locustfile.py
│       └── scenarios.py
│
├── docker/                          # Docker 配置
│   ├── Dockerfile                  # 生产镜像
│   ├── Dockerfile.dev              # 开发镜像
│   ├── docker-compose.yml          # 生产环境
│   └── docker-compose.dev.yml      # 开发环境
│
├── docs/                            # 文档
│   ├── API.md                      # API 文档
│   ├── DEPLOYMENT.md               # 部署文档
│   ├── DEVELOPMENT.md              # 开发指南
│   └── TESTING.md                  # 测试指南
│
├── .github/                         # GitHub 配置
│   └── workflows/
│       ├── ci.yml                  # CI 流程
│       └── cd.yml                  # CD 流程
│
├── .env.example                    # 环境变量模板
├── .gitignore                      # Git 忽略文件
├── .dockerignore                   # Docker 忽略文件
├── README.md                       # 项目说明
├── TASKS.md                        # 开发任务清单
├── ARCHITECTURE.md                 # 本文件
├── run.py                          # 启动脚本
└── pyproject.toml                  # 项目配置（Poetry）

```

## 4. 数据库设计优化

### 4.1 表结构设计

#### visits 表（访问记录）
```sql
CREATE TABLE visits (
    -- 主键和标识
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id TEXT UNIQUE NOT NULL,
    session_id TEXT,                          -- 会话ID（同一用户多次访问）

    -- 时间信息
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- IP 信息
    ip_address TEXT NOT NULL,
    ip_country TEXT,
    ip_country_code TEXT,                     -- 国家代码（US, CN等）
    ip_city TEXT,
    ip_region TEXT,                           -- 省份/州
    ip_latitude REAL,                         -- 纬度
    ip_longitude REAL,                        -- 经度
    ip_isp TEXT,                              -- ISP 提供商
    is_proxy BOOLEAN DEFAULT 0,
    is_datacenter BOOLEAN DEFAULT 0,          -- 是否数据中心IP

    -- 请求信息
    user_agent TEXT,
    referrer TEXT,
    page_url TEXT NOT NULL,
    query_string TEXT,                        -- URL 参数

    -- 设备信息（从 UA 解析）
    device_type TEXT,                         -- desktop/mobile/tablet/bot
    device_brand TEXT,                        -- Apple, Samsung, etc.
    device_model TEXT,                        -- iPhone 12, etc.
    browser TEXT,
    browser_version TEXT,
    os TEXT,
    os_version TEXT,

    -- 浏览器指纹
    screen_resolution TEXT,                   -- 1920x1080
    screen_color_depth INTEGER,               -- 色深
    viewport_size TEXT,                       -- 视口大小
    timezone TEXT,
    timezone_offset INTEGER,                  -- 时区偏移（分钟）
    language TEXT,
    languages TEXT,                           -- 所有语言列表（JSON）
    platform TEXT,
    cpu_cores INTEGER,                        -- CPU 核心数
    memory INTEGER,                           -- 内存大小（GB）

    -- 高级指纹
    canvas_fingerprint TEXT,
    webgl_fingerprint TEXT,
    webgl_vendor TEXT,
    webgl_renderer TEXT,
    fonts_hash TEXT,
    fonts_list TEXT,                          -- 完整字体列表（JSON）
    audio_fingerprint TEXT,                   -- 音频指纹
    plugins_hash TEXT,                        -- 插件哈希

    -- 浏览器特性
    cookies_enabled BOOLEAN,
    do_not_track BOOLEAN,
    has_touch_support BOOLEAN,
    has_session_storage BOOLEAN,
    has_local_storage BOOLEAN,
    has_indexed_db BOOLEAN,

    -- 行为数据
    stay_duration INTEGER DEFAULT 0,          -- 停留时间（秒）
    scroll_depth INTEGER DEFAULT 0,           -- 滚动深度（%）
    scroll_count INTEGER DEFAULT 0,           -- 滚动次数
    click_count INTEGER DEFAULT 0,            -- 点击次数
    mouse_move_count INTEGER DEFAULT 0,       -- 鼠标移动次数
    mouse_movements TEXT,                     -- 鼠标轨迹采样（JSON）
    keyboard_events INTEGER DEFAULT 0,        -- 键盘事件次数

    -- 页面交互
    previous_page TEXT,                       -- 上一页 URL
    next_page TEXT,                           -- 下一页 URL
    page_depth INTEGER DEFAULT 1,             -- 浏览深度
    is_bounce BOOLEAN DEFAULT 0,              -- 是否跳出

    -- 分析字段
    is_bot BOOLEAN DEFAULT 0,
    bot_type TEXT,                            -- 机器人类型
    is_suspicious BOOLEAN DEFAULT 0,          -- 是否可疑
    suspicious_reasons TEXT,                  -- 可疑原因（JSON数组）
    authenticity_score REAL DEFAULT 0.0,      -- 真实性评分（0-100）
    fingerprint_hash TEXT NOT NULL,           -- 综合指纹哈希
    fingerprint_quality INTEGER DEFAULT 0,    -- 指纹质量分（0-100）

    -- 元数据
    data_version INTEGER DEFAULT 1,           -- 数据版本（用于迁移）
    raw_data TEXT,                            -- 原始数据备份（JSON）
    notes TEXT,                               -- 备注

    -- 索引
    INDEX idx_timestamp (timestamp),
    INDEX idx_ip (ip_address),
    INDEX idx_fingerprint (fingerprint_hash),
    INDEX idx_session (session_id),
    INDEX idx_device_type (device_type),
    INDEX idx_is_bot (is_bot),
    INDEX idx_score (authenticity_score)
);
```

#### sessions 表（会话聚合）
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    fingerprint_hash TEXT,

    -- 会话信息
    first_visit_time DATETIME,
    last_visit_time DATETIME,
    visit_count INTEGER DEFAULT 1,
    total_duration INTEGER DEFAULT 0,         -- 总停留时间

    -- 聚合数据
    unique_pages INTEGER DEFAULT 1,           -- 访问的唯一页面数
    avg_authenticity_score REAL,

    INDEX idx_fingerprint (fingerprint_hash),
    INDEX idx_first_visit (first_visit_time)
);
```

#### analytics_summary 表（统计汇总）
```sql
CREATE TABLE analytics_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 时间维度
    date DATE NOT NULL,
    hour INTEGER,                             -- 0-23，NULL 表示全天

    -- 访问统计
    total_visits INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,        -- 基于指纹哈希
    unique_ips INTEGER DEFAULT 0,
    bot_visits INTEGER DEFAULT 0,
    suspicious_visits INTEGER DEFAULT 0,

    -- 设备统计
    desktop_visits INTEGER DEFAULT 0,
    mobile_visits INTEGER DEFAULT 0,
    tablet_visits INTEGER DEFAULT 0,

    -- 行为统计
    avg_stay_duration REAL DEFAULT 0.0,
    avg_scroll_depth REAL DEFAULT 0.0,
    avg_page_depth REAL DEFAULT 0.0,
    bounce_rate REAL DEFAULT 0.0,

    -- 质量统计
    avg_authenticity_score REAL DEFAULT 0.0,
    avg_fingerprint_quality REAL DEFAULT 0.0,

    -- 地理统计
    top_countries TEXT,                       -- JSON: [{"country": "US", "count": 100}]

    -- 元数据
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(date, hour)
);
```

#### detection_rules 表（检测规则配置）
```sql
CREATE TABLE detection_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT UNIQUE NOT NULL,
    rule_type TEXT NOT NULL,                  -- bot/proxy/suspicious
    enabled BOOLEAN DEFAULT 1,

    -- 规则配置
    config TEXT NOT NULL,                     -- JSON 配置
    threshold REAL,

    -- 统计信息
    trigger_count INTEGER DEFAULT 0,
    last_triggered DATETIME,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 索引策略

#### 主要索引
```sql
-- 时间范围查询
CREATE INDEX idx_visits_timestamp ON visits(timestamp);

-- IP 查询
CREATE INDEX idx_visits_ip ON visits(ip_address);

-- 指纹去重
CREATE INDEX idx_visits_fingerprint ON visits(fingerprint_hash);

-- 会话关联
CREATE INDEX idx_visits_session ON visits(session_id);

-- 质量筛选
CREATE INDEX idx_visits_score ON visits(authenticity_score);
CREATE INDEX idx_visits_bot ON visits(is_bot);

-- 复合索引（常见查询组合）
CREATE INDEX idx_visits_date_device ON visits(date(timestamp), device_type);
CREATE INDEX idx_visits_date_score ON visits(date(timestamp), authenticity_score);
```

## 5. API 设计

### 5.1 API 版本策略
- 使用 URL 路径版本: `/api/v1/...`
- 当前版本: v1
- 向后兼容原则

### 5.2 端点设计

#### 追踪 API (Public)
```
POST   /api/v1/track                  # 记录访问
POST   /api/v1/track/behavior         # 更新行为数据
GET    /api/v1/track/pixel.gif        # 追踪像素
```

#### 管理 API (Protected)
```
# 访问记录
GET    /api/v1/admin/visits           # 访问列表（分页、筛选）
GET    /api/v1/admin/visits/{id}      # 访问详情
DELETE /api/v1/admin/visits/{id}      # 删除访问记录

# 统计分析
GET    /api/v1/admin/stats/summary    # 统计摘要
GET    /api/v1/admin/stats/trend      # 访问趋势
GET    /api/v1/admin/stats/geo        # 地理分布
GET    /api/v1/admin/stats/devices    # 设备分布
GET    /api/v1/admin/stats/referrers  # 来源分布

# 异常检测
GET    /api/v1/admin/detection/bots   # 机器人检测结果
GET    /api/v1/admin/detection/proxies # 代理检测结果
GET    /api/v1/admin/detection/suspicious # 可疑访问

# 数据导出
GET    /api/v1/admin/export/csv       # 导出 CSV
GET    /api/v1/admin/export/json      # 导出 JSON

# 系统管理
GET    /api/v1/admin/system/health    # 系统健康检查
POST   /api/v1/admin/system/cleanup   # 数据清理
GET    /api/v1/admin/rules            # 获取检测规则
PUT    /api/v1/admin/rules/{id}       # 更新检测规则
```

#### 认证 API
```
POST   /api/v1/auth/login             # 登录
POST   /api/v1/auth/logout            # 登出
GET    /api/v1/auth/me                # 当前用户信息
```

#### WebSocket
```
WS     /api/v1/ws/live                # 实时访问推送
```

### 5.3 响应格式标准

#### 成功响应
```json
{
  "success": true,
  "data": {...},
  "meta": {
    "timestamp": "2025-12-02T10:00:00Z",
    "version": "v1"
  }
}
```

#### 分页响应
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

#### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Invalid fingerprint data",
    "details": {...}
  }
}
```

## 6. 安全方案

### 6.1 认证和授权
- **方式**: JWT (JSON Web Token)
- **存储**: HTTP-only Cookie + LocalStorage
- **过期**: 访问令牌 15 分钟，刷新令牌 7 天

### 6.2 安全措施
```python
# API 限流
- 追踪 API: 100 req/min per IP
- 管理 API: 1000 req/min per user

# 输入验证
- 所有输入使用 Pydantic 验证
- SQL 注入防护（SQLAlchemy ORM）
- XSS 防护（输出转义）

# CORS 配置
- 开发环境: 允许所有来源
- 生产环境: 仅允许配置的域名

# HTTPS
- 生产环境强制 HTTPS
- HSTS 头部启用
```

## 7. 性能优化策略

### 7.1 数据库优化
```python
# 连接池配置
POOL_SIZE = 20
MAX_OVERFLOW = 40
POOL_TIMEOUT = 30

# 查询优化
- 使用索引
- 避免 N+1 查询
- 使用批量操作
- 定期 VACUUM（SQLite）
```

### 7.2 缓存策略
```python
# 内存缓存（开发/小规模）
- 统计数据: TTL 5 分钟
- 配置数据: TTL 1 小时

# Redis 缓存（生产/大规模）
- 实时统计: TTL 1 分钟
- 历史统计: TTL 1 小时
- 检测规则: TTL 10 分钟
```

### 7.3 异步处理
```python
# 后台任务
- 统计数据聚合: 每 5 分钟
- 数据清理: 每天凌晨 2 点
- 导出文件清理: 每小时

# 使用 BackgroundTasks
- 异常检测
- 评分计算
- 日志写入
```

## 8. 部署方案

### 8.1 Docker 部署（推荐）

#### 生产环境
```yaml
# docker-compose.yml
services:
  web:
    image: adalliance-tracker:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///data/tracker.db
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./data:/app/data
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
```

### 8.2 传统部署

#### 使用 Systemd 服务
```ini
[Unit]
Description=AdAlliance Tracker
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/adalliance-tracker
ExecStart=/opt/adalliance-tracker/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## 9. 监控和日志

### 9.1 日志策略
```python
# 日志级别
- 开发环境: DEBUG
- 生产环境: INFO

# 日志输出
- 控制台: 结构化 JSON
- 文件: 按日期轮转
- 错误追踪: Sentry（可选）

# 日志内容
- API 请求/响应
- 数据库查询（慢查询）
- 异常和错误
- 业务指标
```

### 9.2 监控指标
```python
# 应用指标
- QPS（每秒查询数）
- 响应时间（P50, P95, P99）
- 错误率
- 数据库连接数

# 业务指标
- 访问量
- 异常检测率
- 真实性评分分布
- 指纹重复率
```

## 10. 开发工作流

### 10.1 分支策略
```
main          # 生产环境
├── develop   # 开发环境
├── feature/* # 功能分支
└── hotfix/*  # 紧急修复
```

### 10.2 代码规范
```python
# 格式化
black --line-length 88 backend/

# 类型检查
mypy backend/app

# 代码检查
flake8 backend/app

# 测试覆盖率
pytest --cov=app --cov-report=html
```

## 11. 测试策略

### 11.1 测试金字塔
```
E2E Tests (10%)          # Playwright
  ↑
Integration Tests (30%)  # Pytest + TestClient
  ↑
Unit Tests (60%)         # Pytest
```

### 11.2 测试覆盖率目标
- 核心业务逻辑: 90%+
- API 路由: 80%+
- 工具函数: 95%+
- 整体覆盖率: 80%+

## 12. 未来扩展

### Phase 2 功能
- [ ] PostgreSQL 支持
- [ ] Redis 缓存集成
- [ ] 多站点管理
- [ ] A/B 测试功能
- [ ] 告警通知（邮件/Webhook）
- [ ] 数据备份和恢复
- [ ] API 文档自动生成
- [ ] Grafana 仪表盘

### Phase 3 功能
- [ ] 机器学习异常检测
- [ ] 实时流处理（Kafka）
- [ ] 分布式追踪
- [ ] 国际化支持
- [ ] 移动端管理 App

---

**文档版本**: 1.0
**最后更新**: 2025-12-02
**维护者**: Development Team
