# Vastu One — Complete Prompts

## 1. Email Integration

Bhai, mujhe Vastu One project mein Gmail SMTP email integration complete karna hai.

PROJECT: C:\Users\HP\Desktop\vastu-one
GMAIL: dashaenterprises21@gmail.com
APP PASSWORD: [YAHAN NAYA APP PASSWORD DAALO]

TASK:
1. Gmail App Password setup
2. .env mein SMTP config
3. engine/services/email_service.py verify
4. api/routes/email_routes.py verify
5. api/main.py mein register
6. test_email.py chalao

GMAIL APP PASSWORD:
1. https://myaccount.google.com/security → 2-Step Verification ON
2. https://myaccount.google.com/apppasswords → App name: "Vastu One" → Create
3. 16-digit password copy karo

POWERSHELL:
$new_password = "PASTE_16_DIGIT"
$env_content = Get-Content .env -Raw
$env_content = $env_content -replace "SMTP_PASSWORD=.*", "SMTP_PASSWORD=$new_password"
Set-Content -Path .env -Value $env_content -Encoding UTF8
python test_direct.py

AB YEH SAB KARO AUR OUTPUT PASTE KARO.

---

## 2. WhatsApp Integration

Bhai, Vastu One mein WhatsApp integration karo.

OPTION: [wa.me Links / Cloud API / Twilio]

FILES:
- frontend/static/whatsapp-share.js (verify)
- engine/services/whatsapp_service.py
- api/routes/whatsapp_routes.py

FEATURES:
- Share on WhatsApp
- Send to specific number
- Support chat

AB YEH SAB KARO AUR OUTPUT PASTE KARO.

---

## 3. Invoice/Subscription/Refund

Bhai, Vastu One mein yeh 3 pages verify karo:

1. frontend/legal/invoice.html
2. frontend/legal/subscription.html
3. frontend/legal/refund-request.html

TEST:
Start-Process "http://localhost:8000/legal/subscription.html"

AB YEH SAB KARO AUR OUTPUT PASTE KARO.

---

## 4. Full Project Status

Bhai, Vastu One ka full status check karo.

PROJECT: C:\Users\HP\Desktop\vastu-one

CHECK:
1. python test_all_engines.py
2. kundli-pro.html — 46 cards
3. PDF download — 47 sections
4. Legal pages — /legal/*
5. Razorpay — /api/payments/plans
6. Email — test_email.py
7. WhatsApp share
8. git status

AB YEH SAB CHECK KARO AUR FULL REPORT DO.
