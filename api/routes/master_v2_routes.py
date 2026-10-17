"""
VASTU ONE - Master Prediction API Routes
All 6 layers in one endpoint
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS

router = APIRouter(prefix="/api/world/master-v2", tags=["world-master-v2"])


@router.get("/countries")
async def list_countries():
    return {"countries": list(COUNTRY_CHARTS.keys()), "total": len(COUNTRY_CHARTS)}


@router.get("/predict/{country}")
async def master_predict(country: str):
    result = get_master_prediction(country)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/predict/{country}/{year}/{month}/{day}")
async def master_predict_date(country: str, year: int, month: int, day: int):
    target = datetime(year, month, day)
    result = get_master_prediction(country, target)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
