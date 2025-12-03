"""
FastAPI 主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.config import settings
from app.api.v1 import tracker, admin, auth

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AdAllianceTools 流量测试网站 - 访问追踪 API",
    debug=settings.DEBUG,
)

# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(tracker.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

# 静态文件服务
frontend_dir = Path(__file__).parent.parent.parent / "frontend"

if (frontend_dir / "static").exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir / "static")), name="static")

if (frontend_dir / "public").exists():
    app.mount("/public", StaticFiles(directory=str(frontend_dir / "public"), html=True), name="public")

if (frontend_dir / "admin").exists():
    app.mount("/admin", StaticFiles(directory=str(frontend_dir / "admin"), html=True), name="admin")


@app.get("/", response_class=HTMLResponse)
async def root():
    """根路径重定向到测试页面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AdAlliance Tracker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            .links { margin-top: 20px; }
            .links a {
                display: inline-block;
                margin: 10px 10px 10px 0;
                padding: 10px 20px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
            .links a:hover { background: #0056b3; }
            .info {
                margin-top: 20px;
                padding: 15px;
                background: #e7f3ff;
                border-left: 4px solid #007bff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 AdAlliance 访问追踪系统</h1>
            <p>用于测试流量生成工具的浏览器指纹伪装和行为模拟效果</p>

            <div class="info">
                <strong>系统状态：</strong> ✅ 运行中<br>
                <strong>版本：</strong> """ + settings.APP_VERSION + """<br>
                <strong>环境：</strong> """ + settings.ENVIRONMENT + """
            </div>

            <div class="links">
                <a href="/public/index.html">📄 测试主页</a>
                <a href="/admin/index.html">🔧 管理后台</a>
                <a href="/docs">📚 API 文档</a>
                <a href="/health">🏥 健康检查</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/v1/info")
async def api_info():
    """API 信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "api_version": "v1",
        "endpoints": {
            "tracker": "/api/v1/track",
            "behavior": "/api/v1/track/behavior",
            "docs": "/docs"
        }
    }
