// ═══ VASTU ONE — REPORTS LIST ═══

let allReports = [];
let currentFilter = "all";

const PACKAGE_ICONS = {
    bronze: "🎯",
    silver: "⭐",
    gold: "👑",
    platinum: "💎"
};
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("vastu_access_token");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }
    loadReports();
});

async function loadReports() {
    const token = localStorage.getItem("vastu_access_token");
    const grid = document.getElementById("reportsGrid");

    try {
        const response = await fetch("/api/user/reports", {
            headers: { "Authorization": "Bearer " + token }
        });

        if (response.status === 401) {
            localStorage.removeItem("vastu_access_token");
            window.location.href = "/login.html";
            return;
        }

        if (!response.ok) throw new Error("Failed to load reports");

        const data = await response.json();
        allReports = data.reports || [];

        renderReports(allReports);

    } catch (err) {
        console.error(err);
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>
                <h3>Reports लोड नहीं हो पाईं</h3>
                <p>कुछ गड़बड़ हो गई — page refresh करें</p>
            </div>
        `;
    }
}

function renderReports(reports) {
    const grid = document.getElementById("reportsGrid");

    if (!reports || reports.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <h3>अभी कोई Report नहीं है</h3>
                <p>अपना पहला plan upload करें और report पाएँ</p>
                <a href="/upload" class="btn-new">📤 पहली Report बनाएँ</a>
            </div>
        `;
        return;
    }

    grid.innerHTML = "";
    reports.forEach(report => {
        const card = document.createElement("div");
        const pkg = (report.package || "silver").toLowerCase();
        card.className = `report-card ${pkg}`;

        const icon = PACKAGE_ICONS[pkg] || "📄";
        const status = (report.payment_status || "pending").toLowerCase();
        const createdDate = report.created_at
            ? new Date(report.created_at).toLocaleDateString('hi-IN', {
                day: '2-digit', month: 'short', year: 'numeric'
            })
            : "—";

        const isPaid = status === "paid";
        const viewUrl = report.view_url || `/report/${report.report_id}`;

        card.innerHTML = `
            <div class="card-top">
                <div class="card-icon">${icon}</div>
                <span class="status-badge ${status}">
                    ${status === 'paid' ? '✅ Paid' : status === 'pending' ? '⏳ Pending' : '❌ Failed'}
                </span>
            </div>

            <div class="report-id">${report.report_id || 'N/A'}</div>
            <div class="report-package">${pkg} Package</div>
            <div class="report-price">₹${(report.price || 0).toLocaleString('en-IN')}</div>

            <div class="report-meta">
                <div class="meta-row">
                    <span class="label">तारीख</span>
                    <span class="value">${createdDate}</span>
                </div>
            </div>

            <div class="card-actions">
                <a href="${isPaid ? viewUrl : '#'}"
                   class="btn-action btn-view"
                   ${isPaid ? '' : 'onclick="event.preventDefault(); alert(\'Payment pending है — पहले payment करें\')"'}>
                    ${isPaid ? '📄 देखें' : '⏳ Pending'}
                </a>
                <button class="btn-action btn-share"
                        ${isPaid ? '' : 'disabled'}
                        onclick="shareReport('${report.report_id}', '${viewUrl}')">
                    📱 Share
                </button>
            </div>
        `;

        grid.appendChild(card);
    });
}

function filterReports(filter, btn) {
    currentFilter = filter;
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    let filtered = allReports;

    if (filter === "paid") {
        filtered = allReports.filter(r => r.payment_status === "paid");
    } else if (filter === "pending") {
        filtered = allReports.filter(r => r.payment_status === "pending");
    } else if (["bronze", "silver", "gold", "platinum"].includes(filter)) {
        filtered = allReports.filter(r => r.package === filter);
    }

    renderReports(filtered);
}

function shareReport(reportId, viewUrl) {
    const fullUrl = window.location.origin + viewUrl;
    const text = `🕉️ VASTU ONE — आपकी वास्तु रिपोर्ट\n\n` +
                 `Report ID: ${reportId}\n` +
                 `देखें: ${fullUrl}\n\n` +
                 `India Ka No.1 Vastu Engine`;

    if (navigator.share) {
        navigator.share({
            title: "Vastu One Report",
            text: text,
            url: fullUrl
        }).catch(err => console.log("Share cancelled", err));
    } else {
        // WhatsApp fallback
        const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(text)}`;
        window.open(whatsappUrl, "_blank");
    }
}