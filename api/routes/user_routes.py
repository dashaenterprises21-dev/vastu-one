"""
Vastu One - User Routes
Profile, Reports history, Account settings
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from database.models import User, Report
from database.schemas import (
    UserResponse, ProfileUpdate, PasswordChange, MessageResponse
)
from api.auth import get_current_user, hash_password, verify_password

router = APIRouter(prefix="/api/user", tags=["User"])


@router.get("/profile", response_model=UserResponse)
def get_profile(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


@router.put("/profile", response_model=UserResponse)
def update_profile(
    data: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.name is not None:
        user.name = data.name.strip()
    if data.phone is not None:
        # Check phone uniqueness
        existing = db.query(User).filter(
            User.phone == data.phone, User.id != user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="फ़ोन नंबर पहले से registered है")
        user.phone = data.phone
    if data.city is not None:
        user.city = data.city
    if data.state is not None:
        user.state = data.state
    if data.profile_image is not None:
        user.profile_image = data.profile_image

    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.post("/change-password", response_model=MessageResponse)
def change_password(
    data: PasswordChange,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="पुराना password गलत है")

    user.password_hash = hash_password(data.new_password)
    db.commit()

    return MessageResponse(message="Password बदल गया")


@router.get("/reports")
def get_my_reports(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reports = db.query(Report).filter(Report.user_id == user.id).order_by(
        Report.created_at.desc()
    ).all()

    return {
        "total": len(reports),
        "reports": [
            {
                "report_id": r.report_id,
                "package": r.package,
                "price": r.price,
                "payment_status": r.payment_status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "view_url": f"/report/{r.report_id}",
            }
            for r in reports
        ],
    }


@router.delete("/account", response_model=MessageResponse)
def delete_account(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """DPDP compliance — user can delete account"""
    user.is_active = False
    db.commit()
    return MessageResponse(message="Account delete हो गया")