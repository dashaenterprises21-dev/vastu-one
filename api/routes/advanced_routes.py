from fastapi import APIRouter
from engine.astro.election_prediction import predict_elections
# from engine.astro.celebrity_charts import get_all_celebrities, analyze_celebrity  # TODO: file missing
from engine.astro.world_prediction_extended import get_extended_countries, analyze_extended_country

router = APIRouter(prefix="/api/advanced", tags=["advanced"])

@router.get("/elections")
async def get_elections():
    return predict_elections()

@router.get("/celebrities")
async def get_celebrities():
    return {"celebrities": get_all_celebrities(), "total": len(get_all_celebrities())}

@router.get("/celebrity/{name}")
async def get_celebrity(name: str):
    return analyze_celebrity(name)

@router.get("/countries/extended")
async def get_countries_extended():
    return {"countries": get_extended_countries(), "total": len(get_extended_countries())}

@router.get("/country/extended/{name}")
async def get_country_extended(name: str):
    return analyze_extended_country(name)
