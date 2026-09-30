// ═══════════════════════════════════════════════════════════════
// VASTU ONE — Authentication JavaScript
// Login, Signup, Password Toggle, Particles
// ═══════════════════════════════════════════════════════════════

// ═══ LOGIN HANDLER ═══
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const btn = document.getElementById("submitBtn");
    const errorBox = document.getElementById("errorBox");

    // Hide previous error
    if (errorBox) errorBox.style.display = "none";

    // Validation
    if (!email || !password) {
        showError("ईमेल और पासवर्ड दोनों भरें");
        return;
    }

    // Loading state
    btn.disabled = true;
    btn.querySelector(".btn-text").textContent = "प्रवेश हो रहा है...";
    btn.querySelector(".btn-arrow").textContent = "⏳";

    try {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.detail || "प्रवेश नहीं हो सका — ईमेल या पासवर्ड गलत है");
            btn.disabled = false;
            btn.querySelector(".btn-text").textContent = "प्रवेश करें";
            btn.querySelector(".btn-arrow").textContent = "→";
            return;
        }

        // Success — save token
        localStorage.setItem("vastu_token", data.access_token || data.token);
        localStorage.setItem("vastu_user", JSON.stringify(data.user || {}));

        showSuccess("स्वागत है, " + (data.user?.name || "User") + "!");

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 800);

    } catch (err) {
        console.error("Login error:", err);
        showError("कुछ गड़बड़ हो गई — दोबारा try करें");
        btn.disabled = false;
        btn.querySelector(".btn-text").textContent = "प्रवेश करें";
        btn.querySelector(".btn-arrow").textContent = "→";
    }
}

// ═══ SIGNUP HANDLER ═══
async function handleSignup(event) {
    event.preventDefault();

    const name = document.getElementById("name")?.value.trim();
    const email = document.getElementById("email")?.value.trim();
    const phone = document.getElementById("phone")?.value.trim();
    const password = document.getElementById("password")?.value;
    const confirmPassword = document.getElementById("confirmPassword")?.value;
    const btn = document.getElementById("submitBtn");

    if (!name || !email || !password) {
        showError("सभी ज़रूरी fields भरें");
        return;
    }

    if (password.length < 8) {
        showError("पासवर्ड कम से कम 8 characters का होना चाहिए");
        return;
    }

    if (confirmPassword && password !== confirmPassword) {
        showError("पासवर्ड match नहीं कर रहे");
        return;
    }

    if (phone && phone.length < 10) {
        showError("फ़ोन नंबर 10 digit का होना चाहिए");
        return;
    }

    btn.disabled = true;
    btn.querySelector(".btn-text").textContent = "खाता बन रहा है...";
    btn.querySelector(".btn-arrow").textContent = "⏳";

    try {
        const response = await fetch("/api/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, phone, password })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.detail || "साइनअप नहीं हो सका");
            btn.disabled = false;
            btn.querySelector(".btn-text").textContent = "खाता बनाएँ";
            btn.querySelector(".btn-arrow").textContent = "→";
            return;
        }

        showSuccess("खाता बन गया! अब प्रवेश करें...");

        setTimeout(() => {
            window.location.href = "/login";
        }, 1200);

    } catch (err) {
        console.error("Signup error:", err);
        showError("कुछ गड़बड़ हो गई — दोबारा try करें");
        btn.disabled = false;
        btn.querySelector(".btn-text").textContent = "खाता बनाएँ";
        btn.querySelector(".btn-arrow").textContent = "→";
    }
}

// ═══ PASSWORD TOGGLE ═══
function togglePassword() {
    const input = document.getElementById("password");
    if (!input) return;

    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}

// ═══ ERROR DISPLAY ═══
function showError(msg) {
    const box = document.getElementById("errorBox");
    if (!box) {
        alert(msg);
        return;
    }
    box.textContent = "⚠️ " + msg;
    box.style.display = "block";
    box.className = "error-box error";
}

// ═══ SUCCESS DISPLAY ═══
function showSuccess(msg) {
    const box = document.getElementById("errorBox");
    if (!box) return;
    box.textContent = "✅ " + msg;
    box.style.display = "block";
    box.className = "error-box success";
}

// ═══ LOGOUT ═══
function logout() {
    localStorage.removeItem("vastu_token");
    localStorage.removeItem("vastu_user");
    window.location.href = "/login";
}

// ═══ CHECK AUTH (for protected pages) ═══
function requireAuth() {
    const token = localStorage.getItem("vastu_token");
    if (!token) {
        window.location.href = "/login";
        return false;
    }
    return true;
}

// ═══ GET AUTH HEADERS ═══
function getAuthHeaders() {
    const token = localStorage.getItem("vastu_token");
    return {
        "Content-Type": "application/json",
        "Authorization": token ? `Bearer ${token}` : ""
    };
}

// ═══ PARTICLES (background animation) ═══
function createParticles() {
    const container = document.querySelector(".bg-om");
    if (!container) return;

    for (let i = 0; i < 15; i++) {
        const particle = document.createElement("span");
        particle.className = "particle";
        particle.textContent = "ॐ";
        particle.style.left = Math.random() * 100 + "%";
        particle.style.animationDelay = Math.random() * 5 + "s";
        particle.style.animationDuration = (5 + Math.random() * 5) + "s";
        particle.style.fontSize = (12 + Math.random() * 20) + "px";
        container.appendChild(particle);
    }
}

// ═══ INIT ═══
document.addEventListener("DOMContentLoaded", () => {
    createParticles();

    // Auto-redirect if already logged in
    if (window.location.pathname === "/login" || window.location.pathname === "/signup") {
        const token = localStorage.getItem("vastu_token");
        if (token) {
            // Optional: uncomment if you want auto-redirect
            // window.location.href = "/dashboard";
        }
    }
});
