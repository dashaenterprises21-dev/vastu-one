"""
Vastu One - Payment Routes (Razorpay)
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import razorpay
import hmac
import hashlib

from database.db import get_db
from database.models import User, Report
from api.auth import get_current_user, get_optional_user
from api.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

router = APIRouter(prefix="/api/payment", tags=["Payment"])

# ═══ PACKAGES ═══
PACKAGES = {
    "bronze": {"name": "Bronze Report", "price": 999},
    "silver": {"name": "Silver Report", "price": 2999},
    "gold": {"name": "Gold Report", "price": 9999},
    "platinum": {"name": "Platinum Report", "price": 24999},
}


# ═══ RAZORPAY CLIENT ═══
def get_razorpay_client():
    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise HTTPException(status_code=500, detail="Razorpay keys not configured")
    return razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# ═══ REQUEST MODELS ═══
class CreateOrderRequest(BaseModel):
    package: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    package: str


# ═══ CREATE ORDER ═══
@router.post("/create-order")
def create_order(
    data: CreateOrderRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a Razorpay order"""

    if data.package not in PACKAGES:
        raise HTTPException(status_code=400, detail="Invalid package")

    pkg = PACKAGES[data.package]
    amount_paise = pkg["price"] * 100  # Razorpay uses paise

    try:
        client = get_razorpay_client()

        # Create Razorpay order
        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"vastu_{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "notes": {
                "user_id": str(user.id),
                "user_email": user.email,
                "package": data.package,
                "package_name": pkg["name"],
            },
        }

        order = client.order.create(data=order_data)

        # Save report entry with pending status
        report_id = f"VAI-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        report = Report(
            user_id=user.id,
            report_id=report_id,
            package=data.package,
            price=pkg["price"],
            payment_status="pending",
            payment_id=order["id"],
        )
        db.add(report)
        db.commit()

        return {
            "status": "success",
            "order_id": order["id"],
            "amount": amount_paise,
            "currency": "INR",
            "package": data.package,
            "package_name": pkg["name"],
            "report_id": report_id,
            "key_id": RAZORPAY_KEY_ID,
            "user": {
                "name": user.name,
                "email": user.email,
                "phone": user.phone or "",
            },
        }

    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ═══ VERIFY PAYMENT ═══
@router.post("/verify")
def verify_payment(
    data: VerifyPaymentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Verify Razorpay payment signature"""

    if data.package not in PACKAGES:
        raise HTTPException(status_code=400, detail="Invalid package")

    try:
        # Verify signature
        message = f"{data.razorpay_order_id}|{data.razorpay_payment_id}"
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

        if generated_signature != data.razorpay_signature:
            # Payment verification failed
            report = db.query(Report).filter(
                Report.payment_id == data.razorpay_order_id,
                Report.user_id == user.id,
            ).first()
            if report:
                report.payment_status = "failed"
                db.commit()
            raise HTTPException(status_code=400, detail="Payment verification failed")

        # Payment verified — update report
        report = db.query(Report).filter(
            Report.payment_id == data.razorpay_order_id,
            Report.user_id == user.id,
        ).first()

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        report.payment_status = "paid"
        report.payment_id = data.razorpay_payment_id
        report.expires_at = datetime.now(timezone.utc) + timedelta(days=365)
        db.commit()
        db.refresh(report)
                
        # 📧 Send payment success email
        try:
            from engine.notifications import NotificationService
            ns = NotificationService()
            ns.send_payment_success(
                user_email=user.email,
                user_name=user.name,
                user_phone=user.phone or "",
                report_id=report.report_id,
                package=report.package or data.package,
                amount=report.price,
            )
        except Exception as e:
            print(f"[WARNING] Email notification failed: {e}")

        return {
            "status": "success",
            "message": "Payment verified",
            "report_id": report.report_id,
            "package": report.package,
            "amount": report.price,
            "view_url": f"/report/{report.report_id}",
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ═══ GET MY PAYMENTS ═══
@router.get("/history")
def payment_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get payment history for current user"""
    reports = db.query(Report).filter(
        Report.user_id == user.id,
        Report.payment_status.in_(["paid", "pending", "failed"]),
    ).order_by(Report.created_at.desc()).all()

    return {
        "total": len(reports),
        "payments": [
            {
                "report_id": r.report_id,
                "package": r.package,
                "price": r.price,
                "status": r.payment_status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in reports
        ],
    }


# ═══ GET PACKAGES ═══
@router.get("/packages")
def get_packages():
    """List all available packages"""
    return {"packages": [
        {"id": k, "name": v["name"], "price": v["price"]}
        for k, v in PACKAGES.items()
    ]}