"""
VASTU ONE - PDF Report Generator (ReportLab)
==============================================
Generates branded PDF reports using ReportLab (pure Python, no GTK deps).
"""
from __future__ import annotations
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO
from typing import Any

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether,
)


# ==========================================
# BRAND COLORS
# ==========================================
VOID = colors.HexColor("#05060F")
GOLD = colors.HexColor("#D4AF37")
GOLD_LIGHT = colors.HexColor("#F4D97C")
GREY_TEXT = colors.HexColor("#666666")
LIGHT_GREY = colors.HexColor("#E0E0E0")
BG_LIGHT = colors.HexColor("#FAFAFA")
RED = colors.HexColor("#DC2626")
ORANGE = colors.HexColor("#EA580C")
YELLOW = colors.HexColor("#F59E0B")
GREEN = colors.HexColor("#16A34A")
BLUE = colors.HexColor("#2563EB")


# ==========================================
# STYLES
# ==========================================
def get_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name="BrandName",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=VOID,
        alignment=TA_CENTER,
        letterSpacing=2,
        spaceAfter=6,
    ))
    
    styles.add(ParagraphStyle(
        name="Tagline",
        fontName="Helvetica",
        fontSize=10,
        textColor=GREY_TEXT,
        alignment=TA_CENTER,
        letterSpacing=2,
        spaceAfter=24,
    ))
    
    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=VOID,
        alignment=TA_CENTER,
        spaceAfter=6,
    ))
    
    styles.add(ParagraphStyle(
        name="PropertyName",
        fontName="Helvetica",
        fontSize=14,
        textColor=colors.HexColor("#333333"),
        alignment=TA_CENTER,
        spaceAfter=4,
    ))
    
    styles.add(ParagraphStyle(
        name="PropertyAddress",
        fontName="Helvetica",
        fontSize=10,
        textColor=GREY_TEXT,
        alignment=TA_CENTER,
        spaceAfter=30,
    ))
    
    styles.add(ParagraphStyle(
        name="SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=VOID,
        spaceAfter=6,
        spaceBefore=12,
    ))
    
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.HexColor("#333333"),
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=13,
    ))
    
    styles.add(ParagraphStyle(
        name="SmallText",
        fontName="Helvetica",
        fontSize=8,
        textColor=GREY_TEXT,
        alignment=TA_CENTER,
        spaceAfter=4,
    ))
    
    styles.add(ParagraphStyle(
        name="Disclaimer",
        fontName="Helvetica",
        fontSize=8,
        textColor=GREY_TEXT,
        alignment=TA_LEFT,
        leading=12,
    ))
    
    styles.add(ParagraphStyle(
        name="CellText",
        fontName="Helvetica",
        fontSize=8,
        textColor=colors.HexColor("#333333"),
        leading=11,
    ))
    
    styles.add(ParagraphStyle(
        name="CellBold",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=VOID,
        leading=11,
    ))
    
    return styles


