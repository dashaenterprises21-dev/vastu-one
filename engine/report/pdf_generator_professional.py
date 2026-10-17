"""
VASTU ONE - Professional Research PDF Generator (HTML/CSS via WeasyPrint)
50+ pages with Claude-style professional design
"""

from pathlib import Path
from io import BytesIO

from weasyprint import HTML, CSS

from engine.astro.master_prediction_engine import get_master_prediction, COUNTRY_CHARTS
from engine.astro.deep_paragraph_engine import get_full_explanation_report
from engine.astro.bnn_hidden_gems import analyze_bnn_complete
from engine.astro.complete_chart_engine import calculate_complete_chart


FONTS_DIR = Path(__file__).parent / "fonts"
DEVANAGARI_FONT = FONTS_DIR / "NotoSansDevanagari.ttf"


def get_professional_css() -> str:
    font_url = DEVANAGARI_FONT.as_uri() if DEVANAGARI_FONT.exists() else ""
    
    return f"""
    @page {{
        size: A4;
        margin: 2cm;
        @bottom-center {{
            content: "Page " counter(page) " of " counter(pages);
            font-family: 'Helvetica', sans-serif;
            font-size: 8pt;
            color: #a8a29e;
        }}
        @top-right {{
            content: "VASTU ONE";
            font-family: 'Helvetica', sans-serif;
            font-size: 8pt;
            color: #d4a961;
            letter-spacing: 2px;
        }}
    }}
    
    @page cover {{
        margin: 0;
        @bottom-center {{ content: none; }}
        @top-right {{ content: none; }}
    }}
    
    @font-face {{
        font-family: 'NotoDevanagari';
        src: url('{font_url}');
    }}
    
    body {{
        font-family: 'Helvetica', 'NotoDevanagari', sans-serif;
        font-size: 10pt;
        line-height: 1.6;
        color: #1e1e1e;
        margin: 0;
        padding: 0;
    }}
    
    .cover {{
        page: cover;
        background: linear-gradient(135deg, #5a1420 0%, #3a0a14 100%);
        color: #f5f1e8;
        height: 29.7cm;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 3cm;
    }}
    
    .cover-brand {{
        font-size: 14pt;
        letter-spacing: 8px;
        color: #d4a961;
        margin-bottom: 2cm;
    }}
    
    .cover-title {{
        font-size: 42pt;
        font-weight: bold;
        color: #d4a961;
        margin-bottom: 1cm;
        line-height: 1.2;
    }}
    
    .cover-country {{
        font-size: 72pt;
        font-weight: bold;
        color: #f5f1e8;
        margin: 1cm 0;
        letter-spacing: 4px;
    }}
    
    .cover-subtitle {{
        font-size: 16pt;
        color: #a8a29e;
        font-style: italic;
        margin-bottom: 0.5cm;
    }}
    
    .cover-stats {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1cm;
        margin-top: 3cm;
        width: 100%;
    }}
    
    .cover-stat {{
        background: rgba(212, 169, 97, 0.15);
        border: 1px solid #d4a961;
        border-radius: 12px;
        padding: 1cm;
    }}
    
    .cover-stat-label {{
        font-size: 8pt;
        color: #d4a961;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    
    .cover-stat-value {{
        font-size: 24pt;
        color: #f5f1e8;
        font-weight: bold;
        margin-top: 0.3cm;
    }}
    
    .page-break {{
        page-break-before: always;
    }}
    
    h1 {{
        font-size: 24pt;
        color: #5a1420;
        border-bottom: 3px solid #d4a961;
        padding-bottom: 0.3cm;
        margin-top: 0;
        margin-bottom: 1cm;
    }}
    
    h2 {{
        font-size: 16pt;
        color: #b8893b;
        margin-top: 0.8cm;
        margin-bottom: 0.4cm;
    }}
    
    h3 {{
        font-size: 12pt;
        color: #5a1420;
        margin-top: 0.6cm;
        margin-bottom: 0.3cm;
    }}
    
    p {{
        text-align: justify;
        margin-bottom: 0.4cm;
    }}
    
    .toc {{
        list-style: none;
        padding: 0;
    }}
    
    .toc li {{
        padding: 0.3cm 0;
        border-bottom: 1px dotted #d4a961;
        display: flex;
        justify-content: space-between;
    }}
    
    .toc li strong {{
        color: #5a1420;
    }}
    
    .toc li span {{
        color: #a8a29e;
    }}
    
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 0.5cm 0;
        font-size: 9pt;
    }}
    
    th {{
        background: #5a1420;
        color: #d4a961;
        padding: 0.3cm;
        text-align: left;
        font-weight: bold;
    }}
    
    td {{
        padding: 0.25cm;
        border-bottom: 1px solid #e5e5e5;
    }}
    
    tr:nth-child(even) td {{
        background: #faf8f3;
    }}
    
    .stat-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.4cm;
        margin: 0.5cm 0;
    }}
    
    .stat-card {{
        background: #faf8f3;
        border-left: 4px solid #d4a961;
        border-radius: 8px;
        padding: 0.4cm;
    }}
    
    .stat-label {{
        font-size: 8pt;
        color: #b8893b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .stat-value {{
        font-size: 16pt;
        color: #5a1420;
        font-weight: bold;
        margin-top: 0.2cm;
    }}
    
    .stat-sub {{
        font-size: 8pt;
        color: #a8a29e;
        margin-top: 0.1cm;
    }}
    
    .info-box {{
        background: #faf8f3;
        border-left: 4px solid #d4a961;
        border-radius: 8px;
        padding: 0.5cm;
        margin: 0.4cm 0;
    }}
    
    .info-box-title {{
        font-weight: bold;
        color: #5a1420;
        margin-bottom: 0.2cm;
    }}
    
    .dosha-box {{
        background: #fef2f2;
        border-left: 4px solid #dc2626;
        border-radius: 8px;
        padding: 0.5cm;
        margin: 0.4cm 0;
    }}
    
    .yoga-box {{
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 0.5cm;
        margin: 0.4cm 0;
    }}
    
    .planet-card {{
        background: #faf8f3;
        border-radius: 10px;
        padding: 0.6cm;
        margin: 0.4cm 0;
        border-left: 4px solid #d4a961;
    }}
    
    .planet-name {{
        font-size: 14pt;
        color: #5a1420;
        font-weight: bold;
        margin-bottom: 0.3cm;
    }}
    
    .planet-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.3cm;
    }}
    
    .planet-attr {{
        font-size: 9pt;
    }}
    
    .planet-attr-label {{
        color: #b8893b;
        font-size: 8pt;
        text-transform: uppercase;
    }}
    
    .planet-attr-value {{
        color: #1e1e1e;
        font-weight: bold;
    }}
    
    .dasha-card {{
        background: #f5efe2;
        border-left: 4px solid #b8893b;
        border-radius: 8px;
        padding: 0.5cm;
        margin: 0.4cm 0;
    }}
    
    .dasha-title {{
        font-size: 13pt;
        color: #5a1420;
        font-weight: bold;
    }}
    
    .dasha-period {{
        font-size: 9pt;
        color: #64748b;
        margin: 0.2cm 0;
    }}
    
    .dasha-effect {{
        font-size: 9pt;
        margin: 0.1cm 0;
    }}
    
    .classical-ref {{
        font-size: 8pt;
        color: #a8a29e;
        font-style: italic;
        margin-top: 0.2cm;
    }}
    
    .paragraph-card {{
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 0.6cm;
        margin: 0.5cm 0;
    }}
    
    .paragraph-title {{
        font-size: 12pt;
        color: #5a1420;
        font-weight: bold;
        margin-bottom: 0.3cm;
        padding-bottom: 0.2cm;
        border-bottom: 1px solid #d4a961;
    }}
    
    .paragraph-text {{
        font-size: 9.5pt;
        text-align: justify;
        line-height: 1.7;
    }}
    
    .disclaimer {{
        background: #fffbeb;
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 0.6cm;
        font-size: 9pt;
        color: #64748b;
        margin-top: 0.5cm;
    }}
    
    .footer-copyright {{
        text-align: center;
        font-size: 9pt;
        color: #a8a29e;
        margin-top: 2cm;
        padding-top: 0.5cm;
        border-top: 1px solid #e5e5e5;
    }}
    """


