/**
 * Vastu One — Ashtakavarga Grid Generator
 * 12 rashis × 7 planets + Lagna, color-coded scores
 */

const AK_RASHIS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"];
const AK_RASHIS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"];

const AK_PLANETS = ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"];
const AK_PLANETS_HINDI = {
  "Surya": "सूर्य", "Chandra": "चंद्र", "Mangal": "मंगल", "Budh": "बुध",
  "Guru": "गुरु", "Shukra": "शुक्र", "Shani": "शनि"
};
const AK_PLANETS_SHORT = {
  "Surya": "सू", "Chandra": "चं", "Mangal": "मं", "Budh": "बु",
  "Guru": "गु", "Shukra": "शु", "Shani": "श"
};

/**
 * Color code for score 0-8
 */
function akColor(score) {
  if (score >= 6) return { bg: "rgba(34,197,94,0.35)",  txt: "#22c55e", border: "#22c55e" };
  if (score >= 5) return { bg: "rgba(132,204,22,0.30)", txt: "#84cc16", border: "#84cc16" };
  if (score >= 4) return { bg: "rgba(234,179,8,0.30)",  txt: "#eab308", border: "#eab308" };
  if (score >= 3) return { bg: "rgba(249,115,22,0.30)", txt: "#f97316", border: "#f97316" };
  if (score >= 1) return { bg: "rgba(239,68,68,0.30)",  txt: "#ef4444", border: "#ef4444" };
  return { bg: "rgba(100,100,100,0.20)", txt: "#666", border: "#444" };
}

