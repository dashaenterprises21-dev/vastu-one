from pathlib import Path

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vastu One  Complete Vedic Tech Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/royal-theme.css">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --gold: #d4a961;
  --gold-deep: #b8893b;
  --dark-red: #5a1420;
  --dark-red-deep: #3a0a14;
  --ivory: #f5f1e8;
  --ivory-muted: #a8a29e;
  --bg: #0a0608;
  --bg-card: rgba(90,20,32,0.3);
  --border: rgba(212,169,97,0.2);
}
html { scroll-behavior: smooth; }
body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--ivory); overflow-x: hidden; line-height: 1.6; }

/* NAVBAR */
.navbar { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; padding: 1rem 2rem; background: rgba(10,6,8,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); transition: all 0.3s; }
.navbar-inner { max-width: 1400px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
.navbar-brand { font-family: 'Fraunces', serif; font-size: 24px; color: var(--gold); letter-spacing: 3px; text-decoration: none; font-weight: 500; }
.navbar-brand span { color: var(--ivory); }
.navbar-links { display: flex; gap: 2rem; align-items: center; }
.navbar-links a { color: var(--ivory-muted); text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.3s; position: relative; }
.navbar-links a:hover { color: var(--gold); }
.navbar-links a::after { content: ''; position: absolute; bottom: -4px; left: 0; width: 0; height: 2px; background: var(--gold); transition: width 0.3s; }
.navbar-links a:hover::after { width: 100%; }
.navbar-actions { display: flex; gap: 1rem; align-items: center; }
.navbar-btn { padding: 10px 24px; border-radius: 100px; font-size: 13px; font-weight: 600; text-decoration: none; transition: all 0.3s; display: inline-flex; align-items: center; gap: 6px; }
.navbar-btn-login { background: transparent; color: var(--ivory); border: 1px solid var(--border); }
.navbar-btn-login:hover { border-color: var(--gold); background: rgba(212,169,97,0.1); }
.navbar-btn-signup { background: linear-gradient(135deg, var(--gold), var(--gold-deep)); color: var(--dark-red-deep); box-shadow: 0 4px 20px rgba(212,169,97,0.3); }
.navbar-btn-signup:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(212,169,97,0.5); }
.mobile-menu-btn { display: none; background: none; border: none; color: var(--gold); font-size: 24px; cursor: pointer; }