# ==========================================
# GENERATOR
# ==========================================
class PDFGenerator:
    """Generates branded PDF reports using ReportLab."""
    
    def __init__(self):
        self.styles = get_styles()
    
    def _severity_color(self, severity: str) -> colors.Color:
        return {
            "critical": RED,
            "high": ORANGE,
            "medium": YELLOW,
            "low": colors.HexColor("#6B7280"),
            "informational": GREEN,
        }.get(severity, GREY_TEXT)
    
    def _draw_page_footer(self, canvas, doc):
        """Draw footer on every page."""
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GREY_TEXT)
        canvas.drawCentredString(
            A4[0] / 2,
            12 * mm,
            f"VASTU ONE — Traceable Vastu Intelligence | Page {doc.page}"
        )
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(0.5)
        canvas.line(15 * mm, 15 * mm, A4[0] - 15 * mm, 15 * mm)
        canvas.restoreState()
    
    def render(self, report_data: dict) -> bytes:
        """Render report data to PDF bytes."""
        buf = BytesIO()
        
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
            title="VASTU ONE Report",
            author="VASTU ONE",
        )
        
        story = []
        s = self.styles
        
        # ============ COVER ============
        story.append(Spacer(1, 40 * mm))
        story.append(Paragraph("VASTU <font color='#D4AF37'>ONE</font>", s["BrandName"]))
        story.append(Paragraph("TRACEABLE VASTU INTELLIGENCE", s["Tagline"]))
        
        story.append(Spacer(1, 15 * mm))
        story.append(HRFlowable(width="60%", thickness=1, color=GOLD, hAlign="CENTER"))
        story.append(Spacer(1, 8 * mm))
        
        package_name = report_data.get("package", "VASTU").replace("_", " ").title()
        story.append(Paragraph(f"{package_name} Report", s["ReportTitle"]))
        story.append(Spacer(1, 4 * mm))
        story.append(Paragraph(report_data.get("property_name", "Property"), s["PropertyName"]))
        story.append(Paragraph(report_data.get("property_address", ""), s["PropertyAddress"]))
        
        story.append(Spacer(1, 25 * mm))
        
        # Cover footer details
        report_id = report_data.get("id", "unknown")
        generated = report_data.get("generated_at", datetime.utcnow().isoformat())[:19].replace("T", " ")
        consultant = report_data.get("consultant_name", "VASTU ONE")
        
        cover_info = [
            ["Report ID", report_id[:8] + "..."],
            ["Generated", generated],
            ["Consultant", consultant],
        ]
        cover_table = Table(cover_info, colWidths=[35 * mm, 80 * mm])
        cover_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 0), (0, -1), GREY_TEXT),
            ("TEXTCOLOR", (1, 0), (1, -1), VOID),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(cover_table)
        
        story.append(PageBreak())
        
        # ============ EXECUTIVE SUMMARY ============
        story.append(Paragraph("Executive Summary", s["SectionTitle"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=8))
        
        findings = report_data.get("findings", [])
        guna = report_data.get("guna_profile", {})
        scores = report_data.get("scores", {})
        overall_score = scores.get("score", 0)
        confidence = int(scores.get("confidence", 0) * 100)
        
        # Score card
        if overall_score >= 75:
            score_color = GREEN
        elif overall_score >= 50:
            score_color = YELLOW
        else:
            score_color = RED
        
        summary_data = [
            [
                Paragraph("<b>Overall Score</b>", s["CellText"]),
                Paragraph("<b>Confidence</b>", s["CellText"]),
                Paragraph("<b>Findings</b>", s["CellText"]),
                Paragraph("<b>Verdict</b>", s["CellText"]),
            ],
            [
                Paragraph(f"<font size='18' color='{score_color.hexval()}'><b>{overall_score}</b></font>", s["CellText"]),
                Paragraph(f"<font size='18'><b>{confidence}%</b></font>", s["CellText"]),
                Paragraph(f"<font size='18'><b>{len(findings)}</b></font>", s["CellText"]),
                Paragraph(f"<font size='11'><b>{guna.get('verdict', 'N/A')}</b></font>", s["CellText"]),
            ],
        ]
        
        summary_table = Table(summary_data, colWidths=[45 * mm, 45 * mm, 45 * mm, 45 * mm])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F5F5F5")),
            ("BACKGROUND", (0, 1), (-1, 1), colors.white),
            ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_GREY),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, LIGHT_GREY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 6 * mm))
        
        engines_count = report_data.get("engines_count", 14)
        story.append(Paragraph(
            f"This report analyzes the property using <b>{engines_count} Vastu intelligence engines</b>. "
            f"Each finding is traceable to a source with a confidence level. "
            f"Recommendations are prioritized by severity and cost.",
            s["BodyText2"]
        ))
        
        # ============ GUNA PROFILE ============
        story.append(Spacer(1, 6 * mm))
        story.append(Paragraph("Guna Profile", s["SectionTitle"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=8))
        
        tamas = guna.get("tamas_score", 0)
        rajas = guna.get("rajas_score", 0)
        sattva = guna.get("sattva_score", 0)
        
        # Guna bar
        bar_width = 170 * mm
        tamas_w = tamas * bar_width
        rajas_w = rajas * bar_width
        sattva_w = sattva * bar_width
        
        guna_bar = Table(
            [["", "", ""]],
            colWidths=[max(tamas_w, 0.1), max(rajas_w, 0.1), max(sattva_w, 0.1)],
            rowHeights=[8 * mm],
        )
        guna_bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), RED),
            ("BACKGROUND", (1, 0), (1, 0), YELLOW),
            ("BACKGROUND", (2, 0), (2, 0), GREEN),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(guna_bar)
        story.append(Spacer(1, 3 * mm))
        
        legend_data = [[
            Paragraph(f"<font color='#DC2626'>■</font> Tamas (Inertia): {int(tamas * 100)}%", s["CellText"]),
            Paragraph(f"<font color='#F59E0B'>■</font> Rajas (Activity): {int(rajas * 100)}%", s["CellText"]),
            Paragraph(f"<font color='#16A34A'>■</font> Sattva (Harmony): {int(sattva * 100)}%", s["CellText"]),
        ]]
        legend_table = Table(legend_data, colWidths=[57 * mm, 57 * mm, 56 * mm])
        legend_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(legend_table)
        
        # ============ FINDINGS ============
        story.append(PageBreak())
        story.append(Paragraph("Findings", s["SectionTitle"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=8))
        
        if findings:
            table_data = [[
                Paragraph("<b>Engine</b>", s["CellBold"]),
                Paragraph("<b>Severity</b>", s["CellBold"]),
                Paragraph("<b>Guna</b>", s["CellBold"]),
                Paragraph("<b>Description</b>", s["CellBold"]),
            ]]
            
            for f in findings:
                sev = f.get("severity", "informational")
                sev_color = self._severity_color(sev)
                table_data.append([
                    Paragraph(f.get("engine", "—"), s["CellText"]),
                    Paragraph(f"<font color='{sev_color.hexval()}'><b>{sev.upper()}</b></font>", s["CellText"]),
                    Paragraph(f.get("guna", "—"), s["CellText"]),
                    Paragraph(f.get("description", ""), s["CellText"]),
                ])
            
            findings_table = Table(
                table_data,
                colWidths=[30 * mm, 25 * mm, 22 * mm, 93 * mm],
                repeatRows=1,
            )
            findings_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), VOID),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
                ("LINEBELOW", (0, 1), (-1, -1), 0.25, LIGHT_GREY),
            ]))
            story.append(findings_table)
        else:
            story.append(Paragraph("No findings recorded.", s["BodyText2"]))
        
        # ============ CONSULTANT ============
        story.append(Spacer(1, 12 * mm))
        consultant_name = report_data.get("consultant_name", "VASTU ONE")
        consultant_email = report_data.get("consultant_email", "hello@vastuone.in")
        
        consultant_content = [
            [Paragraph("<b>CONSULTANT</b>", ParagraphStyle(
                name="ConsultantLabel",
                fontName="Helvetica",
                fontSize=8,
                textColor=GREY_TEXT,
                letterSpacing=1,
            ))],
            [Paragraph(f"<b>{consultant_name}</b>", ParagraphStyle(
                name="ConsultantName",
                fontName="Helvetica-Bold",
                fontSize=11,
                textColor=VOID,
            ))],
            [Paragraph(consultant_email, s["CellText"])],
        ]
        consultant_table = Table(consultant_content, colWidths=[170 * mm])
        consultant_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, GOLD),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(consultant_table)
        
        # ============ DISCLAIMER ============
        story.append(Spacer(1, 10 * mm))
        disclaimer_text = (
            "<b>Disclaimer:</b> This report is generated by VASTU ONE based on the data provided and the "
            "selected Vastu tradition(s). Findings are traceable to sources where available. Vastu is a "
            "traditional system and results may vary. This report does not replace professional architectural, "
            "structural, or legal advice. Consult the original sources for critical decisions. Major findings "
            "may require human expert review before implementation."
        )
        
        disclaimer_table = Table(
            [[Paragraph(disclaimer_text, s["Disclaimer"])]],
            colWidths=[170 * mm],
        )
        disclaimer_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8F8F8")),
            ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(disclaimer_table)
        
        # Build PDF
        doc.build(story, onFirstPage=self._draw_page_footer, onLaterPages=self._draw_page_footer)
        
        pdf_bytes = buf.getvalue()
        buf.close()
        return pdf_bytes


