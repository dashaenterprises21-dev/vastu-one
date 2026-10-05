// ═══ VASTU AI - DETAILED REPORT RENDERER ═══
const ELEMENT_MAP = {
    "Earth": "पृथ्वी", "Water": "जल", "Fire": "अग्नि",
    "Air": "वायु", "Space": "आकाश"
};

document.addEventListener("DOMContentLoaded", async () => {
    const pathParts = window.location.pathname.split("/");
    const reportId = pathParts[pathParts.length - 1];

    if (!reportId || reportId === "report") {
        document.getElementById("reportContent").innerHTML =
            "<div class='loading'>❌ रिपोर्ट ID नहीं मिली</div>";
        return;
    }

    try {
        const response = await fetch(`/api/report/data/${reportId}`);
        if (!response.ok) throw new Error("Report not found");
        const data = await response.json();
        renderReport(data);
    } catch (err) {
        document.getElementById("reportContent").innerHTML =
            `<div class='loading'>❌ रिपोर्ट नहीं मिली: ${err.message}</div>`;
    }
});

function buildChakraGrid(all_status, plan) {
    const statusMap = {};
    all_status.forEach(s => statusMap[s.pada] = s);

    const planMap = {};
    plan.forEach(p => planMap[`${p.row}-${p.col}`] = p.object);

    let html = '<div class="chakra-grid">';
    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            const pada = r * 9 + c + 1;
            const status = statusMap[pada] || {};
            const obj = planMap[`${r}-${c}`] || "";

            let zc;
            if (r < 3 && c < 3) zc = "NE";
            else if (r < 3 && c > 5) zc = "NW";
            else if (r > 5 && c < 3) zc = "SE";
            else if (r > 5 && c > 5) zc = "SW";
            else if (r < 3) zc = "N";
            else if (r > 5) zc = "S";
            else if (c < 3) zc = "W";
            else if (c > 5) zc = "E";
            else zc = "brahma";

            let cls = `zone-${zc}`;
            if (status.status === "defect") cls += " zone-defect";
            else if (status.status === "correct") cls += " zone-correct";

            const hindi = status.hindi ? status.hindi.substring(0, 2) : "—";
            const objShort = obj ? obj.substring(0, 4) : "";

            html += `<div class="chakra-cell ${cls}">
                <div>${hindi}</div>
                ${objShort ? `<div style="font-size:6px;opacity:0.8">${objShort}</div>` : ''}
            </div>`;
        }
    }
    html += '</div>';
    return html;
}

