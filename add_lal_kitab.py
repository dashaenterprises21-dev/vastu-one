from pathlib import Path

# 1) Update astro_engine_v3_complete.py
p = Path("engine/astro/astro_engine_v3_complete.py")
c = p.read_text(encoding="utf-8")

# Add import
if "LalKitabEngine" not in c:
    c = c.replace(
        "    from engine.astro.life_prediction import LifePredictionEngine\n    CLASSICAL_AVAILABLE = True",
        "    from engine.astro.life_prediction import LifePredictionEngine\n    from engine.astro.lal_kitab_engine import LalKitabEngine\n    CLASSICAL_AVAILABLE = True",
        1
    )

# Add lal_kitab in full_report
if "lal_kitab" not in c:
    c = c.replace(
        '''        # Life Predictions (deep personal analysis)
        life_predictions = {}
        try:
            life_engine = LifePredictionEngine(positions, lagna, bhava_chalit, dasha)
            life_predictions = life_engine.analyze_all()
        except Exception as e:
            print(f"Life prediction error: {e}")''',
        '''        # Life Predictions (deep personal analysis)
        life_predictions = {}
        try:
            life_engine = LifePredictionEngine(positions, lagna, bhava_chalit, dasha)
            life_predictions = life_engine.analyze_all()
        except Exception as e:
            print(f"Life prediction error: {e}")

        # Lal Kitab Analysis
        lal_kitab = {"findings": [], "remedies": [], "total_findings": 0, "total_remedies": 0}
        try:
            lk_engine = LalKitabEngine(positions, lagna)
            lal_kitab = lk_engine.analyze_all()
        except Exception as e:
            print(f"Lal Kitab error: {e}")''',
        1
    )

    c = c.replace(
        '''            "life_predictions": life_predictions,
        }''',
        '''            "life_predictions": life_predictions,
            "lal_kitab": lal_kitab,
        }''',
        1
    )

p.write_text(c, encoding="utf-8")
print("Engine updated!")

# 2) Update frontend
p2 = Path("frontend/kundli-pro.html")
c2 = p2.read_text(encoding="utf-8")

# Add Lal Kitab section
NEW_SECTION = '''    <!-- 25. LAL KITAB -->
    <div class="section"><div class="section-header"><div class="section-icon">📕</div><div><div class="section-title">Lal Kitab Analysis</div><div class="section-sub">Unique Totke • Low-Cost Remedies</div></div></div><div id="lal-kitab-grid"></div></div>

</main>'''

if "id=\"lal-kitab-grid\"" not in c2:
    c2 = c2.replace("</main>", NEW_SECTION, 1)

# Add render function
NEW_RENDER = '''function renderLalKitab(lk) {
  if (!lk || !lk.findings || !lk.findings.length) {
    document.getElementById('lal-kitab-grid').innerHTML = '<div class="card">Koi Lal Kitab finding nahi.</div>';
    return;
  }
  var html = '';
  for (var i = 0; i < lk.findings.length; i++) {
    var f = lk.findings[i];
    html += '<div class="card" style="margin-bottom:20px;">' +
      '<div style="display:flex;justify-content:space-between;align-items:start;gap:12px;flex-wrap:wrap;">' +
      '<div><div class="card-value hindi">' + f.title + '</div>' +
      '<div style="font-size:11px;color:var(--gold);margin-top:4px;">Lal Kitab 1952</div></div>' +
      '<span style="background:rgba(212,175,55,0.15);color:var(--gold);font-size:10px;padding:4px 10px;border-radius:6px;font-weight:700;">BHAV ' + f.bhav + '</span>' +
      '</div>' +
      '<div style="margin-top:14px;font-size:14px;color:var(--muted);line-height:1.7;">' + f.detail + '</div>' +
      '<div style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap;">' +
      (f.effects || []).map(function (e) { return '<span style="font-size:10px;padding:3px 8px;background:rgba(248,113,113,0.1);color:var(--danger);border-radius:6px;">' + e + '</span>'; }).join('') +
      '</div>';

    if (f.remedies && f.remedies.length) {
      html += '<div style="margin-top:16px;padding:16px;background:rgba(212,175,55,0.05);border-radius:10px;">' +
        '<div style="font-size:11px;color:var(--gold);font-weight:700;margin-bottom:12px;">LAL KITAB TOTKE (' + f.remedies.length + ')</div>';
      for (var j = 0; j < f.remedies.length; j++) {
        var r = f.remedies[j];
        html += '<div style="padding:10px 0;border-bottom:1px solid rgba(212,175,55,0.1);">' +
          '<span style="font-size:10px;color:var(--gold);text-transform:uppercase;font-weight:700;">' + r.type + '</span>' +
          '<div style="font-size:14px;margin-top:4px;color:var(--starlight);">' + r.text + '</div>' +
          (r.detail ? '<div style="font-size:11px;color:var(--muted);margin-top:4px;">' + r.detail + '</div>' : '') +
          '</div>';
      }
      html += '</div>';
    }
    html += '</div>';
  }
  document.getElementById('lal-kitab-grid').innerHTML = html;
}

// Init i18n'''

if "function renderLalKitab" not in c2:
    c2 = c2.replace("// Init i18n", NEW_RENDER, 1)

# Add call
if "renderLalKitab(data.lal_kitab)" not in c2:
    c2 = c2.replace(
        "renderLifePredictions(data.life_predictions || {});",
        "renderLifePredictions(data.life_predictions || {});\n    renderLalKitab(data.lal_kitab || {});",
        1
    )

p2.write_text(c2, encoding="utf-8")
print("Frontend updated!")
print("DONE!")