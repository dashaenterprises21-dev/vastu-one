"""
Complete Astro V3 API — Full Engine
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "engine"))
from engine.astro.astro_engine_v3_complete import AstroEngineV3Complete

router = APIRouter(prefix="/api/astro-v3", tags=["Astro V3 Complete"])
engine = AstroEngineV3Complete()


class BirthRequest(BaseModel):
    dob: str
    tob: Optional[str] = "12:00"
    place: Optional[str] = "Unknown"


@router.post("/full-report")
def full_report(req: BirthRequest):
    return engine.full_report(req.dob, req.tob, req.place)


@router.post("/positions")
def positions(req: BirthRequest):
    return engine.calculate_positions(req.dob, req.tob)


@router.post("/lagna")
def lagna(req: BirthRequest):
    return engine.calculate_lagna(req.dob, req.tob, req.place)


@router.post("/bhava-chalit")
def bhava(req: BirthRequest):
    return engine.bhava_chalit(req.dob, req.tob, req.place)


@router.post("/shodashvarga")
def varga(req: BirthRequest):
    return engine.shodashvarga(req.dob, req.tob)


@router.post("/dasha")
def dasha(req: BirthRequest):
    return engine.vimshottari_dasha(req.dob, req.tob)


@router.post("/ashtakavarga")
def ashtak(req: BirthRequest):
    return engine.ashtakavarga(req.dob, req.tob)


@router.post("/shadbala")
def shadbala(req: BirthRequest):
    return engine.shadbala(req.dob, req.tob)


@router.post("/yogas")
def yogas(req: BirthRequest):
    return engine.detect_yogas(req.dob, req.tob)


@router.post("/doshas")
def doshas(req: BirthRequest):
    return engine.detect_doshas(req.dob, req.tob)


@router.get("/health")
def health():
    return {"status": "ok", "engine": "astro_v3_complete"}
