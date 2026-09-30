// ═══ VASTU ONE — Plan Upload ═══

let selectedFile = null;

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("vastu_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    attachUploadListeners();
});

// ═══ UPLOAD LISTENERS ═══
function attachUploadListeners() {
    const zone = document.getElementById("uploadZone");
    const input = document.getElementById("planInput");

    zone.addEventListener("click", () => input.click());

    zone.addEventListener("dragover", (e) => {
        e.preventDefault();
        zone.classList.add("dragover");
    });

    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));

    zone.addEventListener("drop", (e) => {
        e.preventDefault();
        zone.classList.remove("dragover");
        if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
    });

    input.addEventListener("change", (e) => {
        if (e.target.files[0]) handleFile(e.target.files[0]);
    });
}

// ═══ FILE HANDLING ═══
function handleFile(file) {
    const allowed = ["image/png", "image/jpeg", "image/jpg", "image/webp"];

    if (!allowed.includes(file.type)) {
        alert("❌ सिर्फ PNG, JPG, JPEG, WEBP files allowed हैं");
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

        // Show preview, hide others
        document.getElementById("stepUpload").style.display = "none";
        document.getElementById("stepPreview").style.display = "block";
        document.getElementById("stepLoading").style.display = "none";
        document.getElementById("stepError").style.display = "none";
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
    document.getElementById("planInput").value = "";

    document.getElementById("stepUpload").style.display = "block";
    document.getElementById("stepPreview").style.display = "none";
    document.getElementById("stepLoading").style.display = "none";
    document.getElementById("stepError").style.display = "none";
}

// ═══ ANALYZE PLAN ═══
async function analyzePlan() {
    if (!selectedFile) {
        alert("पहले file चुनें");
        return;
    }

    const token = localStorage.getItem("vastu_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    // Show loading
    document.getElementById("stepPreview").style.display = "none";
    document.getElementById("stepLoading").style.display = "block";

    // Animate progress steps
    animateProgress();

    // Prepare form data
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("/api/plan/analyze", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed");
        }

        // Success — redirect to report
        showSuccessAndRedirect(data.report_id);

    } catch (err) {
        console.error(err);
        showError(err.message);
    }
}

// ═══ PROGRESS ANIMATION ═══
function animateProgress() {
    const steps = ["ps1", "ps2", "ps3", "ps4", "ps5", "ps6"];

    // Reset
    steps.forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove("active", "done");
        el.textContent = "⏳ " + el.textContent.replace("⏳ ", "").replace("✓ ", "");
    });

    // Animate each step
    steps.forEach((id, i) => {
        setTimeout(() => {
            const el = document.getElementById(id);

            // Mark previous as done
            if (i > 0) {
                const prev = document.getElementById(steps[i - 1]);
                prev.classList.remove("active");
                prev.classList.add("done");
                prev.textContent = "✓ " + prev.textContent.replace("⏳ ", "").replace("✓ ", "");
            }

            // Activate current
            el.classList.add("active");
            el.textContent = "⏳ " + el.textContent.replace("⏳ ", "").replace("✓ ", "");
        }, i * 1200);
    });
}

// ═══ SUCCESS ═══
function showSuccessAndRedirect(reportId) {
    // Mark all steps done
    ["ps1", "ps2", "ps3", "ps4", "ps5", "ps6"].forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove("active");
        el.classList.add("done");
        el.textContent = "✓ " + el.textContent.replace("⏳ ", "").replace("✓ ", "");
    });

    // Redirect to report
    setTimeout(() => {
        window.location.href = "/plan-report/" + reportId;
    }, 800);
}

// ═══ ERROR ═══
function showError(message) {
    document.getElementById("stepLoading").style.display = "none";
    document.getElementById("stepError").style.display = "block";
    document.getElementById("errorMessage").textContent = message;
}