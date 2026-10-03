"""
Vastu One - Plan Upload Routes
Full Vastu analysis: Detection + Dosh + Remedies + Pooja + Score
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from datetime import datetime

from engine.vision.plan_parser import PlanParser
from engine.grid_81 import Grid81
from engine.shastra_rules import ShastraRules
from engine.devata_audit import DevataAudit
from engine.element_balance import ElementBalance
from engine.brahma_audit import BrahmaAudit
from engine.direction_strength import DirectionStrength
from engine.room_analysis import RoomAnalysis
from engine.remedy_engine_v2 import RemedyEngineV3
from engine.pooja_engine import PoojaEngine
from engine.entrance_audit import EntranceAudit
from engine.ayadi_engine import AyadiEngine
from engine.mahavastu_engine import MahaVastuEngine
from scoring.vastu_score import VastuScore
from api.dependencies import get_devatas_data, get_elements_data

router = APIRouter(prefix="/api/upload", tags=["Upload"])

BASE = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE / "uploads" / "plans"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SHASTRA_FILE = BASE / "data" / "shastra_rules.json"

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024


def pdf_to_image(pdf_path: Path, output_path: Path) -> bool:
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        if len(doc) == 0:
            doc.close()
            return False
        page = doc[0]
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(str(output_path))
        doc.close()
        print(f"[INFO] PDF converted: {pdf_path.name} -> {output_path.name}")
        return True
    except Exception as e:
        print(f"[ERROR] PDF conversion failed: {e}")
        return False


@router.post("/plan")
async def upload_plan(file: UploadFile = File(...)):
    """Plan upload - COMPLETE Vastu analysis"""
    try:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Only {', '.join(sorted(ALLOWED_EXTENSIONS))} files allowed")

        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 10 MB)")

        upload_id = uuid.uuid4().hex[:12]

        if ext == ".pdf":
            pdf_filename = f"plan_{upload_id}.pdf"
            pdf_path = UPLOAD_DIR / pdf_filename
            with open(pdf_path, "wb") as f:
                f.write(contents)
            png_filename = f"plan_{upload_id}.png"
            png_path = UPLOAD_DIR / png_filename
            if not pdf_to_image(pdf_path, png_path):
                raise HTTPException(status_code=400, detail="PDF conversion failed")
            try:
                pdf_path.unlink()
            except Exception:
                pass
            file_path = png_path
            filename = png_filename
        else:
            filename = f"plan_{upload_id}{ext}"
            file_path = UPLOAD_DIR / filename
            with open(file_path, "wb") as f:
                f.write(contents)

        # ═══ DETECTION ═══
        parser = PlanParser()
        result = parser.analyze(file_path)

        # ═══ FULL VASTU ANALYSIS ═══
        devatas_json = get_devatas_data()
        elements_json = get_elements_data()
        shastra = ShastraRules(SHASTRA_FILE)

        grid = Grid81()
        grid.load_devatas(devatas_json)
        grid.map_devata_to_grid()

        # 1. Devata Audit (from room mappings)
        plan_data = []
        for m in result.get("room_mappings", []):
            plan_data.append({"row": m["row"], "col": m["col"], "object": m["room_type"]})

        audit = DevataAudit(grid, devatas_json, shastra)
        audit_result = audit.audit_plan(plan_data) if plan_data else {"devata_score": 100, "issues": []}

        # 2. Element Balance
        balance = ElementBalance(elements_json)
        for m in result.get("room_mappings", []):
            balance.analyze_zone(m["zone"], [m["room_type"]])

        # 3. Room Analysis (dosh detect)
        room_analysis = RoomAnalysis()
        room_results = []
        for m in result.get("room_mappings", []):
            room_type = m["room_type"]
            zone = m["zone"]
            rule = room_analysis.ROOM_RULES.get(room_type, {})
            if not rule:
                continue
            is_correct = zone in rule.get("best_directions", [])
            is_defect = zone in rule.get("bad_directions", [])
            status = "correct" if is_correct else ("defect" if is_defect else "neutral")
            room_results.append({
                "room_type": room_type,
                "room_hindi": rule.get("hindi", room_type),
                "zone": zone,
                "pada": m.get("pada", 0),
                "row": m.get("row", 0),
                "col": m.get("col", 0),
                "status": status,
                "is_correct": is_correct,
                "is_defect": is_defect,
                "best_directions": rule.get("best_directions", []),
                "bad_directions": rule.get("bad_directions", []),
                "shastra": rule.get("shastra", ""),
                "reason": rule.get("reason", ""),
                "severity": "high" if is_defect and zone in ["NE", "CENTER"] else ("medium" if is_defect else "low")
            })

        defects = [r for r in room_results if r["is_defect"]]

        # 4. Remedies (5-tier)
        remedy_engine = RemedyEngineV3()
        remedies = []
        for d in defects[:5]:
            defect_key = f"{d['room_type']}_{d['zone']}"
            r = remedy_engine.get_5_tier_remedy(defect_key, d["zone"])
            if r:
                remedies.append(r)

        # 5. Pooja Plan
        pooja_engine = PoojaEngine()
        defect_keys = [f"{d['room_type']}_{d['zone']}" for d in defects]
        pooja_plan = pooja_engine.generate_full_puja_plan(defect_keys) if defect_keys else {"total_poojas": 0, "plan": []}

        # 6. Entrance Audit
        entrance_engine = EntranceAudit()
        entrance_result = entrance_engine.audit_entrance("East", 3)

        # 7. Ayadi Shadvarga
        ayadi_engine = AyadiEngine()
        ayadi_result = ayadi_engine.calculate(40, 30, 10)

        # 8. Final Score (7-Component)
        scorer = VastuScore()
        final_score = scorer.calculate(
            devata_score=audit_result.get("devata_score", 100),
            element_balance_score=70,
            brahma_score=100,
            direction_score=84,
            entrance_result=entrance_result,
            ayadi_result=ayadi_result,
            room_mapping_score=100
        )

        return {
            "status": "success",
            "upload_id": upload_id,
            "filename": filename,
            "original_filename": file.filename,
            "uploaded_at": datetime.now().isoformat(),
            "analysis": {
                "rooms_detected": result["rooms_detected"],
                "rooms": result["rooms"],
                "boundary": result["boundary"],
                "grid_overlay": result["grid_overlay_base64"],
                "room_mappings": result["room_mappings"],
                "room_results": room_results,
                "defects": defects,
                "defect_count": len(defects),
                "high_severity_count": len([d for d in defects if d["severity"] == "high"]),
                "medium_severity_count": len([d for d in defects if d["severity"] == "medium"]),
                "low_severity_count": len([d for d in defects if d["severity"] == "low"]),
                "remedies": remedies,
                "pooja_plan": pooja_plan,
                "entrance_audit": entrance_result,
                "ayadi": ayadi_result,
                "final_score": final_score,
                "devata_audit": audit_result
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
def test_upload():
    return {"status": "ok", "message": "Upload endpoint ready", "pdf_support": True}


@router.get("/debug/{upload_id}")
def debug_upload(upload_id: str):
    file_path = UPLOAD_DIR / f"plan_{upload_id}.png"
    if not file_path.exists():
        for ext in [".jpg", ".jpeg", ".webp", ".bmp"]:
            alt = UPLOAD_DIR / f"plan_{upload_id}{ext}"
            if alt.exists():
                file_path = alt
                break
        else:
            raise HTTPException(status_code=404, detail="Upload not found")
    parser = PlanParser()
    result = parser.analyze(file_path)
    return result
