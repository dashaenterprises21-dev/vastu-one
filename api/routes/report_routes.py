"""
VASTU ONE - Report Routes
==========================
Report generation + CRUD.
"""
from __future__ import annotations
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Client, Property, Report, ReportStatus
from engine.orchestrator import orchestrator


router = APIRouter(prefix="/api/reports", tags=["reports"])


# ==========================================
# SCHEMAS
# ==========================================
class GenerateReportRequest(BaseModel):
    property_id: str
    package: str = Field("vastu_basic", max_length=50)
    property_data: dict[str, Any] = Field(default_factory=dict)
    price_inr: float | None = None


class ReportResponse(BaseModel):
    id: str
    property_id: str
    package: str
    status: str
    findings: list
    guna_profile: dict
    scores: dict
    pdf_url: str | None
    price_inr: float | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    total: int
    items: list[ReportResponse]


class ReportStatusUpdate(BaseModel):
    status: ReportStatus


# ==========================================
# GENERATE
# ==========================================
@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(
    req: GenerateReportRequest,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a Vastu report for a property.
    
    Runs the engine orchestrator, saves findings + guna profile + score.
    """
    # Verify property belongs to tenant
    stmt = (
        select(Property)
        .join(Client)
        .where(
            Property.id == req.property_id,
            Client.tenant_id == current_user.tenant_id,
        )
    )
    prop = (await db.execute(stmt)).scalar_one_or_none()
    if not prop:
        raise HTTPException(404, "Property not found in your tenant")
    
    # Merge DB data + user-provided data
    property_data = {
        "name": prop.name,
        "property_type": prop.property_type.value,
        "north_direction_deg": prop.north_direction_deg or 0,
        "latitude": prop.latitude,
        "longitude": prop.longitude,
        **req.property_data,
    }
    
    # Run orchestrator
    try:
        result = orchestrator.run_all(property_data)
    except Exception as e:
        raise HTTPException(500, f"Engine orchestration failed: {e}")
    
    # Save report
    report = Report(
        property_id=req.property_id,
        package=req.package,
        status=ReportStatus.DRAFT,
        findings=result.get("findings", []),
        guna_profile=result.get("guna_profile", {}),
        scores=result.get("overall_score", {}),
        price_inr=req.price_inr,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


# ==========================================
# LIST
# ==========================================
@router.get("", response_model=ReportListResponse)
async def list_reports(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    property_id: str | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    """List reports in current tenant."""
    stmt = (
        select(Report)
        .join(Property)
        .join(Client)
        .where(Client.tenant_id == current_user.tenant_id)
    )
    if property_id:
        stmt = stmt.where(Report.property_id == property_id)
    if status_filter:
        stmt = stmt.where(Report.status == status_filter)
    
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0
    
    stmt = stmt.order_by(Report.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    return ReportListResponse(total=total, items=list(items))


# ==========================================
# GET ONE
# ==========================================
@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get single report (tenant-scoped)."""
    stmt = (
        select(Report)
        .join(Property)
        .join(Client)
        .where(Report.id == report_id, Client.tenant_id == current_user.tenant_id)
    )
    report = (await db.execute(stmt)).scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    return report


# ==========================================
# UPDATE STATUS
# ==========================================
@router.put("/{report_id}/status", response_model=ReportResponse)
async def update_report_status(
    report_id: str,
    req: ReportStatusUpdate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Update report status (draft → in_review → approved → delivered)."""
    stmt = (
        select(Report)
        .join(Property)
        .join(Client)
        .where(Report.id == report_id, Client.tenant_id == current_user.tenant_id)
    )
    report = (await db.execute(stmt)).scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    
    report.status = req.status
    await db.commit()
    await db.refresh(report)
    return report


# ==========================================
# DELETE
# ==========================================
@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: str,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Delete report."""
    stmt = (
        select(Report)
        .join(Property)
        .join(Client)
        .where(Report.id == report_id, Client.tenant_id == current_user.tenant_id)
    )
    report = (await db.execute(stmt)).scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    
    await db.delete(report)
    await db.commit()
    return None

# ==========================================
# PDF DOWNLOAD
# ==========================================
from fastapi.responses import StreamingResponse
from io import BytesIO
from engine.report.pdf_generator import pdf_generator


@router.get("/{report_id}/pdf")
async def download_report_pdf(
    report_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Download report as PDF.
    Fetches report from DB, generates branded PDF, returns as attachment.
    """
    # Fetch report (tenant-scoped)
    stmt = (
        select(Report)
        .join(Property)
        .join(Client)
        .where(Report.id == report_id, Client.tenant_id == current_user.tenant_id)
    )
    report = (await db.execute(stmt)).scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    
    # Fetch property + client for branding
    prop_stmt = select(Property).where(Property.id == report.property_id)
    prop = (await db.execute(prop_stmt)).scalar_one_or_none()
    
    # Build report_data
    report_data = {
        "id": report.id,
        "package": report.package,
        "property_name": prop.name if prop else "Property",
        "property_address": f"{prop.address or ''}, {prop.city or ''} {prop.pincode or ''}".strip(", "),
        "generated_at": report.created_at.isoformat(),
        "consultant_name": current_user.full_name,
        "consultant_email": current_user.email,
        "engines_count": 14,
        "findings": report.findings or [],
        "guna_profile": report.guna_profile or {},
        "scores": report.scores or {},
    }
    
    # Generate PDF
    try:
        pdf_bytes = pdf_generator.render(report_data)
    except Exception as e:
        raise HTTPException(500, f"PDF generation failed: {e}")
    
    # Return as streaming response
    filename = f"vastu_one_report_{report.id[:8]}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )
