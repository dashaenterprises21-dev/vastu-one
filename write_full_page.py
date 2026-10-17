from pathlib import Path

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Complete Prediction - Vastu One</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/royal-theme.css">
<style>
.fp-page { max-width: 1300px; margin: 0 auto; padding: 40px 24px 80px; }
.fp-hero { text-align: center; margin-bottom: 30px; }
.fp-hero-eyebrow { display: inline-flex; align-items: center; gap: 14px; font-size: 11px; letter-spacing: 0.32em; color: var(--gold); text-transform: uppercase; font-weight: 600; padding: 8px 20px; border: 1px solid var(--line-gold); border-radius: 100px; margin-bottom: 24px; }
.fp-hero-title { font-family: var(--font-display); font-size: 48px; color: var(--ivory); margin: 0 0 12px 0; font-weight: 500; }
.fp-hero-sub { font-size: 15px; color: var(--ivory-muted); font-style: italic; max-width: 700px; margin: 0 auto; }
.fp-countries { display: flex; gap: 8px; justify-content: center; margin: 24px 0; flex-wrap: wrap; }
.fp-btn { padding: 8px 16px; background: rgba(255,255,255,0.03); border: 1px solid var(--line); border-radius: 100px; color: var(--ivory-muted); font-size: 12px; cursor: pointer; transition: all 0.25s; }
.fp-btn:hover { border-color: var(--gold); color: var(--ivory); }
.fp-btn.active { background: rgba(212,169,97,0.15); border-color: var(--gold); color: var(--gold); }
.fp-tabs { display: flex; gap: 6px; margin: 28px 0 20px; flex-wrap: wrap; border-bottom: 1px solid var(--line); }
.fp-tab { padding: 10px 16px; background: transparent; border: none; color: var(--ivory-muted); font-size: 13px; cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -1px; transition: all 0.25s; }
.fp-tab:hover { color: var(--ivory); }
.fp-tab.active { color: var(--gold); border-bottom-color: var(--gold); }
.fp-content { display: none; }
.fp-content.active { display: block; animation: fadeIn 0.4s; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

.section { background: linear-gradient(135deg, rgba(90,20,32,0.5), rgba(50,10,18,0.65)); border: 1px solid var(--line-gold); border-radius: 16px; padding: 28px; margin-bottom: 20px; }
.section-title { font-family: var(--font-display); font-size: 26px; color: var(--gold); margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--line); }
.subsection { margin-bottom: 24px; }
.subsection-title { font-size: 18px; color: var(--gold); font-weight: 600; margin-bottom: 12px; }
.prediction-item { background: rgba(255,255,255,0.03); border-left: 4px solid var(--gold); border-radius: 10px; padding: 20px; margin-bottom: 14px; }
.prediction-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; flex-wrap: wrap; gap: 10px; }
.prediction-title { font-size: 16px; color: var(--ivory); font-weight: 600; }
.prediction-category { font-size: 10px; color: var(--gold); letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700; background: rgba(212,169,97,0.12); padding: 4px 10px; border-radius: 100px; }
.prediction-body { font-size: 14px; color: var(--ivory); line-height: 1.7; margin-bottom: 10px; }
.prediction-reasoning { font-size: 13px; color: var(--ivory-muted); line-height: 1.6; padding: 12px; background: rgba(0,0,0,0.2); border-radius: 8px; margin-bottom: 10px; }
.prediction-reasoning strong { color: var(--gold); }
.prediction-ref { font-size: 11px; color: var(--gold-deep); font-style: italic; padding-top: 10px; border-top: 1px solid var(--line); }
.confidence { display: inline-block; font-size: 11px; padding: 3px 12px; border-radius: 100px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.conf-High { background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid rgba(239,68,68,0.4); }
.conf-VeryHigh { background: rgba(239,68,68,0.25); color: #fca5a5; border: 1px solid #ef4444; }
.conf-Medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.4); }
.conf-Strong { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.4); }
.conf-Moderate { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.4); }
.conf-Active { background: rgba(139,92,246,0.15); color: #c4b5fd; border: 1px solid rgba(139,92,246,0.4); }

.stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin-bottom: 20px; }
.stat-card { padding: 16px; background: rgba(255,255,255,0.03); border-radius: 12px; border-left: 3px solid var(--gold); }
.stat-label { font-size: 10px; color: var(--gold); letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700; margin-bottom: 6px; }
.stat-value { font-size: 20px; color: var(--ivory); font-weight: 600; font-family: var(--font-display); }
.stat-sub { font-size: 11px; color: var(--ivory-muted); margin-top: 4px; }

