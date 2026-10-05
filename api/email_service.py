"""
VASTU ONE - Email Service
==========================
SMTP-based email sender with HTML templates.
"""
from __future__ import annotations
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


class EmailService:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.user = os.getenv("SMTP_USER", "")
        self.password = os.getenv("SMTP_PASSWORD", "")
        self.from_name = os.getenv("SMTP_FROM_NAME", "VASTU ONE")
        self.from_email = os.getenv("SMTP_FROM_EMAIL", self.user or "noreply@vastuone.in")
        self.enabled = bool(self.user and self.password)
    
    def send(self, to_email: str, subject: str, html_body: str, text_body: Optional[str] = None) -> bool:
        if not self.enabled:
            print(f"\n{'=' * 70}")
            print(f"📧 EMAIL (dev mode — SMTP not configured)")
            print(f"{'=' * 70}")
            print(f"To:      {to_email}")
            print(f"Subject: {subject}")
            if text_body:
                print(text_body)
            print(f"{'=' * 70}\n")
            return True
        
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP(self.host, self.port, timeout=15) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"⚠️  Email send failed: {e}")
            return False
    
    def _base_template(self, title: str, content: str) -> str:
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title></head>
<body style="margin:0;padding:0;background:#05060F;font-family:-apple-system,sans-serif;color:#F8F7F2;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#05060F;padding:40px 20px;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#0A0D1A;border-radius:12px;border:1px solid rgba(248,247,242,0.08);">
<tr><td style="padding:32px 40px;border-bottom:1px solid rgba(248,247,242,0.08);">
<div style="font-family:Georgia,serif;font-size:24px;font-weight:700;">VASTU <span style="color:#D4AF37;">ONE</span></div>
<div style="font-size:10px;letter-spacing:2px;color:rgba(248,247,242,0.65);text-transform:uppercase;margin-top:4px;">Traceable Vastu Intelligence</div>
</td></tr>
<tr><td style="padding:40px;">{content}</td></tr>
<tr><td style="padding:24px 40px;background:#05060F;border-top:1px solid rgba(248,247,242,0.08);font-size:12px;color:rgba(248,247,242,0.35);text-align:center;">
<p style="margin:0;">© 2026 VASTU ONE. All rights reserved.</p>
</td></tr>
</table></td></tr></table>
</body></html>"""
    
    def send_welcome(self, to_email: str, full_name: str, tenant_name: str) -> bool:
        content = f"""
        <h2 style="font-family:Georgia,serif;font-size:24px;margin:0 0 16px;">Welcome to VASTU ONE</h2>
        <p style="font-size:15px;line-height:1.6;color:rgba(248,247,242,0.75);margin:0 0 16px;">Hi {full_name},</p>
        <p style="font-size:15px;line-height:1.6;color:rgba(248,247,242,0.75);margin:0 0 24px;">
            Your workspace <strong style="color:#D4AF37;">{tenant_name}</strong> is ready.
        </p>
        <a href="http://localhost:8000/dashboard.html" style="display:inline-block;padding:14px 28px;background:#D4AF37;color:#05060F;text-decoration:none;border-radius:8px;font-weight:600;font-size:14px;">Open Dashboard →</a>
        """
        return self.send(to_email, f"Welcome to VASTU ONE — {tenant_name}", self._base_template("Welcome", content), f"Welcome, {full_name}!")
    
    def send_password_reset(self, to_email: str, full_name: str, reset_token: str) -> bool:
        reset_url = f"http://localhost:8000/reset-password.html?token={reset_token}"
        content = f"""
        <h2 style="font-family:Georgia,serif;font-size:24px;margin:0 0 16px;">Reset your password</h2>
        <p style="font-size:15px;line-height:1.6;color:rgba(248,247,242,0.75);margin:0 0 16px;">Hi {full_name},</p>
        <p style="font-size:15px;line-height:1.6;color:rgba(248,247,242,0.75);margin:0 0 24px;">
            Click below to reset your password. Link expires in <strong>30 minutes</strong>.
        </p>
        <a href="{reset_url}" style="display:inline-block;padding:14px 28px;background:#D4AF37;color:#05060F;text-decoration:none;border-radius:8px;font-weight:600;font-size:14px;">Reset Password →</a>
        <p style="font-size:13px;color:rgba(248,247,242,0.5);margin:24px 0 0;">Or copy this link:<br><span style="color:#D4AF37;word-break:break-all;">{reset_url}</span></p>
        """
        return self.send(to_email, "Reset your VASTU ONE password", self._base_template("Password Reset", content), f"Reset link: {reset_url}")
    
    def send_otp(self, to_email: str, full_name: str, otp_code: str) -> bool:
        content = f"""
        <h2 style="font-family:Georgia,serif;font-size:24px;margin:0 0 16px;">Your verification code</h2>
        <p style="font-size:15px;color:rgba(248,247,242,0.75);margin:0 0 24px;">Hi {full_name}, enter this code:</p>
        <div style="text-align:center;padding:24px;background:#05060F;border-radius:8px;border:1px solid rgba(212,175,55,0.3);margin:0 0 24px;">
            <div style="font-family:'Courier New',monospace;font-size:36px;font-weight:700;letter-spacing:8px;color:#D4AF37;">{otp_code}</div>
        </div>
        <p style="font-size:13px;color:rgba(248,247,242,0.5);">Expires in 10 minutes.</p>
        """
        return self.send(to_email, f"Your VASTU ONE code: {otp_code}", self._base_template("OTP", content), f"OTP: {otp_code}")
    
    def send_password_changed(self, to_email: str, full_name: str) -> bool:
        content = f"""
        <h2 style="font-family:Georgia,serif;font-size:24px;margin:0 0 16px;">Password changed</h2>
        <p style="font-size:15px;color:rgba(248,247,242,0.75);margin:0 0 16px;">Hi {full_name},</p>
        <p style="font-size:15px;color:rgba(248,247,242,0.75);">Your VASTU ONE password was changed. If this wasn't you, contact support.</p>
        """
        return self.send(to_email, "Your VASTU ONE password was changed", self._base_template("Password Changed", content), f"Hi {full_name}, password changed.")


# Singleton
email_service = EmailService()