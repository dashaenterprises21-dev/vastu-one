// VASTU ONE - Advanced Analysis JS

const API = '';

const TABS = {
    entrance: renderEntranceTab,
    ayadi: renderAyadiTab,
    plot: renderPlotTab,
    remedies: renderRemediesTab,
    pooja: renderPoojaTab
};

function showTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById('tab-content').innerHTML = TABS[tabName]();
}

// ═══ ENTRANCE ═══
function renderEntranceTab() {
    return `
    <div class="card">
        <h2>🚪 32 Entrance Padas Audit</h2>
        <p>Apne ghar ka main entrance check karein</p>
        <div class="form-group">
            <label>Direction (दिशा)</label>
            <select id="ent-direction">
                <option value="East">East (पूर्व) - E1 to E8</option>
                <option value="South">South (दक्षिण) - S1 to S8</option>
                <option value="West">West (पश्चिम) - W1 to W8</option>
                <option value="North">North (उत्तर) - N1 to N8</option>
            </select>
        </div>
        <div class="form-group">
            <label>Pada (1-8)</label>
            <input type="number" id="ent-pada" min="1" max="8" value="3">
        </div>
        <div class="form-group">
            <label>Exact Degree (optional)</label>
            <input type="number" id="ent-degree" step="0.1" placeholder="95.5">
        </div>
        <button class="btn-primary" onclick="auditEntrance()">Audit Entrance</button>
        <div id="ent-result"></div>
    </div>

    <div class="card">
        <h2>📋 32 Padas — Full Reference</h2>
        <p>Har pada ka code, direction, degree range, aur verdict</p>

        <h3>🌅 EAST (पूर्व) — 67.5° to 157.5°</h3>
        <div class="pada-grid">
            <div class="pada-card avoid">
                <div class="pada-code">E1</div>
                <div class="pada-name">Shikhi (शिखी)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 67.5° - 78.75°</div>
                <div class="pada-verdict verdict-bad">❌ Loss of wealth</div>
            </div>
            <div class="pada-card medium">
                <div class="pada-code">E2</div>
                <div class="pada-name">Parjanya (पर्जन्य)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 78.75° - 90°</div>
                <div class="pada-verdict verdict-med">⚠️ Health issues</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">E3</div>
                <div class="pada-name">Jayanta (जयन्त)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 90° - 101.25°</div>
                <div class="pada-verdict verdict-best">✅ BEST - Victory</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">E4</div>
                <div class="pada-name">Indra (इन्द्र)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 101.25° - 112.5°</div>
                <div class="pada-verdict verdict-best">✅ Power, wealth</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">E5</div>
                <div class="pada-name">Surya (सूर्य)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 112.5° - 123.75°</div>
                <div class="pada-verdict verdict-best">✅ Fame, vitality</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">E6</div>
                <div class="pada-name">Satya (सत्य)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 123.75° - 135°</div>
                <div class="pada-verdict verdict-best">✅ Truth, success</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">E7</div>
                <div class="pada-name">Bhusha (भूष)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 135° - 146.25°</div>
                <div class="pada-verdict verdict-bad">❌ Financial loss</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">E8</div>
                <div class="pada-name">Akasha (आकाश)</div>
                <div class="pada-direction">📍 East</div>
                <div class="pada-degree">🧭 146.25° - 157.5°</div>
                <div class="pada-verdict verdict-bad">❌ Loss of children</div>
            </div>
        </div>

        <h3>🌞 SOUTH (दक्षिण) — 157.5° to 247.5°</h3>
        <div class="pada-grid">
            <div class="pada-card avoid">
                <div class="pada-code">S1</div>
                <div class="pada-name">Anila (अनिल)</div>
                <div class="pada-direction">�� South</div>
                <div class="pada-degree">🧭 157.5° - 168.75°</div>
                <div class="pada-verdict verdict-bad">❌ Fear, quarrel</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">S2</div>
                <div class="pada-name">Pusha (पूषा)</div>
                <div class="pada-direction">📍 South</div>
                <div class="pada-degree">🧭 168.75° - 180°</div>
                <div class="pada-verdict verdict-best">✅ BEST - Nourishment</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">S3</div>
                <div class="pada-name">Vitatha (वितथ)</div>
                <div class="pada-direction">📍 South</div>
                <div class="pada-degree">🧭 180° - 191.25°</div>
                <div class="pada-verdict verdict-bad">❌ Obstacles</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">S4</div>
                <div class="pada-name">Grihakshata (गृहक्षत)</div>
                <div class="pada-direction">📍 South</div>
                <div class="pada-degree">🧭 191.25° - 202.5°</div>
                <div class="pada-verdict verdict-best">✅ BEST - Wealth</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">S5</div>
                <div class="pada-name">Yama (यम)</div>
                <div class="pada-direction">📍 South</div>
                <div class="pada-degree">🧭 202.5° - 213.75°</div>
                <div class="pada-verdict verdict-bad">❌ Worst - Death</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">S6</div>
                <div class="pada-name">Gandharva (गन्धर्व)</div>
                <div class="pada-direction">📍 South</div>
                <div class="pada-degree">🧭 213.75° - 225°</div>
                <div class="pada-verdict verdict-best">✅ Luxury, comfort</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">S7</div>
                <div class="pada-name">Bhrungaraja (भृंगराज)</div>
                <div class="pada-direction">📍 South</div>
                <div class="pada-degree">🧭 225° - 236.25°</div>
                <div class="pada-verdict verdict-bad">❌ Fear, anxiety</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">S8</div>
                <div class="pada-name">Mriga (मृग)</div>
                <div class="pada-direction">📍 South</div>
                <div class="pada-degree">🧭 236.25° - 247.5°</div>
                <div class="pada-verdict verdict-bad">❌ Accidents</div>
            </div>
        </div>

        <h3>🌇 WEST (पश्चिम) — 247.5° to 337.5°</h3>
        <div class="pada-grid">
            <div class="pada-card avoid">
                <div class="pada-code">W1</div>
                <div class="pada-name">Pitara (पितर)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 247.5° - 258.75°</div>
                <div class="pada-verdict verdict-bad">❌ Ancestral issues</div>
            </div>
            <div class="pada-card medium">
                <div class="pada-code">W2</div>
                <div class="pada-name">Dauvarika (दौवारिक)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 258.75° - 270°</div>
                <div class="pada-verdict verdict-med">⚠️ Medium</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">W3</div>
                <div class="pada-name">Sugriva (सुग्रीव)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 270° - 281.25°</div>
                <div class="pada-verdict verdict-best">✅ BEST - Money</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">W4</div>
                <div class="pada-name">Pushpadanta (पुष्पदन्त)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 281.25° - 292.5°</div>
                <div class="pada-verdict verdict-best">✅ Finance, income</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">W5</div>
                <div class="pada-name">Varuna (वरुण)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 292.5° - 303.75°</div>
                <div class="pada-verdict verdict-best">✅ Rain, purification</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">W6</div>
                <div class="pada-name">Asura (असुर)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 303.75° - 315°</div>
                <div class="pada-verdict verdict-bad">❌ Negativity</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">W7</div>
                <div class="pada-name">Shesha (शेष)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 315° - 326.25°</div>
                <div class="pada-verdict verdict-best">✅ Savings</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">W8</div>
                <div class="pada-name">Rajayakshma (राजयक्ष्मा)</div>
                <div class="pada-direction">📍 West</div>
                <div class="pada-degree">🧭 326.25° - 337.5°</div>
                <div class="pada-verdict verdict-bad">❌ Disease</div>
            </div>
        </div>

        <h3>🌄 NORTH (उत्तर) — 337.5° to 67.5°</h3>
        <div class="pada-grid">
            <div class="pada-card avoid">
                <div class="pada-code">N1</div>
                <div class="pada-name">Roga (रोग)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 337.5° - 348.75°</div>
                <div class="pada-verdict verdict-bad">❌ Disease</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">N2</div>
                <div class="pada-name">Ahi (अहि)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 348.75° - 0°</div>
                <div class="pada-verdict verdict-bad">❌ Fear, anxiety</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">N3</div>
                <div class="pada-name">Mukhya (मुख्य)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 0° - 11.25°</div>
                <div class="pada-verdict verdict-best">✅ Career, success</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">N4</div>
                <div class="pada-name">Bhallataka (भल्लाटक)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 11.25° - 22.5°</div>
                <div class="pada-verdict verdict-best">✅ BEST - Growth</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">N5</div>
                <div class="pada-name">Soma (सोम)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 22.5° - 33.75°</div>
                <div class="pada-verdict verdict-best">✅ Wealth, prosperity</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">N6</div>
                <div class="pada-name">Sarpa (सर्प)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 33.75° - 45°</div>
                <div class="pada-verdict verdict-bad">❌ Fear</div>
            </div>
            <div class="pada-card best">
                <div class="pada-code">N7</div>
                <div class="pada-name">Aditi (अदिति)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 45° - 56.25°</div>
                <div class="pada-verdict verdict-best">✅ Creativity, children</div>
            </div>
            <div class="pada-card avoid">
                <div class="pada-code">N8</div>
                <div class="pada-name">Diti (दिति)</div>
                <div class="pada-direction">📍 North</div>
                <div class="pada-degree">🧭 56.25° - 67.5°</div>
                <div class="pada-verdict verdict-bad">❌ Obstacles</div>
            </div>
        </div>
    </div>`;
}

