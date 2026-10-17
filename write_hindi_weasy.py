from pathlib import Path

code = '''"""
VASTU ONE - Hindi PDF Generator using WeasyPrint
Proper Devanagari shaping via Pango/HarfBuzz
"""

from weasyprint import HTML, CSS
from pathlib import Path
from io import BytesIO

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.report.multi_language import get_translation, LANGUAGES


FONTS_DIR = Path(__file__).parent / "fonts"
DEVANAGARI_FONT = FONTS_DIR / "NotoSansDevanagari.ttf"


def get_hindi_css() -> str:
    """CSS with proper Devanagari font"""
    return """
    @font-face {
        font-family: 'NotoDevanagari';
        src: url('file:///""" + str(DEVANAGARI_FONT).replace("\\\\", "/") + """');
        font-weight: normal;
    }
    @font-face {
        font-family: 'NotoDevanagari';
        src: url('file:///""" + str(DEVANAGARI_FONT).replace("\\\\", "/") + """');
        font-weight: bold;
    }
    body {
        font-family: 'NotoDevanagari', 'Noto Sans Devanagari', sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #1e1e1e;
        margin: 0;
        padding: 0;
    }
    h1 { font-size: 28pt; color: #5a1420; text-align: center; margin-bottom: 10px; }
    h2 { font-size: 18pt; color: #5a1420; border-bottom: 2px solid #d4a961; padding-bottom: 5px; margin-top: 20px; }
    h3 { font-size: 14pt; color: #b8893b; margin-top: 15px; margin-bottom: 8px; }
    .cover { text-align: center; padding: 60px 20px; }
    .cover-title { font-size: 42pt; color: #5a1420; font-weight: bold; }
    .cover-subtitle { font-size: 16pt; color: #a8a29e; font-style: italic; }
    .cover-country { font-size: 56pt; color: #5a1420; font-weight: bold; margin: 30px 0; }
    .section { margin: 20px 0; }
    .key-value { display: flex; justify-content: space-between; border-bottom: 1px dotted #ddd; padding: 4px 0; }
    .key { font-weight: bold; color: #5a1420; }
    .value { color: #1e1e1e; }
    .yoga { background: #faf8f3; border-left: 3px solid #d4a961; padding: 8px 12px; margin: 8px 0; }
    .dosha { background: #fef2f2; border-left: 3px solid #dc2626; padding: 8px 12px; margin: 8px 0; }
    .dasha { background: #f5efe2; border-left: 3px solid #b8893b; padding: 10px 12px; margin: 10px 0; }
    .transit { background: #faf8f3; border-left: 3px solid #10b981; padding: 8px 12px; margin: 8px 0; }
    .page-break { page-break-before: always; }
    .footer { text-align: center; font-size: 9pt; color: #a8a29e; margin-top: 30px; }
    ul { margin: 5px 0; padding-left: 20px; }
    li { margin: 3px 0; }
    """


def build_hindi_html(data: dict, t: dict) -> str:
    """Build HTML for Hindi PDF"""
    country = data["country"]
    
    # Cover
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body>
    <div class="cover">
        <div class="cover-title">VASTU ONE</div>
        <div class="cover-subtitle">{t.get('title', '')}</div>
        <div class="cover-country">{country.upper()}</div>
        <div class="cover-subtitle">{t.get('subtitle', '')}</div>
        <div class="cover-subtitle">{t.get('generated', '')}: {data['date']}</div>
        <div style="margin-top:40px;">
            <div class="key-value"><span class="key">{t.get('total_predictions', '')}</span><span class="value">{data.get('total_predictions', 0)}</span></div>
            <div class="key-value"><span class="key">{t.get('total_yogas', '')}</span><span class="value">{data.get('yogas_complete', {}).get('total_yogas', 0)}</span></div>
            <div class="key-value"><span class="key">{t.get('ashtakavarga_points', '')}</span><span class="value">{data.get('ashtakavarga', {}).get('total', 0)}</span></div>
            <div class="key-value"><span class="key">{t.get('strongest_planet', '')}</span><span class="value">{data.get('shadbala', {}).get('strongest', '')}</span></div>
            <div class="key-value"><span class="key">{t.get('weakest_planet', '')}</span><span class="value">{data.get('shadbala', {}).get('weakest', '')}</span></div>
        </div>
    </div>
    """
    
    # Executive Summary
    html += f"""
    <div class="page-break"></div>
    <h2>1. {t.get('exec_summary', '')}</h2>
    <p>यह रिपोर्ट {country} का 12-लेयर ज्योतिषीय विश्लेषण प्रस्तुत करती है। यह स्विस एफेमेरिस का उपयोग करके वास्तविक ग्रहों की गणना पर आधारित है।</p>
    <h3>मुख्य निष्कर्ष</h3>
    <div class="key-value"><span class="key">महादशा</span><span class="value">{data.get('complete_dasha', {}).get('levels', {}).get('mahadasha', {}).get('planet', '')}</span></div>
    <div class="key-value"><span class="key">अंतर्दशा</span><span class="value">{data.get('complete_dasha', {}).get('levels', {}).get('antardasha', {}).get('planet', '')}</span></div>
    <div class="key-value"><span class="key">प्रत्यंतर्दशा</span><span class="value">{data.get('complete_dasha', {}).get('levels', {}).get('pratyantardasha', {}).get('planet', '')}</span></div>
    <div class="key-value"><span class="key">सबसे मजबूत ग्रह</span><span class="value">{data.get('shadbala', {}).get('strongest', '')}</span></div>
    <div class="key-value"><span class="key">सबसे कमजोर ग्रह</span><span class="value">{data.get('shadbala', {}).get('weakest', '')}</span></div>
    <div class="key-value"><span class="key">कुल योग</span><span class="value">{data.get('yogas_complete', {}).get('total_yogas', 0)}</span></div>
    <div class="key-value"><span class="key">अष्टकवर्ग अंक</span><span class="value">{data.get('ashtakavarga', {}).get('total', 0)}</span></div>
    <div class="key-value"><span class="key">गोचर परिणाम</span><span class="value">{data.get('transit_ashtakavarga', {}).get('overall_verdict', '')}</span></div>
    """
    
    # Planetary Deep
    html += f"""
    <div class="page-break"></div>
    <h2>2. {t.get('planetary_deep', '')}</h2>
    """
    planets = data.get("planetary_deep", {}).get("planets", {})
    for name, p in planets.items():
        html += f"""
        <h3>{name} — {p.get('rashi', '')} {p.get('degree', 0)}°</h3>
        <div class="key-value"><span class="key">राशि</span><span class="value">{p.get('rashi', '')}</span></div>
        <div class="key-value"><span class="key">अंश</span><span class="value">{p.get('degree', 0)}°</span></div>
        <div class="key-value"><span class="key">भाव</span><span class="value">{p.get('house', '')}</span></div>
        <div class="key-value"><span class="key">स्थिति</span><span class="value">{p.get('dignity', '')}</span></div>
        <div class="key-value"><span class="key">अवस्था</span><span class="value">{p.get('avastha', {}).get('state', '')}</span></div>
        <div class="key-value"><span class="key">सप्तवर्गज बल</span><span class="value">{p.get('saptavargaja_bala', {}).get('percentage', 0)}%</span></div>
        <div class="key-value"><span class="key">दिग्बल</span><span class="value">{p.get('digbala', {}).get('digbala', 0)}/60</span></div>
        <div class="key-value"><span class="key">नक्षत्र स्वामी</span><span class="value">{p.get('nakshatra_lord', '')}</span></div>
        <div class="key-value"><span class="key">नक्षत्र देवता</span><span class="value">{p.get('nakshatra_deity', '')}</span></div>
        """
    
    # Dasha 5 Levels
    html += f"""
    <div class="page-break"></div>
    <h2>3. {t.get('dasha_5', '')}</h2>
    """
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
        html += f"""
        <div class="dasha">
            <h3>{title}: {level.get('planet', '')}</h3>
            <p>अवधि: {level.get('start_date', '')} से {level.get('end_date', '')}</p>
        """
        if level.get("effects"):
            html += f"<p>सकारात्मक: {level['effects'].get('positive', '')}</p>"
            html += f"<p>नकारात्मक: {level['effects'].get('negative', '')}</p>"
        html += "</div>"
    
    # Yogas
    html += f"""
    <div class="page-break"></div>
    <h2>4. {t.get('yoga', '')}</h2>
    <p>कुल योग: {data.get('yogas_complete', {}).get('total_yogas', 0)}</p>
    """
    yogas = data.get("yogas_complete", {})
    if yogas.get("auspicious"):
        html += f"<h3>{t.get('auspicious', 'शुभ योग')}</h3>"
        for y in yogas["auspicious"]:
            html += f"""
            <div class="yoga">
                <strong>{y['name']}</strong> ({y['strength']})
                <p>{y['effect']}</p>
                <p><em>{t.get('classical_ref', 'शास्त्रीय संदर्भ')}: {y.get('classical_ref', '')}</em></p>
            </div>
            """
    if yogas.get("doshas"):
        html += f"<h3>{t.get('doshas', 'दोष')}</h3>"
        for y in yogas["doshas"]:
            html += f"""
            <div class="dosha">
                <strong>{y['name']}</strong> ({y['strength']})
                <p>{y['effect']}</p>
            </div>
            """
    
    # Transit
    html += f"""
    <div class="page-break"></div>
    <h2>5. {t.get('transit', '')}</h2>
    <p>समग्र परिणाम: {data.get('transit_ashtakavarga', {}).get('overall_verdict', '')}</p>
    """
    for tr in data.get("transit_ashtakavarga", {}).get("transit_analysis", []):
        html += f"""
        <div class="transit">
            <strong>{tr['planet']}</strong> in {tr['rashi']} (भाव {tr['house']}) — बिंदु: {tr['bindu']}/8
            <p>परिणाम: {tr['verdict']}</p>
        </div>
        """
    
    # Varshphal
    html += f"""
    <div class="page-break"></div>
    <h2>6. {t.get('varshphal', '')}</h2>
    """
    varsh = data.get("varshphal", {})
    for year in ["2026", "2027", "2028"]:
        v = varsh.get(year, {})
        if not v:
            continue
        html += f"""
        <h3>वर्ष {year}</h3>
        <div class="key-value"><span class="key">सौर वापसी</span><span class="value">{v.get('solar_return_date', '')}</span></div>
        <div class="key-value"><span class="key">मुंथा</span><span class="value">{v.get('muntha', {}).get('rashi', '')}</span></div>
        <div class="key-value"><span class="key">वर्षेश्वर</span><span class="value">{v.get('year_lord', {}).get('planet', '')}</span></div>
        """
    
    # Nadi/Bhrigu
    html += f"""
    <div class="page-break"></div>
    <h2>7. {t.get('nadi', '')}</h2>
    """
    nadi = data.get("nadi_bhrigu", {})
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        html += f"""
        <div class="key-value"><span class="key">नक्षत्र</span><span class="value">{n.get('nakshatra', '')}</span></div>
        <div class="key-value"><span class="key">नाड़ी</span><span class="value">{n.get('nadi', '')}</span></div>
        <div class="key-value"><span class="key">पिछला जन्म</span><span class="value">{n.get('past_life', '')}</span></div>
        """
    if nadi.get("karmic_debts"):
        html += "<h3>कर्म ऋण</h3><ul>"
        for k in nadi["karmic_debts"]:
            html += f"<li><strong>{k['name']}</strong> — {k['remedy']}</li>"
        html += "</ul>"
    
    # BNN
    html += f"""
    <div class="page-break"></div>
    <h2>8. {t.get('bnn', '')}</h2>
    """
    bnn = data.get("bnn_data", {})
    if bnn.get("conjunctions_5_degree"):
        html += "<h3>5-डिग्री युति</h3><ul>"
        for c in bnn["conjunctions_5_degree"]:
            html += f"<li>{c['planets'][0]} + {c['planets'][1]} ({c['degree_diff']}°) — {c['strength']}</li>"
        html += "</ul>"
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        html += "<h3>कारक</h3><ul>"
        for k, v in bnn["karakas"]["karakas"].items():
            html += f"<li><strong>{k}</strong>: {v['planet']}</li>"
        html += "</ul>"
    
    # Deep Paragraphs
    html += f"""
    <div class="page-break"></div>
    <h2>9. {t.get('paragraphs', '')}</h2>
    """
    paragraphs_data = data.get("paragraphs_data", {})
    paragraphs = paragraphs_data.get("paragraphs", [])
    for p in paragraphs:
        html += f"""
        <h3>{p.get('title', '')}</h3>
        <p style="text-align:justify;">{p.get('paragraph', '')}</p>
        """
    
    # Disclaimer
    html += f"""
    <div class="page-break"></div>
    <h2>10. {t.get('disclaimer', '')}</h2>
    <p>यह रिपोर्ट स्विस एफेमेरिस और शास्त्रीय वैदिक ज्योतिष सिद्धांतों का उपयोग करके बनाई गई है। यह केवल शैक्षिक और सूचनात्मक उद्देश्यों के लिए है।</p>
    <p class="footer">© 2026 Vastu One · Nagpur, Maharashtra</p>
    </body>
    </html>
    """
    
    return html


def generate_hindi_pdf_weasy(country: str = "India", lang: str = "hi") -> BytesIO:
    """Generate Hindi PDF using WeasyPrint"""
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
    html_content = build_hindi_html(data, t)
    css_content = get_hindi_css()
    
    buffer = BytesIO()
    HTML(string=html_content).write_pdf(buffer, stylesheets=[CSS(string=css_content)])
    buffer.seek(0)
    return buffer


def save_hindi_pdf_weasy(country: str = "India", lang: str = "hi", output_path: str = None):
    if output_path is None:
        output_path = "reports/" + country + "_" + lang + "_report.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_hindi_pdf_weasy(country, lang)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating Hindi PDF with WeasyPrint (proper Devanagari shaping)...")
    path = save_hindi_pdf_weasy("India", "hi")
    if path:
        size = Path(path).stat().st_size
        print("PDF generated: " + path)
        print("Size: " + str(size) + " bytes (" + str(round(size/1024, 1)) + " KB)")
'''

Path("engine/report/pdf_generator_hindi_weasy.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/report/pdf_generator_hindi_weasy.py").stat().st_size, "bytes")