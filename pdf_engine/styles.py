from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Nirmala UI — Windows 10/11 का built-in Hindi font (best ligature support)
NIRMALA_REG = Path("C:/Windows/Fonts/Nirmala.ttf")
NIRMALA_BOLD = Path("C:/Windows/Fonts/NirmalaB.ttf")

FONT_REG = "VastuHindi"
FONT_BOLD_REG = "VastuHindi-Bold"
HINDI_OK = False

try:
    if NIRMALA_REG.exists() and NIRMALA_BOLD.exists():
        pdfmetrics.registerFont(TTFont(FONT_REG, str(NIRMALA_REG)))
        pdfmetrics.registerFont(TTFont(FONT_BOLD_REG, str(NIRMALA_BOLD)))
        HINDI_OK = True
        print("[INFO] Using Nirmala UI font for Hindi")
    else:
        print("[WARNING] Nirmala UI not found, using Helvetica")
except Exception as e:
    print(f"[WARNING] Hindi font not loaded: {e}")
    HINDI_OK = False


BRAND = {
    "primary":     colors.HexColor("#f59e0b"),
    "primary_dark":colors.HexColor("#d97706"),
    "dark":        colors.HexColor("#0f1419"),
    "dark_2":      colors.HexColor("#1e2530"),
    "text":        colors.HexColor("#0f1419"),
    "text_dim":    colors.HexColor("#6b7280"),
    "green":       colors.HexColor("#10b981"),
    "red":         colors.HexColor("#ef4444"),
    "blue":        colors.HexColor("#3b82f6"),
    "orange":      colors.HexColor("#f97316"),
    "purple":      colors.HexColor("#8b5cf6"),
    "border":      colors.HexColor("#e5e7eb"),
    "bg_light":    colors.HexColor("#f9fafb"),
}

PAGE_SIZE = A4
MARGIN = 18 * mm
CONTENT_WIDTH = PAGE_SIZE[0] - 2 * MARGIN

FONT = FONT_REG if HINDI_OK else "Helvetica"
FONT_BOLD = FONT_BOLD_REG if HINDI_OK else "Helvetica-Bold"
FONT_ITALIC = FONT_REG if HINDI_OK else "Helvetica-Oblique"


def get_styles():
    return {
        "cover_title": ParagraphStyle("cover_title", fontName=FONT_BOLD, fontSize=36, leading=42, textColor=BRAND["primary"], alignment=TA_CENTER, spaceAfter=8),
        "cover_subtitle": ParagraphStyle("cover_subtitle", fontName=FONT, fontSize=14, leading=20, textColor=BRAND["text_dim"], alignment=TA_CENTER, spaceAfter=30),
        "cover_score": ParagraphStyle("cover_score", fontName=FONT_BOLD, fontSize=72, leading=80, textColor=BRAND["primary"], alignment=TA_CENTER),
        "cover_grade": ParagraphStyle("cover_grade", fontName=FONT_BOLD, fontSize=22, leading=28, textColor=BRAND["text"], alignment=TA_CENTER, spaceAfter=20),
        "cover_info": ParagraphStyle("cover_info", fontName=FONT, fontSize=11, leading=18, textColor=BRAND["text"], alignment=TA_CENTER),
        "h1": ParagraphStyle("h1", fontName=FONT_BOLD, fontSize=20, leading=26, textColor=BRAND["text"], spaceBefore=12, spaceAfter=10),
        "h2": ParagraphStyle("h2", fontName=FONT_BOLD, fontSize=14, leading=20, textColor=BRAND["primary_dark"], spaceBefore=8, spaceAfter=6),
        "body": ParagraphStyle("body", fontName=FONT, fontSize=10.5, leading=16, textColor=BRAND["text"], spaceAfter=6),
        "body_dim": ParagraphStyle("body_dim", fontName=FONT, fontSize=9.5, leading=14, textColor=BRAND["text_dim"], spaceAfter=4),
        "card_title": ParagraphStyle("card_title", fontName=FONT_BOLD, fontSize=12, leading=16, textColor=BRAND["text"], spaceAfter=4),
        "card_meta": ParagraphStyle("card_meta", fontName=FONT, fontSize=9.5, leading=14, textColor=BRAND["text_dim"], spaceAfter=6),
        "shastra_ref": ParagraphStyle("shastra_ref", fontName=FONT, fontSize=9.5, leading=14, textColor=BRAND["purple"], spaceAfter=6),
        "mantra": ParagraphStyle("mantra", fontName=FONT_BOLD, fontSize=11, leading=16, textColor=BRAND["primary_dark"], alignment=TA_CENTER),
        "footer": ParagraphStyle("footer", fontName=FONT, fontSize=8, leading=10, textColor=BRAND["text_dim"], alignment=TA_CENTER),
    }


BRAND_TEXT = {
    "company": "Vastu AI",
    "tagline": "शास्त्र-आधारित वास्तु विश्लेषण",
    "tagline_en": "Scripture-Based Vastu Analysis",
    "sources": "बृहत्संहिता • समरांगण सूत्रधार • मयमतम् • मानसार",
    "footer": "Vastu AI — भारत का पहला शास्त्र-आधारित वास्तु विश्लेषण सिस्टम",
    "disclaimer": "यह रिपोर्ट बृहत्संहिता, समरांगण सूत्रधार, मयमतम् और मानसार जैसे प्राचीन शास्त्रों के सिद्धांतों पर आधारित है। यह पेशेवर वास्तु परामर्श का विकल्प नहीं है। महत्वपूर्ण निर्णयों के लिए योग्य वास्तु विशेषज्ञ से परामर्श करें।",
}