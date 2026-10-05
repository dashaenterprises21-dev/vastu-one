// ═══ VASTU ONE — CHAKRA FORM (Enterprise) ═══

const DEVATAS = [
    "शिखी","पर्जन्य","जयन्त","इन्द्र","सूर्य","सत्य","भूष","आकाश","अनिल",
    "पूषा","वितथ","गृहक्षत","यम","गन्धर्व","भृंगराज","मृग","पितर","दौवारिक",
    "सुग्रीव","पुष्पदन्त","वरुण","असुर","शेष","राजयक्ष्मा","रोग","अहि","मुख्य",
    "भल्लाटक","सोम","सर्प","अदिति","दिति","आप","सावित्र","जय","रुद्र",
    "अर्यमा","सविता","विवस्वान","विबुधाधिप","ब्रह्मा","मित्र","राजयक्ष्मा","पृथ्वीधर","आपवत्स",
    "रोग","अहि","मुख्य","भल्लाटक","सोम","सर्प","अदिति","दिति","आप",
    "सावित्र","जय","रुद्र","अर्यमा","सविता","विवस्वान","विबुधाधिप","मित्र","पृथ्वीधर",
    "आपवत्स","सुग्रीव","पुष्पदन्त","वरुण","असुर","शेष","राजयक्ष्मा","रोग","अहि",
    "मुख्य","भल्लाटक","सोम","सर्प","अदिति","दिति","आप","सावित्री","ब्रह्मा"
];

const ROOMS = {
    kitchen: { name: "Kitchen", hindi: "रसोई", icon: "🍳" },
    bedroom: { name: "Bedroom", hindi: "शयनकक्ष", icon: "🛏️" },
    master_bedroom: { name: "Master", hindi: "मुख्य कक्ष", icon: "🛏️" },
    living: { name: "Living", hindi: "बैठक", icon: "🛋️" },
    dining: { name: "Dining", hindi: "भोजन", icon: "🍽️" },
    toilet: { name: "Toilet", hindi: "शौचालय", icon: "🚿" },
    bathroom: { name: "Bathroom", hindi: "स्नानघर", icon: "🛁" },
    pooja: { name: "Pooja", hindi: "पूजा", icon: "🙏" },
    balcony: { name: "Balcony", hindi: "छज्जा", icon: "🌅" },
    store: { name: "Store", hindi: "भंडार", icon: "📦" },
    staircase: { name: "Stairs", hindi: "सीढ़ी", icon: "🪜" },
    main_entry: { name: "Entry", hindi: "द्वार", icon: "🚪" },
    cash_locker: { name: "Cash", hindi: "तिजोरी", icon: "💰" },
    water_tank: { name: "Water", hindi: "जल टंकी", icon: "💧" },
    parking: { name: "Parking", hindi: "पार्किंग", icon: "🚗" }
};

const PRESETS = {
    "2bhk": [
        { pada: 3, type: "kitchen" },
        { pada: 75, type: "master_bedroom" },
        { pada: 68, type: "bedroom" },
        { pada: 5, type: "living" },
        { pada: 13, type: "toilet" },
        { pada: 8, type: "balcony" },
        { pada: 2, type: "main_entry" }
    ],
    "3bhk": [
        { pada: 3, type: "kitchen" },
        { pada: 75, type: "master_bedroom" },
        { pada: 68, type: "bedroom" },
        { pada: 62, type: "bedroom" },
        { pada: 5, type: "living" },
        { pada: 7, type: "dining" },
        { pada: 13, type: "toilet" },
        { pada: 14, type: "toilet" },
        { pada: 8, type: "balcony" },
        { pada: 4, type: "pooja" },
        { pada: 6, type: "main_entry" }
    ],
    "villa": [
        { pada: 3, type: "kitchen" },
        { pada: 75, type: "master_bedroom" },
        { pada: 68, type: "bedroom" },
        { pada: 62, type: "bedroom" },
        { pada: 5, type: "living" },
        { pada: 7, type: "dining" },
        { pada: 13, type: "toilet" },
        { pada: 14, type: "toilet" },
        { pada: 4, type: "pooja" },
        { pada: 8, type: "balcony" },
        { pada: 77, type: "store" },
        { pada: 76, type: "staircase" },
        { pada: 25, type: "parking" },
        { pada: 2, type: "main_entry" }
    ]
};

