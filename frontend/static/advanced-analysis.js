// VASTU ONE - Advanced Studio

let selectedFile = null;
let analysisResult = null;
let currentZoom = 1;
let panX = 0, panY = 0;
let isDragging = false;
let startX = 0, startY = 0;

const planInput = document.getElementById("planInput");
const uploadZone = document.getElementById("uploadZone");

if (uploadZone) {
    uploadZone.addEventListener("click", () => planInput.click());
    uploadZone.addEventListener("dragover", (e) => { e.preventDefault(); uploadZone.classList.add("dragover"); });
    uploadZone.addEventListener("dragleave", () => uploadZone.classList.remove("dragover"));
    uploadZone.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadZone.classList.remove("dragover");
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
    });
}

if (planInput) {
    planInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });
}

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
    const preview = document.getElementById("previewImage");

    if (isPDF) {
        preview.style.display = "none";
        let pdfBox = document.getElementById("pdfPreviewBox");
        if (!pdfBox) {
            pdfBox = document.createElement("div");
            pdfBox.id = "pdfPreviewBox";
            pdfBox.style.cssText = "padding:60px;text-align:center;background:#15192B;border-radius:12px;";
            pdfBox.innerHTML = '<div style="font-size:64px;">📄</div><p style="margin-top:16px;font-size:18px;">PDF File Ready</p>';
            preview.parentElement.appendChild(pdfBox);
        }
        pdfBox.style.display = "block";
    } else {
        preview.style.display = "block";
        const reader = new FileReader();
        reader.onload = (e) => { preview.src = e.target.result; };
        reader.readAsDataURL(file);
    }

    document.getElementById("fileName").textContent = file.name;
    document.getElementById("fileSize").textContent = formatSize(file.size);
    document.getElementById("uploadSection").style.display = "none";
    document.getElementById("previewSection").style.display = "block";
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function removeFile() {
    selectedFile = null;
    planInput.value = "";
    document.getElementById("previewSection").style.display = "none";
    document.getElementById("uploadSection").style.display = "block";
    document.getElementById("resultsSection").style.display = "none";
}

function startOver() {
    removeFile();
    analysisResult = null;
}

async function analyzePlan() {
    if (!selectedFile) return;
    document.getElementById("previewSection").style.display = "none";
    document.getElementById("loadingSection").style.display = "block";
    animateSteps();

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("/api/upload/plan", { method: "POST", body: formData });
        if (!response.ok) {
            const err = await response.text();
            throw new Error("Analysis failed: " + response.status);
        }
        const data = await response.json();
        analysisResult = data;
        localStorage.setItem("plan_analysis", JSON.stringify(data));
        await new Promise(r => setTimeout(r, 1500));
        renderResults(data);
    } catch (err) {
        alert("Error: " + err.message);
        document.getElementById("loadingSection").style.display = "none";
        document.getElementById("previewSection").style.display = "block";
    }
}

function animateSteps() {
    const steps = ["ps1", "ps2", "ps3", "ps4", "ps5", "ps6"];
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
                if (prev) { prev.classList.remove("active"); prev.classList.add("done"); }
            }
            el.classList.add("active");
        }, i * 800);
    });
}

