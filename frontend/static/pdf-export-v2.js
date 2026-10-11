/**
 * Vastu One — Complete Professional PDF Report
 * Mahroon Cinematic · 25+ pages · Every section from page
 */

const PDF_SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"];
const PDF_SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"];
const PDF_PLANETS_HINDI = {"Surya":"सू","Chandra":"चं","Mangal":"मं","Budh":"बु","Guru":"गु","Shukra":"शु","Shani":"श","Rahu":"रा","Ketu":"के"};
const PDF_PLANETS_FULL = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"};

function pdfNorthChart(data) {
  const size = 480;
  const lagnaRashi = (data.lagna && data.lagna.lagna_rashi) || "Mesh";
  const lagnaIdx = PDF_SIGNS.indexOf(lagnaRashi);
  const positions = data.positions || {};
  const bp = {};
  for (let i = 1; i <= 12; i++) bp[i] = [];
  for (const [planet, pd] of Object.entries(positions)) {
    if (pd.bhav >= 1 && pd.bhav <= 12) bp[pd.bhav].push({ hindi: pd.hindi || PDF_PLANETS_HINDI[planet] || planet, retro: pd.retrograde === true });
  }
  const M = 10, C = size / 2;
  const bc = {
    1:[C,M+65], 2:[M+60,M+60], 3:[M+40,M+90], 4:[M+65,C], 5:[M+40,size-M-90], 6:[M+60,size-M-60],
    7:[C,size-M-65], 8:[size-M-60,size-M-60], 9:[size-M-40,size-M-90], 10:[size-M-65,C], 11:[size-M-40,M+90], 12:[size-M-60,M+60]
  };
  let svg = '<svg viewBox="0 0 '+size+' '+size+'" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:440px;background:#2a0810;border-radius:8px;">';
  svg += '<rect x="'+M+'" y="'+M+'" width="'+(size-2*M)+'" height="'+(size-2*M)+'" fill="none" stroke="#d4a961" stroke-width="2"/>';
  svg += '<line x1="'+M+'" y1="'+M+'" x2="'+(size-M)+'" y2="'+(size-M)+'" stroke="#d4a961" stroke-width="1.2"/>';
  svg += '<line x1="'+(size-M)+'" y1="'+M+'" x2="'+M+'" y2="'+(size-M)+'" stroke="#d4a961" stroke-width="1.2"/>';
  svg += '<polygon points="'+C+','+M+' '+(size-M)+','+C+' '+C+','+(size-M)+' '+M+','+C+'" fill="none" stroke="#d4a961" stroke-width="1.5"/>';
  for (let b = 1; b <= 12; b++) {
    const p = bc[b];
    const ri = (lagnaIdx + b - 1) % 12;
    svg += '<text x="'+(p[0]-22)+'" y="'+(p[1]-12)+'" fill="#d4a961" font-size="10" font-weight="700" opacity="0.7">'+b+'</text>';
    svg += '<text x="'+(p[0]-18)+'" y="'+(p[1]+2)+'" fill="#f5ede0" font-size="9" opacity="0.7">'+PDF_SIGNS_HINDI[ri]+'</text>';
    (bp[b] || []).forEach(function(pl, i) {
      svg += '<text x="'+(p[0]-15)+'" y="'+(p[1]+18+i*14)+'" fill="'+(b===1?'#e0b968':'#f5ede0')+'" font-size="13" font-weight="600">'+pl.hindi+(pl.retro?'R':'')+'</text>';
    });
  }
  svg += '<text x="'+C+'" y="'+(C-8)+'" text-anchor="middle" fill="#d4a961" font-size="11" font-weight="700">LAGNA</text>';
  svg += '<text x="'+C+'" y="'+(C+8)+'" text-anchor="middle" fill="#f5ede0" font-size="13" font-weight="700">'+PDF_SIGNS_HINDI[lagnaIdx]+'</text>';
  svg += '</svg>';
  return svg;
}

function pdfSouthChart(data) {
  const size = 480;
  const lagnaRashi = (data.lagna && data.lagna.lagna_rashi) || "Mesh";
  const positions = data.positions || {};
  const rp = {};
  for (let i = 0; i < 12; i++) rp[PDF_SIGNS[i]] = [];
  for (const [planet, pd] of Object.entries(positions)) {
    if (pd.rashi && rp[pd.rashi]) rp[pd.rashi].push({ hindi: pd.hindi || PDF_PLANETS_HINDI[planet] || planet, retro: pd.retrograde === true });
  }
  const grid = {"Mesh":{r:0,c:0},"Vrishabh":{r:0,c:1},"Mithun":{r:0,c:2},"Kark":{r:0,c:3},"Simha":{r:1,c:3},"Kanya":{r:2,c:3},"Tula":{r:3,c:3},"Vrishchik":{r:3,c:2},"Dhanu":{r:3,c:1},"Makar":{r:3,c:0},"Kumbh":{r:2,c:0},"Meen":{r:1,c:0}};
  const CS = size / 4;
  let svg = '<svg viewBox="0 0 '+size+' '+size+'" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:440px;background:#2a0810;border-radius:8px;">';
  for (let i = 0; i <= 4; i++) {
    svg += '<line x1="'+(i*CS)+'" y1="0" x2="'+(i*CS)+'" y2="'+size+'" stroke="#d4a961" stroke-width="'+(i===0||i===4?2:1.2)+'"/>';
    svg += '<line x1="0" y1="'+(i*CS)+'" x2="'+size+'" y2="'+(i*CS)+'" stroke="#d4a961" stroke-width="'+(i===0||i===4?2:1.2)+'"/>';
  }
  svg += '<rect x="'+CS+'" y="'+CS+'" width="'+(2*CS)+'" height="'+(2*CS)+'" fill="#2a0810"/>';
  for (const sign of PDF_SIGNS) {
    const g = grid[sign];
    const x = g.c * CS, y = g.r * CS;
    const isL = sign === lagnaRashi;
    const sh = PDF_SIGNS_HINDI[PDF_SIGNS.indexOf(sign)];
    if (isL) svg += '<rect x="'+(x+2)+'" y="'+(y+2)+'" width="'+(CS-4)+'" height="'+(CS-4)+'" fill="rgba(212,169,97,0.15)"/>';
    svg += '<text x="'+(x+6)+'" y="'+(y+16)+'" fill="#d4a961" font-size="12" font-weight="700">'+sh+'</text>';
    if (isL) svg += '<text x="'+(x+CS-6)+'" y="'+(y+16)+'" text-anchor="end" fill="#e0b968" font-size="8" font-weight="700">LAGNA</text>';
    (rp[sign] || []).forEach(function(p, i) {
      svg += '<text x="'+(x+10+(i%2)*45)+'" y="'+(y+46+Math.floor(i/2)*18)+'" fill="'+(isL?'#e0b968':'#f5ede0')+'" font-size="13" font-weight="600">'+p.hindi+(p.retro?'R':'')+'</text>';
    });
  }
  svg += '<text x="'+(size/2)+'" y="'+(size/2+8)+'" text-anchor="middle" fill="#d4a961" font-size="24" opacity="0.4">ॐ</text>';
  svg += '</svg>';
  return svg;
}

