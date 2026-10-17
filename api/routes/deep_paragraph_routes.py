"""
VASTU ONE - Deep Paragraph API Routes
"""

from fastapi import APIRouter, HTTPException
from engine.astro.deep_paragraph_engine import get_full_explanation_report
from engine.astro.bnn_hidden_gems import analyze_bnn_complete
from engine.astro.complete_chart_engine import calculate_complete_chart
from engine.astro.master_prediction_engine import COUNTRY_CHARTS

router = APIRouter(prefix="/api/world/deep-paragraph", tags=["deep-paragraph"])


@router.get("/countries")
async def list_countries():
    return {"countries": list(COUNTRY_CHARTS.keys()), "total": len(COUNTRY_CHARTS)}


@router.get("/paragraphs/{country}")
async def get_paragraphs(country: str):
    result = get_full_explanation_report(country)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/bnn/{country}")
async def get_bnn(country: str):
    if country not in COUNTRY_CHARTS:
        raise HTTPException(status_code=404, detail="Country not found")
    data = COUNTRY_CHARTS[country]
    y, m, d = data["date"]
    chart = calculate_complete_chart(y, m, d, data["time"], data["lat"], data["lng"])
    return analyze_bnn_complete(chart)
