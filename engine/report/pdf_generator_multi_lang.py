"""
VASTU ONE - Multi-Language Research PDF Generator
Supports: English, Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, Sanskrit
With proper font support for Hindi/Devanagari
"""

from datetime import datetime
from pathlib import Path
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.report.multi_language import get_translation, get_supported_languages, LANGUAGES


# 
# FONT SETUP
# 

FONTS_DIR = Path(__file__).parent / "fonts"

def register_fonts():
    """Register custom fonts for Hindi/Devanagari support"""
    registered = {}
    
    # Register Noto Sans Devanagari (for Hindi, Marathi, Sanskrit)
    devanagari_path = FONTS_DIR / "NotoSansDevanagari.ttf"
    if devanagari_path.exists():
        try:
            pdfmetrics.registerFont(TTFont("NotoDevanagari", str(devanagari_path)))
            registered["devanagari"] = True
            print(" Noto Sans Devanagari font registered")
        except Exception as e:
            print(f" Error registering Devanagari font: {e}")
            registered["devanagari"] = False
    else:
        print(" NotoSansDevanagari.ttf not found")
        registered["devanagari"] = False
    
    return registered


FONTS = register_fonts()


# 
# COLORS
# 

GOLD = HexColor("#d4a961")
GOLD_DEEP = HexColor("#b8893b")
DARK_RED = HexColor("#5a1420")
IVORY_MUTED = HexColor("#a8a29e")
RED = HexColor("#dc2626")
GREEN = HexColor("#10b981")


def get_styles(lang: str = "en"):
    """Get styles with language-specific font"""
    s = getSampleStyleSheet()
    
    # Use Devanagari font for Hindi, Marathi, Sanskrit
    body_font = "NotoDevanagari" if lang in ["hi", "mr", "sa"] and FONTS.get("devanagari") else "Helvetica"
    title_font = "NotoDevanagari" if lang in ["hi", "mr", "sa"] and FONTS.get("devanagari") else "Helvetica-Bold"
    
    s.add(ParagraphStyle(name="CoverTitle", parent=s["Title"], fontSize=42, textColor=GOLD, alignment=TA_CENTER, spaceAfter=20, fontName=title_font, leading=50))
    s.add(ParagraphStyle(name="CoverSubtitle", parent=s["Normal"], fontSize=16, textColor=IVORY_MUTED, alignment=TA_CENTER, spaceAfter=10, fontName=body_font))
    s.add(ParagraphStyle(name="CoverCountry", parent=s["Title"], fontSize=56, textColor=DARK_RED, alignment=TA_CENTER, spaceAfter=14, fontName=title_font))
    s.add(ParagraphStyle(name="SectionTitle", parent=s["Heading1"], fontSize=24, textColor=DARK_RED, spaceAfter=16, spaceBefore=20, fontName=title_font))
    s.add(ParagraphStyle(name="SubSection", parent=s["Heading2"], fontSize=16, textColor=GOLD_DEEP, spaceAfter=10, spaceBefore=14, fontName=title_font))
    s.add(ParagraphStyle(name="SubSubSection", parent=s["Heading3"], fontSize=13, textColor=DARK_RED, spaceAfter=6, spaceBefore=8, fontName=title_font))
    # हद/दवनगर क लए जयद leading (मतरओ क लए जगह)
    if lang in ["hi", "mr", "sa"]:
        body_leading = 18
        body_fontsize = 11
    else:
        body_leading = 15
        body_fontsize = 10
    
    s.add(ParagraphStyle(name="BodyText2", parent=s["Normal"], fontSize=body_fontsize, textColor=black, leading=body_leading, spaceAfter=8, alignment=TA_JUSTIFY, fontName=body_font, wordWrap="CJK"))
    s.add(ParagraphStyle(name="SmallText", parent=s["Normal"], fontSize=8, textColor=IVORY_MUTED, leading=12, fontName=body_font))
    s.add(ParagraphStyle(name="ParagraphText", parent=s["Normal"], fontSize=10, textColor=black, leading=15, spaceAfter=10, alignment=TA_JUSTIFY, leftIndent=10, rightIndent=10, fontName=body_font))
    s.add(ParagraphStyle(name="Quote", parent=s["Normal"], fontSize=10, textColor=DARK_RED, leading=15, spaceAfter=8, leftIndent=20, rightIndent=20, fontName=body_font))
    
    return s


