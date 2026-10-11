/**
 * Vastu One — Phase 6 Renderer
 * 6 Final Engines: Nakshatra Nadi, Jaimini, KP+, Varshphal+, Transit+, LK+
 */

function renderPhase6Sections(data) {
  if (!data) return;
  renderNakshatraNadi(data.nakshatra_nadi || {});
  renderJaimini(data.jaimini || {});
  renderKPEnhanced(data.kp_enhanced || {});
  renderVarshphalEnhanced(data.varshphal_enhanced || {});
  renderTransitEnhanced(data.transit_enhanced || {});
  renderLalKitabEnhanced(data.lalkitab_enhanced || {});
}

// ═══ 1. NAKSHATRA NADI ═══
function renderNakshatraNadi(n) {
  var t = document.getElementById('nakshatra-nadi-container');
  if (!t || !n.planets) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Planetary Nakshatra Details</h4>';
  Object.entries(n.planets).forEach(function(e) {
    var p = e[1];
    html += '<div style="margin-bottom:12px;padding:14px;background:rgba(90,20,32,0.4);border-left:3px solid var(--gold);border-radius:8px;">';
    html += '<div style="font-size:13px;color:var(--gold);font-weight:600;margin-bottom:6px;">' + p.hindi + ' — ' + p.nakshatra + ' (Pada ' + p.pada + ')</div>';
    html += '<div style="font-size:11.5px;color:var(--ivory-muted);line-height:1.7;">';
    html += '<span style="margin-right:12px;"><strong style="color:var(--gold);">Lord:</strong> ' + p.lord + '</span>';
    html += '<span style="margin-right:12px;"><strong style="color:var(--gold);">Devta:</strong> ' + p.devta + '</span>';
    html += '<span style="margin-right:12px;"><strong style="color:var(--gold);">Gana:</strong> ' + p.gana + '</span>';
    html += '<span style="margin-right:12px;"><strong style="color:var(--gold);">Nadi:</strong> ' + p.nadi + '</span>';
    html += '<span><strong style="color:var(--gold);">Yoni:</strong> ' + p.yoni + '</span>';
    html += '</div></div>';
  });
  t.innerHTML = html;
}

// ═══ 2. JAIMINI ═══
function renderJaimini(j) {
  var t = document.getElementById('jaimini-container');
  if (!t || !j.chara_karakas) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Chara Karakas</h4>';
  var rows = j.chara_karakas.map(function(k) {
    return [k.num + '. ' + k.hindi, k.planet_hindi, k.degree + '°'];
  });
  html += tableHTML(['Karaka', 'Planet', 'Degree'], rows);

  if (j.karakamsha) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:20px 0 12px;">Karakamsha</h4>';
    html += '<div style="padding:14px;background:rgba(212,169,97,0.1);border-radius:8px;">';
    html += '<div style="font-size:14px;color:var(--gold);">' + j.karakamsha.atra_hindi + '</div>';
    html += '<div style="font-size:13px;color:var(--ivory);margin-top:6px;">' + j.karakamsha.atra_planet + ' → ' + j.karakamsha.atra_rashi + '</div>';
    html += '</div>';
  }
  t.innerHTML = html;
}

// ═══ 3. KP ENHANCED ═══
function renderKPEnhanced(k) {
  var t = document.getElementById('kp-enhanced-container');
  if (!t || !k.sub_sub_analysis) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Sub-Sub Lord Analysis</h4>';
  var rows = k.sub_sub_analysis.map(function(p) {
    return [p.hindi, p.nakshatra, p.nakshatra_lord, p.sub_lord, p.sub_sub_lord];
  });
  html += tableHTML(['Planet', 'Nakshatra', 'Star Lord', 'Sub Lord', 'Sub-Sub Lord'], rows);

  if (k.ruling_planets) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:20px 0 12px;">Ruling Planets</h4>';
    var rp = k.ruling_planets;
    html += cardHTML('Day Lord', rp.day_lord || '—');
    html += cardHTML('Moon Star Lord', rp.moon_star_lord || '—');
    html += cardHTML('Lagna Sign Lord', rp.lagna_sign_lord || '—');
    html += cardHTML('Lagna Star Lord', rp.lagna_star_lord || '—');
  }
  t.innerHTML = html;
}

