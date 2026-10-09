"""
Numerology V3 Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "engine"))
from engine.numerology.numerology_engine_v3 import NumerologyEngineV3

router = APIRouter(prefix="/api/numerology-v3", tags=["Numerology V3"])
engine = NumerologyEngineV3()

class NumRequest(BaseModel):
    dob: str
    name: str

@router.post("/full-report")
def full_report(req: NumRequest):
    return engine.full_report(req.dob, req.name)

@router.get("/health")
def health():
    return {"status": "ok", "engine": "numerology_v3"}
