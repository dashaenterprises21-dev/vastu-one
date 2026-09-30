// ═══ VASTU ONE — AUTH LOGIC ═══

function createParticles() {
    const container = document.getElementById("particles");
    if (!container) return;
    for (let i = 0; i < 25; i++) {
        const p = document.createElement("div");
        p.className = "particle";
        p.style.left = Math.random() * 100 + "%";
        p.style.animationDelay = Math.random() * 8 + "s";
        p.style.animationDuration = (6 + Math.random() * 6) + "s";
        container.appendChild(p);
    }
}

function togglePassword() {
    const input = document.getElementById("password");
    const btn = document.querySelector(".toggle-password");
    if (!input || !btn) return;

    if (input.type === "password") {
        input.type = "text";
        btn.textContent = "🙈";
    } else {
        input.type = "password";
        btn.textContent = "👁️";
    }
}

function showError(msg) {
    const box = document.getElementById("errorBox");
    if (!box) return;
    box.textContent = "❌ " + msg;
    box.style.background = "rgba(239, 68, 68, 0.1)";
    box.style.borderColor = "rgba(239, 68, 68, 0.4)";
    box.style.color = "#fca5a5";
    box.style.display = "block";
    setTimeout(() => { box.style.display = "none"; }, 5000);
}

function showSuccess(msg) {
    const box = document.getElementById("errorBox");
    if (!box) return;
    box.textContent = "✅ " + msg;
    box.style.background = "rgba(16, 185, 129, 0.1)";
    box.style.borderColor = "rgba(16, 185, 129, 0.4)";
    box.style.color = "#6ee7b7";
    box.style.display = "block";
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const btn = document.getElementById("submitBtn");

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
            showError(data.detail || "प्रवेश नहीं हो सका");
            btn.disabled = false;
            btn.querySelector(".btn-text").textContent = "प्रवेश करें";
            btn.querySelector(".btn-arrow").textContent = "→";
            return;
        }

        localStorage.setItem("vastu_token", data.access_token);
        localStorage.setItem("vastu_user", JSON.stringify(data.user));
        showSuccess("स्वागत है, " + data.user.name + "!");

        setTimeout(() => { window.location.href = "/dashboard"; }, 800);

    } catch (err) {
        console.error(err);
        showError("कुछ गड़बड़ हो गई — दोबारा try करें");
        btn.disabled = false;
        btn.querySelector(".btn-text").textContent = "प्रवेश करें";
        btn.querySelector(".btn-arrow").textContent = "→";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    createParticles();
});