let selectedRoom = null;
let selectedSize = "medium";
let cells = {};       // { pada: { type, size, note } }
let history = [];
let historyIndex = -1;
let compassRotation = 0;
let overlayVisible = false;

// ═══ INIT ═══
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("vastu_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    buildGrid();
    attachPaletteListeners();
    attachKeyboardShortcuts();
    loadDraft();
});

// ═══ BUILD GRID ═══
function buildGrid() {
    const grid = document.getElementById("chakraGrid");
    grid.innerHTML = "";

    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            const pada = row * 9 + col + 1;
            const zone = getZone(row, col);

            const cell = document.createElement("div");
            cell.className = `cell zone-${zone}`;
            cell.dataset.pada = pada;
            cell.innerHTML = `
                <span class="cell-pada">${pada}</span>
                <span class="cell-devata">${DEVATAS[pada - 1] || ""}</span>
            `;

            cell.addEventListener("click", () => handleCellClick(pada));
            cell.addEventListener("contextmenu", (e) => {
                e.preventDefault();
                handleRightClick(pada);
            });

            grid.appendChild(cell);
        }
    }

    // Re-apply existing cells
    Object.entries(cells).forEach(([pada, data]) => {
        applyCellToGrid(parseInt(pada), data);
    });
}

function getZone(row, col) {
    if (row < 3 && col < 3) return "NE";
    if (row < 3 && col > 5) return "NW";
    if (row > 5 && col < 3) return "SE";
    if (row > 5 && col > 5) return "SW";
    if (row < 3) return "N";
    if (row > 5) return "S";
    if (col < 3) return "W";
    if (col > 5) return "E";
    return "CENTER";
}

function applyCellToGrid(pada, data) {
    const cell = document.querySelector(`.cell[data-pada="${pada}"]`);
    if (!cell) return;

    const info = ROOMS[data.type];
    if (!info) return;

    cell.classList.add("filled", `size-${data.size || "medium"}`);
    if (data.note) cell.classList.add("has-note");

    cell.innerHTML = `
        <span class="cell-pada">${pada}</span>
        <span class="cell-icon">${info.icon}</span>
        <span class="cell-room">${info.name}</span>
    `;
}

// ═══ PALETTE ═══
function attachPaletteListeners() {
    document.querySelectorAll(".palette-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".palette-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            selectedRoom = btn.dataset.room;

            const info = ROOMS[selectedRoom];
            document.getElementById("selectedRoomValue").textContent =
                `${info.icon} ${info.name} (${info.hindi})`;

            document.getElementById("sizePicker").style.display = "block";
        });
    });
}

function setRoomSize(size) {
    selectedSize = size;
    document.querySelectorAll(".size-btn").forEach(b => b.classList.remove("active"));
    document.querySelector(`.size-btn[data-size="${size}"]`).classList.add("active");
}

// ═══ CELL CLICK ═══
function handleCellClick(pada) {
    if (!selectedRoom) {
        alert("पहले दाएँ से room चुनें");
        return;
    }

    saveHistory();

    // If same room → remove
    if (cells[pada] && cells[pada].type === selectedRoom) {
        delete cells[pada];
        const cell = document.querySelector(`.cell[data-pada="${pada}"]`);
        cell.className = `cell zone-${cell.dataset.zone || getZoneFromPada(pada)}`;
        cell.innerHTML = `
            <span class="cell-pada">${pada}</span>
            <span class="cell-devata">${DEVATAS[pada - 1] || ""}</span>
        `;
    } else {
        cells[pada] = { type: selectedRoom, size: selectedSize, note: cells[pada]?.note || "" };
        applyCellToGrid(pada, cells[pada]);
    }

    updateStats();
    autoSaveDraft();
}

