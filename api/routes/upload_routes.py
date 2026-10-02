"""
Vastu One - Plan Upload Routes
Supports: PNG, JPG, JPEG, WEBP, BMP, PDF
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from datetime import datetime

from engine.vision.plan_parser import PlanParser

router = APIRouter(prefix="/api/upload", tags=["Upload"])

BASE = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE / "uploads" / "plans"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def pdf_to_image(pdf_path: Path, output_path: Path) -> bool:
    """
    Convert first page of PDF to PNG image using PyMuPDF.
    Returns True if successful.
    """
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(pdf_path))
        if len(doc) == 0:
            doc.close()
            return False
        page = doc[0]
        # Render at high DPI (2x zoom = ~150 DPI)
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(str(output_path))
        doc.close()
        print(f"[INFO] PDF converted: {pdf_path.name} -> {output_path.name} ({pix.width}x{pix.height})")
        return True
    except Exception as e:
        print(f"[ERROR] PDF conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


@router.post("/plan")
async def upload_plan(file: UploadFile = File(...)):
    """
    Plan upload - image (PNG, JPG) ya PDF - AI analysis
    """
    try:
        # Validate extension
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Only {', '.join(sorted(ALLOWED_EXTENSIONS))} files allowed"
            )

        # Read file
        contents = await file.read()

        # Validate size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 10 MB)")

        upload_id = uuid.uuid4().hex[:12]

        if ext == ".pdf":
            # Save PDF temporarily
            pdf_filename = f"plan_{upload_id}.pdf"
            pdf_path = UPLOAD_DIR / pdf_filename
            with open(pdf_path, "wb") as f:
                f.write(contents)

            # Convert PDF to PNG
            png_filename = f"plan_{upload_id}.png"
            png_path = UPLOAD_DIR / png_filename

            if not pdf_to_image(pdf_path, png_path):
                raise HTTPException(
                    status_code=400,
                    detail="PDF conversion failed - file corrupt ya empty hai"
                )

            # Delete original PDF
            try:
                pdf_path.unlink()
            except Exception:
                pass

            file_path = png_path
            filename = png_filename

        else:
            # Regular image
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
            "original_filename": file.filename,
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
        "upload_dir": str(UPLOAD_DIR),
        "allowed_extensions": sorted(ALLOWED_EXTENSIONS),
        "pdf_support": True
    }


@router.get("/debug/{upload_id}")
def debug_upload(upload_id: str):
    """Debug - show all YOLO detections for an uploaded plan"""
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

    return {
        "upload_id": upload_id,
        "yolo_available": result["yolo_available"],
        "total_detections": result["total_detections"],
        "all_detections": result["detections"],
        "rooms_after_grouping": result["rooms_detected"],
        "rooms": result["rooms"],
        "mappings": result["room_mappings"],
    }
