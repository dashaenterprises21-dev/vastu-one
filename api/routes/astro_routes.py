"""
Astro Routes — Vastu One Enterprise API
Kundli, Planets, Dasha, Houses
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "engine"))
from engine.astro.astro_engine_v3_complete import AstroEngineV3Complete

router = APIRouter(prefix="/api/astro", tags=["Astro"])
engine = AstroEngineV3Complete()


# ─────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────
class KundliRequest(BaseModel):
    dob: str
    tob: Optional[str] = "12:00"
    place: Optional[str] = "Unknown"


class PlanetDirectionRequest(BaseModel):
    direction: str


class HouseRequest(BaseModel):
    house_number: int


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────
@router.post("/kundli")
def get_kundli(req: KundliRequest):
    """Kundli generate karo"""
    result = engine.generate_kundli(req.dob, req.tob, req.place)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/planets")
def get_planets():
    """Saare planets ka direction map"""
    return engine.planet_direction_map()


@router.post("/planets/direction")
def get_planets_by_direction(req: PlanetDirectionRequest):
    """Direction ke planets"""
    result = engine.planet_for_direction(req.direction.upper())
    if not result:
        raise HTTPException(status_code=404, detail=f"No planets for direction {req.direction}")
    return result


@router.post("/house")
def get_house(req: HouseRequest):
    """House analysis (1-12)"""
    result = engine.house_analysis(req.house_number)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/dasha")
def get_dasha(nakshatra: str = "Ashwini"):
    """Vimshottari Dasha"""
    return engine.vimshottari_dasha(nakshatra)


@router.post("/full-report")
def get_full_report(req: KundliRequest):
    """Complete astro report"""
    return engine.full_report(req.dob, req.tob, req.place)


@router.get("/health")
def health():
    """Health check"""
    return {"status": "ok", "engine": "astro"}
