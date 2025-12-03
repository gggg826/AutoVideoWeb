"""
Database initialization script
Creates all database tables
"""
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine, Base
from app.models.visit import Visit  # Import all models


async def init_database():
    """Initialize database"""
    print("[INFO] Initializing database...")

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    print("[OK] Database initialized successfully!")
    print(f"[INFO] Created tables: {', '.join(Base.metadata.tables.keys())}")


async def drop_database():
    """Drop all tables (use with caution)"""
    print("[WARNING] About to drop all database tables!")
    confirm = input("Confirm deletion? (yes/no): ")

    if confirm.lower() == "yes":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("[OK] All tables dropped")
    else:
        print("[CANCELLED] Operation cancelled")


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        asyncio.run(drop_database())
    else:
        asyncio.run(init_database())