.planet-card { background: rgba(255,255,255,0.03); border-radius: 12px; padding: 18px; margin-bottom: 12px; border-left: 4px solid var(--gold); }
.planet-name { font-family: var(--font-display); font-size: 20px; color: var(--gold); font-weight: 600; margin-bottom: 10px; }
.planet-info { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; margin-bottom: 10px; }
.planet-attr { font-size: 12px; }
.planet-attr-label { color: var(--gold-deep); font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; }
.planet-attr-value { color: var(--ivory); font-weight: 500; margin-top: 2px; }
.planet-explanation { font-size: 13px; color: var(--ivory-muted); line-height: 1.7; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--line); }

.loading { text-align: center; padding: 60px; color: var(--ivory-muted); }
@media (max-width: 768px) { .fp-hero-title { font-size: 32px; } .section { padding: 20px; } }
</style>
</head>
<body>
<header class="nav">
  <div class="nav-inner">
    <div class="brand"><a href="/" style="color:inherit;text-decoration:none;">VASTU ONE</a></div>
    <nav class="nav-links">
      <a href="/">Home</a>
      <a href="/world-prediction.html">World</a>
      <a href="/real-transit.html">Real Transit</a>
      <a href="/full-prediction.html" class="active">Full</a>
    </nav>
  </div>
</header>

<main class="fp-page">
  <div class="fp-hero">
    <div class="fp-hero-eyebrow">Complete Astrological Analysis</div>
    <h1 class="fp-hero-title">Full Prediction Report</h1>
    <p class="fp-hero-sub">Swiss Ephemeris calculations with detailed explanations, reasoning, and classical references for every prediction</p>
  </div>

  <div class="fp-countries" id="fpCountries"><div class="loading">Loading...</div></div>
  <div class="fp-tabs" id="fpTabs" style="display:none;">
    <button class="fp-tab active" data-tab="overview">Overview</button>
    <button class="fp-tab" data-tab="planets">Planets</button>
    <button class="fp-tab" data-tab="dasha">Dasha</button>
    <button class="fp-tab" data-tab="yogas">Yogas</button>
    <button class="fp-tab" data-tab="predictions">All Predictions</button>
  </div>
  <div id="fpContent"><div class="loading">Select a country to see detailed analysis</div></div>
</main>

<script>
var DATA = null;

function switchTab(name) {
  document.querySelectorAll('.fp-tab').forEach(function(t) { t.classList.remove('active'); });
  document.querySelectorAll('.fp-content').forEach(function(c) { c.classList.remove('active'); });
  document.querySelector('.fp-tab[data-tab="' + name + '"]').classList.add('active');
  var el = document.getElementById('tab-' + name);
  if (el) el.classList.add('active');
}

function getDashaMeaning(planet) {
  var m = { "Sun": "leadership, authority, government focus", "Moon": "public emotions, water resources, mass movements", "Mars": "military action, conflict, courage, land", "Mercury": "diplomacy, communication, trade, intelligence", "Jupiter": "growth, wisdom, prosperity, spirituality, education", "Venus": "luxury, arts, diplomacy, relationships, aesthetics", "Saturn": "discipline, delays, structural change, labor", "Rahu": "sudden change, transformation, foreign influence, technology", "Ketu": "spirituality, isolation, sudden events, occult" };
  return m[planet] || "general effects";
}

function getPlanetMeaning(planet) {
  var m = { "Sun": "represents leadership, government, authority, and the soul of the nation", "Moon": "represents the public, masses, emotional state, and water resources", "Mars": "represents military, defense, aggression, courage, and land", "Mercury": "represents communication, diplomacy, trade, media, and intelligence", "Jupiter": "represents wisdom, growth, prosperity, law, religion, and education", "Venus": "represents luxury, arts, diplomacy, relationships, and aesthetics", "Saturn": "represents discipline, delays, structure, longevity, and labor", "Rahu": "represents transformation, foreign influence, technology, and sudden change", "Ketu": "represents spirituality, isolation, sudden events, and occult knowledge" };
  return m[planet] || "a specific planetary influence";
}

