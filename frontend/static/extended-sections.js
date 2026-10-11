/**
 * Vastu One — Extended Sections Renderer
 * 16 new sections: Panchang, KP, Medical, etc.
 */

function scrollToPanel(id) {
  showPanel(id);
  var el = document.getElementById('panel-' + id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showPanel(id, btn) {
  document.querySelectorAll('.detail-panel').forEach(function(p) {
    p.classList.remove('active');
  });
  var panel = document.getElementById('panel-' + id);
  if (panel) panel.classList.add('active');

  document.querySelectorAll('.detail-nav-item').forEach(function(b) {
    b.classList.remove('active');
  });
  if (btn) {
    btn.classList.add('active');
  } else {
    // Find matching nav button
    document.querySelectorAll('.detail-nav-item').forEach(function(b) {
      if (b.textContent.toLowerCase().includes(id.replace(/-/g, ' ').split(' ')[0].toLowerCase())) {
        b.classList.add('active');
      }
    });
  }
}

function renderExtendedSections(data) {
  var d = data || {};

  // 1. Panchang
  renderPanchang(d.panchang || {});
  // 2. Graha Maitri
  renderGrahaMaitri(d.graha_maitri || {});
  // 3. Aspects
  renderAspects(d.aspects || {});
  // 4. Gemstone
  renderGemstone(d.gemstone || {});
  // 5. Nakshatra
  renderNakshatra(d.nakshatra || {});
  // 6. Sade Sati
  renderSadeSati(d.sade_sati || {});
  // 7. Kaal Sarp
  renderKaalSarp(d.kaal_sarp || {});
  // 8. Transit
  renderTransit(d.transit || {});
  // 9. Yogini Dasha
  renderYoginiDasha(d.yogini_dasha || {});
  // 10. Pitru Dosha
  renderPitruDosha(d.pitru_dosha || {});
  // 11. Yogas Extended
  renderYogasExtended(d.yogas_extended || {});
  // 12. Doshas Extended
  renderDoshasExtended(d.doshas_extended || {});
  // 13. Sudarshan Chakra
  renderSudarshan(d.sudarshan_chakra || {});
  // 14. KP System
  renderKP(d.kp_system || {});
  // 15. Varshphal
  renderVarshphal(d.varshphal || {});
  // 16. Medical
  renderMedical(d.medical_astrology || {});

  console.log('✅ All 16 extended sections rendered');
}

// Helper
function cardHTML(title, content, color) {
  color = color || 'var(--gold)';
  return '<div style="margin-bottom:16px;padding:16px;background:rgba(90,20,32,0.4);border-left:3px solid ' + color + ';border-radius:8px;">' +
    '<div style="font-size:13px;font-weight:600;color:' + color + ';margin-bottom:8px;">' + title + '</div>' +
    '<div style="font-size:13px;color:var(--ivory-muted);line-height:1.7;">' + content + '</div></div>';
}

function listHTML(items) {
  if (!items || !items.length) return '<span style="color:var(--ivory-dim);">—</span>';
  return '<ul style="padding-left:20px;margin:8px 0;">' + items.map(function(i) { return '<li style="color:var(--ivory-muted);margin-bottom:4px;">' + i + '</li>'; }).join('') + '</ul>';
}

function tableHTML(headers, rows) {
  var h = '<table style="width:100%;border-collapse:collapse;font-size:12px;margin:12px 0;">';
  h += '<thead><tr>';
  headers.forEach(function(hd) {
    h += '<th style="padding:10px 12px;background:rgba(212,169,97,0.12);color:var(--gold);font-size:10px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;text-align:left;border-bottom:1px solid rgba(212,169,97,0.3);">' + hd + '</th>';
  });
  h += '</tr></thead><tbody>';
  rows.forEach(function(r) {
    h += '<tr>';
    r.forEach(function(c, i) {
      h += '<td style="padding:8px 12px;border-bottom:1px solid rgba(212,169,97,0.15);color:var(--ivory-muted);font-size:12px;">' + c + '</td>';
    });
    h += '</tr>';
  });
  return h + '</tbody></table>';
}

// ═══ 1. PANCHANG ═══
function renderPanchang(p) {
  var t = document.getElementById('panchang-container');
  if (!t || !p.panchang) return;
  var f = p.panchang || {};
  var m = p.muhurta || {};
  var sun = p.sun_moon || {};
  var html = '';
  html += tableHTML(['Element', 'Value'], [
    ['तिथि', f.tithi || '—'],
    ['पक्ष', f.paksha_hindi || '—'],
    ['नक्षत्र', f.nakshatra || '—'],
    ['योग', f.yoga || '—'],
    ['करण', f.karana || '—'],
    ['वार', f.vaar || '—'],
    ['सूर्योदय', sun.sunrise || '—'],
    ['सूर्यास्त', sun.sunset || '—'],
    ['राहु काल', m.rahu_kaal || '—'],
    ['यमगंड', m.yamaganda || '—'],
    ['गुलिक काल', m.gulika_kaal || '—']
  ]);
  t.innerHTML = html;
}

// ═══ 2. GRAHA MAITRI ═══
function renderGrahaMaitri(g) {
  var t = document.getElementById('graha-maitri-container');
  if (!t || !g.natural) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Natural Friendships</h4>';
  var rows = [];
  Object.entries(g.natural).forEach(function(e) {
    var p = e[1];
    rows.push([p.hindi, (p.friends || []).join(', '), (p.enemies || []).join(', ')]);
  });
  html += tableHTML(['Planet', 'Friends', 'Enemies'], rows);
  t.innerHTML = html;
}

// ═══ 3. ASPECTS ═══
function renderAspects(a) {
  var t = document.getElementById('aspects-container');
  if (!t || !a.aspects) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Planetary Aspects (' + a.aspects.length + ')</h4>';
  var rows = a.aspects.slice(0, 30).map(function(asp) {
    return [asp.from_hindi, asp.aspect + 'th', asp.to_hindi, 'Bhava ' + asp.bhava];
  });
  html += tableHTML(['From', 'Aspect', 'To', 'Bhava'], rows);
  t.innerHTML = html;
}

// ═══ 4. GEMSTONE ═══
function renderGemstone(g) {
  var t = document.getElementById('gemstone-container');
  if (!t || !g.recommendations) return;
  var html = '';
  if (g.recommendations.length === 0) {
    html = '<p style="color:var(--ivory-dim);">No specific gemstone recommendation</p>';
  } else {
    g.recommendations.forEach(function(r) {
      html += cardHTML(
        '💎 ' + r.name + ' (' + r.english + ')',
        '<div><strong>Planet:</strong> ' + r.planet_hindi + '</div>' +
        '<div><strong>Metal:</strong> ' + r.metal + '</div>' +
        '<div><strong>Finger:</strong> ' + r.finger + '</div>' +
        '<div><strong>Day:</strong> ' + r.day + '</div>' +
        '<div><strong>Weight:</strong> ' + r.weight + '</div>' +
        '<div><strong>Mantra:</strong> ' + r.mantra + '</div>'
      );
    });
  }
  t.innerHTML = html;
}

// ═══ 5. NAKSHATRA ═══
function renderNakshatra(n) {
  var t = document.getElementById('nakshatra-container');
  if (!t) return;
  var bn = n.birth_nakshatra || {};
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Birth Nakshatra</h4>';
  html += cardHTML(
    '⭐ ' + (bn.name || '—') + ' (' + (bn.english || '') + ')',
    '<div><strong>Lord:</strong> ' + (bn.lord || '—') + '</div>' +
    '<div><strong>Devta:</strong> ' + (bn.devta || '—') + '</div>' +
    '<div><strong>Gana:</strong> ' + (bn.gana || '—') + '</div>' +
    '<div><strong>Yoni:</strong> ' + (bn.yoni || '—') + '</div>' +
    '<div><strong>Nadi:</strong> ' + (bn.nadi || '—') + '</div>' +
    '<div><strong>Varna:</strong> ' + (bn.varna || '—') + '</div>' +
    '<div><strong>Nature:</strong> ' + (bn.nature || '—') + '</div>'
  );
  t.innerHTML = html;
}

// ═══ 6. SADE SATI ═══
function renderSadeSati(s) {
  var t = document.getElementById('sade-sati-container');
  if (!t || !s.current_status) return;
  var cs = s.current_status;
  var html = '';
  html += cardHTML(
    '🪐 ' + (cs.status || ''),
    '<div><strong>Moon Rashi:</strong> ' + (cs.moon_rashi_hindi || '') + '</div>' +
    '<div><strong>Shani Rashi:</strong> ' + (cs.shani_rashi_hindi || '') + '</div>' +
    '<div><strong>In Sade Sati:</strong> ' + (cs.in_sade_sati ? 'हाँ' : 'नहीं') + '</div>'
  );
  if (s.effects && s.effects.length) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">Effects</h4>' + listHTML(s.effects);
  }
  if (s.remedies && s.remedies.length) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">उपाय</h4>';
    s.remedies.forEach(function(r) { html += cardHTML(r.remedy, '<em>' + r.type + '</em>', '#7ee0a0'); });
  }
  t.innerHTML = html;
}

