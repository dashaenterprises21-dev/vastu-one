"""
VASTU ONE — Deep World Prediction Routes
"""

from fastapi import APIRouter, HTTPException
from engine.astro.deep_world_prediction import analyze_deep_world_prediction, get_all_deep_countries

router = APIRouter(prefix="/api/world/deep", tags=["world-deep"])


@router.get("/countries")
async def list_countries():
    return {"countries": get_all_deep_countries(), "total": len(get_all_deep_countries())}


@router.get("/predict/{country}")
async def deep_predict(country: str):
    result = analyze_deep_world_prediction(country)
    if not result or not result.get("chart"):
        raise HTTPException(status_code=404, detail=f"Country not found: {country}")
    return result