function getHouseMeaning(house) {
  var m = { 1: "country, leadership, national identity", 2: "wealth, economy, currency, banking", 3: "communication, neighbors, borders, media", 4: "land, earthquakes, natural disasters, public welfare", 5: "education, youth, creativity, political succession", 6: "enemies, war, disease, military, health", 7: "partnerships, alliances, war, international relations", 8: "death, transformations, sudden events, crisis", 9: "dharma, religion, foreign relations, higher learning", 10: "government, politics, leadership, authority", 11: "gains, alliances, economy, income", 12: "losses, foreign, spiritual, espionage" };
  return m[house] || "general matters";
}

function overviewHtml(d) {
  var h = '<div class="section"><div class="section-title">Key Metrics</div><div class="stat-grid">';
  h += '<div class="stat-card"><div class="stat-label">Ascendant</div><div class="stat-value">' + d.chart.ascendant.rashi + '</div><div class="stat-sub">' + d.chart.ascendant.degree + ' deg</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Sun Sign</div><div class="stat-value">' + d.chart.sun.rashi + '</div><div class="stat-sub">' + d.chart.sun.degree + ' deg</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Moon Sign</div><div class="stat-value">' + d.chart.moon.rashi + '</div><div class="stat-sub">' + d.chart.moon.degree + ' deg</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Mahadasha</div><div class="stat-value">' + d.dasha.mahadasha.lord + '</div><div class="stat-sub">Age ' + d.dasha.age_years + '</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Antardasha</div><div class="stat-value">' + d.dasha.antardasha.lord + '</div><div class="stat-sub">Current period</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Strongest Planet</div><div class="stat-value">' + d.shadbala.strongest + '</div><div class="stat-sub">Max Shadbala</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Weakest Planet</div><div class="stat-value">' + d.shadbala.weakest + '</div><div class="stat-sub">Min Shadbala</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Total Yogas</div><div class="stat-value">' + d.yogas.total_yogas + '</div><div class="stat-sub">' + d.yogas.auspicious.length + ' auspicious</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Ashtakavarga</div><div class="stat-value">' + d.ashtakavarga.total + '</div><div class="stat-sub">Total points</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Predictions</div><div class="stat-value">' + d.total_predictions + '</div><div class="stat-sub">All categories</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Varshphal Year</div><div class="stat-value">' + d.varshphal.year + '</div><div class="stat-sub">Muntha: ' + d.varshphal.muntha.rashi + '</div></div>';
  h += '<div class="stat-card"><div class="stat-label">Year Lord</div><div class="stat-value">' + d.varshphal.year_lord.planet + '</div><div class="stat-sub">Annual ruler</div></div>';
  h += '</div></div>';
  
  h += '<div class="section"><div class="section-title">Executive Summary</div>';
  h += '<div class="prediction-item">';
  h += '<div class="prediction-body"><strong>' + d.country + '</strong> is currently in <strong>' + d.dasha.mahadasha.lord + ' Mahadasha</strong> with <strong>' + d.dasha.antardasha.lord + ' Antardasha</strong>. This period emphasizes ' + getDashaMeaning(d.dasha.mahadasha.lord) + '.</div>';
  h += '<div class="prediction-reasoning"><strong>Reasoning:</strong> The Mahadasha lord ' + d.dasha.mahadasha.lord + ' rules the current 16-year period, while ' + d.dasha.antardasha.lord + ' governs the sub-period. Together they create a specific energy pattern.</div>';
  h += '<div class="prediction-ref">Reference: BPHS Ch. 46 - Vimshottari Dasha System</div>';
  h += '</div></div>';
  
  return h;
}

