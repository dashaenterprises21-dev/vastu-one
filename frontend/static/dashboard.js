// ═══ VASTU ONE — Dashboard ═══

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("vastu_access_token");
    const userJson = localStorage.getItem("vastu_user");

    if (!token || !userJson) {
        window.location.href = "/login.html";
        return;
    }

    try {
        const user = JSON.parse(userJson);
        const initial = (user.name || "U").charAt(0).toUpperCase();

        document.getElementById("userAvatar").textContent = initial;
        document.getElementById("userAvatarLarge").textContent = initial;
        document.getElementById("userName").textContent = user.name || "User";
        document.getElementById("userEmail").textContent = user.email || "";
        document.getElementById("welcomeName").textContent = user.name || "User";

        // Set date
        const today = new Date();
        const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        document.getElementById("welcomeDate").textContent = today.toLocaleDateString('hi-IN', options);
    } catch (err) {
        console.error(err);
        window.location.href = "/login.html";
        return;
    }

    loadStats();
    loadRecentReports();
});

// ═══ SIDEBAR TOGGLE ═══
function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("open");
}

// ═══ USER MENU ═══
function toggleUserMenu() {
    document.getElementById("userDropdown").classList.toggle("show");
}

document.addEventListener("click", (e) => {
    const menu = document.getElementById("userDropdown");
    const userArea = document.querySelector(".navbar-user");
    if (menu && userArea && !userArea.contains(e.target)) {
        menu.classList.remove("show");
    }
});

