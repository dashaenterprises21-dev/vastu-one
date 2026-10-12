"""
VASTU ONE - Full Prediction API Routes
All engines combined
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from engine.astro.predictions_engine import get_predictions, COUNTRY_CHARTS

router = APIRouter(prefix="/api/world/full", tags=["world-full"])


@router.get("/countries")
async def list_countries():
    return {"countries": list(COUNTRY_CHARTS.keys()), "total": len(COUNTRY_CHARTS)}


@router.get("/predict/{country}")
async def full_predict(country: str):
    result = get_predictions(country)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/predict/{country}/{year}/{month}/{day}")
async def full_predict_date(country: str, year: int, month: int, day: int):
    target = datetime(year, month, day)
    result = get_predictions(country, target)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
