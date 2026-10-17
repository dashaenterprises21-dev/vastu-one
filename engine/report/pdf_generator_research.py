"""
VASTU ONE - Research Grade PDF Report Generator
Includes all 12 layers: Planetary Deep, Dasha 5 Levels, 100+ Yogas, 
Ashtakavarga+Transit, Varshphal, Nadi/Bhrigu, BNN Hidden Gems, Deep Paragraphs
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

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.astro.deep_paragraph_engine import get_full_explanation_report
from engine.astro.bnn_hidden_gems import analyze_bnn_complete
from engine.astro.complete_chart_engine import calculate_complete_chart


GOLD = HexColor("#d4a961")
GOLD_DEEP = HexColor("#b8893b")
DARK_RED = HexColor("#5a1420")
IVORY_MUTED = HexColor("#a8a29e")
RED = HexColor("#dc2626")
GREEN = HexColor("#10b981")


def get_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="CoverTitle", parent=s["Title"], fontSize=42, textColor=GOLD, alignment=TA_CENTER, spaceAfter=20, fontName="Helvetica-Bold", leading=50))
    s.add(ParagraphStyle(name="CoverSubtitle", parent=s["Normal"], fontSize=16, textColor=IVORY_MUTED, alignment=TA_CENTER, spaceAfter=10, fontName="Helvetica-Oblique"))
    s.add(ParagraphStyle(name="CoverCountry", parent=s["Title"], fontSize=56, textColor=DARK_RED, alignment=TA_CENTER, spaceAfter=14, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SectionTitle", parent=s["Heading1"], fontSize=24, textColor=DARK_RED, spaceAfter=16, spaceBefore=20, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SubSection", parent=s["Heading2"], fontSize=16, textColor=GOLD_DEEP, spaceAfter=10, spaceBefore=14, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SubSubSection", parent=s["Heading3"], fontSize=13, textColor=DARK_RED, spaceAfter=6, spaceBefore=8, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="BodyText2", parent=s["Normal"], fontSize=10, textColor=black, leading=15, spaceAfter=8, alignment=TA_JUSTIFY))
    s.add(ParagraphStyle(name="SmallText", parent=s["Normal"], fontSize=8, textColor=IVORY_MUTED, leading=12))
    s.add(ParagraphStyle(name="ParagraphText", parent=s["Normal"], fontSize=10, textColor=black, leading=15, spaceAfter=10, alignment=TA_JUSTIFY, leftIndent=10, rightIndent=10))
    s.add(ParagraphStyle(name="Quote", parent=s["Normal"], fontSize=10, textColor=DARK_RED, leading=15, spaceAfter=8, leftIndent=20, rightIndent=20, fontName="Helvetica-Oblique"))
    return s


def make_cover(story, data, styles):
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("VASTU ONE", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Research Grade Astrological Report", styles["CoverSubtitle"]))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(data["country"].upper(), styles["CoverCountry"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("12-Layer Master Prediction Analysis", styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Generated: " + data["date"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 2*cm))
    
    summary = [
        ["Metric", "Value"],
        ["Total Predictions", str(data.get("total_predictions", 0))],
        ["Yogas Detected", str(data.get("yogas_complete", {}).get("total_yogas", 0))],
        ["Ashtakavarga Points", str(data.get("ashtakavarga", {}).get("total", 0))],
        ["Strongest Planet", data.get("shadbala", {}).get("strongest", "")],
        ["Weakest Planet", data.get("shadbala", {}).get("weakest", "")],
        ["Mahadasha", data.get("complete_dasha", {}).get("levels", {}).get("mahadasha", {}).get("planet", "")],
        ["Antardasha", data.get("complete_dasha", {}).get("levels", {}).get("antardasha", {}).get("planet", "")],
        ["Pratyantardasha", data.get("complete_dasha", {}).get("levels", {}).get("pratyantardasha", {}).get("planet", "")],
        ["Varshphal Year", str(data.get("varshphal", {}).get("2026", {}).get("year", 2026))],
        ["BNN Yogas", str(len(data.get("bnn_data", {}).get("bnn_yogas", [])))],
        ["Karakas", str(len(data.get("bnn_data", {}).get("karakas", {}).get("karakas", {})))],
    ]
    
    t = Table(summary, colWidths=[7*cm, 7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("BACKGROUND", (0, 1), (0, -1), HexColor("#f5efe2")),
        ("TEXTCOLOR", (0, 1), (0, -1), DARK_RED),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Based on: BPHS, Phaladeepika, Bhrigu Samhita, Nadi Astrology, Saravali, Jaimini Sutras, Bhrigu Nandi Nadi", styles["CoverSubtitle"]))
    story.append(PageBreak())


def make_toc(story, styles):
    story.append(Paragraph("Table of Contents", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=20))
    
    toc = [
        "1. Executive Summary",
        "2. Birth Chart Analysis",
        "3. Planetary Deep Analysis (20+ Attributes per Planet)",
        "4. Complete Dasha (5 Levels)",
        "5. Yoga Analysis (100+ Combinations)",
        "6. Ashtakavarga + Transit Integration",
        "7. Varshphal (Annual Charts 2026-2028)",
        "8. Nadi/Bhrigu Karmic Analysis",
        "9. BNN Hidden Gems (5-Degree Rule, Karakas, Trinal Combinations)",
        "10. Deep Paragraph Explanations (22 Detailed Analyses)",
        "11. Research References",
        "12. Disclaimer",
    ]
    for t in toc:
        story.append(Paragraph(t, styles["BodyText2"]))
    story.append(PageBreak())


def make_exec_summary(story, data, styles):
    story.append(Paragraph("1. Executive Summary", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph("This research-grade report presents a complete 12-layer astrological analysis of " + data["country"] + " using Swiss Ephemeris for actual planetary calculations. The report combines classical Vedic astrology principles with advanced Bhrigu Nandi Nadi (BNN) techniques to provide " + str(data.get("total_predictions", 0)) + " distinct predictions across multiple systems.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("Key Findings", styles["SubSection"]))
    findings = [
        "Current Mahadasha: " + data.get("complete_dasha", {}).get("levels", {}).get("mahadasha", {}).get("planet", ""),
        "Current Antardasha: " + data.get("complete_dasha", {}).get("levels", {}).get("antardasha", {}).get("planet", ""),
        "Current Pratyantardasha: " + data.get("complete_dasha", {}).get("levels", {}).get("pratyantardasha", {}).get("planet", ""),
        "Strongest Planet: " + data.get("shadbala", {}).get("strongest", ""),
        "Weakest Planet: " + data.get("shadbala", {}).get("weakest", ""),
        "Total Yogas: " + str(data.get("yogas_complete", {}).get("total_yogas", 0)),
        "Ashtakavarga: " + str(data.get("ashtakavarga", {}).get("total", 0)) + " points",
        "Transit Verdict: " + data.get("transit_ashtakavarga", {}).get("overall_verdict", ""),
        "Varshphal 2026: Muntha " + data.get("varshphal", {}).get("2026", {}).get("muntha", {}).get("rashi", ""),
        "BNN Conjunctions: " + str(len(data.get("bnn_data", {}).get("conjunctions_5_degree", []))),
        "Karakas: " + str(len(data.get("bnn_data", {}).get("karakas", {}).get("karakas", {}))),
    ]
    for f in findings:
        story.append(Paragraph(" " + f, styles["BodyText2"]))
    story.append(PageBreak())


def make_planets_deep(story, data, styles):
    story.append(Paragraph("3. Planetary Deep Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph("Each planet in the birth chart represents a specific dimension of the country's destiny. This section provides 20+ attributes per planet including Avastha, Saptavargaja Bala, Digbala, Ishta/Kashta Phala, and Nakshatra details.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
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
            ["Saptavargaja Bala", str(p.get("saptavargaja_bala", {}).get("percentage", 0)) + "%"],
            ["Digbala", str(p.get("digbala", {}).get("digbala", 0)) + "/60"],
            ["Naisargika Bala", str(p.get("naisargika_bala", {}).get("value", 0)) + "/60"],
            ["Ishta Phala", str(p.get("ishta_kashta", {}).get("ishta_phala", 0))],
            ["Kashta Phala", str(p.get("ishta_kashta", {}).get("kashta_phala", 0))],
            ["Nakshatra Lord", p.get("nakshatra_lord", "")],
            ["Nakshatra Deity", p.get("nakshatra_deity", "")],
        ]
        t = Table(info, colWidths=[5*cm, 10*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
            ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_dasha_5_levels(story, data, styles):
    story.append(Paragraph("4. Complete Dasha (5 Levels)", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    levels = data.get("complete_dasha", {}).get("levels", {})
    level_names = [("mahadasha", "Mahadasha (Major Period)"), ("antardasha", "Antardasha (Sub-Period)"), ("pratyantardasha", "Pratyantardasha (Sub-Sub)"), ("sookshma", "Sookshma (Micro)"), ("prana", "Prana (Finest)")]
    
    for key, title in level_names:
        level = levels.get(key, {})
        if not level:
            continue
        story.append(Paragraph(title + ": " + level.get("planet", ""), styles["SubSection"]))
        story.append(Paragraph("Period: " + level.get("start_date", "") + " to " + level.get("end_date", ""), styles["BodyText2"]))
        if level.get("effects"):
            story.append(Paragraph("Positive: " + level["effects"].get("positive", ""), styles["BodyText2"]))
            story.append(Paragraph("Negative: " + level["effects"].get("negative", ""), styles["BodyText2"]))
            story.append(Paragraph("Reference: " + level["effects"].get("classical_ref", ""), styles["SmallText"]))
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_yogas(story, data, styles):
    story.append(Paragraph("5. Yoga Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    yogas = data.get("yogas_complete", {})
    story.append(Paragraph("Total Yogas: " + str(yogas.get("total_yogas", 0)) + " (" + str(len(yogas.get("auspicious", []))) + " auspicious, " + str(len(yogas.get("doshas", []))) + " doshas)", styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    if yogas.get("auspicious"):
        story.append(Paragraph("Auspicious Yogas", styles["SubSection"]))
        for y in yogas["auspicious"]:
            story.append(Paragraph(" " + y["name"] + " (" + y["strength"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  " + y["effect"], styles["BodyText2"]))
            story.append(Paragraph("  " + y.get("classical_ref", ""), styles["SmallText"]))
        story.append(Spacer(1, 0.3*cm))
    
    if yogas.get("doshas"):
        story.append(Paragraph("Doshas", styles["SubSection"]))
        for y in yogas["doshas"]:
            story.append(Paragraph(" " + y["name"] + " (" + y["strength"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  " + y["effect"], styles["BodyText2"]))
            story.append(Paragraph("  " + y.get("classical_ref", ""), styles["SmallText"]))
    story.append(PageBreak())


def make_transit_ashtaka(story, data, styles):
    story.append(Paragraph("6. Ashtakavarga + Transit Integration", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    transit = data.get("transit_ashtakavarga", {})
    story.append(Paragraph("Overall Verdict: " + transit.get("overall_verdict", "") + " (" + str(transit.get("positive_count", 0)) + " positive, " + str(transit.get("negative_count", 0)) + " negative)", styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    for t in transit.get("transit_analysis", []):
        story.append(Paragraph(t["planet"] + " in " + t["rashi"] + " (House " + str(t["house"]) + ")  Bindu: " + str(t["bindu"]) + "/8", styles["SubSubSection"]))
        story.append(Paragraph("Verdict: " + t["verdict"], styles["BodyText2"]))
    story.append(PageBreak())


def make_varshphal(story, data, styles):
    story.append(Paragraph("7. Varshphal (Annual Charts 2026-2028)", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    varsh = data.get("varshphal", {})
    for year in ["2026", "2027", "2028"]:
        v = varsh.get(year, {})
        if not v:
            continue
        story.append(Paragraph("Year " + year, styles["SubSection"]))
        story.append(Paragraph("Solar Return: " + v.get("solar_return_date", ""), styles["BodyText2"]))
        story.append(Paragraph("Muntha: " + v.get("muntha", {}).get("rashi", "") + " (House " + str(v.get("muntha", {}).get("house", "")) + ")", styles["BodyText2"]))
        story.append(Paragraph("Muntha Meaning: " + v.get("muntha", {}).get("meaning", ""), styles["BodyText2"]))
        story.append(Paragraph("Year Lord: " + v.get("year_lord", {}).get("planet", ""), styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_nadi_bhrigu(story, data, styles):
    story.append(Paragraph("8. Nadi/Bhrigu Karmic Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    nadi = data.get("nadi_bhrigu", {})
    
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        story.append(Paragraph("Nadi Karma", styles["SubSection"]))
        story.append(Paragraph("Nakshatra: " + n.get("nakshatra", "") + " | Nadi: " + n.get("nadi", ""), styles["BodyText2"]))
        story.append(Paragraph("Karma: " + n.get("karma", ""), styles["BodyText2"]))
        story.append(Paragraph("Past Life: " + n.get("past_life", ""), styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    
    if nadi.get("karmic_debts"):
        story.append(Paragraph("Karmic Debts", styles["SubSection"]))
        for k in nadi["karmic_debts"]:
            story.append(Paragraph(" " + k["name"] + " (" + k["type"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  Cause: " + k["cause"], styles["BodyText2"]))
            story.append(Paragraph("  Remedy: " + k["remedy"], styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    
    if nadi.get("spiritual_evolution"):
        se = nadi["spiritual_evolution"]
        story.append(Paragraph("Spiritual Evolution", styles["SubSection"]))
        story.append(Paragraph("Level: " + se.get("level", ""), styles["BodyText2"]))
        story.append(Paragraph("9th Lord: " + se.get("lord_9th", "") + " | 12th Lord: " + se.get("lord_12th", ""), styles["BodyText2"]))
    story.append(PageBreak())


def make_bnn(story, data, styles):
    story.append(Paragraph("9. BNN Hidden Gems", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    bnn = data.get("bnn_data", {})
    
    if bnn.get("conjunctions_5_degree"):
        story.append(Paragraph("5-Degree Conjunctions (BNN Rule)", styles["SubSection"]))
        for c in bnn["conjunctions_5_degree"]:
            story.append(Paragraph(" " + c["planets"][0] + " + " + c["planets"][1] + " (" + str(c["degree_diff"]) + ")  " + c["strength"], styles["BodyText2"]))
            story.append(Paragraph("  " + c["bnn_effect"], styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        story.append(Paragraph("Karakas (Jaimini System)", styles["SubSection"]))
        for k, v in bnn["karakas"]["karakas"].items():
            story.append(Paragraph(" " + k + ": " + v["planet"] + " (" + str(v["degree"]) + ")  " + v["meaning"], styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    
    if bnn.get("nakshatra_pada"):
        story.append(Paragraph("Nakshatra Pada Analysis", styles["SubSection"]))
        for n in bnn["nakshatra_pada"]:
            story.append(Paragraph(" " + n["planet"] + " in " + n["nakshatra"] + " pada " + str(n["pada"]) + "  " + n["pada_meaning"], styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    
    if bnn.get("trinal_combinations"):
        story.append(Paragraph("Trinal Rashi Combinations", styles["SubSection"]))
        for t in bnn["trinal_combinations"][:10]:
            story.append(Paragraph(" " + t["planets"][0] + " + " + t["planets"][1] + " (" + t["rashis"][0] + " + " + t["rashis"][1] + ")", styles["BodyText2"]))
    story.append(PageBreak())


def make_deep_paragraphs(story, data, styles):
    story.append(Paragraph("10. Deep Paragraph Explanations", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    paragraphs_data = data.get("paragraphs_data", {})
    paragraphs = paragraphs_data.get("paragraphs", [])
    
    story.append(Paragraph("Total Detailed Analyses: " + str(len(paragraphs)), styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    for p in paragraphs:
        story.append(Paragraph(p.get("title", ""), styles["SubSubSection"]))
        story.append(Paragraph(p.get("paragraph", ""), styles["ParagraphText"]))
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_disclaimer(story, styles):
    story.append(Paragraph("12. Disclaimer", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    text = """
    This report is generated using Swiss Ephemeris for actual planetary calculations and classical Vedic astrology principles from BPHS, Phaladeepika, Bhrigu Samhita, Nadi Astrology, Saravali, Jaimini Sutras, and Bhrigu Nandi Nadi (BNN).
    <br/><br/>
    <b>Purpose:</b> This research-grade report is provided for educational and informational purposes only. It represents astrological analysis based on traditional principles and should not be considered as absolute truth or professional advice.
    <br/><br/>
    <b>Limitations:</b> Astrological predictions are probabilistic in nature. They indicate trends and tendencies rather than fixed outcomes. Many factors influence real-world events, including human free will and collective action.
    <br/><br/>
    <b>No Liability:</b> Vastu One, its creators, and affiliates are not responsible for any decisions, actions, or consequences arising from the use of this report.
    <br/><br/>
    <b> 2026 Vastu One  India  All Rights Reserved</b>
    """
    story.append(Paragraph(text, styles["BodyText2"]))


def generate_research_pdf(country: str = "India") -> BytesIO:
    """Generate complete research-grade PDF"""
    data = get_master_prediction(country)
    if "error" in data:
        return None
    
    # Add paragraphs and BNN
    data["paragraphs_data"] = get_full_explanation_report(country)
    
    birth_data = COUNTRY_CHARTS[country]
    y, m, d = birth_data["date"]
    chart = calculate_complete_chart(y, m, d, birth_data["time"], birth_data["lat"], birth_data["lng"])
    data["bnn_data"] = analyze_bnn_complete(chart)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm, title="Vastu One Research Report - " + country, author="Vastu One")
    
    styles = get_styles()
    story = []
    
    make_cover(story, data, styles)
    make_toc(story, styles)
    make_exec_summary(story, data, styles)
    make_planets_deep(story, data, styles)
    make_dasha_5_levels(story, data, styles)
    make_yogas(story, data, styles)
    make_transit_ashtaka(story, data, styles)
    make_varshphal(story, data, styles)
    make_nadi_bhrigu(story, data, styles)
    make_bnn(story, data, styles)
    make_deep_paragraphs(story, data, styles)
    make_disclaimer(story, styles)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def save_research_pdf(country: str = "India", output_path: str = None):
    if output_path is None:
        output_path = "reports/" + country + "_research_report.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_research_pdf(country)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating research-grade PDF report...")
    path = save_research_pdf("India")
    if path:
        size = Path(path).stat().st_size
        print("PDF generated: " + path)
        print("Size: " + str(size) + " bytes (" + str(round(size/1024, 1)) + " KB)")