// ═══ 4. VARSHPHAL ENHANCED ═══
function renderVarshphalEnhanced(v) {
  var t = document.getElementById('varshphal-enhanced-container');
  if (!t || !v.next_5_years) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">5-Year Annual Forecast</h4>';
  v.next_5_years.forEach(function(y) {
    html += '<div style="margin-bottom:14px;padding:16px;background:rgba(90,20,32,0.4);border-left:3px solid var(--gold);border-radius:8px;">';
    html += '<div style="font-size:14px;color:var(--gold);font-weight:600;margin-bottom:8px;">' + y.year + ' (Age ' + y.age + ')</div>';
    html += '<div style="font-size:12px;color:var(--ivory-muted);margin-bottom:6px;"><strong style="color:var(--gold);">Muntha:</strong> ' + y.muntha_rashi_hindi + '</div>';
    html += '<div style="font-size:12px;color:var(--ivory-muted);margin-bottom:8px;"><strong style="color:var(--gold);">Year Lord:</strong> ' + y.year_lord_hindi + ' — ' + y.year_lord_effects + '</div>';
    html += '</div>';
  });
  t.innerHTML = html;
}

// ═══ 5. TRANSIT ENHANCED ═══
function renderTransitEnhanced(tr) {
  var t = document.getElementById('transit-enhanced-container');
  if (!t || !tr.current_transits) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Current Transits</h4>';
  var rows = tr.current_transits.map(function(x) {
    return [x.planet_hindi, x.rashi_hindi, 'L: ' + x.from_lagna, 'M: ' + x.from_chandra, x.effect_from_moon];
  });
  html += tableHTML(['Planet', 'Rashi', 'From Lagna', 'From Moon', 'Effect'], rows);

  if (tr.monthly_predictions) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:20px 0 12px;">12-Month Forecast</h4>';
    tr.monthly_predictions.forEach(function(m) {
      html += cardHTML(m.month, (m.highlights || []).join('<br>'));
    });
  }
  t.innerHTML = html;
}

// ═══ 6. LAL KITAB ENHANCED ═══
function renderLalKitabEnhanced(lk) {
  var t = document.getElementById('lalkitab-enhanced-container');
  if (!t) return;
  var html = '';

  if (lk.teva_analysis) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">3 Teva Analysis</h4>';
    lk.teva_analysis.forEach(function(tv) {
      html += cardHTML(tv.teva_hindi, '<strong style="color:var(--gold);">' + tv.rashi_hindi + '</strong> — ' + tv.meaning);
    });
  }

  if (lk.house_wise_remedies) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:20px 0 12px;">House-wise Remedies</h4>';
    lk.house_wise_remedies.forEach(function(h) {
      var remedies = h.remedies.map(function(r) { return '<strong style="color:var(--gold);">' + r.planet_hindi + ':</strong> ' + r.remedy; }).join('<br>');
      html += cardHTML('Bhava ' + h.house + ' (' + h.planets.join(', ') + ')', remedies);
    });
  }

  if (lk.kudrati_upay) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:20px 0 12px;">Natural Remedies</h4>';
    html += '<ul style="padding-left:20px;color:var(--ivory-muted);font-size:13px;line-height:1.8;">';
    lk.kudrati_upay.forEach(function(u) { html += '<li>' + u + '</li>'; });
    html += '</ul>';
  }
  t.innerHTML = html;
}

// Hook into renderExtendedSections
var origExtended6 = window.renderExtendedSections;
window.renderExtendedSections = function(data) {
  if (origExtended6) origExtended6(data);
  renderPhase6Sections(data);
};

window.renderPhase6Sections = renderPhase6Sections;
console.log('✅ Phase 6 renderer loaded');