async function auditEntrance() {
    const direction = document.getElementById('ent-direction').value;
    const pada = parseInt(document.getElementById('ent-pada').value);
    const degree = document.getElementById('ent-degree').value;

    const body = { direction, pada };
    if (degree) body.degree = parseFloat(degree);

    try {
        const res = await fetch(`${API}/api/advanced/entrance/audit`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });
        const data = await res.json();
        document.getElementById('ent-result').innerHTML = `
            <div class="result-box ${data.data.status}">
                <h3>${data.data.verdict}</h3>
                <p><b>Pada:</b> ${data.data.name} (${data.data.hindi})</p>
                <p><b>Effect:</b> ${data.data.effect}</p>
                <p><b>Shastra:</b> ${data.data.shastra}</p>
                ${data.data.remedy ? `<p><b>Remedy:</b> ${data.data.remedy.pooja || 'Multiple remedies available'}</p>` : ''}
            </div>`;
    } catch (e) {
        document.getElementById('ent-result').innerHTML = `<p class="error">Error: ${e.message}</p>`;
    }
}

async function listAllPadas() {
    const res = await fetch(`${API}/api/advanced/entrance/all`);
    const data = await res.json();
    let html = '<div class="grid">';
    for (const p of data.padas) {
        html += `<div class="mini-card ${p.best ? 'best' : 'avoid'}">
            <b>${p.direction} #${p.pada}</b><br>
            ${p.name} (${p.hindi})<br>
            <small>${p.effect}</small>
        </div>`;
    }
    html += '</div>';
    document.getElementById('all-padas').innerHTML = html;
}

