// VASTU ONE - Plan Upload Logic

let selectedFile = null;
let analysisResult = null;

const planInput = document.getElementById("planInput");

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
    analyzePlan();
}

async function analyzePlan() {
    if (!selectedFile) {
        alert("Pehle file chunein");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    // Show loading if element exists
    const loadingEl = document.getElementById("loadingSection");
    if (loadingEl) loadingEl.style.display = "block";

    try {
        const response = await fetch("/api/upload/plan", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error("Upload failed: " + response.status + " - " + errText);
        }

        const data = await response.json();
        analysisResult = data;

        // Store for report page
        localStorage.setItem("plan_analysis", JSON.stringify(data));

        // Redirect to report page
        const reportId = data.upload_id || "latest";
        window.location.href = "/plan-report?id=" + reportId;

    } catch (err) {
        alert("Error: " + err.message);
        console.error(err);
        if (loadingEl) loadingEl.style.display = "none";
    }
}
