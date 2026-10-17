from pathlib import Path

code = '''"""
VASTU ONE - Multi-Language PDF Generator using WeasyPrint
Supports: English, Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, Sanskrit
"""

from weasyprint import HTML, CSS
from pathlib import Path
from io import BytesIO

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.report.multi_language import get_translation, LANGUAGES


FONTS_DIR = Path(__file__).parent / "fonts"

# Font mapping per language
LANGUAGE_FONTS = {
    "en": {"font": "Helvetica", "file": None},
    "hi": {"font": "NotoDevanagari", "file": "NotoSansDevanagari.ttf"},
    "mr": {"font": "NotoDevanagari", "file": "NotoSansDevanagari.ttf"},
    "sa": {"font": "NotoDevanagari", "file": "NotoSansDevanagari.ttf"},
    "gu": {"font": "NotoGujarati", "file": "NotoSansGujarati.ttf"},
    "ta": {"font": "NotoTamil", "file": "NotoSansTamil.ttf"},
    "te": {"font": "NotoTelugu", "file": "NotoSansTelugu.ttf"},
    "bn": {"font": "NotoBengali", "file": "NotoSansBengali.ttf"},
}


def get_font_css(lang: str) -> str:
    """Get font-face CSS for the language"""
    font_info = LANGUAGE_FONTS.get(lang, LANGUAGE_FONTS["en"])
    font_file = font_info["file"]
    
    if font_file is None:
        return ""
    
    font_path = FONTS_DIR / font_file
    if not font_path.exists():
        return ""
    
    font_url = "file:///" + str(font_path).replace("\\\\", "/")
    
    css = f"""
    @font-face {{
        font-family: '{font_info["font"]}';
        src: url('{font_url}');
        font-weight: normal;
    }}
    @font-face {{
        font-family: '{font_info["font"]}';
        src: url('{font_url}');
        font-weight: bold;
    }}
    """
    return css


def get_full_css(lang: str) -> str:
    """Get full CSS with language-specific font"""
    font_info = LANGUAGE_FONTS.get(lang, LANGUAGE_FONTS["en"])
    font_family = font_info["font"]
    
    font_css = get_font_css(lang)
    
    return font_css + f"""
    body {{
        font-family: '{font_family}', 'Noto Sans', 'Noto Sans Devanagari', sans-serif;
        font-size: 11pt;
        line-height: 1.7;
        color: #1e1e1e;
        margin: 0;
        padding: 0;
    }}
    h1 {{ font-size: 28pt; color: #5a1420; text-align: center; margin-bottom: 10px; }}
    h2 {{ font-size: 18pt; color: #5a1420; border-bottom: 2px solid #d4a961; padding-bottom: 5px; margin-top: 20px; }}
    h3 {{ font-size: 14pt; color: #b8893b; margin-top: 15px; margin-bottom: 8px; }}
    .cover {{ text-align: center; padding: 60px 20px; }}
    .cover-title {{ font-size: 42pt; color: #5a1420; font-weight: bold; }}
    .cover-subtitle {{ font-size: 16pt; color: #a8a29e; font-style: italic; }}
    .cover-country {{ font-size: 56pt; color: #5a1420; font-weight: bold; margin: 30px 0; }}
    .key-value {{ display: flex; justify-content: space-between; border-bottom: 1px dotted #ddd; padding: 4px 0; }}
    .key {{ font-weight: bold; color: #5a1420; }}
    .value {{ color: #1e1e1e; }}
    .yoga {{ background: #faf8f3; border-left: 3px solid #d4a961; padding: 8px 12px; margin: 8px 0; }}
    .dosha {{ background: #fef2f2; border-left: 3px solid #dc2626; padding: 8px 12px; margin: 8px 0; }}
    .dasha {{ background: #f5efe2; border-left: 3px solid #b8893b; padding: 10px 12px; margin: 10px 0; }}
    .transit {{ background: #faf8f3; border-left: 3px solid #10b981; padding: 8px 12px; margin: 8px 0; }}
    .page-break {{ page-break-before: always; }}
    .footer {{ text-align: center; font-size: 9pt; color: #a8a29e; margin-top: 30px; }}
    ul {{ margin: 5px 0; padding-left: 20px; }}
    li {{ margin: 3px 0; }}
    """


def build_html(data: dict, t: dict, lang: str) -> str:
    """Build HTML content"""
    country = data["country"]
    font_info = LANGUAGE_FONTS.get(lang, LANGUAGE_FONTS["en"])
    
    # Translation strings (fallback to English)
    def tr(key, default=""):
        return t.get(key, default) or default
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body>
    <div class="cover">
        <div class="cover-title">VASTU ONE</div>
        <div class="cover-subtitle">{tr('title', 'Research Grade Astrological Report')}</div>
        <div class="cover-country">{country.upper()}</div>
        <div class="cover-subtitle">{tr('subtitle', '12-Layer Master Prediction Analysis')}</div>
        <div class="cover-subtitle">{tr('generated', 'Generated')}: {data['date']}</div>
        <div style="margin-top:40px;">
            <div class="key-value"><span class="key">{tr('total_predictions', 'Total Predictions')}</span><span class="value">{data.get('total_predictions', 0)}</span></div>
            <div class="key-value"><span class="key">{tr('total_yogas', 'Total Yogas')}</span><span class="value">{data.get('yogas_complete', {}).get('total_yogas', 0)}</span></div>
            <div class="key-value"><span class="key">{tr('ashtakavarga_points', 'Ashtakavarga')}</span><span class="value">{data.get('ashtakavarga', {}).get('total', 0)}</span></div>
            <div class="key-value"><span class="key">{tr('strongest_planet', 'Strongest')}</span><span class="value">{data.get('shadbala', {}).get('strongest', '')}</span></div>
            <div class="key-value"><span class="key">{tr('weakest_planet', 'Weakest')}</span><span class="value">{data.get('shadbala', {}).get('weakest', '')}</span></div>
        </div>
    </div>
    """
    
    # Executive Summary
    html += f"""
    <div class="page-break"></div>
    <h2>1. {tr('exec_summary', 'Executive Summary')}</h2>
    <p>{tr('exec_text', 'This research-grade report presents a complete 12-layer astrological analysis of')} {country}.</p>
    <h3>{tr('key_findings', 'Key Findings')}</h3>
    <div class="key-value"><span class="key">{tr('mahadasha', 'Mahadasha')}</span><span class="value">{data.get('complete_dasha', {}).get('levels', {}).get('mahadasha', {}).get('planet', '')}</span></div>
    <div class="key-value"><span class="key">{tr('antardasha', 'Antardasha')}</span><span class="value">{data.get('complete_dasha', {}).get('levels', {}).get('antardasha', {}).get('planet', '')}</span></div>
    <div class="key-value"><span class="key">{tr('pratyantardasha', 'Pratyantardasha')}</span><span class="value">{data.get('complete_dasha', {}).get('levels', {}).get('pratyantardasha', {}).get('planet', '')}</span></div>
    <div class="key-value"><span class="key">{tr('strongest_planet', 'Strongest')}</span><span class="value">{data.get('shadbala', {}).get('strongest', '')}</span></div>
    <div class="key-value"><span class="key">{tr('weakest_planet', 'Weakest')}</span><span class="value">{data.get('shadbala', {}).get('weakest', '')}</span></div>
    <div class="key-value"><span class="key">{tr('total_yogas', 'Total Yogas')}</span><span class="value">{data.get('yogas_complete', {}).get('total_yogas', 0)}</span></div>
    <div class="key-value"><span class="key">{tr('ashtakavarga_points', 'Ashtakavarga')}</span><span class="value">{data.get('ashtakavarga', {}).get('total', 0)}</span></div>
    <div class="key-value"><span class="key">{tr('transit', 'Transit')}</span><span class="value">{data.get('transit_ashtakavarga', {}).get('overall_verdict', '')}</span></div>
    """
    
    # Planetary Deep
    html += f"""
    <div class="page-break"></div>
    <h2>2. {tr('planetary_deep', 'Planetary Deep Analysis')}</h2>
    """
    planets = data.get("planetary_deep", {}).get("planets", {})
    for name, p in planets.items():
        html += f"""
        <h3>{name} — {p.get('rashi', '')} {p.get('degree', 0)}°</h3>
        <div class="key-value"><span class="key">{tr('rashi', 'Rashi')}</span><span class="value">{p.get('rashi', '')}</span></div>
        <div class="key-value"><span class="key">{tr('degree', 'Degree')}</span><span class="value">{p.get('degree', 0)}°</span></div>
        <div class="key-value"><span class="key">{tr('house', 'House')}</span><span class="value">{p.get('house', '')}</span></div>
        <div class="key-value"><span class="key">{tr('dignity', 'Dignity')}</span><span class="value">{p.get('dignity', '')}</span></div>
        <div class="key-value"><span class="key">{tr('avastha', 'Avastha')}</span><span class="value">{p.get('avastha', {}).get('state', '')}</span></div>
        <div class="key-value"><span class="key">{tr('saptavargaja', 'Saptavargaja')}</span><span class="value">{p.get('saptavargaja_bala', {}).get('percentage', 0)}%</span></div>
        <div class="key-value"><span class="key">{tr('digbala', 'Digbala')}</span><span class="value">{p.get('digbala', {}).get('digbala', 0)}/60</span></div>
        <div class="key-value"><span class="key">{tr('nakshatra_lord', 'Nakshatra Lord')}</span><span class="value">{p.get('nakshatra_lord', '')}</span></div>
        <div class="key-value"><span class="key">{tr('nakshatra_deity', 'Nakshatra Deity')}</span><span class="value">{p.get('nakshatra_deity', '')}</span></div>
        """
    
    # Dasha 5 Levels
    html += f"""
    <div class="page-break"></div>
    <h2>3. {tr('dasha_5', 'Complete Dasha (5 Levels)')}</h2>
    """
    levels = data.get("complete_dasha", {}).get("levels", {})
    level_names = [
        ("mahadasha", tr("mahadasha", "Mahadasha")),
        ("antardasha", tr("antardasha", "Antardasha")),
        ("pratyantardasha", tr("pratyantardasha", "Pratyantardasha")),
        ("sookshma", tr("sookshma", "Sookshma")),
        ("prana", tr("prana", "Prana")),
    ]
    for key, title in level_names:
        level = levels.get(key, {})
        if not level:
            continue
        html += f"""
        <div class="dasha">
            <h3>{title}: {level.get('planet', '')}</h3>
            <p>{tr('period', 'Period')}: {level.get('start_date', '')} - {level.get('end_date', '')}</p>
        """
        if level.get("effects"):
            html += f"<p>{tr('positive', 'Positive')}: {level['effects'].get('positive', '')}</p>"
            html += f"<p>{tr('negative', 'Negative')}: {level['effects'].get('negative', '')}</p>"
        html += "</div>"
    
    # Yogas
    html += f"""
    <div class="page-break"></div>
    <h2>4. {tr('yoga', 'Yoga Analysis')}</h2>
    <p>{tr('total_yogas', 'Total Yogas')}: {data.get('yogas_complete', {}).get('total_yogas', 0)}</p>
    """
    yogas = data.get("yogas_complete", {})
    if yogas.get("auspicious"):
        html += f"<h3>{tr('auspicious', 'Auspicious Yogas')}</h3>"
        for y in yogas["auspicious"]:
            html += f"""
            <div class="yoga">
                <strong>{y['name']}</strong> ({y['strength']})
                <p>{y['effect']}</p>
                <p><em>{tr('classical_ref', 'Classical Ref')}: {y.get('classical_ref', '')}</em></p>
            </div>
            """
    if yogas.get("doshas"):
        html += f"<h3>{tr('doshas', 'Doshas')}</h3>"
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
    <h2>5. {tr('transit', 'Transit + Ashtakavarga')}</h2>
    <p>{tr('overall_verdict', 'Overall Verdict')}: {data.get('transit_ashtakavarga', {}).get('overall_verdict', '')}</p>
    """
    for tr_item in data.get("transit_ashtakavarga", {}).get("transit_analysis", []):
        html += f"""
        <div class="transit">
            <strong>{tr_item['planet']}</strong> in {tr_item['rashi']} (House {tr_item['house']}) — Bindu: {tr_item['bindu']}/8
            <p>{tr('verdict', 'Verdict')}: {tr_item['verdict']}</p>
        </div>
        """
    
    # Varshphal
    html += f"""
    <div class="page-break"></div>
    <h2>6. {tr('varshphal', 'Varshphal (Annual Charts)')}</h2>
    """
    varsh = data.get("varshphal", {})
    for year in ["2026", "2027", "2028"]:
        v = varsh.get(year, {})
        if not v:
            continue
        html += f"""
        <h3>{tr('year', 'Year')} {year}</h3>
        <div class="key-value"><span class="key">{tr('solar_return', 'Solar Return')}</span><span class="value">{v.get('solar_return_date', '')}</span></div>
        <div class="key-value"><span class="key">{tr('muntha', 'Muntha')}</span><span class="value">{v.get('muntha', {}).get('rashi', '')}</span></div>
        <div class="key-value"><span class="key">{tr('year_lord', 'Year Lord')}</span><span class="value">{v.get('year_lord', {}).get('planet', '')}</span></div>
        """
    
    # Nadi/Bhrigu
    html += f"""
    <div class="page-break"></div>
    <h2>7. {tr('nadi', 'Nadi/Bhrigu Karmic Analysis')}</h2>
    """
    nadi = data.get("nadi_bhrigu", {})
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        html += f"""
        <div class="key-value"><span class="key">{tr('nakshatra', 'Nakshatra')}</span><span class="value">{n.get('nakshatra', '')}</span></div>
        <div class="key-value"><span class="key">{tr('nadi_type', 'Nadi')}</span><span class="value">{n.get('nadi', '')}</span></div>
        <div class="key-value"><span class="key">{tr('past_life', 'Past Life')}</span><span class="value">{n.get('past_life', '')}</span></div>
        """
    if nadi.get("karmic_debts"):
        html += f"<h3>{tr('karmic_debts', 'Karmic Debts')}</h3><ul>"
        for k in nadi["karmic_debts"]:
            html += f"<li><strong>{k['name']}</strong> — {k['remedy']}</li>"
        html += "</ul>"
    
    # BNN
    html += f"""
    <div class="page-break"></div>
    <h2>8. {tr('bnn', 'BNN Hidden Gems')}</h2>
    """
    bnn = data.get("bnn_data", {})
    if bnn.get("conjunctions_5_degree"):
        html += f"<h3>{tr('5_degree', '5-Degree Conjunctions')}</h3><ul>"
        for c in bnn["conjunctions_5_degree"]:
            html += f"<li>{c['planets'][0]} + {c['planets'][1]} ({c['degree_diff']}°) — {c['strength']}</li>"
        html += "</ul>"
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        html += f"<h3>{tr('karakas', 'Karakas')}</h3><ul>"
        for k, v in bnn["karakas"]["karakas"].items():
            html += f"<li><strong>{k}</strong>: {v['planet']}</li>"
        html += "</ul>"
    
    # Deep Paragraphs
    html += f"""
    <div class="page-break"></div>
    <h2>9. {tr('paragraphs', 'Deep Paragraph Explanations')}</h2>
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
    <h2>10. {tr('disclaimer', 'Disclaimer')}</h2>
    <p>{tr('disclaimer_text', 'This report is generated using Swiss Ephemeris for actual planetary calculations and classical Vedic astrology principles. It is provided for educational and informational purposes only.')}</p>
    <p class="footer">© 2026 Vastu One · Nagpur, Maharashtra</p>
    </body>
    </html>
    """
    
    return html


def generate_multi_lang_pdf(country: str = "India", lang: str = "en") -> BytesIO:
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
    html_content = build_html(data, t, lang)
    css_content = get_full_css(lang)
    
    buffer = BytesIO()
    HTML(string=html_content).write_pdf(buffer, stylesheets=[CSS(string=css_content)])
    buffer.seek(0)
    return buffer


def save_multi_lang_pdf(country: str = "India", lang: str = "en", output_path: str = None):
    if output_path is None:
        output_path = "reports/" + country + "_" + lang + "_report.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_multi_lang_pdf(country, lang)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating multi-language PDFs...")
    print()
    for lang in ["en", "hi", "mr", "gu", "ta", "te", "bn", "sa"]:
        print(f"Generating {LANGUAGES.get(lang)} ({lang})...")
        path = save_multi_lang_pdf("India", lang)
        if path:
            size = Path(path).stat().st_size
            print(f"  ✅ {path} ({round(size/1024, 1)} KB)")
        else:
            print(f"  ❌ Failed")
        print()
'''

Path("engine/report/pdf_generator_multi_weasy.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/report/pdf_generator_multi_weasy.py").stat().st_size, "bytes")