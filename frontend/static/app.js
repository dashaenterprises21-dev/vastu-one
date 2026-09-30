// ═══ STATE ═══
const DEVATAS_81 = [
    // 81 पदों के देवता (9x9) — दिशा के साथ
    // Row 0
    {pada:1,devata:"Shikhi",hindi:"शिखी",zone:"NE"},{pada:2,devata:"Parjanya",hindi:"पर्जन्य",zone:"NE"},{pada:3,devata:"Jayanta",hindi:"जयन्त",zone:"NE"},{pada:4,devata:"Indra",hindi:"इन्द्र",zone:"NE"},{pada:5,devata:"Surya",hindi:"सूर्य",zone:"E"},{pada:6,devata:"Satya",hindi:"सत्य",zone:"E"},{pada:7,devata:"Bhusha",hindi:"भूष",zone:"E"},{pada:8,devata:"Akasha",hindi:"आकाश",zone:"E"},{pada:9,devata:"Anila",hindi:"अनिल",zone:"NE"},
    // Row 1
    {pada:10,devata:"Pusha",hindi:"पूषा",zone:"E"},{pada:11,devata:"Vitatha",hindi:"वितथ",zone:"E"},{pada:12,devata:"Grihakshata",hindi:"गृहक्षत",zone:"E"},{pada:13,devata:"Yama",hindi:"यम",zone:"SE"},{pada:14,devata:"Gandharva",hindi:"गन्धर्व",zone:"SE"},{pada:15,devata:"Bhrungaraja",hindi:"भृंगराज",zone:"SE"},{pada:16,devata:"Mriga",hindi:"मृग",zone:"SE"},{pada:17,devata:"Pitara",hindi:"पितर",zone:"S"},{pada:18,devata:"Dauvarika",hindi:"दौवारिक",zone:"S"},
    // Row 2
    {pada:19,devata:"Sugriva",hindi:"सुग्रीव",zone:"S"},{pada:20,devata:"Pushpadanta",hindi:"पुष्पदन्त",zone:"S"},{pada:21,devata:"Varuna",hindi:"वरुण",zone:"S"},{pada:22,devata:"Asura",hindi:"असुर",zone:"SW"},{pada:23,devata:"Shesha",hindi:"शेष",zone:"SW"},{pada:24,devata:"Rajayakshma",hindi:"राजयक्ष्मा",zone:"SW"},{pada:25,devata:"Roga",hindi:"रोग",zone:"SW"},{pada:26,devata:"Ahi",hindi:"अहि",zone:"W"},{pada:27,devata:"Mukhya",hindi:"मुख्य",zone:"W"},
    // Row 3
    {pada:28,devata:"Bhallataka",hindi:"भल्लाटक",zone:"W"},{pada:29,devata:"Soma",hindi:"सोम",zone:"W"},{pada:30,devata:"Sarpa",hindi:"सर्प",zone:"NW"},{pada:31,devata:"Aditi",hindi:"अदिति",zone:"NW"},{pada:32,devata:"Diti",hindi:"दिति",zone:"NW"},{pada:33,devata:"Apa",hindi:"आप",zone:"N"},{pada:34,devata:"Savitra",hindi:"सावित्र",zone:"N"},{pada:35,devata:"Jaya",hindi:"जय",zone:"N"},{pada:36,devata:"Rudra",hindi:"रुद्र",zone:"N"},
    // Rows 3-5 middle
    {pada:37,devata:"Aryama",hindi:"अर्यमा",zone:"N"},{pada:38,devata:"Savita",hindi:"सविता",zone:"N"},{pada:39,devata:"Vivasvan",hindi:"विवस्वान",zone:"E"},{pada:40,devata:"Vibudhadhipa",hindi:"विबुधाधिप",zone:"E"},{pada:41,devata:"Mitra",hindi:"मित्र",zone:"CENTER"},{pada:42,devata:"Rajayakshma-inner",hindi:"राजयक्ष्मा",zone:"CENTER"},{pada:43,devata:"Prithvidhara",hindi:"पृथ्वीधर",zone:"CENTER"},{pada:44,devata:"Apavatsa",hindi:"आपवत्स",zone:"CENTER"},{pada:45,devata:"Brahma",hindi:"ब्रह्मा",zone:"CENTER"}
];

// ═══ OBJECT OPTIONS ═══
const OBJECT_OPTIONS = [
    {value:"toilet", label:"🚽 शौचालय"},
    {value:"kitchen", label:"🍳 रसोई"},
    {value:"bed", label:"🛏️ बिस्तर"},
    {value:"cash", label:"💰 तिजोरी/नकद"},
    {value:"water", label:"💧 जल/फव्वारा"},
    {value:"fire", label:"🔥 अग्नि/चूल्हा"},
    {value:"heavy", label:"⚖️ भारी सामान"},
    {value:"clutter", label:"📦 अव्यवस्था"},
    {value:"storage", label:"🗄️ भंडारण"},
    {value:"open", label:"🔓 खुला"},
    {value:"light", label:"💡 प्रकाश"},
    {value:"prayer", label:"🙏 पूजा स्थल"},
    {value:"plants", label:"🌿 पौधे"},
    {value:"mirror", label:"🪞 दर्पण"},
    {value:"locker", label:"🔐 लॉकर"},
    {value:"empty", label:"⬜ खाली"},
];

