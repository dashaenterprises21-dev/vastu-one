from fastapi import APIRouter, HTTPException
from engine.astro.master_world_prediction import analyze_master_world, get_all_master_countries

router = APIRouter(prefix="/api/world/master", tags=["world-master"])

@router.get("/countries")
async def list_countries():
    return {"countries": get_all_master_countries(), "total": len(get_all_master_countries())}

@router.get("/predict/{country}")
async def master_predict(country: str):
    result = analyze_master_world(country)
    if not result or not result.get("chart"):
        raise HTTPException(status_code=404, detail=f"Country not found: {country}")
    return result
