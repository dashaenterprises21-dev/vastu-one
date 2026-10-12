"""
VASTU ONE — World Prediction Routes
"""

from fastapi import APIRouter, HTTPException
from engine.astro.world_prediction_engine import analyze_world_prediction, get_all_countries

router = APIRouter(prefix="/api/world", tags=["world"])


@router.get("/countries")
async def list_countries():
    """List all countries"""
    return {"countries": get_all_countries(), "total": len(get_all_countries())}


@router.get("/predict/{country}")
async def predict_country(country: str):
    """Get prediction for a country"""
    result = analyze_world_prediction(country)
    if not result or not result.get("chart_data"):
        raise HTTPException(status_code=404, detail=f"Country not found: {country}")
    return result
