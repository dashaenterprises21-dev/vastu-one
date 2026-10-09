from pathlib import Path

# 1) Update astro_engine_v3_complete.py
p = Path("engine/astro/astro_engine_v3_complete.py")
c = p.read_text(encoding="utf-8")

# Add import
if "LifePredictionEngine" not in c:
    c = c.replace(
        "    from engine.astro.classical_granthas import ClassicalGranthasEngine\n    CLASSICAL_AVAILABLE = True",
        "    from engine.astro.classical_granthas import ClassicalGranthasEngine\n    from engine.astro.life_prediction import LifePredictionEngine\n    CLASSICAL_AVAILABLE = True",
        1
    )

# Add life predictions in full_report
if "life_predictions" not in c:
    c = c.replace(
        '''        classical = {"yogas": [], "doshas": [], "predictions": [], "total_yogas": 0, "total_doshas": 0}
        if CLASSICAL_AVAILABLE:
            try:
                classical_engine = ClassicalGranthasEngine(positions, lagna, positions, dasha)
                classical = classical_engine.analyze_all()
            except Exception as e:
                print(f"Classical analysis error: {e}")''',
        '''        classical = {"yogas": [], "doshas": [], "predictions": [], "total_yogas": 0, "total_doshas": 0}
        if CLASSICAL_AVAILABLE:
            try:
                classical_engine = ClassicalGranthasEngine(positions, lagna, positions, dasha)
                classical = classical_engine.analyze_all()
            except Exception as e:
                print(f"Classical analysis error: {e}")

        # Life Predictions (deep personal analysis)
        life_predictions = {}
        try:
            life_engine = LifePredictionEngine(positions, lagna, bhava_chalit, dasha)
            life_predictions = life_engine.analyze_all()
        except Exception as e:
            print(f"Life prediction error: {e}")''',
        1
    )

    # Add to return dict
    c = c.replace(
        '''            "classical": classical,
        }''',
        '''            "classical": classical,
            "life_predictions": life_predictions,
        }''',
        1
    )

p.write_text(c, encoding="utf-8")
print("Engine updated!")

# 2) Add frontend sections
p2 = Path("frontend/kundli-pro.html")
c2 = p2.read_text(encoding="utf-8")

# Add 8 new sections before footer
NEW_SECTIONS = '''    <!-- 14. EDUCATION -->
    <div class="section"><div class="section-header"><div class="section-icon">📚</div><div><div class="section-title">Education</div><div class="section-sub">Field • Higher studies • Obstacles</div></div></div><div id="education-grid"></div></div>
    <!-- 15. CAREER -->
    <div class="section"><div class="section-header"><div class="section-icon">💼</div><div><div class="section-title">Career Analysis</div><div class="section-sub">Field • Job vs Business • Timing</div></div></div><div id="career-grid"></div></div>
    <!-- 16. BUSINESS -->
    <div class="section"><div class="section-header"><div class="section-icon">📈</div><div><div class="section-title">Business Guidance</div><div class="section-sub">Type • Partner • Alone vs Together</div></div></div><div id="business-grid"></div></div>
    <!-- 17. PERSONAL LIFE -->
    <div class="section"><div class="section-header"><div class="section-icon">👤</div><div><div class="section-title">Personal Life</div><div class="section-sub">Personality • Strengths • Weaknesses</div></div></div><div id="personal-grid"></div></div>
    <!-- 18. MARRIAGE -->
    <div class="section"><div class="section-header"><div class="section-icon">💑</div><div><div class="section-title">Marriage</div><div class="section-sub">Timing • Partner • Happiness</div></div></div><div id="marriage-grid"></div></div>
    <!-- 19. CHILDREN -->
    <div class="section"><div class="section-header"><div class="section-icon">👶</div><div><div class="section-title">Children</div><div class="section-sub">Count • Timing • Nature</div></div></div><div id="children-grid"></div></div>
    <!-- 20. LOCATION -->
    <div class="section"><div class="section-header"><div class="section-icon">🌍</div><div><div class="section-title">Location</div><div class="section-sub">City • Country • Direction</div></div></div><div id="location-grid"></div></div>
    <!-- 21. WEALTH -->
    <div class="section"><div class="section-header"><div class="section-icon">💰</div><div><div class="section-title">Wealth Analysis</div><div class="section-sub">Level • Source • Timing</div></div></div><div id="wealth-grid"></div></div>
    <!-- 22. HEALTH -->
    <div class="section"><div class="section-header"><div class="section-icon">🏥</div><div><div class="section-title">Health</div><div class="section-sub">Weak organs • Prevention</div></div></div><div id="health-grid"></div></div>
    <!-- 23. SPIRITUAL -->
    <div class="section"><div class="section-header"><div class="section-icon">🕉️</div><div><div class="section-title">Spiritual Path</div><div class="section-sub">Bhakti • Gyan • Dhyan</div></div></div><div id="spiritual-grid"></div></div>
    <!-- 24. DREAMS -->
    <div class="section"><div class="section-header"><div class="section-icon">🌟</div><div><div class="section-title">Dreams Fulfillment</div><div class="section-sub">Timing • Best period</div></div></div><div id="dreams-grid"></div></div>

</main>'''

