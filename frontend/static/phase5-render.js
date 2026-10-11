/**
 * Vastu One — Phase 5 Renderer
 * Shadvarga, Guna Milan, Numerology, Classical References
 */

function renderPhase5Sections(data) {
  if (!data) return;
  renderShadvarga(data.shadvarga || {});
  renderGunaMilan(data.ashtakoota || {});
  renderNumerology(data.numerology || {});
  renderClassicalRefs(data.classical_references || []);
}

// ═══ 1. SHADVARGA ═══
function renderShadvarga(s) {
  var t = document.getElementById('shadvarga-container');
  if (!t || !s) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">7 Divisional Charts</h4>';
  Object.entries(s).forEach(function(e) {
    var varga = e[0];
    var v = e[1];
    html += '<div style="margin-bottom:16px;padding:14px;background:rgba(90,20,32,0.4);border-left:3px solid var(--gold);border-radius:8px;">';
    html += '<div style="font-size:14px;color:var(--gold);font-weight:600;margin-bottom:6px;">' + varga + ' — ' + v.name + '</div>';
    html += '<div style="font-size:12px;color:var(--ivory-muted);margin-bottom:8px;">' + v.meaning + ' · Lagna: ' + v.lagna_hindi + '</div>';
    html += '<div style="font-size:11.5px;color:var(--ivory-muted);line-height:1.6;">';
    Object.entries(v.planets || {}).forEach(function(pe) {
      var p = pe[1];
      html += '<span style="display:inline-block;margin-right:12px;"><strong style="color:var(--gold);">' + p.hindi + '</strong> ' + p.varga_rashi_hindi + '</span>';
    });
    html += '</div></div>';
  });
  t.innerHTML = html;
}

// ═══ 2. GUNA MILAN ═══
function renderGunaMilan(g) {
  var t = document.getElementById('guna-milan-container');
  if (!t || !g.scores) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">Ashtakoota Guna Milan — ' + g.total + '/36</h4>';
  html += '<div style="padding:16px;background:rgba(212,169,97,0.1);border-radius:10px;text-align:center;margin-bottom:16px;">';
  html += '<div style="font-size:32px;color:var(--gold);font-weight:700;">' + g.total + '/36</div>';
  html += '<div style="font-size:13px;color:var(--ivory-muted);margin-top:6px;">' + g.percentage + '% · ' + g.verdict + '</div>';
  html += '</div>';
  var rows = [];
  Object.entries(g.scores).forEach(function(e) {
    var name = e[0].replace(/_/g, ' ').toUpperCase();
    var sc = e[1];
    rows.push([name, sc.score + '/' + sc.max]);
  });
  html += '<table style="width:100%;border-collapse:collapse;font-size:12px;">';
  rows.forEach(function(r) {
    html += '<tr><td style="padding:8px;border-bottom:1px solid rgba(212,169,97,0.15);color:var(--ivory-muted);">' + r[0] + '</td>';
    html += '<td style="padding:8px;border-bottom:1px solid rgba(212,169,97,0.15);color:var(--gold);font-weight:600;text-align:right;">' + r[1] + '</td></tr>';
  });
  html += '</table>';
  t.innerHTML = html;
}

// ═══ 3. NUMEROLOGY ═══
function renderNumerology(n) {
  var t = document.getElementById('numerology-container');
  if (!t || !n.mulank) return;
  var html = '';
  html += cardHTML('🔢 Mulank (Birth Number)', '<strong style="color:var(--gold);font-size:20px;">' + n.mulank.number + '</strong> — ' + n.mulank.info.hindi + '<br><span style="color:var(--ivory-dim);font-size:12px;">' + n.mulank.info.traits + '</span>');
  html += cardHTML('🌟 Bhagyank (Destiny Number)', '<strong style="color:var(--gold);font-size:20px;">' + n.bhagyank.number + '</strong> — ' + n.bhagyank.info.hindi + '<br><span style="color:var(--ivory-dim);font-size:12px;">' + n.bhagyank.info.traits + '</span>');
  html += cardHTML('�� Naamank (Chaldean)', '<strong style="color:var(--gold);font-size:20px;">' + n.naamank_chaldean.number + '</strong><br><span style="color:var(--ivory-dim);font-size:12px;">' + n.naamank_chaldean.info.hindi + '</span>');
  html += cardHTML('📝 Naamank (Pythagorean)', '<strong style="color:var(--gold);font-size:20px;">' + n.naamank_pythagorean.number + '</strong>');
  html += cardHTML('✨ Lucky Details', 
    '<div><strong style="color:var(--gold);">Number:</strong> ' + n.lucky_number + '</div>' +
    '<div><strong style="color:var(--gold);">Color:</strong> ' + n.lucky_color + '</div>' +
    '<div><strong style="color:var(--gold);">Day:</strong> ' + n.lucky_day + '</div>' +
    '<div><strong style="color:var(--gold);">Gemstone:</strong> ' + n.lucky_gemstone + '</div>');
  t.innerHTML = html;
}

// ═══ 4. CLASSICAL REFERENCES ═══
function renderClassicalRefs(refs) {
  var t = document.getElementById('classical-refs-container');
  if (!t || !refs || !refs.length) return;
  var html = '<h4 style="color:var(--gold);font-size:14px;margin-bottom:12px;">' + refs.length + ' Classical References</h4>';
  var rows = refs.slice(0, 30).map(function(r) {
    return [r.text + ' ' + r.chapter + '.' + r.shloka, r.ref];
  });
  html += '<table style="width:100%;border-collapse:collapse;font-size:11.5px;">';
  html += '<thead><tr style="background:rgba(212,169,97,0.12);"><th style="padding:10px;text-align:left;color:var(--gold);font-size:10px;text-transform:uppercase;letter-spacing:0.1em;">Reference</th><th style="padding:10px;text-align:left;color:var(--gold);font-size:10px;text-transform:uppercase;letter-spacing:0.1em;">Description</th></tr></thead><tbody>';
  rows.forEach(function(r) {
    html += '<tr><td style="padding:8px 10px;border-bottom:1px solid rgba(212,169,97,0.15);color:var(--gold);font-family:monospace;">' + r[0] + '</td>';
    html += '<td style="padding:8px 10px;border-bottom:1px solid rgba(212,169,97,0.15);color:var(--ivory-muted);">' + r[1] + '</td></tr>';
  });
  html += '</tbody></table>';
  t.innerHTML = html;
}

function cardHTML(title, content) {
  return '<div style="margin-bottom:12px;padding:14px;background:rgba(90,20,32,0.4);border-left:3px solid var(--gold);border-radius:8px;">' +
    '<div style="font-size:12px;color:var(--gold);font-weight:600;margin-bottom:6px;">' + title + '</div>' +
    '<div style="font-size:13px;color:var(--ivory-muted);line-height:1.6;">' + content + '</div></div>';
}

// Hook into existing renderExtendedSections
var origExtended = window.renderExtendedSections;
window.renderExtendedSections = function(data) {
  if (origExtended) origExtended(data);
  renderPhase5Sections(data);
};

window.renderPhase5Sections = renderPhase5Sections;
console.log('✅ Phase 5 renderer loaded');
