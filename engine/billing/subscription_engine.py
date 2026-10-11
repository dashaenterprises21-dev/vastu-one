"""
VASTU ONE — Subscription Plans (Razorpay)
Monthly/Yearly plans with auto-renewal
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta


class SubscriptionEngine:
    PLANS = {
        "basic": {
            "name": "Basic",
            "price": 299,
            "period": "monthly",
            "features": [
                "5 Kundli reports/month",
                "Basic charts",
                "PDF download",
                "Email support",
            ],
            "razorpay_plan_id": "plan_basic_monthly",
        },
        "pro": {
            "name": "Pro",
            "price": 999,
            "period": "monthly",
            "features": [
                "Unlimited kundli reports",
                "All 50+ charts",
                "PDF + Excel export",
                "Priority support",
                "Consultation 1/month",
            ],
            "razorpay_plan_id": "plan_pro_monthly",
        },
        "enterprise": {
            "name": "Enterprise",
            "price": 4999,
            "period": "monthly",
            "features": [
                "Everything in Pro",
                "Multi-user access",
                "White-label PDF",
                "API access",
                "Dedicated support",
                "Consultation 4/month",
            ],
            "razorpay_plan_id": "plan_enterprise_monthly",
        },
    }

    def __init__(self, user: Dict = None):
        self.user = user or {}

    def get_plans(self) -> List[Dict]:
        return [{"id": k, **v} for k, v in self.PLANS.items()]

    def get_plan(self, plan_id: str) -> Dict:
        return self.PLANS.get(plan_id, {})

    def create_subscription(self, plan_id: str, customer_id: str) -> Dict:
        """Create Razorpay subscription"""
        plan = self.get_plan(plan_id)
        if not plan:
            return {"error": "Invalid plan"}

        return {
            "plan_id": plan["razorpay_plan_id"],
            "customer_id": customer_id,
            "status": "created",
            "amount": plan["price"] * 100,
            "currency": "INR",
        }

    def calculate_proration(self, old_plan: str, new_plan: str, days_used: int) -> Dict:
        old_price = self.get_plan(old_plan).get("price", 0)
        new_price = self.get_plan(new_plan).get("price", 0)
        daily_old = old_price / 30
        daily_new = new_price / 30
        refund = daily_old * (30 - days_used)
        charge = daily_new * (30 - days_used)
        return {
            "refund": round(refund, 2),
            "charge": round(charge, 2),
            "net": round(charge - refund, 2),
        }


def get_subscription_plans():
    return SubscriptionEngine().get_plans()