if "id=\"education-grid\"" not in c2:
    c2 = c2.replace("</main>", NEW_SECTIONS, 1)

# Add render functions
NEW_RENDER = '''function renderLifePredictions(life) {
  if (!life) return;

  function card2(label, value, sub) {
    return '<div class="card"><div class="card-label">' + label + '</div><div class="card-value hindi" style="font-size:18px;">' + value + '</div><div class="card-sub">' + (sub || '') + '</div></div>';
  }

  // Education
  if (life.education) {
    var e = life.education;
    document.getElementById('education-grid').innerHTML = '<div class="grid-4">' +
      card2('Best Field', e.best_field, e.higher_education) +
      card2('Subjects', (e.subjects || []).slice(0,3).join(', '), 'Recommended') +
      card2('Obstacles', (e.obstacles || []).join(', '), '') +
      card2('Source', e.source, '') +
      '</div>';
  }

  // Career
  if (life.career) {
    var e = life.career;
    document.getElementById('career-grid').innerHTML = '<div class="grid-4">' +
      card2('Best Field', e.best_field, '') +
      card2('Job vs Business', e.job_vs_business, '') +
      card2('Timing', e.timing, '') +
      card2('Source', e.source, '') +
      '</div>';
  }

  // Business
  if (life.business) {
    var e = life.business;
    document.getElementById('business-grid').innerHTML = '<div class="grid-4">' +
      card2('Business Type', e.best_business_type, '') +
      card2('Alone or Partner', e.partner_or_alone, '') +
      card2('Partner Nature', e.partner_nature, '') +
      card2('Expansion', e.expansion_timing, '') +
      '</div>';
  }

  // Personal
  if (life.personal_life) {
    var e = life.personal_life;
    document.getElementById('personal-grid').innerHTML = '<div class="grid-4">' +
      card2('Personality', e.personality, '') +
      card2('Strengths', (e.strengths || []).join(', '), '') +
      card2('Weaknesses', (e.weaknesses || []).join(', '), '') +
      card2('Source', e.source, '') +
      '</div>';
  }

  // Marriage
  if (life.marriage) {
    var e = life.marriage;
    document.getElementById('marriage-grid').innerHTML = '<div class="grid-4">' +
      card2('Timing', e.timing, '') +
      card2('Type', e.marriage_type, '') +
      card2('Partner Nature', e.partner_nature, '') +
      card2('Happiness', e.happiness, (e.warnings || []).join(' • ')) +
      '</div>';
  }

  // Children
  if (life.children) {
    var e = life.children;
    document.getElementById('children-grid').innerHTML = '<div class="grid-4">' +
      card2('Count', e.count, '') +
      card2('Timing', e.timing, '') +
      card2('Nature', e.nature, '') +
      card2('Warnings', (e.warnings || []).join(', '), '') +
      '</div>';
  }

  // Location
  if (life.location) {
    var e = life.location;
    document.getElementById('location-grid').innerHTML = '<div class="grid-4">' +
      card2('Best Direction', e.best_direction, '') +
      card2('Best Country', e.best_country, '') +
      card2('City Type', e.best_city_type, '') +
      card2('Source', e.source, '') +
      '</div>';
  }

  // Wealth
  if (life.wealth) {
    var e = life.wealth;
    document.getElementById('wealth-grid').innerHTML = '<div class="grid-4">' +
      card2('Wealth Level', e.wealth_level, '') +
      card2('Source', e.source, '') +
      card2('Timing', e.timing, '') +
      card2('Source Text', e.source_text, '') +
      '</div>';
  }

  // Health
  if (life.health) {
    var e = life.health;
    document.getElementById('health-grid').innerHTML = '<div class="grid-4">' +
      card2('Weak Organs', (e.weak_organs || []).join(', '), '') +
      card2('Preventions', (e.preventions || []).join(', '), '') +
      card2('Recommendation', e.recommendation, '') +
      card2('Source', e.source, '') +
      '</div>';
  }

  // Spiritual
  if (life.spiritual) {
    var e = life.spiritual;
    document.getElementById('spiritual-grid').innerHTML = '<div class="grid-4">' +
      card2('Path', e.path, '') +
      card2('Guru', e.guru, '') +
      card2('Practice', e.practice, '') +
      card2('Source', e.source, '') +
      '</div>';
  }

  // Dreams
  if (life.dreams) {
    var e = life.dreams;
    document.getElementById('dreams-grid').innerHTML = '<div class="grid-4">' +
      card2('Best Period', e.best_period, '') +
      card2('Current Dasha', e.current_dasha, '') +
      card2('Recommendation', e.recommendation, '') +
      card2('Source', e.source, '') +
      '</div>';
  }
}

// Init i18n'''

if "function renderLifePredictions" not in c2:
    c2 = c2.replace("// Init i18n", NEW_RENDER, 1)

# Add call in analyzeKundli
if "renderLifePredictions(data.life_predictions)" not in c2:
    c2 = c2.replace(
        "renderPredictions(data.classical ? data.classical.predictions : []);",
        "renderPredictions(data.classical ? data.classical.predictions : []);\n    renderLifePredictions(data.life_predictions || {});",
        1
    )

p2.write_text(c2, encoding="utf-8")
print("Frontend updated!")
print("DONE!")