"""Auto-generate certificates for 100% complete enrollments."""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from database.base import AsyncSessionLocal
from database.models import Enrollment, Certificate
from sqlalchemy import select
import secrets
from datetime import datetime


def generate_cert_number():
    year = datetime.utcnow().year
    rand = secrets.token_hex(4).upper()
    return f"V1-{year}-{rand}"


async def auto_generate():
    async with AsyncSessionLocal() as db:
        # Find 100% complete enrollments without certificates
        stmt = (
            select(Enrollment)
            .outerjoin(Certificate, Certificate.enrollment_id == Enrollment.id)
            .where(
                Enrollment.progress_pct >= 100,
                Certificate.id.is_(None),
            )
        )
        enrollments = (await db.execute(stmt)).scalars().all()

        print(f"Found {len(enrollments)} enrollments ready for certificates")

        for e in enrollments:
            cert = Certificate(
                enrollment_id=e.id,
                certificate_number=generate_cert_number(),
            )
            db.add(cert)
            print(f"  + Created certificate for enrollment {e.id[:8]}")

        await db.commit()
        print(f"Done! {len(enrollments)} certificates created.")


asyncio.run(auto_generate())