"""
数据库迁移脚本：添加浏览器地理位置字段
为 visits 表添加浏览器地理位置相关字段
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
    print("[INFO] 开始数据库迁移：添加浏览器地理位置字段...")

    migration_sql = """
    ALTER TABLE visits ADD COLUMN browser_latitude REAL;
    ALTER TABLE visits ADD COLUMN browser_longitude REAL;
    ALTER TABLE visits ADD COLUMN browser_accuracy REAL;
    ALTER TABLE visits ADD COLUMN browser_altitude REAL;
    ALTER TABLE visits ADD COLUMN browser_altitude_accuracy REAL;
    """

    try:
        async with engine.begin() as conn:
            # 检查字段是否已存在
            result = await conn.execute(text("PRAGMA table_info(visits)"))
            columns = [row[1] for row in result.fetchall()]

            if 'browser_latitude' in columns:
                print("[WARN] 字段已存在，跳过迁移")
                return

            # 执行迁移
            for statement in migration_sql.strip().split(';'):
                if statement.strip():
                    await conn.execute(text(statement.strip()))
                    print(f"[INFO] 执行: {statement.strip()[:50]}...")

        print("[SUCCESS] 数据库迁移完成！")
        print("[INFO] 已添加以下字段：")
        print("  - browser_latitude (浏览器纬度)")
        print("  - browser_longitude (浏览器经度)")
        print("  - browser_accuracy (位置精度)")
        print("  - browser_altitude (海拔高度)")
        print("  - browser_altitude_accuracy (海拔精度)")

    except Exception as e:
        print(f"[ERROR] 迁移失败: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(migrate())