/* HERO */
.hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 8rem 2rem 4rem; position: relative; background: radial-gradient(ellipse at top, rgba(90,20,32,0.6) 0%, var(--bg) 70%); overflow: hidden; }
.hero::before { content: ''; position: absolute; inset: 0; background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23d4a961' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"); opacity: 0.5; }
.hero-content { position: relative; z-index: 1; max-width: 1000px; }
.hero-badge { display: inline-flex; align-items: center; gap: 10px; font-size: 11px; letter-spacing: 0.3em; color: var(--gold); text-transform: uppercase; font-weight: 600; padding: 10px 24px; border: 1px solid rgba(212,169,97,0.4); border-radius: 100px; margin-bottom: 2rem; background: rgba(212,169,97,0.05); animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
.hero h1 { font-family: 'Fraunces', serif; font-size: 82px; font-weight: 400; line-height: 1.05; margin-bottom: 1.5rem; background: linear-gradient(135deg, var(--ivory) 0%, var(--gold) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: -0.02em; }
.hero p { font-size: 22px; color: var(--ivory-muted); max-width: 750px; margin: 0 auto 3rem; line-height: 1.7; font-style: italic; }
.hero-cta { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 5rem; }
.btn { padding: 18px 40px; border-radius: 100px; font-size: 15px; font-weight: 600; text-decoration: none; transition: all 0.3s; letter-spacing: 0.5px; display: inline-flex; align-items: center; gap: 10px; }
.btn-primary { background: linear-gradient(135deg, var(--gold), var(--gold-deep)); color: var(--dark-red-deep); box-shadow: 0 10px 40px rgba(212,169,97,0.3); }
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 15px 50px rgba(212,169,97,0.5); }
.btn-secondary { background: transparent; color: var(--ivory); border: 1px solid rgba(212,169,97,0.4); }
.btn-secondary:hover { border-color: var(--gold); background: rgba(212,169,97,0.1); transform: translateY(-3px); }

/* STATS BAR */
.stats-bar { display: flex; justify-content: center; gap: 5rem; flex-wrap: wrap; padding-top: 3rem; border-top: 1px solid var(--border); }
.stat-item { text-align: center; }
.stat-number { font-family: 'Fraunces', serif; font-size: 52px; color: var(--gold); font-weight: 500; line-height: 1; }
.stat-label { font-size: 11px; color: var(--ivory-muted); letter-spacing: 0.15em; text-transform: uppercase; margin-top: 0.75rem; font-weight: 600; }

/* SECTION COMMON */
section { padding: 7rem 2rem; }
.container { max-width: 1300px; margin: 0 auto; }
.section-header { text-align: center; margin-bottom: 4rem; }
.section-eyebrow { font-size: 12px; color: var(--gold); letter-spacing: 0.3em; text-transform: uppercase; font-weight: 700; margin-bottom: 1rem; display: inline-block; padding: 6px 20px; border: 1px solid var(--border); border-radius: 100px; }
.section-title { font-family: 'Fraunces', serif; font-size: 52px; font-weight: 400; margin-bottom: 1rem; line-height: 1.15; }
.section-subtitle { font-size: 18px; color: var(--ivory-muted); max-width: 650px; margin: 0 auto; font-style: italic; }

/* MODULES */
.modules { background: linear-gradient(180deg, var(--bg), rgba(90,20,32,0.15), var(--bg)); }
.modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 24px; }
.module-card { background: linear-gradient(135deg, rgba(90,20,32,0.5), rgba(50,10,18,0.7)); border: 1px solid var(--border); border-radius: 20px; padding: 36px; transition: all 0.4s; cursor: pointer; position: relative; overflow: hidden; text-decoration: none; display: block; }
.module-card::before { content: ''; position: absolute; top: 0; left: 36px; right: 36px; height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); opacity: 0; transition: opacity 0.4s; }
.module-card:hover { transform: translateY(-8px); border-color: var(--gold); box-shadow: 0 40px 80px -20px rgba(212,169,97,0.35); }
.module-card:hover::before { opacity: 1; }
.module-icon { width: 64px; height: 64px; border-radius: 16px; background: rgba(212,169,97,0.12); display: flex; align-items: center; justify-content: center; font-size: 30px; margin-bottom: 24px; border: 1px solid rgba(212,169,97,0.3); }
.module-title { font-family: 'Fraunces', serif; font-size: 26px; color: var(--ivory); margin-bottom: 12px; font-weight: 500; }
.module-desc { font-size: 14px; color: var(--ivory-muted); line-height: 1.7; margin-bottom: 20px; }
.module-features { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
.module-feature { font-size: 13px; color: var(--gold); display: flex; align-items: center; gap: 8px; }
.module-feature::before { content: ''; font-size: 8px; }
.module-link { font-size: 14px; color: var(--gold); font-weight: 600; display: inline-flex; align-items: center; gap: 6px; letter-spacing: 0.5px; transition: gap 0.3s; }
.module-card:hover .module-link { gap: 12px; }

/* FEATURES */
.features { background: var(--bg); }
.features-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 3rem; }
.feature-card { padding: 32px; border-radius: 16px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); transition: all 0.3s; }
.feature-card:hover { border-color: rgba(212,169,97,0.4); background: rgba(212,169,97,0.04); transform: translateY(-4px); }
.feature-icon { font-size: 36px; margin-bottom: 20px; display: block; }
.feature-title { font-size: 17px; font-weight: 600; color: var(--ivory); margin-bottom: 10px; }
.feature-desc { font-size: 14px; color: var(--ivory-muted); line-height: 1.7; }

