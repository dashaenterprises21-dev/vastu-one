"""
Vastu One - Notifications
Email automatic notifications
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").replace(" ", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "VASTU ONE")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USER)


class NotificationService:

    def send_email(self, to_email: str, subject: str, html_body: str) -> bool:
        if not SMTP_USER or not SMTP_PASSWORD:
            print("[WARNING] Email not configured")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
            msg["To"] = to_email

            msg.attach(MIMEText(html_body, "html", "utf-8"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_FROM_EMAIL, to_email, msg.as_string())

            print(f"[INFO] Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"[ERROR] Email failed: {e}")
            return False

    def send_payment_success(self, user_email, user_name, user_phone, report_id, package, amount):
        subject = f"✅ Payment Successful — VASTU ONE"
        body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; background: #f9fafb; padding: 40px 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <div style="background: linear-gradient(135deg, #fbbf24, #d97706); padding: 32px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">🕉️ VASTU ONE</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0; font-size: 14px;">India Ka No.1 Vastu Engine</p>
                </div>
                <div style="padding: 40px 32px;">
                    <h2 style="color: #0f1419; margin: 0 0 16px;">नमस्ते {user_name} 🙏</h2>
                    <p style="color: #4b5563; font-size: 16px;">आपका payment <b style="color: #10b981;">successfully received</b> हो गया है।</p>
                    <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px; border-radius: 8px; margin: 24px 0;">
                        <p style="margin: 0; color: #92400e;"><b>Report ID:</b> {report_id}</p>
                        <p style="margin: 8px 0 0; color: #92400e;"><b>Package:</b> {package.upper()}</p>
                        <p style="margin: 8px 0 0; color: #92400e;"><b>Amount:</b> ₹{amount:,}</p>
                    </div>
                    <p style="color: #4b5563;">अब अपना floor plan upload करें — AI complete वास्तु विश्लेषण करेगा।</p>
                    <div style="text-align: center; margin: 32px 0;">
                        <a href="http://127.0.0.1:8000/plan-upload" style="display: inline-block; background: linear-gradient(135deg, #fbbf24, #d97706); color: white; padding: 14px 32px; text-decoration: none; border-radius: 10px; font-weight: 700;">
                            📤 अब Plan Upload करें
                        </a>
                    </div>
                </div>
                <div style="background: #f9fafb; padding: 24px; text-align: center; font-size: 12px; color: #6b7280;">
                    <p>बृहत्संहिता • समरांगण सूत्रधार • मयमतम् • मानसार</p>
                    <p>© 2026 VASTU ONE</p>
                </div>
            </div>
        </body>
        </html>
        """
        return {"email_sent": self.send_email(user_email, subject, body), "whatsapp_sent": False}

    def send_report_ready(self, user_email, user_name, user_phone, report_id, score, grade, defects):
        subject = f"📄 आपकी वास्तु रिपोर्ट तैयार है — {report_id}"
        body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; background: #f9fafb; padding: 40px 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <div style="background: linear-gradient(135deg, #fbbf24, #d97706); padding: 32px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">🕉️ VASTU ONE</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0; font-size: 14px;">आपकी रिपोर्ट तैयार है</p>
                </div>
                <div style="padding: 40px 32px;">
                    <h2 style="color: #0f1419; margin: 0 0 16px;">नमस्ते {user_name} 🎉</h2>
                    <p style="color: #4b5563; font-size: 16px;">आपके घर का वास्तु विश्लेषण पूरा हो गया है!</p>
                    <div style="background: #fef3c7; border-radius: 12px; padding: 24px; text-align: center; margin: 24px 0;">
                        <div style="font-size: 48px; font-weight: 800; color: #d97706;">{score}</div>
                        <div style="font-size: 14px; color: #92400e;">/ 100</div>
                        <div style="display: inline-block; background: #f59e0b; color: white; padding: 8px 24px; border-radius: 8px; margin-top: 12px; font-weight: 700; font-size: 18px;">{grade}</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: #f9fafb; border-radius: 12px;">
                        <div style="font-size: 32px; font-weight: 700; color: #ef4444;">{defects}</div>
                        <div style="font-size: 12px; color: #6b7280; text-transform: uppercase;">दोष मिले</div>
                    </div>
                    <div style="text-align: center; margin: 32px 0;">
                        <a href="http://127.0.0.1:8000/plan-report/{report_id}" style="display: inline-block; background: linear-gradient(135deg, #fbbf24, #d97706); color: white; padding: 14px 32px; text-decoration: none; border-radius: 10px; font-weight: 700;">
                            📄 पूरी रिपोर्ट देखें
                        </a>
                    </div>
                </div>
                <div style="background: #f9fafb; padding: 24px; text-align: center; font-size: 12px; color: #6b7280;">
                    <p>© 2026 VASTU ONE — सर्वे भवन्तु सुखिनः</p>
                </div>
            </div>
        </body>
        </html>
        """
        return {"email_sent": self.send_email(user_email, subject, body), "whatsapp_sent": False}


if __name__ == "__main__":
    ns = NotificationService()
    print("\n📧 Testing email...")
    ok = ns.send_email(
        to_email="dashaenterprises21@gmail.com",
        subject="✅ Test — VASTU ONE",
        html_body="<h1>🕉️ Test</h1><p>Notification system working!</p>"
    )
    print(f"Email: {'✅ SUCCESS' if ok else '❌ FAILED'}")