"""
数据库迁移脚本：添加全量采集字段
为 visits 表添加硬件、网络、浏览器功能、指纹、电池、性能等全部新字段
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
    # WebGL 详细信息
    ("webgl_vendor", "VARCHAR(200)"),
    ("webgl_renderer", "VARCHAR(200)"),

    # 硬件信息
    ("device_memory", "FLOAT"),
    ("hardware_concurrency", "INTEGER"),
    ("color_depth", "INTEGER"),
    ("pixel_ratio", "FLOAT"),
    ("max_touch_points", "INTEGER"),

    # 网络信息
    ("connection_type", "VARCHAR(20)"),
    ("connection_downlink", "FLOAT"),
    ("connection_rtt", "INTEGER"),
    ("connection_save_data", "BOOLEAN"),

    # 浏览器功能
    ("cookies_enabled", "BOOLEAN"),
    ("do_not_track", "BOOLEAN"),
    ("pdf_viewer_enabled", "BOOLEAN"),
    ("plugins_hash", "VARCHAR(64)"),

    # 音频指纹
    ("audio_fingerprint", "VARCHAR(64)"),

    # 媒体设备
    ("media_devices_hash", "VARCHAR(64)"),

    # 存储支持
    ("local_storage_enabled", "BOOLEAN"),
    ("session_storage_enabled", "BOOLEAN"),
    ("indexed_db_enabled", "BOOLEAN"),

    # 广告拦截检测
    ("ad_blocker_detected", "BOOLEAN"),

    # 电池信息
    ("battery_charging", "BOOLEAN"),
    ("battery_level", "INTEGER"),
    ("battery_charging_time", "FLOAT"),
    ("battery_discharging_time", "FLOAT"),

    # WebRTC 哈希
    ("webrtc_hash", "VARCHAR(64)"),

    # 语音列表哈希
    ("speech_voices_hash", "VARCHAR(64)"),

    # 性能指标
    ("page_load_time", "INTEGER"),
    ("dom_parse_time", "INTEGER"),
    ("dns_time", "INTEGER"),
    ("tcp_time", "INTEGER"),
    ("ttfb", "INTEGER"),

    # Headless 检测
    ("is_headless", "BOOLEAN"),
]


async def migrate():
    """执行数据库迁移"""
    print("[INFO] 开始数据库迁移：添加全量采集字段...")

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
        print(f"\n[INFO] 新增字段分类：")
        print("  - WebGL 详细: webgl_vendor, webgl_renderer")
        print("  - 硬件信息: device_memory, hardware_concurrency, color_depth, pixel_ratio, max_touch_points")
        print("  - 网络信息: connection_type, connection_downlink, connection_rtt, connection_save_data")
        print("  - 浏览器功能: cookies_enabled, do_not_track, pdf_viewer_enabled, plugins_hash")
        print("  - 音频指纹: audio_fingerprint")
        print("  - 媒体设备: media_devices_hash")
        print("  - 存储支持: local_storage_enabled, session_storage_enabled, indexed_db_enabled")
        print("  - 广告拦截: ad_blocker_detected")
        print("  - 电池信息: battery_charging, battery_level, battery_charging_time, battery_discharging_time")
        print("  - WebRTC: webrtc_hash")
        print("  - 语音列表: speech_voices_hash")
        print("  - 性能指标: page_load_time, dom_parse_time, dns_time, tcp_time, ttfb")
        print("  - Headless 检测: is_headless")

    except Exception as e:
        print(f"[ERROR] 迁移失败: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(migrate())