function renderResults(data) {
    document.getElementById("loadingSection").style.display = "none";
    document.getElementById("resultsSection").style.display = "block";
    const a = data.analysis || {};

    // SCORE
    if (a.final_score) {
        const score = a.final_score.total_score || 0;
        document.getElementById("scoreNumber").textContent = score;
        document.getElementById("scoreGrade").textContent = a.final_score.grade || "-";
        const bd = a.final_score.breakdown || {};
        let bdHtml = "";
        for (const [k, v] of Object.entries(bd)) {
            bdHtml += '<div class="bd-item"><span>' + k.replace(/_/g, " ") + '</span><b>' + v + '</b></div>';
        }
        document.getElementById("scoreBreakdown").innerHTML = bdHtml;
    }

    // STATS
    document.getElementById("statRooms").textContent = a.rooms_detected || 0;
    document.getElementById("statDosh").textContent = a.defect_count || 0;
    document.getElementById("statHigh").textContent = a.high_severity_count || 0;
    document.getElementById("statMedium").textContent = a.medium_severity_count || 0;

    // GRID OVERLAY
    if (a.grid_overlay) {
        document.getElementById("gridOverlayImage").src = "data:image/png;base64," + a.grid_overlay;
    }

    // DOSH
    if (a.defects && a.defects.length > 0) {
        document.getElementById("doshBlock").style.display = "block";
        document.getElementById("doshCount").textContent = "(" + a.defects.length + ")";
        let dh = "";
        a.defects.forEach(d => {
            const sevClass = d.severity === "high" ? "sev-high" : (d.severity === "medium" ? "sev-medium" : "sev-low");
            const sevLabel = d.severity === "high" ? "HIGH" : (d.severity === "medium" ? "MEDIUM" : "LOW");
            dh += '<div class="defect-card ' + sevClass + '">';
            dh += '<div class="defect-header"><span class="defect-room">' + (d.room_hindi || d.room_type) + '</span><span class="defect-sev ' + sevClass + '">' + sevLabel + '</span></div>';
            dh += '<div class="defect-zone">Zone: ' + d.zone + ' | Pada #' + (d.pada || 0) + '</div>';
            dh += '<div class="defect-problem"><b>Problem:</b> ' + (d.reason || "") + '</div>';
            dh += '<div class="defect-shastra"><b>Shastra:</b> ' + (d.shastra || "") + '</div>';
            dh += '<div class="defect-fix"><b>Fix:</b> ' + (d.best_directions || []).join(", ") + ' mein shift karein</div>';
            dh += '</div>';
        });
        document.getElementById("defectsList").innerHTML = dh;
    }

    // REMEDIES
    if (a.remedies && a.remedies.length > 0) {
        document.getElementById("remediesBlock").style.display = "block";
        let rh = "";
        a.remedies.forEach(r => {
            rh += '<div class="remedy-card">';
            rh += '<h3>' + r.defect + '</h3>';
            rh += '<p class="remedy-problem">' + r.problem + '</p>';
            if (r.tier_1_simple && r.tier_1_simple.remedies) {
                rh += '<div class="tier"><h4>🟢 Tier 1: Simple Fixes</h4><ul>';
                r.tier_1_simple.remedies.forEach(x => { rh += '<li>' + x.action + ' - ' + (x.cost || "") + '</li>'; });
                rh += '</ul></div>';
            }
            if (r.tier_2_space_surgery && r.tier_2_space_surgery.allowed) {
                rh += '<div class="tier"><h4>🔵 Tier 2: Space Surgery</h4><p>' + r.tier_2_space_surgery.instructions + '</p></div>';
            }
            if (r.tier_3_pyramids) {
                rh += '<div class="tier"><h4>🟣 Tier 3: Pyramids</h4><p>' + r.tier_3_pyramids.placement + ' - ' + r.tier_3_pyramids.cost_estimate + '</p></div>';
            }
            if (r.tier_4_pooja && r.tier_4_pooja.remedies) {
                rh += '<div class="tier"><h4>🟡 Tier 4: Pooja & Mantra</h4><ul>';
                r.tier_4_pooja.remedies.forEach(x => { rh += '<li>' + x.action + ' - ' + (x.cost || "") + '</li>'; });
                rh += '</ul></div>';
            }
            rh += '<div class="mantra-box"><b>Mantra:</b> ' + r.mantra + '</div>';
            rh += '<div class="total-cost">Total: ' + r.total_cost_estimate + '</div>';
            rh += '</div>';
        });
        document.getElementById("remediesList").innerHTML = rh;
    }

    // POOJA
    if (a.pooja_plan && a.pooja_plan.plan && a.pooja_plan.plan.length > 0) {
        document.getElementById("poojaBlock").style.display = "block";
        let ph = "";
        a.pooja_plan.plan.forEach(p => {
            ph += '<div class="pooja-card">';
            ph += '<h3>' + p.pooja + '</h3>';
            ph += '<div class="pooja-mantra">' + p.mantra + '</div>';
            ph += '<div class="pooja-detail"><b>Count:</b> ' + p.count + '</div>';
            ph += '<div class="pooja-detail"><b>Direction:</b> ' + p.direction + '</div>';
            ph += '<div class="pooja-detail"><b>Timing:</b> ' + p.timing + '</div>';
            ph += '<div class="pooja-cost">' + p.cost + '</div>';
            ph += '</div>';
        });
        document.getElementById("poojaList").innerHTML = ph;
        document.getElementById("poojaTotal").textContent = "Total: " + a.pooja_plan.total_cost;
    }

    // ENTRANCE
    if (a.entrance_audit) {
        document.getElementById("entranceBlock").style.display = "block";
        const e = a.entrance_audit;
        const cls = e.status === "correct" ? "correct" : "defect";
        let eh = '<div class="entrance-card ' + cls + '">';
        eh += '<div class="entrance-name">' + e.name + ' (' + e.hindi + ')</div>';
        eh += '<div class="entrance-dir">Direction: ' + e.direction + ' | Pada #' + e.pada + '</div>';
        eh += '<div class="entrance-effect">' + e.effect + '</div>';
        eh += '<div class="entrance-shastra">Shastra: ' + e.shastra + '</div>';
        eh += '</div>';
        document.getElementById("entranceCard").innerHTML = eh;
    }

    // AYADI
    if (a.ayadi) {
        document.getElementById("ayadiBlock").style.display = "block";
        const ay = a.ayadi;
        let ah = "";
        ah += '<div class="ayadi-item"><b>' + ay.aya + '</b><span>Aya</span></div>';
        ah += '<div class="ayadi-item"><b>' + ay.vyaya + '</b><span>Vyaya</span></div>';
        ah += '<div class="ayadi-item"><b>' + ay.rksa + '</b><span>Rksa</span></div>';
        ah += '<div class="ayadi-item"><b>' + ay.yoni + '</b><span>Yoni</span></div>';
        ah += '<div class="ayadi-item"><b>' + ay.vara + '</b><span>Vara</span></div>';
        ah += '<div class="ayadi-item"><b>' + ay.tithi + '</b><span>Tithi</span></div>';
        document.getElementById("ayadiGrid").innerHTML = ah;
        document.getElementById("ayadiVerdict").textContent = ay.verdict;
    }

    document.getElementById("resultsSection").scrollIntoView({ behavior: "smooth" });
}

