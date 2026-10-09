"""
Pooja Routes — Vastu One Enterprise API
Pooja + Mantra recommendations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

router = APIRouter(prefix="/api/pooja", tags=["Pooja"])

with open(os.path.join(DATA_DIR, "pooja_mantra.json"), "r", encoding="utf-8-sig") as f:
    POOJA_DATA = json.load(f)


# ─────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────
class PoojaRequest(BaseModel):
    purpose: str


class MantraRequest(BaseModel):
    planet: str


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────
@router.get("/all")
def get_all_pooja():
    """Saari pooja + mantra"""
    return POOJA_DATA


@router.post("/by-purpose")
def get_pooja_by_purpose(req: PoojaRequest):
    """Purpose ke hisaab se pooja"""
    result = []
    poojas = POOJA_DATA.get("poojas", POOJA_DATA)
    if isinstance(poojas, dict):
        for name, info in poojas.items():
            if isinstance(info, dict) and info.get("purpose") == req.purpose:
                result.append({"name": name, **info})
    elif isinstance(poojas, list):
        result = [p for p in poojas if p.get("purpose") == req.purpose]
    if not result:
        raise HTTPException(status_code=404, detail=f"No pooja for purpose {req.purpose}")
    return result


@router.post("/mantra")
def get_mantra(req: MantraRequest):
    """Planet ka mantra"""
    mantras = POOJA_DATA.get("mantras", {})
    if req.planet in mantras:
        return {"planet": req.planet, "mantra": mantras[req.planet]}
    raise HTTPException(status_code=404, detail=f"No mantra for planet {req.planet}")


@router.get("/health")
def health():
    """Health check"""
    return {"status": "ok", "engine": "pooja"}
