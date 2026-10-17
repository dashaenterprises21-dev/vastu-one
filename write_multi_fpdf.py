from pathlib import Path

code = '''"""
VASTU ONE - Multi-Language PDF Generator using fpdf2
Proper shaping for Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, Sanskrit
"""

from fpdf import FPDF
from pathlib import Path
from io import BytesIO

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.report.multi_language import get_translation, LANGUAGES
from engine.report.devanagari_reshaper import reshape_devanagari


FONTS_DIR = Path(__file__).parent / "fonts"

# Font mapping per language
LANGUAGE_FONTS = {
    "en": {"font": "Helvetica", "file": None, "shaping": False, "reshaper": None},
    "hi": {"font": "NotoDevanagari", "file": "NotoSansDevanagari.ttf", "shaping": True, "reshaper": reshape_devanagari},
    "mr": {"font": "NotoDevanagari", "file": "NotoSansDevanagari.ttf", "shaping": True, "reshaper": reshape_devanagari},
    "sa": {"font": "NotoDevanagari", "file": "NotoSansDevanagari.ttf", "shaping": True, "reshaper": reshape_devanagari},
    "gu": {"font": "NotoGujarati", "file": "NotoSansGujarati.ttf", "shaping": True, "reshaper": None},
    "ta": {"font": "NotoTamil", "file": "NotoSansTamil.ttf", "shaping": True, "reshaper": None},
    "te": {"font": "NotoTelugu", "file": "NotoSansTelugu.ttf", "shaping": True, "reshaper": None},
    "bn": {"font": "NotoBengali", "file": "NotoSansBengali.ttf", "shaping": True, "reshaper": None},
}


class MultiLangPDF(FPDF):
    """Custom PDF class with multi-language support"""
    
    def __init__(self, lang: str = "en"):
        super().__init__()
        self.lang = lang
        self.font_info = LANGUAGE_FONTS.get(lang, LANGUAGE_FONTS["en"])
        self.font_family = self.font_info["font"]
        
        # Register font if needed
        if self.font_info["file"]:
            font_path = FONTS_DIR / self.font_info["file"]
            if font_path.exists():
                self.add_font(self.font_family, "", str(font_path), uni=True)
                self.add_font(self.font_family, "B", str(font_path), uni=True)
                if self.font_info["shaping"]:
                    self.set_text_shaping(True)
        
        self.set_auto_page_break(auto=True, margin=15)
    
    def _r(self, text: str) -> str:
        """Reshape text if needed"""
        if not text:
            return ""
        text = str(text)
        reshaper = self.font_info.get("reshaper")
        if reshaper:
            return reshaper(text)
        return text
    
    def header(self):
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(180, 140, 80)
        self.cell(0, 10, "VASTU ONE", align="C")
        self.ln(15)
    
    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_family, "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
    
    def section_title(self, title: str):
        self.set_font(self.font_family, "B", 16)
        self.set_text_color(90, 20, 32)
        self.cell(0, 12, self._r(title), align="L")
        self.ln(8)
        self.set_draw_color(212, 169, 97)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)
    
    def sub_section(self, title: str):
        self.set_font(self.font_family, "B", 12)
        self.set_text_color(180, 140, 80)
        self.cell(0, 10, self._r(title), align="L")
        self.ln(8)
    
    def body_text(self, text: str):
        self.set_font(self.font_family, "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, self._r(text))
        self.ln(3)
    
    def key_value(self, key: str, value: str):
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(90, 20, 32)
        self.cell(50, 7, self._r(key), align="L")
        self.set_font(self.font_family, "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(0, 7, self._r(value), align="L")
        self.ln(7)


def generate_multi_pdf(country: str = "India", lang: str = "en") -> BytesIO:
    """Generate PDF in specified language"""
    data = get_master_prediction(country)
    if "error" in data:
        return None
    
    # Add paragraphs if not present
    if "paragraphs_data" not in data:
        try:
            from engine.astro.deep_paragraph_engine import get_full_explanation_report
            data["paragraphs_data"] = get_full_explanation_report(country)
        except:
            pass
    
    # Add BNN if not present
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
    
    t = get_translation(lang)
    pdf = MultiLangPDF(lang)
    pdf.add_page()
    
    # Cover
    pdf.set_font(pdf.font_family, "B", 32)
    pdf.set_text_color(90, 20, 32)
    pdf.ln(30)
    pdf.cell(0, 15, "VASTU ONE", align="C")
    pdf.ln(15)
    pdf.set_font(pdf.font_family, "", 18)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, pdf._r(t.get("title", "Research Grade Astrological Report")), align="C")
    pdf.ln(10)
    pdf.set_font(pdf.font_family, "B", 36)
    pdf.set_text_color(90, 20, 32)
    pdf.cell(0, 15, country.upper(), align="C")
    pdf.ln(15)
    pdf.set_font(pdf.font_family, "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, pdf._r(t.get("subtitle", "12-Layer Master Prediction Analysis")), align="C")
    pdf.ln(10)
    pdf.cell(0, 10, pdf._r(t.get("generated", "Generated")) + ": " + data["date"], align="C")
    pdf.ln(30)
    
    # Key metrics
    pdf.set_font(pdf.font_family, "", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, pdf._r(t.get("total_predictions", "Total Predictions")) + ": " + str(data.get("total_predictions", 0)), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, pdf._r(t.get("total_yogas", "Total Yogas")) + ": " + str(data.get("yogas_complete", {}).get("total_yogas", 0)), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, pdf._r(t.get("ashtakavarga_points", "Ashtakavarga")) + ": " + str(data.get("ashtakavarga", {}).get("total", 0)), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, pdf._r(t.get("strongest_planet", "Strongest")) + ": " + data.get("shadbala", {}).get("strongest", ""), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, pdf._r(t.get("weakest_planet", "Weakest")) + ": " + data.get("shadbala", {}).get("weakest", ""), align="C")
    pdf.ln(8)
    
    # Page 2: Executive Summary
    pdf.add_page()
    pdf.section_title("1. " + t.get("exec_summary", "Executive Summary"))
    pdf.body_text(f"This research-grade report presents a complete 12-layer astrological analysis of {country}.")
    pdf.ln(5)
    pdf.sub_section(t.get("key_findings", "Key Findings"))
    pdf.key_value(t.get("mahadasha", "Mahadasha"), data.get("complete_dasha", {}).get("levels", {}).get("mahadasha", {}).get("planet", ""))
    pdf.key_value(t.get("antardasha", "Antardasha"), data.get("complete_dasha", {}).get("levels", {}).get("antardasha", {}).get("planet", ""))
    pdf.key_value(t.get("pratyantardasha", "Pratyantardasha"), data.get("complete_dasha", {}).get("levels", {}).get("pratyantardasha", {}).get("planet", ""))
    pdf.key_value(t.get("strongest_planet", "Strongest"), data.get("shadbala", {}).get("strongest", ""))
    pdf.key_value(t.get("weakest_planet", "Weakest"), data.get("shadbala", {}).get("weakest", ""))
    pdf.key_value(t.get("total_yogas", "Total Yogas"), str(data.get("yogas_complete", {}).get("total_yogas", 0)))
    pdf.key_value(t.get("ashtakavarga_points", "Ashtakavarga"), str(data.get("ashtakavarga", {}).get("total", 0)))
    pdf.key_value(t.get("transit", "Transit"), data.get("transit_ashtakavarga", {}).get("overall_verdict", ""))
    
    # Page 3: Planetary Deep
    pdf.add_page()
    pdf.section_title("2. " + t.get("planetary_deep", "Planetary Deep Analysis"))
    planets = data.get("planetary_deep", {}).get("planets", {})
    for name, p in planets.items():
        pdf.sub_section(name + "  " + p.get("rashi", "") + " " + str(p.get("degree", 0)) + "")
        pdf.key_value(t.get("rashi", "Rashi"), p.get("rashi", ""))
        pdf.key_value(t.get("degree", "Degree"), str(p.get("degree", 0)) + "")
        pdf.key_value(t.get("house", "House"), str(p.get("house", "")))
        pdf.key_value(t.get("dignity", "Dignity"), p.get("dignity", ""))
        pdf.key_value(t.get("avastha", "Avastha"), p.get("avastha", {}).get("state", ""))
        pdf.key_value(t.get("saptavargaja", "Saptavargaja"), str(p.get("saptavargaja_bala", {}).get("percentage", 0)) + "%")
        pdf.key_value(t.get("digbala", "Digbala"), str(p.get("digbala", {}).get("digbala", 0)) + "/60")
        pdf.key_value(t.get("nakshatra_lord", "Nakshatra Lord"), p.get("nakshatra_lord", ""))
        pdf.key_value(t.get("nakshatra_deity", "Nakshatra Deity"), p.get("nakshatra_deity", ""))
        pdf.ln(3)
    
    # Page 4: Dasha
    pdf.add_page()
    pdf.section_title("3. " + t.get("dasha_5", "Complete Dasha (5 Levels)"))
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
        pdf.sub_section(title + ": " + level.get("planet", ""))
        pdf.body_text(t.get("period", "Period") + ": " + level.get("start_date", "") + " - " + level.get("end_date", ""))
        if level.get("effects"):
            pdf.body_text(t.get("positive", "Positive") + ": " + level["effects"].get("positive", ""))
            pdf.body_text(t.get("negative", "Negative") + ": " + level["effects"].get("negative", ""))
        pdf.ln(2)
    
    # Page 5: Yogas
    pdf.add_page()
    pdf.section_title("4. " + t.get("yoga", "Yoga Analysis"))
    yogas = data.get("yogas_complete", {})
    pdf.body_text(t.get("total_yogas", "Total Yogas") + ": " + str(yogas.get("total_yogas", 0)))
    if yogas.get("auspicious"):
        pdf.sub_section(t.get("auspicious", "Auspicious Yogas"))
        for y in yogas["auspicious"]:
            pdf.body_text(" " + y["name"] + " (" + y["strength"] + ")")
            pdf.body_text("  " + y["effect"])
            pdf.body_text("  " + t.get("classical_ref", "Classical Ref") + ": " + y.get("classical_ref", ""))
    if yogas.get("doshas"):
        pdf.sub_section(t.get("doshas", "Doshas"))
        for y in yogas["doshas"]:
            pdf.body_text(" " + y["name"] + " (" + y["strength"] + ")")
            pdf.body_text("  " + y["effect"])
    
    # Page 6: Transit
    pdf.add_page()
    pdf.section_title("5. " + t.get("transit", "Transit + Ashtakavarga"))
    transit = data.get("transit_ashtakavarga", {})
    pdf.body_text(t.get("overall_verdict", "Overall Verdict") + ": " + transit.get("overall_verdict", ""))
    for tr_item in transit.get("transit_analysis", []):
        pdf.body_text(tr_item["planet"] + " in " + tr_item["rashi"] + " (House " + str(tr_item["house"]) + ")  Bindu: " + str(tr_item["bindu"]) + "/8")
        pdf.body_text("  " + tr_item["verdict"])
    
    # Page 7: Varshphal
    pdf.add_page()
    pdf.section_title("6. " + t.get("varshphal", "Varshphal (Annual Charts)"))
    varsh = data.get("varshphal", {})
    for year in ["2026", "2027", "2028"]:
        v = varsh.get(year, {})
        if not v:
            continue
        pdf.sub_section(t.get("year", "Year") + " " + year)
        pdf.body_text(t.get("solar_return", "Solar Return") + ": " + v.get("solar_return_date", ""))
        pdf.body_text(t.get("muntha", "Muntha") + ": " + v.get("muntha", {}).get("rashi", ""))
        pdf.body_text(t.get("year_lord", "Year Lord") + ": " + v.get("year_lord", {}).get("planet", ""))
    
    # Page 8: Nadi/Bhrigu
    pdf.add_page()
    pdf.section_title("7. " + t.get("nadi", "Nadi/Bhrigu Karmic Analysis"))
    nadi = data.get("nadi_bhrigu", {})
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        pdf.body_text(t.get("nakshatra", "Nakshatra") + ": " + n.get("nakshatra", "") + " | " + t.get("nadi_type", "Nadi") + ": " + n.get("nadi", ""))
        pdf.body_text(t.get("past_life", "Past Life") + ": " + n.get("past_life", ""))
    if nadi.get("karmic_debts"):
        pdf.sub_section(t.get("karmic_debts", "Karmic Debts"))
        for k in nadi["karmic_debts"]:
            pdf.body_text(" " + k["name"] + "  " + k["remedy"])
    
    # Page 9: BNN
    pdf.add_page()
    pdf.section_title("8. " + t.get("bnn", "BNN Hidden Gems"))
    bnn = data.get("bnn_data", {})
    if bnn.get("conjunctions_5_degree"):
        pdf.sub_section(t.get("5_degree", "5-Degree Conjunctions"))
        for c in bnn["conjunctions_5_degree"]:
            pdf.body_text(" " + c["planets"][0] + " + " + c["planets"][1] + " (" + str(c["degree_diff"]) + ")  " + c["strength"])
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        pdf.sub_section(t.get("karakas", "Karakas"))
        for k, v in bnn["karakas"]["karakas"].items():
            pdf.body_text(" " + k + ": " + v["planet"])
    
    # Page 10: Deep Paragraphs
    pdf.add_page()
    pdf.section_title("9. " + t.get("paragraphs", "Deep Paragraph Explanations"))
    paragraphs_data = data.get("paragraphs_data", {})
    paragraphs = paragraphs_data.get("paragraphs", [])
    for p in paragraphs:
        pdf.sub_section(p.get("title", ""))
        pdf.body_text(p.get("paragraph", ""))
        pdf.ln(2)
    
    # Final: Disclaimer
    pdf.add_page()
    pdf.section_title("10. " + t.get("disclaimer", "Disclaimer"))
    pdf.body_text("This report is generated using Swiss Ephemeris for actual planetary calculations and classical Vedic astrology principles. It is provided for educational and informational purposes only.")
    pdf.ln(10)
    pdf.body_text(" 2026 Vastu One  Nagpur, Maharashtra")
    
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


def save_multi_pdf(country: str = "India", lang: str = "en", output_path: str = None):
    if output_path is None:
        output_path = "reports/" + country + "_" + lang + "_report.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_multi_pdf(country, lang)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating multi-language PDFs (fpdf2)...")
    print()
    for lang in ["en", "hi", "mr", "gu", "ta", "te", "bn", "sa"]:
        print(f"Generating {LANGUAGES.get(lang)} ({lang})...")
        path = save_multi_pdf("India", lang)
        if path:
            size = Path(path).stat().st_size
            print(f"   {path} ({round(size/1024, 1)} KB)")
        else:
            print(f"   Failed")
        print()
'''

Path("engine/report/pdf_generator_multi_fpdf.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/report/pdf_generator_multi_fpdf.py").stat().st_size, "bytes")