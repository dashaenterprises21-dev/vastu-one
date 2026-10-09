// VASTU ONE — Settings

const SETTINGS_KEY = "vastu_settings";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("vastu_access_token");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    loadSettings();
});

// ═══ LOAD SETTINGS ═══
function loadSettings() {
    try {
        const saved = localStorage.getItem(SETTINGS_KEY);
        if (!saved) return;

        const settings = JSON.parse(saved);

        // Notifications
        if (settings.notifEmail !== undefined) document.getElementById("notifEmail").checked = settings.notifEmail;
        if (settings.notifWhatsapp !== undefined) document.getElementById("notifWhatsapp").checked = settings.notifWhatsapp;
        if (settings.notifSms !== undefined) document.getElementById("notifSms").checked = settings.notifSms;
        if (settings.notifMarketing !== undefined) document.getElementById("notifMarketing").checked = settings.notifMarketing;

        // Language & Region
        if (settings.language) document.getElementById("languageSelect").value = settings.language;
        if (settings.timezone) document.getElementById("timezoneSelect").value = settings.timezone;

        // Preferences
        if (settings.theme) document.getElementById("themeSelect").value = settings.theme;
        if (settings.reportType) document.getElementById("reportTypeSelect").value = settings.reportType;
        if (settings.units) document.getElementById("unitSelect").value = settings.units;

        // Privacy
        if (settings.privacyAnalytics !== undefined) document.getElementById("privacyAnalytics").checked = settings.privacyAnalytics;
        if (settings.privacyProfile !== undefined) document.getElementById("privacyProfile").checked = settings.privacyProfile;

    } catch (err) {
        console.error("Failed to load settings:", err);
    }
}

// ═══ SAVE SETTINGS ═══
function saveSettings() {
    const btn = document.getElementById("saveBtn");
    btn.disabled = true;
    btn.textContent = "सेव हो रहा है...";

    const settings = {
        notifEmail: document.getElementById("notifEmail").checked,
        notifWhatsapp: document.getElementById("notifWhatsapp").checked,
        notifSms: document.getElementById("notifSms").checked,
        notifMarketing: document.getElementById("notifMarketing").checked,
        language: document.getElementById("languageSelect").value,
        timezone: document.getElementById("timezoneSelect").value,
        theme: document.getElementById("themeSelect").value,
        reportType: document.getElementById("reportTypeSelect").value,
        units: document.getElementById("unitSelect").value,
        privacyAnalytics: document.getElementById("privacyAnalytics").checked,
        privacyProfile: document.getElementById("privacyProfile").checked,
        updatedAt: new Date().toISOString()
    };

    try {
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
        showToast("✅ सेटिंग सेव हो गई", "success");
    } catch (err) {
        showToast("❌ सेव नहीं हो पाई", "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "💾 सारी सेटिंग सेव करें";
    }
}

// ═══ EXPORT DATA ═══
async function exportData() {
    const token = localStorage.getItem("vastu_access_token");

    try {
        const response = await fetch("/api/user/reports", {
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) throw new Error("Failed to fetch");

        const data = await response.json();

        const exportData = {
            user: JSON.parse(localStorage.getItem("vastu_user") || "{}"),
            reports: data.reports || [],
            exportedAt: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `vastu-one-data-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);

        showToast("✅ Data export हो गया", "success");

    } catch (err) {
        showToast("❌ Export failed: " + err.message, "error");
    }
}

// ═══ DELETE ACCOUNT ═══
async function deleteAccount() {
    if (!confirm("⚠️ क्या आप वाकई अकाउंट डिलीट करना चाहते हैं?\n\nये action वापस नहीं होगा।\nसारी reports हमेशा के लिए मिट जाएँगी।")) {
        return;
    }

    if (!confirm("🔴 आखिरी बार पूछ रहे हैं — पक्का डिलीट करें?")) {
        return;
    }

    const token = localStorage.getItem("vastu_access_token");

    try {
        const response = await fetch("/api/user/account", {
            method: "DELETE",
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) throw new Error("Delete failed");

        showToast("✅ अकाउंट डिलीट हो गया", "success");

        setTimeout(() => {
            localStorage.removeItem("vastu_access_token");
            localStorage.removeItem("vastu_user");
            window.location.href = "/login.html";
        }, 1500);

    } catch (err) {
        showToast("❌ Delete failed: " + err.message, "error");
    }
}

// ═══ TOAST ═══
function showToast(msg, type = "info") {
    const existing = document.querySelector(".toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.className = "toast " + type;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// ═══ SIDEBAR TOGGLE ═══
function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("open");
}

// ═══ LOGOUT ═══
async function logout() {
    const token = localStorage.getItem("vastu_access_token");
    try {
        await fetch("/api/auth/logout", {
            method: "POST",
            headers: { "Authorization": "Bearer " + token }
        });
    } catch (err) { console.error(err); }
    localStorage.removeItem("vastu_access_token");
    localStorage.removeItem("vastu_user");
    window.location.href = "/login.html";
}