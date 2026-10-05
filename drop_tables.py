"""Drop all tables and types from public schema"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from database.base import engine
from sqlalchemy import text


async def main():
    async with engine.begin() as conn:
        # Drop all tables
        await conn.execute(text("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """))
        print("✅ All tables dropped")
        
        # Drop all custom enum types
        await conn.execute(text("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (
                    SELECT typname FROM pg_type 
                    WHERE typtype = 'e' 
                    AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
                ) LOOP
                    EXECUTE 'DROP TYPE IF EXISTS ' || quote_ident(r.typname) || ' CASCADE';
                END LOOP;
            END $$;
        """))
        print("✅ All enum types dropped")


if __name__ == "__main__":
    asyncio.run(main())