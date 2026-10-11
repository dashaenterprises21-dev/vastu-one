/**
 * Vastu One — Premium Gate
 * Section 1-9 FREE, Section 10+ BLUR
 */

var GATE_DONE = false;

function applyPremiumGate() {
  if (GATE_DONE) return;

  var sections = Array.from(document.querySelectorAll('.section'));
  if (sections.length < 5) return;

  console.log('🔍 Total sections found:', sections.length);

  // Lock all sections from index 9 onwards (0-based index 9 = 10th section)
  var CUTOFF_INDEX = 9;
  var count = 0;

  for (var i = CUTOFF_INDEX; i < sections.length; i++) {
    if (!sections[i].classList.contains('premium-locked')) {
      sections[i].classList.add('premium-locked');
      count++;
    }
  }

  // Add banner before section 10 (index 9)
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
  console.log('✅ Premium gate applied — ' + count + ' sections locked (from #' + (CUTOFF_INDEX + 1) + ')');

  // Log section names
  sections.forEach(function(s, i) {
    var t = s.querySelector('.section-title');
    var title = t ? t.textContent.trim().substring(0, 30) : '(no title)';
    var locked = s.classList.contains('premium-locked');
    console.log('  ' + (i+1) + ': ' + (locked ? '🔒' : '✅') + ' ' + title);
  });
}

function unlockPremium() {
  document.querySelectorAll('.premium-locked').forEach(function(el) {
    el.classList.add('unlocked');
  });
  var b = document.getElementById('premiumBanner');
  if (b) b.style.display = 'none';
  console.log('✅ Premium unlocked — all sections visible');
}

// Hook analyzeKundli
var orig = window.analyzeKundli;
window.analyzeKundli = async function() {
  if (orig) await orig.apply(this, arguments);
  setTimeout(applyPremiumGate, 2000);
  setTimeout(applyPremiumGate, 4000);
};

// Page load fallback
setTimeout(function() {
  if (document.querySelectorAll('.section').length > 5) applyPremiumGate();
}, 3000);

// Interval fallback
var iv = setInterval(function() {
  if (GATE_DONE) { clearInterval(iv); return; }
  if (document.querySelectorAll('.section').length > 5) applyPremiumGate();
}, 2000);

window.applyPremiumGate = applyPremiumGate;
window.unlockPremium = unlockPremium;
console.log('✅ Premium gate loaded (cutoff: section 10)');
