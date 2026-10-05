// VASTU ONE - Premium Report Page (Full Analysis)

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
        if (!data || !data.analysis) {
            showError("Report incomplete. Dobaara upload karein.");
            return;
        }
        renderReport(data);
    } catch (err) {
        console.error(err);
        showError("Report load nahi ho paayi. Dobaara try karein.");
    }
}

function showError(msg) {
    const el = document.getElementById("reportContent");
    if (!el) return;
    el.innerHTML = '<div style="text-align:center;padding:60px;">' +
        '<div style="font-size:64px;">Warning</div>' +
        '<h2 style="color:#ef4444;margin-top:20px;">' + msg + '</h2>' +
        '<a href="/plan-upload" style="display:inline-block;margin-top:30px;padding:14px 32px;background:linear-gradient(135deg,#f59e0b,#f97316);color:#000;text-decoration:none;border-radius:10px;font-weight:700;">Naya Plan Upload Karein</a>' +
        '</div>';
}

function renderReport(data) {
    const a = data.analysis || {};
    const uploadInfo = {
        upload_id: data.upload_id || "N/A",
        filename: data.filename || "N/A",
        uploaded_at: data.uploaded_at || new Date().toISOString()
    };

    let html = "";

    // ═══ HEADER ═══
    html += '<div class="report-header">';
    html += '<div class="om-icon">Om</div>';
    html += '<h1>VASTU ANALYSIS REPORT</h1>';
    html += '<div class="report-meta">';
    html += '<span><b>Report ID:</b> ' + uploadInfo.upload_id + '</span>';
    html += '<span><b>File:</b> ' + uploadInfo.filename + '</span>';
    html += '<span><b>Date:</b> ' + new Date(uploadInfo.uploaded_at).toLocaleDateString('en-IN') + '</span>';
    html += '</div></div>';

    // ═══ SCORE HERO ═══
    if (a.final_score) {
        const score = a.final_score.total_score || 0;
        const grade = a.final_score.grade || "N/A";
        html += '<div class="score-hero">';
        html += '<div class="score-circle"><div class="score-number">' + score + '</div><div class="score-max">/ 100</div></div>';
        html += '<div class="score-grade">' + grade + '</div>';
        html += '<div class="score-breakdown">';
        const bd = a.final_score.breakdown || {};
        for (const [key, val] of Object.entries(bd)) {
            html += '<div class="bd-item"><span>' + key.replace(/_/g, ' ') + '</span><b>' + val + '</b></div>';
        }
        html += '</div></div>';
    }

    // ═══ STATS GRID ═══
    html += '<div class="stats-grid">';
    html += '<div class="stat-card"><div class="stat-value">' + (a.rooms_detected || 0) + '</div><div class="stat-label">Rooms</div></div>';
    html += '<div class="stat-card defect"><div class="stat-value">' + (a.defect_count || 0) + '</div><div class="stat-label">Total Dosh</div></div>';
    html += '<div class="stat-card severe"><div class="stat-value">' + (a.high_severity_count || 0) + '</div><div class="stat-label">High Dosh</div></div>';
    html += '<div class="stat-card medium"><div class="stat-value">' + (a.medium_severity_count || 0) + '</div><div class="stat-label">Medium Dosh</div></div>';
    html += '</div>';

    // ═══ GRID OVERLAY ═══
    if (a.grid_overlay) {
        html += '<div class="section">';
        html += '<h2>81 Pad Grid Overlay</h2>';
        html += '<div class="image-viewer">';
        html += '<div class="image-controls">';
        html += '<button onclick="zoomIn()">+</button>';
        html += '<button onclick="zoomOut()">-</button>';
        html += '<button onclick="resetZoom()">R</button>';
        html += '</div>';
        html += '<div class="image-container" id="imageContainer">';
        html += '<img id="zoomImage" src="data:image/png;base64,' + a.grid_overlay + '" alt="Grid">';
        html += '</div>';
        html += '<div class="image-zoom-info" id="zoomInfo">100%</div>';
        html += '</div></div>';
    }

    // ═══ DOSH SECTION ═══
    if (a.defects && a.defects.length > 0) {
        html += '<div class="section">';
        html += '<h2>Dosh Detected (' + a.defects.length + ')</h2>';
        html += '<div class="defects-grid">';
        a.defects.forEach(d => {
            const sevClass = d.severity === 'high' ? 'sev-high' : (d.severity === 'medium' ? 'sev-medium' : 'sev-low');
            const sevLabel = d.severity === 'high' ? 'HIGH' : (d.severity === 'medium' ? 'MEDIUM' : 'LOW');
            html += '<div class="defect-card ' + sevClass + '">';
            html += '<div class="defect-header">';
            html += '<span class="defect-room">' + (d.room_hindi || d.room_type) + '</span>';
            html += '<span class="defect-sev ' + sevClass + '">' + sevLabel + '</span>';
            html += '</div>';
            html += '<div class="defect-zone">Zone: ' + d.zone + ' | Pada #' + d.pada + '</div>';
            html += '<div class="defect-problem"><b>Problem:</b> ' + (d.reason || '') + '</div>';
            html += '<div class="defect-shastra"><b>Shastra:</b> ' + (d.shastra || '') + '</div>';
            html += '<div class="defect-fix"><b>Fix:</b> ' + (d.best_directions || []).join(', ') + ' mein shift karein</div>';
            html += '</div>';
        });
        html += '</div></div>';
    }

    // ═══ REMEDIES SECTION ═══
    if (a.remedies && a.remedies.length > 0) {
        html += '<div class="section">';
        html += '<h2>5-Tier Remedies</h2>';
        a.remedies.forEach(r => {
            html += '<div class="remedy-card">';
            html += '<h3>' + r.defect + '</h3>';
            html += '<p class="remedy-problem">' + r.problem + '</p>';
            // Tier 1
            if (r.tier_1_simple && r.tier_1_simple.remedies) {
                html += '<div class="tier"><h4>Tier 1: Simple Fixes</h4><ul>';
                r.tier_1_simple.remedies.forEach(x => {
                    html += '<li>' + x.action + ' - ' + (x.cost || '') + '</li>';
                });
                html += '</ul></div>';
            }
            // Tier 2
            if (r.tier_2_space_surgery && r.tier_2_space_surgery.allowed) {
                html += '<div class="tier"><h4>Tier 2: Space Surgery (MahaVastu)</h4>';
                html += '<p>' + r.tier_2_space_surgery.instructions + '</p>';
                html += '</div>';
            }
            // Tier 3
            if (r.tier_3_pyramids) {
                html += '<div class="tier"><h4>Tier 3: Pyramids</h4>';
                html += '<p>' + r.tier_3_pyramids.placement + ' - ' + r.tier_3_pyramids.cost_estimate + '</p>';
                html += '</div>';
            }
            // Tier 4
            if (r.tier_4_pooja && r.tier_4_pooja.remedies) {
                html += '<div class="tier"><h4>Tier 4: Pooja & Mantra</h4><ul>';
                r.tier_4_pooja.remedies.forEach(x => {
                    html += '<li>' + x.action + ' - ' + (x.cost || '') + '</li>';
                });
                html += '</ul></div>';
            }
            html += '<div class="mantra-box"><b>Mantra:</b> ' + r.mantra + '</div>';
            html += '<div class="total-cost">Total: ' + r.total_cost_estimate + '</div>';
            html += '</div>';
        });
        html += '</div>';
    }

    // ═══ POOJA SECTION ═══
    if (a.pooja_plan && a.pooja_plan.plan && a.pooja_plan.plan.length > 0) {
        html += '<div class="section">';
        html += '<h2>Pooja Plan (' + a.pooja_plan.total_poojas + ')</h2>';
        html += '<div class="pooja-grid">';
        a.pooja_plan.plan.forEach(p => {
            html += '<div class="pooja-card">';
            html += '<h3>' + p.pooja + '</h3>';
            html += '<div class="pooja-mantra">' + p.mantra + '</div>';
            html += '<div class="pooja-detail">Count: ' + p.count + ' | Direction: ' + p.direction + '</div>';
            html += '<div class="pooja-detail">Timing: ' + p.timing + '</div>';
            html += '<div class="pooja-cost">' + p.cost + '</div>';
            html += '</div>';
        });
        html += '</div>';
        html += '<div class="pooja-total">Total Cost: ' + a.pooja_plan.total_cost + '</div>';
        html += '</div>';
    }

    // ═══ ENTRANCE SECTION ═══
    if (a.entrance_audit) {
        const e = a.entrance_audit;
        html += '<div class="section">';
        html += '<h2>Entrance Audit (32 Padas)</h2>';
        html += '<div class="entrance-card ' + (e.status === 'correct' ? 'correct' : 'defect') + '">';
        html += '<div class="entrance-name">' + e.name + ' (' + e.hindi + ')</div>';
        html += '<div class="entrance-dir">Direction: ' + e.direction + ' | Pada #' + e.pada + '</div>';
        html += '<div class="entrance-effect">' + e.effect + '</div>';
        html += '<div class="entrance-shastra">Shastra: ' + e.shastra + '</div>';
        html += '</div></div>';
    }

    // ═══ AYADI SECTION ═══
    if (a.ayadi) {
        const ay = a.ayadi;
        html += '<div class="section">';
        html += '<h2>Ayadi Shadvarga</h2>';
        html += '<div class="ayadi-grid">';
        html += '<div class="ayadi-item"><b>' + ay.aya + '</b><br>Aya</div>';
        html += '<div class="ayadi-item"><b>' + ay.vyaya + '</b><br>Vyaya</div>';
        html += '<div class="ayadi-item"><b>' + ay.rksa + '</b><br>Rksa</div>';
        html += '<div class="ayadi-item"><b>' + ay.yoni + '</b><br>Yoni</div>';
        html += '<div class="ayadi-item"><b>' + ay.vara + '</b><br>Vara</div>';
        html += '<div class="ayadi-item"><b>' + ay.tithi + '</b><br>Tithi</div>';
        html += '</div>';
        html += '<div class="ayadi-verdict">' + ay.verdict + '</div>';
        html += '</div>';
    }

    // ═══ CTA ═══
    html += '<div class="cta">';
    html += '<h3>Personal Consultation Chahiye?</h3>';
    html += '<p>Vastu expert se 1:1 baat karein</p>';
    html += '<p><b>WhatsApp: +91-9890602105</b></p>';
    html += '<p><b>Email: dashaenterprises21@gmail.com</b></p>';
    html += '</div>';

    document.getElementById("reportContent").innerHTML = html;
}

