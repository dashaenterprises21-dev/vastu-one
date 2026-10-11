/**
 * Vastu One — North Indian Chart v3
 * House-fixed, sign-rotating layout
 * Proper planet placement in diamond triangles
 */

const NI_SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"];
const NI_SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"];
const NI_PLANET_HINDI = {"Surya":"सू","Chandra":"चं","Mangal":"मं","Budh":"बु","Guru":"गु","Shukra":"शु","Shani":"श","Rahu":"रा","Ketu":"के"};

function niPlanetHindi(p) {
  return NI_PLANET_HINDI[p] || p;
}

function generateNorthIndianChart(data) {
  if (!data || !data.positions) {
    return '<div style="padding:20px;color:#888;">Chart data available nahi hai.</div>';
  }

  const lagnaRashi = data.lagna ? data.lagna.lagna_rashi : "Mesh";
  const lagnaIdx = NI_SIGNS.indexOf(lagnaRashi);

  // Build bhava -> planets map
  const bhavaPlanets = {};
  for (let i = 1; i <= 12; i++) bhavaPlanets[i] = [];
  for (const [planet, pd] of Object.entries(data.positions)) {
    if (pd.bhav >= 1 && pd.bhav <= 12) {
      bhavaPlanets[pd.bhav].push({
        hindi: pd.hindi || niPlanetHindi(planet),
        retro: pd.retrograde === true
      });
    }
  }

  const S = 600;
  const M = 20;
  const C = S / 2;
  const W = S - 2 * M;

  // ═══ TRADITIONAL NORTH INDIAN LAYOUT ═══
  // 12 triangles — each bhava ka center coordinate
  // Layout: Diamond + diagonals create 12 triangular sections
  // House 1 = top-center (Lagna), anti-clockwise
  const bhavaCenters = {
    1:  [C, M + 55],           // Top-center (Lagna)
    2:  [M + 55, M + 55],      // Top-left corner
    3:  [M + 55, M + 150],     // Left-upper
    4:  [M + 80, C],           // Left-center
    5:  [M + 55, S - M - 150], // Left-lower
    6:  [M + 55, S - M - 55],  // Bottom-left corner
    7:  [C, S - M - 55],       // Bottom-center
    8:  [S - M - 55, S - M - 55], // Bottom-right corner
    9:  [S - M - 55, S - M - 150], // Right-lower
    10: [S - M - 80, C],       // Right-center
    11: [S - M - 55, M + 150], // Right-upper
    12: [S - M - 55, M + 55]   // Top-right corner
  };

  let svg = '<svg viewBox="0 0 ' + S + ' ' + S + '" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:transparent;border-radius:12px;">';

  // Background
  svg += '<rect x="' + M + '" y="' + M + '" width="' + W + '" height="' + W + '" fill="rgba(10,10,18,0.6)" stroke="rgba(212,175,55,0.4)" stroke-width="1.5"/>';

  // Two diagonals (corner to corner)
  svg += '<line x1="' + M + '" y1="' + M + '" x2="' + (S-M) + '" y2="' + (S-M) + '" stroke="rgba(212,175,55,0.5)" stroke-width="1"/>';
  svg += '<line x1="' + (S-M) + '" y1="' + M + '" x2="' + M + '" y2="' + (S-M) + '" stroke="rgba(212,175,55,0.5)" stroke-width="1"/>';

  // Inner diamond
  svg += '<polygon points="' + C + ',' + M + ' ' + (S-M) + ',' + C + ' ' + C + ',' + (S-M) + ' ' + M + ',' + C + '" fill="none" stroke="rgba(212,175,55,0.6)" stroke-width="1.5"/>';

  // ═══ DRAW EACH BHAVA ═══
  for (let bhav = 1; bhav <= 12; bhav++) {
    const pos = bhavaCenters[bhav];
    const rashiIdx = (lagnaIdx + bhav - 1) % 12;
    const rashiHindi = NI_SIGNS_HINDI[rashiIdx];

    // House number — small, top-left of cell
    svg += '<text x="' + (pos[0] - 28) + '" y="' + (pos[1] - 18) + '" fill="#D4AF37" font-size="11" font-weight="700" opacity="0.7">' + bhav + '</text>';

    // Rashi name (Hindi) — below house number
    svg += '<text x="' + (pos[0] - 24) + '" y="' + (pos[1] - 2) + '" fill="#888" font-size="10">' + rashiHindi + '</text>';

    // Planets — vertically stacked
    const planets = bhavaPlanets[bhav] || [];
    planets.forEach(function(p, i) {
      const py = pos[1] + 18 + i * 16;
      const retro = p.retro ? "R" : "";
      const color = (bhav === 1) ? '#FFD700' : '#fff';
      svg += '<text x="' + (pos[0] - 20) + '" y="' + py + '" fill="' + color + '" font-size="14" font-weight="600">' + p.hindi + retro + '</text>';
    });
  }

  // Center — Lagna info
  svg += '<text x="' + C + '" y="' + (C - 10) + '" text-anchor="middle" fill="#D4AF37" font-size="12" font-weight="700">LAGNA</text>';
  svg += '<text x="' + C + '" y="' + (C + 10) + '" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">' + NI_SIGNS_HINDI[lagnaIdx] + '</text>';
  svg += '<text x="' + C + '" y="' + (C + 26) + '" text-anchor="middle" fill="#888" font-size="10">' + lagnaRashi + '</text>';

  svg += '</svg>';
  return svg;
}

function renderNorthIndianChart(data, targetId) {
  const t = document.getElementById(targetId);
  if (!t) return;
  t.innerHTML = generateNorthIndianChart(data);
}

window.generateNorthIndianChart = generateNorthIndianChart;
window.renderNorthIndianChart = renderNorthIndianChart;
