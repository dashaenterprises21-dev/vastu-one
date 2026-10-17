"""
VASTU ONE - PDF Report Generator V3
60+ page comprehensive report
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

from engine.astro.predictions_engine import get_predictions
from engine.astro.deep_paragraph_engine import get_full_explanation_report
from engine.astro.bnn_hidden_gems import analyze_bnn_complete
from engine.astro.complete_chart_engine import calculate_complete_chart
from engine.astro.complete_chart_engine import RASHI_LORDS


GOLD = HexColor("#d4a961")
GOLD_DEEP = HexColor("#b8893b")
DARK_RED = HexColor("#5a1420")
IVORY_MUTED = HexColor("#a8a29e")
RED = HexColor("#dc2626")
GREEN = HexColor("#10b981")


def get_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="CoverTitle", parent=s["Title"], fontSize=44, textColor=GOLD, alignment=TA_CENTER, spaceAfter=24, fontName="Helvetica-Bold", leading=52))
    s.add(ParagraphStyle(name="CoverSubtitle", parent=s["Normal"], fontSize=18, textColor=IVORY_MUTED, alignment=TA_CENTER, spaceAfter=12, fontName="Helvetica-Oblique"))
    s.add(ParagraphStyle(name="CoverCountry", parent=s["Title"], fontSize=60, textColor=DARK_RED, alignment=TA_CENTER, spaceAfter=16, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SectionTitle", parent=s["Heading1"], fontSize=28, textColor=DARK_RED, spaceAfter=20, spaceBefore=24, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SubSection", parent=s["Heading2"], fontSize=18, textColor=GOLD_DEEP, spaceAfter=12, spaceBefore=16, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="SubSubSection", parent=s["Heading3"], fontSize=14, textColor=DARK_RED, spaceAfter=8, spaceBefore=10, fontName="Helvetica-Bold"))
    s.add(ParagraphStyle(name="BodyText2", parent=s["Normal"], fontSize=11, textColor=black, leading=17, spaceAfter=10, alignment=TA_JUSTIFY))
    s.add(ParagraphStyle(name="SmallText", parent=s["Normal"], fontSize=9, textColor=IVORY_MUTED, leading=13))
    s.add(ParagraphStyle(name="Prediction", parent=s["Normal"], fontSize=11, textColor=black, leading=15, spaceAfter=8, leftIndent=14))
    s.add(ParagraphStyle(name="Quote", parent=s["Normal"], fontSize=11, textColor=DARK_RED, leading=17, spaceAfter=10, leftIndent=20, rightIndent=20, fontName="Helvetica-Oblique"))
    return s


def _dasha_meaning(p):
    m = {"Sun": "leadership, authority, government", "Moon": "public emotions, water, mass movements", "Mars": "military action, conflict, courage", "Mercury": "diplomacy, communication, trade", "Jupiter": "growth, wisdom, prosperity, spirituality", "Venus": "luxury, arts, diplomacy", "Saturn": "discipline, delays, structural change", "Rahu": "sudden change, transformation, foreign", "Ketu": "spirituality, isolation, sudden events"}
    return m.get(p, "general effects")


def _rashi_meaning(r):
    m = {"Mesh": "leadership, military, initiative", "Vrishabh": "economy, wealth, stability", "Mithun": "communication, media, diplomacy", "Kark": "land, earthquake, public welfare", "Simha": "government, authority, leadership", "Kanya": "analysis, service, health", "Tula": "diplomacy, alliances, trade", "Vrishchik": "crisis, transformation, secrets", "Dhanu": "religion, foreign, law", "Makar": "governance, structure, discipline", "Kumbh": "technology, innovation, masses", "Meen": "spirituality, foreign, compassion"}
    return m.get(r, "general")


def _planet_meaning(p):
    m = {"Sun": "leadership, authority, government", "Moon": "public, emotions, water", "Mars": "military, aggression, courage", "Mercury": "communication, trade, diplomacy", "Jupiter": "wisdom, growth, prosperity", "Venus": "luxury, diplomacy, arts", "Saturn": "discipline, delays, structures", "Rahu": "transformation, foreign, sudden change", "Ketu": "spirituality, isolation, sudden events"}
    return m.get(p, "general")


def make_cover(story, data, styles):
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("VASTU ONE", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Swiss Ephemeris  |  Classical Vedic Astrology", styles["CoverSubtitle"]))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(data["country"].upper(), styles["CoverCountry"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Complete Astrological Analysis Report", styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Generated: " + data["date"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 3*cm))
    summary = [["Metric", "Value"], ["Total Predictions", str(data["total_predictions"])], ["Yogas Detected", str(data["yogas"]["total_yogas"])], ["Auspicious Yogas", str(len(data["yogas"]["auspicious"]))], ["Doshas", str(len(data["yogas"]["doshas"]))], ["Ashtakavarga Points", str(data["ashtakavarga"]["total"])], ["Strongest Planet", data["shadbala"]["strongest"]], ["Weakest Planet", data["shadbala"]["weakest"]], ["Mahadasha", data["dasha"]["mahadasha"]["lord"]], ["Antardasha", data["dasha"]["antardasha"]["lord"]], ["Vratyantardasha", data["dasha"]["pratyantardasha"]["lord"]], ["Varshphal Year", str(data["varshphal"]["year"])], ["Muntha Rashi", data["varshphal"]["muntha"]["rashi"]]]
    t = Table(summary, colWidths=[7*cm, 7*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("BACKGROUND", (0, 1), (0, -1), HexColor("#f5efe2")), ("TEXTCOLOR", (0, 1), (0, -1), DARK_RED), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 11), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    story.append(t)
    story.append(PageBreak())


def make_toc(story, styles):
    story.append(Paragraph("Table of Contents", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=20))
    toc = ["1. Executive Summary", "2. Birth Chart Analysis", "3. Planetary Positions Deep", "4. Vimshottari Dasha", "5. Yoga Analysis", "6. Ashtakavarga", "7. Shadbala", "8. Nakshatra Analysis", "9. Varshphal", "10. Transit Analysis", "11. Complete Predictions", "12. Risk Assessment", "13. Remedies", "14. Case Studies", "15. Research References", "16. Glossary", "17. Disclaimer"]
    for t in toc:
        story.append(Paragraph(t, styles["BodyText2"]))
    story.append(PageBreak())


def make_exec_summary(story, data, styles):
    story.append(Paragraph("1. Executive Summary", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    story.append(Paragraph("This comprehensive astrological report presents a detailed analysis of <b>" + data["country"] + "</b> using Swiss Ephemeris for actual planetary calculations. The report combines classical Vedic astrology principles with modern computational methods to provide <b>" + str(data["total_predictions"]) + " distinct predictions</b>.", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Key Findings", styles["SubSection"]))
    findings = ["Mahadasha: <b>" + data["dasha"]["mahadasha"]["lord"] + "</b> — " + _dasha_meaning(data["dasha"]["mahadasha"]["lord"]), "Antardasha: <b>" + data["dasha"]["antardasha"]["lord"] + "</b>", "Pratyantardasha: <b>" + data["dasha"]["pratyantardasha"]["lord"] + "</b>", "Strongest: <b>" + data["shadbala"]["strongest"] + "</b>", "Weakest: <b>" + data["shadbala"]["weakest"] + "</b>", "Yogas: <b>" + str(data["yogas"]["total_yogas"]) + "</b>", "Ashtakavarga: <b>" + str(data["ashtakavarga"]["total"]) + "</b>", "Varshphal: <b>" + str(data["varshphal"]["year"]) + "</b>"]
    for f in findings:
        story.append(Paragraph("- " + f, styles["BodyText2"]))
    story.append(PageBreak())


def make_birth_chart(story, data, styles):
    story.append(Paragraph("2. Birth Chart Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    asc = data["chart"]["ascendant"]
    story.append(Paragraph("Ascendant: <b>" + asc["rashi"] + "</b> at <b>" + str(asc["degree"]) + " degrees</b>", styles["BodyText2"]))
    story.append(Paragraph("Rashi Lord: <b>" + RASHI_LORDS.get(asc["rashi"], "Unknown") + "</b>", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    sun = data["chart"]["sun"]
    moon = data["chart"]["moon"]
    story.append(Paragraph("Sun: <b>" + str(sun.get("rashi", "")) + " " + str(sun.get("degree", 0)) + " deg</b> — " + str(sun.get("nakshatra", "")), styles["BodyText2"]))
    story.append(Paragraph("Moon: <b>" + str(moon.get("rashi", "")) + " " + str(moon.get("degree", 0)) + " deg</b> — " + str(moon.get("nakshatra", "")), styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("House Significations", styles["SubSection"]))
    houses = [["House", "Significations"], ["1", "Country, leadership, identity"], ["2", "Wealth, economy, currency"], ["3", "Communication, neighbors, borders"], ["4", "Land, earthquakes, natural disasters"], ["5", "Education, youth, creativity"], ["6", "Enemies, war, disease, military"], ["7", "Partnerships, alliances, war"], ["8", "Death, transformations, sudden events"], ["9", "Dharma, religion, foreign relations"], ["10", "Government, politics, leadership"], ["11", "Gains, alliances, economy"], ["12", "Losses, foreign, spiritual"]]
    t = Table(houses, colWidths=[2*cm, 13*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(PageBreak())


def make_planetary_deep(story, data, styles):
    story.append(Paragraph("3. Planetary Positions Deep Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    planets = data.get("chart", {}).get("planets", {})
    if not planets:
        planets = {"Sun": data["chart"]["sun"], "Moon": data["chart"]["moon"]}
    for name, p in planets.items():
        story.append(Paragraph(name + " - " + _planet_meaning(name), styles["SubSubSection"]))
        nak = p.get("nakshatra", "")
        pada = p.get("pada", "")
        if isinstance(nak, dict):
            pada = nak.get("pada", "")
            nak = nak.get("name", "")
        info = [["Attribute", "Value"], ["Rashi", str(p.get("rashi", ""))], ["Degree", str(p.get("degree", 0)) + " deg"], ["House", str(p.get("house", ""))], ["Dignity", str(p.get("dignity", ""))], ["Nakshatra", str(nak)], ["Pada", str(pada)]]
        t = Table(info, colWidths=[4*cm, 11*cm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
        story.append(t)
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_dasha(story, data, styles):
    story.append(Paragraph("4. Vimshottari Dasha", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    d = data["dasha"]
    story.append(Paragraph("Current Dasha", styles["SubSection"]))
    dd = [["Level", "Planet", "Lord", "Meaning"], ["Mahadasha", d["mahadasha"]["planet"], d["mahadasha"]["lord"], _dasha_meaning(d["mahadasha"]["lord"])], ["Antardasha", d["antardasha"]["planet"], d["antardasha"]["lord"], _dasha_meaning(d["antardasha"]["lord"])], ["Pratyantardasha", d["pratyantardasha"]["planet"], d["pratyantardasha"]["lord"], _dasha_meaning(d["pratyantardasha"]["lord"])]]
    t = Table(dd, colWidths=[3*cm, 2.5*cm, 2.5*cm, 7*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Full Mahadasha Sequence", styles["SubSection"]))
    sd = [["#", "Planet", "Lord", "Start", "End", "Years"]]
    for i, dasha in enumerate(d["full_mahadasha_sequence"], 1):
        sd.append([str(i), dasha["planet"], dasha["lord"], str(dasha["start_age"]), str(dasha["end_age"]), str(dasha["years"])])
    t = Table(sd, colWidths=[1*cm, 3*cm, 3*cm, 2.5*cm, 2.5*cm, 3*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(PageBreak())


def make_yoga(story, data, styles):
    story.append(Paragraph("5. Yoga Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    story.append(Paragraph("Total Yogas: <b>" + str(data["yogas"]["total_yogas"]) + "</b>", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Auspicious Yogas (" + str(len(data["yogas"]["auspicious"])) + ")", styles["SubSection"]))
    for y in data["yogas"]["auspicious"]:
        story.append(Paragraph("<b>" + y["name"] + "</b> (" + y["strength"] + ")", styles["Prediction"]))
        story.append(Paragraph("  " + y["effect"], styles["Prediction"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Doshas (" + str(len(data["yogas"]["doshas"])) + ")", styles["SubSection"]))
    for y in data["yogas"]["doshas"]:
        story.append(Paragraph("<b>" + y["name"] + "</b> (" + y["strength"] + ")", styles["Prediction"]))
        story.append(Paragraph("  " + y["effect"], styles["Prediction"]))
    story.append(PageBreak())


def make_ashtakavarga(story, data, styles):
    story.append(Paragraph("6. Ashtakavarga 337 Points", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    story.append(Paragraph("Total: <b>" + str(data["ashtakavarga"]["total"]) + "</b>", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Strongest Signs", styles["SubSection"]))
    sd = [["Rank", "Rashi", "Points", "Meaning"]]
    for i, (r, s) in enumerate(data["ashtakavarga"]["strongest"], 1):
        sd.append([str(i), r, str(s), _rashi_meaning(r)])
    t = Table(sd, colWidths=[1.5*cm, 3*cm, 2*cm, 8.5*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f0fdf4")])]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Weakest Signs", styles["SubSection"]))
    wd = [["Rank", "Rashi", "Points", "Meaning"]]
    for i, (r, s) in enumerate(data["ashtakavarga"]["weakest"], 1):
        wd.append([str(i), r, str(s), _rashi_meaning(r)])
    t = Table(wd, colWidths=[1.5*cm, 3*cm, 2*cm, 8.5*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#fef2f2")])]))
    story.append(t)
    story.append(PageBreak())


def make_shadbala(story, data, styles):
    story.append(Paragraph("7. Shadbala Six Strengths", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    rd = [["Rank", "Planet", "Total Strength", "Grade"]]
    for i, (p, t) in enumerate(data["shadbala"]["ranking"], 1):
        grade = "Strong" if t > 390 else "Moderate" if t > 350 else "Weak"
        rd.append([str(i), p, str(round(t, 2)), grade])
    t = Table(rd, colWidths=[1.5*cm, 3*cm, 4.5*cm, 4*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 10), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("<b>Strongest:</b> " + data["shadbala"]["strongest"], styles["BodyText2"]))
    story.append(Paragraph("<b>Weakest:</b> " + data["shadbala"]["weakest"], styles["BodyText2"]))
    story.append(PageBreak())


def make_nakshatra(story, data, styles):
    story.append(Paragraph("8. Nakshatra Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    for planet, n in data["nakshatra"].items():
        story.append(Paragraph(planet + " - " + n["nakshatra"] + " (Pada " + str(n["pada"]) + ")", styles["SubSubSection"]))
        info = [["Attribute", "Value"], ["Nakshatra", n["nakshatra"]], ["Pada", str(n["pada"])], ["Lord", n["lord"]], ["Deity", n["deity"]], ["Shakti", n.get("shakti", "")], ["Gana", n.get("gana", "")]]
        t = Table(info, colWidths=[4*cm, 11*cm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
        story.append(t)
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_varshphal(story, data, styles):
    story.append(Paragraph("9. Varshphal Annual Chart", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    v = data["varshphal"]
    story.append(Paragraph("Year: <b>" + str(v["year"]) + "</b>", styles["BodyText2"]))
    vd = [["Attribute", "Value", "Meaning"], ["Muntha Rashi", v["muntha"]["rashi"], v["muntha"]["meaning"]], ["Year Lord", v["year_lord"]["planet"], _planet_meaning(v["year_lord"]["planet"])], ["Annual Ascendant", v["ascendant"]["rashi"] + " " + str(v["ascendant"]["degree"]) + " deg", "Theme"]]
    t = Table(vd, colWidths=[4*cm, 5*cm, 6*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(PageBreak())


def make_transit(story, data, styles):
    story.append(Paragraph("10. Transit Analysis", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    td = [["Planet", "Rashi", "Degree", "House", "Nakshatra"]]
    for t in data.get("transit", {}).get("planets", []):
        td.append([t["planet"], t["rashi"], str(round(t["degree"], 2)) + " deg", str(t["house"]), t.get("nakshatra", "")])
    t = Table(td, colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2*cm, 5.5*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(PageBreak())


def make_predictions(story, data, styles):
    story.append(Paragraph("11. Complete Predictions", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    story.append(Paragraph("Total: <b>" + str(data["total_predictions"]) + "</b>", styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))
    cats = {}
    for p in data["predictions"]:
        cat = p["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(p)
    for cat, preds in cats.items():
        story.append(Paragraph(cat + " (" + str(len(preds)) + ")", styles["SubSection"]))
        for p in preds:
            story.append(Paragraph("<b>- " + p["title"] + "</b>", styles["Prediction"]))
            story.append(Paragraph("  " + p["prediction"], styles["Prediction"]))
            if p.get("confidence"):
                story.append(Paragraph("  Confidence: " + p["confidence"], styles["SmallText"]))
        story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())


def make_risk(story, data, styles):
    story.append(Paragraph("12. Risk Assessment", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    risks = []
    for t in data.get("transit", {}).get("planets", []):
        if t["planet"] == "Moon" and t["house"] == 4:
            risks.append(("Earthquake", "High", "Moon in 4th transit", "Preparedness"))
        if t["planet"] == "Mars" and t["house"] in [1, 6, 8]:
            risks.append(("War / Military", "High", "Mars in angular house", "Diplomacy"))
        if t["planet"] == "Rahu" and t["house"] == 10:
            risks.append(("Political Upheaval", "High", "Rahu in 10th", "Coalition building"))
    for y in data["yogas"]["doshas"]:
        risks.append((y["name"], y["strength"], y["effect"], "Specific remedies"))
    if not risks:
        risks.append(("General Stability", "Low", "No major indicators", "Maintain status quo"))
    rd = [["Risk", "Severity", "Indicator", "Action"]]
    for r in risks:
        rd.append(list(r))
    t = Table(rd, colWidths=[3.5*cm, 2*cm, 5*cm, 5.5*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#fef2f2")])]))
    story.append(t)
    story.append(PageBreak())


def make_remedies(story, data, styles):
    story.append(Paragraph("13. Remedies 20+ Upay", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    weakest = data["shadbala"]["weakest"]
    remedies = [("Strengthen " + weakest, "Worship deity, recite mantra, donate", "Daily/weekly"), ("Sun Worship", "Aditya Hridayam, Surya Namaskar", "Morning"), ("Gayatri Mantra", "108 recitations", "Twice daily"), ("Mahamrityunjaya", "Protection from crises", "Weekly"), ("Hanuman Chalisa", "Mars and Saturn strength", "Tue/Sat"), ("Shani Shanti", "Saturn-related delays", "Saturday"), ("Rahu-Ketu Shanti", "Nodal afflictions", "As prescribed"), ("Ganesh Puja", "Obstacle removal", "Before events"), ("Lakshmi Puja", "Economic prosperity", "Friday"), ("Durga Puja", "Protection and strength", "Navratri"), ("Navagraha Puja", "Planetary peace", "As needed"), ("Rudrabhishek", "Saturn and Rahu pacification", "Monthly"), ("Vishnu Sahasranama", "Overall well-being", "Weekly"), ("Sundarkand", "Courage and obstacles", "Tuesday"), ("Ekadashi Fast", "Spiritual growth", "Twice monthly"), ("Donate to needy", "Karma cleansing", "Regular"), ("Plant trees", "Environmental balance", "Ongoing"), ("Serve elderly", "Jupiter blessings", "Regular"), ("Om Namah Shivaya", "Transformation", "Daily 108x"), ("Yoga meditation", "Mental peace", "Daily")]
    rd = [["Remedy", "Description", "Frequency"]]
    for r in remedies:
        rd.append(list(r))
    t = Table(rd, colWidths=[4.5*cm, 7.5*cm, 3*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f0fdf4")])]))
    story.append(t)
    story.append(PageBreak())


def make_case_studies(story, data, styles):
    story.append(Paragraph("14. Historical Case Studies", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    studies = [("2001 Bhuj Earthquake", "Saturn-Moon in 4th house", "Gujarat earthquake (7.7)"), ("2004 Indian Ocean Tsunami", "Rahu-Ketu with Moon in water", "Sumatra tsunami"), ("2008 Mumbai Attacks", "Mars-Rahu in 6th/8th house", "26/11 attacks"), ("2015 Nepal Earthquake", "Saturn transit in 4th", "Gorkha earthquake (7.8)"), ("2019 Pulwama Attack", "Mars-Ketu in 8th house", "Pulwama attack"), ("2020 COVID Pandemic", "Rahu-Ketu on 6th house", "Global pandemic")]
    for name, indicator, event in studies:
        story.append(Paragraph("<b>" + name + "</b>", styles["SubSubSection"]))
        story.append(Paragraph("Astrological Indicator: " + indicator, styles["BodyText2"]))
        story.append(Paragraph("Actual Event: " + event, styles["BodyText2"]))
        story.append(Spacer(1, 0.2*cm))
    story.append(PageBreak())


def make_research(story, data, styles):
    story.append(Paragraph("15. Research References", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    refs = [("1", "Brihat Parashara Hora Shastra", "Ch. 45, 8, 42"), ("2", "Phaladeepika", "Ch. 15"), ("3", "Bhrigu Samhita", "Karmic Events"), ("4", "Nadi Astrology", "Shanti Kandam"), ("5", "Samarangana Sutradhara", "Vastu Purusha"), ("6", "Saravali", "Ch. 32"), ("7", "Jaimini Sutras", "Chara Dasha"), ("8", "Hora Sara", "Ch. 18"), ("9", "Prashna Marga", "Ch. 12"), ("10", "Muhurta Chintamani", "Ch. 8"), ("11", "Brihat Samhita", "Ch. 5, 46"), ("12", "Uttara Kalamrita", "Ch. 4"), ("13", "Sarvartha Chintamani", "Ch. 10"), ("14", "Prasna Tantra", "Ch. 3"), ("15", "Krishnamurti Paddhati", "KP Reader 1-6"), ("16", "Lal Kitab", "Rahu-Ketu"), ("17", "Bhrigu Nandi Nadi", "Vol. 1-3"), ("18", "Charaka Samhita", "Ch. 6"), ("19", "Sushruta Samhita", "Ch. 4"), ("20", "Arthashastra", "Kautilya"), ("21", "Manusmriti", "Ch. 7"), ("22", "Ramayana", "Yuddha Kand"), ("23", "Mahabharata", "Bhishma Parva"), ("24", "Atharvaveda", "Bhaumi Sukta"), ("25", "Vishnu Purana", "Ch. 5")]
    rd = [["#", "Text", "Chapters"]]
    for r in refs:
        rd.append(list(r))
    t = Table(rd, colWidths=[1*cm, 6*cm, 8*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(PageBreak())


def make_glossary(story, styles):
    story.append(Paragraph("16. Glossary", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    terms = [("Rashi", "Zodiac sign"), ("Nakshatra", "Lunar mansion"), ("Pada", "Quarter of nakshatra"), ("Lagna", "Ascendant"), ("Mahadasha", "Major planetary period"), ("Antardasha", "Sub-period"), ("Pratyantardasha", "Sub-sub-period"), ("Yoga", "Planetary combination"), ("Dosha", "Challenging combination"), ("Ashtakavarga", "337 point system"), ("Shadbala", "6-fold strength"), ("Varshphal", "Annual chart"), ("Muntha", "Annual progressed point"), ("Gochar", "Transit"), ("Exaltation", "Highest strength"), ("Debilitation", "Lowest strength"), ("Combustion", "Close to Sun"), ("Retrograde", "Backward motion"), ("Bindu", "Ashtakavarga point"), ("Kendra", "Angular houses"), ("Trikona", "Trinal houses"), ("Dusthana", "Difficult houses"), ("Upachaya", "Growth houses"), ("Raja Yoga", "Power combination"), ("Dhana Yoga", "Wealth combination"), ("Kaal Sarpa Yoga", "Planets between Rahu-Ketu"), ("Mangal Dosha", "Mars affliction"), ("Gaja Kesari Yoga", "Jupiter-Moon fame"), ("Budha-Aditya Yoga", "Intelligence"), ("Chandra-Mangal Yoga", "Wealth"), ("Kemadruma Yoga", "Isolated Moon"), ("Amala Yoga", "Fame"), ("Parvata Yoga", "Wealth"), ("Kahala Yoga", "Courage"), ("Vasumati Yoga", "Independence"), ("Sunapha Yoga", "Wealth"), ("Anapha Yoga", "Health"), ("Durudhara Yoga", "Wealth"), ("Panch Mahapurusha", "Five great yogas")]
    gd = [["Term", "Definition"]]
    for term, definition in terms:
        gd.append([term, definition])
    t = Table(gd, colWidths=[5*cm, 10*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK_RED), ("TEXTCOLOR", (0, 0), (-1, 0), GOLD), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("GRID", (0, 0), (-1, -1), 0.5, GOLD), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#faf8f3")])]))
    story.append(t)
    story.append(PageBreak())


def make_disclaimer(story, styles):
    story.append(Paragraph("17. Disclaimer", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))
    text = "This report is generated using Swiss Ephemeris for actual planetary calculations and classical Vedic astrology principles from BPHS, Phaladeepika, Bhrigu Samhita, Nadi Astrology, Saravali, Jaimini Sutras, and other classical texts.<br/><br/><b>Purpose:</b> Educational and informational only. Not a substitute for professional advice.<br/><br/><b>Limitations:</b> Astrological predictions are probabilistic, not deterministic.<br/><br/><b>No Liability:</b> Vastu One and its creators are not responsible for any decisions arising from this report.<br/><br/><b>Copyright 2026 Vastu One - India - All Rights Reserved</b>"
    story.append(Paragraph(text, styles["BodyText2"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("-- End of Report --", styles["Quote"]))



def make_bnn_section(story, data, styles):
    """BNN Hidden Gems section"""
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


def make_deep_paragraphs_section(story, data, styles):
    """Deep Paragraph Explanations section"""
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

def generate_pdf(country="India"):
    data = get_predictions(country)
    if "error" in data:
        return None
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm, title="Vastu One - " + country + " Report", author="Vastu One")
    styles = get_styles()
    story = []
    make_cover(story, data, styles)
    make_toc(story, styles)
    make_exec_summary(story, data, styles)
    make_birth_chart(story, data, styles)
    make_planetary_deep(story, data, styles)
    make_dasha(story, data, styles)
    make_yoga(story, data, styles)
    make_ashtakavarga(story, data, styles)
    make_shadbala(story, data, styles)
    make_nakshatra(story, data, styles)
    make_varshphal(story, data, styles)
    make_transit(story, data, styles)
    make_predictions(story, data, styles)
    make_risk(story, data, styles)
    make_remedies(story, data, styles)
    make_case_studies(story, data, styles)
    make_research(story, data, styles)
    make_glossary(story, styles)
    make_disclaimer(story, styles)
    doc.build(story)
    buffer.seek(0)
    return buffer


def save_pdf(country="India", output_path=None):
    if output_path is None:
        output_path = "reports/" + country + "_v3_report.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_pdf(country)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating PDF V3...")
    path = save_pdf("India")
    if path:
        size = Path(path).stat().st_size
        print("PDF: " + path)
        print("Size: " + str(size) + " bytes (" + str(round(size/1024, 1)) + " KB)")