function generateAshtakavargaGrid(data) {
  if (!data || !data.ashtakavarga) {
    return '<div style="padding:20px;color:#888;">Ashtakavarga data available nahi hai.</div>';
  }

  const ak = data.ashtakavarga;
  const bhinn = ak.bhinnashtakavarga || ak.bhinna || {};
  const sarva = ak.sarvashtakavarga || ak.sarva || {};

  if (Object.keys(bhinn).length === 0) {
    return '<div style="padding:20px;color:#888;">Ashtakavarga empty hai.</div>';
  }

  let html = '<div style="overflow-x:auto;padding:8px 0;">';

  // ══════════════════════════════════════════
  // TABLE 1: Bhinnashtakavarga (Planet-wise)
  // ══════════════════════════════════════════
  html += '<div style="margin-bottom:32px;">';
  html += '<h3 style="color:#D4AF37;font-size:16px;font-weight:700;margin-bottom:12px;">Bhinnashtakavarga — Planet-wise Scores</h3>';
  html += '<div style="font-size:12px;color:#888;margin-bottom:12px;">Each planet\'s score (0-8) in each rashi. Higher = stronger.</div>';

  html += '<table style="width:100%;border-collapse:separate;border-spacing:2px;font-family:Inter,sans-serif;">';

  // Header row — rashis
  html += '<thead><tr>';
  html += '<th style="padding:10px 8px;text-align:left;background:rgba(212,175,55,0.15);color:#D4AF37;font-size:11px;font-weight:700;border-radius:4px;">Planet</th>';
  AK_RASHIS_HINDI.forEach(function(r) {
    html += '<th style="padding:10px 6px;text-align:center;background:rgba(212,175,55,0.15);color:#D4AF37;font-size:11px;font-weight:700;border-radius:4px;">' + r + '</th>';
  });
  html += '<th style="padding:10px 6px;text-align:center;background:rgba(212,175,55,0.25);color:#FFD700;font-size:11px;font-weight:700;border-radius:4px;">Total</th>';
  html += '</tr></thead>';

  // Body rows
  html += '<tbody>';
  AK_PLANETS.forEach(function(planet) {
    const pData = bhinn[planet] || {};
    const scores = pData.scores || [];
    const total = pData.total || 0;
    const avg = pData.average || (scores.length > 0 ? (total / scores.length) : 0);

    html += '<tr>';
    // Planet name
    html += '<td style="padding:8px;background:rgba(255,255,255,0.04);color:#fff;font-size:12px;font-weight:600;border-radius:4px;">';
    html += AK_PLANETS_HINDI[planet] || planet;
    html += '</td>';

    // Scores
    for (let i = 0; i < 12; i++) {
      const score = scores[i] !== undefined ? scores[i] : 0;
      const c = akColor(score);
      html += '<td style="padding:8px 6px;text-align:center;background:' + c.bg + ';color:' + c.txt + ';font-size:13px;font-weight:700;border-radius:4px;">' + score + '</td>';
    }

    // Total
    html += '<td style="padding:8px 6px;text-align:center;background:rgba(212,175,55,0.15);color:#FFD700;font-size:13px;font-weight:700;border-radius:4px;">' + total + '</td>';
    html += '</tr>';
  });
  html += '</tbody>';
  html += '</table>';
  html += '</div>';

  // ══════════════════════════════════════════
  // TABLE 2: Sarvashtakavarga (Sum)
  // ══════════════════════════════════════════
  html += '<div style="margin-bottom:32px;">';
  html += '<h3 style="color:#D4AF37;font-size:16px;font-weight:700;margin-bottom:12px;">Sarvashtakavarga — Total Strength per Rashi</h3>';
  html += '<div style="font-size:12px;color:#888;margin-bottom:12px;">Sum of all planets\' scores. Higher total = rashi stronger. Max ~56.</div>';

  // Compute sarva from bhinn if not available
  let sarvaScores = [];
  if (Array.isArray(sarva) && sarva.length === 12) {
    sarvaScores = sarva;
  } else if (sarva.scores && sarva.scores.length === 12) {
    sarvaScores = sarva.scores;
  } else {
    // Compute from bhinn
    for (let i = 0; i < 12; i++) {
      let sum = 0;
      AK_PLANETS.forEach(function(p) {
        const pData = bhinn[p] || {};
        const scores = pData.scores || [];
        sum += (scores[i] || 0);
      });
      sarvaScores.push(sum);
    }
  }

  const maxSarva = Math.max.apply(null, sarvaScores.concat([1]));

  html += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;">';
  AK_RASHIS_HINDI.forEach(function(rashi, idx) {
    const score = sarvaScores[idx] || 0;
    const pct = Math.round((score / maxSarva) * 100);
    let color;
    if (score >= 30) color = "#22c55e";
    else if (score >= 25) color = "#84cc16";
    else if (score >= 20) color = "#eab308";
    else if (score >= 15) color = "#f97316";
    else color = "#ef4444";

    html += '<div style="padding:12px 8px;background:rgba(255,255,255,0.03);border-radius:8px;text-align:center;border:1px solid ' + color + '44;">';
    html += '<div style="font-size:12px;color:#888;margin-bottom:6px;">' + rashi + '</div>';
    html += '<div style="font-size:22px;font-weight:700;color:' + color + ';">' + score + '</div>';
    html += '<div style="margin-top:6px;height:4px;background:rgba(255,255,255,0.1);border-radius:2px;overflow:hidden;">';
    html += '<div style="height:100%;width:' + pct + '%;background:' + color + ';border-radius:2px;"></div>';
    html += '</div>';
    html += '</div>';
  });
  html += '</div>';
  html += '</div>';

  // ══════════════════════════════════════════
  // LEGEND
  // ══════════════════════════════════════════
  html += '<div style="padding:12px;background:rgba(255,255,255,0.02);border-radius:8px;">';
  html += '<div style="font-size:11px;color:#888;margin-bottom:8px;">SCORE LEGEND (Bhinnashtakavarga)</div>';
  html += '<div style="display:flex;flex-wrap:wrap;gap:12px;font-size:11px;">';
  const legendItems = [
    { label: "6-8 (Strong)", color: "#22c55e" },
    { label: "5 (Good)", color: "#84cc16" },
    { label: "4 (Average)", color: "#eab308" },
    { label: "3 (Below Avg)", color: "#f97316" },
    { label: "1-2 (Weak)", color: "#ef4444" },
    { label: "0 (Very Weak)", color: "#666" }
  ];
  legendItems.forEach(function(item) {
    html += '<div style="display:flex;align-items:center;gap:6px;">';
    html += '<span style="display:inline-block;width:14px;height:14px;background:' + item.color + ';border-radius:3px;"></span>';
    html += '<span style="color:#ccc;">' + item.label + '</span>';
    html += '</div>';
  });
  html += '</div>';
  html += '</div>';

  html += '</div>';
  return html;
}

function renderAshtakavargaGrid(data, targetId) {
  const t = document.getElementById(targetId);
  if (!t) return;
  t.innerHTML = generateAshtakavargaGrid(data);
}

window.generateAshtakavargaGrid = generateAshtakavargaGrid;
window.renderAshtakavargaGrid = renderAshtakavargaGrid;
