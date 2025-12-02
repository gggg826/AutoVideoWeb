"""
应用启动脚本
运行 FastAPI 应用服务器
"""
import uvicorn
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.app.config import settings


if __name__ == "__main__":
    print("="  * 60)
    print(f"🚀 启动 {settings.APP_NAME}")
    print(f"📦 版本: {settings.APP_VERSION}")
    print(f"🌍 环境: {settings.ENVIRONMENT}")
    print(f"🔧 调试模式: {settings.DEBUG}")
    print(f"📍 地址: http://{settings.HOST}:{settings.PORT}")
    print("=" * 60)
    print()
    print("📚 API 文档: http://localhost:8000/docs")
    print("🧪 测试页面: http://localhost:8000/public/index.html")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    print()

    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