// ═══ ZOOM & PAN ═══
let currentZoom = 1;
let panX = 0, panY = 0;
let isDragging = false;
let startX = 0, startY = 0;

function zoomIn() { currentZoom = Math.min(currentZoom + 0.2, 5); applyTransform(); }
function zoomOut() { currentZoom = Math.max(currentZoom - 0.2, 0.5); applyTransform(); }
function resetZoom() { currentZoom = 1; panX = 0; panY = 0; applyTransform(); }

function applyTransform() {
    const img = document.getElementById('zoomImage');
    const info = document.getElementById('zoomInfo');
    if (!img) return;
    img.style.transform = 'translate(' + panX + 'px, ' + panY + 'px) scale(' + currentZoom + ')';
    if (info) info.textContent = Math.round(currentZoom * 100) + '%';
}

document.addEventListener('wheel', (e) => {
    if (e.target.id === 'zoomImage') {
        e.preventDefault();
        if (e.deltaY < 0) zoomIn(); else zoomOut();
    }
}, { passive: false });

document.addEventListener('mousedown', (e) => {
    if (e.target.id === 'zoomImage') {
        isDragging = true;
        startX = e.clientX - panX;
        startY = e.clientY - panY;
    }
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        applyTransform();
    }
});

document.addEventListener('mouseup', () => { isDragging = false; });
