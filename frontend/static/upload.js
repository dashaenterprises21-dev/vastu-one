// VASTU ONE - Upload Logic

let selectedFile = null;
let analysisResult = null;

const uploadZone = document.getElementById("uploadZone");
const fileInput = document.getElementById("fileInput");

// DRAG & DROP
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

// FILE HANDLING
function handleFile(file) {
    const allowed = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp", "application/pdf"];

    if (!allowed.includes(file.type)) {
        alert("Sirf PNG, JPG, PDF files allowed hain");
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert("File 10 MB se chhoti honi chahiye");
        return;
    }

    selectedFile = file;

    const isPDF = file.type === "application/pdf";

    if (isPDF) {
        // PDF - show placeholder
        document.getElementById("previewImage").style.display = "none";
        document.getElementById("pdfPreview").style.display = "block";
    } else {
        // Image - show preview
        document.getElementById("previewImage").style.display = "block";
        document.getElementById("pdfPreview").style.display = "none";
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById("previewImage").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    document.getElementById("fileName").textContent = file.name;
    document.getElementById("fileSize").textContent = formatSize(file.size);
    document.getElementById("previewSection").style.display = "block";
    document.getElementById("uploadZone").style.display = "none";
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

// ANALYSIS
async function analyzePlan() {
    if (!selectedFile) return;

    document.getElementById("previewSection").style.display = "none";
    document.getElementById("loadingSection").style.display = "block";

    animateSteps();

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("/api/upload/plan", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error("Analysis failed: " + response.status + " - " + errText);
        }

        const data = await response.json();
        analysisResult = data;

        await new Promise(r => setTimeout(r, 1500));

        renderResults(data);

    } catch (err) {
        alert("Error: " + err.message);
        console.error(err);
        document.getElementById("loadingSection").style.display = "none";
        document.getElementById("previewSection").style.display = "block";
    }
}

function animateSteps() {
    const steps = ["step1", "step2", "step3", "step4"];
    steps.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove("active", "done");
    });

    steps.forEach((id, i) => {
        setTimeout(() => {
            const el = document.getElementById(id);
            if (!el) return;
            if (i > 0) {
                const prev = document.getElementById(steps[i-1]);
                if (prev) {
                    prev.classList.remove("active");
                    prev.classList.add("done");
                }
            }
            el.classList.add("active");
        }, i * 800);
    });
}

// RENDER RESULTS
function renderResults(data) {
    document.getElementById("loadingSection").style.display = "none";
    document.getElementById("resultsSection").style.display = "block";

    const a = data.analysis;

    document.getElementById("roomsCount").textContent = a.rooms_detected || 0;
    document.getElementById("boundaryArea").textContent =
        a.boundary ? Math.round(a.boundary.area / 1000) + "K px" : "-";
    document.getElementById("mappingsCount").textContent =
        (a.room_mappings || []).length;

    if (a.grid_overlay) {
        document.getElementById("gridOverlayImage").src =
            "data:image/png;base64," + a.grid_overlay;
    }

    const roomsList = document.getElementById("roomsList");
    roomsList.innerHTML = "";
    (a.rooms || []).forEach((room, i) => {
        const div = document.createElement("div");
        div.className = "room-item";
        div.innerHTML = `
            <div class="room-type">Room ${i+1}</div>
            <div class="room-meta">
                Type: ${room.type || "unknown"}<br>
                Area: ${Math.round(room.area)} px<br>
                Center: (${room.center[0]}, ${room.center[1]})
            </div>
        `;
        roomsList.appendChild(div);
    });

    const mappingsList = document.getElementById("mappingsList");
    mappingsList.innerHTML = "";
    if ((a.room_mappings || []).length === 0) {
        mappingsList.innerHTML = "<p style='color:#999'>Koi room mapping nahi mili</p>";
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
                    Pad #${m.pada} | Row ${m.row}, Col ${m.col}
                </div>
            `;
            mappingsList.appendChild(div);
        });
    }

    document.getElementById("resultsSection").scrollIntoView({ behavior: "smooth" });
}

// FULL REPORT
function generateFullReport() {
    if (!analysisResult) {
        alert("Pehle analysis complete karein");
        return;
    }

    localStorage.setItem("plan_analysis", JSON.stringify(analysisResult));
    alert("Analysis saved! Ab aap full report generate kar sakte hain.");
}
