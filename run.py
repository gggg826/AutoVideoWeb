"""
Application startup script
Runs the FastAPI application server
"""
import uvicorn
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.app.config import settings


if __name__ == "__main__":
    print("="  * 60)
    print(f"Starting {settings.APP_NAME}")
    print(f"Version: {settings.APP_VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Address: http://{settings.HOST}:{settings.PORT}")
    print("=" * 60)
    print()
    print("API Docs:   http://localhost:8000/docs")
    print("Test Page:  http://localhost:8000/public/index.html")
    print("Admin:      http://localhost:8000/admin/index.html")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