// ═══ 7. KAAL SARP ═══
function renderKaalSarp(k) {
  var t = document.getElementById('kaal-sarp-container');
  if (!t) return;
  var html = '';
  if (!k.has_dosha) {
    html = cardHTML('✅ कोई काल सर्प दोष नहीं', 'भाग्य अनुकूल है', '#7ee0a0');
  } else {
    html += cardHTML('🐍 काल सर्प दोष', 'Type: ' + ((k.type && k.type.name) || '—'), '#f0a0a0');
    if (k.effects) html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">Effects</h4>' + listHTML(k.effects);
    if (k.remedies) {
      html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">उपाय</h4>';
      k.remedies.forEach(function(r) { html += cardHTML(r.remedy, '<em>' + r.type + '</em>', '#7ee0a0'); });
    }
  }
  t.innerHTML = html;
}

// ═══ 8. TRANSIT ═══
function renderTransit(tr) {
  var t = document.getElementById('transit-container');
  if (!t || !tr.current_transits) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Current Transits</h4>';
  var rows = tr.current_transits.map(function(x) {
    return [x.planet_hindi, x.rashi_hindi, 'Bhava ' + x.bhava, x.nature];
  });
  html += tableHTML(['Planet', 'Rashi', 'Bhava', 'Nature'], rows);
  t.innerHTML = html;
}

