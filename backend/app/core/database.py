"""
数据库配置和会话管理
使用 SQLAlchemy 异步引擎
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# 创建异步会话工厂
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# ORM 模型基类
Base = declarative_base()


# 依赖注入：获取数据库会话
async def get_db() -> AsyncSession:
    """
    获取数据库会话的依赖函数
    用于 FastAPI 路由的依赖注入
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# 数据库初始化函数
async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 数据库清理函数
async def drop_db():
    """删除所有数据库表（仅用于开发/测试）"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
