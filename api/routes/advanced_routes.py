"""
Vastu One - Advanced Vastu Routes
Includes: 32 Entrance Padas, Ayadi, 3-Tier Remedies, Pooja, Plot Layout
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from engine.entrance_audit import EntranceAudit
from engine.ayadi_engine import AyadiEngine
from engine.remedy_engine_v2 import RemedyEngineV3
from engine.pooja_engine import PoojaEngine
from engine.plot_layout_engine import PlotLayoutEngine
from engine.mahavastu_engine import MahaVastuEngine

router = APIRouter(prefix="/api/advanced", tags=["Advanced Vastu"])


class EntranceRequest(BaseModel):
    direction: str
    pada: int
    degree: Optional[float] = None


class AyadiRequest(BaseModel):
    length: float
    breadth: float
    height: float


class PlotLayoutRequest(BaseModel):
    plot_length: float
    plot_breadth: float
    facing_direction: str = "North"


class MultiPoojaRequest(BaseModel):
    defects: List[str]


@router.post("/entrance/audit")
def audit_entrance(req: EntranceRequest):
    try:
        engine = EntranceAudit()
        result = engine.audit_entrance(req.direction, req.pada, req.degree)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entrance/all")
def list_all_padas():
    engine = EntranceAudit()
    return {"status": "success", "padas": engine.list_all_padas()}


@router.post("/ayadi/calculate")
def calculate_ayadi(req: AyadiRequest):
    try:
        engine = AyadiEngine()
        result = engine.calculate(req.length, req.breadth, req.height)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/remedies/all")
def list_all_remedies():
    engine = RemedyEngineV3()
    return {"status": "success", "defects": engine.list_all_defects()}


@router.get("/remedies/{defect_key}")
def get_remedy(defect_key: str):
    engine = RemedyEngineV3()
    result = engine.get_remedy(defect_key)
    if not result:
        raise HTTPException(status_code=404, detail="Defect not found")
    return {"status": "success", "data": result}


@router.get("/pooja/all")
def list_all_poojas():
    engine = PoojaEngine()
    return {"status": "success", "poojas": engine.list_all_poojas()}


@router.get("/pooja/for-defect/{defect_key}")
def get_pooja_for_defect(defect_key: str):
    engine = PoojaEngine()
    result = engine.get_pooja_for_defect(defect_key)
    return {"status": "success", "data": result}


@router.post("/pooja/plan")
def generate_pooja_plan(req: MultiPoojaRequest):
    engine = PoojaEngine()
    result = engine.generate_full_puja_plan(req.defects)
    return {"status": "success", "data": result}


@router.post("/plot/layout")
def generate_plot_layout(req: PlotLayoutRequest):
    try:
        engine = PlotLayoutEngine()
        result = engine.generate_layout(req.plot_length, req.plot_breadth, req.facing_direction)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══ MAHAVASTU ═══
class SpaceSurgeryRequest(BaseModel):
    zone: str
    defect_type: str = "cut_corner"


class PyramidRequest(BaseModel):
    zone: str
    issue_type: str = "Cut_Corner"


class MarmaRequest(BaseModel):
    marma_zone: str


@router.post("/mahavastu/space-surgery")
def space_surgery(req: SpaceSurgeryRequest):
    engine = MahaVastuEngine()
    result = engine.suggest_space_surgery(req.zone, req.defect_type)
    return {"status": "success", "data": result}


@router.post("/mahavastu/pyramids")
def pyramids(req: PyramidRequest):
    engine = MahaVastuEngine()
    result = engine.suggest_pyramids(req.zone, req.issue_type)
    return {"status": "success", "data": result}


@router.post("/mahavastu/marma")
def marma(req: MarmaRequest):
    engine = MahaVastuEngine()
    result = engine.suggest_marma_remedy(req.marma_zone)
    return {"status": "success", "data": result}