function getZoneFromPada(pada) {
    const row = Math.floor((pada - 1) / 9);
    const col = (pada - 1) % 9;
    return getZone(row, col);
}

// ═══ RIGHT CLICK — NOTES ═══
let currentNotePada = null;

function handleRightClick(pada) {
    if (!cells[pada]) {
        alert("पहले इस cell में room रखें");
        return;
    }

    currentNotePada = pada;
    const info = ROOMS[cells[pada].type];
    document.getElementById("noteInfo").innerHTML =
        `<b>${info.icon} ${info.name}</b> — पद #${pada}`;
    document.getElementById("noteInput").value = cells[pada].note || "";
    document.getElementById("notesPanel").style.display = "block";
    document.getElementById("notesPanel").scrollIntoView({ behavior: "smooth" });
}

function saveNote() {
    if (currentNotePada && cells[currentNotePada]) {
        cells[currentNotePada].note = document.getElementById("noteInput").value.trim();
        const cell = document.querySelector(`.cell[data-pada="${currentNotePada}"]`);
        if (cells[currentNotePada].note) {
            cell.classList.add("has-note");
        } else {
            cell.classList.remove("has-note");
        }
        autoSaveDraft();
    }
    closeNotes();
}

function closeNotes() {
    document.getElementById("notesPanel").style.display = "none";
    currentNotePada = null;
}

// ═══ HISTORY ═══
function saveHistory() {
    history = history.slice(0, historyIndex + 1);
    history.push(JSON.parse(JSON.stringify(cells)));
    historyIndex = history.length - 1;

    if (history.length > 50) {
        history.shift();
        historyIndex--;
    }
}

function undo() {
    if (historyIndex <= 0) return;
    historyIndex--;
    cells = JSON.parse(JSON.stringify(history[historyIndex]));
    rebuildFromCells();
}

function redo() {
    if (historyIndex >= history.length - 1) return;
    historyIndex++;
    cells = JSON.parse(JSON.stringify(history[historyIndex]));
    rebuildFromCells();
}

function rebuildFromCells() {
    buildGrid();
    updateStats();
    autoSaveDraft();
}

// ═══ SAVE DRAFT ═══
function autoSaveDraft() {
    try {
        localStorage.setItem("vastu_chakra_draft", JSON.stringify({
            cells,
            propertyType: document.getElementById("propertyType").value,
            floor: document.getElementById("floor").value,
            plotShape: document.getElementById("plotShape").value,
            savedAt: new Date().toISOString()
        }));
    } catch (e) { console.error(e); }
}

function saveDraft() {
    autoSaveDraft();
    alert("✅ Draft saved!");
}

function loadDraft() {
    try {
        const draft = localStorage.getItem("vastu_chakra_draft");
        if (!draft) return;

        const data = JSON.parse(draft);
        if (!data.cells) return;

        if (Object.keys(data.cells).length === 0) return;

        if (confirm("पिछला draft मिला — load करें?")) {
            cells = data.cells;
            if (data.propertyType) document.getElementById("propertyType").value = data.propertyType;
            if (data.floor) document.getElementById("floor").value = data.floor;
            if (data.plotShape) document.getElementById("plotShape").value = data.plotShape;
            buildGrid();
            updateStats();
        }
    } catch (e) { console.error(e); }
}

// ═══ STATS ═══
function updateStats() {
    const total = Object.keys(cells).length;
    document.getElementById("totalRooms").textContent = total;
    document.getElementById("filledCells").textContent = total;
}

// ═══ CLEAR ═══
function clearAll() {
    if (Object.keys(cells).length > 0 && !confirm("सारे rooms हट जाएँगे?")) return;
    saveHistory();
    cells = {};
    buildGrid();
    updateStats();
    autoSaveDraft();
}

