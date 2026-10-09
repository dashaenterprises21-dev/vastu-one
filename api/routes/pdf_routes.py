from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
import uuid

from api.models.schemas import AnalyzeRequest
from api.dependencies import get_devatas_data, get_elements_data
from engine.vastu.grid_81 import Grid81
from engine.vastu.shastra_rules import ShastraRules
from engine.vastu.devata_audit import DevataAudit
from engine.vastu.element_balance import ElementBalance
from engine.vastu.brahma_audit import BrahmaAudit
from engine.vastu.direction_strength import DirectionStrength
from engine.vastu.remedy_engine import RemedyEngine
from scoring.vastu_score import VastuScore
from pdf_engine.html_report import HTMLVastuReport

router = APIRouter(prefix="/api/pdf", tags=["PDF Reports"])

BASE = Path(__file__).resolve().parent.parent.parent
SHASTRA_FILE = BASE / "data" / "shastra_rules.json"
OUTPUT_DIR = BASE / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


@router.post("/generate")
def generate_pdf(req: AnalyzeRequest):
    """
    PDF report generate करो और download link दो
    """
    try:
        # 1. पूरा analysis चलाओ
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
        remedy = RemedyEngine(devatas_json, elements_json)
        scorer = VastuScore()

        plan_data = [{"row": p.row, "col": p.col, "object": p.object} for p in req.plan]
        audit_result = audit.audit_plan(plan_data)

        for p in req.plan:
            zone = grid.get_zone(p.row, p.col)
            balance.analyze_zone(zone, [p.object])
            direction.analyze_zone(zone, [p.object])
            brahma.audit_center(p.row, p.col, p.object)

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

        analysis_data = {
            "devata_audit": audit_result,
            "element_balance": imbalance,
            "brahma_audit": brahma.get_details(),
            "direction_strength": {
                "total_score": direction.calculate_score(),
                "zones": direction.get_details()
            },
            "remedies": remedies,
            "final_score": final
        }

        # 2. PDF generate करो
        report_id = f"VAI-{uuid.uuid4().hex[:8].upper()}"
        filename = f"vastu_report_{report_id}.pdf"
        output_path = OUTPUT_DIR / filename

        generator = HTMLVastuReport(str(output_path))
        generator.generate(analysis_data, client_info={
                "name": getattr(req, "client_name", "ग्राहक"),
                "address": getattr(req, "client_address", ""),
            }, raw_devatas=devatas_json, plan_data=plan_data)

        return {
            "status": "success",
            "report_id": report_id,
            "filename": filename,
            "download_url": f"/api/pdf/download/{filename}",
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
def download_pdf(filename: str):
    """PDF download करो"""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )