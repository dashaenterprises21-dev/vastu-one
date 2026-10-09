// ═══ VASTU ONE — PRICING & PAYMENT ═══

let currentBilling = "monthly";

// ═══ BILLING TOGGLE ═══
function toggleBilling(type, btn) {
    currentBilling = type;
    document.querySelectorAll(".toggle-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    document.querySelectorAll(".amount").forEach(el => {
        const price = type === "monthly" ? el.dataset.monthly : el.dataset.annual;
        el.textContent = Number(price).toLocaleString("en-IN");
    });

    updateBuyButtons();
}

function updateBuyButtons() {
    const packages = {
        bronze: { monthly: 999, annual: 799 },
        silver: { monthly: 2999, annual: 2399 },
        gold: { monthly: 9999, annual: 7999 },
        platinum: { monthly: 24999, annual: 19999 }
    };

    document.querySelectorAll(".btn-buy").forEach(btn => {
        const match = btn.className.match(/(\w+)-btn/);
        if (match && packages[match[1]]) {
            const price = packages[match[1]][currentBilling];
            const name = match[1].charAt(0).toUpperCase() + match[1].slice(1);
            btn.textContent = `Buy ${name} — ₹${price.toLocaleString("en-IN")}`;
        }
    });
}

// ═══ RAZORPAY PAYMENT ═══
async function buyPackage(packageName, price) {
    const token = localStorage.getItem("vastu_access_token");

    if (!token) {
        if (confirm("पहले login करें, फिर package खरीदें?\n\nLogin page पर जाएँ?")) {
            window.location.href = "/login.html";
        }
        return;
    }

    const prices = { bronze: 999, silver: 2999, gold: 9999, platinum: 24999 };
    const actualPrice = prices[packageName] || price;

    if (!confirm(`Package: ${packageName.toUpperCase()}\nPrice: ₹${actualPrice.toLocaleString("en-IN")}\n\nअभी pay करें?`)) {
        return;
    }

    // Show loading
    showLoading(true);

    try {
        // 1. Create order on backend
        const orderResponse = await fetch("/api/payment/create-order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ package: packageName })
        });

        const orderData = await orderResponse.json();

        if (!orderResponse.ok) {
            throw new Error(orderData.detail || "Order creation failed");
        }

        // 2. Open Razorpay checkout
        const options = {
            key: orderData.key_id,
            amount: orderData.amount,
            currency: "INR",
            name: "VASTU ONE",
            description: orderData.package_name,
            image: "/static/logo/vastu_logo.png",
            order_id: orderData.order_id,

            prefill: {
                name: orderData.user.name,
                email: orderData.user.email,
                contact: orderData.user.phone,
            },

            notes: {
                package: packageName,
                report_id: orderData.report_id,
            },

            theme: {
                color: "#f59e0b",
            },

            handler: async function (response) {
                // 3. Verify payment on backend
                await verifyPayment(response, packageName, token);
            },

            modal: {
                ondismiss: function () {
                    showLoading(false);
                    console.log("Payment cancelled");
                }
            }
        };

        const razorpay = new Razorpay(options);
        razorpay.on("payment.failed", function (response) {
            showLoading(false);
            alert("❌ Payment failed: " + response.error.description);
        });

        razorpay.open();

    } catch (err) {
        console.error(err);
        showLoading(false);
        alert("❌ Error: " + err.message);
    }
}

// ═══ VERIFY PAYMENT ═══
async function verifyPayment(razorpayResponse, packageName, token) {
    try {
        const response = await fetch("/api/payment/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                razorpay_order_id: razorpayResponse.razorpay_order_id,
                razorpay_payment_id: razorpayResponse.razorpay_payment_id,
                razorpay_signature: razorpayResponse.razorpay_signature,
                package: packageName
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Verification failed");
        }

        showLoading(false);
        showSuccessModal(data);

    } catch (err) {
        console.error(err);
        showLoading(false);
        alert("❌ Payment verification failed: " + err.message);
    }
}

// ═══ LOADING ═══
function showLoading(show) {
    let loader = document.getElementById("loader");
    if (!loader) {
        loader = document.createElement("div");
        loader.id = "loader";
        loader.innerHTML = `
            <div class="loader-overlay">
                <div class="loader-spinner"></div>
                <p>Processing...</p>
            </div>
        `;
        document.body.appendChild(loader);
    }
    loader.style.display = show ? "flex" : "none";
}

// ═══ SUCCESS MODAL ═══
function showSuccessModal(data) {
    const modal = document.createElement("div");
    modal.className = "success-modal-overlay";
    modal.innerHTML = `
        <div class="success-modal">
            <div class="success-icon">🎉</div>
            <h2>Payment Successful!</h2>
            <p>आपका ${data.package} package activate हो गया।</p>
            <div class="success-details">
                <p><b>Report ID:</b> ${data.report_id}</p>
                <p><b>Amount:</b> ₹${data.amount.toLocaleString("en-IN")}</p>
            </div>
            <p class="success-note">अब अपना plan upload करें — report generate हो जाएगी।</p>
            <div class="success-actions">
                <a href="/upload" class="btn-primary">📤 Plan Upload करें</a>
                <a href="/dashboard" class="btn-secondary">Dashboard</a>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// ═══ INIT ═══
document.addEventListener("DOMContentLoaded", () => {
    updateBuyButtons();
});