function pdfDashaTimeline(data) {
  const md = (data.dasha && data.dasha.mahadashas) || [];
  const cur = (data.dasha && data.dasha.current_mahadasha) || {};
  if (md.length === 0) return '';
  const colors = {"Surya":"#FF6B35","Chandra":"#C0C0C0","Mangal":"#DC143C","Budh":"#4CAF50","Guru":"#FFD700","Shukra":"#FF69B4","Shani":"#4A4A8A","Rahu":"#8B4513","Ketu":"#808080"};
  let tot = 0; md.forEach(function(m){ tot += (m.duration_years || 0); });
  if (tot === 0) return '';
  const W = 900, H = 140, PAD = 20;
  const pxY = (W - 2*PAD) / tot;
  let svg = '<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#2a0810;border-radius:8px;">';
  let cx = PAD;
  md.forEach(function(m) {
    const dur = m.duration_years || 0;
    const w = dur * pxY;
    const col = colors[m.planet] || '#666';
    const isC = m.planet === cur.planet;
    svg += '<rect x="'+cx+'" y="40" width="'+w+'" height="50" fill="'+col+'" opacity="'+(isC?1:0.65)+'" stroke="'+(isC?'#e0b968':'#333')+'" stroke-width="'+(isC?2:1)+'"/>';
    if (w > 30) {
      svg += '<text x="'+(cx+w/2)+'" y="62" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">'+(PDF_PLANETS_HINDI[m.planet]||'')+'</text>';
      svg += '<text x="'+(cx+w/2)+'" y="80" text-anchor="middle" fill="#fff" font-size="10">'+dur+'y</text>';
    }
    cx += w;
  });
  svg += '</svg>';
  return svg;
}