// ═══ PRESETS ═══
function loadPreset(name) {
    if (!PRESETS[name]) return;
    if (Object.keys(cells).length > 0 && !confirm("पुराने rooms हट जाएँगे?")) return;

    saveHistory();
    cells = {};
    PRESETS[name].forEach(item => {
        cells[item.pada] = { type: item.type, size: "medium", note: "" };
    });
    buildGrid();
    updateStats();
    autoSaveDraft();
}

// ═══ COMPASS ROTATION ═══
function rotateCompass() {
    compassRotation = (compassRotation + 90) % 360;
    document.getElementById("compass").style.transform = `rotate(${compassRotation}deg)`;
    const opposite = (compassRotation + 180) % 360;
    document.querySelectorAll(".compass-dir").forEach(el => {
        el.style.transform = `rotate(${-compassRotation}deg)`;
    });
}

// ═══ CHAKRA OVERLAY ═══
function toggleOverlay() {
    overlayVisible = !overlayVisible;
    document.getElementById("chakraOverlay").style.display = overlayVisible ? "block" : "none";
}

// ═══ CHAKRA REFERENCE ═══
function showChakraReference() {
    const modal = document.createElement("div");
    modal.className = "loading-overlay";
    modal.style.cursor = "pointer";
    modal.innerHTML = `
        <div style="max-width: 95vw; max-height: 95vh;">
            <img src="/static/vastu-chakra.jpg" style="max-width: 100%; max-height: 90vh; border-radius: 16px; box-shadow: 0 0 60px rgba(245, 158, 11, 0.5);" alt="Vastu Chakra">
            <p style="text-align: center; margin-top: 16px; color: #fbbf24; font-size: 14px;">
                📖 असली 81 पद वास्तु मंडल — 45 देवता • 32 बाहरी + 13 अंदर
            </p>
            <p style="text-align: center; color: #8b7d6b; font-size: 12px; margin-top: 8px;">क्लिक करके बंद करें</p>
        </div>
    `;
    modal.onclick = () => modal.remove();
    document.body.appendChild(modal);
}

// ═══ PRINT ═══
function printLayout() {
    window.print();
}

// ═══ KEYBOARD ═══
function attachKeyboardShortcuts() {
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "z" && !e.shiftKey) {
            e.preventDefault();
            undo();
        }
        if ((e.ctrlKey || e.metaKey) && (e.key === "y" || (e.shiftKey && e.key === "z"))) {
            e.preventDefault();
            redo();
        }
        if ((e.ctrlKey || e.metaKey) && e.key === "s") {
            e.preventDefault();
            saveDraft();
        }
        if ((e.ctrlKey || e.metaKey) && e.key === "p") {
            e.preventDefault();
            printLayout();
        }
    });
}

// ═══ ANALYZE ═══
async function analyzeVastu() {
    if (Object.keys(cells).length === 0) {
        alert("कम से कम एक room रखें");
        return;
    }

    const token = localStorage.getItem("vastu_token");
    const btn = document.getElementById("analyzeBtn");
    const overlay = document.getElementById("loadingOverlay");

    btn.disabled = true;
    overlay.style.display = "flex";

    const roomsList = Object.entries(cells).map(([pada, data]) => {
        const row = Math.floor((parseInt(pada) - 1) / 9);
        const col = (parseInt(pada) - 1) % 9;
        return {
            pada: parseInt(pada),
            row: row,
            col: col,
            zone: getZone(row, col),
            type: data.type,
            size: data.size || "medium",
            note: data.note || ""
        };
    });

    try {
        const payload = {
            rooms: roomsList,
            property_type: document.getElementById("propertyType").value,
            floor: document.getElementById("floor").value,
            plot_shape: document.getElementById("plotShape").value,
            plot_length: parseFloat(document.getElementById("plotLength").value) || null,
            plot_width: parseFloat(document.getElementById("plotWidth").value) || null
        };

        const response = await fetch("/api/chakra/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed");
        }

        localStorage.setItem("last_analysis", JSON.stringify(data));
        window.location.href = "/report/" + data.report_id;

    } catch (err) {
        console.error(err);
        alert("❌ " + err.message);
        btn.disabled = false;
        overlay.style.display = "none";
    }
}