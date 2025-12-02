"""
数据库初始化脚本
创建所有数据库表
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine, Base
from app.models.visit import Visit  # 导入所有模型


async def init_database():
    """初始化数据库"""
    print("🔧 开始初始化数据库...")

    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)

    print("✅ 数据库初始化完成！")
    print(f"📊 创建的表: {', '.join(Base.metadata.tables.keys())}")


async def drop_database():
    """删除所有表（谨慎使用）"""
    print("⚠️  警告：即将删除所有数据库表！")
    confirm = input("确认删除？(yes/no): ")

    if confirm.lower() == "yes":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("✅ 所有表已删除")
    else:
        print("❌ 操作已取消")


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        asyncio.run(drop_database())
    else:
        asyncio.run(init_database())
