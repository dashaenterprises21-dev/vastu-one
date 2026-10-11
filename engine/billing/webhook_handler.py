"""
VASTU ONE — Razorpay Webhook Handler
Verify signatures + process events
"""

import hmac
import hashlib
import os
from typing import Dict, Any


class WebhookHandler:
    def __init__(self):
        self.webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")

    def verify_signature(self, body: bytes, signature: str) -> bool:
        """Verify Razorpay webhook signature"""
        if not self.webhook_secret:
            return False
        expected = hmac.new(
            self.webhook_secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def process_event(self, event: Dict) -> Dict:
        """Process webhook event"""
        event_type = event.get("event", "")
        payload = event.get("payload", {})

        if event_type == "payment.captured":
            return self._handle_payment_captured(payload)
        elif event_type == "payment.failed":
            return self._handle_payment_failed(payload)
        elif event_type == "refund.processed":
            return self._handle_refund(payload)
        elif event_type == "subscription.activated":
            return self._handle_subscription(payload)
        else:
            return {"status": "ignored", "event": event_type}

    def _handle_payment_captured(self, payload):
        payment = payload.get("payment", {}).get("entity", {})
        return {
            "status": "success",
            "action": "mark_order_paid",
            "order_id": payment.get("order_id"),
            "payment_id": payment.get("id"),
            "amount": payment.get("amount"),
        }

    def _handle_payment_failed(self, payload):
        payment = payload.get("payment", {}).get("entity", {})
        return {
            "status": "failed",
            "action": "mark_order_failed",
            "order_id": payment.get("order_id"),
        }

    def _handle_refund(self, payload):
        refund = payload.get("refund", {}).get("entity", {})
        return {
            "status": "refunded",
            "action": "mark_order_refunded",
            "refund_id": refund.get("id"),
            "payment_id": refund.get("payment_id"),
        }

    def _handle_subscription(self, payload):
        sub = payload.get("subscription", {}).get("entity", {})
        return {
            "status": "active",
            "action": "activate_subscription",
            "subscription_id": sub.get("id"),
        }


def verify_webhook(body, signature):
    return WebhookHandler().verify_signature(body, signature)


def process_webhook_event(event):
    return WebhookHandler().process_event(event)
