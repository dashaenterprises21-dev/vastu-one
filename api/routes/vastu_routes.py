from fastapi import APIRouter, HTTPException
from pathlib import Path
from api.models.schemas import AnalyzeRequest, AnalyzeResponse
from api.dependencies import get_devatas_data, get_elements_data
from engine.vastu.grid_81 import Grid81
from engine.vastu.shastra_rules import ShastraRules
from engine.vastu.devata_audit import DevataAudit
from engine.vastu.element_balance import ElementBalance
from engine.vastu.brahma_audit import BrahmaAudit
from engine.vastu.direction_strength import DirectionStrength
from engine.vastu.room_analysis import RoomAnalysis
from engine.vastu.remedy_engine import RemedyEngine
from scoring.vastu_score import VastuScore

router = APIRouter(prefix="/api/vastu", tags=["Vastu Analysis"])

BASE = Path(__file__).resolve().parent.parent.parent
SHASTRA_FILE = BASE / "data" / "shastra_rules.json"


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_plan(req: AnalyzeRequest):
    try:
        devatas_json = get_devatas_data()
        elements_json = get_elements_data()
        shastra = ShastraRules(SHASTRA_FILE)

        grid = Grid81()
        grid.load_devatas(devatas_json)
        grid.map_devata_to_grid()

        audit = DevataAudit(grid, devatas_json, shastra)
        balance = ElementBalance(elements_json)
        brahma = BrahmaAudit()
        direction = DirectionStrength()
        room_analysis = RoomAnalysis()
        remedy = RemedyEngine(devatas_json, elements_json)
        scorer = VastuScore()

        plan_data = [{"row": p.row, "col": p.col, "object": p.object} for p in req.plan]
        audit_result = audit.audit_plan(plan_data)

        # हर object को engines में भेजो
        for p in req.plan:
            zone = grid.get_zone(p.row, p.col)
            balance.analyze_zone(zone, [p.object])
            direction.analyze_zone(zone, [p.object])
            brahma.audit_center(p.row, p.col, p.object)

        # Room analysis
        room_analysis.identify_rooms(plan_data, grid)
        room_summary = room_analysis.get_summary()

        imbalance = balance.get_imbalance()
        imbalance["element_score"] = balance.calculate_score()
        imbalance["balance"] = balance.balance

        remedies = []
        for issue in audit_result["issues"]:
            r = remedy.remedy_for_devata(issue["devata"])
            if r:
                r["shastra_reference"] = issue.get("shastra_reference")
                remedies.append(r)

        final = scorer.calculate(
            devata_score=audit_result["devata_score"],
            element_balance_score=balance.calculate_score(),
            brahma_score=brahma.calculate_score(),
            direction_score=direction.calculate_score()
        )

        return {
            "devata_audit": audit_result,
            "element_balance": imbalance,
            "brahma_audit": brahma.get_details(),
            "direction_strength": {
                "total_score": direction.calculate_score(),
                "zones": direction.get_details()
            },
            "room_analysis": room_summary,
            "remedies": remedies,
            "final_score": final
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))