// ZOOM
function zoomIn() { currentZoom = Math.min(currentZoom + 0.2, 5); applyTransform(); }
function zoomOut() { currentZoom = Math.max(currentZoom - 0.2, 0.5); applyTransform(); }
function resetZoom() { currentZoom = 1; panX = 0; panY = 0; applyTransform(); }
function applyTransform() {
    const img = document.getElementById("gridOverlayImage");
    const info = document.getElementById("zoomInfo");
    if (!img) return;
    img.style.transform = "translate(" + panX + "px," + panY + "px) scale(" + currentZoom + ")";
    if (info) info.textContent = Math.round(currentZoom * 100) + "%";
}

document.addEventListener("wheel", (e) => {
    if (e.target.id === "gridOverlayImage") {
        e.preventDefault();
        if (e.deltaY < 0) zoomIn(); else zoomOut();
    }
}, { passive: false });

document.addEventListener("mousedown", (e) => {
    if (e.target.id === "gridOverlayImage") { isDragging = true; startX = e.clientX - panX; startY = e.clientY - panY; }
});
document.addEventListener("mousemove", (e) => {
    if (isDragging) { panX = e.clientX - startX; panY = e.clientY - startY; applyTransform(); }
});
document.addEventListener("mouseup", () => { isDragging = false; });

async function downloadPDF() {
    if (!analysisResult) { alert("Pehle analysis karein"); return; }
    
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = "PDF Generate Ho Rahi Hai...";
    
    try {
        // Step 1: PDF generate karo
        const response = await fetch("/api/pdf/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                plan: [],
                report_id: analysisResult.upload_id || "report"
            })
        });
        
        if (!response.ok) {
            throw new Error("PDF generate failed: " + response.status);
        }
        
        const data = await response.json();
        
        if (data.filename) {
            // Step 2: Download karo
            window.open("/api/pdf/download/" + data.filename, "_blank");
            btn.textContent = "Download PDF";
            btn.disabled = false;
        } else {
            throw new Error("PDF filename nahi mila");
        }
        
    } catch (err) {
        alert("PDF Error: " + err.message);
        btn.textContent = "Download PDF";
        btn.disabled = false;
    }
}