def make_cover(story, data, styles, t, lang):
    """Cover page with language support"""
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("VASTU ONE", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(t["title"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(data["country"].upper(), styles["CoverCountry"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(t["subtitle"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(t["generated"] + ": " + data["date"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 2*cm))
    
    summary = [
        [t.get("total_predictions", "Total Predictions"), str(data.get("total_predictions", 0))],
        [t.get("total_yogas", "Total Yogas"), str(data.get("yogas_complete", {}).get("total_yogas", 0))],
        [t.get("ashtakavarga_points", "Ashtakavarga Points"), str(data.get("ashtakavarga", {}).get("total", 0))],
        [t.get("strongest_planet", "Strongest Planet"), data.get("shadbala", {}).get("strongest", "")],
        [t.get("weakest_planet", "Weakest Planet"), data.get("shadbala", {}).get("weakest", "")],
        [t.get("mahadasha", "Mahadasha"), data.get("complete_dasha", {}).get("levels", {}).get("mahadasha", {}).get("planet", "")],
    ]
    
    tbl = Table(summary, colWidths=[7*cm, 7*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), HexColor("#f5efe2")),
        ("TEXTCOLOR", (0, 0), (0, -1), DARK_RED),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(tbl)
    story.append(PageBreak())


def make_toc(story, t, styles):
    """Table of contents with language support"""
    story.append(Paragraph(t["toc"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=20))
    
    toc = [
        t["exec_summary"],
        t["birth_chart"],
        t["planetary_deep"],
        t["dasha_5"],
        t["yoga"],
        t["transit"],
        t["varshphal"],
        t["nadi"],
        t["bnn"],
        t["paragraphs"],
        t["remedies"],
        t["historical"],
        t["references"],
        t["disclaimer"],
    ]
    for i, item in enumerate(toc, 1):
        story.append(Paragraph(f"{i}. {item}", styles["BodyText2"]))
    story.append(PageBreak())


def make_exec_summary(story, data, styles, t, lang):
    """Executive summary with language support"""
    story.append(Paragraph("1. " + t["exec_summary"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    country = data["country"]
    intro = f"This research-grade report presents a complete 12-layer astrological analysis of {country} using Swiss Ephemeris for actual planetary calculations. The report combines classical Vedic astrology principles with advanced Bhrigu Nandi Nadi (BNN) techniques to provide {data.get('total_predictions', 0)} distinct predictions across multiple systems."
    story.append(Paragraph(intro, styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("Key Findings", styles["SubSection"]))
    findings = [
        f"Mahadasha: {data.get('complete_dasha', {}).get('levels', {}).get('mahadasha', {}).get('planet', '')}",
        f"Antardasha: {data.get('complete_dasha', {}).get('levels', {}).get('antardasha', {}).get('planet', '')}",
        f"Pratyantardasha: {data.get('complete_dasha', {}).get('levels', {}).get('pratyantardasha', {}).get('planet', '')}",
        f"Strongest Planet: {data.get('shadbala', {}).get('strongest', '')}",
        f"Weakest Planet: {data.get('shadbala', {}).get('weakest', '')}",
        f"Total Yogas: {data.get('yogas_complete', {}).get('total_yogas', 0)}",
        f"Ashtakavarga: {data.get('ashtakavarga', {}).get('total', 0)} points",
        f"Transit Verdict: {data.get('transit_ashtakavarga', {}).get('overall_verdict', '')}",
    ]
    for f in findings:
        story.append(Paragraph(" " + f, styles["BodyText2"]))
    story.append(PageBreak())


def make_planets_deep(story, data, styles, t, lang):
    """Planetary deep analysis"""
    story.append(Paragraph("3. " + t["planetary_deep"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    planets = data.get("planetary_deep", {}).get("planets", {})
    for name, p in planets.items():
        story.append(Paragraph(name + "  " + p.get("rashi", "") + " " + str(p.get("degree", 0)) + "", styles["SubSubSection"]))
        
        info = [
            ["Attribute", "Value"],
            ["Rashi", p.get("rashi", "")],
            ["Degree", str(p.get("degree", 0)) + ""],
            ["House", str(p.get("house", ""))],
            ["Dignity", p.get("dignity", "")],
            ["Avastha", p.get("avastha", {}).get("state", "")],
            ["Saptavargaja", str(p.get("saptavargaja_bala", {}).get("percentage", 0)) + "%"],
            ["Digbala", str(p.get("digbala", {}).get("digbala", 0)) + "/60"],
            ["Nakshatra Lord", p.get("nakshatra_lord", "")],
            ["Nakshatra Deity", p.get("nakshatra_deity", "")],
        ]
        tbl = Table(info, colWidths=[5*cm, 10*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
            ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_dasha_5_levels(story, data, styles, t, lang):
    """Dasha 5 levels"""
    story.append(Paragraph("4. " + t["dasha_5"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    levels = data.get("complete_dasha", {}).get("levels", {})
    level_names = [
        ("mahadasha", t.get("mahadasha", "Mahadasha")),
        ("antardasha", t.get("antardasha", "Antardasha")),
        ("pratyantardasha", t.get("pratyantardasha", "Pratyantardasha")),
        ("sookshma", t.get("sookshma", "Sookshma")),
        ("prana", t.get("prana", "Prana")),
    ]
    
    for key, title in level_names:
        level = levels.get(key, {})
        if not level:
            continue
        story.append(Paragraph(title + ": " + level.get("planet", ""), styles["SubSection"]))
        story.append(Paragraph("Period: " + level.get("start_date", "") + " to " + level.get("end_date", ""), styles["BodyText2"]))
        if level.get("effects"):
            story.append(Paragraph(t.get("positive", "Positive") + ": " + level["effects"].get("positive", ""), styles["BodyText2"]))
            story.append(Paragraph(t.get("negative", "Negative") + ": " + level["effects"].get("negative", ""), styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_yogas(story, data, styles, t, lang):
    """Yogas"""
    story.append(Paragraph("5. " + t["yoga"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    yogas = data.get("yogas_complete", {})
    story.append(Paragraph(t.get("total_yogas", "Total Yogas") + ": " + str(yogas.get("total_yogas", 0)), styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    if yogas.get("auspicious"):
        story.append(Paragraph(t.get("auspicious", "Auspicious Yogas"), styles["SubSection"]))
        for y in yogas["auspicious"]:
            story.append(Paragraph(" " + y["name"] + " (" + y["strength"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  " + y["effect"], styles["BodyText2"]))
            story.append(Paragraph("  " + t.get("classical_ref", "Classical Ref") + ": " + y.get("classical_ref", ""), styles["SmallText"]))
        story.append(Spacer(1, 0.3*cm))
    
    if yogas.get("doshas"):
        story.append(Paragraph(t.get("doshas", "Doshas"), styles["SubSection"]))
        for y in yogas["doshas"]:
            story.append(Paragraph(" " + y["name"] + " (" + y["strength"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  " + y["effect"], styles["BodyText2"]))
    story.append(PageBreak())


def make_transit(story, data, styles, t, lang):
    """Transit + Ashtakavarga"""
    story.append(Paragraph("6. " + t["transit"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    transit = data.get("transit_ashtakavarga", {})
    story.append(Paragraph("Overall Verdict: " + transit.get("overall_verdict", ""), styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    for tr in transit.get("transit_analysis", []):
        story.append(Paragraph(tr["planet"] + " in " + tr["rashi"] + " (House " + str(tr["house"]) + ")  Bindu: " + str(tr["bindu"]) + "/8", styles["SubSubSection"]))
        story.append(Paragraph("Verdict: " + tr["verdict"], styles["BodyText2"]))
    story.append(PageBreak())


def make_varshphal(story, data, styles, t, lang):
    """Varshphal"""
    story.append(Paragraph("7. " + t["varshphal"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    varsh = data.get("varshphal", {})
    for year in ["2026", "2027", "2028"]:
        v = varsh.get(year, {})
        if not v:
            continue
        story.append(Paragraph("Year " + year, styles["SubSection"]))
        story.append(Paragraph("Solar Return: " + v.get("solar_return_date", ""), styles["BodyText2"]))
        story.append(Paragraph("Muntha: " + v.get("muntha", {}).get("rashi", ""), styles["BodyText2"]))
        story.append(Paragraph("Year Lord: " + v.get("year_lord", {}).get("planet", ""), styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_nadi(story, data, styles, t, lang):
    """Nadi/Bhrigu"""
    story.append(Paragraph("8. " + t["nadi"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    nadi = data.get("nadi_bhrigu", {})
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        story.append(Paragraph("Nakshatra: " + n.get("nakshatra", "") + " | Nadi: " + n.get("nadi", ""), styles["BodyText2"]))
        story.append(Paragraph("Past Life: " + n.get("past_life", ""), styles["BodyText2"]))
    
    if nadi.get("karmic_debts"):
        story.append(Paragraph("Karmic Debts", styles["SubSection"]))
        for k in nadi["karmic_debts"]:
            story.append(Paragraph(" " + k["name"] + "  " + k["remedy"], styles["BodyText2"]))
    story.append(PageBreak())


def make_bnn(story, data, styles, t, lang):
    """BNN Hidden Gems"""
    story.append(Paragraph("9. " + t["bnn"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    bnn = data.get("bnn_data", {})
    
    if bnn.get("conjunctions_5_degree"):
        story.append(Paragraph("5-Degree Conjunctions", styles["SubSection"]))
        for c in bnn["conjunctions_5_degree"]:
            story.append(Paragraph(" " + c["planets"][0] + " + " + c["planets"][1] + " (" + str(c["degree_diff"]) + ")  " + c["strength"], styles["BodyText2"]))
    
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        story.append(Paragraph("Karakas", styles["SubSection"]))
        for k, v in bnn["karakas"]["karakas"].items():
            story.append(Paragraph(" " + k + ": " + v["planet"], styles["BodyText2"]))
    story.append(PageBreak())


def make_paragraphs(story, data, styles, t, lang):
    """Deep Paragraphs"""
    story.append(Paragraph("10. " + t["paragraphs"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    paragraphs_data = data.get("paragraphs_data", {})
    paragraphs = paragraphs_data.get("paragraphs", [])
    
    for p in paragraphs:
        story.append(Paragraph(p.get("title", ""), styles["SubSubSection"]))
        story.append(Paragraph(p.get("paragraph", ""), styles["ParagraphText"]))
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_disclaimer(story, styles, t, lang):
    """Disclaimer"""
    story.append(Paragraph("12. " + t["disclaimer"], styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    text = "This report is generated using Swiss Ephemeris for actual planetary calculations and classical Vedic astrology principles. It is provided for educational and informational purposes only."
    story.append(Paragraph(text, styles["BodyText2"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(" 2026 Vastu One  India", styles["BodyText2"]))


def generate_multi_language_pdf(country: str = "India", lang: str = "en") -> BytesIO:
    """Generate PDF in specified language"""
    data = get_master_prediction(country)
    if "error" in data:
        return None
    
    # Add paragraphs and BNN if not present
    if "paragraphs_data" not in data:
        try:
            from engine.astro.deep_paragraph_engine import get_full_explanation_report
            data["paragraphs_data"] = get_full_explanation_report(country)
        except:
            pass
    
    if "bnn_data" not in data:
        try:
            from engine.astro.bnn_hidden_gems import analyze_bnn_complete
            from engine.astro.complete_chart_engine import calculate_complete_chart
            birth_data = COUNTRY_CHARTS[country]
            y, m, d = birth_data["date"]
            chart = calculate_complete_chart(y, m, d, birth_data["time"], birth_data["lat"], birth_data["lng"])
            data["bnn_data"] = analyze_bnn_complete(chart)
        except:
            pass
    
    # Get translations
    t = get_translation(lang)
    styles = get_styles(lang)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm, title="Vastu One - " + country + " - " + LANGUAGES.get(lang, "en"))
    
    story = []
    make_cover(story, data, styles, t, lang)
    make_toc(story, t, styles)
    make_exec_summary(story, data, styles, t, lang)
    make_planets_deep(story, data, styles, t, lang)
    make_dasha_5_levels(story, data, styles, t, lang)
    make_yogas(story, data, styles, t, lang)
    make_transit(story, data, styles, t, lang)
    make_varshphal(story, data, styles, t, lang)
    make_nadi(story, data, styles, t, lang)
    make_bnn(story, data, styles, t, lang)
    make_paragraphs(story, data, styles, t, lang)
    make_disclaimer(story, styles, t, lang)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def save_multi_language_pdf(country: str = "India", lang: str = "en", output_path: str = None):
    """Save PDF to file"""
    if output_path is None:
        output_path = "reports/" + country + "_" + lang + "_report.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_multi_language_pdf(country, lang)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Supported languages:", list(LANGUAGES.keys()))
    print()
    
    for lang in ["en", "hi"]:
        print(f"Generating {LANGUAGES.get(lang)} PDF...")
        path = save_multi_language_pdf("India", lang)
        if path:
            size = Path(path).stat().st_size
            print(f"  PDF: {path}")
            print(f"  Size: {size} bytes ({round(size/1024, 1)} KB)")
        print()
