"""
Vastu One - Configuration
Loads from .env file with fallbacks
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = BASE_DIR / ".env"
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
except ImportError:
    BASE_DIR = Path(__file__).resolve().parent.parent

# ═══ OWNER ═══
OWNER_NAME = os.getenv("OWNER_NAME", "Deepak Nagpure")
OWNER_EMAIL = os.getenv("OWNER_EMAIL", "dashaenterprises21@gmail.com")
OWNER_PHONE = os.getenv("OWNER_PHONE", "9890602105")
OWNER_CITY = os.getenv("OWNER_CITY", "Nagpur")

# ═══ BRAND ═══
BRAND_NAME = os.getenv("BRAND_NAME", "VASTU ONE")
BRAND_TAGLINE = os.getenv("BRAND_TAGLINE", "India Ka No.1 Vastu Engine")

# ═══ PATHS ═══
DATA_DIR = BASE_DIR / "data"
DEVATAS_FILE = DATA_DIR / "devatas_45.json"
ELEMENTS_FILE = DATA_DIR / "elements_5.json"
REPORTS_DIR = BASE_DIR / "reports_data"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure directories exist
for d in [REPORTS_DIR, UPLOADS_DIR, OUTPUT_DIR]:
    d.mkdir(exist_ok=True)

# ═══ API ═══
API_TITLE = f"{BRAND_NAME} API"
API_DESCRIPTION = f"{BRAND_TAGLINE} - Vastu Analysis API"
API_VERSION = "1.0.0"

# ═══ JWT ═══
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "vastu-one-secret-key-deepak-nagpure-2026-change-in-production"
)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", "7"))

# ═══ EMAIL ═══
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", OWNER_EMAIL)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", BRAND_NAME)
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", OWNER_EMAIL)

# ═══ DATABASE ═══
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'vastu_one.db'}")

# ═══ PAYMENT ═══
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

# ═══ SERVER ═══
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))