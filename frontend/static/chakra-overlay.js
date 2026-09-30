// ═══ VASTU ONE — CHAKRA OVERLAY ═══

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

let canvas = null;
let chakraImage = null;
let planImage = null;
let planURL = null;
let currentRoom = null;
let placedRooms = []; // { pada, row, col, zone, type, markerX, markerY }

// ═══ INIT ═══
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("vastu_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }
    initCanvas();
    attachUpload();
    buildPalette();
});

function initCanvas() {
    canvas = new fabric.Canvas("canvas", {
        backgroundColor: "#ffffff",
        selection: false,
    });
}

// ═══ UPLOAD ═══
function attachUpload() {
    const zone = document.getElementById("uploadZone");
    const input = document.getElementById("planInput");

    zone.addEventListener("click", () => input.click());
    zone.addEventListener("dragover", (e) => { e.preventDefault(); zone.classList.add("dragover"); });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", (e) => {
        e.preventDefault();
        zone.classList.remove("dragover");
        if (e.dataTransfer.files[0]) handlePlanFile(e.dataTransfer.files[0]);
    });

    input.addEventListener("change", (e) => {
        if (e.target.files[0]) handlePlanFile(e.target.files[0]);
    });
}

function handlePlanFile(file) {
    if (file.size > 10 * 1024 * 1024) {
        alert("File 10 MB से छोटी होनी चाहिए");
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        planURL = e.target.result;
        loadPlanOnCanvas(planURL);
    };
    reader.readAsDataURL(file);
}

function loadPlanOnCanvas(url) {
    fabric.Image.fromURL(url, (img) => {
        // Resize to fit
        const maxW = 900;
        const maxH = 700;
        let scale = 1;

        if (img.width > maxW) scale = maxW / img.width;
        if (img.height * scale > maxH) scale = maxH / img.height;

        img.set({
            left: 0,
            top: 0,
            scaleX: scale,
            scaleY: scale,
            selectable: false,
            evented: false,
            name: "plan"
        });

        planImage = img;

        const canvasW = img.width * scale;
        const canvasH = img.height * scale;

        canvas.setWidth(canvasW);
        canvas.setHeight(canvasH);
        canvas.clear();
        canvas.backgroundColor = "#ffffff";
        canvas.add(img);
        canvas.sendToBack(img);
        canvas.renderAll();

        // Load chakra overlay
        loadChakraOverlay(canvasW, canvasH);

        // Show next steps
        document.getElementById("stepUpload").style.display = "none";
        document.getElementById("stepCanvas").style.display = "block";
        document.getElementById("stepPalette").style.display = "block";
        document.getElementById("stepOptions").style.display = "block";
        document.getElementById("stepSubmit").style.display = "block";
    }, { crossOrigin: "anonymous" });
}

// ═══ CHAKRA OVERLAY ═══
function loadChakraOverlay(canvasW, canvasH) {
    fabric.Image.fromURL("/static/vastu-chakra.jpg", (img) => {
        const size = Math.min(canvasW, canvasH) * 0.75;
        const scale = size / Math.max(img.width, img.height);

        img.set({
            left: (canvasW - img.width * scale) / 2,
            top: (canvasH - img.height * scale) / 2,
            scaleX: scale,
            scaleY: scale,
            opacity: 0.35,
            selectable: true,
            hasControls: true,
            hasBorders: true,
            lockUniScaling: true,
            name: "chakra",
            cornerColor: "#f59e0b",
            cornerSize: 12,
            transparentCorners: false,
            borderColor: "#f59e0b",
        });

        chakraImage = img;
        canvas.add(img);
        canvas.bringToFront(img);
        canvas.setActiveObject(img);
        canvas.renderAll();
    });
}

// ═══ CHAKRA CONTROLS ═══
function rotateChakra(deg) {
    if (!chakraImage) return;
    chakraImage.rotate((chakraImage.angle || 0) + deg);
    canvas.renderAll();
}

function toggleChakra() {
    if (!chakraImage) return;
    chakraImage.set("visible", !chakraImage.visible);
    canvas.renderAll();
}

function opacityChakra() {
    if (!chakraImage) return;
    const current = chakraImage.opacity;
    const next = current > 0.5 ? 0.2 : current > 0.15 ? 0.5 : 0.15;
    // Cycle: 0.35 → 0.15 → 0.5 → 0.35 → ...
    let newOp = 0.35;
    if (current > 0.45) newOp = 0.15;
    else if (current > 0.25) newOp = 0.5;
    else if (current > 0.1) newOp = 0.35;
    chakraImage.set("opacity", newOp);
    canvas.renderAll();
}

