// ═══ VASTU ONE - Upload Logic ═══

let selectedFile = null;
let analysisResult = null;

const uploadZone = document.getElementById("uploadZone");
const fileInput = document.getElementById("fileInput");

// ═══ DRAG & DROP ═══
uploadZone.addEventListener("click", () => fileInput.click());

uploadZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadZone.classList.add("dragover");
});

uploadZone.addEventListener("dragleave", () => {
    uploadZone.classList.remove("dragover");
});

uploadZone.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});

fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) handleFile(file);
});

// ═══ FILE HANDLING ═══
function handleFile(file) {
    const allowed = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp"];

    if (!allowed.includes(file.type)) {
        alert("❌ सिर्फ PNG, JPG, JPEG, WEBP, BMP files allowed हैं");
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert("❌ File 10 MB से छोटी होनी चाहिए");
        return;
    }

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById("previewImage").src = e.target.result;
        document.getElementById("fileName").textContent = file.name;
        document.getElementById("fileSize").textContent = formatSize(file.size);
        document.getElementById("previewSection").style.display = "block";
        document.getElementById("uploadZone").style.display = "none";
    };
    reader.readAsDataURL(file);
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function removeFile() {
    selectedFile = null;
    fileInput.value = "";
    document.getElementById("previewSection").style.display = "none";
    document.getElementById("uploadZone").style.display = "block";
    document.getElementById("resultsSection").style.display = "none";
}

function startOver() {
    removeFile();
    analysisResult = null;
}

// ═══ ANALYSIS ═══
async function analyzePlan() {
    if (!selectedFile) return;

    document.getElementById("previewSection").style.display = "none";
    document.getElementById("loadingSection").style.display = "block";

    // Progress animation
    animateSteps();

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("/api/upload/plan", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Analysis failed: " + response.status);
        }

        const data = await response.json();
        analysisResult = data;

        // Wait for progress animation to complete
        await new Promise(r => setTimeout(r, 1500));

        renderResults(data);

    } catch (err) {
        alert("❌ Error: " + err.message);
        console.error(err);
        document.getElementById("loadingSection").style.display = "none";
        document.getElementById("previewSection").style.display = "block";
    }
}

function animateSteps() {
    const steps = ["step1", "step2", "step3", "step4"];
    steps.forEach(id => {
        document.getElementById(id).classList.remove("active", "done");
    });

    steps.forEach((id, i) => {
        setTimeout(() => {
            const el = document.getElementById(id);
            if (i > 0) {
                document.getElementById(steps[i-1]).classList.remove("active");
                document.getElementById(steps[i-1]).classList.add("done");
                document.getElementById(steps[i-1]).textContent = "✓ " + document.getElementById(steps[i-1]).textContent.replace("⏳ ", "").replace("✓ ", "");
            }
            el.classList.add("active");
            el.textContent = "⏳ " + el.textContent.replace("⏳ ", "").replace("✓ ", "");
        }, i * 800);
    });
}

// ═══ RENDER RESULTS ═══
function renderResults(data) {
    document.getElementById("loadingSection").style.display = "none";
    document.getElementById("resultsSection").style.display = "block";

    const a = data.analysis;

    // Stats
    document.getElementById("roomsCount").textContent = a.rooms_detected || 0;
    document.getElementById("boundaryArea").textContent =
        a.boundary ? Math.round(a.boundary.area / 1000) + "K px" : "—";
    document.getElementById("mappingsCount").textContent =
        (a.room_mappings || []).length;

    // Grid Overlay
    if (a.grid_overlay) {
        document.getElementById("gridOverlayImage").src =
            "data:image/png;base64," + a.grid_overlay;
    }

    // Rooms
    const roomsList = document.getElementById("roomsList");
    roomsList.innerHTML = "";
    (a.rooms || []).forEach((room, i) => {
        const div = document.createElement("div");
        div.className = "room-item";
        div.innerHTML = `
            <div class="room-type">🏠 Room ${i+1}</div>
            <div class="room-meta">
                Type: ${room.type || "unknown"}<br>
                Area: ${Math.round(room.area)} px²<br>
                Center: (${room.center[0]}, ${room.center[1]})
            </div>
        `;
        roomsList.appendChild(div);
    });

    // Mappings
    const mappingsList = document.getElementById("mappingsList");
    mappingsList.innerHTML = "";
    if ((a.room_mappings || []).length === 0) {
        mappingsList.innerHTML = "<p style='color:var(--text-dim)'>कोई room mapping नहीं मिली</p>";
    } else {
        a.room_mappings.forEach(m => {
            const div = document.createElement("div");
            div.className = "mapping-item";
            div.innerHTML = `
                <div class="room-type">
                    ${m.room_type || "Room"}
                    <span class="zone-badge">${m.zone}</span>
                </div>
                <div class="room-meta">
                    पद #${m.pada} | Row ${m.row}, Col ${m.col}
                </div>
            `;
            mappingsList.appendChild(div);
        });
    }

    // Scroll to results
    document.getElementById("resultsSection").scrollIntoView({ behavior: "smooth" });
}

// ═══ FULL REPORT ═══
function generateFullReport() {
    if (!analysisResult) {
        alert("पहले analysis complete करें");
        return;
    }

    // Store in localStorage for report page
    localStorage.setItem("plan_analysis", JSON.stringify(analysisResult));

    alert("✅ Analysis saved! अब आप full report generate कर सकते हैं।");
    // Future: redirect to report page with package selection
    // window.location.href = "/report/select-package";
}