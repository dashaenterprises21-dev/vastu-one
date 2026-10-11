/**
 * Vastu One — South Indian Chart Generator (v2)
 */

const SI_SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"];
const SI_SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"];

function siPlanetHindi(p) {
  const h = {"Surya":"सू","Chandra":"चं","Mangal":"मं","Budh":"बु","Guru":"गु","Shukra":"शु","Shani":"श","Rahu":"रा","Ketu":"के"};
  return h[p] || p;
}

function generateSouthIndianChart(data) {
  if (!data || !data.positions) {
    return '<div style="padding:20px;color:#888;">Chart data available nahi hai.</div>';
  }

  const lagnaRashi = data.lagna ? data.lagna.lagna_rashi : "Mesh";

  const rashiPlanets = {};
  for (let i = 0; i < 12; i++) rashiPlanets[SI_SIGNS[i]] = [];

  for (const [planet, pdata] of Object.entries(data.positions)) {
    const r = pdata.rashi;
    if (r && rashiPlanets[r] !== undefined) {
      rashiPlanets[r].push({
        planet: planet,
        hindi: pdata.hindi || siPlanetHindi(planet),
        retro: pdata.retrograde === true
      });
    }
  }

  const grid = {
    "Mesh":      { r: 0, c: 0 },
    "Vrishabh":  { r: 0, c: 1 },
    "Mithun":    { r: 0, c: 2 },
    "Kark":      { r: 0, c: 3 },
    "Simha":     { r: 1, c: 3 },
    "Kanya":     { r: 2, c: 3 },
    "Tula":      { r: 3, c: 3 },
    "Vrishchik": { r: 3, c: 2 },
    "Dhanu":     { r: 3, c: 1 },
    "Makar":     { r: 3, c: 0 },
    "Kumbh":     { r: 2, c: 0 },
    "Meen":      { r: 1, c: 0 }
  };

  const CS = 125;
  const S = CS * 4;

  let svg = '<svg viewBox="0 0 ' + S + ' ' + S + '" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:#0a0a0f;border-radius:12px;">';

  for (let i = 0; i <= 4; i++) {
    svg += '<line x1="' + (i*CS) + '" y1="0" x2="' + (i*CS) + '" y2="' + S + '" stroke="#D4AF37" stroke-width="' + (i===0||i===4?2:1.2) + '"/>';
    svg += '<line x1="0" y1="' + (i*CS) + '" x2="' + S + '" y2="' + (i*CS) + '" stroke="#D4AF37" stroke-width="' + (i===0||i===4?2:1.2) + '"/>';
  }

  svg += '<rect x="' + CS + '" y="' + CS + '" width="' + (2*CS) + '" height="' + (2*CS) + '" fill="#0a0a0f"/>';

  for (const sign of SI_SIGNS) {
    const g = grid[sign];
    const x = g.c * CS;
    const y = g.r * CS;
    const isLagna = sign === lagnaRashi;
    const signHindi = SI_SIGNS_HINDI[SI_SIGNS.indexOf(sign)];

    if (isLagna) {
      svg += '<rect x="' + (x+2) + '" y="' + (y+2) + '" width="' + (CS-4) + '" height="' + (CS-4) + '" fill="rgba(212,175,55,0.15)"/>';
    }

    svg += '<text x="' + (x + 8) + '" y="' + (y + 20) + '" fill="#D4AF37" font-size="15" font-weight="700">' + signHindi + '</text>';
    svg += '<text x="' + (x + 8) + '" y="' + (y + 34) + '" fill="#666" font-size="9">' + sign + '</text>';

    if (isLagna) {
      svg += '<text x="' + (x + CS - 8) + '" y="' + (y + 20) + '" text-anchor="end" fill="#FFD700" font-size="10" font-weight="700">LAGNA</text>';
    }

    const planets = rashiPlanets[sign] || [];
    planets.forEach(function(p, i) {
      const col = i % 2;
      const row = Math.floor(i / 2);
      const px = x + 12 + col * 60;
      const py = y + 58 + row * 22;
      const retro = p.retro ? "R" : "";
      const color = isLagna ? '#FFD700' : '#fff';
      svg += '<text x="' + px + '" y="' + py + '" fill="' + color + '" font-size="15" font-weight="600">' + p.hindi + retro + '</text>';
    });
  }

  const C2 = S / 2;
  svg += '<text x="' + C2 + '" y="' + (C2 + 8) + '" text-anchor="middle" fill="#D4AF37" font-size="28" opacity="0.6">ॐ</text>';

  svg += '</svg>';
  return svg;
}

function renderSouthIndianChart(data, targetId) {
  const t = document.getElementById(targetId);
  if (!t) return;
  t.innerHTML = generateSouthIndianChart(data);
}
window.generateSouthIndianChart = generateSouthIndianChart;
window.renderSouthIndianChart = renderSouthIndianChart;