function resetChakra() {
    if (!chakraImage) return;
    const canvasW = canvas.getWidth();
    const canvasH = canvas.getHeight();
    const size = Math.min(canvasW, canvasH) * 0.75;
    const scale = size / Math.max(chakraImage.width, chakraImage.height);

    chakraImage.set({
        left: (canvasW - chakraImage.width * scale) / 2,
        top: (canvasH - chakraImage.height * scale) / 2,
        scaleX: scale,
        scaleY: scale,
        angle: 0,
        opacity: 0.35,
        visible: true
    });
    canvas.renderAll();
}

// ═══ PALETTE ═══
function buildPalette() {
    const palette = document.getElementById("roomPalette");
    palette.innerHTML = Object.entries(ROOMS).map(([key, info]) => `
        <button class="palette-btn" data-room="${key}">
            <span class="palette-icon">${info.icon}</span>
            <span class="palette-label">${info.name}</span>
            <span class="palette-hindi">${info.hindi}</span>
        </button>
    `).join("");

    palette.querySelectorAll(".palette-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            palette.querySelectorAll(".palette-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentRoom = btn.dataset.room;
        });
    });

    // Canvas click → place room
    canvas.on("mouse:down", (opt) => {
        if (!currentRoom) return;
        const pointer = canvas.getPointer(opt.e);

        // Check if clicking on chakra (if so, don't place)
        const target = opt.target;
        if (target && target.name === "chakra") return;

        placeRoomMarker(pointer.x, pointer.y, currentRoom);
    });
}

function placeRoomMarker(x, y, roomType) {
    const info = ROOMS[roomType];

    // Calculate position relative to chakra to determine pada
    let pada = null;
    let row = null;
    let col = null;
    let zone = null;

    if (chakraImage) {
        // Get chakra bounding box
        const chakraBox = chakraImage.getBoundingRect(true);
        // Check if click is inside chakra
        if (x >= chakraBox.left && x <= chakraBox.left + chakraBox.width &&
            y >= chakraBox.top && y <= chakraBox.top + chakraBox.height) {

            // Calculate pada from position (9x9 grid inside chakra)
            const relX = (x - chakraBox.left) / chakraBox.width;
            const relY = (y - chakraBox.top) / chakraBox.height;

            // Rotate coordinates by chakra angle if needed
            let angle = (chakraImage.angle || 0) * Math.PI / 180;
            // Note: for simplicity, ignoring rotation for pada calculation

            col = Math.min(8, Math.max(0, Math.floor(relX * 9)));
            row = Math.min(8, Math.max(0, Math.floor(relY * 9)));
            pada = row * 9 + col + 1;
            zone = getZone(row, col);
        }
    }

    // Create marker
    const marker = new fabric.Group([
        new fabric.Circle({
            radius: 22,
            fill: "#f59e0b",
            stroke: "#1a1410",
            strokeWidth: 2,
            originX: "center",
            originY: "center"
        }),
        new fabric.Text(info.icon, {
            fontSize: 22,
            originX: "center",
            originY: "center",
            top: -2
        })
    ], {
        left: x,
        top: y,
        originX: "center",
        originY: "center",
        selectable: true,
        hasControls: false,
        hasBorders: true,
        name: "room-" + placedRooms.length,
        roomType: roomType,
        pada: pada,
        row: row,
        col: col,
        zone: zone,
        cornerColor: "#1a1410",
        borderColor: "#1a1410"
    });

    canvas.add(marker);
    canvas.bringToFront(marker);

    placedRooms.push({
        marker: marker,
        type: roomType,
        pada: pada,
        row: row,
        col: col,
        zone: zone
    });

    canvas.renderAll();
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

// ═══ ANALYZE ═══
async function analyzeVastu() {
    if (placedRooms.length === 0) {
        alert("कम से कम एक room place करें");
        return;
    }

    // Filter only rooms with valid pada
    const roomsData = placedRooms
        .filter(r => r.pada !== null)
        .map(r => ({
            pada: r.pada,
            row: r.row,
            col: r.col,
            zone: r.zone,
            type: r.type,
            size: "medium",
            note: ""
        }));

    if (roomsData.length === 0) {
        alert("Rooms चक्र के अंदर रखें — चक्र पर click करें");
        return;
    }

    const token = localStorage.getItem("vastu_token");
    const btn = document.getElementById("analyzeBtn");
    const overlay = document.getElementById("loadingOverlay");

    btn.disabled = true;
    overlay.style.display = "flex";

    try {
        const response = await fetch("/api/chakra/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                rooms: roomsData,
                property_type: document.getElementById("propertyType").value,
                floor: document.getElementById("floor").value,
                plot_shape: document.getElementById("plotShape").value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed");
        }

        localStorage.setItem("last_analysis", JSON.stringify(data));
        window.location.href = "/chakra-report/" + data.report_id;

    } catch (err) {
        console.error(err);
        alert("❌ " + err.message);
        btn.disabled = false;
        overlay.style.display = "none";
    }
}