function renderReport(data) {
    const el = document.getElementById("reportContent");
    const d = data.analysis;
    const client = data.client_info || {};
    const fs = d.final_score;
    const da = d.devata_audit;
    const eb = d.element_balance;
    const ba = d.brahma_audit || {};
    const ds = d.direction_strength || { zones: [] };
    const ra = d.room_analysis || { rooms: [] };
    const remedies = d.remedies || [];

    let html = "";

    // ═══════════════════════════════════════
    // COVER
    // ═══════════════════════════════════════
    html += `
    <div class="report-header">
        <img src="/static/logo/vastu_logo.png" alt="Vastu One" class="report-logo">
        <h1>VASTU ONE</h1>
        <div class="subtitle">India Ka No.1 Vastu Engine</div>
        <div class="subtitle" style="margin-top:4px;">शास्त्र-आधारित वास्तु विश्लेषण</div>
        <div class="report-meta">
            <span><b>नाम:</b> ${client.name || "ग्राहक"}</span>
            <span><b>तारीख:</b> ${data.report_date}</span>
            <span><b>आईडी:</b> ${data.report_id}</span>
        </div>
    </div>`;

    // SCORE
    html += `
    <div class="score-hero">
        <div class="score-number">${fs.total_score}</div>
        <div class="score-max">/ 100</div>
        <div class="score-grade">${fs.grade}</div>
    </div>`;

    // ═══════════════════════════════════════
    // METHODOLOGY
    // ═══════════════════════════════════════
    html += `<div class="section"><h2>हमारी विधि (Methodology)</h2>
        <p>यह रिपोर्ट निम्नलिखित 7 चरणों में तैयार की गई है:</p>
        <div class="method-step"><span class="step-num">1</span> आपका plan (row, column, object) लिया जाता है</div>
        <div class="method-step"><span class="step-num">2</span> 81 पदों में map किया जाता है — <b>बृहत्संहिता अध्याय 53.45</b></div>
        <div class="method-step"><span class="step-num">3</span> 45 देवताओं से check किया जाता है — <b>समरांगण सूत्रधार अध्याय 39</b></div>
        <div class="method-step"><span class="step-num">4</span> 5 तत्वों का balance देखा जाता है — <b>मयमतम्</b></div>
        <div class="method-step"><span class="step-num">5</span> ब्रह्मस्थान का audit होता है — <b>बृहत्संहिता 53.67</b></div>
        <div class="method-step"><span class="step-num">6</span> शास्त्रीय नियम लागू होते हैं — हर दोष के लिए श्लोक प्रमाण के साथ</div>
        <div class="method-step"><span class="step-num">7</span> Action Plan बनाया जाता है — Priority के अनुसार</div>
    </div>`;

    // ═══════════════════════════════════════
    // EXECUTIVE SUMMARY
    // ═══════════════════════════════════════
    html += `<div class="section"><h2>कार्यकारी सारांश</h2>
        <table class="data-table">
        <thead><tr><th>घटक</th><th>स्कोर</th><th>वज़न</th><th>स्थिति</th></tr></thead>
        <tbody>
            <tr><td>देवता ऑडिट (45 देवता)</td><td>${fs.breakdown.devata_audit}</td><td>35%</td><td>${fs.breakdown.devata_audit >= 80 ? 'उत्तम' : fs.breakdown.devata_audit >= 60 ? 'मध्यम' : 'सुधार आवश्यक'}</td></tr>
            <tr><td>तत्व संतुलन (5 तत्व)</td><td>${fs.breakdown.element_balance}</td><td>20%</td><td>${fs.breakdown.element_balance >= 80 ? 'उत्तम' : fs.breakdown.element_balance >= 60 ? 'मध्यम' : 'सुधार आवश्यक'}</td></tr>
            <tr><td>ब्रह्मस्थान</td><td>${fs.breakdown.brahma_sthan}</td><td>25%</td><td>${fs.breakdown.brahma_sthan >= 80 ? 'उत्तम' : fs.breakdown.brahma_sthan >= 60 ? 'मध्यम' : 'सुधार आवश्यक'}</td></tr>
            <tr><td>दिशा शक्ति (16 ज़ोन)</td><td>${fs.breakdown.direction_strength}</td><td>20%</td><td>${fs.breakdown.direction_strength >= 80 ? 'उत्तम' : fs.breakdown.direction_strength >= 60 ? 'मध्यम' : 'सुधार आवश्यक'}</td></tr>
            <tr class="total"><td>कुल स्कोर</td><td>${fs.total_score}</td><td>100%</td><td>${fs.grade}</td></tr>
        </tbody></table>

        <h3>मुख्य निष्कर्ष</h3>
        <p>इस विश्लेषण में <b>${da.total_issues} दोष</b> और <b>${da.total_correct || 0} सही स्थान</b> पाए गए हैं।</p>`;

    if (da.issues && da.issues.length) {
        html += `<h3>⚠️ मुख्य दोष</h3>`;
        da.issues.forEach(issue => {
            html += `<p>• <b>${issue.hindi} (${issue.direction})</b> — ${issue.problem} — प्रभाव: ${issue.domain_affected.join(', ')}</p>`;
        });
    }

    if (da.positive_hits && da.positive_hits.length) {
        html += `<h3>✅ सही स्थान</h3>`;
        da.positive_hits.forEach(hit => {
            html += `<p>• <b>${hit.hindi} (${hit.direction})</b> — ${hit.object} सही जगह पर</p>`;
        });
    }
    html += `</div>`;

    // ═══════════════════════════════════════
    // 81 PADA VISUAL CHAKRA
    // ═══════════════════════════════════════
    html += `<div class="section"><h2>81 पद वास्तु चक्र</h2>
        <p>यह आपके plan का visual representation है — 9×9 ग्रिड में। हर cell एक देवता का क्षेत्र है।</p>
        ${buildChakraGrid(da.all_devatas_status || [], data.plan || [])}
        <div class="chakra-legend">
            <span><span class="legend-box zone-defect"></span> दोष</span>
            <span><span class="legend-box zone-correct"></span> सही</span>
            <span><span class="legend-box zone-brahma"></span> ब्रह्मस्थान</span>
            <span><span class="legend-box zone-NE"></span> ईशान</span>
            <span><span class="legend-box zone-SE"></span> आग्नेय</span>
            <span><span class="legend-box zone-SW"></span> नैऋत्य</span>
            <span><span class="legend-box zone-NW"></span> वायव्य</span>
        </div>
    </div>`;

    // ═══════════════════════════════════════
    // 45 DEVATAS STATUS TABLE
    // ═══════════════════════════════════════
    if (da.all_devatas_status && da.all_devatas_status.length) {
        html += `<div class="section"><h2>देवता Status Table</h2>
            <p>आपके plan की वस्तुएँ किस देवता के क्षेत्र में हैं — पूरा status।</p>
            <table class="data-table">
            <thead><tr><th>पद</th><th>देवता</th><th>दिशा</th><th>वस्तु</th><th>स्थिति</th><th>प्रभाव</th></tr></thead>
            <tbody>`;
        da.all_devatas_status.forEach(d => {
            const st = d.status === "defect" ? "दोष" : d.status === "correct" ? "सही" : "सामान्य";
            const cls = d.status === "defect" ? "row-defect" : d.status === "correct" ? "row-correct" : "";
            html += `<tr class="${cls}">
                <td>#${d.pada}</td>
                <td><b>${d.hindi}</b></td>
                <td>${d.direction}</td>
                <td>${d.object}</td>
                <td>${st}</td>
                <td>${(d.domain || []).join(', ')}</td>
            </tr>`;
        });
        html += `</tbody></table></div>`;
    }

    // ═══════════════════════════════════════
    // DIRECTION STRENGTH (16 Zones)
    // ═══════════════════════════════════════
    if (ds.zones && ds.zones.length) {
        html += `<div class="section"><h2>16 ज़ोन दिशा शक्ति</h2>
            <p>हर दिशा का score — 0 (कमज़ोर) से 100 (उत्तम)।</p>`;
        ds.zones.forEach(zone => {
            if (!zone.used) return;
            const statusCls = zone.status === 'excellent' ? 'green' : zone.status === 'good' ? 'blue' : zone.status === 'average' ? 'orange' : 'red';
            html += `<div class="card">
                <div class="card-header">
                    <span class="card-title">${zone.name} (${zone.zone})</span>
                    <span class="badge badge-${statusCls}">${zone.score}/100</span>
                </div>
                <div class="card-row"><b>तत्व:</b> ${zone.element} | <b>देवता:</b> ${zone.deity}</div>
                ${zone.objects && zone.objects.length ? `<div class="card-row"><b>वस्तुएँ:</b> ${zone.objects.join(', ')}</div>` : ''}
                ${zone.notes && zone.notes.length ? `<div class="card-row"><b>टिप्पणी:</b> ${zone.notes.join(' • ')}</div>` : ''}
            </div>`;
        });
        html += `</div>`;
    }

    // ═══════════════════════════════════════
    // ROOM-WISE ANALYSIS
    // ═══════════════════════════════════════
    if (ra.rooms && ra.rooms.length) {
        html += `<div class="section"><h2>कक्ष-वार विश्लेषण</h2>
            <p>आपके plan में <b>${ra.total_rooms_analyzed} कमरे/वस्तुएँ</b> मिलीं। इनमें <b>${ra.correct_placements} सही</b> और <b>${ra.defects} दोषपूर्ण</b> हैं।</p>`;
        ra.rooms.forEach(room => {
            const stCls = room.status === 'correct' ? 'green' : room.status === 'defect' ? 'red' : 'orange';
            const stTxt = room.status === 'correct' ? 'सही' : room.status === 'defect' ? 'दोष' : 'सामान्य';
            html += `<div class="card room">
                <div class="card-header">
                    <span class="card-title">${room.room_hindi} — ${room.zone}</span>
                    <span class="badge badge-${stCls}">${stTxt}</span>
                </div>
                <div class="card-row"><b>वस्तु:</b> ${room.object}</div>
                <div class="card-row"><b>इष्ट दिशाएँ:</b> ${room.best_directions.join(', ')}</div>
                <div class="card-row"><b>अशुभ दिशाएँ:</b> ${room.bad_directions.join(', ')}</div>
                <div class="card-row"><b>कारण:</b> ${room.reason}</div>
                ${room.shastra ? `<div class="shastra-ref">${room.shastra}</div>` : ''}
            </div>`;
        });
        html += `</div>`;
    }

    // ═══════════════════════════════════════
    // DETAILED DEFECTS
    // ═══════════════════════════════════════
    if (da.issues && da.issues.length) {
        html += `<div class="section"><h2>विस्तृत दोष विश्लेषण</h2>`;
        da.issues.forEach((issue, i) => {
            html += `<div class="card">
                <div class="card-header">
                    <span class="card-title">दोष #${i+1}: ${issue.hindi} (${issue.direction})</span>
                    <span class="badge badge-red">${issue.severity === 'high' ? 'गंभीर' : 'मध्यम'}</span>
                </div>
                <div class="card-row"><b>समस्या:</b> ${issue.problem}</div>
                <div class="card-row"><b>प्रभाव:</b> ${issue.domain_affected.join(', ')}</div>
                <div class="card-row"><b>पद संख्या:</b> #${issue.pada}</div>
                ${issue.shastra_reference ? `
                <div class="shastra-ref">
                    <b>शास्त्र प्रमाण (${issue.shastra_reference.source} ${issue.shastra_reference.chapter}.${issue.shastra_reference.verse}):</b><br>
                    ${issue.shastra_reference.meaning}
                </div>` : ''}
            </div>`;
        });
        html += `</div>`;
    }

    // ═══════════════════════════════════════
    // REMEDIES
    // ═══════════════════════════════════════
    if (remedies.length) {
        html += `<div class="section"><h2>शास्त्रोक्त उपाय</h2>`;
        remedies.forEach((r, i) => {
            html += `<div class="card remedy">
                <div class="card-header">
                    <span class="card-title">उपाय #${i+1}: ${r.hindi} (${r.devata})</span>
                    <span class="badge badge-blue">${r.direction}</span>
                </div>
                <div class="card-row"><b style="color:#10b981;">✅ करें:</b> ${r.remedy.positive_objects.join(', ')}</div>
                <div class="card-row"><b style="color:#ef4444;">❌ न करें:</b> ${r.remedy.avoid.join(', ')}</div>
                <div class="card-row"><b style="color:#3b82f6;">🎨 रंग:</b> ${r.remedy.color.join(', ')}</div>
                <div class="card-row"><b style="color:#8b5cf6;">💡 तत्व संतुलन:</b> ${r.remedy.element_balance.join(', ')}</div>
                <div class="mantra">🕉️ मंत्र: ${r.remedy.mantra}</div>
            </div>`;
        });
        html += `</div>`;
    }

    // ═══════════════════════════════════════
    // BRAHMASTHAN
    // ═══════════════════════════════════════
    if (ba.score !== undefined) {
        html += `<div class="section"><h2>ब्रह्मस्थान विश्लेषण</h2>
            <p>ब्रह्मस्थान — घर का केंद्र (पद #45) — सबसे पवित्र स्थान है। इसे खाली और स्वच्छ रखना शास्त्रों में अनिवार्य है।</p>
            <div class="card">
                <div class="card-header">
                    <span class="card-title">केंद्र में रखी वस्तु: ${ba.center_object || 'कुछ नहीं'}</span>
                    <span class="badge badge-${ba.score >= 80 ? 'green' : ba.score >= 50 ? 'orange' : 'red'}">स्कोर: ${ba.score}/100</span>
                </div>
                ${ba.shastra_reason ? `<div class="shastra-ref"><b>शास्त्र कारण:</b> ${ba.shastra_reason}</div>` : ''}
            </div>
            <h3>ब्रह्मस्थान में क्या रखें</h3>
            <div class="card">
                <div class="card-row"><b style="color:#10b981;">✅ करें:</b> खुला स्थान, प्रकाश, पूजा स्थल, तुलसी का पौधा</div>
                <div class="card-row"><b style="color:#ef4444;">❌ न करें:</b> शौचालय, भारी सामान, अग्नि, जल स्रोत, भंडारण, बिस्तर</div>
            </div>
        </div>`;
    }

    // ═══════════════════════════════════════
    // ELEMENTS BALANCE
    // ═══════════════════════════════════════
    if (eb.balance) {
        html += `<div class="section"><h2>पंच तत्व संतुलन</h2>
            <table class="data-table">
            <thead><tr><th>तत्व</th><th>संतुलन</th><th>स्थिति</th></tr></thead>
            <tbody>`;
        for (const [name, val] of Object.entries(eb.balance)) {
            const status = val < 0 ? 'कमज़ोर' : val > 3 ? 'प्रबल' : 'संतुलित';
            const cls = val < 0 ? 'row-defect' : val > 3 ? 'row-correct' : '';
            html += `<tr class="${cls}"><td><b>${ELEMENT_MAP[name] || name}</b></td><td>${val}</td><td>${status}</td></tr>`;
        }
        html += `</tbody></table>`;
        if (eb.weak_elements && eb.weak_elements.length) {
            html += `<h3>⚠️ कमज़ोर तत्व</h3>`;
            eb.weak_elements.forEach(el => {
                html += `<p>• <b>${ELEMENT_MAP[el] || el}</b> कमज़ोर है — इसका संतुलन ज़रूरी है।</p>`;
            });
        }
        html += `</div>`;
    }

    // ═══════════════════════════════════════
    // SHASTRA REFERENCES
    // ═══════════════════════════════════════
    html += `<div class="section"><h2>शास्त्र प्रमाण</h2>
        <p>इस रिपोर्ट में उपयोग किए गए शास्त्रीय स्रोत:</p>
        <div class="card">
            <div class="card-row"><b>📖 बृहत्संहिता (वराहमिहिर, 6वीं सदी)</b></div>
            <div class="card-row">वास्तु मंडल, 45 देवता, 81 पद, गृह-निर्माण नियम</div>
        </div>
        <div class="card">
            <div class="card-row"><b>📖 समरांगण सूत्रधार (राजा भोज, 11वीं सदी)</b></div>
            <div class="card-row">द्वार विधान, मर्म-वेध, दिशा प्रवा</div>
        </div>
        <div class="card">
            <div class="card-row"><b>📖 मयमतम् (मयमुनि)</b></div>
            <div class="card-row">आवासीय वास्तु, कक्ष योजना</div>
        </div>
        <div class="card">
            <div class="card-row"><b>📖 मानसार</b></div>
            <div class="card-row">वास्तु विश्वकोश — मंदिर, नगर, गृह</div>
        </div>`;

    if (da.issues && da.issues.length) {
        const withRef = da.issues.filter(i => i.shastra_reference);
        if (withRef.length) {
            html += `<h3>इस रिपोर्ट में उद्धृत श्लोक</h3>`;
            withRef.forEach(issue => {
                const ref = issue.shastra_reference;
                html += `<div class="card">
                    <div class="card-row"><b>${ref.source} — अध्याय ${ref.chapter}, श्लोक ${ref.verse}</b></div>
                    <div class="card-row"><i>"${ref.meaning}"</i></div>
                </div>`;
            });
        }
    }
    html += `</div>`;

    // ═══════════════════════════════════════
    // ACTION PLAN
    // ═══════════════════════════════════════
    html += `<div class="section"><h2>कार्य योजना (Action Plan)</h2>`;

    if (da.issues && da.issues.length) {
        const high = da.issues.filter(i => i.severity === 'high');
        if (high.length) {
            html += `<h3 style="color:#ef4444;">🔴 उच्च प्राथमिकता</h3>`;
            high.forEach(issue => {
                html += `<div class="action-item priority-high">
                    <b>उच्च</b> — ${issue.hindi} (${issue.direction}) — ${issue.problem}
                </div>`;
            });
        }
    }

    if (ba.score !== undefined && ba.score < 50) {
        html += `<div class="action-item priority-high">
            <b>उच्च</b> — ब्रह्मस्थान सुधार — केंद्र से भारी/अशुभ वस्तुएँ हटाएँ
        </div>`;
    }

    if (eb.weak_elements && eb.weak_elements.length) {
        html += `<h3 style="color:#f59e0b;">🟡 मध्यम प्राथमिकता</h3>`;
        eb.weak_elements.forEach(el => {
            html += `<div class="action-item priority-medium">
                <b>मध्यम</b> — ${ELEMENT_MAP[el] || el} तत्व को संतुलित करें — रंग, वस्तुएँ बदलें
            </div>`;
        });
    }

    html += `<h3 style="color:#10b981;">🟢 दीर्घकालिक सुझाव</h3>
        <div class="action-item priority-low">
            <b>निम्न</b> — नियमित रूप से 81 पद ग्रिड का पुनः मूल्यांकन करें
        </div>
        <div class="action-item priority-low">
            <b>निम्न</b> — बड़े बदलाव (निर्माण, विस्तार) से पहले वास्तु परामर्श लें
        </div>
    </div>`;

    // ═══════════════════════════════════════
    // CONCLUSION + ROLE
    // ═══════════════════════════════════════
    html += `<div class="section"><h2>निष्कर्ष और हमारी भूमिका</h2>`;

    if (fs.total_score >= 90) {
        html += `<p>आपका स्थान शास्त्रों के अनुसार <b>उत्तम</b> है। कोई बड़ा दोष नहीं मिला।</p>`;
    } else if (fs.total_score >= 70) {
        html += `<p>आपका स्थान <b>अच्छा</b> है, लेकिन कुछ सुधार संभव हैं।</p>`;
    } else if (fs.total_score >= 50) {
        html += `<p>आपके स्थान में <b>कुछ महत्वपूर्ण दोष</b> हैं। उपाय जल्दी करें।</p>`;
    } else {
        html += `<p><b>गंभीर दोष</b> पाए गए हैं। तुरंत विशेषज्ञ से परामर्श लें।</p>`;
    }

    html += `
    <div class="role-section">
        <h3>🕉️ हमारी भूमिका</h3>
        <p><b>Vastu AI एक शास्त्र-आधारित analysis tool है।</b> हमारा काम: बृहत्संहिता, समरांगण सूत्रधार, मयमतम् और मानसार — इन 4 प्रामाणिक ग्रंथों का ज्ञान AI के माध्यम से तेज़ी से आप तक पहुँचाना।</p>
        <p><b>हम क्या नहीं करते:</b> हम आपके व्यक्तिगत जीवन, भाग्य, या भविष्य की भविष्यवाणी नहीं करते। हम पेशेवर वास्तु परामर्श का विकल्प नहीं हैं।</p>
        <p><b>आपकी भूमिका:</b> यह रिपोर्ट एक <b>मार्गदर्शिका</b> है। किसी भी बड़े निर्णय (निर्माण, खरीद, विस्तार) से पहले इस रिपोर्ट को अपने architect या अनुभवी वास्तु विशेषज्ञ से verify ज़रूर करवाएँ।</p>
    </div>`;

    // CTA
    html += `
    <div class="cta">
        <h3>🕉️ व्यक्तिगत परामर्श चाहिए?</h3>
        <p>वास्तु विशेषज्ञ से 1:1 बात करें</p>
        <p><b>📞 व्हाट्सएप: +91-XXXXX-XXXXX</b></p>
        <p><b>📧 ईमेल: consult@vastuai.in</b></p>
        <p><b>🌐 वेबसाइट: vastuai.in</b></p>
    </div>`;

    // DISCLAIMER
    html += `<div class="disclaimer">
        <h3>कानूनी सूचना (Legal Notice)</h3>
        <p>यह रिपोर्ट बृहत्संहिता, समरांगण सूत्रधार, मयमतम् और मानसार जैसे प्राचीन शास्त्रों के सिद्धांतों पर आधारित है। यह केवल सूचनात्मक और शैक्षिक उद्देश्य के लिए है। Vastu AI, इसके संस्थापक, कर्मचारी और सहयोगी — किसी भी प्रत्यक्ष या अप्रत्यक्ष परिणाम, हानि या क्षति के लिए ज़िम्मेदार नहीं होंगे। सभी शास्त्रीय संदर्भ मूल ग्रंथों से लिए गए हैं और उनकी व्याख्या AI द्वारा की गई है।</p>
    </div>`;

    html += `</div>`;

    // FOOTER
    html += `<div class="report-footer">VASTU ONE — India Ka No.1 Vastu Engine</div>`;

    el.innerHTML = html;
}