"""
VASTU ONE — Complete Razorpay Routes
All payment endpoints
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import Optional, List
import os
import razorpay
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_db
from engine.report.invoice_generator import generate_invoice
from engine.billing.subscription_engine import SubscriptionEngine
from engine.billing.refund_engine import RefundEngine
from engine.billing.webhook_handler import WebhookHandler
from engine.billing.payment_link_engine import PaymentLinkEngine

router = APIRouter(prefix="/api/payments", tags=["payments"])

# Razorpay client
RAZORPAY_KEY = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))


# ═══ MODELS ═══
class CreateOrderReq(BaseModel):
    amount: float
    currency: str = "INR"
    description: Optional[str] = "Order"
    customer_id: Optional[str] = None
    items: Optional[List[dict]] = None


class VerifyPaymentReq(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class RefundReq(BaseModel):
    payment_id: str
    amount: float
    reason: Optional[str] = "Customer request"


class SubscriptionReq(BaseModel):
    plan_id: str
    customer_id: str


# ═══ ORDER CREATE ═══
@router.post("/create-order")
async def create_order(req: CreateOrderReq):
    try:
        order_data = {
            "amount": int(req.amount * 100),  # paise
            "currency": req.currency,
            "receipt": f"rcpt_{os.urandom(4).hex()}",
            "notes": {"description": req.description},
        }
        order = client.order.create(data=order_data)
        return {"success": True, "order": order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══ VERIFY PAYMENT ═══
@router.post("/verify")
async def verify_payment(req: VerifyPaymentReq):
    try:
        params = {
            "razorpay_order_id": req.razorpay_order_id,
            "razorpay_payment_id": req.razorpay_payment_id,
            "razorpay_signature": req.razorpay_signature,
        }
        client.utility.verify_payment_signature(params)
        return {"success": True, "message": "Payment verified"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid signature")


# ═══ INVOICE ═══
@router.post("/invoice")
async def create_invoice(order: dict):
    html = generate_invoice(order)
    return {"success": True, "html": html}


# ═══ SUBSCRIPTION ═══
@router.get("/plans")
async def get_plans():
    return {"plans": SubscriptionEngine().get_plans()}


@router.post("/subscribe")
async def create_subscription(req: SubscriptionReq):
    result = SubscriptionEngine().create_subscription(req.plan_id, req.customer_id)
    return result


# ═══ REFUND ═══
@router.post("/refund")
async def refund(req: RefundReq):
    result = RefundEngine().create_refund(req.payment_id, req.amount, req.reason)
    return result


# ═══ WEBHOOK ═══
@router.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")
    handler = WebhookHandler()
    if not handler.verify_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    event = await request.json()
    result = handler.process_event(event)
    return result


# ═══ PAYMENT LINK ═══
@router.post("/payment-link")
async def create_payment_link(amount: float, description: str):
    result = PaymentLinkEngine().create_link(amount, description)
    return result


# ═══ KUNDLI PAYMENT ═══
@router.post("/kundli-payment")
async def kundli_payment(kundli_id: str, amount: float = 99):
    try:
        order_data = {
            "amount": int(amount * 100),
            "currency": "INR",
            "receipt": f"kundli_{kundli_id}",
            "notes": {"kundli_id": kundli_id, "type": "kundli_premium"},
        }
        order = client.order.create(data=order_data)
        return {"success": True, "order": order, "kundli_id": kundli_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══ CONSULTATION PAYMENT ═══
@router.post("/consultation-payment")
async def consultation_payment(astrologer_id: str, amount: float = 500, slot: str = ""):
    try:
        order_data = {
            "amount": int(amount * 100),
            "currency": "INR",
            "receipt": f"consult_{astrologer_id}",
            "notes": {"astrologer_id": astrologer_id, "slot": slot, "type": "consultation"},
        }
        order = client.order.create(data=order_data)
        return {"success": True, "order": order, "astrologer_id": astrologer_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