# Singleton
pdf_generator = PDFGenerator()


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    
    test_data = {
        "id": "54b776ee-b203-47d7-a2a8-907d2b44f7c0",
        "package": "vastu_advanced",
        "property_name": "Rajesh Kumar Residence",
        "property_address": "Plot 45, Civil Lines, Nagpur, 440001",
        "generated_at": datetime.utcnow().isoformat(),
        "consultant_name": "Deepak Nagpure",
        "consultant_email": "deepak@vastuone.in",
        "engines_count": 14,
        "findings": [
            {"engine": "soil_engine", "severity": "informational", "guna": "Sattva", "description": "Soil: Brahmin, Excellent"},
            {"engine": "water_engine", "severity": "informational", "guna": "Sattva", "description": "Underground tank in NE - IDEAL"},
            {"engine": "colour_engine", "severity": "medium", "guna": "Tamas", "description": "Blue colour in SE - INAUSPICIOUS"},
            {"engine": "direction_strength", "severity": "informational", "guna": "Mixed", "description": "Direction N analyzed"},
            {"engine": "direction_strength", "severity": "informational", "guna": "Mixed", "description": "Direction NE analyzed"},
            {"engine": "direction_strength", "severity": "informational", "guna": "Mixed", "description": "Direction E analyzed"},
            {"engine": "direction_strength", "severity": "informational", "guna": "Mixed", "description": "Direction SE analyzed"},
        ],
        "guna_profile": {
            "verdict": "Positive House",
            "tamas_score": 0.15,
            "rajas_score": 0.20,
            "sattva_score": 0.65,
        },
        "scores": {
            "score": 72,
            "confidence": 0.92,
        },
    }
    
    pdf_bytes = pdf_generator.render(test_data)
    output = Path("test_report.pdf")
    output.write_bytes(pdf_bytes)
    print(f"✅ PDF generated: {output.absolute()}")
    print(f"   Size: {len(pdf_bytes)} bytes ({len(pdf_bytes) / 1024:.1f} KB)")