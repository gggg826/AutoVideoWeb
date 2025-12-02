# AdAllianceTools 测试网站

## 项目概述

这是一个用于测试 AdAllianceTools 流量生成工具的 Web 应用，用于验证：
- 浏览器指纹伪装效果
- 真人行为模拟质量
- 代理池切换效果
- 访问统计和分析

## 功能特性

### 1. 访问者信息记录
- **基础信息**：IP地址、访问时间、User-Agent、Referrer
- **浏览器指纹**：设备类型、屏幕分辨率、时区、语言、平台
- **高级指纹**：Canvas指纹、WebGL指纹、字体列表
- **行为数据**：页面停留时间、滚动深度、鼠标移动轨迹

### 2. 管理后台
- **实时监控**：访问日志实时展示、在线访客统计
- **统计分析**：访问量趋势、IP分布、设备类型分布、时区分布
- **指纹分析**：检测重复访问、识别异常指纹、评估真实性评分
- **数据导出**：CSV/JSON格式导出访问日志

### 3. 测试页面
- **目标页面**：模拟广告展示页面（带追踪像素）
- **着陆页**：简单的内容页面（测试停留时间）
- **多页浏览**：多个页面测试页面跳转

## 技术栈

### 后端
- **Python 3.10+**
- **FastAPI 0.109+**：高性能Web框架
- **SQLite3**：轻量级数据库（可扩展到PostgreSQL）
- **Pydantic**：数据验证
- **Uvicorn**：ASGI服务器

### 前端
- **HTML5 + CSS3 + JavaScript**
- **Chart.js**：数据可视化
- **DataTables**：表格展示
- **FingerprintJS**：浏览器指纹采集

## 项目结构

```
Web/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI应用入口
│   │   ├── models.py          # 数据模型
│   │   ├── database.py        # 数据库连接
│   │   ├── crud.py            # 数据库操作
│   │   ├── schemas.py         # Pydantic模型
│   │   ├── routers/           # API路由
│   │   │   ├── tracker.py     # 追踪API
│   │   │   ├── admin.py       # 管理API
│   │   │   └── analytics.py  # 分析API
│   │   └── utils/
│   │       ├── fingerprint.py # 指纹分析
│   │       └── detection.py   # 异常检测
│   ├── requirements.txt       # Python依赖
│   └── config.py              # 配置文件
│
├── frontend/                   # 前端代码
│   ├── public/                # 测试页面
│   │   ├── index.html         # 主页
│   │   ├── landing.html       # 着陆页
│   │   ├── ad-page.html       # 广告页
│   │   └── js/
│   │       └── tracker.js     # 追踪脚本
│   ├── admin/                 # 管理后台
│   │   ├── index.html         # 仪表盘
│   │   ├── logs.html          # 访问日志
│   │   ├── analytics.html     # 统计分析
│   │   └── js/
│   │       ├── dashboard.js   # 仪表盘逻辑
│   │       └── api.js         # API调用
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── common.js
│
├── data/                      # 数据目录
│   ├── tracker.db            # SQLite数据库
│   └── exports/              # 导出文件
│
├── docker/                    # Docker配置
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── tests/                     # 测试代码
│   ├── test_api.py
│   └── test_fingerprint.py
│
├── .env.example               # 环境变量模板
├── .gitignore
├── README.md                  # 本文件
└── run.py                     # 启动脚本
```

## 开发计划（4周）

### Week 1: 基础设施搭建（P0）
**目标**: 完成基础框架和数据库设计

#### Day 1-2: 项目初始化
- [P0-1] 创建项目结构
- [P0-2] 配置开发环境（虚拟环境、依赖安装）
- [P0-3] 数据库设计（访问日志表、指纹表）
- [P0-4] FastAPI基础框架搭建

**验收标准**:
- ✅ 项目结构完整
- ✅ FastAPI启动成功（http://localhost:8000）
- ✅ 数据库表创建成功
- ✅ Swagger文档可访问（/docs）

#### Day 3-5: 核心追踪API
- [P0-5] 实现追踪API端点（POST /api/track）
- [P0-6] IP信息采集（真实IP、代理IP检测）
- [P0-7] User-Agent解析（设备类型、浏览器、操作系统）
- [P0-8] 基础指纹采集（Canvas、WebGL、字体）
- [P0-9] 数据库CRUD操作

