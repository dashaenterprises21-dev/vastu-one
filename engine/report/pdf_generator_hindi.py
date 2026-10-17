"""
VASTU ONE - Hindi PDF Generator using fpdf2 + uharfbuzz
Proper Devanagari shaping for Hindi, Marathi, Sanskrit
"""

from fpdf import FPDF
from pathlib import Path
from io import BytesIO

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.report.multi_language import get_translation, LANGUAGES
from engine.report.devanagari_reshaper import reshape_devanagari


FONTS_DIR = Path(__file__).parent / "fonts"
DEVANAGARI_FONT = FONTS_DIR / "NotoSansDevanagari.ttf"


class HindiPDF(FPDF):
    """Custom PDF class with Hindi support"""
    
    def __init__(self):
        super().__init__()
        self.add_font("Devanagari", "", str(DEVANAGARI_FONT), uni=True)
        self.add_font("Devanagari", "B", str(DEVANAGARI_FONT), uni=True)
        self.set_text_shaping(True)  # Enable Devanagari shaping
        self.set_auto_page_break(auto=True, margin=15)
    
    def _r(self, text: str) -> str:
        """Reshape Devanagari text for fpdf2"""
        return reshape_devanagari(str(text)) if text else ""
    
    def header(self):
        self.set_font("Devanagari", "B", 10)
        self.set_text_color(180, 140, 80)
        self.cell(0, 10, "VASTU ONE", align="C")
        self.ln(15)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Devanagari", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
    
    def section_title(self, title: str):
        self.set_font("Devanagari", "B", 16)
        self.set_text_color(90, 20, 32)
        self.cell(0, 12, self._r(title), align="L")
        self.ln(8)
        self.set_draw_color(212, 169, 97)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)
    
    def sub_section(self, title: str):
        self.set_font("Devanagari", "B", 12)
        self.set_text_color(180, 140, 80)
        self.cell(0, 10, self._r(title), align="L")
        self.ln(8)
    
    def body_text(self, text: str):
        self.set_font("Devanagari", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, self._r(text))
        self.ln(3)
    
    def key_value(self, key: str, value: str):
        self.set_font("Devanagari", "B", 10)
        self.set_text_color(90, 20, 32)
        self.cell(50, 7, self._r(key), align="L")
        self.set_font("Devanagari", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(0, 7, self._r(value), align="L")
        self.ln(7)


def generate_hindi_pdf(country: str = "India", lang: str = "hi") -> BytesIO:
    """Generate Hindi PDF with proper Devanagari shaping"""
    data = get_master_prediction(country)
    if "error" in data:
        return None
    
    t = get_translation(lang)
    pdf = HindiPDF()
    pdf.add_page()
    
    # Cover
    pdf.set_font("Devanagari", "B", 32)
    pdf.set_text_color(90, 20, 32)
    pdf.ln(30)
    pdf.cell(0, 15, "VASTU ONE", align="C")
    pdf.ln(15)
    pdf.set_font("Devanagari", "", 18)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, t["title"], align="C")
    pdf.ln(10)
    pdf.set_font("Devanagari", "B", 36)
    pdf.set_text_color(90, 20, 32)
    pdf.cell(0, 15, country.upper(), align="C")
    pdf.ln(15)
    pdf.set_font("Devanagari", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, t["subtitle"], align="C")
    pdf.ln(10)
    pdf.cell(0, 10, t["generated"] + ": " + data["date"], align="C")
    pdf.ln(30)
    
    # Key metrics
    pdf.set_font("Devanagari", "", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, t.get("total_predictions", "Total Predictions") + ": " + str(data.get("total_predictions", 0)), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, t.get("total_yogas", "Total Yogas") + ": " + str(data.get("yogas_complete", {}).get("total_yogas", 0)), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, t.get("ashtakavarga_points", "Ashtakavarga") + ": " + str(data.get("ashtakavarga", {}).get("total", 0)), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, t.get("strongest_planet", "Strongest") + ": " + data.get("shadbala", {}).get("strongest", ""), align="C")
    pdf.ln(8)
    pdf.cell(0, 8, t.get("weakest_planet", "Weakest") + ": " + data.get("shadbala", {}).get("weakest", ""), align="C")
    pdf.ln(8)
    
    # Page 2: Executive Summary
    pdf.add_page()
    pdf.section_title("1. " + t["exec_summary"])
    pdf.body_text(f"यह रपरट {country} क 12-लयर जयतषय वशलषण परसतत करत ह यह सवस एफमरस क उपयग करक वसतवक गरह क गणन पर आधरत ह")
    pdf.ln(5)
    pdf.sub_section("मखय नषकरष")
    pdf.key_value("महदश", data.get("complete_dasha", {}).get("levels", {}).get("mahadasha", {}).get("planet", ""))
    pdf.key_value("अतरदश", data.get("complete_dasha", {}).get("levels", {}).get("antardasha", {}).get("planet", ""))
    pdf.key_value("परतयतरदश", data.get("complete_dasha", {}).get("levels", {}).get("pratyantardasha", {}).get("planet", ""))
    pdf.key_value("सबस मजबत गरह", data.get("shadbala", {}).get("strongest", ""))
    pdf.key_value("सबस कमजर गरह", data.get("shadbala", {}).get("weakest", ""))
    pdf.key_value("कल यग", str(data.get("yogas_complete", {}).get("total_yogas", 0)))
    pdf.key_value("अषटकवरग अक", str(data.get("ashtakavarga", {}).get("total", 0)))
    pdf.key_value("गचर परणम", data.get("transit_ashtakavarga", {}).get("overall_verdict", ""))
    
    # Page 3: Planetary Deep
    pdf.add_page()
    pdf.section_title("2. " + t["planetary_deep"])
    planets = data.get("planetary_deep", {}).get("planets", {})
    for name, p in planets.items():
        pdf.sub_section(name + "  " + p.get("rashi", "") + " " + str(p.get("degree", 0)) + "")
        pdf.key_value("रश", p.get("rashi", ""))
        pdf.key_value("अश", str(p.get("degree", 0)) + "")
        pdf.key_value("भव", str(p.get("house", "")))
        pdf.key_value("सथत", p.get("dignity", ""))
        pdf.key_value("अवसथ", p.get("avastha", {}).get("state", ""))
        pdf.key_value("सपतवरगज बल", str(p.get("saptavargaja_bala", {}).get("percentage", 0)) + "%")
        pdf.key_value("दगबल", str(p.get("digbala", {}).get("digbala", 0)) + "/60")
        pdf.key_value("नकषतर सवम", p.get("nakshatra_lord", ""))
        pdf.key_value("नकषतर दवत", p.get("nakshatra_deity", ""))
        pdf.ln(3)
    
    # Page 4: Dasha 5 Levels
    pdf.add_page()
    pdf.section_title("3. " + t["dasha_5"])
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
        pdf.body_text("अवध: " + level.get("start_date", "") + " स " + level.get("end_date", ""))
        if level.get("effects"):
            pdf.body_text("सकरतमक: " + level["effects"].get("positive", ""))
            pdf.body_text("नकरतमक: " + level["effects"].get("negative", ""))
        pdf.ln(2)
    
    # Page 5: Yogas
    pdf.add_page()
    pdf.section_title("4. " + t["yoga"])
    yogas = data.get("yogas_complete", {})
    pdf.body_text("कल यग: " + str(yogas.get("total_yogas", 0)))
    if yogas.get("auspicious"):
        pdf.sub_section(t.get("auspicious", "शभ यग"))
        for y in yogas["auspicious"]:
            pdf.body_text(" " + y["name"] + " (" + y["strength"] + ")")
            pdf.body_text("  " + y["effect"])
            pdf.body_text("  " + t.get("classical_ref", "शसतरय सदरभ") + ": " + y.get("classical_ref", ""))
    if yogas.get("doshas"):
        pdf.sub_section(t.get("doshas", "दष"))
        for y in yogas["doshas"]:
            pdf.body_text(" " + y["name"] + " (" + y["strength"] + ")")
            pdf.body_text("  " + y["effect"])
    
    # Page 6: Transit
    pdf.add_page()
    pdf.section_title("5. " + t["transit"])
    transit = data.get("transit_ashtakavarga", {})
    pdf.body_text("समगर परणम: " + transit.get("overall_verdict", ""))
    for tr in transit.get("transit_analysis", []):
        pdf.body_text(tr["planet"] + " in " + tr["rashi"] + " (भव " + str(tr["house"]) + ")  बद: " + str(tr["bindu"]) + "/8")
        pdf.body_text("परणम: " + tr["verdict"])
    
    # Page 7: Varshphal
    pdf.add_page()
    pdf.section_title("6. " + t["varshphal"])
    varsh = data.get("varshphal", {})
    for year in ["2026", "2027", "2028"]:
        v = varsh.get(year, {})
        if not v:
            continue
        pdf.sub_section("वरष " + year)
        pdf.body_text("सर वपस: " + v.get("solar_return_date", ""))
        pdf.body_text("मथ: " + v.get("muntha", {}).get("rashi", ""))
        pdf.body_text("वरषशवर: " + v.get("year_lord", {}).get("planet", ""))
    
    # Page 8: Nadi/Bhrigu
    pdf.add_page()
    pdf.section_title("7. " + t["nadi"])
    nadi = data.get("nadi_bhrigu", {})
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        pdf.body_text("नकषतर: " + n.get("nakshatra", "") + " | नड: " + n.get("nadi", ""))
        pdf.body_text("पछल जनम: " + n.get("past_life", ""))
    if nadi.get("karmic_debts"):
        pdf.sub_section("करम ऋण")
        for k in nadi["karmic_debts"]:
            pdf.body_text(" " + k["name"] + "  " + k["remedy"])
    
    # Page 9: BNN
    pdf.add_page()
    pdf.section_title("8. " + t["bnn"])
    bnn = data.get("bnn_data", {})
    if bnn.get("conjunctions_5_degree"):
        pdf.sub_section("5-डगर यत")
        for c in bnn["conjunctions_5_degree"]:
            pdf.body_text(" " + c["planets"][0] + " + " + c["planets"][1] + " (" + str(c["degree_diff"]) + ")  " + c["strength"])
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        pdf.sub_section("करक")
        for k, v in bnn["karakas"]["karakas"].items():
            pdf.body_text(" " + k + ": " + v["planet"])
    
    # Page 10: Deep Paragraphs
    pdf.add_page()
    pdf.section_title("9. " + t["paragraphs"])
    paragraphs_data = data.get("paragraphs_data", {})
    paragraphs = paragraphs_data.get("paragraphs", [])
    for p in paragraphs:
        pdf.sub_section(p.get("title", ""))
        pdf.body_text(p.get("paragraph", ""))
        pdf.ln(2)
    
    # Final: Disclaimer
    pdf.add_page()
    pdf.section_title("10. " + t["disclaimer"])
    pdf.body_text("यह रपरट सवस एफमरस और शसतरय वदक जयतष सदधत क उपयग करक बनई गई ह यह कवल शकषक और सचनतमक उददशय क लए ह")
    pdf.ln(10)
    pdf.body_text(" 2026 Vastu One  India")
    
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


def save_hindi_pdf(country: str = "India", lang: str = "hi", output_path: str = None):
    if output_path is None:
        output_path = "reports/" + country + "_" + lang + "_report.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_hindi_pdf(country, lang)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating Hindi PDF with proper Devanagari shaping...")
    path = save_hindi_pdf("India", "hi")
    if path:
        size = Path(path).stat().st_size
        print("PDF generated: " + path)
        print("Size: " + str(size) + " bytes (" + str(round(size/1024, 1)) + " KB)")
