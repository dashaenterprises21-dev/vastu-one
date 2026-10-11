"""
VASTU ONE — Invoice Generator
Auto-generate PDF invoices for orders
"""

from datetime import datetime
from typing import Dict, Any
import uuid


class InvoiceGenerator:
    """Generate HTML/PDF invoices"""

    def generate_html(self, order: Dict) -> str:
        order_id = order.get("id", "")
        customer = order.get("customer", {})
        items = order.get("items", [])
        total = order.get("total", 0)
        date = order.get("created_at", datetime.now().isoformat())
        razorpay_id = order.get("razorpay_payment_id", "")

        html = '<div style="max-width:800px;margin:0 auto;padding:40px;background:#fdfaf3;font-family:Georgia,serif;color:#1f1b18;">'
        html += '<div style="border-bottom:3px double #b8860b;padding-bottom:20px;margin-bottom:30px;">'
        html += '<div style="display:flex;justify-content:space-between;align-items:center;">'
        html += '<div><h1 style="font-family:Georgia,serif;font-size:32px;color:#6b1420;margin:0;">VASTU ONE</h1>'
        html += '<div style="font-size:12px;color:#8a7563;letter-spacing:0.2em;margin-top:4px;">TAX INVOICE</div></div>'
        html += '<div style="text-align:right;font-size:12px;color:#5c4433;">'
        html += '<div><strong>Invoice #:</strong> INV-' + str(order_id)[:8].upper() + '</div>'
        html += '<div><strong>Date:</strong> ' + str(date)[:10] + '</div>'
        html += '</div></div></div>'

        html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:30px;">'
        html += '<div><div style="font-size:11px;color:#b8860b;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px;">Bill To</div>'
        html += '<div style="font-size:14px;line-height:1.7;">'
        html += '<div><strong>' + (customer.get("name", "Customer")) + '</strong></div>'
        html += '<div>' + (customer.get("email", "")) + '</div>'
        html += '<div>' + (customer.get("phone", "")) + '</div>'
        html += '</div></div>'
        html += '<div><div style="font-size:11px;color:#b8860b;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px;">Payment Details</div>'
        html += '<div style="font-size:13px;line-height:1.7;">'
        html += '<div><strong>Method:</strong> Razorpay</div>'
        html += '<div><strong>Payment ID:</strong> ' + razorpay_id + '</div>'
        html += '</div></div></div>'

        # Items table
        html += '<table style="width:100%;border-collapse:collapse;margin-bottom:30px;">'
        html += '<thead><tr style="background:#6b1420;color:#f5ede0;">'
        html += '<th style="padding:12px;text-align:left;font-size:12px;letter-spacing:0.1em;">Item</th>'
        html += '<th style="padding:12px;text-align:center;font-size:12px;">Qty</th>'
        html += '<th style="padding:12px;text-align:right;font-size:12px;">Price</th>'
        html += '<th style="padding:12px;text-align:right;font-size:12px;">Total</th>'
        html += '</tr></thead><tbody>'

        for item in items:
            price = item.get("price", 0)
            qty = item.get("quantity", 1)
            html += '<tr style="border-bottom:1px solid #e5d8c5;">'
            html += '<td style="padding:12px;font-size:14px;">' + item.get("name", "Item") + '</td>'
            html += '<td style="padding:12px;text-align:center;font-size:14px;">' + str(qty) + '</td>'
            html += '<td style="padding:12px;text-align:right;font-size:14px;">' + str(price) + '</td>'
            html += '<td style="padding:12px;text-align:right;font-size:14px;">' + str(price * qty) + '</td>'
            html += '</tr>'

        html += '</tbody></table>'

        # Total
        html += '<div style="text-align:right;margin-bottom:30px;">'
        html += '<div style="font-size:14px;color:#5c4433;margin-bottom:6px;">Subtotal: ' + str(total) + '</div>'
        html += '<div style="font-size:14px;color:#5c4433;margin-bottom:6px;">GST (18%): ' + str(round(total * 0.18, 2)) + '</div>'
        html += '<div style="font-size:22px;color:#6b1420;font-weight:700;border-top:2px solid #b8860b;padding-top:10px;margin-top:10px;">Grand Total: ' + str(round(total * 1.18, 2)) + '</div>'
        html += '</div>'

        html += '<div style="border-top:1px solid #e5d8c5;padding-top:20px;text-align:center;font-size:12px;color:#8a7563;">'
        html += '<div>Thank you for your business!</div>'
        html += '<div style="margin-top:6px;">Vastu One · Made with care in India</div>'
        html += '</div></div>'

        return html


def generate_invoice(order: Dict) -> str:
    return InvoiceGenerator().generate_html(order)
