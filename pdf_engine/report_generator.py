"""
Vastu AI - PDF Report Generator
CTO Note: यही वो फाइल है जो पैसा कमाएगी। हर detail professional होनी चाहिए।
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

from pdf_engine.styles import BRAND, get_styles, BRAND_TEXT, PAGE_SIZE, MARGIN, FONT, FONT_BOLD
from pdf_engine.charts import score_circle, elements_bar_chart


class VastuReportGenerator:
    """Professional PDF report generator"""

    def __init__(self, output_path):
        self.output_path = output_path
        self.styles = get_styles()
        self.story = []
        self.page_num = 0

    # ═══════════════════════════════════════
    # MAIN BUILD
    # ═══════════════════════════════════════
    def generate(self, data, client_info=None):
        """
        data: API का response (analyze endpoint से)
        client_info: {"name": ..., "address": ..., "phone": ...}
        """
        client_info = client_info or {}

        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=PAGE_SIZE,
            leftMargin=MARGIN,
            rightMargin=MARGIN,
            topMargin=MARGIN,
            bottomMargin=MARGIN,
            title="Vastu AI Report",
            author="Vastu AI",
            subject="Vastu Analysis Report"
        )

        # Build all pages
        self._build_cover(data, client_info)
        self.story.append(PageBreak())

        self._build_executive_summary(data)
        self.story.append(PageBreak())

        self._build_pada_grid(data)
        self.story.append(PageBreak())

        self._build_defects(data)
        self.story.append(PageBreak())

        self._build_remedies(data)
        self.story.append(PageBreak())

        self._build_elements(data)
        self.story.append(PageBreak())

        self._build_conclusion(data, client_info)

        # Add footer to every page
        doc.build(self.story,
                  onFirstPage=self._footer,
                  onLaterPages=self._footer)

        return self.output_path

    # ═══════════════════════════════════════
    # PAGE 1: COVER
    # ═══════════════════════════════════════
    def _build_cover(self, data, client_info):
        s = self.styles

        self.story.append(Spacer(1, 20 * mm))

        # Logo / Title
        self.story.append(Paragraph("🕉️", 
            self._custom_style(fontSize=48, alignment=TA_CENTER)))
        self.story.append(Spacer(1, 6 * mm))
        self.story.append(Paragraph("VASTU AI", s["cover_title"]))
        self.story.append(Paragraph(BRAND_TEXT["tagline"], s["cover_subtitle"]))

        self.story.append(Spacer(1, 20 * mm))

        # Score display
        score = data["final_score"]["total_score"]
        grade = data["final_score"]["grade"]

        self.story.append(Paragraph(
            f'<font size="14" color="#6b7280">कुल वास्तु स्कोर</font>',
            s["cover_info"]))
        self.story.append(Spacer(1, 4 * mm))
        self.story.append(Paragraph(f"{score}", s["cover_score"]))
        self.story.append(Paragraph("/ 100", s["cover_info"]))
        self.story.append(Spacer(1, 6 * mm))

        # Grade badge (colored box)
        grade_color = self._grade_color(score)
        grade_table = Table(
            [[Paragraph(f'<b>{grade}</b>', 
                self._custom_style(fontSize=18, textColor=colors.white,
                                    alignment=TA_CENTER))]],
            colWidths=[120 * mm],
            rowHeights=[14 * mm]
        )
        grade_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), grade_color),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROUNDEDCORNERS", [6, 6, 6, 6]),
        ]))
        self.story.append(grade_table)

        self.story.append(Spacer(1, 30 * mm))

        # Client info box
        info_data = [
            ["Client Name", client_info.get("name", "_________________")],
            ["Address", client_info.get("address", "_________________")],
            ["Report Date", datetime.now().strftime("%d %B %Y")],
            ["Report ID", f"VAI-{datetime.now().strftime('%Y%m%d%H%M')}"],
        ]
        info_table = Table(info_data, colWidths=[50 * mm, 90 * mm])
        info_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
            ("FONTNAME", (1, 0), (1, -1), FONT),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), BRAND["text_dim"]),
            ("TEXTCOLOR", (1, 0), (1, -1), BRAND["text"]),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -2), 0.5, BRAND["border"]),
        ]))
        self.story.append(info_table)

        self.story.append(Spacer(1, 15 * mm))
        self.story.append(Paragraph(BRAND_TEXT["sources"], 
            self._custom_style(fontSize=10, 
                                textColor=BRAND["text_dim"],
                                alignment=TA_CENTER)))

    # ═══════════════════════════════════════
    # PAGE 2: EXECUTIVE SUMMARY
    # ═══════════════════════════════════════
    def _build_executive_summary(self, data):
        s = self.styles
        self.story.append(Paragraph("कार्यकारी सारांश", s["h1"]))
        self.story.append(Paragraph("Executive Summary", s["body_dim"]))
        self.story.append(Spacer(1, 5 * mm))

        # Score breakdown table
        bd = data["final_score"]["breakdown"]
        rows = [
            ["Component", "Score", "Weight"],
            ["Devata Audit (45 Devatas)", f"{bd['devata_audit']}", "35%"],
            ["Element Balance (5 Elements)", f"{bd['element_balance']}", "20%"],
            ["Brahmasthan", f"{bd['brahma_sthan']}", "25%"],
            ["Direction Strength (16 Zones)", f"{bd['direction_strength']}", "20%"],
            ["Total Score", f"{data['final_score']['total_score']}", "100%"],
        ]
        table = Table(rows, colWidths=[80 * mm, 40 * mm, 40 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND["dark_2"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("BACKGROUND", (0, -1), (-1, -1), BRAND["bg_light"]),
            ("FONTNAME", (0, -1), (-1, -1), FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, BRAND["border"]),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        self.story.append(table)

        self.story.append(Spacer(1, 10 * mm))

        # Key findings
        total_issues = data["devata_audit"]["total_issues"]
        self.story.append(Paragraph("🔍 मुख्य निष्कर्ष", s["h2"]))
        self.story.append(Paragraph(
            f"इस विश्लेषण में <b>{total_issues} दोष</b> पाए गए हैं। "
            f"नीचे मुख्य दोष और उनके शास्त्रीय कारण दिए गए हैं:",
            s["body"]))

        # List top 3 issues
        for issue in data["devata_audit"]["issues"][:3]:
            self.story.append(Paragraph(
                f"• <b>{issue['hindi']} ({issue['direction']})</b> — "
                f"{issue['problem']} — "
                f"असर: {', '.join(issue['domain_affected'])}",
                s["body"]))

        self.story.append(Spacer(1, 8 * mm))

        # Remedy preview
        self.story.append(Paragraph("💡 मुख्य उपाय", s["h2"]))
        for r in data["remedies"][:3]:
            self.story.append(Paragraph(
                f"• <b>{r['hindi']}</b> — "
                f"{', '.join(r['remedy']['positive_objects'][:3])}",
                s["body"]))

    # ═══════════════════════════════════════
    # PAGE 3: PADA GRID
    # ═══════════════════════════════════════
    def _build_pada_grid(self, data):
        s = self.styles
        self.story.append(Paragraph("81 पद वास्तु मंडल", s["h1"]))
        self.story.append(Paragraph(
            "यह 9×9 ग्रिड 45 देवताओं के निवास स्थान को दर्शाता है। "
            "लाल रंग में वे पद हैं जहाँ दोष पाए गए हैं।",
            s["body_dim"]))
        self.story.append(Spacer(1, 5 * mm))

        # Color legend
        legend_data = [
            ["🟢 ईशान (NE)", "🔵 वायव्य (NW)", "🟡 ब्रह्मस्थान"],
            ["🔴 अग्नि (SE)", "🟠 नैऋत्य (SW)", "🟣 पश्चिम (W)"],
        ]
        legend_table = Table(legend_data, colWidths=[55 * mm, 55 * mm, 55 * mm])
        legend_table.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        self.story.append(legend_table)

        self.story.append(Spacer(1, 8 * mm))

        # Note about grid
        self.story.append(Paragraph(
            "<b>नोट:</b> पूरी 81-पद ग्रिड की डिटेल इस रिपोर्ट के "
            "डिजिटल वर्जन में interactive है। यहाँ हम मुख्य दोष "
            "बताते हैं।",
            s["body_dim"]))

        self.story.append(Spacer(1, 8 * mm))

        # Issues with pada numbers
        self.story.append(Paragraph("दोष स्थान (पद संख्या):", s["h2"]))
        for issue in data["devata_audit"]["issues"]:
            self.story.append(Paragraph(
                f"• पद #{issue['pada']} — {issue['hindi']} ({issue['direction']})",
                s["body"]))

    # ═══════════════════════════════════════
    # PAGE 4-5: DETAILED DEFECTS
    # ═══════════════════════════════════════
    def _build_defects(self, data):
        s = self.styles
        self.story.append(Paragraph("विस्तृत दोष विश्लेषण", s["h1"]))
        self.story.append(Paragraph("Detailed Defect Analysis", s["body_dim"]))
        self.story.append(Spacer(1, 5 * mm))

        for i, issue in enumerate(data["devata_audit"]["issues"], 1):
            # Card header
            severity_color = (BRAND["red"] if issue["severity"] == "high" 
                              else BRAND["orange"])
            severity_text = "गंभीर" if issue["severity"] == "high" else "मध्यम"

            card_header = Table([[
                Paragraph(f'<b>दोष #{i}: {issue["hindi"]} ({issue["direction"]})</b>',
                          self._custom_style(fontSize=12, textColor=colors.white)),
                Paragraph(f'<b>{severity_text}</b>',
                          self._custom_style(fontSize=10, textColor=colors.white,
                                              alignment=TA_CENTER))
            ]], colWidths=[120 * mm, 40 * mm])
            card_header.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), severity_color),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            self.story.append(card_header)

            # Body
            body_data = [
                ["Problem", issue["problem"]],
                ["Impact", ", ".join(issue["domain_affected"])],
                ["Pada #", f"#{issue['pada']}"],
            ]

            # Shastra reference
            if issue.get("shastra_reference"):
                ref = issue["shastra_reference"]
                body_data.append([
                    "Shastra Reference",
                    f"{ref.get('source', '')} — {ref.get('meaning', '')[:100]}"
                ])

            body_table = Table(body_data, colWidths=[35 * mm, 125 * mm])
            body_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
                ("FONTNAME", (1, 0), (1, -1), FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("TEXTCOLOR", (0, 0), (0, -1), BRAND["text_dim"]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), BRAND["bg_light"]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ]))
            self.story.append(body_table)
            self.story.append(Spacer(1, 8 * mm))

    # ═══════════════════════════════════════
    # PAGE 6-7: REMEDIES
    # ═══════════════════════════════════════
    def _build_remedies(self, data):
        s = self.styles
        self.story.append(Paragraph("शास्त्रोक्त उपाय", s["h1"]))
        self.story.append(Paragraph("Scripture-Based Remedies", s["body_dim"]))
        self.story.append(Spacer(1, 5 * mm))

        for i, r in enumerate(data["remedies"], 1):
            # Header
            header = Table([[
                Paragraph(f'<b>उपाय #{i}: {r["hindi"]} ({r["devata"]})</b>',
                          self._custom_style(fontSize=12, textColor=colors.white)),
                Paragraph(f'<b>{r["direction"]}</b>',
                          self._custom_style(fontSize=10, textColor=colors.white,
                                              alignment=TA_CENTER))
            ]], colWidths=[120 * mm, 40 * mm])
            header.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), BRAND["primary_dark"]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            self.story.append(header)

            # Remedies content
            remedy = r["remedy"]
            rows = [
                ["✅ Do", ", ".join(remedy.get("positive_objects", []))],
                ["❌ Avoid", ", ".join(remedy.get("avoid", []))],
                ["🎨 Colors", ", ".join(remedy.get("color", []))],
                ["💡 Element Balance", ", ".join(remedy.get("element_balance", []))],
            ]
            table = Table(rows, colWidths=[35 * mm, 125 * mm])
            table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("TEXTCOLOR", (0, 0), (0, -1), BRAND["text_dim"]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), BRAND["bg_light"]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, BRAND["border"]),
            ]))
            self.story.append(table)

            # Mantra
            self.story.append(Spacer(1, 3 * mm))
            mantra_table = Table([[
                Paragraph(f'🕉️ <b>मंत्र:</b> {remedy.get("mantra", "")}',
                          s["mantra"])
            ]], colWidths=[160 * mm])
            mantra_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), 
                 colors.HexColor("#fef3c7")),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]))
            self.story.append(mantra_table)

            self.story.append(Spacer(1, 8 * mm))

    # ═══════════════════════════════════════
    # PAGE 8: ELEMENTS CHART
    # ═══════════════════════════════════════
    def _build_elements(self, data):
        s = self.styles
        self.story.append(Paragraph("पंच तत्व संतुलन", s["h1"]))
        self.story.append(Paragraph("5 Elements Balance", s["body_dim"]))
        self.story.append(Spacer(1, 5 * mm))

        balance = data["element_balance"]["balance"]

        # Element cards
        element_hindi = {
            "Earth": "पृथ्वी", "Water": "जल", "Fire": "अग्नि",
            "Air": "वायु", "Space": "आकाश"
        }

        rows = [["Element", "Balance", "Status"]]
        for name, val in balance.items():
            status = ("कमज़ोर" if val < 0 
                     else "प्रबल" if val > 3 
                     else "संतुलित")
            rows.append([
                f"{element_hindi.get(name, name)} ({name})",
                str(val),
                status
            ])

        table = Table(rows, colWidths=[70 * mm, 40 * mm, 50 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND["dark_2"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, BRAND["border"]),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))

        # Color rows based on status
        for i, (name, val) in enumerate(balance.items(), start=1):
            if val < 0:
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, i), (-1, i), 
                     colors.HexColor("#fee2e2"))]))
            elif val > 3:
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, i), (-1, i), 
                     colors.HexColor("#d1fae5"))]))

        self.story.append(table)

        self.story.append(Spacer(1, 10 * mm))

        # Weak elements warning
        weak = data["element_balance"]["weak_elements"]
        if weak:
            self.story.append(Paragraph("⚠️ कमज़ोर तत्व", s["h2"]))
            for el in weak:
                hindi = element_hindi.get(el, el)
                self.story.append(Paragraph(
                    f"• <b>{hindi} ({el})</b> कमज़ोर है — "
                    f"इसका संतुलन ज़रूरी है।",
                    s["body"]))

    # ═══════════════════════════════════════
    # PAGE 9: CONCLUSION
    # ═══════════════════════════════════════
    def _build_conclusion(self, data, client_info):
        s = self.styles
        self.story.append(Paragraph("निष्कर्ष और अगले कदम", s["h1"]))
        self.story.append(Spacer(1, 5 * mm))

        score = data["final_score"]["total_score"]
        if score >= 90:
            msg = ("आपका स्थान शास्त्रों के अनुसार उत्तम है। "
                   "कोई बड़ा दोष नहीं मिला।")
        elif score >= 70:
            msg = ("आपका स्थान अच्छा है, लेकिन कुछ सुधार संभव हैं। "
                   "ऊपर दिए गए उपाय अपनाएं।")
        elif score >= 50:
            msg = ("आपके स्थान में कुछ महत्वपूर्ण दोष हैं। "
                   "उपाय जल्दी करें।")
        else:
            msg = ("गंभीर दोष पाए गए हैं। तुरंत विशेषज्ञ से "
                   "परामर्श लें।")

        self.story.append(Paragraph(msg, s["body"]))
        self.story.append(Spacer(1, 8 * mm))

        # Consultation CTA
        cta = Table([[
            Paragraph(
                '<b>🕉️ व्यक्तिगत परामर्श चाहिए?</b><br/>'
                'वास्तु विशेषज्ञ से 1:1 बात करें<br/>'
                '<br/>'
                '📞 WhatsApp: +91-XXXXX-XXXXX<br/>'
                '📧 Email: consult@vastuai.in<br/>'
                '🌐 Website: vastuai.in',
                self._custom_style(fontSize=11, alignment=TA_CENTER,
                                    textColor=BRAND["text"]))
        ]], colWidths=[160 * mm])
        cta.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fef3c7")),
            ("TOPPADDING", (0, 0), (-1, -1), 15),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ("BOX", (0, 0), (-1, -1), 1, BRAND["primary"]),
        ]))
        self.story.append(cta)

        self.story.append(Spacer(1, 10 * mm))

        # Disclaimer
        self.story.append(Paragraph("डिस्क्लेमर", s["h2"]))
        self.story.append(Paragraph(BRAND_TEXT["disclaimer"], s["body_dim"]))

    # ═══════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════
    def _footer(self, canvas, doc):
        """हर page पर footer"""
        canvas.saveState()
        canvas.setFont(FONT, 8)
        canvas.setFillColor(BRAND["text_dim"])
        canvas.drawCentredString(
            PAGE_SIZE[0] / 2, 10 * mm,
            f"{BRAND_TEXT['footer']}  |  Page {doc.page}"
        )
        canvas.restoreState()

    def _custom_style(self, fontSize=10, textColor=None, alignment=TA_LEFT):
        from reportlab.lib.styles import ParagraphStyle
        return ParagraphStyle(
            "custom",
            fontName=FONT,
            fontSize=fontSize,
            leading=fontSize * 1.4,
            textColor=textColor or BRAND["text"],
            alignment=alignment,
        )

    def _grade_color(self, score):
        if score >= 90: return BRAND["green"]
        if score >= 70: return BRAND["primary"]
        if score >= 50: return BRAND["orange"]
        return BRAND["red"]