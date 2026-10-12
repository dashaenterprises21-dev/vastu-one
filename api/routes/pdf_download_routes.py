"""
VASTU ONE - PDF Download API
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from engine.report.pdf_generator_v3 import generate_pdf

router = APIRouter(prefix="/api/world/full", tags=["world-full"])


@router.get("/pdf/{country}")
async def download_pdf(country: str):
    buffer = generate_pdf(country)
    if buffer is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=" + country + "_report.pdf"}
    )
