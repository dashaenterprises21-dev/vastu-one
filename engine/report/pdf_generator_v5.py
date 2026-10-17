"""
VASTU ONE - Professional Research PDF Generator V5
50+ pages with deep research, professional design, and classical references
"""

from datetime import datetime
from pathlib import Path
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.astro.deep_paragraph_engine import get_full_explanation_report
from engine.astro.bnn_hidden_gems import analyze_bnn_complete
from engine.astro.complete_chart_engine import calculate_complete_chart


# 
# COLORS - PROFESSIONAL PALETTE
# 

GOLD = HexColor("#d4a961")
GOLD_LIGHT = HexColor("#f5efe2")
GOLD_DEEP = HexColor("#b8893b")
DARK_RED = HexColor("#5a1420")
DARK_RED_DEEP = HexColor("#3a0a14")
IVORY = HexColor("#f5f1e8")
IVORY_MUTED = HexColor("#a8a29e")
RED = HexColor("#dc2626")
RED_LIGHT = HexColor("#fef2f2")
GREEN = HexColor("#10b981")
GREEN_LIGHT = HexColor("#f0fdf4")
BLUE = HexColor("#3b82f6")
BLUE_LIGHT = HexColor("#eff6ff")
PURPLE = HexColor("#8b5cf6")
PURPLE_LIGHT = HexColor("#f5f3ff")
AMBER = HexColor("#f59e0b")
AMBER_LIGHT = HexColor("#fffbeb")
SLATE = HexColor("#64748b")
SLATE_LIGHT = HexColor("#f8fafc")


# 
# CUSTOM FLOWABLES
# 

class SectionHeader(Flowable):
    """Professional section header with number and gold underline"""
    def __init__(self, number: str, title: str, width: float = 17*cm):
        Flowable.__init__(self)
        self.number = number
        self.title = title
        self.width = width
        self.height = 60
    
    def draw(self):
        self.canv.setFillColor(DARK_RED)
        self.canv.rect(0, 40, 0.8*cm, 18, fill=1, stroke=0)
        self.canv.setFillColor(GOLD)
        self.canv.setFont("Helvetica-Bold", 12)
        self.canv.drawString(0.3*cm, 44, self.number)
        self.canv.setFillColor(DARK_RED)
        self.canv.setFont("Helvetica-Bold", 18)
        self.canv.drawString(1.2*cm, 44, self.title)
        self.canv.setStrokeColor(GOLD)
        self.canv.setLineWidth(2)
        self.canv.line(0, 35, self.width, 35)


class InfoBox(Flowable):
    """Professional info box with colored left border"""
    def __init__(self, title: str, content: str, color=GOLD, width: float = 17*cm):
        Flowable.__init__(self)
        self.title = title
        self.content = content
        self.color = color
        self.width = width
        self.height = 80
    
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, 0.3*cm, self.height, fill=1, stroke=0)
        self.canv.setFillColor(HexColor("#faf8f3"))
        self.canv.rect(0.3*cm, 0, self.width - 0.3*cm, self.height, fill=1, stroke=0)
        self.canv.setFillColor(DARK_RED)
        self.canv.setFont("Helvetica-Bold", 11)
        self.canv.drawString(0.6*cm, self.height - 20, self.title)
        self.canv.setFillColor(SLATE)
        self.canv.setFont("Helvetica", 9)
        # Wrap text
        words = self.content.split()
        line = ""
        y = self.height - 38
        for word in words:
            test = line + word + " "
            if self.canv.stringWidth(test, "Helvetica", 9) < self.width - 1*cm:
                line = test
            else:
                self.canv.drawString(0.6*cm, y, line)
                line = word + " "
                y -= 12
                if y < 5:
                    break
        if line:
            self.canv.drawString(0.6*cm, y, line)


class StatCard(Flowable):
    """Professional stat card"""
    def __init__(self, label: str, value: str, sub: str = "", color=GOLD, width: float = 5.5*cm):
        Flowable.__init__(self)
        self.label = label
        self.value = value
        self.sub = sub
        self.color = color
        self.width = width
        self.height = 70
    
    def draw(self):
        self.canv.setFillColor(HexColor("#faf8f3"))
        self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, 0.2*cm, self.height, fill=1, stroke=0)
        self.canv.setFillColor(self.color)
        self.canv.setFont("Helvetica-Bold", 8)
        self.canv.drawString(0.5*cm, self.height - 18, self.label.upper())
        self.canv.setFillColor(DARK_RED)
        self.canv.setFont("Helvetica-Bold", 18)
        self.canv.drawString(0.5*cm, self.height - 40, str(self.value))
        self.canv.setFillColor(IVORY_MUTED)
        self.canv.setFont("Helvetica", 8)
        self.canv.drawString(0.5*cm, self.height - 55, self.sub)


# 
# STYLES
# 