// ═══ LOAD STATS ═══
async function loadStats() {
    try {
        const token = localStorage.getItem("vastu_access_token");
        const response = await fetch("/api/user/reports", {
            headers: { "Authorization": "Bearer " + token }
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) return;
        const data = await response.json();

        const reports = data.reports || [];
        const totalSpent = reports.reduce((sum, r) => sum + (r.price || 0), 0);

        // Fetch analysis details for avg score and defects
        let totalScore = 0;
        let scoreCount = 0;
        let totalDefects = 0;

        // Fetch first 5 reports for stats
        for (const report of reports.slice(0, 5)) {
            try {
                const detailRes = await fetch(`/api/plan/report/${report.report_id}`, {
                    headers: { "Authorization": "Bearer " + token }
                });

                if (detailRes.ok) {
                    const detail = await detailRes.json();
                    const analysis = detail.analysis;

                    if (analysis) {
                        // Try different score locations
                        const score = analysis.overall_score
                            || (analysis.combined_analysis && analysis.combined_analysis.combined_score)
                            || (analysis.final_score && analysis.final_score.total_score);

                        if (score) {
                            totalScore += score;
                            scoreCount++;
                        }

                        const defects = analysis.defects
                            || analysis.severe_defects
                            || (analysis.devata_audit && analysis.devata_audit.total_issues)
                            || 0;

                        totalDefects += defects;
                    }
                }
            } catch (e) {
                // Skip if report detail not available
            }
        }

        const avgScore = scoreCount > 0 ? (totalScore / scoreCount).toFixed(1) : "—";

        document.getElementById("statReports").textContent = reports.length;
        document.getElementById("statSpent").textContent = "₹" + totalSpent.toLocaleString("en-IN");
        document.getElementById("statAvgScore").textContent = avgScore;
        document.getElementById("statDefects").textContent = totalDefects;
        document.getElementById("reportCount").textContent = reports.length;

    } catch (err) {
        console.error(err);
    }
}

// ═══ LOAD RECENT REPORTS ═══
async function loadRecentReports() {
    const tbody = document.getElementById("reportsBody");

    try {
        const token = localStorage.getItem("vastu_access_token");
        const response = await fetch("/api/user/reports", {
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) return;
        const data = await response.json();

        if (!data.reports || data.reports.length === 0) {
            return; // Empty state in HTML
        }

        tbody.innerHTML = "";
        data.reports.slice(0, 5).forEach(report => {
            const tr = document.createElement("tr");
            const isPaid = report.payment_status === "paid";
            const viewUrl = `/plan-report/${report.report_id}`;

            const date = report.created_at
                ? new Date(report.created_at).toLocaleDateString('hi-IN', {
                    day: '2-digit', month: 'short', year: 'numeric'
                  })
                : "—";

            tr.innerHTML = `
                <td><b>${report.report_id}</b></td>
                <td>${(report.package || 'silver').charAt(0).toUpperCase() + (report.package || 'silver').slice(1)}</td>
                <td>₹${report.price || 0}</td>
                <td><span class="status-badge ${isPaid ? 'paid' : 'pending'}">${isPaid ? '✅ Paid' : '⏳ Pending'}</span></td>
                <td>${date}</td>
                <td><a href="${isPaid ? viewUrl : '#'}" class="view-link">${isPaid ? 'देखें →' : '—'}</a></td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error(err);
    }
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



// ═══ SEARCH FUNCTIONALITY ═══
const searchInput = document.querySelector(".search-box input");
if (searchInput) {
    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase().trim();
        filterReports(query);
    });

    // ⌘K / Ctrl+K shortcut
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "k") {
            e.preventDefault();
            searchInput.focus();
        }
    });
}

function filterReports(query) {
    const rows = document.querySelectorAll("#reportsBody tr");
    let visibleCount = 0;

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (!query || text.includes(query)) {
            row.style.display = "";
            visibleCount++;
        } else {
            row.style.display = "none";
        }
    });

    // Show "no results" message
    const tbody = document.getElementById("reportsBody");
    const existing = tbody.querySelector(".no-results-row");

    if (visibleCount === 0 && query && !existing) {
        const tr = document.createElement("tr");
        tr.className = "no-results-row";
        tr.innerHTML = `
            <td colspan="6" style="text-align: center; padding: 40px; color: var(--text-dim);">
                🔍 "${query}" के लिए कोई result नहीं मिला
            </td>
        `;
        tbody.appendChild(tr);
    } else if (existing && visibleCount > 0) {
        existing.remove();
    }
}

// ═══ NOTIFICATIONS ═══
async function loadNotifications() {
    try {
        const token = localStorage.getItem("vastu_access_token");
        const response = await fetch("/api/user/reports", {
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) return;
        const data = await response.json();
        const reports = data.reports || [];
        const recent = reports.slice(0, 3);

        const notifDot = document.querySelector(".notif-dot");
        if (notifDot) {
            notifDot.style.display = recent.length > 0 ? "block" : "none";
        }

        const notifBtn = document.querySelector(".icon-btn[title='Notifications']");
        if (notifBtn) {
            notifBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                showNotifications(recent);
            });
        }
    } catch (err) {
        console.error("Notifications error:", err);
    }
}

function showNotifications(reports) {
    // Remove existing
    const existing = document.querySelector(".notif-panel");
    if (existing) {
        existing.remove();
        return;
    }

    const panel = document.createElement("div");
    panel.className = "notif-panel";
    panel.style.cssText = `
        position: fixed;
        top: 76px;
        right: 20px;
        background: var(--card);
        border: 1px solid var(--border-bright);
        border-radius: 14px;
        padding: 8px;
        min-width: 320px;
        max-width: 400px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        z-index: 200;
    `;

    if (reports.length === 0) {
        panel.innerHTML = `
            <div style="padding: 20px; text-align: center; color: var(--text-dim); font-size: 13px;">
                🔔 कोई नई सूचना नहीं
            </div>
        `;
    } else {
        panel.innerHTML = `
            <div style="padding: 12px 14px; border-bottom: 1px solid var(--border); font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); font-weight: 700;">
                🔔 हाल की सूचनाएँ
            </div>
            ${reports.map(r => `
                <a href="/plan-report/${r.report_id}" style="display: flex; gap: 12px; padding: 12px 14px; text-decoration: none; color: var(--text); border-radius: 8px; transition: background 0.2s;" onmouseover="this.style.background='rgba(245,158,11,0.06)'" onmouseout="this.style.background='transparent'">
                    <span style="font-size: 20px;">📄</span>
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-size: 13px; font-weight: 600; color: var(--gold-bright); margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            ${r.report_id}
                        </div>
                        <div style="font-size: 11px; color: var(--text-dim);">
                            ${r.package ? r.package.toUpperCase() : 'Report'} • ${r.payment_status === 'paid' ? '✅ Paid' : '⏳ Pending'}
                        </div>
                    </div>
                </a>
            `).join("")}
            <div style="padding: 8px 14px; border-top: 1px solid var(--border); text-align: center;">
                <a href="/reports" style="color: var(--gold); font-size: 12px; font-weight: 600; text-decoration: none;">
                    सब देखें →
                </a>
            </div>
        `;
    }

    document.body.appendChild(panel);

    // Close on outside click
    setTimeout(() => {
        document.addEventListener("click", function closePanel(e) {
            if (!panel.contains(e.target) && !e.target.closest(".icon-btn")) {
                panel.remove();
                document.removeEventListener("click", closePanel);
            }
        });
    }, 100);
}

// ═══ CALL ON LOAD ═══
document.addEventListener("DOMContentLoaded", () => {
    loadNotifications();
});