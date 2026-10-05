"""VASTU ONE - Database Connection Test"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from database.base import init_db, engine
from sqlalchemy import text


async def main():
    try:
        # Test connection
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connected to: {version[:60]}...")
        
        # Create all tables
        await init_db()
        print("✅ All tables created/verified")
        
        # List tables
        async with engine.connect() as conn:
            result = await conn.execute(text(
                "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"
            ))
            tables = [row[0] for row in result]
            print(f"\n📊 Tables in database ({len(tables)}):")
            for t in tables:
                print(f"   - {t}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())