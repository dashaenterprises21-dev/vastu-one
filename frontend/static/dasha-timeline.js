/**
 * Vastu One — Dasha Timeline Generator
 * 120-year Vimshottari Dasha visual timeline
 */

const DASHA_PLANETS_HINDI = {
  "Surya": "सू", "Chandra": "चं", "Mangal": "मं", "Budh": "बु",
  "Guru": "गु", "Shukra": "शु", "Shani": "श", "Rahu": "रा", "Ketu": "के"
};

const DASHA_PLANETS_FULL_HINDI = {
  "Surya": "सूर्य", "Chandra": "चंद्र", "Mangal": "मंगल", "Budh": "बुध",
  "Guru": "गुरु", "Shukra": "शुक्र", "Shani": "शनि", "Rahu": "राहु", "Ketu": "केतु"
};

const DASHA_COLORS = {
  "Surya": "#FF6B35", "Chandra": "#C0C0C0", "Mangal": "#DC143C",
  "Budh": "#4CAF50", "Guru": "#FFD700", "Shukra": "#FF69B4",
  "Shani": "#4A4A8A", "Rahu": "#8B4513", "Ketu": "#808080"
};

/**
 * Generate Dasha Timeline (horizontal bar chart)
 */
function generateDashaTimeline(data) {
  if (!data || !data.dasha) {
    return '<div style="padding:20px;color:#888;">Dasha data available nahi hai.</div>';
  }

  const dashaData = data.dasha;
  const mahadashas = dashaData.mahadashas || [];
  const current = dashaData.current_mahadasha || {};

  if (mahadashas.length === 0) {
    return '<div style="padding:20px;color:#888;">Mahadasha list empty hai.</div>';
  }

  // Calculate total years for scale
  let totalYears = 0;
  const startYear = 0; // relative year
  mahadashas.forEach(function(m) {
    totalYears += (m.duration_years || 0);
  });

  if (totalYears === 0) totalYears = 120;

  const W = 1100;
  const H = 240;
  const PAD_LEFT = 60;
  const PAD_RIGHT = 40;
  const BAR_Y = 80;
  const BAR_H = 50;
  const chartW = W - PAD_LEFT - PAD_RIGHT;

  // Scale: pixels per year
  const pxPerYear = chartW / totalYears;

  let svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;background:#0a0a0f;border-radius:12px;font-family:Inter,sans-serif;">';

  // Title
  svg += '<text x="' + (W/2) + '" y="30" text-anchor="middle" fill="#D4AF37" font-size="18" font-weight="700">Vimshottari Dasha Timeline</text>';
  svg += '<text x="' + (W/2) + '" y="50" text-anchor="middle" fill="#888" font-size="12">120 Years — Vimshottari Mahadasha</text>';

  // Background bar
  svg += '<rect x="' + PAD_LEFT + '" y="' + BAR_Y + '" width="' + chartW + '" height="' + BAR_H + '" fill="#1a1a24" stroke="#333" stroke-width="1"/>';

  // Draw each mahadasha block
  let currentX = PAD_LEFT;
  let cumulativeYear = 0;

  mahadashas.forEach(function(m, idx) {
    const duration = m.duration_years || 0;
    const blockW = duration * pxPerYear;
    const planet = m.planet || "";
    const color = DASHA_COLORS[planet] || "#666";
    const isCurrent = (planet === current.planet);

    // Block
    svg += '<rect x="' + currentX + '" y="' + BAR_Y + '" width="' + blockW + '" height="' + BAR_H + '" fill="' + color + '" opacity="' + (isCurrent ? 1 : 0.65) + '" stroke="' + (isCurrent ? '#FFD700' : '#333') + '" stroke-width="' + (isCurrent ? 2 : 1) + '"/>';

    // Current highlight
    if (isCurrent) {
      svg += '<rect x="' + (currentX - 2) + '" y="' + (BAR_Y - 2) + '" width="' + (blockW + 4) + '" height="' + (BAR_H + 4) + '" fill="none" stroke="#FFD700" stroke-width="2" stroke-dasharray="4,2"/>';
    }

    // Planet symbol
    if (blockW > 30) {
      svg += '<text x="' + (currentX + blockW/2) + '" y="' + (BAR_Y + 22) + '" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">' + (DASHA_PLANETS_HINDI[planet] || planet[0]) + '</text>';
      svg += '<text x="' + (currentX + blockW/2) + '" y="' + (BAR_Y + 38) + '" text-anchor="middle" fill="#fff" font-size="11" opacity="0.9">' + duration + 'y</text>';
    }

    // Year marks below
    const startAge = m.start_age || 0;
    const endAge = m.end_age || 0;
    if (blockW > 40) {
      svg += '<text x="' + currentX + '" y="' + (BAR_Y + BAR_H + 16) + '" fill="#666" font-size="9">' + startAge.toFixed(0) + '</text>';
    }
    if (idx === mahadashas.length - 1 || blockW > 40) {
      svg += '<text x="' + (currentX + blockW) + '" y="' + (BAR_Y + BAR_H + 16) + '" text-anchor="end" fill="#666" font-size="9">' + endAge.toFixed(0) + '</text>';
    }

    // Dates above block (only if wide enough)
    if (blockW > 70) {
      const startDate = (m.start_date || "").substring(0, 7);
      const endDate = (m.end_date || "").substring(0, 7);
      svg += '<text x="' + (currentX + blockW/2) + '" y="' + (BAR_Y - 12) + '" text-anchor="middle" fill="#aaa" font-size="9">' + startDate + '</text>';
      svg += '<text x="' + (currentX + blockW/2) + '" y="' + (BAR_Y - 2) + '" text-anchor="middle" fill="#aaa" font-size="9">' + endDate + '</text>';
    }

    currentX += blockW;
    cumulativeYear += duration;
  });

  // "Now" marker
  let nowX = PAD_LEFT;
  const currentStart = (current.start_date || "").substring(0, 10);
  let cumulativeForNow = 0;
  for (let i = 0; i < mahadashas.length; i++) {
    const m = mahadashas[i];
    if ((m.start_date || "").substring(0, 10) === currentStart) {
      // Found current — calculate position within it
      const today = new Date();
      const mStart = new Date(m.start_date);
      const mEnd = new Date(m.end_date);
      const totalMs = mEnd - mStart;
      const elapsedMs = today - mStart;
      const fraction = Math.max(0, Math.min(1, elapsedMs / totalMs));
      nowX = PAD_LEFT + (cumulativeForNow * pxPerYear) + (fraction * (m.duration_years || 0) * pxPerYear);
      break;
    }
    cumulativeForNow += (m.duration_years || 0);
  }

  svg += '<line x1="' + nowX + '" y1="' + (BAR_Y - 25) + '" x2="' + nowX + '" y2="' + (BAR_Y + BAR_H + 25) + '" stroke="#FFD700" stroke-width="2" stroke-dasharray="5,3"/>';
  svg += '<text x="' + nowX + '" y="' + (BAR_Y - 30) + '" text-anchor="middle" fill="#FFD700" font-size="11" font-weight="700">NOW</text>';

  // Legend
  const legendY = H - 25;
  let legendX = PAD_LEFT;
  const planetList = ["Surya", "Chandra", "Mangal", "Budh", "Guru", "Shukra", "Shani", "Rahu", "Ketu"];
  planetList.forEach(function(p) {
    svg += '<rect x="' + legendX + '" y="' + (legendY - 8) + '" width="10" height="10" fill="' + DASHA_COLORS[p] + '"/>';
    svg += '<text x="' + (legendX + 14) + '" y="' + legendY + '" fill="#888" font-size="10">' + (DASHA_PLANETS_FULL_HINDI[p] || p) + '</text>';
    legendX += 70;
  });

  svg += '</svg>';
  return svg;
}