// ═══ AYADI ═══
function renderAyadiTab() {
    return `
    <div class="card">
        <h2>📐 Ayadi Shadvarga Calculator</h2>
        <p>Building dimensions se fate calculate karein</p>
        <div class="form-row">
            <div class="form-group">
                <label>Length (ft)</label>
                <input type="number" id="ay-length" value="40" step="0.1">
            </div>
            <div class="form-group">
                <label>Breadth (ft)</label>
                <input type="number" id="ay-breadth" value="30" step="0.1">
            </div>
            <div class="form-group">
                <label>Height (ft)</label>
                <input type="number" id="ay-height" value="10" step="0.1">
            </div>
        </div>
        <button class="btn-primary" onclick="calculateAyadi()">Calculate Ayadi</button>
        <div id="ay-result"></div>
    </div>`;
}

async function calculateAyadi() {
    const body = {
        length: parseFloat(document.getElementById('ay-length').value),
        breadth: parseFloat(document.getElementById('ay-breadth').value),
        height: parseFloat(document.getElementById('ay-height').value)
    };
    const res = await fetch(`${API}/api/advanced/ayadi/calculate`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });
    const data = await res.json();
    const d = data.data;
    document.getElementById('ay-result').innerHTML = `
        <div class="result-box ${d.grade}">
            <h3>${d.verdict}</h3>
            <div class="stats">
                <div class="stat"><b>${d.aya}</b><br>Aya</div>
                <div class="stat"><b>${d.vyaya}</b><br>Vyaya</div>
                <div class="stat"><b>${d.rksa}</b><br>Rksa</div>
                <div class="stat"><b>${d.yoni}</b><br>Yoni</div>
                <div class="stat"><b>${d.vara}</b><br>Vara</div>
                <div class="stat"><b>${d.tithi}</b><br>Tithi</div>
            </div>
        </div>`;
}

// ═══ PLOT ═══
function renderPlotTab() {
    return `
    <div class="card">
        <h2>🏗️ Plot Layout Generator</h2>
        <p>Khali plot ka Vastu layout (authority norms ke saath)</p>
        <div class="form-row">
            <div class="form-group">
                <label>Plot Length (ft)</label>
                <input type="number" id="pl-length" value="40">
            </div>
            <div class="form-group">
                <label>Plot Breadth (ft)</label>
                <input type="number" id="pl-breadth" value="60">
            </div>
            <div class="form-group">
                <label>Facing</label>
                <select id="pl-facing">
                    <option value="North">North</option>
                    <option value="East">East</option>
                    <option value="South">South</option>
                    <option value="West">West</option>
                </select>
            </div>
        </div>
        <button class="btn-primary" onclick="generatePlot()">Generate Layout</button>
        <div id="pl-result"></div>
    </div>`;
}

