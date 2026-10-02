// ═══════════════════════════════════════════════════════════════
// VASTU ONE — Plan Upload Logic (Multi-Step UI)
// ═══════════════════════════════════════════════════════════════

let selectedFile = null;

// ═══ DOM ELEMENTS ═══
const planInput = document.getElementById("planInput");
const uploadZone = document.getElementById("uploadZone");
const stepUpload = document.getElementById("stepUpload");
const stepPreview = document.getElementById("stepPreview");
const stepLoading = document.getElementById("stepLoading");
const stepError = document.getElementById("stepError");
const previewImage = document.getElementById("previewImage");
const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");
const errorTitle = document.getElementById("errorTitle");
const errorMessage = document.getElementById("errorMessage");

// ═══ UPLOAD ZONE EVENTS ═══
if (uploadZone) {
    uploadZone.addEventListener("click", () => planInput.click());
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
}

if (planInput) {
    planInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });
}

// ═══ FILE HANDLING ═══
function handleFile(file) {
    const allowed = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp", "application/pdf"];

    if (!allowed.includes(file.type)) {
        showError("Galat File Type", "Sirf PNG, JPG, PDF files allowed hain");
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showError("File Bahut Badi", "File 10 MB se chhoti honi chahiye");
        return;
    }

    selectedFile = file;
    showPreview(file);
}

// ═══ SHOW PREVIEW STEP ═══
function showPreview(file) {
    // Hide upload, show preview
    if (stepUpload) stepUpload.style.display = "none";
    if (stepPreview) stepPreview.style.display = "block";
    if (stepLoading) stepLoading.style.display = "none";
    if (stepError) stepError.style.display = "none";

    // File info
    if (fileName) fileName.textContent = file.name;
    if (fileSize) fileSize.textContent = formatSize(file.size);

    // Image preview
    if (previewImage) {
        if (file.type === "application/pdf") {
            previewImage.style.display = "none";
            // Show PDF placeholder
            let pdfBox = document.getElementById("pdfPreviewBox");
            if (!pdfBox) {
                pdfBox = document.createElement("div");
                pdfBox.id = "pdfPreviewBox";
                pdfBox.style.cssText = "padding:60px 20px; text-align:center; background:#f9f9f9; border-radius:12px;";
                pdfBox.innerHTML = '<div style="font-size:64px;">📄</div><p style="margin-top:16px; font-size:18px; font-weight:600;">PDF File Ready</p><p style="color:#666; font-size:14px;">Analysis ke liye "AI se Analyze karein" dabayein</p>';
                previewImage.parentElement.appendChild(pdfBox);
            }
            pdfBox.style.display = "block";
        } else {
            previewImage.style.display = "block";
            const pdfBox = document.getElementById("pdfPreviewBox");
            if (pdfBox) pdfBox.style.display = "none";
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    }
}

// ═══ ANALYZE PLAN ═══
async function analyzePlan() {
    if (!selectedFile) {
        showError("File Nahi Hai", "Pehle file chunein");
        return;
    }

    // Hide preview, show loading
    if (stepPreview) stepPreview.style.display = "none";
    if (stepLoading) stepLoading.style.display = "block";

    // Animate progress steps
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
            throw new Error("Server error " + response.status + ": " + errText);
        }

        const data = await response.json();
        localStorage.setItem("plan_analysis", JSON.stringify(data));

        // Wait for animation to complete
        await new Promise(r => setTimeout(r, 2000));

        // Redirect to report page
        const reportId = data.upload_id || "latest";
        window.location.href = "/plan-report?id=" + reportId;

    } catch (err) {
        console.error(err);
        showError("Analysis Fail Ho Gaya", err.message || "Dobaara try karein");
    }
}

// ═══ PROGRESS STEPS ANIMATION ═══
function animateSteps() {
    const steps = ["ps1", "ps2", "ps3", "ps4", "ps5", "ps6"];
    const messages = [
        "Plan पढ़ा जा रहा है",
        "Rooms detect हो रहे हैं",
        "Directions निकाले जा रहे हैं",
        "45 देवताओं से check हो रहा है",
        "शास्त्र प्रमाण जोड़े जा रहे हैं",
        "Report तैयार हो रही है"
    ];

    steps.forEach((id, i) => {
        setTimeout(() => {
            const el = document.getElementById(id);
            if (!el) return;
            // Mark previous as done
            if (i > 0) {
                const prev = document.getElementById(steps[i-1]);
                if (prev) {
                    prev.classList.add("done");
                    prev.textContent = "✅ " + messages[i-1];
                }
            }
            el.classList.add("active");
            el.textContent = "⏳ " + messages[i];
        }, i * 1500);
    });

    // Last step complete after all
    setTimeout(() => {
        const last = document.getElementById(steps[steps.length-1]);
        if (last) {
            last.classList.add("done");
            last.textContent = "✅ " + messages[messages.length-1];
        }
    }, steps.length * 1500);
}

// ═══ ERROR DISPLAY ═══
function showError(title, message) {
    if (stepUpload) stepUpload.style.display = "none";
    if (stepPreview) stepPreview.style.display = "none";
    if (stepLoading) stepLoading.style.display = "none";
    if (stepError) stepError.style.display = "block";

    if (errorTitle) errorTitle.textContent = title;
    if (errorMessage) errorMessage.textContent = message;
}

// ═══ REMOVE FILE / RESET ═══
function removeFile() {
    selectedFile = null;
    if (planInput) planInput.value = "";
    if (previewImage) previewImage.src = "";

    if (stepUpload) stepUpload.style.display = "block";
    if (stepPreview) stepPreview.style.display = "none";
    if (stepLoading) stepLoading.style.display = "none";
    if (stepError) stepError.style.display = "none";
}

// ═══ FORMAT SIZE ═══
function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}
