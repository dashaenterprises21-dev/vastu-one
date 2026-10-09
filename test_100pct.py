"""Test: Update enrollment to 100% to trigger auto-cert generation."""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from database.base import AsyncSessionLocal
from database.models import Enrollment
from sqlalchemy import select, update


async def update_to_100():
    async with AsyncSessionLocal() as db:
        # Update enrollment 81a981f4... to 100%
        enrollment_id = "81a981f4-30ec-4bcb-93e4-90da6b2380eb"

        stmt = (
            update(Enrollment)
            .where(Enrollment.id == enrollment_id)
            .values(progress_pct=100.0)
        )
        await db.execute(stmt)
        await db.commit()

        # Verify
        check = await db.execute(
            select(Enrollment).where(Enrollment.id == enrollment_id)
        )
        e = check.scalar_one()
        print(f"Updated: progress = {e.progress_pct}%")


asyncio.run(update_to_100())