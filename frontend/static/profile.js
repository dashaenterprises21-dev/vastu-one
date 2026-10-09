// VASTU ONE — Profile

let currentUser = null;

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("vastu_access_token");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    await loadProfile();
    loadBirthInfo();
});

// ═══ LOAD PROFILE ═══
async function loadProfile() {
    try {
        const token = localStorage.getItem("vastu_access_token");
        const response = await fetch("/api/user/profile", {
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) throw new Error("Failed to load profile");

        currentUser = await response.json();
        const initial = (currentUser.name || "U").charAt(0).toUpperCase();

        document.getElementById("profileAvatar").textContent = initial;
        document.getElementById("profileName").textContent = currentUser.name;
        document.getElementById("profileEmail").textContent = currentUser.email;
        document.getElementById("profileRole").textContent = currentUser.role || "User";

        document.getElementById("inputName").value = currentUser.name || "";
        document.getElementById("inputEmail").value = currentUser.email || "";
        document.getElementById("inputPhone").value = currentUser.phone || "";
        document.getElementById("inputCity").value = currentUser.city || "";
        document.getElementById("inputState").value = currentUser.state || "";

    } catch (err) {
        console.error(err);
        showToast("प्रोफाइल लोड नहीं हो पाई", "error");
    }
}

// ═══ UPDATE PROFILE ═══
async function updateProfile(event) {
    event.preventDefault();
    const token = localStorage.getItem("vastu_access_token");
    const btn = document.getElementById("saveBtn");
    btn.disabled = true;
    btn.textContent = "सेव हो रहा है...";

    try {
        const body = {
            name: document.getElementById("inputName").value.trim(),
            phone: document.getElementById("inputPhone").value.trim() || null,
            city: document.getElementById("inputCity").value.trim() || null,
            state: document.getElementById("inputState").value.trim() || null,
        };

        const response = await fetch("/api/user/profile", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) throw new Error("Update failed");

        const data = await response.json();
        localStorage.setItem("vastu_user", JSON.stringify(data));

        showToast("✅ प्रोफाइल अपडेट हो गई", "success");
        setTimeout(() => loadProfile(), 500);

    } catch (err) {
        console.error(err);
        showToast("प्रोफाइल अपडेट नहीं हो पाई", "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "💾 सेव करें";
    }
}

// ═══ BIRTH INFO (for Astro) ═══
function saveBirthInfo(event) {
    event.preventDefault();
    const birthInfo = {
        dob: document.getElementById("inputDob").value,
        time: document.getElementById("inputTime").value,
        birthCity: document.getElementById("inputBirthCity").value.trim(),
    };

    localStorage.setItem("vastu_birth_info", JSON.stringify(birthInfo));
    showToast("✅ जन्म जानकारी सेव हो गई", "success");
}

function loadBirthInfo() {
    try {
        const saved = localStorage.getItem("vastu_birth_info");
        if (!saved) return;

        const info = JSON.parse(saved);
        if (info.dob) document.getElementById("inputDob").value = info.dob;
        if (info.time) document.getElementById("inputTime").value = info.time;
        if (info.birthCity) document.getElementById("inputBirthCity").value = info.birthCity;
    } catch (e) { console.error(e); }
}

// ═══ CHANGE PASSWORD ═══
async function changePassword(event) {
    event.preventDefault();
    const token = localStorage.getItem("vastu_access_token");
    const oldPass = document.getElementById("oldPassword").value;
    const newPass = document.getElementById("newPassword").value;

    try {
        const response = await fetch("/api/user/change-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ old_password: oldPass, new_password: newPass })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail || "Failed");

        showToast("✅ पासवर्ड बदल गया", "success");
        document.getElementById("passwordForm").reset();

    } catch (err) {
        showToast("❌ " + err.message, "error");
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