function planetsHtml(d) {
  var h = '<div class="section"><div class="section-title">Planetary Positions with Full Explanation</div>';
  var planets = d.chart.planets || { "Sun": d.chart.sun, "Moon": d.chart.moon };
  Object.entries(planets).forEach(function(e) {
    var name = e[0], p = e[1];
    var nak = p.nakshatra;
    if (typeof nak === 'object' && nak !== null) nak = nak.name;
    h += '<div class="planet-card">';
    h += '<div class="planet-name">' + name + '</div>';
    h += '<div class="planet-info">';
    h += '<div class="planet-attr"><div class="planet-attr-label">Rashi</div><div class="planet-attr-value">' + (p.rashi || '') + '</div></div>';
    h += '<div class="planet-attr"><div class="planet-attr-label">Degree</div><div class="planet-attr-value">' + (p.degree || 0) + ' deg</div></div>';
    h += '<div class="planet-attr"><div class="planet-attr-label">House</div><div class="planet-attr-value">' + (p.house || '') + '</div></div>';
    h += '<div class="planet-attr"><div class="planet-attr-label">Dignity</div><div class="planet-attr-value">' + (p.dignity || 'Neutral') + '</div></div>';
    h += '<div class="planet-attr"><div class="planet-attr-label">Nakshatra</div><div class="planet-attr-value">' + (nak || '') + '</div></div>';
    h += '</div>';
    h += '<div class="planet-explanation"><strong>Meaning:</strong> ' + getPlanetMeaning(name) + '. In house ' + p.house + ', this planet influences ' + getHouseMeaning(p.house) + '.</div>';
    h += '</div>';
  });
  h += '</div>';
  return h;
}

function dashaHtml(d) {
  var h = '<div class="section"><div class="section-title">Vimshottari Dasha - Full Timeline</div>';
  h += '<div class="subsection"><div class="subsection-title">Current Dasha</div>';
  h += '<div class="prediction-item"><div class="prediction-header"><div class="prediction-title">Mahadasha: ' + d.dasha.mahadasha.lord + '</div><span class="confidence conf-High">Active</span></div>';
  h += '<div class="prediction-body">' + getDashaMeaning(d.dasha.mahadasha.lord) + '</div>';
  h += '<div class="prediction-reasoning"><strong>Duration:</strong> Age ' + d.dasha.mahadasha.start_age + ' to ' + d.dasha.mahadasha.end_age + '</div>';
  h += '<div class="prediction-ref">BPHS Ch. 46 - Mahadasha effects</div></div>';
  h += '<div class="prediction-item"><div class="prediction-header"><div class="prediction-title">Antardasha: ' + d.dasha.antardasha.lord + '</div><span class="confidence conf-Medium">Sub-period</span></div>';
  h += '<div class="prediction-body">' + getDashaMeaning(d.dasha.antardasha.lord) + '</div>';
  h += '<div class="prediction-reasoning"><strong>Effect:</strong> ' + d.dasha.mahadasha.lord + '-' + d.dasha.antardasha.lord + ' period creates combined influence</div></div>';
  h += '<div class="prediction-item"><div class="prediction-header"><div class="prediction-title">Pratyantardasha: ' + d.dasha.pratyantardasha.lord + '</div><span class="confidence conf-Moderate">Micro-period</span></div>';
  h += '<div class="prediction-body">' + getDashaMeaning(d.dasha.pratyantardasha.lord) + '</div></div>';
  h += '</div></div>';
  
  h += '<div class="section"><div class="section-title">Full Mahadasha Sequence</div>';
  d.dasha.full_mahadasha_sequence.forEach(function(ds) {
    h += '<div class="prediction-item"><div class="prediction-header"><div class="prediction-title">' + ds.planet + ' (' + ds.lord + ')</div><span class="confidence conf-Moderate">' + ds.years.toFixed(1) + ' years</span></div>';
    h += '<div class="prediction-reasoning"><strong>Period:</strong> Age ' + ds.start_age.toFixed(1) + ' to ' + ds.end_age.toFixed(1) + ' - ' + getDashaMeaning(ds.lord) + '</div></div>';
  });
  h += '</div>';
  return h;
}

function yogasHtml(d) {
  var h = '<div class="section"><div class="section-title">Auspicious Yogas (' + d.yogas.auspicious.length + ')</div>';
  d.yogas.auspicious.forEach(function(y) {
    h += '<div class="prediction-item"><div class="prediction-header"><div class="prediction-title">' + y.name + '</div><span class="confidence conf-' + y.strength + '">' + y.strength + '</span></div>';
    h += '<div class="prediction-body">' + y.effect + '</div>';
    h += '<div class="prediction-reasoning"><strong>Why it matters:</strong> This yoga combines specific planetary energies to produce positive outcomes in the areas mentioned.</div>';
    h += '<div class="prediction-ref">Reference: Phaladeepika Ch. 6 - Yoga combinations</div></div>';
  });
  h += '</div>';
  
  h += '<div class="section"><div class="section-title">Doshas (' + d.yogas.doshas.length + ')</div>';
  d.yogas.doshas.forEach(function(y) {
    h += '<div class="prediction-item" style="border-left-color:#ef4444;"><div class="prediction-header"><div class="prediction-title">' + y.name + '</div><span class="confidence conf-' + y.strength + '">' + y.strength + '</span></div>';
    h += '<div class="prediction-body">' + y.effect + '</div>';
    h += '<div class="prediction-reasoning"><strong>Remedy needed:</strong> This dosha requires specific remedial measures to mitigate its effects.</div>';
    h += '<div class="prediction-ref">Reference: BPHS Ch. 8 - Dosha analysis</div></div>';
  });
  h += '</div>';
  return h;
}

