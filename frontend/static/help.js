// VASTU ONE — Help / FAQ

const FAQ_DATA = [
    {
        category: "general",
        question: "VASTU ONE क्या है?",
        answer: "<b>VASTU ONE</b> भारत का पहला शास्त्र-आधारित वास्तु विश्लेषण system है। हम बृहत्संहिता, समरांगण सूत्रधार, मयमतम् और मानसार जैसे प्राचीन ग्रंथों के आधार पर AI से आपके घर/office का complete वास्तु विश्लेषण करते हैं।"
    },
    {
        category: "general",
        question: "ये कैसे काम करता है?",
        answer: "3 simple steps:<ul><li><b>Step 1:</b> अपना floor plan upload करें (image/PDF/photo)</li><li><b>Step 2:</b> AI आपके plan को पढ़कर rooms detect करेगा</li><li><b>Step 3:</b> 45 देवताओं + 81 पद + शास्त्र प्रमाण से analysis मिलेगा</li></ul>पूरी report 2-3 मिनट में तैयार हो जाती है।"
    },
    {
        category: "general",
        question: "क्या मेरा data safe है?",
        answer: "बिल्कुल। <b>हम आपका data किसी को नहीं बेचते, न share करते हैं।</b> सारा data encrypted है (AES-256), और आप कभी भी अपना account delete कर सकते हैं। DPDP Act 2023 compliant हैं।"
    },
    {
        category: "plan",
        question: "कौन-सी file format support है?",
        answer: "हम ये formats support करते हैं:<ul><li>PNG, JPG, JPEG, WEBP (max 10 MB)</li><li>Hand-drawn plan की photo भी चलेगी</li><li>Architect का PDF plan — उसकी photo लेकर upload करें</li></ul>"
    },
    {
        category: "plan",
        question: "Plan कैसा होना चाहिए?",
        answer: "<b>Best results के लिए:</b><ul><li>Plan clear और readable हो</li><li>Room names visible हों (BEDROOM, KITCHEN, etc.)</li><li>Compass/North arrow दिखे</li><li>Dimensions लिखे हों (12'x10')</li><li>Top-down view हो (किसी angle से photo न लें)</li></ul>"
    },
    {
        category: "plan",
        question: "क्या मैं manually rooms add कर सकता हूँ?",
        answer: "हाँ! अगर AI कुछ rooms miss कर दे, तो आप <b>Chakra Overlay</b> page पर जाकर manually rooms रख सकते हैं। हर room का type और direction आप खुद set कर सकते हैं।"
    },
    {
        category: "report",
        question: "Report में क्या-क्या मिलता है?",
        answer: "हर report में:<ul><li><b>Overall Score</b> (0-100) + Grade</li><li><b>Room-by-Room Analysis</b> — हर room का direction + status</li><li><b>दोष Detection</b> — कौन-सा room कहाँ गलत</li><li><b>शास्त्र प्रमाण</b> — हर दोष का श्लोक (बृहत्संहिता/मयमतम्)</li><li><b>Non-Demolition उपाय</b> — बिना तोड़-फोड़ solutions</li><li><b>मंत्र + रंग</b> — हर उपाय के साथ</li><li><b>PDF Download</b> — print के लिए</li></ul>"
    },
    {
        category: "report",
        question: "Report कितने time में बनती है?",
        answer: "AI analysis में <b>30-60 seconds</b> लगते हैं। फिर report page खुल जाती है जहाँ आप:<ul><li>Screen पर पूरी report देख सकते हैं</li><li>PDF download कर सकते हैं (Ctrl+P)</li><li>WhatsApp पर share कर सकते हैं</li></ul>"
    },
    {
        category: "report",
        question: "क्या report बार-बार download कर सकते हैं?",
        answer: "हाँ! <b>Lifetime access</b> है। अपने dashboard में जाएँ → \"मेरी रिपोर्ट\" → जो भी report चाहिए उस पर \"देखें\" दबाएँ।"
    },
    {
        category: "payment",
        question: "Payment कैसे करें?",
        answer: "हम <b>Razorpay</b> use करते हैं — India का सबसे trusted payment gateway। Options:<ul><li>UPI (PhonePe, GPay, Paytm)</li><li>Debit/Credit Card</li><li>Net Banking</li><li>Wallet</li></ul>Payment 100% secure है।"
    },
    {
        category: "payment",
        question: "कौन-से packages हैं?",
        answer: "4 packages:<ul><li><b>🥉 Bronze — ₹999</b> — Basic report, 5 दोष, 5 उपाय</li><li><b>🥈 Silver — ₹2,999</b> — 15-page detailed, 81 पद, PDF download</li><li><b>🥇 Gold — ₹9,999</b> — 30-page, कक्ष-वार, 5-year roadmap</li><li><b>💎 Platinum — ₹24,999</b> — 50-page + 1:1 consultation + 1 साल support</li></ul>"
    },
    {
        category: "payment",
        question: "क्या refund मिलता है?",
        answer: "हाँ! <b>7 दिन के अंदर full refund</b> अगर report से संतुष्ट नहीं हैं। बस WhatsApp पर message करें: +91 98906 02105"
    },
    {
        category: "vastu",
        question: "45 देवता क्या हैं?",
        answer: "<b>81 पद वास्तु मंडल</b> में 45 देवता बैठे हैं:<ul><li><b>32 बाहरी</b> — शिखी, इंद्र, यम, वरुण, सोम आदि</li><li><b>13 भीतरी</b> — ब्रह्मा (केंद्र), मित्र, आर्यमा, विवस्वान आदि</li></ul>हर देवता का अपना क्षेत्र, direction, और असर है। हम हर room को 45 देवताओं से verify करते हैं।"
    },
    {
        category: "vastu",
        question: "ब्रह्मस्थान क्या है?",
        answer: "<b>ब्रह्मस्थान</b> घर का केंद्र है (पद #45) — सबसे पवित्र स्थान। शास्त्रों के अनुसार इसे <b>खाली और स्वच्छ</b> रखना चाहिए। अगर यहाँ शौचालय, भारी सामान, या अग्नि है तो गंभीर दोष माना जाता है।"
    },
    {
        category: "vastu",
        question: "\"South entry खराब\" सच है?",
        answer: "<b>नहीं, ये गलत धारणा है।</b> बृहत्संहिता 53.71 के अनुसार दक्षिण का <b>4th pada (गृहक्षत)</b> मुख्य द्वार के लिए <b>BEST</b> है। इससे धन, वंश, और पशु वृद्धि होती है। हम यही सच बताते हैं — शास्त्र प्रमाण के साथ।"
    },
    {
        category: "vastu",
        question: "क्या remedies तोड़-फोड़ के बिना हैं?",
        answer: "हाँ! <b>100% non-demolition remedies।</b> हम कभी नहीं कहते \"दीवार तोड़ो\" या \"किचन shift करो\"। हम बताते हैं:<ul><li>कौन-सा रंग use करें</li><li>कौन-सी वस्तु कहाँ रखें</li><li>कौन-सा मंत्र जपें</li><li>कौन-सा यंत्र स्थापित करें</li></ul>"
    }
];

