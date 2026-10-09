"""
VASTU ONE - LMS v2: Certificate Generation (Enhanced)
=====================================================
Auto-generate premium certificates with QR verification.
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
from reportlab.lib.utils import ImageReader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from database.base import get_db
from database.models import Certificate, Course, Enrollment, User

import qrcode


router = APIRouter(prefix="/api/lms/v2/certificates", tags=["lms-v2-certificates"])


# Colors
VOID = colors.HexColor("#05060F")
GOLD = colors.HexColor("#D4AF37")
GOLD_DIM = colors.HexColor("#8B7020")
STARLIGHT = colors.HexColor("#F8F7F2")
MUTED = colors.HexColor("#8B8B8B")


def generate_certificate_number() -> str:
    """Generate unique certificate number."""
    prefix = "V1"
    year = datetime.utcnow().year
    random_part = secrets.token_hex(4).upper()
    return f"{prefix}-{year}-{random_part}"


def generate_qr_image(data: str):
    """Generate QR code as PIL image."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#D4AF37", back_color="#05060F")
    return img


def draw_certificate(
    c: canvas.Canvas,
    student_name: str,
    course_title: str,
    cert_number: str,
    issued_at: datetime,
    verify_url: str,
):
    """Draw premium certificate with QR code, signature, seal."""
    width, height = landscape(A4)

    # === BACKGROUND ===
    c.setFillColor(VOID)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Subtle radial gradient effect (manual)
    c.setFillColor(colors.HexColor("#0A0C1A"))
    c.circle(width / 2, height / 2, 200 * mm, fill=1, stroke=0)
    c.setFillColor(VOID)
    c.rect(0, 0, width, height, fill=0, stroke=0)

    # === GOLD BORDER (double) ===
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.rect(15 * mm, 15 * mm, width - 30 * mm, height - 30 * mm)

    c.setLineWidth(0.5)
    c.rect(18 * mm, 18 * mm, width - 36 * mm, height - 36 * mm)

    # === CORNER ORNAMENTS ===
    corner_size = 10 * mm
    corners = [
        (15 * mm, 15 * mm, 1, 1),
        (width - 15 * mm - corner_size, 15 * mm, -1, 1),
        (15 * mm, height - 15 * mm - corner_size, 1, -1),
        (width - 15 * mm - corner_size, height - 15 * mm - corner_size, -1, -1),
    ]
    for x, y, dx, dy in corners:
        c.setFillColor(GOLD)
        c.rect(x, y, corner_size, corner_size, fill=1, stroke=0)
        c.setFillColor(VOID)
        inner_offset = 3 * mm
        c.rect(
            x + (inner_offset if dx > 0 else 0),
            y + (inner_offset if dy > 0 else 0),
            corner_size - 2 * inner_offset,
            corner_size - 2 * inner_offset,
            fill=1, stroke=0,
        )
        c.setFillColor(GOLD)
        c.circle(
            x + corner_size / 2,
            y + corner_size / 2,
            1 * mm,
            fill=1, stroke=0,
        )

    # === HEADER: VASTU ONE ===
    c.setFillColor(STARLIGHT)
    c.setFont("Times-Bold", 40)
    c.drawCentredString(width / 2, height - 42 * mm, "VASTU ONE")

    c.setFillColor(GOLD)
    c.setFont("Helvetica", 10)
    c.drawCentredString(
        width / 2, height - 50 * mm, "T R A C E A B L E   V A S T U   I N T E L L I G E N C E"
    )

    # === DECORATIVE DIVIDER ===
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(width / 2 - 50 * mm, height - 55 * mm, width / 2 - 5 * mm, height - 55 * mm)
    c.line(width / 2 + 5 * mm, height - 55 * mm, width / 2 + 50 * mm, height - 55 * mm)
    c.circle(width / 2, height - 55 * mm, 1.5 * mm, fill=1, stroke=0)

    # === TITLE ===
    c.setFillColor(GOLD)
    c.setFont("Times-Italic", 22)
    c.drawCentredString(width / 2, height - 68 * mm, "Certificate of Completion")

    # === INTRO TEXT ===
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 82 * mm, "This is to certify that")

    # === STUDENT NAME (LARGE, GOLD) ===
    c.setFillColor(GOLD)
    c.setFont("Times-BoldItalic", 36)
    c.drawCentredString(width / 2, height - 100 * mm, student_name)

    # Name underline
    name_width = c.stringWidth(student_name, "Times-BoldItalic", 36)
    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.5)
    c.line(
        width / 2 - name_width / 2,
        height - 103 * mm,
        width / 2 + name_width / 2,
        height - 103 * mm,
    )

    # === COMPLETION TEXT ===
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 113 * mm, "has successfully completed the course")

    # === COURSE TITLE ===
    c.setFillColor(STARLIGHT)
    c.setFont("Times-Bold", 24)
    c.drawCentredString(width / 2, height - 128 * mm, course_title)

    # === SIGNATURE (left) ===
    sig_y = 45 * mm
    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.5)
    c.line(50 * mm, sig_y, 90 * mm, sig_y)

    c.setFillColor(GOLD)
    c.setFont("Times-Italic", 12)
    c.drawCentredString(70 * mm, sig_y + 3 * mm, "Acharya Nagpure")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawCentredString(70 * mm, sig_y - 4 * mm, "FOUNDER & DIRECTOR")

    # === SEAL (right) ===
    seal_x, seal_y = width - 70 * mm, sig_y + 3 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.circle(seal_x, seal_y, 12 * mm, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.circle(seal_x, seal_y, 10 * mm, fill=0, stroke=1)
    c.setFillColor(GOLD)
    c.setFont("Times-Bold", 10)
    c.drawCentredString(seal_x, seal_y + 2 * mm, "VASTU")
    c.setFont("Times-Bold", 9)
    c.drawCentredString(seal_x, seal_y - 2 * mm, "ONE")
    c.setFont("Helvetica", 6)
    c.drawCentredString(seal_x, seal_y - 5 * mm, "VERIFIED")

    # === QR CODE (bottom center) ===
    qr_img = generate_qr_image(verify_url)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_reader = ImageReader(qr_buffer)

    qr_size = 22 * mm
    c.drawImage(
        qr_reader,
        width / 2 - qr_size / 2,
        22 * mm,
        width=qr_size,
        height=qr_size,
        mask="auto",
    )

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6)
    c.drawCentredString(width / 2, 19 * mm, "Scan to verify")

    # === FOOTER INFO ===
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(30 * mm, 25 * mm, f"Certificate No: {cert_number}")
    c.drawString(30 * mm, 22 * mm, f"Issued: {issued_at.strftime('%d %B %Y')}")

    c.drawRightString(width - 30 * mm, 25 * mm, "VASTU ONE Academy")
    c.drawRightString(width - 30 * mm, 22 * mm, "hello@vastuone.in")

    # === VERIFY URL ===
    c.setFillColor(GOLD_DIM)
    c.setFont("Helvetica", 7)
    c.drawCentredString(width / 2, 12 * mm, f"Verify: {verify_url}")