// ═══ 9. YOGINI DASHA ═══
function renderYoginiDasha(y) {
  var t = document.getElementById('yogini-dasha-container');
  if (!t || !y.current_yogini) return;
  var cy = y.current_yogini;
  var html = cardHTML('🎭 Current Yogini', '<strong>' + cy.name + '</strong> — ' + cy.planet + ' (' + cy.years + ' years)');
  if (y.full_cycle) {
    var rows = y.full_cycle.slice(0, 8).map(function(p) {
      return [p.yogini, p.planet, p.years + 'y', p.start, p.end, p.is_current ? '← NOW' : ''];
    });
    html += tableHTML(['Yogini', 'Planet', 'Years', 'Start', 'End', ''], rows);
  }
  t.innerHTML = html;
}

// ═══ 10. PITRU DOSHA ═══
function renderPitruDosha(p) {
  var t = document.getElementById('pitru-dosha-container');
  if (!t) return;
  var html = '';
  if (!p.has_dosha) {
    html = cardHTML('✅ कोई पितृ दोष नहीं', 'पूर्वज प्रसन्न हैं', '#7ee0a0');
  } else {
    html += cardHTML('👴 पितृ दोष', p.reasons ? p.reasons.join('<br>') : '', '#f0a0a0');
    if (p.effects) html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">Effects</h4>' + listHTML(p.effects);
    if (p.remedies) {
      html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">उपाय</h4>';
      p.remedies.forEach(function(r) { html += cardHTML(r.remedy, '<em>' + r.type + '</em>', '#7ee0a0'); });
    }
  }
  t.innerHTML = html;
}

