"""
VASTU ONE — Payment Link Generator
Create shareable payment links
"""

from typing import Dict, Any
import uuid
from datetime import datetime, timedelta


class PaymentLinkEngine:
    def create_link(self, amount: float, description: str, customer: Dict = None, expire_hours: int = 24) -> Dict:
        """Create a payment link"""
        link_id = "plink_" + uuid.uuid4().hex[:12]
        return {
            "id": link_id,
            "amount": amount * 100,  # paise
            "currency": "INR",
            "description": description,
            "customer": customer or {},
            "short_url": f"https://rzp.io/l/{link_id}",
            "expire_by": (datetime.now() + timedelta(hours=expire_hours)).isoformat(),
            "status": "created",
            "created_at": datetime.now().isoformat(),
        }

    def create_kundli_link(self, kundli_id: str, amount: float = 99) -> Dict:
        return self.create_link(amount, f"Kundli Report #{kundli_id}")

    def create_consultation_link(self, astrologer_id: str, amount: float = 500) -> Dict:
        return self.create_link(amount, f"Consultation with Astrologer #{astrologer_id}")


def create_payment_link(amount, description, customer=None):
    return PaymentLinkEngine().create_link(amount, description, customer)