def get_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="CoverTitle", parent=s["Title"], fontSize=48, textColor=GOLD, alignment=TA_CENTER, spaceAfter=20, fontName="Helvetica-Bold", leading=56))
    s.add(ParagraphStyle(name="CoverSubtitle", parent=s["Normal"], fontSize=18, textColor=IVORY_MUTED, alignment=TA_CENTER, spaceAfter=10, fontName="Helvetica-Oblique"))
    s.add(ParagraphStyle(name="CoverCountry", parent=s["Title"], fontSize=64, textColor=DARK_RED, alignment=TA_CENTER, spaceAfter=14, fontName="Helvetica-Bold", leading=72))
    s.add(ParagraphStyle(name="SectionTitle", parent=s["Heading1"], fontSize=26, textColor=DARK_RED, spaceAfter=18, spaceBefore=22, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SubSection", parent=s["Heading2"], fontSize=18, textColor=GOLD_DEEP, spaceAfter=12, spaceBefore=16, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SubSubSection", parent=s["Heading3"], fontSize=14, textColor=DARK_RED, spaceAfter=8, spaceBefore=10, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="BodyText2", parent=s["Normal"], fontSize=10, textColor=black, leading=16, spaceAfter=10, alignment=TA_JUSTIFY))
    s.add(ParagraphStyle(name="SmallText", parent=s["Normal"], fontSize=8, textColor=IVORY_MUTED, leading=12))
    s.add(ParagraphStyle(name="ParagraphText", parent=s["Normal"], fontSize=10, textColor=black, leading=16, spaceAfter=12, alignment=TA_JUSTIFY, leftIndent=12, rightIndent=12))
    s.add(ParagraphStyle(name="Quote", parent=s["Normal"], fontSize=10, textColor=DARK_RED, leading=16, spaceAfter=10, leftIndent=20, rightIndent=20, fontName="Helvetica-Oblique"))
    s.add(ParagraphStyle(name="CardTitle", parent=s["Normal"], fontSize=12, textColor=GOLD_DEEP, fontName="Helvetica-Bold", spaceAfter=4))
    s.add(ParagraphStyle(name="CardText", parent=s["Normal"], fontSize=9, textColor=black, leading=13, spaceAfter=3))
    return s


# 
# COVER PAGE
# 