function predictionsHtml(d) {
  var h = '<div class="section"><div class="section-title">All ' + d.total_predictions + ' Predictions with Full Detail</div>';
  var cats = {};
  d.predictions.forEach(function(p) { if (!cats[p.category]) cats[p.category] = []; cats[p.category].push(p); });
  Object.entries(cats).forEach(function(e) {
    h += '<div class="subsection"><div class="subsection-title">' + e[0] + ' (' + e[1].length + ' predictions)</div>';
    e[1].forEach(function(p) {
      h += '<div class="prediction-item"><div class="prediction-header"><div class="prediction-title">' + p.title + '</div><span class="prediction-category">' + p.category + '</span></div>';
      h += '<div class="prediction-body">' + p.prediction + '</div>';
      if (p.confidence) h += '<span class="confidence conf-' + p.confidence + '">' + p.confidence + '</span>';
      h += '</div>';
    });
    h += '</div>';
  });
  h += '</div>';
  return h;
}

async function loadCountry(country) {
  document.querySelectorAll('.fp-btn').forEach(function(b) { b.classList.remove('active'); });
  var btn = document.querySelector('.fp-btn[data-country="' + country + '"]');
  if (btn) btn.classList.add('active');
  
  document.getElementById('fpContent').innerHTML = '<div class="loading">Calculating complete analysis for ' + country + '...</div>';
  document.getElementById('fpTabs').style.display = 'none';
  
  try {
    var res = await fetch('/api/world/full/predict/' + encodeURIComponent(country));
    if (!res.ok) throw new Error('API error: ' + res.status);
    var d = await res.json();
    DATA = d;
    
    var html = '';
    html += '<div id="tab-overview" class="fp-content active">' + overviewHtml(d) + '</div>';
    html += '<div id="tab-planets" class="fp-content">' + planetsHtml(d) + '</div>';
    html += '<div id="tab-dasha" class="fp-content">' + dashaHtml(d) + '</div>';
    html += '<div id="tab-yogas" class="fp-content">' + yogasHtml(d) + '</div>';
    html += '<div id="tab-predictions" class="fp-content">' + predictionsHtml(d) + '</div>';
    
    document.getElementById('fpContent').innerHTML = html;
    document.getElementById('fpTabs').style.display = 'flex';
    document.querySelectorAll('.fp-tab').forEach(function(t) {
      t.onclick = function() { switchTab(t.dataset.tab); };
    });
  } catch (e) {
    document.getElementById('fpContent').innerHTML = '<div class="loading" style="color:#f0a0a0;">Error: ' + e.message + '</div>';
  }
}

function loadCountries() {
  var countries = ['India', 'USA', 'China', 'Russia', 'Pakistan', 'UK', 'Israel', 'Ukraine', 'Japan', 'Germany', 'France', 'Brazil', 'Australia', 'Canada', 'Saudi Arabia', 'Iran', 'North Korea', 'South Korea', 'Nepal', 'Sri Lanka', 'Bangladesh'];
  var h = '';
  countries.forEach(function(c) {
    h += '<button class="fp-btn" data-country="' + c + '" onclick="loadCountry(\\'' + c + '\\')">' + c + '</button>';
  });
  document.getElementById('fpCountries').innerHTML = h;
  loadCountry('India');
}

document.addEventListener('DOMContentLoaded', loadCountries);
</script>
</body>
</html>
"""

Path("frontend/full-prediction.html").write_text(html, encoding="utf-8")
print("File written:", Path("frontend/full-prediction.html").stat().st_size, "bytes")