// ═══ PRESETS ═══
const PRESETS = {
    default: [
        {row:0, col:0, object:"toilet"},
        {row:4, col:4, object:"heavy"},
        {row:8, col:8, object:"cash"},
        {row:2, col:2, object:"water"}
    ],
    good: [
        {row:0, col:0, object:"prayer"},
        {row:4, col:4, object:"open"},
        {row:8, col:8, object:"heavy"},
        {row:2, col:2, object:"water"},
        {row:6, col:6, object:"locker"},
        {row:0, col:8, object:"light"}
    ],
    bad: [
        {row:0, col:0, object:"toilet"},
        {row:4, col:4, object:"toilet"},
        {row:8, col:8, object:"water"},
        {row:2, col:2, object:"fire"},
        {row:6, col:6, object:"toilet"},
        {row:0, col:8, object:"heavy"}
    ]
};

// ═══ PLAN BUILDER ═══
let planRows = [];

function addPlanRow(row=0, col=0, obj="toilet") {
    planRows.push({row, col, object: obj});
    renderPlanBuilder();
    renderGridPreview();
}

function removePlanRow(index) {
    planRows.splice(index, 1);
    renderPlanBuilder();
    renderGridPreview();
}

function updatePlanRow(index, field, value) {
    planRows[index][field] = field === "row" || field === "col" ? parseInt(value) : value;
    renderGridPreview();
}

function renderPlanBuilder() {
    const builder = document.getElementById("planBuilder");
    builder.innerHTML = "";

    planRows.forEach((p, i) => {
        const div = document.createElement("div");
        div.className = "plan-row";
        div.innerHTML = `
            <div>
                <label>Row</label>
                <input type="number" min="0" max="8" value="${p.row}"
                       onchange="updatePlanRow(${i}, 'row', this.value)">
            </div>
            <div>
                <label>Col</label>
                <input type="number" min="0" max="8" value="${p.col}"
                       onchange="updatePlanRow(${i}, 'col', this.value)">
            </div>
            <div>
                <label>वस्तु</label>
                <select onchange="updatePlanRow(${i}, 'object', this.value)">
                    ${OBJECT_OPTIONS.map(o =>
                        `<option value="${o.value}" ${o.value===p.object?'selected':''}>${o.label}</option>`
                    ).join("")}
                </select>
            </div>
            <button class="btn-remove" onclick="removePlanRow(${i})">×</button>
        `;
        builder.appendChild(div);
    });
}

function loadPreset(name) {
    planRows = JSON.parse(JSON.stringify(PRESETS[name]));
    renderPlanBuilder();
    renderGridPreview();
}

// ═══ GRID PREVIEW ═══
function renderGridPreview() {
    const grid = document.getElementById("gridPreview");
    grid.innerHTML = "";

    // 81 पदों के लिए zone map
    const zoneMap = buildZoneMap();

    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            const cell = document.createElement("div");
            const zone = zoneMap[r][c];
            cell.className = `grid-cell zone-${zone}`;

            // देवता का नाम
            const devata = DEVATAS_81.find(d => d.zone === zone);
            if (devata) cell.textContent = devata.hindi.substring(0, 2);

            // अगर इस cell में कोई object है
            const item = planRows.find(p => p.row === r && p.col === c);
            if (item) {
                cell.classList.add("has-item");
                cell.title = `${devata?.hindi || ""} - ${item.object}`;
            }

            grid.appendChild(cell);
        }
    }
}

function buildZoneMap() {
    const map = [];
    for (let r = 0; r < 9; r++) {
        map[r] = [];
        for (let c = 0; c < 9; c++) {
            let zone;
            if (r === 4 && c === 4) zone = "CENTER";
            else if (r < 3 && c < 3) zone = "NE";
            else if (r < 3 && c > 5) zone = "NW";
            else if (r > 5 && c < 3) zone = "SE";
            else if (r > 5 && c > 5) zone = "SW";
            else if (r < 3) zone = "N";
            else if (r > 5) zone = "S";
            else if (c < 3) zone = "W";
            else if (c > 5) zone = "E";
            else zone = "CENTER";
            map[r][c] = zone;
        }
    }
    return map;
}

// ═══ ANALYZE ═══
async function analyzeVastu() {
    if (planRows.length === 0) {
        alert("कम से कम एक वस्तु जोड़ें");
        return;
    }

    // Show loading
    document.getElementById("loading").style.display = "block";
    document.getElementById("results").style.display = "none";

    try {
        const response = await fetch("/api/vastu/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                plan: planRows,
                property_type: "residential",
                floors: 1
            })
        });

        if (!response.ok) throw new Error("API error: " + response.status);

        const data = await response.json();
        renderResults(data);
    } catch (err) {
        alert("एरर: " + err.message);
        console.error(err);
    } finally {
        document.getElementById("loading").style.display = "none";
    }
}