/* PRICING */
.pricing { background: linear-gradient(180deg, var(--bg), rgba(90,20,32,0.1), var(--bg)); }
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; margin-top: 3rem; }
.pricing-card { background: linear-gradient(135deg, rgba(90,20,32,0.4), rgba(50,10,18,0.6)); border: 1px solid var(--border); border-radius: 24px; padding: 40px 32px; transition: all 0.4s; position: relative; }
.pricing-card.featured { border-color: var(--gold); box-shadow: 0 20px 60px -20px rgba(212,169,97,0.4); transform: scale(1.05); }
.pricing-card:hover { transform: translateY(-8px); border-color: var(--gold); }
.pricing-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, var(--gold), var(--gold-deep)); color: var(--dark-red-deep); padding: 6px 20px; border-radius: 100px; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.pricing-name { font-family: 'Fraunces', serif; font-size: 28px; color: var(--ivory); margin-bottom: 8px; font-weight: 500; }
.pricing-desc { font-size: 13px; color: var(--ivory-muted); margin-bottom: 24px; }
.pricing-price { font-family: 'Fraunces', serif; font-size: 48px; color: var(--gold); font-weight: 500; margin-bottom: 4px; }
.pricing-price span { font-size: 16px; color: var(--ivory-muted); font-family: 'Inter', sans-serif; font-weight: 400; }
.pricing-period { font-size: 13px; color: var(--ivory-muted); margin-bottom: 32px; }
.pricing-features { list-style: none; margin-bottom: 32px; }
.pricing-features li { padding: 10px 0; font-size: 14px; color: var(--ivory); border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; gap: 10px; }
.pricing-features li::before { content: ''; color: var(--gold); font-weight: 700; }
.pricing-btn { display: block; text-align: center; padding: 14px; background: transparent; border: 1px solid var(--gold); color: var(--gold); border-radius: 100px; text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.3s; }
.pricing-btn:hover { background: var(--gold); color: var(--dark-red-deep); }
.pricing-btn-primary { background: linear-gradient(135deg, var(--gold), var(--gold-deep)); color: var(--dark-red-deep); border: none; }
.pricing-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(212,169,97,0.4); }

/* ROADMAP */
.roadmap { background: var(--bg); }
.roadmap-timeline { position: relative; max-width: 900px; margin: 3rem auto 0; padding-left: 40px; }
.roadmap-timeline::before { content: ''; position: absolute; left: 15px; top: 0; bottom: 0; width: 2px; background: linear-gradient(180deg, var(--gold), transparent); }
.roadmap-item { position: relative; padding: 20px 0 40px 30px; }
.roadmap-item::before { content: ''; position: absolute; left: -33px; top: 24px; width: 16px; height: 16px; border-radius: 50%; background: var(--bg); border: 3px solid var(--gold); box-shadow: 0 0 0 4px rgba(212,169,97,0.2); }
.roadmap-item.completed::before { background: var(--gold); }
.roadmap-date { font-size: 12px; color: var(--gold); letter-spacing: 0.15em; text-transform: uppercase; font-weight: 700; margin-bottom: 8px; }
.roadmap-title { font-family: 'Fraunces', serif; font-size: 24px; color: var(--ivory); margin-bottom: 8px; font-weight: 500; }
.roadmap-desc { font-size: 14px; color: var(--ivory-muted); line-height: 1.7; }

/* TESTIMONIALS */
.testimonials { background: linear-gradient(180deg, var(--bg), rgba(90,20,32,0.15), var(--bg)); }
.testimonials-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 24px; margin-top: 3rem; }
.testimonial-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 32px; transition: all 0.3s; }
.testimonial-card:hover { border-color: rgba(212,169,97,0.4); background: rgba(212,169,97,0.04); }
.testimonial-stars { color: var(--gold); font-size: 16px; margin-bottom: 16px; letter-spacing: 2px; }
.testimonial-text { font-size: 15px; color: var(--ivory); line-height: 1.8; margin-bottom: 20px; font-style: italic; }
.testimonial-author { display: flex; align-items: center; gap: 12px; }
.testimonial-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, var(--gold), var(--gold-deep)); display: flex; align-items: center; justify-content: center; font-weight: 700; color: var(--dark-red-deep); font-size: 18px; }
.testimonial-name { font-size: 14px; font-weight: 600; color: var(--ivory); }
.testimonial-role { font-size: 12px; color: var(--ivory-muted); }