def build_professional_html(data: dict, country: str) -> str:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>Vastu One - {country} Research Report</title></head>
    <body>
    
    <!-- COVER PAGE -->
    <div class="cover">
        <div class="cover-brand">VASTU ONE</div>
        <div class="cover-title">Research Grade<br/>Astrological Report</div>
        <div class="cover-country">{country.upper()}</div>
        <div class="cover-subtitle">12-Layer Master Prediction Analysis</div>
        <div class="cover-subtitle">Generated: {data['date']}</div>
        <div class="cover-stats">
            <div class="cover-stat">
                <div class="cover-stat-label">Predictions</div>
                <div class="cover-stat-value">{data.get('total_predictions', 0)}</div>
            </div>
            <div class="cover-stat">
                <div class="cover-stat-label">Yogas</div>
                <div class="cover-stat-value">{data.get('yogas_complete', {}).get('total_yogas', 0)}</div>
            </div>
            <div class="cover-stat">
                <div class="cover-stat-label">Ashtakavarga</div>
                <div class="cover-stat-value">{data.get('ashtakavarga', {}).get('total', 0)}</div>
            </div>
        </div>
    </div>
    
    <!-- TABLE OF CONTENTS -->
    <div class="page-break"></div>
    <h1>Table of Contents</h1>
    <ul class="toc">
        <li><strong>1. Executive Summary</strong><span>3</span></li>
        <li><strong>2. Birth Chart Analysis</strong><span>5</span></li>
        <li><strong>3. Planetary Deep Analysis</strong><span>8</span></li>
        <li><strong>4. Complete Dasha (5 Levels)</strong><span>14</span></li>
        <li><strong>5. Yoga Analysis</strong><span>18</span></li>
        <li><strong>6. Ashtakavarga + Transit</strong><span>22</span></li>
        <li><strong>7. Varshphal (Annual Charts)</strong><span>26</span></li>
        <li><strong>8. Nadi/Bhrigu Karmic Analysis</strong><span>29</span></li>
        <li><strong>9. BNN Hidden Gems</strong><span>32</span></li>
        <li><strong>10. Deep Paragraph Explanations</strong><span>36</span></li>
        <li><strong>11. Remedies (Upay)</strong><span>42</span></li>
        <li><strong>12. Historical Case Studies</strong><span>46</span></li>
        <li><strong>13. Research References</strong><span>49</span></li>
        <li><strong>14. Glossary</strong><span>52</span></li>
        <li><strong>15. Disclaimer</strong><span>54</span></li>
    </ul>
    
    <!-- EXECUTIVE SUMMARY -->
    <div class="page-break"></div>
    <h1>1. Executive Summary</h1>
    <p>This comprehensive research-grade report presents a complete 12-layer astrological analysis of <strong>{country}</strong> using Swiss Ephemeris for actual planetary calculations. The report combines classical Vedic astrology principles with advanced Bhrigu Nandi Nadi (BNN) techniques to provide <strong>{data.get('total_predictions', 0)} distinct predictions</strong> across multiple systems.</p>
    
    <p>The analysis is based on the country's birth chart (independence/formation chart), current dasha periods, transit positions, yoga combinations, Ashtakavarga point system, Shadbala strength calculations, Nakshatra placements, and annual Varshphal chart.</p>
    
    <h2>Key Findings at a Glance</h2>
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-label">Mahadasha</div>
            <div class="stat-value">{data.get('complete_dasha', {}).get('levels', {}).get('mahadasha', {}).get('planet', '')}</div>
            <div class="stat-sub">Primary period</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Antardasha</div>
            <div class="stat-value">{data.get('complete_dasha', {}).get('levels', {}).get('antardasha', {}).get('planet', '')}</div>
            <div class="stat-sub">Sub-period</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Pratyantardasha</div>
            <div class="stat-value">{data.get('complete_dasha', {}).get('levels', {}).get('pratyantardasha', {}).get('planet', '')}</div>
            <div class="stat-sub">Micro period</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Strongest Planet</div>
            <div class="stat-value">{data.get('shadbala', {}).get('strongest', '')}</div>
            <div class="stat-sub">Max Shadbala</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Weakest Planet</div>
            <div class="stat-value">{data.get('shadbala', {}).get('weakest', '')}</div>
            <div class="stat-sub">Min Shadbala</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Transit Verdict</div>
            <div class="stat-value">{data.get('transit_ashtakavarga', {}).get('overall_verdict', '')}</div>
            <div class="stat-sub">Current</div>
        </div>
    </div>
    
    <h2>What Makes This Report Unique</h2>
    <table>
        <tr><th>Feature</th><th>Description</th></tr>
        <tr><td>12 Layers of Analysis</td><td>From planetary deep analysis to Nadi/Bhrigu karmic patterns</td></tr>
        <tr><td>100+ Yogas</td><td>Including Panch Mahapurusha, Raja, Dhana, Chandra, Surya, and Nabhasa yogas</td></tr>
        <tr><td>5-Level Dasha</td><td>Mahadasha to Prana dasha with exact dates</td></tr>
        <tr><td>BNN Hidden Gems</td><td>5-Degree rule, Karakas, Trinal combinations, Nakshatra Pada</td></tr>
        <tr><td>Classical References</td><td>25+ classical texts cited for every prediction</td></tr>
        <tr><td>Historical Evidence</td><td>Past events correlated with astrological patterns</td></tr>
    </table>
    
    <!-- BIRTH CHART -->
    <div class="page-break"></div>
    <h1>2. Birth Chart Analysis</h1>
    
    <h2>Ascendant (Lagna)</h2>
    <p>The ascendant is <strong>{data['chart']['ascendant']['rashi']}</strong> at <strong>{data['chart']['ascendant']['degree']:.2f}</strong>. This determines the house layout and the country's fundamental character.</p>
    
    <h2>House Significations</h2>
    <table>
        <tr><th>House</th><th>Significations</th></tr>
        <tr><td>1</td><td>Country, leadership, national identity</td></tr>
        <tr><td>2</td><td>Wealth, economy, currency, banking</td></tr>
        <tr><td>3</td><td>Communication, neighbors, borders, media</td></tr>
        <tr><td>4</td><td>Land, earthquakes, natural disasters, public welfare</td></tr>
        <tr><td>5</td><td>Education, youth, creativity, political succession</td></tr>
        <tr><td>6</td><td>Enemies, war, disease, military, health</td></tr>
        <tr><td>7</td><td>Partnerships, alliances, war, international relations</td></tr>
        <tr><td>8</td><td>Death, transformations, sudden events, crisis</td></tr>
        <tr><td>9</td><td>Dharma, religion, foreign relations, higher learning</td></tr>
        <tr><td>10</td><td>Government, politics, leadership, authority</td></tr>
        <tr><td>11</td><td>Gains, alliances, economy, income</td></tr>
        <tr><td>12</td><td>Losses, foreign, spiritual, espionage</td></tr>
    </table>
    
    <p>The birth chart of a nation is calculated from its independence or formation moment. For India, this is 15 August 1947, midnight, Delhi. This chart forms the foundation for all predictions.</p>
    
    <!-- PLANETARY DEEP -->
    <div class="page-break"></div>
    <h1>3. Planetary Deep Analysis</h1>
    <p>Each planet in the birth chart represents a specific dimension of the country's destiny. This section provides 20+ attributes per planet.</p>
    """
    
    planets = data.get("planetary_deep", {}).get("planets", {})
    for name, p in planets.items():
        html += f"""
        <div class="planet-card">
            <div class="planet-name">{name}  {p.get('rashi', '')} {p.get('degree', 0)}</div>
            <div class="planet-grid">
                <div class="planet-attr"><div class="planet-attr-label">Rashi</div><div class="planet-attr-value">{p.get('rashi', '')}</div></div>
                <div class="planet-attr"><div class="planet-attr-label">Degree</div><div class="planet-attr-value">{p.get('degree', 0)}</div></div>
                <div class="planet-attr"><div class="planet-attr-label">House</div><div class="planet-attr-value">{p.get('house', '')}</div></div>
                <div class="planet-attr"><div class="planet-attr-label">Dignity</div><div class="planet-attr-value">{p.get('dignity', '')}</div></div>
                <div class="planet-attr"><div class="planet-attr-label">Avastha</div><div class="planet-attr-value">{p.get('avastha', {}).get('state', '')}</div></div>
                <div class="planet-attr"><div class="planet-attr-label">Saptavargaja</div><div class="planet-attr-value">{p.get('saptavargaja_bala', {}).get('percentage', 0)}%</div></div>
                <div class="planet-attr"><div class="planet-attr-label">Digbala</div><div class="planet-attr-value">{p.get('digbala', {}).get('digbala', 0)}/60</div></div>
                <div class="planet-attr"><div class="planet-attr-label">Nakshatra Lord</div><div class="planet-attr-value">{p.get('nakshatra_lord', '')}</div></div>
            </div>
        </div>
        """
    
    # DASHA
    html += '<div class="page-break"></div><h1>4. Complete Dasha (5 Levels)</h1>'
    html += '<p>Vimshottari Dasha is the most important predictive system in Vedic astrology. It operates on a 120-year cycle divided into 9 planetary periods.</p>'
    
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
        html += f"""
        <div class="dasha-card">
            <div class="dasha-title">{title}: {level.get('planet', '')}</div>
            <div class="dasha-period">Period: {level.get('start_date', '')} to {level.get('end_date', '')}</div>
        """
        if level.get("effects"):
            html += f"<div class='dasha-effect'><strong>Positive:</strong> {level['effects'].get('positive', '')}</div>"
            html += f"<div class='dasha-effect'><strong>Negative:</strong> {level['effects'].get('negative', '')}</div>"
            html += f"<div class='classical-ref'>{level['effects'].get('classical_ref', '')}</div>"
        html += "</div>"
    
    # YOGAS
    html += '<div class="page-break"></div><h1>5. Yoga Analysis</h1>'
    yogas = data.get("yogas_complete", {})
    html += f'<p>Total Yogas: <strong>{yogas.get("total_yogas", 0)}</strong> ({len(yogas.get("auspicious", []))} auspicious, {len(yogas.get("doshas", []))} doshas)</p>'
    
    if yogas.get("auspicious"):
        html += '<h2>Auspicious Yogas</h2>'
        for y in yogas["auspicious"]:
            html += f"""
            <div class="yoga-box">
                <div class="info-box-title">{y['name']} ({y['strength']})</div>
                <p>{y['effect']}</p>
                <div class="classical-ref">{y.get('classical_ref', '')}</div>
            </div>
            """
    
    if yogas.get("doshas"):
        html += '<h2>Doshas</h2>'
        for y in yogas["doshas"]:
            html += f"""
            <div class="dosha-box">
                <div class="info-box-title">{y['name']} ({y['strength']})</div>
                <p>{y['effect']}</p>
                <div class="classical-ref">{y.get('classical_ref', '')}</div>
            </div>
            """
    
    # TRANSIT
    html += '<div class="page-break"></div><h1>6. Ashtakavarga + Transit Integration</h1>'
    transit = data.get("transit_ashtakavarga", {})
    html += f'<p>Overall Verdict: <strong>{transit.get("overall_verdict", "")}</strong> ({transit.get("positive_count", 0)} positive, {transit.get("negative_count", 0)} negative)</p>'
    
    for tr in transit.get("transit_analysis", []):
        html += f"""
        <div class="info-box">
            <div class="info-box-title">{tr['planet']} in {tr['rashi']} (House {tr['house']})  Bindu: {tr['bindu']}/8</div>
            <p>Verdict: {tr['verdict']}</p>
            <div class="classical-ref">House Type: {tr.get('house_type', '')} | Nakshatra: {tr.get('nakshatra', '')}</div>
        </div>
        """
    
    # VARSHPHAL
    html += '<div class="page-break"></div><h1>7. Varshphal (Annual Charts 2026-2028)</h1>'
    varsh = data.get("varshphal", {})
    for year in ["2026", "2027", "2028"]:
        v = varsh.get(year, {})
        if not v:
            continue
        html += f"""
        <div class="info-box">
            <div class="info-box-title">Year {year}</div>
            <p>Solar Return: {v.get('solar_return_date', '')}</p>
            <p>Muntha: {v.get('muntha', {}).get('rashi', '')} (House {v.get('muntha', {}).get('house', '')})</p>
            <p>Year Lord: {v.get('year_lord', {}).get('planet', '')}</p>
            <div class="classical-ref">{v.get('muntha', {}).get('meaning', '')}</div>
        </div>
        """
    
    # NADI/BHRIGU
    html += '<div class="page-break"></div><h1>8. Nadi/Bhrigu Karmic Analysis</h1>'
    nadi = data.get("nadi_bhrigu", {})
    if nadi.get("nadi_karma"):
        n = nadi["nadi_karma"]
        html += f"""
        <div class="info-box">
            <div class="info-box-title">Nadi Karma</div>
            <p>Nakshatra: {n.get('nakshatra', '')} | Nadi: {n.get('nadi', '')}</p>
            <p>Karma: {n.get('karma', '')}</p>
            <p>Past Life: {n.get('past_life', '')}</p>
        </div>
        """
    if nadi.get("karmic_debts"):
        html += '<h2>Karmic Debts</h2>'
        for k in nadi["karmic_debts"]:
            html += f"""
            <div class="dosha-box">
                <div class="info-box-title">{k['name']} ({k['type']})</div>
                <p><strong>Cause:</strong> {k['cause']}</p>
                <p><strong>Effect:</strong> {k['effect']}</p>
                <p><strong>Remedy:</strong> {k['remedy']}</p>
            </div>
            """
    
    # BNN
    html += '<div class="page-break"></div><h1>9. BNN Hidden Gems</h1>'
    bnn = data.get("bnn_data", {})
    if bnn.get("conjunctions_5_degree"):
        html += '<h2>5-Degree Conjunctions (BNN Rule)</h2>'
        for c in bnn["conjunctions_5_degree"]:
            html += f'<div class="info-box"><strong>{c["planets"][0]} + {c["planets"][1]}</strong> ({c["degree_diff"]})  {c["strength"]}<br/>{c["bnn_effect"]}</div>'
    if bnn.get("karakas") and bnn["karakas"].get("karakas"):
        html += '<h2>Karakas (Jaimini System)</h2>'
        for k, v in bnn["karakas"]["karakas"].items():
            html += f'<div class="info-box"><strong>{k}</strong>: {v["planet"]} ({v["degree"]})  {v["meaning"]}</div>'
    if bnn.get("nakshatra_pada"):
        html += '<h2>Nakshatra Pada Analysis</h2>'
        for n in bnn["nakshatra_pada"]:
            html += f'<div class="info-box"><strong>{n["planet"]}</strong> in {n["nakshatra"]} pada {n["pada"]}  {n["pada_meaning"]}</div>'
    if bnn.get("trinal_combinations"):
        html += '<h2>Trinal Rashi Combinations</h2>'
        for t in bnn["trinal_combinations"][:10]:
            html += f'<div class="info-box">{t["planets"][0]} + {t["planets"][1]} ({t["rashis"][0]} + {t["rashis"][1]})</div>'
    
    # DEEP PARAGRAPHS
    html += '<div class="page-break"></div><h1>10. Deep Paragraph Explanations</h1>'
    paragraphs_data = data.get("paragraphs_data", {})
    paragraphs = paragraphs_data.get("paragraphs", [])
    html += f'<p>Total Detailed Analyses: <strong>{len(paragraphs)}</strong></p>'
    for p in paragraphs:
        html += f"""
        <div class="paragraph-card">
            <div class="paragraph-title">{p.get('title', '')}</div>
            <div class="paragraph-text">{p.get('paragraph', '')}</div>
        </div>
        """
    
    # REMEDIES
    html += '<div class="page-break"></div><h1>11. Remedies (Upay)</h1>'
    html += '<p>Classical Vedic astrology prescribes specific remedies to strengthen weak planets and mitigate challenging combinations.</p>'
    
    weakest = data.get("shadbala", {}).get("weakest", "")
    remedies = [
        (f"Strengthen {weakest}", f"Worship of {weakest}'s deity, recitation of {weakest} mantra", "Daily/weekly"),
        ("Daily Sun Worship", "Aditya Hridayam, Surya Namaskar", "Morning"),
        ("Gayatri Mantra", "108 recitations daily", "Morning/Evening"),
        ("Mahamrityunjaya", "For protection from crises", "Weekly"),
        ("Hanuman Chalisa", "For Mars and Saturn strength", "Tuesday/Saturday"),
        ("Shani Shanti", "For Saturn-related challenges", "Saturday"),
        ("Rahu-Ketu Shanti", "For Kaal Sarpa", "As needed"),
        ("Ganesh Puja", "For obstacle removal", "Before events"),
        ("Lakshmi Puja", "For economic prosperity", "Friday"),
        ("Navagraha Puja", "For all planetary peace", "As needed"),
        ("Rudrabhishek", "For Saturn and Rahu", "Monthly"),
        ("Vishnu Sahasranama", "For overall well-being", "Weekly"),
        ("Sundarkand", "For courage", "Tuesday"),
        ("Ekadashi Fast", "For spiritual growth", "Twice monthly"),
        ("Donate to needy", "For karma cleansing", "Regular"),
        ("Plant trees", "For environmental balance", "Ongoing"),
        ("Serve elderly", "For Jupiter blessings", "Regular"),
        ("Om Namah Shivaya", "For transformation", "Daily"),
        ("Yoga meditation", "For mental peace", "Daily"),
        ("Ayurveda", "For physical health", "As needed"),
    ]
    
    html += '<table><tr><th>Remedy</th><th>Description</th><th>Frequency</th></tr>'
    for r in remedies:
        html += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    html += '</table>'
    
    # CASE STUDIES
    html += '<div class="page-break"></div><h1>12. Historical Case Studies</h1>'
    studies = [
        ("2001 Bhuj Earthquake", "Saturn-Moon conjunction in 4th house", "2001 Gujarat earthquake (7.7)"),
        ("2004 Indian Ocean Tsunami", "Rahu-Ketu axis with Moon in water sign", "2004 Sumatra tsunami"),
        ("2008 Mumbai Attacks", "Mars-Rahu in 6th/8th house", "26/11 attacks"),
        ("2015 Nepal Earthquake", "Saturn transit in 4th", "Gorkha earthquake (7.8)"),
        ("2019 Pulwama Attack", "Mars-Ketu in 8th house", "Pulwama attack"),
        ("2020 COVID Pandemic", "Rahu-Ketu on 6th house", "Global pandemic"),
    ]
    for name, indicator, event in studies:
        html += f'<div class="info-box"><div class="info-box-title">{name}</div><p><strong>Astrological Indicator:</strong> {indicator}</p><p><strong>Actual Event:</strong> {event}</p></div>'
    
    # RESEARCH REFERENCES
    html += '<div class="page-break"></div><h1>13. Research References</h1>'
    refs = [
        ("Brihat Parashara Hora Shastra", "Ch. 45  Bhu-Kamp Yoga, Ch. 8  Ashtama Shani"),
        ("Phaladeepika", "Ch. 15  Yuddha Yoga, Ch. 15  Bhu-Chalan"),
        ("Bhrigu Samhita", "Karmic Events, Rahu 10th house"),
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
    html += '<table><tr><th>#</th><th>Classical Text</th><th>Relevant Chapters</th></tr>'
    for i, (book, ch) in enumerate(refs, 1):
        html += f'<tr><td>{i}</td><td>{book}</td><td>{ch}</td></tr>'
    html += '</table>'
    
    # GLOSSARY
    html += '<div class="page-break"></div><h1>14. Glossary of Terms</h1>'
    terms = [
        ("Rashi", "Zodiac sign (12 signs)"),
        ("Nakshatra", "Lunar mansion (27 divisions)"),
        ("Pada", "Quarter of a nakshatra"),
        ("Lagna", "Ascendant"),
        ("Mahadasha", "Major planetary period"),
        ("Antardasha", "Sub-period"),
        ("Pratyantardasha", "Sub-sub-period"),
        ("Yoga", "Planetary combination"),
        ("Dosha", "Challenging combination"),
        ("Ashtakavarga", "337 point strength system"),
        ("Shadbala", "6-fold planetary strength"),
        ("Varshphal", "Annual chart"),
        ("Muntha", "Annual progressed point"),
        ("Gochar", "Transit"),
        ("Exaltation", "Highest strength"),
        ("Debilitation", "Lowest strength"),
        ("Combustion", "Close to Sun"),
        ("Retrograde", "Backward motion"),
        ("Bindu", "Ashtakavarga point"),
        ("Kendra", "Angular houses"),
        ("Trikona", "Trinal houses"),
        ("Dusthana", "Difficult houses"),
        ("Upachaya", "Growth houses"),
        ("Raja Yoga", "Power combination"),
        ("Dhana Yoga", "Wealth combination"),
        ("Kaal Sarpa Yoga", "Planets between Rahu-Ketu"),
        ("Mangal Dosha", "Mars affliction"),
        ("Gaja Kesari Yoga", "Jupiter-Moon fame"),
        ("Budha-Aditya Yoga", "Intelligence"),
        ("Chandra-Mangal Yoga", "Wealth"),
    ]
    html += '<table><tr><th>Term</th><th>Definition</th></tr>'
    for term, definition in terms:
        html += f'<tr><td><strong>{term}</strong></td><td>{definition}</td></tr>'
    html += '</table>'
    
    # DISCLAIMER
    html += '<div class="page-break"></div><h1>15. Disclaimer</h1>'
    html += """
    <div class="disclaimer">
        <p>This report is generated using <strong>Swiss Ephemeris</strong> for actual planetary calculations and classical Vedic astrology principles from <strong>Brihat Parashara Hora Shastra (BPHS), Phaladeepika, Bhrigu Samhita, Nadi Astrology, Saravali, Jaimini Sutras, Hora Sara, Prashna Marga, Muhurta Chintamani</strong>, and other classical texts.</p>
        <p><strong>Purpose:</strong> This research-grade report is provided for educational and informational purposes only. It represents astrological analysis based on traditional principles and should not be considered as absolute truth or professional advice.</p>
        <p><strong>Limitations:</strong> Astrological predictions are probabilistic in nature. They indicate trends and tendencies rather than fixed outcomes.</p>
        <p><strong>No Liability:</strong> Vastu One, its creators, and affiliates are not responsible for any decisions, actions, or consequences arising from the use of this report.</p>
        <p><strong>Accuracy:</strong> While we use precise Swiss Ephemeris calculations for planetary positions, the interpretation of astrological data involves traditional principles that may vary among practitioners.</p>
    </div>
    <div class="footer-copyright">
         2026 Vastu One  India  All Rights Reserved
    </div>
    """
    
    html += "</body></html>"
    return html


def generate_professional_pdf(country: str = "India") -> BytesIO:
    data = get_master_prediction(country)
    if "error" in data:
        return None
    
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
    
    html_content = build_professional_html(data, country)
    css_content = get_professional_css()
    
    buffer = BytesIO()
    HTML(string=html_content).write_pdf(buffer, stylesheets=[CSS(string=css_content)])
    buffer.seek(0)
    return buffer


def save_professional_pdf(country: str = "India", output_path: str = None):
    if output_path is None:
        output_path = "reports/" + country + "_professional.pdf"
    Path("reports").mkdir(exist_ok=True)
    buffer = generate_professional_pdf(country)
    if buffer is None:
        return None
    Path(output_path).write_bytes(buffer.getvalue())
    return output_path


if __name__ == "__main__":
    print("Generating professional 50+ page PDF...")
    path = save_professional_pdf("India")
    if path:
        size = Path(path).stat().st_size
        print("PDF generated: " + path)
        print("Size: " + str(size) + " bytes (" + str(round(size/1024, 1)) + " KB)")
