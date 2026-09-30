"""
Vastu One - Chakra Analysis Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import json

from api.auth import get_current_user
from database.db import get_db
from database.models import User, Report
from engine.chakra_analyzer import ChakraAnalyzer

router = APIRouter(prefix="/api/chakra", tags=["Chakra Analysis"])


class RoomItem(BaseModel):
    pada: int
    row: int
    col: int
    zone: str
    type: str
    size: Optional[str] = "medium"
    note: Optional[str] = ""


class AnalyzeRequest(BaseModel):
    rooms: List[RoomItem]
    property_type: Optional[str] = "house"
    floor: Optional[str] = "ground"
    plot_shape: Optional[str] = "square"
    plot_length: Optional[float] = None
    plot_width: Optional[float] = None


@router.post("/analyze")
def analyze_chakra(
    data: AnalyzeRequest,
    user: User = Depends(get_current_user),
    db: "Session" = Depends(get_db),
):
    """Complete Vastu analysis of rooms placed on chakra"""

    if not data.rooms:
        raise HTTPException(status_code=400, detail="कम से कम एक room रखें")

    try:
        analyzer = ChakraAnalyzer()
        result = analyzer.analyze(
            rooms=[r.dict() for r in data.rooms],
            property_type=data.property_type,
            floor=data.floor,
            plot_shape=data.plot_shape,
        )

        # Generate report ID
        report_id = f"VAI-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Save to database
        report = Report(
            user_id=user.id,
            report_id=report_id,
            package="chakra",
            price=0,
            payment_status="paid",
            plan_data={
                "rooms": [r.dict() for r in data.rooms],
                "property_type": data.property_type,
                "floor": data.floor,
                "plot_shape": data.plot_shape,
                "plot_length": data.plot_length,
                "plot_width": data.plot_width,
            },
            analysis_data=result,
        )
        db.add(report)
        db.commit()

        return {
            "status": "success",
            "report_id": report_id,
            "view_url": f"/chakra-report/{report_id}",
            "summary": {
                "total_rooms": result["total_rooms"],
                "correct": result["correct_rooms"],
                "defects": result["defects"],
                "severe": result["severe_defects"],
                "score": result["overall_score"],
                "grade": result["grade"],
            },
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{report_id}")
def get_chakra_report(
    report_id: str,
    user: User = Depends(get_current_user),
    db: "Session" = Depends(get_db),
):
    """Get saved chakra report"""
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