// ══════════════════════════════════════════
function buildPDFReport(data) {
  if (!data) return '<div style="padding:20px;color:#f5ede0;">Report data available nahi hai.</div>';

  const T = {
    bg: '#2a0810', bg2: '#1f060c', maroon: '#6b1420', maroonRich: '#8a1e2e',
    gold: '#d4a961', goldLight: '#e0b968', goldDeep: '#b8893b',
    ivory: '#f5ede0', ivoryMuted: 'rgba(245,237,224,0.78)', ivoryDim: 'rgba(245,237,224,0.5)',
    line: 'rgba(212,169,97,0.18)', lineGold: 'rgba(212,169,97,0.42)',
    card: 'linear-gradient(135deg, rgba(90,20,32,0.55), rgba(50,10,18,0.7))'
  };

  const basic = data.basic || {};
  const lagna = data.lagna || {};
  const positions = data.positions || {};
  const bhava = data.bhava_chalit || {};
  const dasha = data.dasha || {};
  const ashtak = data.ashtakavarga || {};
  const shadbala = data.shadbala || {};
  const yogas = data.yogas || [];
  const doshas = data.doshas || [];
  const lifePred = data.life_predictions || {};
  const lalKitab = data.lal_kitab || {};
  const lifeElab = data.life_elaborated || {};
  const timePred = data.time_prediction || {};
  const shodash = data.shodashvarga || {};
  const marriage = data.marriage_analysis || {};

  let html = '';
  let pg = 1;

  function page(content) {
    return '<div style="max-width:900px;margin:0 auto 24px auto;padding:48px 56px;background:' + T.bg + ';color:' + T.ivory + ';page-break-after:always;position:relative;font-family:Georgia,serif;">' +
      content +
      '<div style="position:absolute;bottom:20px;left:56px;right:56px;display:flex;justify-content:space-between;font-size:10px;color:' + T.ivoryDim + ';letter-spacing:0.1em;border-top:1px solid ' + T.line + ';padding-top:12px;">' +
      '<span>VASTU ONE · KUNDLI REPORT</span><span>Page ' + (pg++) + '</span></div></div>';
  }

  function hero(title, hindi, sub) {
    return '<div style="text-align:center;padding:20px 0 40px;border-bottom:1px solid ' + T.lineGold + ';margin-bottom:40px;position:relative;">' +
      '<div style="font-size:10px;letter-spacing:0.32em;color:' + T.gold + ';font-weight:600;text-transform:uppercase;margin-bottom:16px;">VASTU ONE · KUNDLI REPORT</div>' +
      '<h1 style="font-family:Georgia,serif;font-size:36px;font-weight:400;color:' + T.ivory + ';margin:0 0 8px 0;letter-spacing:-0.02em;">' + title + '</h1>' +
      (hindi ? '<div style="font-family:serif;font-size:19px;color:' + T.gold + ';margin-top:8px;">' + hindi + '</div>' : '') +
      (sub ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:12px;font-style:italic;">' + sub + '</div>' : '') +
      '</div>';
  }

  function stitle(num, title, hindi) {
    return '<div style="margin:32px 0 20px 0;padding-bottom:12px;border-bottom:1px solid ' + T.line + ';position:relative;">' +
      '<div style="font-size:10px;letter-spacing:0.3em;color:' + T.goldDeep + ';font-weight:600;text-transform:uppercase;margin-bottom:8px;">' + num + '</div>' +
      '<h2 style="font-family:Georgia,serif;font-size:22px;font-weight:500;color:' + T.ivory + ';margin:0;">' + title +
      (hindi ? ' <span style="font-size:15px;color:' + T.gold + ';font-weight:400;">' + hindi + '</span>' : '') + '</h2>' +
      '<div style="position:absolute;bottom:-1px;left:0;width:60px;height:2px;background:linear-gradient(90deg,' + T.maroonRich + ',' + T.gold + ');"></div></div>';
  }

  function card(content) {
    return '<div style="background:' + T.card + ';border:1px solid ' + T.lineGold + ';border-radius:14px;padding:22px;margin-bottom:18px;position:relative;">' +
      '<div style="position:absolute;top:0;left:22px;right:22px;height:1px;background:linear-gradient(90deg,transparent,' + T.gold + ',transparent);"></div>' + content + '</div>';
  }

  function tbl(headers, rows) {
    let h = '<table style="width:100%;border-collapse:collapse;font-size:11.5px;margin:14px 0;">';
    h += '<thead><tr>';
    headers.forEach(function(hd) {
      h += '<th style="padding:11px 12px;background:rgba(212,169,97,0.12);color:' + T.gold + ';font-size:10px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;text-align:left;border-bottom:1px solid ' + T.lineGold + ';">' + hd + '</th>';
    });
    h += '</tr></thead><tbody>';
    rows.forEach(function(r) {
      h += '<tr>';
      r.forEach(function(c, i) {
        h += '<td style="padding:9px 12px;border-bottom:1px solid ' + T.line + ';color:' + T.ivoryMuted + ';font-size:11.5px;' + (i===0?'font-weight:600;color:' + T.ivory + ';':'') + '">' + c + '</td>';
      });
      h += '</tr>';
    });
    return h + '</tbody></table>';
  }

  function list(items) {
    if (!items || !items.length) return '';
    let h = '<ul style="font-size:12.5px;color:' + T.ivoryMuted + ';line-height:1.8;padding-left:20px;margin:10px 0;">';
    items.forEach(function(i) { h += '<li>' + i + '</li>'; });
    return h + '</ul>';
  }

  // ══════════════════════════════════════════
  // 1. COVER
  // ══════════════════════════════════════════
  html += '<div style="width:100%;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:60px;background:radial-gradient(ellipse 70% 50% at 15% 0%, rgba(139,30,46,0.35) 0%, transparent 60%),radial-gradient(ellipse 60% 50% at 85% 100%, rgba(212,169,97,0.12) 0%, transparent 60%),' + T.bg + ';color:' + T.ivory + ';page-break-after:always;font-family:Georgia,serif;">' +
    '<div><div style="font-size:14px;letter-spacing:0.4em;color:' + T.gold + ';font-weight:600;margin-bottom:32px;">VASTU ONE</div>' +
    '<div style="font-size:24px;color:' + T.gold + ';margin:32px 0;">✦</div>' +
    '<h1 style="font-family:Georgia,serif;font-size:54px;font-weight:400;color:' + T.ivory + ';margin:24px 0;letter-spacing:-0.02em;line-height:1.05;">Janam Kundli</h1>' +
    '<div style="font-family:serif;font-size:26px;color:' + T.gold + ';margin:16px 0 40px;font-style:italic;">जन्म कुंडली</div>' +
    '<div style="font-size:15px;color:' + T.ivoryMuted + ';font-style:italic;margin-bottom:56px;">Complete Vedic Astrology Report</div>' +
    '<div style="display:inline-block;text-align:left;background:rgba(90,20,32,0.5);border:1px solid ' + T.lineGold + ';border-radius:14px;padding:28px 44px;">' +
    '<div style="font-size:14px;color:' + T.ivoryMuted + ';margin-bottom:12px;"><strong style="display:inline-block;width:180px;color:' + T.gold + ';">Name:</strong> ' + (basic.name || '—') + '</div>' +
    '<div style="font-size:14px;color:' + T.ivoryMuted + ';margin-bottom:12px;"><strong style="display:inline-block;width:180px;color:' + T.gold + ';">DOB:</strong> ' + (basic.dob || '—') + '</div>' +
    '<div style="font-size:14px;color:' + T.ivoryMuted + ';margin-bottom:12px;"><strong style="display:inline-block;width:180px;color:' + T.gold + ';">TOB:</strong> ' + (basic.tob || '—') + '</div>' +
    '<div style="font-size:14px;color:' + T.ivoryMuted + ';margin-bottom:12px;"><strong style="display:inline-block;width:180px;color:' + T.gold + ';">Place:</strong> ' + (basic.place || basic.pob || '—') + '</div>' +
    '<div style="font-size:14px;color:' + T.ivoryMuted + ';"><strong style="display:inline-block;width:180px;color:' + T.gold + ';">Lagna:</strong> ' + (lagna.lagna_hindi || '') + ' (' + (lagna.lagna_rashi || '') + ')</div>' +
    '</div><div style="font-size:12px;color:' + T.ivoryDim + ';margin-top:56px;">Generated on ' + new Date().toLocaleString('en-IN') + '</div></div></div>';

  // ══════════════════════════════════════════
  // 2. BIRTH CHARTS
  // ══════════════════════════════════════════
  html += page(hero('Birth Charts', 'जन्म कुंडली चक्र', 'North & South Indian formats') +
    '<h3 style="font-size:13px;color:' + T.gold + ';letter-spacing:0.18em;text-transform:uppercase;margin:20px 0 14px;text-align:center;">North Indian Chart</h3>' +
    '<div style="text-align:center;margin-bottom:24px;">' + pdfNorthChart(data) + '</div>' +
    '<h3 style="font-size:13px;color:' + T.gold + ';letter-spacing:0.18em;text-transform:uppercase;margin:20px 0 14px;text-align:center;">South Indian Chart</h3>' +
    '<div style="text-align:center;">' + pdfSouthChart(data) + '</div>');

  // ══════════════════════════════════════════
  // 3. LAGNA DETAILS
  // ══════════════════════════════════════════
  html += page(hero('Lagna Details', 'लग्न विवरण', 'Birth chart foundation') +
    tbl(['Parameter', 'Value'], [
      ['Lagna Rashi', (lagna.lagna_hindi || '') + ' (' + (lagna.lagna_rashi || '') + ')'],
      ['Lagna Lord', lagna.lagna_lord || '—'],
      ['Lagna Nakshatra', lagna.lagna_nakshatra || '—'],
      ['Lagna Degree', lagna.lagna_degree ? lagna.lagna_degree.toFixed(2) + '°' : '—'],
      ['Lagna Element', lagna.lagna_element || '—'],
      ['Tithi', basic.tithi || '—'],
      ['Paksha', basic.paksha || '—']
    ]));

  // ══════════════════════════════════════════
  // 4. PLANETARY POSITIONS
  // ══════════════════════════════════════════
  const planetOrder = ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani","Rahu","Ketu"];
  let pRows = [];
  planetOrder.forEach(function(p) {
    const pd = positions[p] || {};
    if (!pd.planet) return;
    pRows.push([
      '<strong>' + (pd.hindi || p) + '</strong>' + (pd.retrograde ? ' <span style="color:#f0a0a0;">R</span>' : ''),
      pd.rashi_hindi || pd.rashi || '—',
      String(pd.bhav || '—'),
      pd.degree ? pd.degree.toFixed(2) + '°' : '—',
      pd.nakshatra || '—',
      String(pd.pada || '—')
    ]);
  });
  html += page(hero('Planetary Positions', 'ग्रह स्थिति', '9 planets with exact degrees') + tbl(['Planet','Rashi','Bhava','Degree','Nakshatra','Pada'], pRows));

  // ══════════════════════════════════════════
  // 5. BHAVA CHALIT
  // ══════════════════════════════════════════
  if (Object.keys(bhava).length > 0) {
    let bRows = [];
    for (let i = 1; i <= 12; i++) {
      const b = bhava[i] || bhava[String(i)];
      if (!b) continue;
      bRows.push([String(b.bhav), b.hindi || '—', b.meaning || '—', b.cusp_rashi_hindi || b.cusp_rashi || '—', b.cusp_degree ? b.cusp_degree.toFixed(2) + '°' : '—']);
    }
    html += page(hero('Bhava Chalit', 'भाव चलित', 'House cusps') + tbl(['Bhava','Name','Meaning','Cusp Rashi','Degree'], bRows));
  }

  // ══════════════════════════════════════════
  // 6. SHODASHAVARGA
  // ══════════════════════════════════════════
  if (Object.keys(shodash).length > 0) {
    let vRows = [];
    ["D-1","D-2","D-3","D-4","D-7","D-9","D-10","D-12","D-16","D-20","D-24","D-27","D-30","D-40","D-45","D-60"].forEach(function(v) {
      const vd = shodash[v]; if (!vd) return;
      let pl = vd.positions ? Object.keys(vd.positions).map(function(p){return PDF_PLANETS_HINDI[p]||p;}).join(' ') : '';
      vRows.push([v, vd.meaning || vd.name || '—', vd.lagna ? (PDF_SIGNS_HINDI[PDF_SIGNS.indexOf(vd.lagna)] || vd.lagna) : '—', pl]);
    });
    html += page(hero('Shodashvarga', 'षोडशवर्ग', '16 divisional charts') + tbl(['Varga','Meaning','Lagna','Planets'], vRows));
  }

  // ══════════════════════════════════════════
  // 7. DASHA TIMELINE
  // ══════════════════════════════════════════
  if (dasha.mahadashas && dasha.mahadashas.length > 0) {
    let content = hero('Vimshottari Dasha', 'विंशोत्तरी दशा', '120-year timeline');
    content += '<div style="margin-bottom:24px;">' + pdfDashaTimeline(data) + '</div>';
    let dRows = [];
    const cur = dasha.current_mahadasha || {};
    dasha.mahadashas.forEach(function(m) {
      const isC = m.planet === cur.planet;
      dRows.push([
        '<strong>' + (m.hindi || '') + '</strong> (' + m.planet + ')' + (isC ? ' <span style="color:#e0b968;">← NOW</span>' : ''),
        m.start_date || '—', m.end_date || '—',
        (m.start_age ? m.start_age.toFixed(0) : '—') + '-' + (m.end_age ? m.end_age.toFixed(0) : '—'),
        (m.duration_years || '—') + 'y'
      ]);
    });
    content += tbl(['Planet','Start','End','Age','Duration'], dRows);
    html += page(content);
  }

  // ══════════════════════════════════════════
  // 8. ASHTAKAVARGA
  // ══════════════════════════════════════════
  if (ashtak.bhinnashtakavarga) {
    let content = hero('Ashtakavarga', 'अष्टकवर्ग', 'Planetary strength per rashi');
    let hdrs = ['Planet']; PDF_SIGNS_HINDI.forEach(function(s){hdrs.push(s);}); hdrs.push('Total');
    let rows = [];
    ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"].forEach(function(p) {
      const pD = ashtak.bhinnashtakavarga[p] || {};
      const sc = pD.scores || [];
      let r = ['<strong>' + PDF_PLANETS_FULL[p] + '</strong>'];
      for (let i = 0; i < 12; i++) r.push(String(sc[i] !== undefined ? sc[i] : 0));
      r.push('<strong style="color:#e0b968;">' + (pD.total || 0) + '</strong>');
      rows.push(r);
    });
    content += tbl(hdrs, rows);
    html += page(content);
  }

  // ══════════════════════════════════════════
  // 9. SHADBALA
  // ══════════════════════════════════════════
  if (Object.keys(shadbala).length > 0) {
    let content = hero('Shadbala', 'षड्बल', 'Six-fold planetary strength');
    let rows = [];
    Object.entries(shadbala).forEach(function(e) {
      const d = e[1] || {};
      const tot = d.total || d.total_bala || 0;
      let st = 'Average';
      if (tot > 400) st = 'Very Strong'; else if (tot > 350) st = 'Strong'; else if (tot < 250) st = 'Weak';
      rows.push([PDF_PLANETS_FULL[e[0]] || e[0], typeof tot === 'number' ? tot.toFixed(1) : String(tot), st]);
    });
    content += tbl(['Planet','Total Bala','Status'], rows);
    html += page(content);
  }

  // ══════════════════════════════════════════
  // 10-21: TIME PREDICTION (7 sections)
  // ══════════════════════════════════════════
  if (timePred.past_prediction) {
    const pp = timePred.past_prediction;
    let content = hero('Past Analysis', 'भूतकाल विश्लेषण', 'Last 20-30 years');
    if (pp.summary) content += '<p style="font-size:12.5px;line-height:1.7;color:' + T.ivoryMuted + ';margin-bottom:18px;">' + pp.summary + '</p>';
    if (pp.dasha_periods) pp.dasha_periods.forEach(function(d) {
      content += card('<div style="font-size:13px;font-weight:600;color:' + T.ivory + ';margin-bottom:6px;">' + (d.hindi || '') + ' (' + d.planet + ') — ' + (d.period || '') + '</div>' +
        (d.what_happened ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';line-height:1.6;margin-bottom:4px;"><strong style="color:' + T.gold + ';">Kya hua:</strong> ' + d.what_happened + '</div>' : '') +
        (d.why_happened ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';line-height:1.6;"><strong style="color:' + T.gold + ';">Kyun:</strong> ' + d.why_happened + '</div>' : ''));
    });
    if (pp.lessons_learned) content += stitle('', 'Lessons Learned') + list(pp.lessons_learned);
    html += page(content);
  }

  if (timePred.present_situation) {
    const ps = timePred.present_situation;
    let content = hero('Present Situation', 'वर्तमान स्थिति', 'Current dasha');
    if (ps.summary) content += '<p style="font-size:12.5px;line-height:1.7;color:' + T.ivoryMuted + ';margin-bottom:18px;">' + ps.summary + '</p>';
    if (ps.current_mahadasha) content += card('<div style="font-size:10px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin-bottom:6px;">Current Mahadasha</div><div style="font-size:17px;color:' + T.ivory + ';font-weight:600;">' + (ps.current_mahadasha.planet || '') + '</div><div style="font-size:12px;color:' + T.ivoryDim + ';margin-top:4px;">' + (ps.current_mahadasha.period || '') + '</div>');
    if (ps.current_antardasha) content += card('<div style="font-size:10px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin-bottom:6px;">Current Antardasha</div><div style="font-size:17px;color:' + T.ivory + ';font-weight:600;">' + (ps.current_antardasha.planet || '') + '</div>');
    if (ps.why_things_are_blocked) content += stitle('', 'क्यों रुका है') + list(ps.why_things_are_blocked);
    if (ps.immediate_actions) content += stitle('', 'तुरंत करें') + list(ps.immediate_actions);
    html += page(content);
  }

  if (timePred.future_prediction) {
    const fp = timePred.future_prediction;
    let content = hero('Future Prediction', 'भविष्यफल', 'Next 5-10 years');
    if (fp.summary) content += '<p style="font-size:12.5px;line-height:1.7;color:' + T.ivoryMuted + ';margin-bottom:18px;">' + fp.summary + '</p>';
    if (fp.next_mahadashas) fp.next_mahadashas.forEach(function(m) {
      content += card('<div style="font-size:13px;font-weight:600;color:' + T.ivory + ';margin-bottom:6px;">' + (m.hindi || '') + ' (' + m.planet + ') — ' + (m.period || '') + '</div>' +
        (m.what_will_happen ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';line-height:1.6;">' + m.what_will_happen + '</div>' : '') +
        (m.opportunities ? '<div style="font-size:12px;color:#7ee0a0;line-height:1.6;">✓ ' + m.opportunities + '</div>' : '') +
        (m.warnings ? '<div style="font-size:12px;color:#f0a0a0;line-height:1.6;">⚠ ' + m.warnings + '</div>' : ''));
    });
    if (fp.next_5_years) content += stitle('', 'Next 5 Years') + tbl(['Year','Prediction','Action'], fp.next_5_years.map(function(y){return [y.year||'', y.prediction||'', y.action||''];}));
    html += page(content);
  }

  if (timePred.karmic_analysis) {
    const ka = timePred.karmic_analysis;
    let content = hero('Karmic Analysis', 'कार्मिक विश्लेषण', 'Past-life debts');
    if (ka.purva_punya) content += card('<div style="font-size:10px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin-bottom:6px;">Purva Punya · 5th House</div><div style="font-size:12.5px;color:' + T.ivoryMuted + ';line-height:1.7;">' + ka.purva_punya + '</div>');
    if (ka.bhagya) content += card('<div style="font-size:10px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin-bottom:6px;">Bhagya · 9th House</div><div style="font-size:12.5px;color:' + T.ivoryMuted + ';line-height:1.7;">' + ka.bhagya + '</div>');
    if (ka.karmic_debts) content += stitle('', 'Karmic Debts') + list(ka.karmic_debts);
    if (ka.how_to_clear) content += stitle('', 'How to Clear') + list(ka.how_to_clear);
    html += page(content);
  }

  if (timePred.blocked_areas && timePred.blocked_areas.length > 0) {
    let content = hero('Blocked Areas', 'अवरोध क्षेत्र', 'Planet-wise blocks');
    timePred.blocked_areas.forEach(function(b) {
      content += card('<div style="font-size:13px;font-weight:600;color:#f0a0a0;margin-bottom:6px;">' + (b.hindi || '') + ' (' + b.planet + ') — भाव ' + b.bhav + '</div>' +
        (b.area ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';">Area: ' + b.area + '</div>' : '') +
        (b.why_blocked ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';">Why: ' + b.why_blocked + '</div>' : '') +
        (b.duration ? '<div style="font-size:12px;color:#f0a0a0;">Duration: ' + b.duration + '</div>' : '') +
        (b.remedy ? '<div style="font-size:12px;color:#7ee0a0;">उपाय: ' + b.remedy + '</div>' : ''));
    });
    html += page(content);
  }

  if (timePred.timing_predictions) {
    const t = timePred.timing_predictions;
    let rows = [];
    [['💼 Career', t.career],['💑 Marriage', t.marriage],['💰 Wealth', t.wealth],['👶 Children', t.children],['🏠 Property', t.property],['🏥 Health', t.health],['🕉️ Spiritual', t.spiritual]].forEach(function(i){if(i[1])rows.push([i[0], i[1]]);});
    html += page(hero('Timing Predictions', 'समय-सूचक भविष्यवाणी', 'When will what happen') + tbl(['Area','Prediction'], rows));
  }

  // ══════════════════════════════════════════
  // LIFE PREDICTIONS (12 areas)
  // ══════════════════════════════════════════
  if (Object.keys(lifePred).length > 0) {
    let content = hero('Life Predictions', 'जीवन भविष्यवाणी', '12 areas of life');
    [['education','📚 शिक्षा · Education'],['career','💼 करियर · Career'],['business','📈 व्यापार · Business'],['personal_life','👤 व्यक्तिगत जीवन'],['marriage','💑 विवाह · Marriage'],['wealth','💰 धन · Wealth'],['health','🏥 स्वास्थ्य · Health'],['children','👶 संतान · Children'],['property','🏠 संपत्ति · Property'],['foreign_travel','🌍 विदेश यात्रा'],['spiritual','🕉️ आध्यात्मिक'],['family','👨‍👩‍👧 परिवार · Family']].forEach(function(a) {
      const val = lifePred[a[0]]; if (!val) return;
      let text = (typeof val === 'string') ? val : (val.summary || val.prediction || JSON.stringify(val).substring(0,300));
      content += card('<div style="font-size:11px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin-bottom:6px;">' + a[1] + '</div><div style="font-size:12.5px;color:' + T.ivoryMuted + ';line-height:1.7;">' + text + '</div>');
    });
    html += page(content);
  }

  // ══════════════════════════════════════════
  // LIFE ELABORATED
  // ══════════════════════════════════════════
  if (Object.keys(lifeElab).length > 0) {
    let content = hero('Deep Life Analysis', 'विस्तृत जीवन विश्लेषण', 'Detailed elaboration');
    Object.entries(lifeElab).forEach(function(e) {
      const key = e[0].replace("elaborated_","").replace(/_/g," ").toUpperCase();
      const val = e[1]; if (!val) return;
      let text = (typeof val === 'string') ? val : (val.summary || val.detail || JSON.stringify(val).substring(0,400));
      content += card('<div style="font-size:11px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin-bottom:6px;">' + key + '</div><div style="font-size:12.5px;color:' + T.ivoryMuted + ';line-height:1.7;">' + text + '</div>');
    });
    html += page(content);
  }

  // ══════════════════════════════════════════
  // MARRIAGE ANALYSIS (full)
  // ══════════════════════════════════════════
  if (marriage && Object.keys(marriage).length > 0) {
    let content = hero('Marriage Analysis', 'विवाह विश्लेषण', 'Complete marriage guidance');

    if (marriage.marriage_yoga) {
      const my = marriage.marriage_yoga;
      content += stitle('01', 'Vivah Yoga', 'विवाह योग');
      content += card('<div style="font-size:12.5px;color:' + T.ivoryMuted + ';line-height:1.7;">' + (my.summary || '') + '</div>' +
        (my.strength ? '<div style="font-size:12px;color:' + T.ivoryDim + ';margin-top:8px;"><strong style="color:' + T.gold + ';">Strength:</strong> ' + my.strength + '</div>' : '') +
        (my.love_or_arranged ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:4px;">' + my.love_or_arranged + '</div>' : ''));
    }

    if (marriage.spouse_analysis) {
      const sa = marriage.spouse_analysis;
      content += stitle('02', 'Spouse Analysis', 'जीवनसाथी विश्लेषण');
      content += card('<div style="font-size:12.5px;color:' + T.ivoryMuted + ';line-height:1.7;">' + (sa.summary || '') + '</div>' +
        (sa.spouse_nature ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:8px;"><strong style="color:' + T.gold + ';">Nature:</strong> ' + sa.spouse_nature + '</div>' : '') +
        (sa.spouse_profession ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:4px;"><strong style="color:' + T.gold + ';">Profession:</strong> ' + sa.spouse_profession + '</div>' : '') +
        (sa.spouse_appearance ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:4px;"><strong style="color:' + T.gold + ';">Appearance:</strong> ' + sa.spouse_appearance + '</div>' : '') +
        (sa.spouse_from_direction ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:4px;"><strong style="color:' + T.gold + ';">Direction:</strong> ' + sa.spouse_from_direction + '</div>' : ''));
    }

    if (marriage.married_life) {
      const ml = marriage.married_life;
      content += stitle('03', 'Married Life', 'विवाहित जीवन');
      content += card('<div style="font-size:14px;color:' + T.ivory + ';font-weight:600;">' + (ml.summary || '') + '</div>' +
        (ml.early_years ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:8px;line-height:1.6;"><strong style="color:' + T.gold + ';">Early:</strong> ' + ml.early_years + '</div>' : '') +
        (ml.mid_years ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:4px;line-height:1.6;"><strong style="color:' + T.gold + ';">Mid:</strong> ' + ml.mid_years + '</div>' : '') +
        (ml.later_years ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:4px;line-height:1.6;"><strong style="color:' + T.gold + ';">Later:</strong> ' + ml.later_years + '</div>' : '') +
        (ml.challenges && ml.challenges.length ? '<div style="font-size:12px;color:#f0a0a0;margin-top:8px;"><strong>⚠ चुनौतियां:</strong>' + list(ml.challenges) + '</div>' : '') +
        (ml.strengths && ml.strengths.length ? '<div style="font-size:12px;color:#7ee0a0;margin-top:8px;"><strong>✓ शक्तियां:</strong>' + list(ml.strengths) + '</div>' : ''));
    }

    if (marriage.marital_harmony) {
      const mh = marriage.marital_harmony;
      content += stitle('04', 'Marital Harmony', 'दांपत्य सुख');
      content += card('<div style="font-size:12.5px;color:' + T.ivoryMuted + ';">' + (mh.summary || '') + '</div>' +
        (mh.relationship_rules && mh.relationship_rules.length ? '<div style="margin-top:10px;"><strong style="color:' + T.gold + ';font-size:12px;">रिश्ते के नियम:</strong>' + list(mh.relationship_rules) + '</div>' : '') +
        (mh.avoid && mh.avoid.length ? '<div style="margin-top:10px;"><strong style="color:#f0a0a0;font-size:12px;">बचें:</strong>' + list(mh.avoid) + '</div>' : ''));
    }

    if (marriage.mangal_dosha) {
      const md = marriage.mangal_dosha;
      content += stitle('05', 'Mangal Dosha', 'मंगल दोष');
      content += card('<div style="font-size:14px;color:' + T.ivory + ';font-weight:600;">' + (md.summary || '') + '</div>' +
        (md.effects && md.effects.length ? '<div style="margin-top:8px;"><strong style="color:' + T.gold + ';font-size:12px;">प्रभाव:</strong>' + list(md.effects) + '</div>' : '') +
        (md.remedies && md.remedies.length ? '<div style="margin-top:8px;"><strong style="color:#7ee0a0;font-size:12px;">उपाय:</strong>' + list(md.remedies) + '</div>' : ''));
    }

    if (marriage.marriage_timing) {
      const mt = marriage.marriage_timing;
      content += stitle('06', 'Marriage Timing', 'विवाह का समय');
      content += card('<div style="font-size:12.5px;color:' + T.ivoryMuted + ';">' + (mt.summary || '') + '</div>' +
        (mt.best_age ? '<div style="font-size:12.5px;color:' + T.ivory + ';margin-top:8px;"><strong style="color:' + T.gold + ';">Best Age:</strong> ' + mt.best_age + '</div>' : '') +
        (mt.immediate_action ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:6px;font-style:italic;">' + mt.immediate_action + '</div>' : ''));
    }

    if (marriage.matching_guidance) {
      const mg = marriage.matching_guidance;
      content += stitle('07', 'Matching Guidance', 'कुंडली मिलान');
      content += card('<div style="font-size:12.5px;color:' + T.ivoryMuted + ';">' + (mg.summary || '') + '</div>' +
        (mg.compatible_rashis && mg.compatible_rashis.length ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:8px;"><strong style="color:' + T.gold + ';">Compatible Rashis:</strong> ' + mg.compatible_rashis.join(', ') + '</div>' : '') +
        (mg.recommended_nakshatras ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';margin-top:4px;"><strong style="color:' + T.gold + ';">Nakshatras:</strong> ' + mg.recommended_nakshatras + '</div>' : ''));
    }

    if (marriage.practical_rules) {
      const pr = marriage.practical_rules;
      content += stitle('08', 'Practical Rules', 'व्यावहारिक नियम');
      if (pr.before_marriage && pr.before_marriage.length) content += '<div style="margin-bottom:10px;"><strong style="color:' + T.gold + ';font-size:12px;">विवाह से पहले:</strong>' + list(pr.before_marriage) + '</div>';
      if (pr.after_marriage && pr.after_marriage.length) content += '<div style="margin-bottom:10px;"><strong style="color:' + T.gold + ';font-size:12px;">विवाह के बाद:</strong>' + list(pr.after_marriage) + '</div>';
      if (pr.spiritual_practices && pr.spiritual_practices.length) content += '<div><strong style="color:' + T.gold + ';font-size:12px;">आध्यात्मिक अभ्यास:</strong>' + list(pr.spiritual_practices) + '</div>';
    }

    html += page(content);
  }

  // ══════════════════════════════════════════
  // YOGAS
  // ══════════════════════════════════════════
  if (yogas.length > 0) {
    let content = hero('Yogas', 'शुभ योग', yogas.length + ' auspicious combinations');
    yogas.forEach(function(y, i) {
      content += card('<div style="font-size:13px;font-weight:600;color:' + T.gold + ';margin-bottom:6px;">' + (i+1) + '. ' + (y.name || y.yoga || 'Yoga') + '</div>' +
        (y.description || y.desc ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';line-height:1.6;">' + (y.description || y.desc) + '</div>' : ''));
    });
    html += page(content);
  }

  // ══════════════════════════════════════════
  // DOSHAS
  // ══════════════════════════════════════════
  if (doshas.length > 0) {
    let content = hero('Doshas', 'दोष', doshas.length + ' challenging combinations');
    doshas.forEach(function(d, i) {
      content += card('<div style="font-size:13px;font-weight:600;color:#f0a0a0;margin-bottom:6px;">' + (i+1) + '. ' + (d.name || d.dosha || 'Dosha') + '</div>' +
        (d.description || d.desc ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';line-height:1.6;margin-bottom:6px;">' + (d.description || d.desc) + '</div>' : '') +
        (d.remedy ? '<div style="font-size:12px;color:#7ee0a0;line-height:1.6;"><strong>उपाय:</strong> ' + d.remedy + '</div>' : ''));
    });
    html += page(content);
  }

  // ══════════════════════════════════════════
  // LAL KITAB
  // ══════════════════════════════════════════
  if (lalKitab.findings && lalKitab.findings.length > 0) {
    let content = hero('Lal Kitab', 'लाल किताब विश्लेषण', 'Unique low-cost remedies');
    lalKitab.findings.forEach(function(f, i) {
      content += card('<div style="font-size:13px;font-weight:600;color:' + T.gold + ';margin-bottom:6px;">' + (i+1) + '. ' + (f.title || f.name || '') + '</div>' +
        (f.description ? '<div style="font-size:12px;color:' + T.ivoryMuted + ';line-height:1.6;margin-bottom:6px;">' + f.description + '</div>' : '') +
        (f.remedy ? '<div style="font-size:12px;color:#7ee0a0;line-height:1.6;"><strong>उपाय:</strong> ' + f.remedy + '</div>' : ''));
    });
    html += page(content);
  }

  // ══════════════════════════════════════════
  // REMEDIES
  // ══════════════════════════════════════════
  html += page(hero('Remedies', 'उपाय', 'Personalized remedies') +
    (doshas.length > 0 ? '<h3 style="font-size:13px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin:20px 0 10px;">Dosha Remedies</h3>' + card(doshas.map(function(d){
      return '<div style="margin-bottom:10px;"><div style="font-size:12.5px;color:' + T.ivory + ';font-weight:600;">' + (d.name || d.dosha) + '</div>' + (d.remedy ? '<div style="font-size:12px;color:#7ee0a0;margin-top:4px;">' + d.remedy + '</div>' : '') + '</div>';
    }).join('')) : '') +
    (timePred.karmic_analysis && timePred.karmic_analysis.how_to_clear ? '<h3 style="font-size:13px;color:' + T.gold + ';letter-spacing:0.16em;text-transform:uppercase;margin:20px 0 10px;">Karmic Remedies</h3>' + card(list(timePred.karmic_analysis.how_to_clear)) : ''));

  // ══════════════════════════════════════════
  // FINAL FOOTER
  // ══════════════════════════════════════════
  html += '<div style="padding:60px 40px;text-align:center;background:' + T.bg2 + ';border-top:1px solid ' + T.line + ';color:' + T.ivory + ';page-break-before:always;font-family:Georgia,serif;">' +
    '<div style="font-size:28px;color:' + T.gold + ';margin-bottom:24px;">✦</div>' +
    '<div style="font-size:20px;letter-spacing:0.32em;color:' + T.gold + ';font-weight:600;margin-bottom:16px;">VASTU ONE</div>' +
    '<div style="font-size:14px;color:' + T.ivoryMuted + ';font-style:italic;margin-bottom:40px;">Every finding has a source. Every decision, a reason.</div>' +
    '<div style="font-size:11px;color:' + T.ivoryDim + ';letter-spacing:0.22em;text-transform:uppercase;">Made with care in India · © ' + new Date().getFullYear() + ' Vastu One</div></div>';

  return html;
}

function exportToPDF(data) {
  if (!data) { alert('Report data available nahi hai.'); return; }
  const content = buildPDFReport(data);
  const w = window.open('', '_blank');
  if (!w) { alert('Popup blocked. Please allow popups.'); return; }

  const styles = `
    @page { size: A4; margin: 10mm; }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: #1f060c; color: #f5ede0; font-family: Georgia, serif; }
    body { padding: 20px; }
    .no-print-bar { position: fixed; top: 20px; right: 20px; z-index: 9999; display: flex; gap: 10px; background: #2a0810; padding: 10px; border-radius: 12px; border: 1px solid rgba(212,169,97,0.4); box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
    .no-print-bar button { border: none; padding: 12px 24px; border-radius: 8px; font-size: 13px; font-weight: 700; cursor: pointer; font-family: -apple-system, sans-serif; letter-spacing: 0.08em; text-transform: uppercase; }
    .btn-print { background: linear-gradient(135deg, #e0b968, #d4a961, #b8893b); color: #2a0810; }
    .btn-close { background: #3d0a12; color: #f5ede0; border: 1px solid rgba(212,169,97,0.4); }
    @media print { body { padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; } .no-print-bar { display: none !important; } }
  `;

  w.document.write('<!DOCTYPE html><html><head><title>Kundli Report — Vastu One</title><style>' + styles + '</style></head><body>');
  w.document.write('<div class="no-print-bar">');
  w.document.write('<button class="btn-print" onclick="window.print()">🖨️ Print / Save as PDF</button>');
  w.document.write('<button class="btn-close" onclick="window.close()">✕ Close</button>');
  w.document.write('</div>');
  w.document.write(content);
  w.document.write('</body></html>');
  w.document.close();
  setTimeout(function() { w.focus(); }, 300);
}

function renderPDFExportButton(data, targetId) {
  const t = document.getElementById(targetId);
  if (!t) return;
  t.innerHTML = '<div style="padding:24px;text-align:center;">' +
    '<button onclick="window.vastuOneLastData && exportToPDF(window.vastuOneLastData)" style="background:linear-gradient(135deg,#e0b968,#d4a961,#b8893b);color:#2a0810;border:none;padding:20px 40px;border-radius:12px;font-size:14px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;cursor:pointer;box-shadow:0 20px 40px -12px rgba(212,169,97,0.4);font-family:Inter,sans-serif;">📄 Download PDF Report</button>' +
    '<div style="margin-top:16px;font-size:12px;color:rgba(245,237,224,0.7);font-style:italic;">Complete kundli report — 50+ pages · All charts · 4 Phases · 15+ engines</div></div>';
}

window.buildPDFReport = buildPDFReport;
window.exportToPDF = exportToPDF;
window.renderPDFExportButton = renderPDFExportButton;
