"""
VASTU ONE — Email Service
Send kundli reports, invoices, OTPs via email
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Dict, List, Optional


class EmailService:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.user = os.getenv("SMTP_USER", "")
        self.password = os.getenv("SMTP_PASSWORD", "").replace(" ", "")
        self.from_name = os.getenv("SMTP_FROM_NAME", "Vastu One")
        self.from_email = os.getenv("SMTP_FROM_EMAIL", self.user)
        
        if not self.user or not self.password:
            print("⚠️ SMTP credentials missing in .env")
    
    def _connect(self):
        """Create SMTP connection"""
        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.login(self.user, self.password)
        return server
    
    def send_html(self, to: str, subject: str, html: str, attachments: List[Dict] = None) -> Dict:
        """Send HTML email with optional attachments"""
        if not self.user or not self.password:
            return {"success": False, "error": "SMTP not configured"}
        
        try:
            msg = MIMEMultipart('mixed')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to
            msg['Subject'] = subject
            
            # HTML body
            msg.attach(MIMEText(html, 'html', 'utf-8'))
            
            # Attachments
            if attachments:
                for att in attachments:
                    part = MIMEApplication(att['data'], _subtype=att.get('type', 'pdf'))
                    part.add_header('Content-Disposition', 'attachment', filename=att['filename'])
                    msg.attach(part)
            
            server = self._connect()
            server.send_message(msg)
            server.quit()
            return {"success": True, "to": to, "subject": subject}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_kundli_report(self, to: str, name: str, pdf_data: bytes = None, report_url: str = "") -> Dict:
        """Send kundli report email"""
        subject = f"🕉️ Aapki Kundli Report Ready Hai — Vastu One"
        
        html = self._kundli_email_template(name, report_url)
        
        attachments = None
        if pdf_data:
            attachments = [{
                'data': pdf_data,
                'filename': f'Kundli-Report-{name}.pdf',
                'type': 'pdf'
            }]
        
        return self.send_html(to, subject, html, attachments)
    
    def send_payment_confirmation(self, to: str, name: str, amount: float, payment_id: str) -> Dict:
        """Send payment confirmation"""
        subject = f"✅ Payment Confirmed — {amount} — Vastu One"
        
        html = f'''
        <div style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; padding: 40px; background: #fdfaf3; color: #1f1b18;">
          <div style="text-align: center; padding-bottom: 24px; border-bottom: 3px double #b8860b;">
            <h1 style="color: #6b1420; margin: 0; font-size: 32px;">VASTU ONE</h1>
            <div style="font-size: 12px; color: #8a7563; letter-spacing: 0.2em; margin-top: 6px;">PAYMENT CONFIRMED</div>
          </div>
          
          <div style="padding: 32px 0;">
            <p style="font-size: 16px;">Namaste <strong>{name}</strong>,</p>
            <p style="font-size: 14px; line-height: 1.7;">Aapka payment successfully process ho gaya hai. Aapki kundli report 2-3 minute mein email pe aayegi.</p>
            
            <div style="background: #f0fdf4; border-left: 4px solid #22c55e; padding: 16px; margin: 24px 0; border-radius: 8px;">
              <div style="font-size: 13px;"><strong>Amount Paid:</strong> {amount}</div>
              <div style="font-size: 13px; margin-top: 6px;"><strong>Payment ID:</strong> <code>{payment_id}</code></div>
            </div>
          </div>
          
          <div style="text-align: center; padding-top: 24px; border-top: 1px solid #e5d8c5; font-size: 12px; color: #8a7563;">
            Vastu One · Every finding has a source<br>
            Made with care in India 🇮🇳
          </div>
        </div>
        '''
        return self.send_html(to, subject, html)
    
    def send_otp(self, to: str, otp: str) -> Dict:
        """Send OTP via email"""
        subject = f"🔐 Your Vastu One OTP: {otp}"
        
        html = f'''
        <div style="font-family: Georgia, serif; max-width: 500px; margin: 0 auto; padding: 40px; background: #fdfaf3;">
          <h2 style="color: #6b1420; text-align: center;">VASTU ONE</h2>
          <p style="font-size: 16px; text-align: center;">Your OTP Code:</p>
          <div style="background: #6b1420; color: #f5ede0; padding: 24px; text-align: center; border-radius: 8px; font-size: 36px; font-weight: 700; letter-spacing: 8px; font-family: monospace;">
            {otp}
          </div>
          <p style="font-size: 13px; color: #8a7563; text-align: center; margin-top: 20px;">Valid for 5 minutes. Do not share with anyone.</p>
        </div>
        '''
        return self.send_html(to, subject, html)
    
    def send_invoice(self, to: str, name: str, order_data: Dict) -> Dict:
        """Send invoice email"""
        subject = f"📄 Invoice #{order_data.get('id', 'N/A')} — Vastu One"
        
        html = f'''
        <div style="font-family: Georgia, serif; max-width: 700px; margin: 0 auto; padding: 40px; background: #fdfaf3;">
          <div style="text-align: center; padding-bottom: 20px; border-bottom: 3px double #b8860b;">
            <h1 style="color: #6b1420; margin: 0;">VASTU ONE</h1>
            <div style="font-size: 11px; color: #8a7563; letter-spacing: 0.2em;">TAX INVOICE</div>
          </div>
          
          <div style="padding: 30px 0;">
            <p>Namaste <strong>{name}</strong>,</p>
            <p>Aapki invoice attached hai.</p>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
              <tr style="background: #6b1420; color: #f5ede0;">
                <th style="padding: 12px; text-align: left;">Item</th>
                <th style="padding: 12px; text-align: right;">Amount</th>
              </tr>
              <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e5d8c5;">Kundli Premium Report</td>
                <td style="padding: 12px; border-bottom: 1px solid #e5d8c5; text-align: right;">505</td>
              </tr>
              <tr>
                <td style="padding: 12px; font-weight: 700; text-align: right;">Total:</td>
                <td style="padding: 12px; font-weight: 700; text-align: right;">505</td>
              </tr>
            </table>
          </div>
          
          <div style="text-align: center; padding-top: 20px; border-top: 1px solid #e5d8c5; font-size: 12px; color: #8a7563;">
            Vastu One · Nagpur, Maharashtra · Made with care in India
          </div>
        </div>
        '''
        return self.send_html(to, subject, html)
    
    def _kundli_email_template(self, name: str, report_url: str) -> str:
        return f'''
        <div style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; padding: 40px; background: #fdfaf3; color: #1f1b18;">
          <div style="text-align: center; padding-bottom: 24px; border-bottom: 3px double #b8860b;">
            <div style="font-size: 14px; color: #b8860b; letter-spacing: 0.3em; margin-bottom: 12px;">VASTU ONE</div>
            <h1 style="color: #6b1420; margin: 0; font-size: 28px;">🕉️ Aapki Kundli Ready Hai</h1>
          </div>
          
          <div style="padding: 32px 0; text-align: center;">
            <p style="font-size: 16px;">Namaste <strong>{name}</strong>,</p>
            <p style="font-size: 14px; line-height: 1.7; color: #5c4433;">
              Aapki complete Vedic Kundli report taiyar hai.<br>
              Neeche diye button se download kar sakte hain.
            </p>
            
            {f'<a href="{report_url}" style="display: inline-block; margin: 24px 0; padding: 16px 40px; background: linear-gradient(135deg, #e0b968, #d4a961, #b8893b); color: #2a0810; text-decoration: none; border-radius: 10px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; font-size: 14px;">📄 Download Kundli Report</a>' if report_url else ''}
            
            <div style="background: #fffbeb; border-left: 4px solid #d4a961; padding: 16px; margin: 24px 0; border-radius: 8px; text-align: left;">
              <div style="font-size: 13px; line-height: 1.7;">
                <strong>📋 Report Includes:</strong><br>
                ✓ 50+ pages complete report<br>
                ✓ 41 Vedic analysis engines<br>
                ✓ Charts, Dashas, Predictions<br>
                ✓ Remedies & Lal Kitab
              </div>
            </div>
            
            <p style="font-size: 12px; color: #8a7563; margin-top: 24px;">
              Report security ke liye, 7 din baad link expire ho jayega.
            </p>
          </div>
          
          <div style="text-align: center; padding-top: 24px; border-top: 1px solid #e5d8c5; font-size: 12px; color: #8a7563;">
            <div style="font-size: 14px; color: #b8860b; margin-bottom: 8px;">✦</div>
            <div><strong>VASTU ONE</strong></div>
            <div style="font-style: italic; margin-top: 4px;">Every finding has a source. Every decision, a reason.</div>
            <div style="margin-top: 8px;">Made with care in India 🇮🇳</div>
          </div>
        </div>
        '''


email_service = EmailService()


def send_kundli_email(to, name, pdf_data=None, report_url=""):
    return email_service.send_kundli_report(to, name, pdf_data, report_url)


def send_payment_email(to, name, amount, payment_id):
    return email_service.send_payment_confirmation(to, name, amount, payment_id)


def send_otp_email(to, otp):
    return email_service.send_otp(to, otp)


def send_invoice_email(to, name, order_data):
    return email_service.send_invoice(to, name, order_data)
