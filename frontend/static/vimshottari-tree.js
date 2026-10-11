/**
 * Vastu One — Vimshottari Nested Tree
 * Expandable Maha → Antar → Pratyantar tree view
 */

const VT_PLANETS_HINDI = {
  "Surya": "सूर्य", "Chandra": "चंद्र", "Mangal": "मंगल", "Budh": "बुध",
  "Guru": "गुरु", "Shukra": "शुक्र", "Shani": "शनि", "Rahu": "राहु", "Ketu": "केतु"
};

const VT_COLORS = {
  "Surya": "#FF6B35", "Chandra": "#C0C0C0", "Mangal": "#DC143C",
  "Budh": "#4CAF50", "Guru": "#FFD700", "Shukra": "#FF69B4",
  "Shani": "#4A4A8A", "Rahu": "#8B4513", "Ketu": "#808080"
};

let VT_TREE_DATA = null;
let VT_EXPANDED = {};

/**
 * Generate tree HTML from dasha data
 */
function generateVimshottariTree(data) {
  if (!data || !data.dasha) {
    return '<div style="padding:20px;color:#888;">Dasha data available nahi hai.</div>';
  }

  const dasha = data.dasha;
  const mahadashas = dasha.mahadashas || [];
  const currentMaha = dasha.current_mahadasha || {};
  const currentAntar = dasha.current_antardasha || {};
  const currentPratyantar = dasha.current_pratyantardasha || {};

  if (mahadashas.length === 0) {
    return '<div style="padding:20px;color:#888;">Mahadasha list empty hai.</div>';
  }

  // Store for later
  VT_TREE_DATA = {
    mahadashas: mahadashas,
    currentMaha: currentMaha.planet,
    currentAntar: currentAntar.planet,
    currentPratyantar: currentPratyantar.planet
  };

  // Auto-expand current mahadasha
  VT_EXPANDED = {};
  mahadashas.forEach(function(m, idx) {
    if (m.planet === currentMaha.planet) {
      VT_EXPANDED['m_' + idx] = true;
    }
  });

  let html = '<div style="padding:8px 0;">';

  // Summary card
  html += '<div style="background:rgba(212,175,55,0.08);border-left:4px solid #D4AF37;padding:16px;border-radius:8px;margin-bottom:20px;">';
  html += '<div style="font-size:11px;color:#D4AF37;font-weight:700;letter-spacing:1px;margin-bottom:8px;">CURRENT PERIOD</div>';
  html += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;">';
  html += '<div><div style="font-size:10px;color:#888;">MAHADASHA</div><div style="font-size:15px;color:#fff;font-weight:700;">' + (VT_PLANETS_HINDI[currentMaha.planet] || currentMaha.planet || '—') + '</div></div>';
  html += '<div><div style="font-size:10px;color:#888;">ANTARDASHA</div><div style="font-size:15px;color:#fff;font-weight:700;">' + (VT_PLANETS_HINDI[currentAntar.planet] || currentAntar.planet || '—') + '</div></div>';
  html += '<div><div style="font-size:10px;color:#888;">PRATYANTARDASHA</div><div style="font-size:15px;color:#fff;font-weight:700;">' + (VT_PLANETS_HINDI[currentPratyantar.planet] || currentPratyantar.planet || '—') + '</div></div>';
  html += '</div>';
  html += '</div>';

  // Tree
  html += '<div style="font-family:Inter,sans-serif;">';
  mahadashas.forEach(function(m, mIdx) {
    html += renderMahaNode(m, mIdx);
  });
  html += '</div>';

  html += '</div>';
  return html;
}

function renderMahaNode(m, mIdx) {
  const planet = m.planet || "";
  const isCurrent = VT_TREE_DATA && VT_TREE_DATA.currentMaha === planet;
  const isExpanded = VT_EXPANDED['m_' + mIdx] === true;
  const color = VT_COLORS[planet] || "#666";
  const antars = m.antardashas || [];

  let html = '<div style="margin-bottom:8px;border-left:3px solid ' + color + ';background:rgba(255,255,255,0.02);border-radius:6px;overflow:hidden;">';

  // Maha header
  html += '<div onclick="toggleVimshottariNode(' + "'m_" + mIdx + "'" + ')" style="padding:12px 16px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;' + (isCurrent ? 'background:rgba(255,215,0,0.1);' : '') + '">';
  html += '<div style="display:flex;align-items:center;gap:12px;">';
  html += '<span style="color:' + color + ';font-size:18px;">' + (isExpanded ? '▼' : '▶') + '</span>';
  html += '<span style="display:inline-block;width:10px;height:10px;background:' + color + ';border-radius:50%;"></span>';
  html += '<span style="font-weight:700;color:#fff;font-size:14px;">' + (VT_PLANETS_HINDI[planet] || planet) + '</span>';
  html += '<span style="color:#888;font-size:11px;">(' + planet + ')</span>';
  if (isCurrent) {
    html += '<span style="background:#FFD700;color:#000;font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;">NOW</span>';
  }
  html += '</div>';
  html += '<div style="color:#888;font-size:11px;">' + (m.start_date || '') + ' → ' + (m.end_date || '') + ' • ' + (m.duration_years || 0) + 'y</div>';
  html += '</div>';

  // Antardasha container
  if (isExpanded && antars.length > 0) {
    html += '<div style="padding:0 0 8px 0;">';
    antars.forEach(function(a, aIdx) {
      html += renderAntarNode(a, mIdx, aIdx, color);
    });
    html += '</div>';
  }

  html += '</div>';
  return html;
}