**验收标准**:
- ✅ 追踪API返回200
- ✅ 访问数据成功写入数据库
- ✅ IP、UA正确解析
- ✅ 基础指纹数据完整

### Week 2: 前端开发（P1）
**目标**: 完成测试页面和管理后台基础功能

#### Day 1-3: 测试页面开发
- [P1-1] 主页设计（index.html）
- [P1-2] 着陆页设计（landing.html）
- [P1-3] 广告页设计（ad-page.html）
- [P1-4] 追踪脚本开发（tracker.js）
  - 自动采集指纹
  - 定时上报行为数据
  - 页面卸载前上报停留时间
- [P1-5] 鼠标轨迹记录
- [P1-6] 滚动深度记录

**验收标准**:
- ✅ 3个测试页面可正常访问
- ✅ tracker.js自动加载并上报数据
- ✅ 行为数据成功记录

#### Day 4-5: 管理后台UI
- [P1-7] 仪表盘页面（index.html）
  - 实时访客数
  - 今日/昨日访问统计
  - 访问趋势图表
- [P1-8] 访问日志页面（logs.html）
  - 表格展示所有访问记录
  - 分页功能
  - 筛选功能（日期、IP、设备类型）

**验收标准**:
- ✅ 仪表盘展示统计数据
- ✅ 访问日志正确展示
- ✅ 筛选功能正常工作

### Week 3: 高级功能（P1）
**目标**: 完成统计分析和异常检测功能

#### Day 1-3: 统计分析API
- [P1-9] 访问量统计API（按小时/天/周/月）
- [P1-10] IP分布统计（按国家/地区）
- [P1-11] 设备类型分布统计
- [P1-12] 时区分布统计
- [P1-13] Referrer来源统计
- [P1-14] 停留时间分析

**验收标准**:
- ✅ 所有统计API返回正确数据
- ✅ 数据聚合逻辑正确
- ✅ 性能优化（1秒内响应）

#### Day 4-5: 异常检测
- [P1-15] 重复访问检测（同一指纹短时间内多次访问）
- [P1-16] 代理检测（识别数据中心IP、代理特征）
- [P1-17] 机器人检测（UA异常、行为异常）
- [P1-18] 真实性评分算法
  - 指纹完整度（60%）
  - 行为自然度（30%）
  - IP质量（10%）

**验收标准**:
- ✅ 异常访问被标记
- ✅ 真实性评分准确
- ✅ 检测规则可配置

### Week 4: 优化和部署（P2）
**目标**: 完成数据导出、性能优化和部署

#### Day 1-2: 数据导出和可视化
- [P2-1] CSV导出功能
- [P2-2] JSON导出功能
- [P2-3] 统计图表优化（Chart.js）
- [P2-4] 实时数据推送（WebSocket）

**验收标准**:
- ✅ 导出文件格式正确
- ✅ 图表实时更新
- ✅ WebSocket连接稳定

#### Day 3-4: 性能优化
- [P2-5] 数据库索引优化
- [P2-6] API响应缓存
- [P2-7] 前端资源压缩
- [P2-8] 负载测试（1000并发）

**验收标准**:
- ✅ API响应时间 < 100ms
- ✅ 数据库查询优化
- ✅ 页面加载 < 2秒

#### Day 5: 部署和文档
- [P2-9] Docker镜像构建
- [P2-10] Docker Compose配置
- [P2-11] 部署文档编写
- [P2-12] API文档完善

**验收标准**:
- ✅ Docker一键部署
- ✅ 文档完整清晰
- ✅ 生产环境测试通过

## 数据库设计