# ==========================================
# ROUTES
# ==========================================

@router.get("/generate/{enrollment_id}")
async def generate_certificate(
    enrollment_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Generate certificate PDF for an enrollment."""
    stmt = select(Enrollment).where(
        Enrollment.id == enrollment_id,
        Enrollment.student_id == current_user.id,
    )
    enrollment = (await db.execute(stmt)).scalar_one_or_none()
    if not enrollment:
        raise HTTPException(404, "Enrollment not found")

    if enrollment.progress_pct < 80:
        raise HTTPException(
            400,
            f"Course incomplete — {enrollment.progress_pct}% done, 80% required",
        )

    course_stmt = select(Course).where(Course.id == enrollment.course_id)
    course = (await db.execute(course_stmt)).scalar_one_or_none()
    if not course:
        raise HTTPException(404, "Course not found")

    # Check existing certificate
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

    # Student name
    student_stmt = select(User).where(User.id == current_user.id)
    student = (await db.execute(student_stmt)).scalar_one_or_none()
    student_name = student.full_name if student else current_user.full_name

    # Verify URL
    verify_url = f"https://vastuone.in/verify/{cert.certificate_number}"

    # Generate PDF
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=landscape(A4))
    draw_certificate(
        c,
        student_name,
        course.title,
        cert.certificate_number,
        cert.issued_at,
        verify_url,
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
    stmt = (
        select(Certificate, Enrollment, Course)
        .join(Enrollment, Certificate.enrollment_id == Enrollment.id)
        .join(Course, Enrollment.course_id == Course.id)
        .where(Enrollment.student_id == current_user.id)
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
                "verify_url": f"/verify/{cert.certificate_number}",
            }
            for cert, enrollment, course in rows
        ]
    }


@router.get("/verify/{certificate_number}")
async def verify_certificate(
    certificate_number: str,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint to verify a certificate."""
    stmt = (
        select(Certificate, Enrollment, Course, User)
        .join(Enrollment, Certificate.enrollment_id == Enrollment.id)
        .join(Course, Enrollment.course_id == Course.id)
        .join(User, Enrollment.student_id == User.id)
        .where(Certificate.certificate_number == certificate_number)
    )
    row = (await db.execute(stmt)).first()
    if not row:
        raise HTTPException(404, "Certificate not found")

    cert, enrollment, course, student = row
    return {
        "valid": True,
        "certificate_number": cert.certificate_number,
        "student_name": student.full_name,
        "course_title": course.title,
        "issued_at": cert.issued_at.isoformat(),
        "issuer": "VASTU ONE Academy",
    }