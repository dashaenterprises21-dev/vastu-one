"""
Vastu AI - HTML Report Routes
Server-side PDF bypass — perfect Hindi in browser
"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from datetime import datetime

from api.models.schemas import AnalyzeRequest
from api.dependencies import get_devatas_data, get_elements_data
from engine.grid_81 import Grid81
from engine.shastra_rules import ShastraRules
from engine.devata_audit import DevataAudit
from engine.element_balance import ElementBalance
from engine.brahma_audit import BrahmaAudit
from engine.direction_strength import DirectionStrength
from engine.room_analysis import RoomAnalysis
from engine.remedy_engine import RemedyEngine
from scoring.vastu_score import VastuScore

router = APIRouter(prefix="/api/report", tags=["Report"])

BASE = Path(__file__).resolve().parent.parent.parent
SHASTRA_FILE = BASE / "data" / "shastra_rules.json"
REPORTS_DIR = BASE / "reports_data"
REPORTS_DIR.mkdir(exist_ok=True)


@router.post("/create")
def create_report(req: AnalyzeRequest):
    """Report generate करो और save करो"""
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

        for p in req.plan:
            zone = grid.get_zone(p.row, p.col)
            balance.analyze_zone(zone, [p.object])
            direction.analyze_zone(zone, [p.object])
            brahma.audit_center(p.row, p.col, p.object)

        room_analysis.identify_rooms(plan_data, grid)

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

        report_id = f"VAI-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        report_data = {
            "report_id": report_id,
            "report_date": datetime.now().strftime("%d %B %Y"),
            "client_info": {
                "name": "ग्राहक",
                "address": "—"
            },
            "plan": plan_data,
            "analysis": {
                "devata_audit": audit_result,
                "element_balance": imbalance,
                "brahma_audit": brahma.get_details(),
                "direction_strength": {
                    "total_score": direction.calculate_score(),
                    "zones": direction.get_details()
                },
                "room_analysis": room_analysis.get_summary(),
                "remedies": remedies,
                "final_score": final
            }
        }

        report_file = REPORTS_DIR / f"{report_id}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        return {
            "status": "success",
            "report_id": report_id,
            "view_url": f"http://127.0.0.1:8000/report/{report_id}"
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data/{report_id}")
def get_report_data(report_id: str):
    """Report data JSON में दो"""
    report_file = REPORTS_DIR / f"{report_id}.json"
    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    with open(report_file, "r", encoding="utf-8") as f:
        return json.load(f)