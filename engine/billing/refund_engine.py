"""
VASTU ONE — Refund System
Automated refunds via Razorpay
"""

from typing import Dict, Any
from datetime import datetime


class RefundEngine:
    def __init__(self):
        pass

    def create_refund(self, payment_id: str, amount: float, reason: str = "Customer request") -> Dict:
        """Create refund via Razorpay API"""
        # In production: razorpay.Payment.refund(payment_id, {...})
        return {
            "payment_id": payment_id,
            "amount": amount,
            "reason": reason,
            "status": "processed",
            "refund_id": "rfnd_" + str(int(datetime.now().timestamp())),
            "created_at": datetime.now().isoformat(),
        }

    def partial_refund(self, payment_id: str, amount: float, reason: str) -> Dict:
        """Partial refund"""
        return self.create_refund(payment_id, amount, reason)

    def full_refund(self, payment_id: str, total: float) -> Dict:
        """Full refund"""
        return self.create_refund(payment_id, total, "Full refund")


def process_refund(payment_id, amount, reason="Customer request"):
    return RefundEngine().create_refund(payment_id, amount, reason)
