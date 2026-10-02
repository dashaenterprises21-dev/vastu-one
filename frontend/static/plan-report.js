// ═══════════════════════════════════════════════════════════════
// VASTU ONE — Plan Report Page
// Reads localStorage data + renders report
// ═══════════════════════════════════════════════════════════════

document.addEventListener("DOMContentLoaded", () => {
    loadReport();
});

function loadReport() {
    try {
        const raw = localStorage.getItem("plan_analysis");
        if (!raw) {
            showError("Report not received. Pehle plan upload karein.");
            return;
        }

        const data = JSON.parse(raw);

        // Check if data has analysis
        if (!data || !data.analysis) {
            showError("Report incomplete hai. Dobaara upload karein.");
            return;
        }

        renderReport(data);

    } catch (err) {
        console.error("Report load error:", err);
        showError("Report load nahi ho paayi. Dobaara try karein.");
    }
}

function showError(msg) {
    const el = document.getElementById("reportContent");
    if (!el) return;
    el.innerHTML = `
        <div style="text-align:center;padding:60px;">
            <div style="font-size:64px;">⚠️</div>
            <h2 style="color:#ef4444;margin-top:20px;">${msg}</h2>
            <a href="/plan-upload" style="display:inline-block;margin-top:30px;padding:14px 32px;background:linear-gradient(135deg,#f59e0b,#f97316);color:#000;text-decoration:none;border-radius:10px;font-weight:700;">
                Naya Plan Upload Karein
            </a>
        </div>
    `;
}

function renderReport(data) {
    const analysis = data.analysis || {};
    const uploadInfo = {
        upload_id: data.upload_id || "N/A",
        filename: data.filename || data.original_filename || "N/A",
        uploaded_at: data.uploaded_at || new Date().toISOString()
    };

    let html = "";

    // HEADER
    html += `
    <div class="report-header">
        <div class="om-icon">🕉️</div>
        <h1>VASTU ANALYSIS REPORT</h1>
        <div class="report-meta">
            <span><b>Report ID:</b> ${uploadInfo.upload_id}</span>
            <span><b>File:</b> ${uploadInfo.filename}</span>
            <span><b>Date:</b> ${new Date(uploadInfo.uploaded_at).toLocaleDateString('en-IN')}</span>
        </div>
    </div>`;

    // STATS — Jo Data Mil Raha Hai
    const roomsDetected = analysis.rooms_detected || 0;
    const mappings = (analysis.room_mappings || []).length;
    const boundaryArea = analysis.boundary ? Math.round(analysis.boundary.area / 1000) : 0;

    html += `
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">${roomsDetected}</div>
            <div class="stat-label">�� Rooms Detected</div>
        </div>
        <div class="stat-card correct">
            <div class="stat-value">${mappings}</div>
            <div class="stat-label">🎯 Rooms Mapped</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${boundaryArea}K</div>
            <div class="stat-label">📐 Area (px)</div>
        </div>
    </div>`;

    // GRID OVERLAY
    if (analysis.grid_overlay) {
        html += `
        <div class="section">
            <h2>🎯 81 Pad Grid Overlay</h2>
            <p style="color:#666;">Aapke plan par 9x9 vastu grid lagaya gaya hai</p>
            <div style="text-align:center;background:#fff;padding:20px;border-radius:12px;margin-top:16px;">
                <img src="data:image/png;base64,${analysis.grid_overlay}" style="max-width:100%;border-radius:8px;" alt="Grid Overlay">
            </div>
        </div>`;
    }

    // ROOMS LIST
    if (analysis.rooms && analysis.rooms.length > 0) {
        html += `
        <div class="section">
            <h2>🏠 Detected Rooms</h2>
            <div class="rooms-grid">`;

        analysis.rooms.forEach((room, i) => {
            html += `
            <div class="card">
                <div class="card-header">
                    <span class="card-title">Room ${i+1}</span>
                </div>
                <div class="card-row"><b>Type:</b> ${room.type || "unknown"}</div>
                <div class="card-row"><b>Area:</b> ${Math.round(room.area || 0)} px²</div>
                <div class="card-row"><b>Center:</b> (${(room.center || [0,0]).join(", ")})</div>
            </div>`;
        });

        html += `</div></div>`;
    } else {
        html += `
        <div class="section">
            <h2>🏠 Detected Rooms</h2>
            <p style="color:#f59e0b;padding:20px;background:#fffbeb;border-radius:8px;">
                ⚠️ Koi room detect nahi hua. Plan clear nahi hai ya YOLO model available nahi hai.
            </p>
        </div>`;
    }

    // MAPPINGS
    if (analysis.room_mappings && analysis.room_mappings.length > 0) {
        html += `
        <div class="section">
            <h2>📊 Room → Vastu Position Mapping</h2>
            <div class="rooms-grid">`;

        analysis.room_mappings.forEach(m => {
            html += `
            <div class="card">
                <div class="card-header">
                    <span class="card-title">${m.room_type || "Room"} <span style="background:#f59e0b;color:#000;padding:2px 8px;border-radius:4px;font-size:12px;">${m.zone}</span></span>
                </div>
                <div class="card-row"><b>Pad:</b> #${m.pada}</div>
                <div class="card-row"><b>Position:</b> Row ${m.row}, Col ${m.col}</div>
            </div>`;
        });

        html += `</div></div>`;
    }

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
