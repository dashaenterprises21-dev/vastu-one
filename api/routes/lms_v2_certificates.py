"""
VASTU ONE - LMS v2: Certificate Generation
============================================
Auto-generate certificates on course completion.
"""
from __future__ import annotations
import secrets
from datetime import datetime
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from database.base import get_db
from database.models import Certificate, Course, Enrollment, User


router = APIRouter(prefix="/api/lms/v2/certificates", tags=["lms-v2-certificates"])


VOID = colors.HexColor("#05060F")
GOLD = colors.HexColor("#D4AF37")
STARLIGHT = colors.HexColor("#F8F7F2")
MUTED = colors.HexColor("#8B8B8B")


def generate_certificate_number() -> str:
    """Generate unique certificate number."""
    prefix = "V1"
    year = datetime.utcnow().year
    random_part = secrets.token_hex(4).upper()
    return f"{prefix}-{year}-{random_part}"


def draw_certificate(c: canvas.Canvas, student_name: str, course_title: str, cert_number: str, issued_at: datetime):
    """Draw certificate content on canvas."""
    width, height = landscape(A4)
    
    # Background
    c.setFillColor(VOID)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Gold border (double)
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.rect(15 * mm, 15 * mm, width - 30 * mm, height - 30 * mm)
    
    c.setLineWidth(0.5)
    c.rect(18 * mm, 18 * mm, width - 36 * mm, height - 36 * mm)
    
    # Corner ornaments
    corner_size = 8 * mm
    corners = [
        (15 * mm, 15 * mm, 1, 1),
        (width - 15 * mm - corner_size, 15 * mm, -1, 1),
        (15 * mm, height - 15 * mm - corner_size, 1, -1),
        (width - 15 * mm - corner_size, height - 15 * mm - corner_size, -1, -1),
    ]
    c.setFillColor(GOLD)
    for x, y, dx, dy in corners:
        c.rect(x, y, corner_size, corner_size, fill=1, stroke=0)
        c.setFillColor(VOID)
        c.rect(x + (2 * mm if dx > 0 else 0), y + (2 * mm if dy > 0 else 0), 
               corner_size - 4 * mm, corner_size - 4 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
    
    # Header — VASTU ONE
    c.setFillColor(STARLIGHT)
    c.setFont("Times-Bold", 36)
    c.drawCentredString(width / 2, height - 40 * mm, "VASTU ONE")
    
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 47 * mm, "TRACEABLE VASTU INTELLIGENCE")
    
    # Divider line
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(width / 2 - 40 * mm, height - 52 * mm, width / 2 + 40 * mm, height - 52 * mm)
    
    # Title
    c.setFillColor(GOLD)
    c.setFont("Times-Italic", 20)
    c.drawCentredString(width / 2, height - 65 * mm, "Certificate of Completion")
    
    # "This is to certify that"
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 78 * mm, "This is to certify that")
    
    # Student name (large, gold)
    c.setFillColor(GOLD)
    c.setFont("Times-BoldItalic", 32)
    c.drawCentredString(width / 2, height - 95 * mm, student_name)
    
    # Underline
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    name_width = c.stringWidth(student_name, "Times-BoldItalic", 32)
    c.line(width / 2 - name_width / 2, height - 97 * mm, width / 2 + name_width / 2, height - 97 * mm)
    
    # "has successfully completed"
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 107 * mm, "has successfully completed the course")
    
    # Course title
    c.setFillColor(STARLIGHT)
    c.setFont("Times-Bold", 22)
    c.drawCentredString(width / 2, height - 122 * mm, course_title)
    
    # Footer info
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(30 * mm, 30 * mm, f"Certificate No: {cert_number}")
    c.drawString(30 * mm, 26 * mm, f"Issued: {issued_at.strftime('%d %B %Y')}")
    
    c.drawRightString(width - 30 * mm, 30 * mm, "VASTU ONE Academy")
    c.drawRightString(width - 30 * mm, 26 * mm, "hello@vastuone.in")
    
    # Verification URL
    verify_url = f"https://vastuone.in/verify/{cert_number}"
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 20 * mm, f"Verify at: {verify_url}")


@router.get("/generate/{enrollment_id}")
async def generate_certificate(
    enrollment_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Generate certificate PDF for an enrollment."""
    # Fetch enrollment
    stmt = select(Enrollment).where(
        Enrollment.id == enrollment_id,
        Enrollment.student_id == current_user.id,
    )
    enrollment = (await db.execute(stmt)).scalar_one_or_none()
    if not enrollment:
        raise HTTPException(404, "Enrollment not found")
    
    # Check completion (80%+ required)
    if enrollment.progress_pct < 80:
        raise HTTPException(400, f"Course incomplete — {enrollment.progress_pct}% done, 80% required")
    
    # Fetch course
    course_stmt = select(Course).where(Course.id == enrollment.course_id)
    course = (await db.execute(course_stmt)).scalar_one_or_none()
    if not course:
        raise HTTPException(404, "Course not found")
    
    # Check if certificate already exists
    cert_stmt = select(Certificate).where(Certificate.enrollment_id == enrollment_id)
    cert = (await db.execute(cert_stmt)).scalar_one_or_none()
    
    if not cert:
        cert = Certificate(
            enrollment_id=enrollment_id,
            certificate_number=generate_certificate_number(),
        )
        db.add(cert)
        await db.commit()
        await db.refresh(cert)
    
    # Generate PDF
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=landscape(A4))
    
    # Student name
    student_stmt = select(User).where(User.id == current_user.id)
    student = (await db.execute(student_stmt)).scalar_one_or_none()
    
    draw_certificate(
        c,
        student.full_name if student else current_user.full_name,
        course.title,
        cert.certificate_number,
        cert.issued_at,
    )
    
    c.save()
    buf.seek(0)
    
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="certificate_{cert.certificate_number}.pdf"',
        },
    )


@router.get("/my-certificates")
async def my_certificates(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """List all certificates for current student."""
    stmt = select(Certificate, Enrollment, Course).join(
        Enrollment, Certificate.enrollment_id == Enrollment.id
    ).join(
        Course, Enrollment.course_id == Course.id
    ).where(
        Enrollment.student_id == current_user.id
    )
    
    rows = (await db.execute(stmt)).all()
    return {
        "certificates": [
            {
                "id": cert.id,
                "certificate_number": cert.certificate_number,
                "course_title": course.title,
                "issued_at": cert.issued_at.isoformat(),
                "download_url": f"/api/lms/v2/certificates/generate/{enrollment.id}",
            }
            for cert, enrollment, course in rows
        ]
    }