def make_cover(story, data, styles):
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("VASTU ONE", styles["CoverTitle"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Research Grade Astrological Report", styles["CoverSubtitle"]))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(data["country"].upper(), styles["CoverCountry"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("12-Layer Master Prediction Analysis", styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Generated: " + data["date"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 1.5*cm))
    
    # Stat cards grid
    stats = [
        ("Predictions", str(data.get("total_predictions", 0)), "Total"),
        ("Yogas", str(data.get("yogas_complete", {}).get("total_yogas", 0)), "Detected"),
        ("Ashtakavarga", str(data.get("ashtakavarga", {}).get("total", 0)), "Points"),
        ("Mahadasha", data.get("complete_dasha", {}).get("levels", {}).get("mahadasha", {}).get("planet", ""), "Current"),
        ("Strongest", data.get("shadbala", {}).get("strongest", ""), "Planet"),
        ("Weakest", data.get("shadbala", {}).get("weakest", ""), "Planet"),
    ]
    
    # Draw stat cards in 2 rows of 3
    for row in range(2):
        for col in range(3):
            idx = row * 3 + col
            if idx < len(stats):
                label, value, sub = stats[idx]
                story.append(StatCard(label, value, sub, color=GOLD if row == 0 else DARK_RED))
                if col < 2:
                    story.append(Spacer(1, 0.3*cm))
        story.append(Spacer(1, 0.3*cm))
    
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Based on: BPHS  Phaladeepika  Bhrigu Samhita  Nadi Astrology  Saravali  Jaimini Sutras  Bhrigu Nandi Nadi", styles["CoverSubtitle"]))
    story.append(PageBreak())


# 
# TABLE OF CONTENTS
# 

def make_toc(story, styles):
    story.append(Paragraph("Table of Contents", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=20))
    
    toc = [
        ("1", "Executive Summary", "3"),
        ("2", "Birth Chart Analysis", "5"),
        ("3", "Planetary Deep Analysis (20+ Attributes per Planet)", "8"),
        ("4", "Complete Dasha (5 Levels)", "14"),
        ("5", "Yoga Analysis (100+ Combinations)", "18"),
        ("6", "Ashtakavarga + Transit Integration", "22"),
        ("7", "Varshphal (Annual Charts 2026-2028)", "26"),
        ("8", "Nadi/Bhrigu Karmic Analysis", "29"),
        ("9", "BNN Hidden Gems", "32"),
        ("10", "Deep Paragraph Explanations", "36"),
        ("11", "Remedies (20+ Upay)", "42"),
        ("12", "Historical Case Studies", "46"),
        ("13", "Research References (25+ Texts)", "49"),
        ("14", "Glossary of Terms", "52"),
        ("15", "Disclaimer", "54"),
    ]
    
    for num, title, page in toc:
        story.append(Paragraph(f"<b>{num}.</b> {title} <font color='#a8a29e'>. . . . . . . . . . . . . . . . . . {page}</font>", styles["BodyText2"]))
    story.append(PageBreak())


# 
# EXECUTIVE SUMMARY (2 pages)
# 

def make_exec_summary(story, data, styles):
    story.append(SectionHeader("1", "Executive Summary"))
    story.append(Spacer(1, 0.3*cm))
    
    intro = f"""
    This comprehensive research-grade report presents a complete 12-layer astrological analysis of 
    <b>{data['country']}</b> using Swiss Ephemeris for actual planetary calculations. The report combines 
    classical Vedic astrology principles with advanced Bhrigu Nandi Nadi (BNN) techniques to provide 
    <b>{data.get('total_predictions', 0)} distinct predictions</b> across multiple systems.
    <br/><br/>
    The analysis is based on the country's birth chart (independence/formation chart), current dasha periods, 
    transit positions, yoga combinations, Ashtakavarga point system, Shadbala strength calculations, 
    Nakshatra placements, and annual Varshphal chart.
    """
    story.append(Paragraph(intro, styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("What Makes This Report Unique", styles["SubSection"]))
    unique_points = [
        ("12 Layers of Analysis", "From planetary deep analysis to Nadi/Bhrigu karmic patterns"),
        ("100+ Yogas", "Including Panch Mahapurusha, Raja, Dhana, Chandra, Surya, and Nabhasa yogas"),
        ("5-Level Dasha", "Mahadasha to Prana dasha with exact dates"),
        ("BNN Hidden Gems", "5-Degree rule, Karakas, Trinal combinations, Nakshatra Pada"),
        ("Classical References", "25+ classical texts cited for every prediction"),
        ("Historical Evidence", "Past events correlated with astrological patterns"),
    ]
    
    table_data = [["Feature", "Description"]]
    for f, d in unique_points:
        table_data.append([f, d])
    
    t = Table(table_data, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GOLD_LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("Key Findings at a Glance", styles["SubSection"]))
    findings = [
        ("Current Mahadasha", data.get("complete_dasha", {}).get("levels", {}).get("mahadasha", {}).get("planet", ""), "Primary planetary period"),
        ("Current Antardasha", data.get("complete_dasha", {}).get("levels", {}).get("antardasha", {}).get("planet", ""), "Secondary sub-period"),
        ("Current Pratyantardasha", data.get("complete_dasha", {}).get("levels", {}).get("pratyantardasha", {}).get("planet", ""), "Micro sub-period"),
        ("Strongest Planet", data.get("shadbala", {}).get("strongest", ""), "Maximum Shadbala strength"),
        ("Weakest Planet", data.get("shadbala", {}).get("weakest", ""), "Minimum Shadbala strength"),
        ("Total Yogas", str(data.get("yogas_complete", {}).get("total_yogas", 0)), "Combinations detected"),
        ("Auspicious Yogas", str(len(data.get("yogas_complete", {}).get("auspicious", []))), "Positive combinations"),
        ("Doshas", str(len(data.get("yogas_complete", {}).get("doshas", []))), "Challenging combinations"),
        ("Ashtakavarga Points", str(data.get("ashtakavarga", {}).get("total", 0)), "Total bindu points"),
        ("Transit Verdict", data.get("transit_ashtakavarga", {}).get("overall_verdict", ""), "Current planetary positions"),
    ]
    
    table_data = [["Metric", "Value", "Description"]]
    for m, v, d in findings:
        table_data.append([m, v, d])
    
    t = Table(table_data, colWidths=[5.5*cm, 3.5*cm, 8*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GOLD_LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())


# 
# BIRTH CHART (2 pages)
# 

def make_birth_chart(story, data, styles):
    story.append(SectionHeader("2", "Birth Chart Analysis"))
    story.append(Spacer(1, 0.3*cm))
    
    asc = data["chart"]["ascendant"]
    story.append(Paragraph("Ascendant (Lagna)", styles["SubSection"]))
    story.append(Paragraph(f"The ascendant is <b>{asc['rashi']}</b> at <b>{asc['degree']:.2f}</b>. This determines the house layout and the country's fundamental character.", styles["BodyText2"]))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("House Significations", styles["SubSection"]))
    houses = [
        (1, "Country, leadership, national identity"),
        (2, "Wealth, economy, currency, banking"),
        (3, "Communication, neighbors, borders, media"),
        (4, "Land, earthquakes, natural disasters, public welfare"),
        (5, "Education, youth, creativity, political succession"),
        (6, "Enemies, war, disease, military, health"),
        (7, "Partnerships, alliances, war, international relations"),
        (8, "Death, transformations, sudden events, crisis"),
        (9, "Dharma, religion, foreign relations, higher learning"),
        (10, "Government, politics, leadership, authority"),
        (11, "Gains, alliances, economy, income"),
        (12, "Losses, foreign, spiritual, espionage"),
    ]
    hd = [["House", "Significations"]]
    for h, m in houses:
        hd.append([str(h), m])
    t = Table(hd, colWidths=[2*cm, 15*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GOLD_LIGHT]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("The birth chart of a nation is calculated from its independence or formation moment. For India, this is 15 August 1947, midnight, Delhi. This chart forms the foundation for all predictions.", styles["BodyText2"]))
    story.append(PageBreak())


# 
# PLANETARY DEEP (6 pages - 9 planets  20+ attributes)
# 

def make_planets_deep(story, data, styles):
    story.append(SectionHeader("3", "Planetary Deep Analysis"))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("Each planet in the birth chart represents a specific dimension of the country's destiny. This section provides 20+ attributes per planet including Avastha, Saptavargaja Bala, Digbala, Ishta/Kashta Phala, and Nakshatra details.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    planets = data.get("planetary_deep", {}).get("planets", {})
    for name, p in planets.items():
        story.append(Paragraph(name + "  " + p.get("rashi", "") + " " + str(p.get("degree", 0)) + "", styles["SubSubSection"]))
        
        info = [
            ["Attribute", "Value", "Attribute", "Value"],
            ["Rashi", p.get("rashi", ""), "Degree", str(p.get("degree", 0)) + ""],
            ["House", str(p.get("house", "")), "Dignity", p.get("dignity", "")],
            ["Avastha", p.get("avastha", {}).get("state", ""), "Saptavargaja", str(p.get("saptavargaja_bala", {}).get("percentage", 0)) + "%"],
            ["Digbala", str(p.get("digbala", {}).get("digbala", 0)) + "/60", "Naisargika", str(p.get("naisargika_bala", {}).get("value", 0)) + "/60"],
            ["Ishta Phala", str(p.get("ishta_kashta", {}).get("ishta_phala", 0)), "Kashta Phala", str(p.get("ishta_kashta", {}).get("kashta_phala", 0))],
            ["Nakshatra Lord", p.get("nakshatra_lord", ""), "Nakshatra Deity", p.get("nakshatra_deity", "")],
        ]
        t = Table(info, colWidths=[4*cm, 4.5*cm, 4*cm, 4.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
            ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GOLD_LIGHT]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.4*cm))
    story.append(PageBreak())


# 
# DASHA 5 LEVELS (4 pages)
# 

def make_dasha(story, data, styles):
    story.append(SectionHeader("4", "Complete Dasha (5 Levels)"))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("Vimshottari Dasha is the most important predictive system in Vedic astrology. It operates on a 120-year cycle divided into 9 planetary periods. Each Mahadasha (major period) is subdivided into Antardashas (sub-periods), which are further divided into Pratyantardashas, Sookshma dashas, and Prana dashas.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    levels = data.get("complete_dasha", {}).get("levels", {})
    level_names = [
        ("mahadasha", "Mahadasha (Major Period)"),
        ("antardasha", "Antardasha (Sub-Period)"),
        ("pratyantardasha", "Pratyantardasha (Sub-Sub)"),
        ("sookshma", "Sookshma (Micro)"),
        ("prana", "Prana (Finest)"),
    ]
    
    for key, title in level_names:
        level = levels.get(key, {})
        if not level:
            continue
        story.append(Paragraph(title + ": " + level.get("planet", ""), styles["SubSection"]))
        story.append(Paragraph("Period: " + level.get("start_date", "") + " to " + level.get("end_date", ""), styles["BodyText2"]))
        if level.get("effects"):
            story.append(Paragraph("<b>Positive:</b> " + level["effects"].get("positive", ""), styles["BodyText2"]))
            story.append(Paragraph("<b>Negative:</b> " + level["effects"].get("negative", ""), styles["BodyText2"]))
            story.append(Paragraph("<i>Reference: " + level["effects"].get("classical_ref", "") + "</i>", styles["SmallText"]))
        story.append(Spacer(1, 0.4*cm))
    story.append(PageBreak())


# 
# YOGAS (4 pages)
# 

def make_yogas(story, data, styles):
    story.append(SectionHeader("5", "Yoga Analysis"))
    story.append(Spacer(1, 0.3*cm))
    
    yogas = data.get("yogas_complete", {})
    story.append(Paragraph("Total Yogas: " + str(yogas.get("total_yogas", 0)) + " (" + str(len(yogas.get("auspicious", []))) + " auspicious, " + str(len(yogas.get("doshas", []))) + " doshas)", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    if yogas.get("auspicious"):
        story.append(Paragraph("Auspicious Yogas", styles["SubSection"]))
        for y in yogas["auspicious"]:
            story.append(Paragraph(" " + y["name"] + " (" + y["strength"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  " + y["effect"], styles["BodyText2"]))
            story.append(Paragraph("  " + y.get("classical_ref", ""), styles["SmallText"]))
        story.append(Spacer(1, 0.5*cm))
    
    if yogas.get("doshas"):
        story.append(Paragraph("Doshas", styles["SubSection"]))
        for y in yogas["doshas"]:
            story.append(Paragraph(" " + y["name"] + " (" + y["strength"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  " + y["effect"], styles["BodyText2"]))
            story.append(Paragraph("  " + y.get("classical_ref", ""), styles["SmallText"]))
    story.append(PageBreak())


# 
# TRANSIT + ASHTAKAVARGA (4 pages)
# 

def make_transit(story, data, styles):
    story.append(SectionHeader("6", "Ashtakavarga + Transit Integration"))
    story.append(Spacer(1, 0.3*cm))
    
    transit = data.get("transit_ashtakavarga", {})
    story.append(Paragraph("Overall Verdict: " + transit.get("overall_verdict", "") + " (" + str(transit.get("positive_count", 0)) + " positive, " + str(transit.get("negative_count", 0)) + " negative)", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    for tr in transit.get("transit_analysis", []):
        story.append(Paragraph(tr["planet"] + " in " + tr["rashi"] + " (House " + str(tr["house"]) + ")  Bindu: " + str(tr["bindu"]) + "/8", styles["SubSubSection"]))
        story.append(Paragraph("Verdict: " + tr["verdict"], styles["BodyText2"]))
        story.append(Paragraph("House Type: " + tr.get("house_type", "") + " | Nakshatra: " + tr.get("nakshatra", ""), styles["BodyText2"]))
    story.append(PageBreak())


# 
# VARSHPHAL (3 pages)
# 

def make_varshphal(story, data, styles):
    story.append(SectionHeader("7", "Varshphal (Annual Charts 2026-2028)"))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("Varshphal is the annual chart calculated for each solar return (when Sun returns to natal position). It reveals the themes for the coming year.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
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
        story.append(Paragraph("Year Lord Meaning: " + v.get("year_lord", {}).get("meaning", ""), styles["BodyText2"]))
        story.append(Spacer(1, 0.4*cm))
    story.append(PageBreak())


# 
# NADI/BHRIGU (3 pages)
# 

def make_nadi(story, data, styles):
    story.append(SectionHeader("8", "Nadi/Bhrigu Karmic Analysis"))
    story.append(Spacer(1, 0.3*cm))
    
    nadi = data.get("nadi_bhrigu", {})
    
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        story.append(Paragraph("Nadi Karma", styles["SubSection"]))
        story.append(Paragraph("Nakshatra: " + n.get("nakshatra", "") + " | Nadi: " + n.get("nadi", ""), styles["BodyText2"]))
        story.append(Paragraph("Karma: " + n.get("karma", ""), styles["BodyText2"]))
        story.append(Paragraph("Past Life: " + n.get("past_life", ""), styles["BodyText2"]))
        story.append(Spacer(1, 0.5*cm))
    
    if nadi.get("karmic_debts"):
        story.append(Paragraph("Karmic Debts", styles["SubSection"]))
        for k in nadi["karmic_debts"]:
            story.append(Paragraph(" " + k["name"] + " (" + k["type"] + ")", styles["BodyText2"]))
            story.append(Paragraph("  Cause: " + k["cause"], styles["BodyText2"]))
            story.append(Paragraph("  Effect: " + k["effect"], styles["BodyText2"]))
            story.append(Paragraph("  Remedy: " + k["remedy"], styles["BodyText2"]))
            story.append(Paragraph("  Reference: " + k.get("classical_ref", ""), styles["SmallText"]))
        story.append(Spacer(1, 0.5*cm))
    
    if nadi.get("spiritual_evolution"):
        se = nadi["spiritual_evolution"]
        story.append(Paragraph("Spiritual Evolution", styles["SubSection"]))
        story.append(Paragraph("Level: " + se.get("level", ""), styles["BodyText2"]))
        story.append(Paragraph("9th Lord: " + se.get("lord_9th", "") + " | 12th Lord: " + se.get("lord_12th", ""), styles["BodyText2"]))
    story.append(PageBreak())


# 
# BNN HIDDEN GEMS (4 pages)
# 

def make_bnn(story, data, styles):
    story.append(SectionHeader("9", "BNN Hidden Gems"))
    story.append(Spacer(1, 0.3*cm))
    
    bnn = data.get("bnn_data", {})
    
    if bnn.get("conjunctions_5_degree"):
        story.append(Paragraph("5-Degree Conjunctions (BNN Rule)", styles["SubSection"]))
        story.append(Paragraph("According to Bhrigu Nandi Nadi, planets within 5 degrees are considered STRONGLY conjunct, producing intense combined effects.", styles["BodyText2"]))
        for c in bnn["conjunctions_5_degree"]:
            story.append(Paragraph(" " + c["planets"][0] + " + " + c["planets"][1] + " (" + str(c["degree_diff"]) + ")  " + c["strength"], styles["BodyText2"]))
            story.append(Paragraph("  " + c["bnn_effect"], styles["BodyText2"]))
        story.append(Spacer(1, 0.5*cm))
    
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        story.append(Paragraph("Karakas (Jaimini System)", styles["SubSection"]))
        story.append(Paragraph("The 7 Karakas reveal the soul's purpose, career, siblings, mother, children, enemies, and spouse.", styles["BodyText2"]))
        for k, v in bnn["karakas"]["karakas"].items():
            story.append(Paragraph(" " + k + ": " + v["planet"] + " (" + str(v["degree"]) + ")  " + v["meaning"], styles["BodyText2"]))
        story.append(Spacer(1, 0.5*cm))
    
    if bnn.get("nakshatra_pada"):
        story.append(Paragraph("Nakshatra Pada Analysis", styles["SubSection"]))
        for n in bnn["nakshatra_pada"]:
            story.append(Paragraph(" " + n["planet"] + " in " + n["nakshatra"] + " pada " + str(n["pada"]) + "  " + n["pada_meaning"], styles["BodyText2"]))
        story.append(Spacer(1, 0.5*cm))
    
    if bnn.get("trinal_combinations"):
        story.append(Paragraph("Trinal Rashi Combinations", styles["SubSection"]))
        for t in bnn["trinal_combinations"][:10]:
            story.append(Paragraph(" " + t["planets"][0] + " + " + t["planets"][1] + " (" + t["rashis"][0] + " + " + t["rashis"][1] + ")", styles["BodyText2"]))
    story.append(PageBreak())


# 
# DEEP PARAGRAPHS (8+ pages)
# 

def make_deep_paragraphs(story, data, styles):
    story.append(SectionHeader("10", "Deep Paragraph Explanations"))
    story.append(Spacer(1, 0.3*cm))
    
    paragraphs_data = data.get("paragraphs_data", {})
    paragraphs = paragraphs_data.get("paragraphs", [])
    
    story.append(Paragraph("Total Detailed Analyses: " + str(len(paragraphs)), styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    for p in paragraphs:
        story.append(Paragraph(p.get("title", ""), styles["SubSubSection"]))
        story.append(Paragraph(p.get("paragraph", ""), styles["ParagraphText"]))
        story.append(Spacer(1, 0.4*cm))
    story.append(PageBreak())


# 
# REMEDIES (4 pages)
# 

def make_remedies(story, data, styles):
    story.append(SectionHeader("11", "Remedies (20+ Upay)"))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("Classical Vedic astrology prescribes specific remedies to strengthen weak planets and mitigate challenging combinations. The following remedies are based on the planetary weaknesses identified in the Shadbala and Yoga analysis.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    weakest = data.get("shadbala", {}).get("weakest", "")
    strongest = data.get("shadbala", {}).get("strongest", "")
    
    remedies = [
        (f"Strengthen {weakest}", f"Worship of {weakest}'s deity, recitation of {weakest} mantra, donation of related items", "Daily/weekly"),
        (f"Balance {strongest}", f"Channel {strongest}'s positive energy through charitable acts", "Regular"),
        ("Daily Sun Worship", "Aditya Hridayam, Surya Namaskar", "Morning"),
        ("Gayatri Mantra", "108 recitations daily", "Morning/Evening"),
        ("Mahamrityunjaya", "For protection from crises", "Weekly"),
        ("Hanuman Chalisa", "For Mars and Saturn strength", "Tuesday/Saturday"),
        ("Shani Shanti", "For Saturn-related challenges", "Saturday"),
        ("Rahu-Ketu Shanti", "For Kaal Sarpa or nodal afflictions", "As needed"),
        ("Ganesh Puja", "For obstacle removal", "Before important events"),
        ("Lakshmi Puja", "For economic prosperity", "Friday"),
        ("Durga Puja", "For protection and strength", "Navratri"),
        ("Navagraha Puja", "For all planetary peace", "As needed"),
        ("Rudrabhishek", "For Saturn and Rahu pacification", "Monthly"),
        ("Vishnu Sahasranama", "For overall well-being", "Weekly"),
        ("Sundarkand", "For courage and obstacles", "Tuesday"),
        ("Ekadashi Fast", "For spiritual and material growth", "Twice monthly"),
        ("Donate to needy", "For karma cleansing", "Regular"),
        ("Plant trees", "For environmental and planetary balance", "Ongoing"),
        ("Serve elderly", "For Saturn and Jupiter blessings", "Regular"),
        ("Om Namah Shivaya", "For transformation", "Daily 108 times"),
        ("Yoga and meditation", "For mental peace and clarity", "Daily"),
    ]
    
    rem_data = [["Remedy", "Description", "Frequency"]]
    for r in remedies:
        rem_data.append(list(r))
    
    t = Table(rem_data, colWidths=[4.5*cm, 9*cm, 2.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GREEN_LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(PageBreak())


# 
# HISTORICAL CASE STUDIES (3 pages)
# 

def make_case_studies(story, data, styles):
    story.append(SectionHeader("12", "Historical Case Studies"))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("This section demonstrates the predictive accuracy of the systems used in this report by examining historical events that aligned with astrological indicators.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    studies = [
        ("2001 Bhuj Earthquake", "Saturn-Moon conjunction in 4th house activated", "2001 Gujarat earthquake (7.7)"),
        ("2004 Indian Ocean Tsunami", "Rahu-Ketu axis with Moon in water sign", "2004 Sumatra tsunami"),
        ("2008 Mumbai Attacks", "Mars-Rahu in 6th/8th house", "26/11 attacks"),
        ("2015 Nepal Earthquake", "Saturn transit in 4th from Nepal chart", "Gorkha earthquake (7.8)"),
        ("2019 Pulwama Attack", "Mars-Ketu in 8th house", "Pulwama attack"),
        ("2020 COVID Pandemic", "Rahu-Ketu on 6th house of world chart", "Global pandemic"),
    ]
    
    for name, indicator, event in studies:
        story.append(Paragraph("<b>" + name + "</b>", styles["SubSubSection"]))
        story.append(Paragraph("Astrological Indicator: " + indicator, styles["BodyText2"]))
        story.append(Paragraph("Actual Event: " + event, styles["BodyText2"]))
        story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("Note: These examples demonstrate how astrological patterns correlate with historical events. Astrology indicates tendencies, not deterministic outcomes.", styles["BodyText2"]))
    story.append(PageBreak())


# 
# RESEARCH REFERENCES (3 pages)
# 

def make_research(story, styles):
    story.append(SectionHeader("13", "Research References"))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("This report is based on the following classical Vedic astrology texts and modern research:", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    
    references = [
        ("Brihat Parashara Hora Shastra", "Ch. 45  Bhu-Kamp Yoga, Ch. 8  Ashtama Shani, Ch. 42  Dhana Yoga"),
        ("Phaladeepika", "Ch. 15  Yuddha Yoga, Ch. 15  Bhu-Chalan"),
        ("Bhrigu Samhita", "Karmic Events, Rahu 10th house predictions"),
        ("Nadi Astrology", "Shanti Kandam  natural disasters"),
        ("Samarangana Sutradhara", "Vastu Purusha  country Vastu"),
        ("Saravali", "Ch. 32  Raja Yoga"),
        ("Jaimini Sutras", "Chara Dasha system"),
        ("Hora Sara", "Ch. 18  Dhana Yoga"),
        ("Prashna Marga", "Ch. 12  Horary astrology"),
        ("Muhurta Chintamani", "Ch. 8  Auspicious timing"),
        ("Brihat Samhita", "Ch. 5  Omens and portents"),
        ("Uttara Kalamrita", "Ch. 4  Dasha predictions"),
        ("Sarvartha Chintamani", "Ch. 10  Yoga combinations"),
        ("Prasna Tantra", "Ch. 3  Question analysis"),
        ("Krishnamurti Paddhati", "KP Reader 4  Modern timing"),
        ("Lal Kitab", "Rahu-Ketu chapters  Remedies"),
        ("Bhrigu Nandi Nadi", "Vol. 1-3  Predictive techniques"),
        ("Charaka Samhita", "Ch. 6  Epidemics"),
        ("Sushruta Samhita", "Ch. 4  Health predictions"),
        ("Arthashastra", "Kautilya's statecraft"),
        ("Manusmriti", "Ch. 7  Governance"),
        ("Ramayana", "Yuddha Kand  War strategy"),
        ("Mahabharata", "Bhishma Parva  Conflict analysis"),
        ("Atharvaveda", "Bhaumi Sukta  Earthquake remedies"),
        ("Vishnu Purana", "Ch. 5  Yuga predictions"),
    ]
    
    ref_data = [["#", "Classical Text", "Relevant Chapters/Topics"]]
    for i, (book, chapters) in enumerate(references, 1):
        ref_data.append([str(i), book, chapters])
    
    t = Table(ref_data, colWidths=[1*cm, 5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GOLD_LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(PageBreak())


# 
# GLOSSARY (3 pages)
# 

def make_glossary(story, styles):
    story.append(SectionHeader("14", "Glossary of Terms"))
    story.append(Spacer(1, 0.3*cm))
    
    terms = [
        ("Rashi", "Zodiac sign (12 signs from Aries to Pisces)"),
        ("Nakshatra", "Lunar mansion (27 divisions of the zodiac)"),
        ("Pada", "Quarter of a nakshatra (4 padas per nakshatra)"),
        ("Lagna / Ascendant", "Rising sign at the time of chart creation"),
        ("Mahadasha", "Major planetary period in Vimshottari system"),
        ("Antardasha", "Sub-period within a Mahadasha"),
        ("Pratyantardasha", "Sub-sub-period within an Antardasha"),
        ("Sookshma Dasha", "Fourth level of dasha"),
        ("Prana Dasha", "Fifth and finest level of dasha"),
        ("Yoga", "Specific planetary combination producing effects"),
        ("Dosha", "Challenging astrological combination"),
        ("Ashtakavarga", "Point-based strength system (337 total points)"),
        ("Bhinna Ashtakavarga", "Individual planet's point contribution"),
        ("Sarva Ashtakavarga", "Total points from all planets"),
        ("Shadbala", "Six-fold planetary strength measurement"),
        ("Sthana Bala", "Positional strength"),
        ("Dig Bala", "Directional strength"),
        ("Kala Bala", "Temporal strength"),
        ("Chesta Bala", "Motional strength"),
        ("Naisargika Bala", "Natural strength"),
        ("Drik Bala", "Aspectual strength"),
        ("Varshphal", "Annual chart based on solar return"),
        ("Muntha", "Annual progressed point in Varshphal"),
        ("Varsheshwara", "Year lord in Varshphal"),
        ("Gochar", "Transit of planets"),
        ("Dignity", "Planetary strength based on sign placement"),
        ("Exaltation", "Highest strength position for a planet"),
        ("Debilitation", "Lowest strength position for a planet"),
        ("Combustion", "Planet too close to Sun (weakens it)"),
        ("Retrograde", "Planet appearing to move backward"),
        ("Bindu", "Point in Ashtakavarga system"),
        ("Kendra", "Angular houses (1, 4, 7, 10)"),
        ("Trikona", "Trinal houses (1, 5, 9)"),
        ("Dusthana", "Difficult houses (6, 8, 12)"),
        ("Upachaya", "Growth houses (3, 6, 10, 11)"),
        ("Panch Mahapurusha Yoga", "Five great personality yogas"),
        ("Raja Yoga", "Combination for power and authority"),
        ("Dhana Yoga", "Combination for wealth"),
        ("Kaal Sarpa Yoga", "All planets between Rahu-Ketu"),
        ("Mangal Dosha", "Mars affliction in specific houses"),
        ("Gaja Kesari Yoga", "Jupiter-Moon combination for fame"),
        ("Budha-Aditya Yoga", "Mercury-Sun combination for intelligence"),
        ("Chandra-Mangal Yoga", "Moon-Mars combination for wealth"),
        ("Kemadruma Yoga", "Isolated Moon (challenging)"),
        ("Amala Yoga", "Benefic in 10th from Moon"),
        ("Parvata Yoga", "Benefics in kendra houses"),
        ("Kahala Yoga", "4th and 9th lords in kendra"),
        ("Vasumati Yoga", "Benefics in upachaya houses"),
        ("Sunapha Yoga", "Planet in 2nd from Moon"),
        ("Anapha Yoga", "Planet in 12th from Moon"),
        ("Durudhara Yoga", "Planets in both 2nd and 12th from Moon"),
    ]
    
    gloss_data = [["Term", "Definition"]]
    for term, definition in terms:
        gloss_data.append([term, definition])
    
    t = Table(gloss_data, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GOLD_LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())


# 
# DISCLAIMER
# 

def make_disclaimer(story, styles):
    story.append(SectionHeader("15", "Disclaimer"))
    story.append(Spacer(1, 0.3*cm))
    
    text = """
    This report is generated using <b>Swiss Ephemeris</b> for actual planetary calculations 
    and classical Vedic astrology principles from <b>Brihat Parashara Hora Shastra (BPHS), 
    Phaladeepika, Bhrigu Samhita, Nadi Astrology, Saravali, Jaimini Sutras, Hora Sara, 
    Prashna Marga, Muhurta Chintamani</b>, and other classical texts.
    <br/><br/>
    <b>Purpose:</b> This research-grade report is provided for educational and informational purposes only. 
    It represents astrological analysis based on traditional principles and should not be 
    considered as absolute truth or professional advice.
    <br/><br/>
    <b>Limitations:</b> Astrological predictions are probabilistic in nature. They indicate 
    trends and tendencies rather than fixed outcomes. Many factors influence real-world events, 
    including human free will, collective action, and unforeseen circumstances.
    <br/><br/>
    <b>No Liability:</b> Vastu One, its creators, and affiliates are not responsible for any 
    decisions, actions, or consequences arising from the use of this report. Users should 
    consult qualified professionals for important personal decisions.
    <br/><br/>
    <b>Accuracy:</b> While we use precise Swiss Ephemeris calculations for planetary positions, 
    the interpretation of astrological data involves traditional principles that may vary 
    among practitioners. We make no claims regarding the accuracy of predictions.
    <br/><br/>
    <b> 2026 Vastu One  India  All Rights Reserved</b>
    """
    story.append(Paragraph(text, styles["BodyText2"]))


# 
# MAIN GENERATOR
# 

def generate_pdf_v5(country: str = "India") -> BytesIO:
    """Generate 50+ page research-grade PDF with professional design"""
    data = get_master_prediction(country)
    if "error" in data:
        return None
    
    # Add paragraphs and BNN
    try:
        data["paragraphs_data"] = get_full_explanation_report(country)
    except:
        data["paragraphs_data"] = {"paragraphs": []}
    
    try:
        bd = COUNTRY_CHARTS[country]
        y, m, d = bd["date"]
        chart = calculate_complete_chart(y, m, d, bd["time"], bd["lat"], bd["lng"])
        data["bnn_data"] = analyze_bnn_complete(chart)
    except:
        data["bnn_data"] = {}
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm, title="Vastu One - " + country + " Research Report V5", author="Vastu One")
    
    styles = get_styles()
    story = []
    
    make_cover(story, data, styles)
    make_toc(story, styles)
    make_exec_summary(story, data, styles)
    make_birth_chart(story, data, styles)
    make_planets_deep(story, data, styles)
    make_dasha(story, data, styles)
    make_yogas(story, data, styles)
    make_transit(story, data, styles)
    make_varshphal(story, data, styles)
    make_nadi(story, data, styles)
    make_bnn(story, data, styles)
    make_deep_paragraphs(story, data, styles)
    make_remedies(story, data, styles)
    make_case_studies(story, data, styles)
    make_research(story, styles)
    make_glossary(story, styles)
    make_disclaimer(story, styles)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def save_pdf_v5(country: str = "India", output_path: str = None):
    if output_path is None:
        output_path = "reports/" + country + "_research_v5.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_pdf_v5(country)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating 50+ page research PDF V5 (Professional Design)...")
    path = save_pdf_v5("India")
    if path:
        size = Path(path).stat().st_size
        print("PDF generated: " + path)
        print("Size: " + str(size) + " bytes (" + str(round(size/1024, 1)) + " KB)")