/* FAQ */
.faq { background: var(--bg); }
.faq-list { max-width: 800px; margin: 3rem auto 0; }
.faq-item { border-bottom: 1px solid var(--border); padding: 24px 0; }
.faq-question { font-size: 18px; font-weight: 600; color: var(--ivory); cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
.faq-question::after { content: '+'; color: var(--gold); font-size: 24px; font-weight: 300; transition: transform 0.3s; }
.faq-item.open .faq-question::after { transform: rotate(45deg); }
.faq-answer { font-size: 14px; color: var(--ivory-muted); line-height: 1.8; max-height: 0; overflow: hidden; transition: all 0.3s; }
.faq-item.open .faq-answer { max-height: 200px; padding-top: 16px; }

/* CTA SECTION */
.cta-section { padding: 8rem 2rem; text-align: center; background: radial-gradient(ellipse at center, rgba(90,20,32,0.5) 0%, var(--bg) 70%); }
.cta-section h2 { font-family: 'Fraunces', serif; font-size: 56px; margin-bottom: 1.5rem; font-weight: 400; line-height: 1.1; }
.cta-section p { font-size: 19px; color: var(--ivory-muted); max-width: 650px; margin: 0 auto 3rem; font-style: italic; }

/* FOOTER */
footer { padding: 5rem 2rem 2rem; border-top: 1px solid var(--border); background: #060405; }
.footer-inner { max-width: 1400px; margin: 0 auto; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1fr; gap: 3rem; margin-bottom: 4rem; }
.footer-brand { font-family: 'Fraunces', serif; font-size: 28px; color: var(--gold); margin-bottom: 1rem; letter-spacing: 4px; }
.footer-tagline { font-size: 14px; color: var(--ivory-muted); line-height: 1.7; margin-bottom: 1.5rem; }
.footer-social { display: flex; gap: 12px; }
.footer-social a { width: 40px; height: 40px; border-radius: 50%; background: rgba(212,169,97,0.1); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; color: var(--gold); text-decoration: none; transition: all 0.3s; font-size: 16px; }
.footer-social a:hover { background: var(--gold); color: var(--dark-red-deep); transform: translateY(-3px); }
.footer-col-title { font-size: 13px; color: var(--gold); font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 1.5rem; }
.footer-col-links { list-style: none; display: flex; flex-direction: column; gap: 12px; }
.footer-col-links a { font-size: 14px; color: var(--ivory-muted); text-decoration: none; transition: color 0.3s; }
.footer-col-links a:hover { color: var(--gold); }
.footer-bottom { padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.06); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.footer-copy { font-size: 13px; color: #6b6b6b; }
.footer-legal { display: flex; gap: 2rem; }
.footer-legal a { font-size: 13px; color: #6b6b6b; text-decoration: none; transition: color 0.3s; }
.footer-legal a:hover { color: var(--gold); }

/* RESPONSIVE */
@media (max-width: 968px) {
  .navbar-links { display: none; }
  .navbar-links.active { display: flex; flex-direction: column; position: absolute; top: 100%; left: 0; right: 0; background: rgba(10,6,8,0.98); padding: 2rem; border-bottom: 1px solid var(--border); }
  .mobile-menu-btn { display: block; }
  .hero h1 { font-size: 52px; }
  .hero p { font-size: 17px; }
  .section-title { font-size: 36px; }
  .cta-section h2 { font-size: 36px; }
  .stats-bar { gap: 2.5rem; }
  .stat-number { font-size: 38px; }
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .pricing-card.featured { transform: none; }
  .roadmap-timeline { padding-left: 30px; }
}
@media (max-width: 640px) {
  .hero h1 { font-size: 40px; }
  .hero-cta { flex-direction: column; }
  .btn { width: 100%; justify-content: center; }
  .footer-grid { grid-template-columns: 1fr; }
  .navbar { padding: 0.75rem 1rem; }
  .navbar-brand { font-size: 20px; }
  .navbar-btn { padding: 8px 16px; font-size: 12px; }
}
</style>
</head>
<body>

<!-- NAVBAR -->
<nav class="navbar" id="navbar">
  <div class="navbar-inner">
    <a href="/" class="navbar-brand">VASTU <span>ONE</span></a>
    <div class="navbar-links" id="navbarLinks">
      <a href="#modules">Modules</a>
      <a href="#features">Features</a>
      <a href="#pricing">Pricing</a>
      <a href="#roadmap">Roadmap</a>
      <a href="#testimonials">Testimonials</a>
      <a href="#faq">FAQ</a>
    </div>
    <div class="navbar-actions">
      <a href="/login.html" class="navbar-btn navbar-btn-login">Login</a>
      <a href="/signup.html" class="navbar-btn navbar-btn-signup">Get Started </a>
      <button class="mobile-menu-btn" onclick="document.getElementById('navbarLinks').classList.toggle('active')"></button>
    </div>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-content">
    <div class="hero-badge"> Complete Vedic Tech Platform </div>
    <h1>Ancient Wisdom.<br/>Modern Precision.</h1>
    <p>The only platform you'll ever need for Vedic Astrology, Vastu, World Predictions, Numerology, and Spiritual Learning  powered by Swiss Ephemeris and 25+ classical texts.</p>
    <div class="hero-cta">
      <a href="/signup.html" class="btn btn-primary">Start Free Trial </a>
      <a href="#modules" class="btn btn-secondary">Explore Modules</a>
    </div>
    <div class="stats-bar">
      <div class="stat-item"><div class="stat-number">43+</div><div class="stat-label">Engines</div></div>
      <div class="stat-item"><div class="stat-number">25</div><div class="stat-label">Countries</div></div>
      <div class="stat-item"><div class="stat-number">100+</div><div class="stat-label">Yogas</div></div>
      <div class="stat-item"><div class="stat-number">50+</div><div class="stat-label">PDF Reports</div></div>
      <div class="stat-item"><div class="stat-number">8</div><div class="stat-label">Languages</div></div>
    </div>
  </div>
</section>

<!-- MODULES -->
<section class="modules" id="modules">
  <div class="container">
    <div class="section-header">
      <div class="section-eyebrow">Our Modules</div>
      <h2 class="section-title">Everything You Need</h2>
      <p class="section-subtitle">From personal kundli to global predictions  all integrated in one platform</p>
    </div>
    <div class="modules-grid">
      <a href="/kundli-pro.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">Astro Engine</div>
        <div class="module-desc">Complete Vedic astrology  birth chart, planetary positions, dasha, yogas, nakshatras, and varshphal.</div>
        <div class="module-features"><span class="module-feature">Swiss Ephemeris calculations</span><span class="module-feature">5-level Vimshottari Dasha</span><span class="module-feature">100+ Yoga detection</span></div>
        <span class="module-link">Open Kundli Pro </span>
      </a>
      <a href="/world-prediction.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">World Prediction</div>
        <div class="module-desc">Deep research-based country analysis  earthquakes, wars, political changes, natural disasters, and economic forecasts.</div>
        <div class="module-features"><span class="module-feature">25 countries analysis</span><span class="module-feature">Earthquake predictions</span><span class="module-feature">War & political forecasts</span></div>
        <span class="module-link">Explore World </span>
      </a>
      <a href="/full-prediction.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">Master Prediction</div>
        <div class="module-desc">12-layer complete analysis with planetary deep dive, BNN hidden gems, and detailed paragraph explanations.</div>
        <div class="module-features"><span class="module-feature">20+ attributes per planet</span><span class="module-feature">BNN 5-degree rule</span><span class="module-feature">Deep paragraph explanations</span></div>
        <span class="module-link">Open Master </span>
      </a>
      <a href="/real-transit.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">Real Transit</div>
        <div class="module-desc">Real-time planetary positions with Swiss Ephemeris  birth chart vs today's transit analysis.</div>
        <div class="module-features"><span class="module-feature">Live planetary positions</span><span class="module-feature">Birth chart comparison</span><span class="module-feature">Yoga detection</span></div>
        <span class="module-link">View Transit </span>
      </a>
      <a href="/vastu.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">Vastu Engine</div>
        <div class="module-desc">Complete Vastu analysis for homes, offices, and commercial spaces  directional charts, remedies, and room-wise guidance.</div>
        <div class="module-features"><span class="module-feature">Directional analysis</span><span class="module-feature">Room-wise remedies</span><span class="module-feature">Five elements balance</span></div>
        <span class="module-link">Open Vastu </span>
      </a>
      <a href="/numerology.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">Numerology</div>
        <div class="module-desc">Chaldean and Pythagorean numerology  life path, destiny, soul urge, and lucky numbers analysis.</div>
        <div class="module-features"><span class="module-feature">Life path number</span><span class="module-feature">Name numerology</span><span class="module-feature">Lucky numbers</span></div>
        <span class="module-link">Open Numerology </span>
      </a>
      <a href="/lms-dashboard.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">LMS Portal</div>
        <div class="module-desc">Learn astrology, vastu, and numerology with structured courses, quizzes, and certificates.</div>
        <div class="module-features"><span class="module-feature">Structured courses</span><span class="module-feature">Video lessons</span><span class="module-feature">Certificates</span></div>
        <span class="module-link">Start Learning </span>
      </a>
      <a href="/shop.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">Shop</div>
        <div class="module-desc">Authentic astrological products  yantras, gemstones, rudraksha, and puja items with certification.</div>
        <div class="module-features"><span class="module-feature">Certified gemstones</span><span class="module-feature">Energized yantras</span><span class="module-feature">Rudraksha collection</span></div>
        <span class="module-link">Shop Now </span>
      </a>
      <a href="/report.html" class="module-card">
        <div class="module-icon"></div>
        <div class="module-title">PDF Reports</div>
        <div class="module-desc">Research-grade astrological reports with classical references  50+ pages of detailed analysis.</div>
        <div class="module-features"><span class="module-feature">50+ page reports</span><span class="module-feature">Classical references</span><span class="module-feature">Multi-language</span></div>
        <span class="module-link">Download Report </span>
      </a>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section class="features" id="features">
  <div class="container">
    <div class="section-header">
      <div class="section-eyebrow">Why Vastu One</div>
      <h2 class="section-title">Built with Precision</h2>
      <p class="section-subtitle">Every calculation backed by Swiss Ephemeris and 25+ classical texts</p>
    </div>
    <div class="features-grid">
      <div class="feature-card"><div class="feature-icon"></div><div class="feature-title">Swiss Ephemeris</div><div class="feature-desc">Actual planetary calculations  not approximations. Every position is astronomically accurate.</div></div>
      <div class="feature-card"><div class="feature-icon"></div><div class="feature-title">25+ Classical Texts</div><div class="feature-desc">BPHS, Phaladeepika, Bhrigu Samhita, Nadi Astrology, Saravali, Jaimini Sutras, and more.</div></div>
      <div class="feature-card"><div class="feature-icon"></div><div class="feature-title">12-Layer Analysis</div><div class="feature-desc">From planetary deep dive to karmic patterns  every dimension covered.</div></div>
      <div class="feature-card"><div class="feature-icon"></div><div class="feature-title">Multi-Language</div><div class="feature-desc">Reports in English, Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, and Sanskrit.</div></div>
      <div class="feature-card"><div class="feature-icon"></div><div class="feature-title">50+ Page Reports</div><div class="feature-desc">Research-grade PDFs with full explanations, historical evidence, and classical references.</div></div>
      <div class="feature-card"><div class="feature-icon"></div><div class="feature-title">Real-Time Transit</div><div class="feature-desc">Live planetary positions updated with every calculation  always current.</div></div>
    </div>
  </div>
</section>

<!-- PRICING -->
<section class="pricing" id="pricing">
  <div class="container">
    <div class="section-header">
      <div class="section-eyebrow">Pricing</div>
      <h2 class="section-title">Choose Your Plan</h2>
      <p class="section-subtitle">Start free. Upgrade when you need more.</p>
    </div>
    <div class="pricing-grid">
      <div class="pricing-card">
        <div class="pricing-name">Starter</div>
        <div class="pricing-desc">Perfect for beginners</div>
        <div class="pricing-price">Free</div>
        <div class="pricing-period">Forever</div>
        <ul class="pricing-features">
          <li>Basic Kundli</li>
          <li>5 modules access</li>
          <li>1 PDF report/month</li>
          <li>Email support</li>
        </ul>
        <a href="/signup.html" class="pricing-btn">Get Started</a>
      </div>
      <div class="pricing-card featured">
        <div class="pricing-badge">Most Popular</div>
        <div class="pricing-name">Pro</div>
        <div class="pricing-desc">For serious practitioners</div>
        <div class="pricing-price">999<span>/month</span></div>
        <div class="pricing-period">Billed monthly</div>
        <ul class="pricing-features">
          <li>All 9 modules</li>
          <li>Unlimited Kundli</li>
          <li>10 PDF reports/month</li>
          <li>World predictions</li>
          <li>Priority support</li>
          <li>Multi-language reports</li>
        </ul>
        <a href="/signup.html" class="pricing-btn pricing-btn-primary">Start Pro </a>
      </div>
      <div class="pricing-card">
        <div class="pricing-name">Enterprise</div>
        <div class="pricing-desc">For institutions</div>
        <div class="pricing-price">Custom</div>
        <div class="pricing-period">Contact us</div>
        <ul class="pricing-features">
          <li>Everything in Pro</li>
          <li>White-label solution</li>
          <li>API access</li>
          <li>Dedicated support</li>
          <li>Custom integrations</li>
        </ul>
        <a href="/contact.html" class="pricing-btn">Contact Sales</a>
      </div>
    </div>
  </div>
</section>

<!-- ROADMAP -->
<section class="roadmap" id="roadmap">
  <div class="container">
    <div class="section-header">
      <div class="section-eyebrow">Roadmap</div>
      <h2 class="section-title">What's Coming Next</h2>
      <p class="section-subtitle">Our journey of continuous improvement</p>
    </div>
    <div class="roadmap-timeline">
      <div class="roadmap-item completed">
        <div class="roadmap-date">Q4 2025  Completed</div>
        <div class="roadmap-title">Core Engines</div>
        <div class="roadmap-desc">Astro engine, Vastu engine, World prediction, PDF reports, LMS portal, E-commerce, Payment gateway, Email system.</div>
      </div>
      <div class="roadmap-item completed">
        <div class="roadmap-date">Q1 2026  Completed</div>
        <div class="roadmap-title">Swiss Ephemeris Integration</div>
        <div class="roadmap-desc">Actual planetary calculations, 5-level Vimshottari Dasha, 100+ Yoga detection, BNN hidden gems.</div>
      </div>
      <div class="roadmap-item">
        <div class="roadmap-date">Q2 2026  In Progress</div>
        <div class="roadmap-title">Multi-Language Support</div>
        <div class="roadmap-desc">Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, Sanskrit PDF reports with proper font shaping.</div>
      </div>
      <div class="roadmap-item">
        <div class="roadmap-date">Q3 2026  Planned</div>
        <div class="roadmap-title">AI-Powered Predictions</div>
        <div class="roadmap-desc">GPT/LLM integration for natural language predictions, personalized insights, and conversational astrology assistant.</div>
      </div>
      <div class="roadmap-item">
        <div class="roadmap-date">Q4 2026  Planned</div>
        <div class="roadmap-title">Mobile Apps</div>
        <div class="roadmap-desc">Native iOS and Android apps with offline support, push notifications, and real-time alerts.</div>
      </div>
      <div class="roadmap-item">
        <div class="roadmap-date">2027  Vision</div>
        <div class="roadmap-title">Global Expansion</div>
        <div class="roadmap-desc">Expansion to 100+ countries, regional languages, and partnerships with astrological institutions worldwide.</div>
      </div>
    </div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section class="testimonials" id="testimonials">
  <div class="container">
    <div class="section-header">
      <div class="section-eyebrow">Testimonials</div>
      <h2 class="section-title">What Our Users Say</h2>
      <p class="section-subtitle">Trusted by thousands of practitioners</p>
    </div>
    <div class="testimonials-grid">
      <div class="testimonial-card">
        <div class="testimonial-stars"></div>
        <div class="testimonial-text">"The most accurate astrology platform I've ever used. The Swiss Ephemeris calculations are spot-on, and the 50+ page PDF reports are incredibly detailed."</div>
        <div class="testimonial-author">
          <div class="testimonial-avatar">R</div>
          <div><div class="testimonial-name">Rajesh Sharma</div><div class="testimonial-role">Astrologer, Delhi</div></div>
        </div>
      </div>
      <div class="testimonial-card">
        <div class="testimonial-stars"></div>
        <div class="testimonial-text">"The World Prediction module is a game-changer. I use it for my research on geopolitical trends. The classical references give it credibility."</div>
        <div class="testimonial-author">
          <div class="testimonial-avatar">P</div>
          <div><div class="testimonial-name">Dr. Priya Patel</div><div class="testimonial-role">Researcher, Mumbai</div></div>
        </div>
      </div>
      <div class="testimonial-card">
        <div class="testimonial-stars"></div>
        <div class="testimonial-text">"The LMS portal helped me learn Vastu from scratch. The structured courses and certificates are perfect for beginners and professionals alike."</div>
        <div class="testimonial-author">
          <div class="testimonial-avatar">A</div>
          <div><div class="testimonial-name">Amit Kumar</div><div class="testimonial-role">Vastu Consultant, Bangalore</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="faq" id="faq">
  <div class="container">
    <div class="section-header">
      <div class="section-eyebrow">FAQ</div>
      <h2 class="section-title">Frequently Asked Questions</h2>
      <p class="section-subtitle">Everything you need to know</p>
    </div>
    <div class="faq-list">
      <div class="faq-item">
        <div class="faq-question" onclick="this.parentElement.classList.toggle('open')">What makes Vastu One different from other astrology platforms?</div>
        <div class="faq-answer">Vastu One uses Swiss Ephemeris for actual planetary calculations  not approximations. Every prediction is backed by 25+ classical texts including BPHS, Phaladeepika, Bhrigu Samhita, Nadi Astrology, and BNN techniques. We provide 12-layer analysis with 20+ attributes per planet.</div>
      </div>
      <div class="faq-item">
        <div class="faq-question" onclick="this.parentElement.classList.toggle('open')">Can I get reports in my regional language?</div>
        <div class="faq-answer">Yes! We support 8 languages: English, Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, and Sanskrit. Every report is generated with proper font shaping for accurate rendering.</div>
      </div>
      <div class="faq-item">
        <div class="faq-question" onclick="this.parentElement.classList.toggle('open')">How accurate are the predictions?</div>
        <div class="faq-answer">Our predictions are based on precise Swiss Ephemeris calculations and classical Vedic principles. While astrology indicates tendencies rather than fixed outcomes, our 12-layer analysis provides the most comprehensive view possible.</div>
      </div>
      <div class="faq-item">
        <div class="faq-question" onclick="this.parentElement.classList.toggle('open')">Can I download the PDF reports?</div>
        <div class="faq-answer">Yes! Pro members can download 10 PDF reports per month (50+ pages each). Enterprise members get unlimited downloads with white-label options.</div>
      </div>
      <div class="faq-item">
        <div class="faq-question" onclick="this.parentElement.classList.toggle('open')">Do you offer API access?</div>
        <div class="faq-answer">Yes! Enterprise plans include full API access for integrating our astrology engines into your own applications. Contact our sales team for details.</div>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-section">
  <div class="container">
    <h2>Begin Your Journey</h2>
    <p>Discover what the stars have written for you  with the precision of Swiss Ephemeris and the wisdom of ancient sages.</p>
    <div class="hero-cta">
      <a href="/signup.html" class="btn btn-primary">Start Free Trial </a>
      <a href="/contact.html" class="btn btn-secondary">Contact Sales</a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">VASTU ONE</div>
        <div class="footer-tagline">Ancient Wisdom. Modern Precision. The complete Vedic tech platform for astrology, vastu, and spiritual learning.</div>
        <div class="footer-social">
          <a href="#"></a><a href="#"></a><a href="#"></a><a href="#"></a><a href="#"></a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Platform</div>
        <ul class="footer-col-links">
          <li><a href="/kundli-pro.html">Kundli Pro</a></li>
          <li><a href="/world-prediction.html">World Prediction</a></li>
          <li><a href="/full-prediction.html">Master Prediction</a></li>
          <li><a href="/real-transit.html">Real Transit</a></li>
          <li><a href="/vastu.html">Vastu Engine</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Resources</div>
        <ul class="footer-col-links">
          <li><a href="/lms-dashboard.html">LMS Portal</a></li>
          <li><a href="/shop.html">Shop</a></li>
          <li><a href="/report.html">PDF Reports</a></li>
          <li><a href="#roadmap">Roadmap</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Company</div>
        <ul class="footer-col-links">
          <li><a href="/about.html">About Us</a></li>
          <li><a href="/contact.html">Contact</a></li>
          <li><a href="/careers.html">Careers</a></li>
          <li><a href="/press.html">Press</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Legal</div>
        <ul class="footer-col-links">
          <li><a href="/legal/privacy.html">Privacy</a></li>
          <li><a href="/legal/terms.html">Terms</a></li>
          <li><a href="/legal/disclaimer.html">Disclaimer</a></li>
          <li><a href="/legal/refund.html">Refund</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy"> 2026 Vastu One  India  All Rights Reserved</div>
      <div class="footer-legal">
        <a href="/legal/privacy.html">Privacy</a>
        <a href="/legal/terms.html">Terms</a>
        <a href="/legal/disclaimer.html">Disclaimer</a>
      </div>
    </div>
  </div>
</footer>

<script>
// Navbar scroll effect
window.addEventListener('scroll', function() {
  var navbar = document.getElementById('navbar');
  if (window.scrollY > 50) {
    navbar.style.background = 'rgba(10,6,8,0.95)';
    navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
  } else {
    navbar.style.background = 'rgba(10,6,8,0.85)';
    navbar.style.boxShadow = 'none';
  }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      document.getElementById('navbarLinks').classList.remove('active');
    }
  });
});
</script>

</body>
</html>
"""

Path("frontend/index.html").write_text(html, encoding="utf-8")
print("File written:", Path("frontend/index.html").stat().st_size, "bytes")