let currentCategory = "all";
let currentSearch = "";

document.addEventListener("DOMContentLoaded", () => {
    renderFAQ();
});

// ═══ RENDER FAQ ═══
function renderFAQ() {
    const container = document.getElementById("faqList");
    let filtered = FAQ_DATA;

    if (currentCategory !== "all") {
        filtered = filtered.filter(f => f.category === currentCategory);
    }

    if (currentSearch) {
        const q = currentSearch.toLowerCase();
        filtered = filtered.filter(f =>
            f.question.toLowerCase().includes(q) ||
            f.answer.toLowerCase().includes(q)
        );
    }

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="faq-item">
                <div class="faq-question" style="justify-content: center;">
                    <h3 style="text-align: center;">कोई सवाल नहीं मिला — WhatsApp पर पूछें</h3>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = "";
    filtered.forEach((faq, i) => {
        const item = document.createElement("div");
        item.className = "faq-item";
        item.innerHTML = `
            <div class="faq-question" onclick="toggleFAQ(this)">
                <h3>${faq.question}</h3>
                <span class="faq-toggle">+</span>
            </div>
            <div class="faq-answer">
                <div class="faq-answer-content">${faq.answer}</div>
            </div>
        `;
        container.appendChild(item);
    });
}

// ═══ TOGGLE FAQ ═══
function toggleFAQ(el) {
    const item = el.parentElement;
    item.classList.toggle("open");
}

// ═══ FILTER CATEGORY ═══
function filterCategory(cat, btn) {
    currentCategory = cat;
    document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    renderFAQ();
}

// ═══ SEARCH ═══
function searchFAQ() {
    currentSearch = document.getElementById("faqSearch").value.trim();
    renderFAQ();
}

// ═══ SIDEBAR TOGGLE ═══
function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("open");
}