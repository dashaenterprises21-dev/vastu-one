"""
Advanced Kundli Routes — Page C
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "engine"))
from engine.astro.advanced_kundli_engine import AdvancedKundliEngine

router = APIRouter(prefix="/api/advanced-kundli", tags=["Advanced Kundli"])
engine = AdvancedKundliEngine()


class KundliRequest(BaseModel):
    dob: str
    tob: Optional[str] = "12:00"
    place: Optional[str] = "Unknown"
    main_door: Optional[str] = "N"


@router.post("/full-report")
def full_report(req: KundliRequest):
    """Complete Advanced Kundli Report"""
    return engine.full_advanced_kundli(req.dob, req.tob, req.place, req.main_door)


@router.post("/charts")
def charts(req: KundliRequest):
    """Visual Charts (North/South Indian)"""
    return engine.generate_charts(req.dob, req.tob, req.place)


@router.post("/aspects")
def aspects(req: KundliRequest):
    """Planetary Aspects"""
    return engine.planetary_aspects(req.dob, req.tob, req.place)


@router.post("/yogas")
def yogas(req: KundliRequest):
    """50+ Yogas"""
    return engine.detect_all_yogas(req.dob, req.tob, req.place)


@router.post("/doshas")
def doshas(req: KundliRequest):
    """20+ Doshas"""
    return engine.detect_all_doshas(req.dob, req.tob, req.place)


@router.post("/dasha-5-level")
def dasha_5_level(req: KundliRequest):
    """5-Level Dasha"""
    return engine.dasha_5_level(req.dob)


@router.post("/transit")
def transit(req: KundliRequest):
    """Current Transits (Gochar)"""
    return engine.transit_gochar(req.dob, req.tob, req.place)


@router.post("/predictions")
def predictions(req: KundliRequest):
    """Life Predictions"""
    return engine.life_predictions(req.dob, req.tob, req.place)


@router.post("/muhurta")
def muhurta(req: KundliRequest):
    """Auspicious Timing"""
    return engine.muhurta(req.dob, req.tob, req.place)


@router.get("/health")
def health():
    return {"status": "ok", "engine": "advanced_kundli"}
