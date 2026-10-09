"""
Advanced Astro Routes — Vastu One Enterprise API
Complete Vedic Astrology endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "engine"))
from engine.astro.advanced_astro_engine import AdvancedAstroEngine

router = APIRouter(prefix="/api/advanced-astro", tags=["Advanced Astro"])
engine = AdvancedAstroEngine()


class BirthRequest(BaseModel):
    dob: str
    tob: Optional[str] = "12:00"
    place: Optional[str] = "Unknown"


class NakshatraRequest(BaseModel):
    nakshatra_name: str


@router.post("/full-report")
def full_report(req: BirthRequest):
    """Complete advanced astro report"""
    return engine.full_advanced_report(req.dob, req.tob, req.place)


@router.post("/lagna")
def lagna(req: BirthRequest):
    """Lagna (Ascendant) calculation"""
    result = engine.calculate_lagna(req.dob, req.tob, req.place)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/grah-positions")
def grah_positions(req: BirthRequest):
    """9 Grah positions"""
    result = engine.calculate_grah_positions(req.dob, req.tob, req.place)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/bhav-analysis")
def bhav_analysis(req: BirthRequest):
    """12 Bhav analysis"""
    result = engine.calculate_bhav_analysis(req.dob, req.tob, req.place)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/nakshatras")
def all_nakshatras():
    """All 27 Nakshatras"""
    return engine.nakshatras


@router.post("/nakshatra")
def nakshatra_details(req: NakshatraRequest):
    """Single Nakshatra details"""
    result = engine.nakshatra_details(req.nakshatra_name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/dasha")
def dasha(req: BirthRequest):
    """Vimshottari Dasha (Maha + Antar)"""
    result = engine.vimshottari_dasha_detailed(req.dob)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/yogas")
def yogas(req: BirthRequest):
    """Detect Yogas"""
    return engine.detect_yogas(req.dob, req.tob, req.place)


@router.post("/doshas")
def doshas(req: BirthRequest):
    """Detect Doshas"""
    return engine.detect_doshas(req.dob, req.tob, req.place)


@router.post("/ashtakavarga")
def ashtakavarga(req: BirthRequest):
    """Ashtakavarga calculation"""
    return engine.ashtakavarga(req.dob, req.tob, req.place)


@router.post("/remedies")
def remedies(req: BirthRequest):
    """Gemstone, Mantra, Daan remedies"""
    return engine.remedies(req.dob, req.tob, req.place)


@router.post("/dasha-timeline")
def dasha_timeline(req: BirthRequest):
    """Dasha timeline for visualization"""
    return engine.dasha_timeline(req.dob)


@router.get("/health")
def health():
    return {"status": "ok", "engine": "advanced_astro"}
