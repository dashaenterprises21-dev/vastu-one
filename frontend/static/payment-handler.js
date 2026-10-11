/**
 * Vastu One — Payment Handler
 * Razorpay integration for premium report
 */

async function buyPremiumReport() {
  var btn = document.getElementById('buyPremiumBtn');
  var status = document.getElementById('paymentStatus');

  if (!window.vastuOneLastData) {
    alert('Pehle kundli analyze karein');
    return;
  }

  btn.disabled = true;
  btn.textContent = '⏳ Opening checkout...';

  try {
    // 1. Create order on backend
    var res = await fetch('/api/payments/kundli-payment?kundli_id=' + Date.now() + '&amount=505', {
      method: 'POST',
    });
    var data = await res.json();

    if (!data.success) {
      throw new Error('Order create failed');
    }

    var order = data.order;

    // 2. Open Razorpay checkout
    var options = {
      key: 'rzp_test_TkaNUKiP6i0BII',  // Your test key
      amount: order.amount,
      currency: order.currency,
      name: 'Vastu One',
      description: 'Premium Kundli PDF Report',
      order_id: order.id,
      handler: function(response) {
        // Payment success
        onPaymentSuccess(response, order);
      },
      prefill: {
        name: document.getElementById('name') ? document.getElementById('name').value : '',
      },
      theme: {
        color: '#6b1420',
      },
      modal: {
        ondismiss: function() {
          btn.disabled = false;
          btn.textContent = '💳 Buy Now 505';
        }
      }
    };

    var rzp = new Razorpay(options);
    rzp.open();

  } catch (err) {
    console.error('Payment error:', err);
    btn.disabled = false;
    btn.textContent = '💳 Buy Now 505';
    if (status) {
      status.style.display = 'block';
      status.style.background = 'rgba(248,113,113,0.15)';
      status.style.color = '#fca5a5';
      status.textContent = '❌ Payment failed: ' + err.message;
    }
  }
}

async function onPaymentSuccess(response, order) {
  var btn = document.getElementById('buyPremiumBtn');
  var status = document.getElementById('paymentStatus');

  try {
    // 1. Verify payment on backend
    var verifyRes = await fetch('/api/payments/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        razorpay_order_id: response.razorpay_order_id,
        razorpay_payment_id: response.razorpay_payment_id,
        razorpay_signature: response.razorpay_signature,
      }),
    });

    var verifyData = await verifyRes.json();

    if (verifyData.success) {
      // Success!
      btn.textContent = '✅ Payment Successful';
      btn.style.background = 'linear-gradient(135deg,#10b981,#059669)';
      btn.disabled = true;

      if (status) {
        status.style.display = 'block';
        status.style.background = 'rgba(16,185,129,0.15)';
        status.style.color = '#7ee0a0';
        status.innerHTML = '✅ <strong>Payment successful!</strong> Premium PDF unlock ho gaya.<br>' +
          '<button onclick="downloadPremiumPDF()" style="margin-top:12px;padding:12px 24px;background:linear-gradient(135deg,#e0b968,#d4a961);color:#2a0810;border:none;border-radius:8px;font-weight:700;cursor:pointer;">📄 Download Premium PDF</button>' +
          '<button onclick="shareOnWhatsApp()" style="margin-top:12px;margin-left:12px;padding:12px 24px;background:#25D366;color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;">💬 Share on WhatsApp</button>';
      }

      // Store payment info
      // Unlock premium sections
      if (typeof unlockPremium === 'function') {
        unlockPremium();
      }

      window.vastuOnePayment = {
        order_id: response.razorpay_order_id,
        payment_id: response.razorpay_payment_id,
        signature: response.razorpay_signature,
        premium: true,
      };

    } else {
      throw new Error('Verification failed');
    }
  } catch (err) {
    console.error('Verify error:', err);
    if (status) {
      status.style.display = 'block';
      status.style.background = 'rgba(248,113,113,0.15)';
      status.style.color = '#fca5a5';
      status.textContent = '❌ Verification failed. Contact support.';
    }
  }
}

function downloadPremiumPDF() {
  // Trigger existing PDF export
  if (window.vastuOneLastData && typeof exportToPDF === 'function') {
    exportToPDF(window.vastuOneLastData);
  }
}

function shareOnWhatsApp() {
  var text = encodeURIComponent('🕉️ Meri Kundli Report — Vastu One\n\n' +
    'Name: ' + (document.getElementById('name') ? document.getElementById('name').value : '') + '\n' +
    'DOB: ' + (document.getElementById('dob') ? document.getElementById('dob').value : '') + '\n\n' +
    'Vastu One se banwayi — vastuone.in');
  window.open('https://wa.me/?text=' + text, '_blank');
}

window.buyPremiumReport = buyPremiumReport;
window.downloadPremiumPDF = downloadPremiumPDF;
window.shareOnWhatsApp = shareOnWhatsApp;

console.log('✅ Payment handler loaded');
