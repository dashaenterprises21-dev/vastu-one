"""
Vastu One - Plan Analysis API
Groq + Vastu Engine + Report Generation
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from datetime import datetime
import shutil
import uuid
from pathlib import Path

from api.auth import get_current_user, get_optional_user
from database.db import get_db
from database.models import User, Report
from engine.vision.groq_plan_reader import GroqPlanReader
from engine.vastu_analyzer import VastuAnalyzer

router = APIRouter(prefix="/api/plan", tags=["Plan Analysis"])

BASE = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE / "uploads" / "plans"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/analyze")
async def analyze_plan_image(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: "Session" = Depends(get_db),
):
    """Complete plan analysis: Groq + Vastu Engine"""

    try:
        # Save uploaded file
        ext = Path(file.filename).suffix.lower()
        if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
            raise HTTPException(status_code=400, detail="Only PNG/JPG/JPEG/WEBP allowed")

        file_id = uuid.uuid4().hex[:12]
        file_path = UPLOAD_DIR / f"plan_{file_id}{ext}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[INFO] Plan uploaded: {file_path}")

        # 1. Groq — extract rooms
        print("[INFO] Sending to Groq for room detection...")
        groq_reader = GroqPlanReader()
        plan_data = groq_reader.analyze_plan(str(file_path))

        print(f"[INFO] Groq detected {len(plan_data.get('rooms', []))} rooms")

        # 2. Vastu Engine — analyze
        print("[INFO] Running Vastu analysis...")
        analyzer = VastuAnalyzer()
        analysis = analyzer.analyze_plan(plan_data)

        # 3. Save to database
        report_id = f"VAI-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        report = Report(
            user_id=user.id,
            report_id=report_id,
            package="plan_analysis",
            price=0,
            payment_status="paid",
            plan_data=plan_data,
            analysis_data=analysis,
        )
        db.add(report)
        db.commit()

                
        # 📧 Send report ready email
        try:
            from engine.notifications import NotificationService
            ns = NotificationService()
            ns.send_report_ready(
                user_email=user.email,
                user_name=user.name,
                user_phone=user.phone or "",
                report_id=report_id,
                score=analysis["overall_score"],
                grade=analysis["grade"],
                defects=analysis["defects"],
            )
        except Exception as e:
            print(f"[WARNING] Email notification failed: {e}")

        print(f"[INFO] Report saved: {report_id}")

        return {
            "status": "success",
            "report_id": report_id,
            "view_url": f"/plan-report/{report_id}",
            "summary": {
                "total_rooms": analysis["total_rooms"],
                "correct": analysis["correct_rooms"],
                "defects": analysis["defects"],
                "severe": analysis["severe_defects"],
                "score": analysis["overall_score"],
                "grade": analysis["grade"],
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{report_id}")
def get_plan_report(
    report_id: str,
    user: User = Depends(get_current_user),
    db: "Session" = Depends(get_db),
):
    """Get saved plan report"""
    report = db.query(Report).filter(
        Report.report_id == report_id,
        Report.user_id == user.id,
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "report_id": report.report_id,
        "created_at": report.created_at.isoformat() if report.created_at else None,
        "plan_data": report.plan_data,
        "analysis": report.analysis_data,
    }