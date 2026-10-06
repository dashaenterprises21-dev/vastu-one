from dotenv import load_dotenv
load_dotenv()
import asyncio
from database.base import AsyncSessionLocal
from database.models import User
from sqlalchemy import select

async def go():
    async with AsyncSessionLocal() as db:
        r = await db.execute(select(User))
        rows = r.scalars().all()
        print("Total users:", len(rows))
        for u in rows:
            print(u.id, "|", u.email, "|", u.role.value, "|", u.tenant_id, "| active:", u.is_active)

asyncio.run(go())