/**
 * Generate Dasha Table (detailed list)
 */
function generateDashaTable(data) {
  if (!data || !data.dasha) {
    return '';
  }

  const mahadashas = data.dasha.mahadashas || [];
  const current = data.dasha.current_mahadasha || {};
  const currentPlanet = current.planet;

  let html = '<div style="margin-top:24px;overflow-x:auto;">';
  html += '<table style="width:100%;border-collapse:collapse;color:#fff;font-size:13px;">';
  html += '<thead><tr style="background:rgba(212,175,55,0.1);">';
  html += '<th style="padding:10px;text-align:left;border-bottom:1px solid #333;color:#D4AF37;">#</th>';
  html += '<th style="padding:10px;text-align:left;border-bottom:1px solid #333;color:#D4AF37;">Planet</th>';
  html += '<th style="padding:10px;text-align:left;border-bottom:1px solid #333;color:#D4AF37;">Start</th>';
  html += '<th style="padding:10px;text-align:left;border-bottom:1px solid #333;color:#D4AF37;">End</th>';
  html += '<th style="padding:10px;text-align:left;border-bottom:1px solid #333;color:#D4AF37;">Age</th>';
  html += '<th style="padding:10px;text-align:left;border-bottom:1px solid #333;color:#D4AF37;">Duration</th>';
  html += '<th style="padding:10px;text-align:left;border-bottom:1px solid #333;color:#D4AF37;">Status</th>';
  html += '</tr></thead><tbody>';

  mahadashas.forEach(function(m, idx) {
    const planet = m.planet || "";
    const isCurrent = (planet === currentPlanet);
    const rowBg = isCurrent ? 'rgba(255,215,0,0.15)' : (idx % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent');
    const status = isCurrent ? '🟢 CURRENT' : (idx < mahadashas.findIndex(function(x) { return x.planet === currentPlanet; }) ? 'Past' : 'Future');

    html += '<tr style="background:' + rowBg + ';">';
    html += '<td style="padding:8px 10px;border-bottom:1px solid #222;">' + (idx + 1) + '</td>';
    html += '<td style="padding:8px 10px;border-bottom:1px solid #222;">';
    html += '<span style="display:inline-block;width:8px;height:8px;background:' + (DASHA_COLORS[planet] || '#666') + ';border-radius:50%;margin-right:6px;"></span>';
    html += (DASHA_PLANETS_FULL_HINDI[planet] || planet) + ' (' + planet + ')';
    html += '</td>';
    html += '<td style="padding:8px 10px;border-bottom:1px solid #222;">' + (m.start_date || '') + '</td>';
    html += '<td style="padding:8px 10px;border-bottom:1px solid #222;">' + (m.end_date || '') + '</td>';
    html += '<td style="padding:8px 10px;border-bottom:1px solid #222;">' + (m.start_age ? m.start_age.toFixed(0) : '') + ' - ' + (m.end_age ? m.end_age.toFixed(0) : '') + '</td>';
    html += '<td style="padding:8px 10px;border-bottom:1px solid #222;">' + (m.duration_years || '') + ' years</td>';
    html += '<td style="padding:8px 10px;border-bottom:1px solid #222;">' + status + '</td>';
    html += '</tr>';
  });

  html += '</tbody></table></div>';
  return html;
}

function renderDashaTimeline(data, targetId) {
  const t = document.getElementById(targetId);
  if (!t) return;
  t.innerHTML = generateDashaTimeline(data) + generateDashaTable(data);
}

window.generateDashaTimeline = generateDashaTimeline;
window.generateDashaTable = generateDashaTable;
window.renderDashaTimeline = renderDashaTimeline;
