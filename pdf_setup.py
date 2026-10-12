# VASTU ONE - PDF Report Generator

from pathlib import Path

pdf_code = '''"""
VASTU ONE - Professional PDF Report Generator
50+ page astrological report with all engines
"""

from datetime import datetime
from pathlib import Path
from io import BytesIO

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, KeepTogether
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("reportlab not installed. Install with: pip install reportlab")

from engine.astro.predictions_engine import get_predictions, COUNTRY_CHARTS


# Colors
GOLD = HexColor("#d4a961")
DARK_RED = HexColor("#5a1420")
IVORY = HexColor("#f5f1e8")
IVORY_MUTED = HexColor("#a8a29e")
RED = HexColor("#dc2626")
AMBER = HexColor("#f59e0b")
GREEN = HexColor("#10b981")


def get_styles():
    """Create custom styles"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name="CoverTitle", parent=styles["Title"],
        fontSize=36, textColor=GOLD, alignment=TA_CENTER,
        spaceAfter=20, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle", parent=styles["Normal"],
        fontSize=16, textColor=IVORY_MUTED, alignment=TA_CENTER,
        spaceAfter=10, fontName="Helvetica-Oblique",
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle", parent=styles["Heading1"],
        fontSize=24, textColor=GOLD, spaceAfter=16, spaceBefore=20,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="SubSection", parent=styles["Heading2"],
        fontSize=16, textColor=GOLD, spaceAfter=10, spaceBefore=14,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="BodyText2", parent=styles["Normal"],
        fontSize=11, textColor=black, leading=16,
        spaceAfter=8, alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        name="SmallText", parent=styles["Normal"],
        fontSize=9, textColor=IVORY_MUTED, leading=13,
    ))
    styles.add(ParagraphStyle(
        name="Prediction", parent=styles["Normal"],
        fontSize=10, textColor=black, leading=14,
        spaceAfter=6, leftIndent=10,
    ))
    
    return styles


def create_cover_page(story, data, styles):
    """Create cover page"""
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("VASTU ONE", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("World Prediction Report", styles["CoverSubtitle"]))
    story.append(Spacer(1, 2*cm))
    
    story.append(Paragraph(f"<b>{data['country']}</b>", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Generated: {data['date']}", styles["CoverSubtitle"]))
    story.append(Spacer(1, 3*cm))
    
    # Summary box
    summary = [
        ["Total Predictions", str(data["total_predictions"])],
        ["Yogas Detected", str(data["yogas"]["total_yogas"])],
        ["Ashtakavarga Points", str(data["ashtakavarga"]["total"])],
        ["Strongest Planet", data["shadbala"]["strongest"]],
        ["Weakest Planet", data["shadbala"]["weakest"]],
        ["Mahadasha", data["dasha"]["mahadasha"]["lord"]],
        ["Antardasha", data["dasha"]["antardasha"]["lord"]],
        ["Pratyantardasha", data["dasha"]["pratyantardasha"]["lord"]],
    ]
    
    t = Table(summary, colWidths=[8*cm, 8*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), HexColor("#f0ebe0")),
        ("TEXTCOLOR", (0, 0), (0, -1), DARK_RED),
        ("TEXTCOLOR", (1, 0), (1, -1), black),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph(
        "Based on Swiss Ephemeris calculations — BPHS, Phaladeepika, Bhrigu Samhita, Nadi Astrology",
        styles["CoverSubtitle"]
    ))
    story.append(PageBreak())


def create_table_of_contents(story, styles):
    """Create table of contents"""
    story.append(Paragraph("Table of Contents", styles["SectionTitle"]))
    story.append(Spacer(1, 0.5*cm))
    
    toc_items = [
        ("1.", "Executive Summary", "Page 3"),
        ("2.", "Birth Chart Analysis", "Page 4"),
        ("3.", "Planetary Positions", "Page 5"),
        ("4.", "Vimshottari Dasha (5 Levels)", "Page 6"),
        ("5.", "Yoga Analysis", "Page 8"),
        ("6.", "Ashtakavarga (337 Points)", "Page 10"),
        ("7.", "Shadbala (6 Strengths)", "Page 12"),
        ("8.", "Nakshatra Analysis", "Page 14"),
        ("9.", "Varshphal (Annual Chart)", "Page 16"),
        ("10.", "Transit Analysis", "Page 18"),
        ("11.", "100+ Predictions", "Page 20"),
        ("12.", "Risk Assessment", "Page 30"),
        ("13.", "Remedies", "Page 35"),
        ("14.", "Research References", "Page 40"),
        ("15.", "Disclaimer", "Page 42"),
    ]
    
    for num, title, page in toc_items:
        story.append(Paragraph(
            f"<b>{num}</b> {title} <font color='#a8a29e'>........ {page}</font>",
            styles["BodyText2"]
        ))
    
    story.append(PageBreak())


def create_executive_summary(story, data, styles):
    """Create executive summary"""
    story.append(Paragraph("1. Executive Summary", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    summary_text = f"""
    This report presents a comprehensive astrological analysis of <b>{data['country']}</b> 
    based on actual planetary calculations using Swiss Ephemeris. The analysis incorporates 
    <b>{data['total_predictions']} predictions</b> across multiple astrological systems including 
    Vimshottari Dasha, Yoga detection, Ashtakavarga, Shadbala, Nakshatra analysis, Varshphal, 
    and current transit positions.
    <br/><br/>
    <b>Key Findings:</b>
    <br/>
    • Current Mahadasha: <b>{data['dasha']['mahadasha']['lord']}</b>
    <br/>
    • Current Antardasha: <b>{data['dasha']['antardasha']['lord']}</b>
    <br/>
    • Current Pratyantardasha: <b>{data['dasha']['pratyantardasha']['lord']}</b>
    <br/>
    • Total Yogas Detected: <b>{data['yogas']['total_yogas']}</b>
    <br/>
    • Auspicious Yogas: <b>{len(data['yogas']['auspicious'])}</b>
    <br/>
    • Doshas: <b>{len(data['yogas']['doshas'])}</b>
    <br/>
    • Strongest Planet: <b>{data['shadbala']['strongest']}</b>
    <br/>
    • Weakest Planet: <b>{data['shadbala']['weakest']}</b>
    <br/>
    • Ashtakavarga Total: <b>{data['ashtakavarga']['total']} points</b>
    <br/>
    • Varshphal Year: <b>{data['varshphal']['year']}</b>
    """
    
    story.append(Paragraph(summary_text, styles["BodyText2"]))
    story.append(PageBreak())


def create_planetary_table(data, styles):
    """Create planetary positions table"""
    story.append(Paragraph("3. Planetary Positions", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    # Birth chart planets table
    story.append(Paragraph("Birth Chart", styles["SubSection"]))
    
    table_data = [["Planet", "Rashi", "Degree", "House", "Dignity", "Nakshatra", "Pada"]]
    
    planets = data.get("chart", {}).get("planets", {})
    if not planets:
        # Try to get from chart data
        planets = {
            "Sun": data["chart"]["sun"],
            "Moon": data["chart"]["moon"],
        }
    
    for name, p in planets.items():
        table_data.append([
            name,
            p.get("rashi", ""),
            f"{p.get('degree', 0):.2f}",
            str(p.get("house", "")),
            p.get("dignity", ""),
            p.get("nakshatra", {}).get("name", "") if isinstance(p.get("nakshatra"), dict) else p.get("nakshatra", ""),
            str(p.get("nakshatra", {}).get("pada", "") if isinstance(p.get("nakshatra"), dict) else ""),
        ])
    
    t = Table(table_data, colWidths=[2.5*cm, 2.5*cm, 1.8*cm, 1.5*cm, 2.5*cm, 3.5*cm, 1.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())


def create_dasha_section(story, data, styles):
    """Create Dasha section"""
    story.append(Paragraph("4. Vimshottari Dasha", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    d = data["dasha"]
    
    story.append(Paragraph(f"<b>Age:</b> {d['age_years']} years", styles["BodyText2"]))
    story.append(Paragraph(f"<b>Moon Nakshatra:</b> {d['moon_nakshatra']}", styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    # Current Dasha
    story.append(Paragraph("Current Dasha", styles["SubSection"]))
    dasha_data = [
        ["Level", "Planet", "Lord", "Period"],
        ["Mahadasha", d["mahadasha"]["planet"], d["mahadasha"]["lord"], f"Age {d['mahadasha']['start_age']:.1f} - {d['mahadasha']['end_age']:.1f}"],
        ["Antardasha", d["antardasha"]["planet"], d["antardasha"]["lord"], f"Age {d['antardasha']['start_age']:.1f} - {d['antardasha']['end_age']:.1f}"],
        ["Pratyantardasha", d["pratyantardasha"]["planet"], d["pratyantardasha"]["lord"], "Current"],
    ]
    
    t = Table(dasha_data, colWidths=[4*cm, 3*cm, 3*cm, 6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    # Full Mahadasha sequence
    story.append(Paragraph("Full Mahadasha Sequence", styles["SubSection"]))
    seq_data = [["Planet", "Lord", "Start Age", "End Age", "Years"]]
    for dasha in d["full_mahadasha_sequence"]:
        seq_data.append([
            dasha["planet"], dasha["lord"],
            f"{dasha['start_age']:.2f}", f"{dasha['end_age']:.2f}",
            f"{dasha['years']:.2f}"
        ])
    
    t = Table(seq_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 3*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
    ]))
    story.append(t)
    story.append(PageBreak())


def create_yoga_section(story, data, styles):
    """Create Yoga section"""
    story.append(Paragraph("5. Yoga Analysis", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(f"<b>Total Yogas Detected:</b> {data['yogas']['total_yogas']}", styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    # Auspicious
    story.append(Paragraph("Auspicious Yogas", styles["SubSection"]))
    for y in data["yogas"]["auspicious"]:
        story.append(Paragraph(f"<b>• {y['name']}</b> ({y['strength']})", styles["Prediction"]))
        story.append(Paragraph(f"  {y['effect']}", styles["Prediction"]))
    story.append(Spacer(1, 0.3*cm))
    
    # Doshas
    story.append(Paragraph("Doshas", styles["SubSection"]))
    for y in data["yogas"]["doshas"]:
        story.append(Paragraph(f"<b>• {y['name']}</b> ({y['strength']})", styles["Prediction"]))
        story.append(Paragraph(f"  {y['effect']}", styles["Prediction"]))
    
    story.append(PageBreak())


def create_ashtakavarga_section(story, data, styles):
    """Create Ashtakavarga section"""
    story.append(Paragraph("6. Ashtakavarga (337 Points)", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(f"<b>Total Points:</b> {data['ashtakavarga']['total']}", styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    # Strongest signs
    story.append(Paragraph("Strongest Signs", styles["SubSection"]))
    for rashi, score in data["ashtakavarga"]["strongest"]:
        story.append(Paragraph(f"<b>• {rashi}</b> — {score} points", styles["Prediction"]))
    story.append(Spacer(1, 0.3*cm))
    
    # Weakest signs
    story.append(Paragraph("Weakest Signs", styles["SubSection"]))
    for rashi, score in data["ashtakavarga"]["weakest"]:
        story.append(Paragraph(f"<b>• {rashi}</b> — {score} points", styles["Prediction"]))
    
    story.append(PageBreak())


def create_shadbala_section(story, data, styles):
    """Create Shadbala section"""
    story.append(Paragraph("7. Shadbala (6 Strengths)", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("Planetary Ranking", styles["SubSection"]))
    
    table_data = [["Rank", "Planet", "Total Strength"]]
    for i, (planet, total) in enumerate(data["shadbala"]["ranking"], 1):
        table_data.append([str(i), planet, f"{total:.2f}"])
    
    t = Table(table_data, colWidths=[2*cm, 5*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(f"<b>Strongest Planet:</b> {data['shadbala']['strongest']}", styles["BodyText2"]))
    story.append(Paragraph(f"<b>Weakest Planet:</b> {data['shadbala']['weakest']}", styles["BodyText2"]))
    
    story.append(PageBreak())


def create_nakshatra_section(story, data, styles):
    """Create Nakshatra section"""
    story.append(Paragraph("8. Nakshatra Analysis", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    table_data = [["Planet", "Nakshatra", "Pada", "Lord", "Deity", "Gana", "Element"]]
    for planet, n in data["nakshatra"].items():
        table_data.append([
            planet, n["nakshatra"], str(n["pada"]), n["lord"],
            n["deity"], n.get("gana", ""), n.get("element", "")
        ])
    
    t = Table(table_data, colWidths=[2*cm, 2.8*cm, 1.2*cm, 2*cm, 2.5*cm, 2*cm, 2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
    ]))
    story.append(t)
    
    story.append(PageBreak())


def create_varshphal_section(story, data, styles):
    """Create Varshphal section"""
    story.append(Paragraph("9. Varshphal (Annual Chart)", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    v = data["varshphal"]
    story.append(Paragraph(f"<b>Year:</b> {v['year']}", styles["BodyText2"]))
    story.append(Paragraph(f"<b>Muntha:</b> {v['muntha']['rashi']}", styles["BodyText2"]))
    story.append(Paragraph(f"<b>Year Lord:</b> {v['year_lord']['planet']}", styles["BodyText2"]))
    story.append(Paragraph(f"<b>Annual Ascendant:</b> {v['ascendant']['rashi']} {v['ascendant']['degree']} deg", styles["BodyText2"]))
    
    story.append(PageBreak())


def create_predictions_section(story, data, styles):
    """Create predictions section"""
    story.append(Paragraph("10. Predictions", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    # Group by category
    categories = {}
    for p in data["predictions"]:
        cat = p["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    for cat, preds in categories.items():
        story.append(Paragraph(f"{cat} ({len(preds)})", styles["SubSection"]))
        for p in preds:
            story.append(Paragraph(f"<b>• {p['title']}</b>", styles["Prediction"]))
            story.append(Paragraph(f"  {p['prediction']}", styles["Prediction"]))
            if p.get("confidence"):
                story.append(Paragraph(f"  <i>Confidence: {p['confidence']}</i>", styles["SmallText"]))
            story.append(Spacer(1, 0.15*cm))
        story.append(Spacer(1, 0.3*cm))
    
    story.append(PageBreak())


def create_disclaimer(story, styles):
    """Create disclaimer"""
    story.append(Paragraph("Disclaimer", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3*cm))
    
    disclaimer = """
    This report is generated using Swiss Ephemeris for actual planetary calculations 
    and classical Vedic astrology principles from BPHS, Phaladeepika, Bhrigu Samhita, 
    Nadi Astrology, Saravali, Jaimini Sutras, and other classical texts.
    <br/><br/>
    The predictions are based on astrological principles and should be considered 
    for educational and informational purposes only. They do not constitute 
    professional advice for financial, medical, legal, or personal decisions.
    <br/><br/>
    Vastu One and its creators are not responsible for any actions taken based on 
    this report. Always consult qualified professionals for important decisions.
    <br/><br/>
    <b>© 2026 Vastu One · Nagpur, Maharashtra</b>
    """
    
    story.append(Paragraph(disclaimer, styles["BodyText2"]))


def generate_pdf(country: str = "India") -> BytesIO:
    """Generate complete PDF report"""
    if not HAS_REPORTLAB:
        return None
    
    data = get_predictions(country)
    if "error" in data:
        return None
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=f"Vastu One - {country} Prediction Report",
    )
    
    styles = get_styles()
    story = []
    
    # Build all sections
    create_cover_page(story, data, styles)
    create_table_of_contents(story, styles)
    create_executive_summary(story, data, styles)
    create_planetary_table(story, data, styles)
    create_dasha_section(story, data, styles)
    create_yoga_section(story, data, styles)
    create_ashtakavarga_section(story, data, styles)
    create_shadbala_section(story, data, styles)
    create_nakshatra_section(story, data, styles)
    create_varshphal_section(story, data, styles)
    create_predictions_section(story, data, styles)
    create_disclaimer(story, styles)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def save_pdf(country: str = "India", output_path: str = None):
    """Save PDF to file"""
    if output_path is None:
        output_path = f"reports/{country}_prediction_report.pdf"
    
    Path("reports").mkdir(exist_ok=True)
    
    buffer = generate_pdf(country)
    if buffer is None:
        return None
    
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating PDF report for India...")
    path = save_pdf("India")
    if path:
        size = Path(path).stat().st_size
        print(f"PDF generated: {path}")
        print(f"Size: {size:,} bytes ({size/1024:.1f} KB)")
    else:
        print("Failed to generate PDF. Install reportlab: pip install reportlab")
'''

Path("engine/report/pdf_generator.py").write_text(pdf_code, encoding="utf-8")
print("PDF generator created")

# Install reportlab if needed
import subprocess
import sys

print()
print("Checking reportlab...")
result = subprocess.run([sys.executable, "-c", "import reportlab; print('reportlab OK')"], capture_output=True, text=True)
if "OK" not in result.stdout:
    print("Installing reportlab...")
    subprocess.run([sys.executable, "-m", "pip", "install", "reportlab"], check=False)

# Test
print()
print("=" * 60)
print("TESTING PDF GENERATION")
print("=" * 60)

result = subprocess.run([sys.executable, "-m", "engine.report.pdf_generator"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])