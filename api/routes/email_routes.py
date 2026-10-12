"""
VASTU ONE — Email Routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from engine.services.email_service import (
    send_kundli_email, send_payment_email, send_otp_email, send_invoice_email
)

router = APIRouter(prefix="/api/email", tags=["email"])


class SendKundliReq(BaseModel):
    to: str
    name: str
    report_url: Optional[str] = ""


class SendPaymentReq(BaseModel):
    to: str
    name: str
    amount: float
    payment_id: str


class SendOTPReq(BaseModel):
    to: str
    otp: str


class SendInvoiceReq(BaseModel):
    to: str
    name: str
    order_data: dict


@router.post("/send-kundli")
async def send_kundli(req: SendKundliReq):
    """Send kundli report email"""
    result = send_kundli_email(req.to, req.name, None, req.report_url)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result


@router.post("/send-payment")
async def send_payment(req: SendPaymentReq):
    """Send payment confirmation email"""
    result = send_payment_email(req.to, req.name, req.amount, req.payment_id)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result


@router.post("/send-otp")
async def send_otp(req: SendOTPReq):
    """Send OTP email"""
    result = send_otp_email(req.to, req.otp)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result


@router.post("/send-invoice")
async def send_invoice(req: SendInvoiceReq):
    """Send invoice email"""
    result = send_invoice_email(req.to, req.name, req.order_data)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result


@router.get("/status")
async def status():
    """Check email service status"""
    from engine.services.email_service import email_service
    return {
        "configured": bool(email_service.user and email_service.password),
        "from_email": email_service.from_email,
        "host": email_service.host,
    }
