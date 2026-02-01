"""
数据库迁移脚本：添加视口大小字段
为 visits 表添加 viewport_size 字段
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from app.core.database import engine


async def migrate():
    """执行数据库迁移"""
    print("[INFO] 开始数据库迁移：添加 viewport_size 字段...")

    try:
        async with engine.begin() as conn:
            # 检查字段是否已存在
            result = await conn.execute(text("PRAGMA table_info(visits)"))
            columns = [row[1] for row in result.fetchall()]

            if 'viewport_size' in columns:
                print("[WARN] 字段已存在，跳过迁移")
                return

            # 执行迁移
            await conn.execute(text("ALTER TABLE visits ADD COLUMN viewport_size VARCHAR(20)"))
            print("[INFO] 执行: ALTER TABLE visits ADD COLUMN viewport_size VARCHAR(20)")

        print("[SUCCESS] 数据库迁移完成！")
        print("[INFO] 已添加字段：")
        print("  - viewport_size (视口大小)")

    except Exception as e:
        print(f"[ERROR] 迁移失败: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(migrate())
