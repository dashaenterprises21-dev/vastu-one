/**
 * Vastu One — Premium Gate
 * Section 1-9 FREE, Section 10+ BLUR (except PDF)
 */

var GATE_DONE = false;

function applyPremiumGate() {
  if (GATE_DONE) return;

  var sections = Array.from(document.querySelectorAll('.section'));
  if (sections.length < 5) return;

  console.log('🔍 Total sections found:', sections.length);

  var CUTOFF_INDEX = 9;
  var count = 0;
  var pdfSkipped = 0;

  for (var i = CUTOFF_INDEX; i < sections.length; i++) {
    var sectionText = (sections[i].textContent || '').toLowerCase();
    
    // Skip PDF/Download/Report sections (always visible)
    if (sectionText.includes('download report') || 
        sectionText.includes('download pdf') ||
        sectionText.includes('pdf report') ||
        sectionText.includes('download')) {
      pdfSkipped++;
      continue;
    }
    
    if (!sections[i].classList.contains('premium-locked')) {
      sections[i].classList.add('premium-locked');
      count++;
    }
  }

  // Add banner before section 10
  if (!document.getElementById('premiumBanner') && sections[CUTOFF_INDEX]) {
    var b = document.createElement('div');
    b.id = 'premiumBanner';
    b.className = 'premium-banner';
    b.innerHTML =
      '<div style="font-size:36px;color:#d4a961;margin-bottom:16px;">💎</div>' +
      '<div class="premium-banner-title">Unlock Full Report</div>' +
      '<div class="premium-banner-sub">' +
      'Aapne abhi tak <strong>9 sections free</strong> mein dekhe.<br>' +
      'Aage ke <strong>sab sections + charts + PDF</strong> unlock karo — sirf 505.' +
      '</div>' +
      '<button class="premium-banner-btn" onclick="buyPremiumReport()">💳 Unlock Full Report 505</button>' +
      '<div class="premium-banner-features">' +
      '<span>✅ All Charts</span>' +
      '<span>✅ Predictions</span>' +
      '<span>✅ 46 Advanced Cards</span>' +
      '<span>✅ PDF Download</span>' +
      '<span>✅ WhatsApp Share</span>' +
      '</div>';
    sections[CUTOFF_INDEX].parentNode.insertBefore(b, sections[CUTOFF_INDEX]);
  }

  GATE_DONE = true;
  console.log('✅ Premium gate applied — ' + count + ' locked, ' + pdfSkipped + ' PDF skipped');
}

function unlockPremium() {
  document.querySelectorAll('.premium-locked').forEach(function(el) {
    el.classList.add('unlocked');
  });
  var b = document.getElementById('premiumBanner');
  if (b) b.style.display = 'none';
  console.log('✅ Premium unlocked');
}

// Hook analyzeKundli
var orig = window.analyzeKundli;
window.analyzeKundli = async function() {
  if (orig) await orig.apply(this, arguments);
  setTimeout(applyPremiumGate, 2000);
};

// Page load fallback (single check, no interval)
window.addEventListener('load', function() {
  setTimeout(function() {
    if (!GATE_DONE && document.querySelectorAll('.section').length > 5) {
      applyPremiumGate();
    }
  }, 3000);
});

window.applyPremiumGate = applyPremiumGate;
window.unlockPremium = unlockPremium;
console.log('✅ Premium gate loaded (no interval)');