// ═══ 11. YOGAS EXTENDED ═══
function renderYogasExtended(y) {
  var t = document.getElementById('yogas-extended-container');
  if (!t || !y.yogas) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Total: ' + (y.total || 0) + ' Yogas</h4>';
  y.yogas.forEach(function(yg) {
    html += cardHTML(
      '🌟 ' + yg.name + ' (' + yg.english + ')',
      '<div>' + (yg.description || '') + '</div>' +
      (yg.effect ? '<div style="color:#7ee0a0;margin-top:6px;">✓ ' + yg.effect + '</div>' : ''),
      'var(--gold)'
    );
  });
  t.innerHTML = html;
}

// ═══ 12. DOSHAS EXTENDED ═══
function renderDoshasExtended(d) {
  var t = document.getElementById('doshas-extended-container');
  if (!t || !d.doshas) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Total: ' + (d.total || 0) + ' Doshas</h4>';
  d.doshas.forEach(function(ds) {
    var color = ds.severity === 'High' ? '#f0a0a0' : '#f59e0b';
    html += cardHTML(
      '⚠️ ' + ds.name + ' (' + ds.english + ')',
      '<div><strong>Severity:</strong> ' + ds.severity + '</div>' +
      '<div>' + (ds.description || '') + '</div>' +
      (ds.effects ? '<div style="margin-top:8px;">' + listHTML(ds.effects) + '</div>' : '') +
      (ds.remedies ? '<div style="color:#7ee0a0;margin-top:6px;"><strong>उपाय:</strong> ' + ds.remedies.join(', ') + '</div>' : ''),
      color
    );
  });
  t.innerHTML = html;
}

// ═══ 13. SUDARSHAN CHAKRA ═══
function renderSudarshan(s) {
  var t = document.getElementById('sudarshan-container');
  if (!t || !s.combined) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Combined Chart</h4>';
  var rows = s.combined.map(function(h) {
    return ['House ' + h.house, h.from_lagna, h.from_chandra, h.from_surya];
  });
  html += tableHTML(['House', 'From Lagna', 'From Chandra', 'From Surya'], rows);
  t.innerHTML = html;
}

// ═══ 14. KP SYSTEM ═══
function renderKP(k) {
  var t = document.getElementById('kp-system-container');
  if (!t || !k.planets_kp) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">KP Planets</h4>';
  var rows = k.planets_kp.map(function(p) {
    return [p.planet, p.nakshatra, p.nakshatra_lord, p.sub_lord, 'Bhava ' + (p.bhava || '')];
  });
  html += tableHTML(['Planet', 'Nakshatra', 'Star Lord', 'Sub Lord', 'Bhava'], rows);
  t.innerHTML = html;
}

// ═══ 15. VARSHPHAL ═══
function renderVarshphal(v) {
  var t = document.getElementById('varshphal-container');
  if (!t || !v.varsha_year) return;
  var html = '';
  html += cardHTML('🎂 Varsha Number', v.varsha_year.varsha_number + ' (Age: ' + v.varsha_year.age + ')');
  if (v.muntha) html += cardHTML('🌙 Muntha', v.muntha.muntha_rashi_hindi);
  if (v.year_lord) html += cardHTML('👑 Year Lord', v.year_lord.lord_hindi + ' — ' + v.year_lord.reason);
  if (v.predictions) html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">Predictions</h4>' + listHTML(v.predictions);
  t.innerHTML = html;
}

// ═══ 16. MEDICAL ═══
function renderMedical(m) {
  var t = document.getElementById('medical-container');
  if (!t) return;
  var html = '';
  if (m.longevity) html += cardHTML('⏳ Longevity', m.longevity.duration);
  if (m.weak_planets && m.weak_planets.length) {
    html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">Weak Planets</h4>';
    m.weak_planets.forEach(function(w) { html += cardHTML(w.planet_hindi, w.reason, '#f0a0a0'); });
  }
  if (m.preventive_care) html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">Preventive Care</h4>' + listHTML(m.preventive_care);
  if (m.health_risks) html += '<h4 style="color:var(--gold);font-size:14px;margin:16px 0 12px;">Health Risks</h4>' + listHTML(m.health_risks);
  t.innerHTML = html;
}

window.scrollToPanel = scrollToPanel;
window.showPanel = showPanel;
window.renderExtendedSections = renderExtendedSections;
