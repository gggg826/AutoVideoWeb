"""
应用配置管理
使用 pydantic-settings 管理环境变量
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""

    # 应用信息
    APP_NAME: str = "AdAlliance Tracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/tracker.db"

    # 安全配置
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "Admin@123"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时

    # CORS 配置
    ALLOWED_ORIGINS: str = "*"
    ALLOWED_METHODS: str = "GET,POST,PUT,DELETE"
    ALLOWED_HEADERS: str = "*"

    # 限流配置
    RATE_LIMIT_PER_MINUTE: int = 100

    # 缓存配置
    CACHE_TTL: int = 300
    MAX_EXPORT_ROWS: int = 10000

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    @property
    def allowed_origins_list(self) -> List[str]:
        """解析 CORS 允许的源列表"""
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
