// ═══ VASTU ONE — Plan Report ═══

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("vastu_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const reportId = window.location.pathname.split("/").pop();
    if (!reportId) {
        showError("Report ID नहीं मिली");
        return;
    }

    try {
        const response = await fetch(`/api/plan/report/${reportId}`, {
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) {
            if (response.status === 404) {
                showError("Report नहीं मिली");
            } else {
                showError("Error: " + response.status);
            }
            return;
        }

        const data = await response.json();
        renderReport(data);

    } catch (err) {
        console.error(err);
        showError("कुछ गड़बड़ हो गई");
    }
});

function showError(msg) {
    document.getElementById("reportContent").innerHTML = `
        <div style="text-align:center;padding:60px;">
            <div style="font-size:64px;">⚠️</div>
            <h2 style="color:#ef4444;">${msg}</h2>
        </div>
    `;
}

function renderReport(data) {
    const analysis = data.analysis;
    const planInfo = analysis.plan_info || {};

    let html = "";

    // HEADER
    html += `
    <div class="report-header">
        <div class="om-icon">🕉️</div>
        <h1>VASTU ANALYSIS REPORT</h1>
        <div class="report-meta">
            <span><b>Report ID:</b> ${data.report_id}</span>
            <span><b>Date:</b> ${new Date(data.created_at).toLocaleDateString('en-IN')}</span>
        </div>
    </div>`;

    // SCORE HERO
    html += `
    <div class="score-hero">
        <div class="score-circle">
            <div class="score-number">${analysis.overall_score}</div>
            <div class="score-max">/ 100</div>
        </div>
        <div class="score-grade">${analysis.grade}</div>
        <p class="score-text">आपके घर का वास्तु स्कोर</p>
    </div>`;

    // QUICK STATS
    html += `
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">${analysis.total_rooms}</div>
            <div class="stat-label">कुल Rooms</div>
        </div>
        <div class="stat-card correct">
            <div class="stat-value">${analysis.correct_rooms}</div>
            <div class="stat-label">✅ सही</div>
        </div>
        <div class="stat-card defect">
            <div class="stat-value">${analysis.defects}</div>
            <div class="stat-label">🟡 दोष</div>
        </div>
        <div class="stat-card severe">
            <div class="stat-value">${analysis.severe_defects}</div>
            <div class="stat-label">🔴 गंभीर</div>
        </div>
    </div>`;

    // PLAN INFO
    if (planInfo.compass_direction || planInfo.total_area) {
        html += `
        <div class="section">
            <h2>📐 Plan की जानकारी</h2>
            <div class="info-grid">
                ${planInfo.compass_direction ? `<div class="info-item"><span>Compass Direction</span><b>${planInfo.compass_direction}</b></div>` : ''}
                ${planInfo.total_area ? `<div class="info-item"><span>Total Area</span><b>${planInfo.total_area}</b></div>` : ''}
            </div>
        </div>`;
    }

    // ENTRY ANALYSIS
    if (analysis.entry_analysis) {
        const entry = analysis.entry_analysis;
        const isDefect = entry.status === "defect";
        html += `
        <div class="section">
            <h2>🚪 मुख्य द्वार (Main Entrance)</h2>
            <div class="card ${isDefect ? 'defect-card' : 'correct-card'}">
                <div class="card-header">
                    <span class="card-title">${entry.position}</span>
                    <span class="badge ${isDefect ? 'badge-red' : 'badge-green'}">
                        ${isDefect ? '🔴 दोष' : '✅ सही'}
                    </span>
                </div>
                ${isDefect && entry.shastra ? `
                <div class="shastra-ref">
                    <b>📖 ${entry.shastra.source} ${entry.shastra.chapter || ''}:</b>
                    ${entry.shastra.meaning || ''}
                </div>` : ''}
                ${isDefect && entry.remedies ? `
                <div class="remedies-box">
                    <b>💊 उपाय:</b>
                    <ul>
                        ${(entry.remedies.if_bad || []).map(r => `<li>${r}</li>`).join("")}
                    </ul>
                    ${entry.remedies.mantra ? `<div class="mantra">🕉️ ${entry.remedies.mantra}</div>` : ''}
                </div>` : ''}
            </div>
        </div>`;
    }

    // ROOMS ANALYSIS
    html += `
    <div class="section">
        <h2>🏠 Room-by-Room Analysis</h2>
        <div class="rooms-grid">`;

    analysis.results.forEach(room => {
        const statusClass = room.status === "correct" ? "correct-card" :
                           room.status === "defect" ? "defect-card" : "neutral-card";
        const badgeClass = room.status === "correct" ? "badge-green" :
                          room.status === "defect" ? "badge-red" : "badge-gray";

        html += `
        <div class="card ${statusClass}">
            <div class="card-header">
                <span class="card-title">
                    ${room.room_icon} ${room.name}
                    ${room.dimensions ? `<small>(${room.dimensions})</small>` : ''}
                </span>
                <span class="badge ${badgeClass}">${room.verdict}</span>
            </div>
            <div class="card-row"><b>Direction:</b> ${room.direction} — ${room.room_hindi}</div>
            <div class="card-row"><b>Best:</b> ${room.best_directions.join(', ')} | <b>Avoid:</b> ${room.bad_directions.join(', ')}</div>
            ${room.status === "defect" && room.shastra ? `
            <div class="shastra-ref">
                <b>📖 ${room.shastra.source}:</b>
                ${room.shastra.meaning || ''}
            </div>` : ''}
            ${room.status === "defect" && room.remedies ? `
            <div class="remedies-box">
                <b>💊 उपाय:</b>
                <ul>
                    ${(room.remedies.if_bad || []).map(r => `<li>${r}</li>`).join("")}
                </ul>
                ${room.remedies.mantra ? `<div class="mantra">🕉️ ${room.remedies.mantra}</div>` : ''}
            </div>` : ''}
        </div>`;
    });

    html += `</div></div>`;

    // CTA
    html += `
    <div class="cta">
        <h3>🕉️ व्यक्तिगत परामर्श चाहिए?</h3>
        <p>वास्तु विशेषज्ञ से 1:1 बात करें</p>
        <p><b>📞 व्हाट्सएप: +91-9890602105</b></p>
        <p><b>📧 ईमेल: dashaenterprises21@gmail.com</b></p>
    </div>`;

    // DISCLAIMER
    html += `
    <div class="disclaimer">
        <h3>कानूनी सूचना</h3>
        <p>यह रिपोर्ट बृहत्संहिता, समरांगण सूत्रधार, मयमतम् और मानसार जैसे प्राचीन शास्त्रों के सिद्धांतों पर आधारित है। Vastu AI किसी भी परिणाम की ज़िम्मेदारी नहीं लेता।</p>
    </div>`;

    document.getElementById("reportContent").innerHTML = html;
}