// ═══ RENDER RESULTS ═══
function renderResults(data) {
    document.getElementById("results").style.display = "block";

    // Score
    animateScore(data.final_score.total_score, data.final_score.grade);

    // Breakdown chips
    const chips = document.getElementById("breakdownChips");
    const bd = data.final_score.breakdown;
    chips.innerHTML = `
        <div class="chip">देवता <strong>${bd.devata_audit}</strong></div>
        <div class="chip">तत्व <strong>${bd.element_balance}</strong></div>
        <div class="chip">ब्रह्मा <strong>${bd.brahma_sthan}</strong></div>
        <div class="chip">दिशा <strong>${bd.direction_strength}</strong></div>
    `;

    // Issues
    const issuesList = document.getElementById("issuesList");
    issuesList.innerHTML = "";
    if (data.devata_audit.issues.length === 0) {
        document.getElementById("issuesBlock").style.display = "none";
    } else {
        document.getElementById("issuesBlock").style.display = "block";
        data.devata_audit.issues.forEach(issue => {
            const card = document.createElement("div");
            card.className = "issue-card";
            card.innerHTML = `
                <div class="card-header">
                    <span class="card-title">${issue.hindi} — ${issue.direction}</span>
                    <span class="card-badge ${issue.severity}">${issue.severity === 'high' ? 'गंभीर' : 'मध्यम'}</span>
                </div>
                <div class="card-meta">
                    <strong>${issue.problem}</strong><br>
                    असर: ${issue.domain_affected.join(", ")}
                </div>
                ${issue.shastra_reference ? `
                    <div class="shastra-ref">
                        📖 <strong>${issue.shastra_reference.source}</strong> — ${issue.shastra_reference.meaning || ''}
                    </div>
                ` : ''}
            `;
            issuesList.appendChild(card);
        });
    }

    // Positives — skip for now (backend से अलग field चाहिए)
    document.getElementById("positivesBlock").style.display = "none";

    // Remedies
    const remediesList = document.getElementById("remediesList");
    remediesList.innerHTML = "";
    if (data.remedies.length === 0) {
        document.getElementById("remediesBlock").style.display = "none";
    } else {
        document.getElementById("remediesBlock").style.display = "block";
        data.remedies.forEach(r => {
            const card = document.createElement("div");
            card.className = "remedy-card";
            card.innerHTML = `
                <div class="card-header">
                    <span class="card-title">${r.hindi} (${r.devata})</span>
                    <span class="card-badge low">${r.direction}</span>
                </div>
                <div class="card-meta">प्रभावित: ${r.problem_domain.join(", ")}</div>
                <div class="remedy-items">
                    ${r.remedy.positive_objects.map(o => `<span class="remedy-tag">✓ ${o}</span>`).join("")}
                    ${r.remedy.color.map(c => `<span class="remedy-tag">🎨 ${c}</span>`).join("")}
                    ${r.remedy.element_balance.map(e => `<span class="remedy-tag">💡 ${e}</span>`).join("")}
                </div>
                <div class="mantra">🕉️ ${r.remedy.mantra}</div>
            `;
            remediesList.appendChild(card);
        });
    }

    // Element Balance
    const elementsGrid = document.getElementById("elementsGrid");
    elementsGrid.innerHTML = "";
    const balance = data.element_balance.balance || {};
    Object.entries(balance).forEach(([name, value]) => {
        const card = document.createElement("div");
        card.className = "element-card " + (value < 0 ? "weak" : value > 3 ? "strong" : "");
        card.innerHTML = `
            <div class="element-name">${name}</div>
            <div class="element-value">${value}</div>
            <div class="element-status">${value < 0 ? "कमज़ोर" : value > 3 ? "प्रबल" : "संतुलित"}</div>
        `;
        elementsGrid.appendChild(card);
    });

    // Scroll to results
    document.getElementById("results").scrollIntoView({behavior: "smooth"});
}

function animateScore(target, grade) {
    const circle = document.getElementById("scoreProgress");
    const number = document.getElementById("scoreNumber");
    const gradeEl = document.getElementById("scoreGrade");

    gradeEl.textContent = grade;
    document.getElementById("scoreMessage").textContent =
        target >= 90 ? "आपका घर शास्त्रों के अनुसार उत्तम है 🎉" :
        target >= 70 ? "अच्छा है, लेकिन कुछ सुधार संभव है" :
        target >= 50 ? "कुछ दोष हैं, उपाय ज़रूरी है" :
        "गंभीर दोष हैं, तुरंत उपाय करें";

    // Animate circle
    const circumference = 534;
    const offset = circumference - (target / 100) * circumference;
    circle.style.strokeDashoffset = offset;

    // Animate number
    let current = 0;
    const step = target / 60;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        number.textContent = current.toFixed(1);
    }, 20);
}

// ═══ INIT ═══
document.addEventListener("DOMContentLoaded", () => {
    loadPreset("default");
    addPlanRow(8, 8, "locker");
    addPlanRow(6, 6, "plants");
    renderGridPreview();
});