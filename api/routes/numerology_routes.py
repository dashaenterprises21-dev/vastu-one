"""
Numerology Routes — Vastu One Enterprise API
Mulank, Bhagyank, Name Number, Property Number
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "engine"))
from engine.numerology.numerology_engine import NumerologyEngine

router = APIRouter(prefix="/api/numerology", tags=["Numerology"])
engine = NumerologyEngine()


# ─────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────
class DOBRequest(BaseModel):
    dob: str


class NameRequest(BaseModel):
    name: str
    system: Optional[str] = "chaldean"


class PropertyRequest(BaseModel):
    property_number: str


class CompatibilityRequest(BaseModel):
    num1: int
    num2: int


class FullReportRequest(BaseModel):
    dob: str
    name: str
    property_number: str


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────
@router.post("/mulank")
def get_mulank(req: DOBRequest):
    """Mulank (Root Number)"""
    result = engine.mulank(req.dob)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/bhagyank")
def get_bhagyank(req: DOBRequest):
    """Bhagyank (Destiny Number)"""
    result = engine.bhagyank(req.dob)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/name-number")
def get_name_number(req: NameRequest):
    """Name Number (Chaldean/Pythagorean)"""
    return engine.name_number(req.name, req.system)


@router.post("/property")
def get_property(req: PropertyRequest):
    """Property Number Analysis"""
    result = engine.property_number_analysis(req.property_number)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/compatibility")
def get_compatibility(req: CompatibilityRequest):
    """Compatibility between two numbers"""
    return engine.compatibility(req.num1, req.num2)


@router.post("/full-report")
def get_full_report(req: FullReportRequest):
    """Complete numerology report"""
    return engine.full_report(req.dob, req.name, req.property_number)


@router.get("/health")
def health():
    """Health check"""
    return {"status": "ok", "engine": "numerology"}