### visits表（访问记录）
```sql
CREATE TABLE visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id TEXT UNIQUE NOT NULL,           -- 唯一访问ID
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- IP信息
    ip_address TEXT NOT NULL,
    ip_country TEXT,
    ip_city TEXT,
    is_proxy BOOLEAN DEFAULT 0,

    -- 请求信息
    user_agent TEXT,
    referrer TEXT,
    page_url TEXT,

    -- 设备信息
    device_type TEXT,                        -- pc/mobile
    browser TEXT,
    browser_version TEXT,
    os TEXT,
    os_version TEXT,

    -- 浏览器指纹
    screen_resolution TEXT,
    timezone TEXT,
    language TEXT,
    platform TEXT,
    canvas_fingerprint TEXT,
    webgl_fingerprint TEXT,
    fonts_hash TEXT,

    -- 行为数据
    stay_duration INTEGER DEFAULT 0,         -- 停留时间（秒）
    scroll_depth INTEGER DEFAULT 0,          -- 滚动深度（%）
    mouse_movements TEXT,                    -- JSON格式鼠标轨迹

    -- 分析字段
    is_bot BOOLEAN DEFAULT 0,
    authenticity_score FLOAT DEFAULT 0.0,    -- 真实性评分（0-100）
    fingerprint_hash TEXT,                   -- 指纹哈希（用于去重）

    INDEX idx_timestamp (timestamp),
    INDEX idx_ip (ip_address),
    INDEX idx_fingerprint (fingerprint_hash)
);
```

### analytics_summary表（统计汇总）
```sql
CREATE TABLE analytics_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    hour INTEGER,                            -- 小时（0-23），NULL表示全天

    total_visits INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,
    bot_visits INTEGER DEFAULT 0,

    avg_stay_duration FLOAT DEFAULT 0.0,
    avg_scroll_depth FLOAT DEFAULT 0.0,
    avg_authenticity_score FLOAT DEFAULT 0.0,

    UNIQUE(date, hour)
);
```

## API端点设计

### 追踪API
- `POST /api/track` - 记录访问信息
- `POST /api/track/behavior` - 记录行为数据（停留时间、滚动）

### 管理API
- `GET /api/admin/visits` - 获取访问列表（分页、筛选）
- `GET /api/admin/visits/{visit_id}` - 获取单个访问详情
- `GET /api/admin/stats/summary` - 获取统计摘要
- `GET /api/admin/stats/trend` - 获取访问趋势
- `GET /api/admin/stats/distribution` - 获取分布统计（IP、设备、时区）
- `GET /api/admin/export/csv` - 导出CSV
- `GET /api/admin/export/json` - 导出JSON

### 实时API
- `WebSocket /ws/live` - 实时访问推送

## 配置说明

### 环境变量（.env）
```env
# 应用配置
APP_NAME=AdAllianceTools Test Site
APP_VERSION=1.0.0
DEBUG=true

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///data/tracker.db

# 安全配置
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123
SECRET_KEY=your-secret-key-here

# CORS配置
ALLOWED_ORIGINS=*

# IP检测配置
IP_API_KEY=your-ip-api-key  # 可选：ipapi.co API密钥
```

## 快速开始

### 本地开发
```bash
# 1. 创建虚拟环境
cd Web
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. 安装依赖
pip install -r backend/requirements.txt

# 3. 初始化数据库
python backend/init_db.py

# 4. 启动开发服务器
python run.py

# 5. 访问
# - 测试页面: http://localhost:8000
# - 管理后台: http://localhost:8000/admin
# - API文档: http://localhost:8000/docs
```

### Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 测试指南

### 使用AdAllianceTools测试
1. 配置AdAllianceTools目标URL为测试网站
2. 启动流量生成
3. 在管理后台查看访问日志和统计
4. 验证指纹伪装效果

### 评估指标
- **指纹多样性**: 不同访问的指纹应该不同
- **时区一致性**: IP国家与时区应该匹配
- **行为自然度**: 停留时间、滚动深度应该符合正态分布
- **真实性评分**: 平均评分应 > 70分

## 性能目标

- **API响应时间**: < 100ms (P95)
- **数据库写入**: > 1000 TPS
- **并发处理**: 支持1000并发访问
- **页面加载**: < 2秒
- **实时推送延迟**: < 500ms

## 安全考虑

- ✅ 管理后台需要身份验证
- ✅ API限流（防止DDOS）
- ✅ SQL注入防护（使用ORM）
- ✅ XSS防护（输出转义）
- ✅ HTTPS支持（生产环境）

## 扩展计划

### Phase 2功能（可选）
- PostgreSQL支持（大数据量）
- Redis缓存（性能提升）
- 多站点支持（多个测试站点）
- A/B测试功能
- 告警功能（异常访问通知）

---

**当前状态**: 准备阶段
**开始日期**: 2025-12-02
**预计完成**: 2025-12-30（4周）