function renderAntarNode(a, mIdx, aIdx, parentColor) {
  const planet = a.planet || "";
  const isCurrent = VT_TREE_DATA && VT_TREE_DATA.currentAntar === planet && VT_TREE_DATA.currentMaha === (VT_TREE_DATA.mahadashas[mIdx] || {}).planet;
  const isExpanded = VT_EXPANDED['a_' + mIdx + '_' + aIdx] === true;
  const color = VT_COLORS[planet] || "#666";
  const pratyantars = a.pratyantardashas || [];

  let html = '<div style="margin:6px 0 6px 30px;border-left:2px solid ' + color + ';background:rgba(255,255,255,0.01);border-radius:4px;">';

  html += '<div onclick="toggleVimshottariNode(' + "'a_" + mIdx + "_" + aIdx + "'" + ')" style="padding:8px 14px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;' + (isCurrent ? 'background:rgba(255,215,0,0.08);' : '') + '">';
  html += '<div style="display:flex;align-items:center;gap:10px;">';
  html += '<span style="color:' + color + ';font-size:13px;">' + (pratyantars.length > 0 ? (isExpanded ? '▼' : '▶') : '•') + '</span>';
  html += '<span style="display:inline-block;width:7px;height:7px;background:' + color + ';border-radius:50%;"></span>';
  html += '<span style="font-weight:600;color:#ddd;font-size:12px;">' + (VT_PLANETS_HINDI[planet] || planet) + '</span>';
  if (isCurrent) {
    html += '<span style="background:#FFD700;color:#000;font-size:8px;font-weight:700;padding:1px 5px;border-radius:3px;">NOW</span>';
  }
  html += '</div>';
  html += '<div style="color:#666;font-size:10px;">' + (a.start_date || '') + ' → ' + (a.end_date || '') + '</div>';
  html += '</div>';

  // Pratyantar container
  if (isExpanded && pratyantars.length > 0) {
    html += '<div style="padding:4px 0 6px 0;">';
    pratyantars.forEach(function(p, pIdx) {
      html += renderPratyantarNode(p, mIdx, aIdx, pIdx);
    });
    html += '</div>';
  }

  html += '</div>';
  return html;
}

function renderPratyantarNode(p, mIdx, aIdx, pIdx) {
  const planet = p.planet || "";
  const color = VT_COLORS[planet] || "#666";
  const isCurrent = VT_TREE_DATA && VT_TREE_DATA.currentPratyantar === planet;

  let html = '<div style="margin:3px 0 3px 30px;padding:6px 12px;display:flex;align-items:center;justify-content:space-between;' + (isCurrent ? 'background:rgba(255,215,0,0.06);border-radius:4px;' : '') + '">';
  html += '<div style="display:flex;align-items:center;gap:8px;">';
  html += '<span style="display:inline-block;width:5px;height:5px;background:' + color + ';border-radius:50%;"></span>';
  html += '<span style="color:#bbb;font-size:11px;">' + (VT_PLANETS_HINDI[planet] || planet) + '</span>';
  if (isCurrent) {
    html += '<span style="background:#FFD700;color:#000;font-size:7px;font-weight:700;padding:1px 4px;border-radius:3px;">NOW</span>';
  }
  html += '</div>';
  html += '<div style="color:#555;font-size:9px;">' + (p.start_date || '') + ' → ' + (p.end_date || '') + '</div>';
  html += '</div>';
  return html;
}

function toggleVimshottariNode(nodeId) {
  VT_EXPANDED[nodeId] = !VT_EXPANDED[nodeId];
  // Re-render
  const container = document.getElementById('vimshottari-tree-container');
  if (container && VT_TREE_DATA) {
    container.innerHTML = generateVimshottariTree({ dasha: VT_TREE_DATA });
  }
}

function renderVimshottariTree(data, targetId) {
  const t = document.getElementById(targetId);
  if (!t) return;
  t.innerHTML = generateVimshottariTree(data);
}

window.generateVimshottariTree = generateVimshottariTree;
window.renderVimshottariTree = renderVimshottariTree;
window.toggleVimshottariNode = toggleVimshottariNode;
