"""
Vastu One - Plan Upload Routes
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid
from datetime import datetime

from engine.vision.plan_parser import PlanParser

router = APIRouter(prefix="/api/upload", tags=["Upload"])

BASE = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE / "uploads" / "plans"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/plan")
async def upload_plan(file: UploadFile = File(...)):
    """
    Plan image upload करो और AI analysis करो
    """
    try:
        # Validate extension
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files allowed"
            )

        # Read file
        contents = await file.read()

        # Validate size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 10 MB)")

        # Save file
        upload_id = uuid.uuid4().hex[:12]
        filename = f"plan_{upload_id}{ext}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(contents)

        # AI Analysis
        parser = PlanParser()
        result = parser.analyze(file_path)

        return {
            "status": "success",
            "upload_id": upload_id,
            "filename": filename,
            "file_path": str(file_path),
            "uploaded_at": datetime.now().isoformat(),
            "analysis": {
                "rooms_detected": result["rooms_detected"],
                "rooms": result["rooms"],
                "boundary": result["boundary"],
                "grid_overlay": result["grid_overlay_base64"],
                "room_mappings": result["room_mappings"]
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
    """Test endpoint"""
    return {
        "status": "ok",
        "message": "Upload endpoint ready",
        "upload_dir": str(UPLOAD_DIR)
    }

@router.get("/debug/{upload_id}")
def debug_upload(upload_id: str):
    """Debug — show all YOLO detections for an uploaded plan"""
    file_path = UPLOAD_DIR / f"plan_{upload_id}.png"
    if not file_path.exists():
        # Try other extensions
        for ext in [".jpg", ".jpeg", ".webp", ".bmp"]:
            alt = UPLOAD_DIR / f"plan_{upload_id}{ext}"
            if alt.exists():
                file_path = alt
                break
        else:
            raise HTTPException(status_code=404, detail="Upload not found")

    parser = PlanParser()
    result = parser.analyze(file_path)

    return {
        "upload_id": upload_id,
        "yolo_available": result["yolo_available"],
        "total_detections": result["total_detections"],
        "all_detections": result["detections"],  # ALL 18
        "rooms_after_grouping": result["rooms_detected"],
        "rooms": result["rooms"],
        "mappings": result["room_mappings"],
    }