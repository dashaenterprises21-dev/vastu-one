from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class PlanItem(BaseModel):
    row: int = Field(..., ge=0, le=8)
    col: int = Field(..., ge=0, le=8)
    object: str


class AnalyzeRequest(BaseModel):
    plan: List[PlanItem]
    property_type: Optional[str] = "residential"
    floors: Optional[int] = 1


class IssueOut(BaseModel):
    pada: int
    devata: str
    hindi: str
    direction: str
    object: Optional[str] = None
    problem: str
    severity: str
    domain_affected: List[str]
    shastra_reference: Optional[Dict[str, Any]] = None
    penalty: Optional[int] = None
    positive_objects: Optional[List[str]] = []
    negative_objects: Optional[List[str]] = []


class DevataStatusOut(BaseModel):
    pada: int
    devata: str
    hindi: str
    direction: str
    object: str
    domain: List[str]
    element: str
    status: str
    reason: Optional[str] = None
    shastra_reference: Optional[Dict[str, Any]] = None


class DevataAuditOut(BaseModel):
    total_issues: int
    total_correct: int
    issues: List[IssueOut]
    positive_hits: List[DevataStatusOut]
    all_devatas_status: List[DevataStatusOut]
    devata_score: int


class ElementBalanceOut(BaseModel):
    weak_elements: List[str]
    strong_elements: List[str]
    element_score: float
    balance: Dict[str, int]


class BrahmaAuditOut(BaseModel):
    center_object: Optional[str] = None
    score: int
    shastra_reason: Optional[str] = None
    issues: List[str]


class ZoneDetailOut(BaseModel):
    zone: str
    name: str
    element: str
    deity: str
    score: float
    base_score: int
    used: bool
    objects: List[str]
    notes: List[str]
    status: str


class DirectionOut(BaseModel):
    total_score: float
    zones: List[ZoneDetailOut]


class RoomItemOut(BaseModel):
    room_type: str
    room_hindi: str
    zone: str
    object: str
    row: int
    col: int
    is_correct: bool
    is_defect: bool
    best_directions: List[str]
    bad_directions: List[str]
    shastra: str
    reason: str
    status: str


class RoomAnalysisOut(BaseModel):
    total_rooms_analyzed: int
    correct_placements: int
    defects: int
    rooms: List[RoomItemOut]


class RemedyOut(BaseModel):
    devata: str
    hindi: str
    direction: str
    problem_domain: List[str]
    remedy: Dict[str, Any]
    shastra_reference: Optional[Dict[str, Any]] = None


class FinalScoreOut(BaseModel):
    total_score: float
    grade: str
    breakdown: Dict[str, float]
    weights: Dict[str, float]


class AnalyzeResponse(BaseModel):
    devata_audit: DevataAuditOut
    element_balance: ElementBalanceOut
    brahma_audit: BrahmaAuditOut
    direction_strength: DirectionOut
    room_analysis: RoomAnalysisOut
    remedies: List[RemedyOut]
    final_score: FinalScoreOut


class HealthOut(BaseModel):
    status: str
    version: str
    total_devatas: int
    total_elements: int