async function generatePlot() {
    const body = {
        plot_length: parseFloat(document.getElementById('pl-length').value),
        plot_breadth: parseFloat(document.getElementById('pl-breadth').value),
        facing_direction: document.getElementById('pl-facing').value
    };
    const res = await fetch(`${API}/api/advanced/plot/layout`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });
    const data = await res.json();
    const d = data.data;
    let rooms = '<div class="grid">';
    for (const r of d.vastu_rooms) {
        rooms += `<div class="mini-card"><b>${r.name}</b><br><small>${r.hindi}</small><br><span class="zone">${r.zone}</span></div>`;
    }
    rooms += '</div>';
    document.getElementById('pl-result').innerHTML = `
        <div class="result-box good">
            <h3>Plot Layout Ready</h3>
            <div class="stats">
                <div class="stat"><b>${d.plot_dimensions.area_sqft}</b><br>Plot sqft</div>
                <div class="stat"><b>${d.authority_norms.ground_coverage_percent}%</b><br>Coverage</div>
                <div class="stat"><b>${d.authority_norms.far_percent}%</b><br>FAR</div>
                <div class="stat"><b>${d.authority_norms.max_storeys}</b><br>Storeys</div>
            </div>
            <h4>Rooms Placed:</h4>
            ${rooms}
        </div>`;
}

// ═══ REMEDIES ═══
function renderRemediesTab() {
    return `
    <div class="card">
        <h2>💊 3-Tier Remedies</h2>
        <p>Defect select karein — Non-Demolition, Pooja, Demolition</p>
        <div id="defects-list">Loading...</div>
    </div>`;
}

async function loadDefects() {
    const res = await fetch(`${API}/api/advanced/remedies/all`);
    const data = await res.json();
    let html = '<div class="grid">';
    for (const d of data.defects) {
        html += `<div class="mini-card clickable" onclick="loadRemedy('${d.key}')">
            <b>${d.defect}</b><br>
            <span class="severity ${d.severity}">${d.severity}</span>
        </div>`;
    }
    html += '</div><div id="remedy-detail"></div>';
    document.getElementById('defects-list').innerHTML = html;
}

async function loadRemedy(key) {
    const res = await fetch(`${API}/api/advanced/remedies/${key}`);
    const data = await res.json();
    const d = data.data;
    let html = `<div class="result-box">
        <h3>${d.defect}</h3>
        <p><b>Problem:</b> ${d.problem}</p>
        <h4>🟢 Tier 1 (Non-Demolition)</h4>
        <ul>${d.tier_1_non_demolition.remedies.map(r => `<li>${r.action} — ${r.cost}</li>`).join('')}</ul>
        <h4>🟡 Tier 2 (Pooja)</h4>
        <ul>${d.tier_2_pooja.remedies.map(r => `<li>${r.action} — ${r.cost}</li>`).join('')}</ul>
        <h4>🔴 Tier 3 (Demolition)</h4>
        <ul>${d.tier_3_demolition.remedies.length ? d.tier_3_demolition.remedies.map(r => `<li>${r.action}</li>`).join('') : '<li>Zaroorat nahi</li>'}</ul>
        <p><b>Total Cost:</b> ${d.total_cost_estimate}</p>
        <p><b>Mantra:</b> ${d.mantra}</p>
    </div>`;
    document.getElementById('remedy-detail').innerHTML = html;
}

// ═══ POOJA ═══
function renderPoojaTab() {
    return `
    <div class="card">
        <h2>🕉️ Pooja & Mantra</h2>
        <div id="pooja-list">Loading...</div>
    </div>`;
}

async function loadPoojas() {
    const res = await fetch(`${API}/api/advanced/pooja/all`);
    const data = await res.json();
    let html = '<div class="grid">';
    for (const p of data.poojas) {
        html += `<div class="mini-card">
            <b>${p.hindi}</b><br>
            <small>${p.purpose}</small><br>
            <span class="cost">${p.cost}</span>
        </div>`;
    }
    html += '</div>';
    document.getElementById('pooja-list').innerHTML = html;
}

// ═══ INIT ═══
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('tab-content').innerHTML = renderEntranceTab();
});

// Load on tab switch
const origShowTab = showTab;
window.showTab = function(tabName) {
    origShowTab(tabName);
    if (tabName === 'remedies') loadDefects();
    if (tabName === 'pooja') loadPoojas();
};
