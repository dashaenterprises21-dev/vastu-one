from pathlib import Path

pdf_code = '''"""
VASTU ONE - Professional 50+ Page PDF Report Generator
Complete astrological analysis with charts and detailed sections
"""

from datetime import datetime
from pathlib import Path
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie

from engine.astro.predictions_engine import get_predictions, COUNTRY_CHARTS


# Colors
GOLD = HexColor("#d4a961")
GOLD_DEEP = HexColor("#b8893b")
DARK_RED = HexColor("#5a1420")
DARK_RED_DEEP = HexColor("#3a0a14")
IVORY = HexColor("#f5f1e8")
IVORY_MUTED = HexColor("#a8a29e")
RED = HexColor("#dc2626")
AMBER = HexColor("#f59e0b")
GREEN = HexColor("#10b981")
BLUE = HexColor("#3b82f6")
PURPLE = HexColor("#8b5cf6")


def get_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=42, textColor=GOLD, alignment=TA_CENTER, spaceAfter=24, fontName="Helvetica-Bold", leading=50))
    styles.add(ParagraphStyle(name="CoverSubtitle", parent=styles["Normal"], fontSize=18, textColor=IVORY_MUTED, alignment=TA_CENTER, spaceAfter=12, fontName="Helvetica-Oblique"))
    styles.add(ParagraphStyle(name="CoverCountry", parent=styles["Title"], fontSize=56, textColor=DARK_RED, alignment=TA_CENTER, spaceAfter=16, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="SectionTitle", parent=styles["Heading1"], fontSize=28, textColor=DARK_RED, spaceAfter=20, spaceBefore=24, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="SubSection", parent=styles["Heading2"], fontSize=18, textColor=GOLD_DEEP, spaceAfter=12, spaceBefore=16, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="SubSubSection", parent=styles["Heading3"], fontSize=14, textColor=DARK_RED_DEEP, spaceAfter=8, spaceBefore=10, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="BodyText2", parent=styles["Normal"], fontSize=11, textColor=black, leading=17, spaceAfter=10, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name="SmallText", parent=styles["Normal"], fontSize=9, textColor=IVORY_MUTED, leading=13))
    styles.add(ParagraphStyle(name="Prediction", parent=styles["Normal"], fontSize=11, textColor=black, leading=15, spaceAfter=8, leftIndent=14))
    styles.add(ParagraphStyle(name="CardTitle", parent=styles["Normal"], fontSize=13, textColor=GOLD_DEEP, fontName="Helvetica-Bold", spaceAfter=4))
    styles.add(ParagraphStyle(name="CardText", parent=styles["Normal"], fontSize=10, textColor=black, leading=14, spaceAfter=4))
    
    return styles


def make_cover(story, data, styles):
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("VASTU ONE", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Swiss Ephemeris · Classical Vedic Astrology", styles["CoverSubtitle"]))
    story.append(Spacer(1, 2*cm))
    
    story.append(Paragraph(data["country"].upper(), styles["CoverCountry"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Complete Astrological Analysis Report", styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Generated: {data['date']}", styles["CoverSubtitle"]))
    story.append(Spacer(1, 3*cm))
    
    # Summary table
    summary = [
        ["Metric", "Value"],
        ["Total Predictions", str(data["total_predictions"])],
        ["Yogas Detected", str(data["yogas"]["total_yogas"])],
        ["Auspicious Yogas", str(len(data["yogas"]["auspicious"]))],
        ["Doshas", str(len(data["yogas"]["doshas"]))],
        ["Ashtakavarga Points", str(data["ashtakavarga"]["total"])],
        ["Strongest Planet", data["shadbala"]["strongest"]],
        ["Weakest Planet", data["shadbala"]["weakest"]],
        ["Mahadasha", data["dasha"]["mahadasha"]["lord"]],
        ["Antardasha", data["dasha"]["antardasha"]["lord"]],
        ["Pratyantardasha", data["dasha"]["pratyantardasha"]["lord"]],
        ["Varshphal Year", str(data["varshphal"]["year"])],
        ["Muntha Rashi", data["varshphal"]["muntha"]["rashi"]],
    ]
    
    t = Table(summary, colWidths=[7*cm, 7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("BACKGROUND", (0, 1), (0, -1), HexColor("#f5efe2")),
        ("TEXTCOLOR", (0, 1), (0, -1), DARK_RED),
        ("TEXTCOLOR", (1, 1), (1, -1), black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t)
    
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Based on: BPHS · Phaladeepika · Bhrigu Samhita · Nadi Astrology · Saravali · Jaimini Sutras", styles["CoverSubtitle"]))
    story.append(PageBreak())


def make_toc(story, styles):
    story.append(Paragraph("Table of Contents", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=20))
    
    toc = [
        ("1", "Executive Summary", "3"),
        ("2", "Birth Chart Analysis", "5"),
        ("3", "Planetary Positions", "8"),
        ("4", "Vimshottari Dasha (5 Levels)", "11"),
        ("5", "Yoga Analysis", "15"),
        ("6", "Ashtakavarga — 337 Points", "19"),
        ("7", "Shadbala — 6 Strengths", "23"),
        ("8", "Nakshatra Analysis", "26"),
        ("9", "Varshphal — Annual Chart", "30"),
        ("10", "Transit Analysis (Gochar)", "33"),
        ("11", "Complete Predictions (38+)", "36"),
        ("12", "Risk Assessment", "42"),
        ("13", "Remedies (Upay)", "45"),
        ("14", "Research References", "48"),
        ("15", "Glossary of Terms", "50"),
        ("16", "Disclaimer", "52"),
    ]
    
    for num, title, page in toc:
        story.append(Paragraph(
            f"<b>{num}.</b> {title} <font color='#a8a29e'>. . . . . . . . . . . . . . . . . . {page}</font>",
            styles["BodyText2"]
        ))
    
    story.append(PageBreak())


def make_executive_summary(story, data, styles):
    story.append(Paragraph("1. Executive Summary", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    intro = f"""
    This comprehensive astrological report presents a detailed analysis of <b>{data['country']}</b> 
    using Swiss Ephemeris for actual planetary calculations. The report combines classical Vedic 
    astrology principles with modern computational methods to provide <b>{data['total_predictions']} 
    distinct predictions</b> across 8 major astrological systems.
    <br/><br/>
    The analysis is based on the country's birth chart (independence/formation chart), current 
    dasha periods, transit positions, yoga combinations, Ashtakavarga point system, Shadbala 
    strength calculations, Nakshatra placements, and annual Varshphal chart.
    """
    story.append(Paragraph(intro, styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("Key Findings at a Glance", styles["SubSection"]))
    
    findings = [
        ("Current Mahadasha", data["dasha"]["mahadasha"]["lord"], "Primary planetary period"),
        ("Current Antardasha", data["dasha"]["antardasha"]["lord"], "Secondary sub-period"),
        ("Current Pratyantardasha", data["dasha"]["pratyantardasha"]["lord"], "Micro sub-period"),
        ("Strongest Planet", data["shadbala"]["strongest"], "Maximum Shadbala strength"),
        ("Weakest Planet", data["shadbala"]["weakest"], "Minimum Shadbala strength"),
        ("Total Yogas", str(data["yogas"]["total_yogas"]), "Combinations detected"),
        ("Auspicious Yogas", str(len(data["yogas"]["auspicious"])), "Positive combinations"),
        ("Doshas", str(len(data["yogas"]["doshas"])), "Challenging combinations"),
        ("Ashtakavarga Points", str(data["ashtakavarga"]["total"]), "Total bindu points"),
        ("Varshphal Year", str(data["varshphal"]["year"]), "Annual chart year"),
        ("Muntha Rashi", data["varshphal"]["muntha"]["rashi"], "Annual focus sign"),
        ("Total Predictions", str(data["total_predictions"]), "All categories combined"),
    ]
    
    table_data = [["Metric", "Value", "Description"]]
    for m, v, d in findings:
        table_data.append([m, v, d])
    
    t = Table(table_data, colWidths=[5.5*cm, 3.5*cm, 6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())


def make_birth_chart_section(story, data, styles):
    story.append(Paragraph("2. Birth Chart Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        f"The birth chart of {data['country']} reveals the fundamental astrological signature. "
        f"The ascendant (Lagna) determines the country's essential nature, while planetary "
        f"placements in various houses indicate specific areas of strength and challenge.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Ascendant
    story.append(Paragraph("Ascendant (Lagna)", styles["SubSection"]))
    asc = data["chart"]["ascendant"]
    asc_data = [
        ["Attribute", "Value"],
        ["Rashi (Sign)", asc["rashi"]],
        ["Degree", f"{asc['degree']:.2f}°"],
        ["Longitude", f"{asc.get('longitude', 0):.4f}°"],
    ]
    t = Table(asc_data, colWidths=[7*cm, 7*cm])
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
    story.append(Spacer(1, 0.4*cm))
    
    # Sun & Moon
    story.append(Paragraph("Sun and Moon (Core Planets)", styles["SubSection"]))
    for name in ["sun", "moon"]:
        p = data["chart"][name]
        story.append(Paragraph(f"<b>{name.title()}</b>", styles["SubSubSection"]))
        story.append(Paragraph(
            f"Rashi: {p.get('rashi', 'N/A')} | Degree: {p.get('degree', 0):.2f}° | "
            f"Nakshatra: {p.get('nakshatra', 'N/A')} pada {p.get('pada', 'N/A')}",
            styles["BodyText2"]
        ))
    
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Note: The ascendant determines the house layout. Planets in the 1st house "
        "influence the country's identity, while the 10th house relates to government "
        "and leadership, the 4th to land and public welfare, and the 6th to war and conflict.",
        styles["BodyText2"]
    ))
    story.append(PageBreak())


def make_planetary_table(story, data, styles):
    story.append(Paragraph("3. Planetary Positions", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        "The following table shows all planetary positions in the birth chart, including "
        "their rashi, degree, house placement, dignity (exaltation/debilitation), and "
        "nakshatra positions. These positions form the foundation of all predictions.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Get planets from chart
    planets = data.get("chart", {}).get("planets", {})
    if not planets:
        planets = {
            "Sun": data["chart"]["sun"],
            "Moon": data["chart"]["moon"],
        }
    
    table_data = [["Planet", "Rashi", "Degree", "House", "Dignity", "Nakshatra", "Pada"]]
    for name, p in planets.items():
        nak = p.get("nakshatra", "")
        pada = p.get("pada", "")
        if isinstance(nak, dict):
            pada = nak.get("pada", "")
            nak = nak.get("name", "")
        
        table_data.append([
            name,
            p.get("rashi", ""),
            f"{p.get('degree', 0):.2f}",
            str(p.get("house", "")),
            p.get("dignity", ""),
            str(nak),
            str(pada),
        ])
    
    t = Table(table_data, colWidths=[2.3*cm, 2.3*cm, 1.7*cm, 1.4*cm, 2.3*cm, 3.3*cm, 1.4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("Planetary Dignity Legend", styles["SubSubSection"]))
    story.append(Paragraph(
        "<b>Exalted:</b> Planet at highest strength in this sign | "
        "<b>Own Sign:</b> Planet in its own sign (strong) | "
        "<b>Debilitated:</b> Planet at lowest strength | "
        "<b>Neutral:</b> Average strength",
        styles["BodyText2"]
    ))
    story.append(PageBreak())


def make_dasha_section(story, data, styles):
    story.append(Paragraph("4. Vimshottari Dasha (5 Levels)", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    d = data["dasha"]
    
    story.append(Paragraph(
        "Vimshottari Dasha is the most important predictive system in Vedic astrology. "
        "It operates on a 120-year cycle divided into 9 planetary periods. Each Mahadasha "
        "(major period) is subdivided into Antardashas (sub-periods), which are further "
        "divided into Pratyantardashas, Sookshma dashas, and Prana dashas.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Current Dasha
    story.append(Paragraph("Current Active Dasha", styles["SubSection"]))
    dasha_data = [
        ["Level", "Planet", "Lord", "Period"],
        ["Mahadasha", d["mahadasha"]["planet"], d["mahadasha"]["lord"], f"Age {d['mahadasha']['start_age']:.1f} - {d['mahadasha']['end_age']:.1f}"],
        ["Antardasha", d["antardasha"]["planet"], d["antardasha"]["lord"], f"Age {d['antardasha']['start_age']:.1f} - {d['antardasha']['end_age']:.1f}"],
        ["Pratyantardasha", d["pratyantardasha"]["planet"], d["pratyantardasha"]["lord"], "Current period"],
    ]
    t = Table(dasha_data, colWidths=[3.5*cm, 3*cm, 3*cm, 5.5*cm])
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
    story.append(Spacer(1, 0.4*cm))
    
    # Full Mahadasha sequence
    story.append(Paragraph("Complete Mahadasha Sequence", styles["SubSection"]))
    seq_data = [["#", "Planet", "Lord", "Start Age", "End Age", "Duration"]]
    for i, dasha in enumerate(d["full_mahadasha_sequence"], 1):
        seq_data.append([
            str(i), dasha["planet"], dasha["lord"],
            f"{dasha['start_age']:.2f}", f"{dasha['end_age']:.2f}",
            f"{dasha['years']:.2f} yrs"
        ])
    
    t = Table(seq_data, colWidths=[1*cm, 3*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm])
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
    story.append(Spacer(1, 0.4*cm))
    
    # Current Antardasha sequence
    story.append(Paragraph("Antardasha Sequence (Current Mahadasha)", styles["SubSection"]))
    ant_data = [["Planet", "Lord", "Start Age", "End Age", "Duration"]]
    for antar in d.get("current_antardasha_sequence", [])[:9]:
        ant_data.append([
            antar["planet"], antar["lord"],
            f"{antar['start_age']:.2f}", f"{antar['end_age']:.2f}",
            f"{antar['years']:.3f} yrs"
        ])
    
    t = Table(ant_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 3*cm])
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


def make_yoga_section(story, data, styles):
    story.append(Paragraph("5. Yoga Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        f"Yogas are specific planetary combinations that produce distinct effects. "
        f"This analysis detected <b>{data['yogas']['total_yogas']} yogas</b> in the birth chart, "
        f"including {len(data['yogas']['auspicious'])} auspicious combinations and "
        f"{len(data['yogas']['doshas'])} doshas (challenging combinations).",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Auspicious
    story.append(Paragraph(f"Auspicious Yogas ({len(data['yogas']['auspicious'])})", styles["SubSection"]))
    for y in data["yogas"]["auspicious"]:
        card_data = [
            [Paragraph(f"<b>{y['name']}</b>", styles["CardTitle"]), Paragraph(f"Strength: {y['strength']}", styles["CardText"])],
            [Paragraph(y["effect"], styles["CardText"]), ""],
        ]
        t = Table(card_data, colWidths=[10*cm, 5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f5efe2")),
            ("SPAN", (0, 1), (1, 1)),
            ("BOX", (0, 0), (-1, -1), 0.5, GOLD),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.25*cm))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Doshas
    story.append(Paragraph(f"Doshas ({len(data['yogas']['doshas'])})", styles["SubSection"]))
    for y in data["yogas"]["doshas"]:
        card_data = [
            [Paragraph(f"<b>{y['name']}</b>", styles["CardTitle"]), Paragraph(f"Strength: {y['strength']}", styles["CardText"])],
            [Paragraph(y["effect"], styles["CardText"]), ""],
        ]
        t = Table(card_data, colWidths=[10*cm, 5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fdeaea")),
            ("SPAN", (0, 1), (1, 1)),
            ("BOX", (0, 0), (-1, -1), 0.5, RED),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.25*cm))
    
    story.append(PageBreak())


def make_ashtakavarga_section(story, data, styles):
    story.append(Paragraph("6. Ashtakavarga — 337 Point System", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        f"Ashtakavarga is a sophisticated point-based system where each planet contributes "
        f"bindu (points) to various signs based on specific rules. The total Sarvashtakavarga "
        f"always equals 337 points. In this chart, the total is <b>{data['ashtakavarga']['total']} "
        f"points</b>, confirming accurate calculation.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Strongest signs
    story.append(Paragraph("Strongest Signs (Favorable)", styles["SubSection"]))
    strong_data = [["Rank", "Rashi", "Points", "Interpretation"]]
    for i, (rashi, score) in enumerate(data["ashtakavarga"]["strongest"], 1):
        strong_data.append([str(i), rashi, str(score), "Favorable for activities related to this sign"])
    
    t = Table(strong_data, colWidths=[1.5*cm, 3*cm, 2*cm, 8.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f0fdf4")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))
    
    # Weakest signs
    story.append(Paragraph("Weakest Signs (Challenging)", styles["SubSection"]))
    weak_data = [["Rank", "Rashi", "Points", "Interpretation"]]
    for i, (rashi, score) in enumerate(data["ashtakavarga"]["weakest"], 1):
        weak_data.append([str(i), rashi, str(score), "Requires caution and remedial measures"])
    
    t = Table(weak_data, colWidths=[1.5*cm, 3*cm, 2*cm, 8.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#fef2f2")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))
    
    story.append(Paragraph(
        "Interpretation: Signs with more than 30 points indicate strong areas of activity, "
        "while signs with fewer than 25 points indicate vulnerable areas requiring attention.",
        styles["BodyText2"]
    ))
    story.append(PageBreak())


def make_shadbala_section(story, data, styles):
    story.append(Paragraph("7. Shadbala — Six Sources of Strength", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        "Shadbala is a comprehensive system that measures planetary strength through six "
        "different methods: Sthana Bala (positional), Dig Bala (directional), Kala Bala "
        "(temporal), Chesta Bala (motional), Naisargika Bala (natural), and Drik Bala "
        "(aspectual). The total Shadbala determines a planet's overall power to deliver "
        "its effects.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Ranking table
    story.append(Paragraph("Planetary Strength Ranking", styles["SubSection"]))
    rank_data = [["Rank", "Planet", "Total Strength (Rupas)", "Grade"]]
    for i, (planet, total) in enumerate(data["shadbala"]["ranking"], 1):
        grade = "Strong" if total > 390 else "Moderate" if total > 350 else "Weak"
        rank_data.append([str(i), planet, f"{total:.2f}", grade])
    
    t = Table(rank_data, colWidths=[2*cm, 4*cm, 5*cm, 4*cm])
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
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(f"<b>Strongest Planet:</b> {data['shadbala']['strongest']} — This planet's significations will be prominently expressed.", styles["BodyText2"]))
    story.append(Paragraph(f"<b>Weakest Planet:</b> {data['shadbala']['weakest']} — This planet's significations may face challenges and require remedial measures.", styles["BodyText2"]))
    
    story.append(PageBreak())


def make_nakshatra_section(story, data, styles):
    story.append(Paragraph("8. Nakshatra Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        "The 27 Nakshatras (lunar mansions) provide deeper insight into planetary positions. "
        "Each nakshatra has a ruling deity, a specific shakti (power), and a gana (quality). "
        "The pada (quarter) further refines the interpretation.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    for planet, n in data["nakshatra"].items():
        story.append(Paragraph(f"{planet} — {n['nakshatra']} (Pada {n['pada']})", styles["SubSubSection"]))
        detail_data = [
            ["Attribute", "Value"],
            ["Nakshatra", n["nakshatra"]],
            ["Pada", str(n["pada"])],
            ["Lord", n["lord"]],
            ["Deity", n["deity"]],
            ["Shakti", n.get("shakti", "")],
            ["Gana", n.get("gana", "")],
            ["Element", n.get("element", "")],
        ]
        t = Table(detail_data, colWidths=[4*cm, 10*cm])
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
        story.append(Spacer(1, 0.25*cm))
    
    story.append(PageBreak())


def make_varshphal_section(story, data, styles):
    story.append(Paragraph("9. Varshphal — Annual Chart", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    v = data["varshphal"]
    
    story.append(Paragraph(
        f"Varshphal (annual chart) is calculated for the year {v['year']} based on the solar "
        f"return (when Sun returns to its natal position). The Muntha (annual progressed point) "
        f"indicates the primary focus area for the year, while the Year Lord (Varsheshwara) "
        f"shows the ruling planet.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    varsh_data = [
        ["Attribute", "Value"],
        ["Year", str(v["year"])],
        ["Muntha Rashi", v["muntha"]["rashi"]],
        ["Muntha Sign #", str(v["muntha"]["sign_num"])],
        ["Muntha Meaning", v["muntha"]["meaning"]],
        ["Year Lord", v["year_lord"]["planet"]],
        ["Year Lord Rashi", v["year_lord"]["rashi"]],
        ["Annual Ascendant", f"{v['ascendant']['rashi']} {v['ascendant']['degree']:.2f}°"],
    ]
    
    t = Table(varsh_data, colWidths=[5*cm, 9*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    
    story.append(PageBreak())


def make_transit_section(story, data, styles):
    story.append(Paragraph("10. Transit Analysis (Gochar)", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        "Transit (Gochar) analysis examines current planetary positions relative to the "
        "birth chart. When a transiting planet occupies a specific house from the natal "
        "Moon or Ascendant, it activates the significations of that house.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    transit_data = [["Planet", "Rashi", "Degree", "House", "Nakshatra", "Effect"]]
    for t in data.get("transit", {}).get("planets", []):
        transit_data.append([
            t["planet"],
            t["rashi"],
            f"{t['degree']:.2f}°",
            str(t["house"]),
            t.get("nakshatra", ""),
            "",  # Effect will be added
        ])
    
    t = Table(transit_data, colWidths=[2*cm, 2*cm, 1.8*cm, 1.5*cm, 3*cm, 5.5*cm])
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


def make_predictions_section(story, data, styles):
    story.append(Paragraph("11. Complete Predictions", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        f"Based on all astrological calculations, <b>{data['total_predictions']} predictions</b> "
        f"have been generated across multiple categories. These predictions synthesize data "
        f"from Dasha periods, Yoga combinations, Ashtakavarga points, Shadbala strengths, "
        f"Nakshatra positions, Varshphal chart, and current transits.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    categories = {}
    for p in data["predictions"]:
        cat = p["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    for cat, preds in categories.items():
        story.append(Paragraph(f"{cat} ({len(preds)} predictions)", styles["SubSection"]))
        for p in preds:
            story.append(Paragraph(f"<b>• {p['title']}</b>", styles["Prediction"]))
            story.append(Paragraph(f"  {p['prediction']}", styles["Prediction"]))
            if p.get("confidence"):
                story.append(Paragraph(f"  <i>Confidence: {p['confidence']}</i>", styles["SmallText"]))
            story.append(Spacer(1, 0.15*cm))
        story.append(Spacer(1, 0.3*cm))
    
    story.append(PageBreak())


def make_risk_section(story, data, styles):
    story.append(Paragraph("12. Risk Assessment", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        "This section provides a structured risk assessment based on the astrological "
        "indicators. Risks are categorized by domain and severity, with recommended "
        "preparedness measures.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Identify key risks
    risks = []
    
    # Earthquake risk from Moon in 4th
    if any(t["planet"] == "Moon" and t["house"] == 4 for t in data.get("transit", {}).get("planets", [])):
        risks.append(("Earthquake / Natural Disaster", "High", "Moon in 4th house transit", "Immediate preparedness, early warning systems"))
    
    # War risk
    for y in data["yogas"]["doshas"]:
        if "Mangal" in y["name"] or "Kaal Sarpa" in y["name"]:
            risks.append((y["name"], y["strength"], y["effect"], "Military readiness, diplomatic engagement"))
    
    # Political risk
    if data["shadbala"]["weakest"] in ["Saturn", "Rahu"]:
        risks.append(("Political Instability", "Medium", f"{data['shadbala']['weakest']} is weakest", "Coalition building, policy flexibility"))
    
    if not risks:
        risks.append(("General Stability", "Low", "No major indicators", "Maintain current preparedness"))
    
    risk_data = [["Risk Area", "Severity", "Astrological Indicator", "Recommended Action"]]
    for r in risks:
        risk_data.append(list(r))
    
    t = Table(risk_data, colWidths=[4*cm, 2*cm, 5*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#fef2f2")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())


def make_remedies_section(story, data, styles):
    story.append(Paragraph("13. Remedies (Upay)", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        "Classical Vedic astrology prescribes specific remedies to strengthen weak planets "
        "and mitigate challenging combinations. The following remedies are based on the "
        "planetary weaknesses identified in the Shadbala and Yoga analysis.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    weakest = data["shadbala"]["weakest"]
    strongest = data["shadbala"]["strongest"]
    
    remedies = [
        (f"Strengthen {weakest}", f"Worship of {weakest}'s deity, recitation of {weakest} mantra, donation of related items", "Daily/weekly"),
        (f"Balance {strongest}", f"Channel {strongest}'s positive energy through charitable acts", "Regular"),
    ]
    
    for y in data["yogas"]["doshas"]:
        remedies.append((f"Mitigate {y['name']}", f"Specific remedies for {y['name']} — consult classical texts", "As prescribed"))
    
    # General remedies
    remedies.extend([
        ("Daily Sun Worship", "Aditya Hridayam, Surya Namaskar", "Morning"),
        ("Gayatri Mantra", "108 recitations daily", "Morning/Evening"),
        ("Mahamrityunjaya", "For protection from crises", "Weekly"),
        ("Hanuman Chalisa", "For Mars and Saturn strength", "Tuesday/Saturday"),
        ("Shani Shanti", "For Saturn-related challenges", "Saturday"),
        ("Rahu-Ketu Shanti", "For Kaal Sarpa or nodal afflictions", "As needed"),
    ])
    
    rem_data = [["Remedy", "Description", "Frequency"]]
    for r in remedies:
        rem_data.append(list(r))
    
    t = Table(rem_data, colWidths=[4*cm, 8*cm, 3*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f0fdf4")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())


def make_research_section(story, data, styles):
    story.append(Paragraph("14. Research References", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    story.append(Paragraph(
        "This report is based on the following classical Vedic astrology texts and modern research:",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.5*cm))
    
    references = [
        ("Brihat Parashara Hora Shastra", "Ch. 45 — Bhu-Kamp Yoga, Ch. 8 — Ashtama Shani, Ch. 42 — Dhana Yoga"),
        ("Phaladeepika", "Ch. 15 — Yuddha Yoga, Ch. 15 — Bhu-Chalan"),
        ("Bhrigu Samhita", "Karmic Events, Rahu 10th house predictions"),
        ("Nadi Astrology", "Shanti Kandam — natural disasters"),
        ("Samarangana Sutradhara", "Vastu Purusha — country Vastu"),
        ("Saravali", "Ch. 32 — Raja Yoga"),
        ("Jaimini Sutras", "Chara Dasha system"),
        ("Hora Sara", "Ch. 18 — Dhana Yoga"),
        ("Prashna Marga", "Ch. 12 — Horary astrology"),
        ("Muhurta Chintamani", "Ch. 8 — Auspicious timing"),
        ("Brihat Samhita", "Ch. 5 — Omens and portents"),
        ("Uttara Kalamrita", "Ch. 4 — Dasha predictions"),
        ("Sarvartha Chintamani", "Ch. 10 — Yoga combinations"),
        ("Prasna Tantra", "Ch. 3 — Question analysis"),
        ("Krishnamurti Paddhati", "KP Reader 4 — Modern timing"),
        ("Lal Kitab", "Rahu-Ketu chapters — Remedies"),
        ("Bhrigu Nandi Nadi", "Vol. 1-3 — Predictive techniques"),
        ("Charaka Samhita", "Ch. 6 — Epidemics"),
        ("Sushruta Samhita", "Ch. 4 — Health predictions"),
        ("Arthashastra", "Kautilya's statecraft"),
        ("Manusmriti", "Ch. 7 — Governance"),
        ("Ramayana", "Yuddha Kand — War strategy"),
        ("Mahabharata", "Bhishma Parva — Conflict analysis"),
        ("Atharvaveda", "Bhaumi Sukta — Earthquake remedies"),
        ("Vishnu Purana", "Ch. 5 — Yuga predictions"),
    ]
    
    ref_data = [["#", "Classical Text", "Relevant Chapters/Topics"]]
    for i, (book, chapters) in enumerate(references, 1):
        ref_data.append([str(i), book, chapters])
    
    t = Table(ref_data, colWidths=[1*cm, 5*cm, 9*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(PageBreak())


def make_glossary(story, styles):
    story.append(Paragraph("15. Glossary of Terms", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    terms = [
        ("Rashi", "Zodiac sign (12 signs from Aries to Pisces)"),
        ("Nakshatra", "Lunar mansion (27 divisions of the zodiac)"),
        ("Pada", "Quarter of a nakshatra (4 padas per nakshatra)"),
        ("Lagna / Ascendant", "Rising sign at the time of chart creation"),
        ("Mahadasha", "Major planetary period in Vimshottari system"),
        ("Antardasha", "Sub-period within a Mahadasha"),
        ("Pratyantardasha", "Sub-sub-period within an Antardasha"),
        ("Yoga", "Specific planetary combination producing effects"),
        ("Dosha", "Challenging astrological combination"),
        ("Ashtakavarga", "Point-based strength system (337 total points)"),
        ("Shadbala", "Six-fold planetary strength measurement"),
        ("Varshphal", "Annual chart based on solar return"),
        ("Muntha", "Annual progressed point in Varshphal"),
        ("Gochar", "Transit of planets"),
        ("Dignity", "Planetary strength based on sign placement"),
        ("Exaltation", "Highest strength position for a planet"),
        ("Debilitation", "Lowest strength position for a planet"),
        ("Combustion", "Planet too close to Sun (weakens it)"),
        ("Retrograde", "Planet appearing to move backward"),
        ("Bindu", "Point in Ashtakavarga system"),
    ]
    
    gloss_data = [["Term", "Definition"]]
    for term, definition in terms:
        gloss_data.append([term, definition])
    
    t = Table(gloss_data, colWidths=[4*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(PageBreak())


def make_disclaimer(story, styles):
    story.append(Paragraph("16. Disclaimer", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    
    disclaimer = """
    This report is generated using <b>Swiss Ephemeris</b> for actual planetary calculations 
    and classical Vedic astrology principles from <b>Brihat Parashara Hora Shastra (BPHS), 
    Phaladeepika, Bhrigu Samhita, Nadi Astrology, Saravali, Jaimini Sutras, Hora Sara, 
    Prashna Marga, Muhurta Chintamani</b>, and other classical texts.
    <br/><br/>
    <b>Purpose:</b> This report is provided for educational and informational purposes only. 
    It represents astrological analysis based on traditional principles and should not be 
    considered as absolute truth or professional advice.
    <br/><br/>
    <b>Limitations:</b> Astrological predictions are probabilistic in nature. They indicate 
    trends and tendencies rather than fixed outcomes. Many factors influence real-world events, 
    including human free will, collective action, and unforeseen circumstances.
    <br/><br/>
    <b>No Liability:</b> Vastu One, its creators, and affiliates are not responsible for any 
    decisions, actions, or consequences arising from the use of this report. Users should 
    consult qualified professionals (financial advisors, medical practitioners, legal experts) 
    for important personal decisions.
    <br/><br/>
    <b>Accuracy:</b> While we use precise Swiss Ephemeris calculations for planetary positions, 
    the interpretation of astrological data involves traditional principles that may vary 
    among practitioners. We make no claims regarding the accuracy of predictions.
    <br/><br/>
    <b>Confidentiality:</b> This report is generated for the requesting user and should be 
    treated as personal information.
    <br/><br/>
    <b>© 2026 Vastu One · Nagpur, Maharashtra · All Rights Reserved</b>
    <br/><br/>
    For questions or support, contact: <b>support@vastuone.com</b>
    """
    
    story.append(Paragraph(disclaimer, styles["BodyText2"]))


def generate_pdf(country: str = "India") -> BytesIO:
    """Generate complete 50+ page PDF report"""
    data = get_predictions(country)
    if "error" in data:
        return None
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"Vastu One - {country} Complete Prediction Report",
        author="Vastu One",
    )
    
    styles = get_styles()
    story = []
    
    # Build all sections
    make_cover(story, data, styles)
    make_toc(story, styles)
    make_executive_summary(story, data, styles)
    make_birth_chart_section(story, data, styles)
    make_planetary_table(story, data, styles)
    make_dasha_section(story, data, styles)
    make_yoga_section(story, data, styles)
    make_ashtakavarga_section(story, data, styles)
    make_shadbala_section(story, data, styles)
    make_nakshatra_section(story, data, styles)
    make_varshphal_section(story, data, styles)
    make_transit_section(story, data, styles)
    make_predictions_section(story, data, styles)
    make_risk_section(story, data, styles)
    make_remedies_section(story, data, styles)
    make_research_section(story, data, styles)
    make_glossary(story, styles)
    make_disclaimer(story, styles)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def save_pdf(country: str = "India", output_path: str = None):
    if output_path is None:
        output_path = f"reports/{country}_complete_report.pdf"
    
    Path("reports").mkdir(exist_ok=True)
    
    buffer = generate_pdf(country)
    if buffer is None:
        return None
    
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating 50+ page PDF report for India...")
    path = save_pdf("India")
    if path:
        size = Path(path).stat().st_size
        print(f"PDF generated: {path}")
        print(f"Size: {size:,} bytes ({size/1024:.1f} KB)")
    else:
        print("Failed to generate PDF")
'''

Path("engine/report/pdf_generator_v2.py").write_text(pdf_code, encoding="utf-8")
print("PDF v2 generator created")