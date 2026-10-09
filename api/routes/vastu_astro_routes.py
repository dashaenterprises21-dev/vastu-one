"""
Vastu-Astro Integration Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "engine"))
from engine.vastu.astro_integration import VastuAstroIntegrationV2

router = APIRouter(prefix="/api/vastu-astro", tags=["Vastu-Astro Integration"])
engine = VastuAstroIntegrationV2()


class IntegrationRequest(BaseModel):
    dob: str
    tob: Optional[str] = "12:00"
    place: Optional[str] = "Unknown"
    main_door_direction: Optional[str] = "N"


@router.post("/full-report")
def full_report(req: IntegrationRequest):
    """Complete Vastu-Astro Integration report"""
    return engine.full_integration_report(req.dob, req.tob, req.place, req.main_door_direction)


@router.post("/bhadhaka")
def bhadhaka(req: IntegrationRequest):
    """Bhadhaka planet calculation"""
    return engine.calculate_bhadhaka(req.dob, req.tob, req.place)


@router.post("/main-door")
def main_door(direction: str = "N"):
    """Main door analysis"""
    return engine.analyze_main_door(direction)


@router.post("/compare")
def compare(req: IntegrationRequest):
    """Bhadhaka vs Main Door comparison"""
    return engine.compare_bhadhaka_door(req.dob, req.tob, req.place, req.main_door_direction)


@router.post("/dasha-alert")
def dasha_alert(req: IntegrationRequest):
    """Dasha alert — current planet direction vs main door"""
    return engine.dasha_alert(req.dob, req.tob, req.place, req.main_door_direction)


@router.post("/remedies")
def remedies(req: IntegrationRequest):
    """Vastu remedies for Bhadhaka and main door"""
    bhadhaka = engine.calculate_bhadhaka(req.dob, req.tob, req.place)
    return engine.vastu_remedies(bhadhaka.get("bhadhaka_planet", ""), req.main_door_direction)


@router.get("/health")
def health():
    return {"status": "ok", "engine": "vastu_astro_integration"}
