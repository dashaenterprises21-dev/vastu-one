"""
VASTU ONE - Real Transit API Routes
Predictions from actual Swiss Ephemeris calculations
"""

from fastapi import APIRouter, HTTPException
from engine.astro.real_transit_engine import analyze_real_transit, RealTransitEngine

router = APIRouter(prefix="/api/world/real", tags=["world-real"])


@router.get("/countries")
async def list_countries():
    """List all 25 countries"""
    countries = list(RealTransitEngine.COUNTRY_DATA.keys()) if hasattr(RealTransitEngine, 'COUNTRY_DATA') else []
    return {"countries": countries, "total": len(countries)}


@router.get("/transit/{country}")
async def get_real_transit(country: str):
    """Get real transit analysis for country"""
    result = analyze_real_transit(country)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/transit/{country}/{year}/{month}/{day}")
async def get_transit_for_date(country: str, year: int, month: int, day: int):
    """Get transit for specific date"""
    from datetime import datetime
    engine = RealTransitEngine(country)
    target = datetime(year, month, day)
    result = engine.analyze_transit(target)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result