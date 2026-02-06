"""
数据库迁移脚本：添加 IP 变化检测字段
为 visits 表添加 last_ip, ip_changed, ip_change_count 字段
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from app.core.database import engine


# 需要添加的新字段列表
NEW_COLUMNS = [
    ("last_ip", "VARCHAR(45)"),
    ("ip_changed", "BOOLEAN DEFAULT 0"),
    ("ip_change_count", "INTEGER DEFAULT 0"),
]


async def migrate():
    """执行数据库迁移"""
    print("[INFO] 开始数据库迁移：添加 IP 变化检测字段...")

    try:
        async with engine.begin() as conn:
            # 检查 visits 表是否存在
            result = await conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='visits'"
            ))
            table_exists = result.fetchone() is not None

            if not table_exists:
                print("[INFO] visits 表不存在，通过 ORM 创建...")
                from app.core.database import Base
                from app.models.visit import Visit  # noqa: F401
                await conn.run_sync(Base.metadata.create_all)
                print("[SUCCESS] 表已通过 ORM 模型创建（包含所有新字段）")
                return

            # 获取当前表的所有字段
            result = await conn.execute(text("PRAGMA table_info(visits)"))
            existing_columns = [row[1] for row in result.fetchall()]

            added = 0
            skipped = 0

            for col_name, col_type in NEW_COLUMNS:
                if col_name in existing_columns:
                    print(f"  [SKIP] {col_name} 已存在")
                    skipped += 1
                    continue

                sql = f"ALTER TABLE visits ADD COLUMN {col_name} {col_type}"
                await conn.execute(text(sql))
                print(f"  [ADD] {col_name} {col_type}")
                added += 1

        print(f"\n[SUCCESS] 数据库迁移完成！")
        print(f"  新增字段: {added}")
        print(f"  已跳过: {skipped}")
        print(f"\n[INFO] 新增字段说明：")
        print("  - last_ip: 最后一次请求的 IP 地址")
        print("  - ip_changed: 访问期间 IP 是否发生变化")
        print("  - ip_change_count: IP 变化次数")

    except Exception as e:
        print(f"[ERROR] 迁移失败: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(migrate())
