from pathlib import Path

p = Path("frontend/kundli-pro.html")
c = p.read_text(encoding="utf-8")

# ============================================
# 1) Add 3 functions before renderPooja
# ============================================
NEW_FUNCTIONS = '''function renderClassicalYogas(yogas) {
  if (!yogas || !yogas.length) {
    document.getElementById('classical-yogas-grid').innerHTML = '<div class="card">Koi classical yoga detect nahi hua.</div>';
    return;
  }
  var html = '';
  for (var i = 0; i < yogas.length; i++) {
    var y = yogas[i];
    html += '<div class="card" style="margin-bottom:16px;">' +
      '<div style="display:flex;justify-content:space-between;align-items:start;gap:12px;flex-wrap:wrap;">' +
      '<div><div class="card-value hindi">' + y.hindi + '</div>' +
      '<div style="font-size:12px;color:var(--muted);">' + y.name + '</div></div>' +
      '<div style="text-align:right;">' +
      '<span style="background:rgba(212,175,55,0.15);color:var(--gold);font-size:10px;padding:4px 10px;border-radius:6px;font-weight:700;">' + y.type + '</span>' +
      '<div style="font-size:10px;color:var(--muted);margin-top:4px;">' + (y.source || '') + '</div>' +
      '</div></div>' +
      '<div style="margin-top:12px;font-size:13px;color:var(--muted);">' + y.description + '</div>' +
      '<div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;">' +
      (y.effects || []).map(function (e) { return '<span style="font-size:10px;padding:3px 8px;background:rgba(74,222,128,0.1);color:var(--success);border-radius:6px;">' + e + '</span>'; }).join('') +
      '</div></div>';
  }
  document.getElementById('classical-yogas-grid').innerHTML = html;
}

function renderClassicalDoshas(doshas) {
  if (!doshas || !doshas.length) {
    document.getElementById('classical-doshas-grid').innerHTML = '<div class="card">Koi classical dosha detect nahi hua!</div>';
    return;
  }
  var html = '';
  for (var i = 0; i < doshas.length; i++) {
    var d = doshas[i];
    var sevColor = d.severity === 'High' ? 'var(--danger)' : d.severity === 'Medium' ? 'var(--warning)' : 'var(--success)';
    html += '<div class="card" style="margin-bottom:20px;border-color:' + sevColor + '40;">' +
      '<div style="display:flex;justify-content:space-between;align-items:start;gap:12px;flex-wrap:wrap;">' +
      '<div><div class="card-value hindi">' + d.hindi + '</div>' +
      '<div style="font-size:12px;color:var(--muted);">' + d.name + '</div>' +
      '<div style="font-size:10px;color:var(--gold);margin-top:4px;">Source: ' + (d.source || '-') + '</div></div>' +
      '<span style="background:' + sevColor + '20;color:' + sevColor + ';font-size:10px;padding:4px 10px;border-radius:6px;font-weight:700;">' + d.severity + '</span>' +
      '</div>' +
      '<div style="margin-top:12px;font-size:13px;color:var(--muted);">' + d.description + '</div>';
    if (d.remedies && d.remedies.length) {
      html += '<div style="margin-top:16px;padding:16px;background:rgba(212,175,55,0.05);border-radius:10px;">' +
        '<div style="font-size:11px;color:var(--gold);font-weight:700;margin-bottom:12px;">REMEDIES (' + d.remedies.length + ')</div>';
      for (var j = 0; j < d.remedies.length; j++) {
        var r = d.remedies[j];
        html += '<div style="padding:8px 0;border-bottom:1px solid rgba(212,175,55,0.1);">' +
          '<span style="font-size:10px;color:var(--gold);text-transform:uppercase;font-weight:700;">' + r.type + '</span>' +
          '<div style="font-size:13px;margin-top:4px;">' + r.text + '</div>' +
          (r.count ? '<div style="font-size:11px;color:var(--muted);">' + r.count + '</div>' : '') +
          '</div>';
      }
      html += '</div>';
    }
    html += '</div>';
  }
  document.getElementById('classical-doshas-grid').innerHTML = html;
}

function renderPredictions(predictions) {
  if (!predictions || !predictions.length) {
    document.getElementById('predictions-grid').innerHTML = '<div class="card">Koi prediction nahi.</div>';
    return;
  }
  var html = '<div class="grid-2">';
  for (var i = 0; i < predictions.length; i++) {
    var p = predictions[i];
    html += '<div class="card"><div class="card-label">' + p.area + '</div>' +
      '<div style="font-size:14px;margin-top:8px;">' + p.prediction + '</div>' +
      (p.source ? '<div style="font-size:11px;color:var(--gold);margin-top:8px;">Source: ' + p.source + '</div>' : '') +
      '</div>';
  }
  html += '</div>';
  document.getElementById('predictions-grid').innerHTML = html;
}

'''

# Insert before "function renderPooja"
if "function renderClassicalYogas" not in c:
    c = c.replace("function renderPooja(doshas) {", NEW_FUNCTIONS + "function renderPooja(doshas) {", 1)

# ============================================
# 2) Add 3 HTML sections before REMEDIES
# ============================================
NEW_SECTIONS = '''    <!-- 11. CLASSICAL YOGAS -->
    <div class="section" id="sec-classical-yogas">
      <div class="section-header">
        <div class="section-icon">📜</div>
        <div>
          <div class="section-title">Classical Yogas (Granthas)</div>
          <div class="section-sub">BPHS • Saravali • Phaladeepika • Jaimini Sutras</div>
        </div>
      </div>
      <div id="classical-yogas-grid"></div>
    </div>

    <!-- 12. CLASSICAL DOSHAS -->
    <div class="section" id="sec-classical-doshas">
      <div class="section-header">
        <div class="section-icon">🔍</div>
        <div>
          <div class="section-title">Classical Doshas (Deep Analysis)</div>
          <div class="section-sub">Pitru • Kaal Sarpa • Grahan • Angarak • Shrapit</div>
        </div>
      </div>
      <div id="classical-doshas-grid"></div>
    </div>

    <!-- 13. PREDICTIONS -->
    <div class="section" id="sec-predictions">
      <div class="section-header">
        <div class="section-icon">🔮</div>
        <div>
          <div class="section-title">Predictions (Life Path)</div>
          <div class="section-sub">Marriage • Career • Health • Wealth</div>
        </div>
      </div>
      <div id="predictions-grid"></div>
    </div>

    <!-- 11. REMEDIES -->'''

if "sec-classical-yogas" not in c:
    c = c.replace("    <!-- 11. REMEDIES -->", NEW_SECTIONS, 1)

# ============================================
# 3) Save
# ============================================
p.write_text(c, encoding="utf-8")
print("DONE - File updated successfully!")
print(f"File size: {len(c)} chars")