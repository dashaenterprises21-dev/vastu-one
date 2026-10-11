/**
 * Vastu One — Cookie Consent
 */

(function() {
  'use strict';

  var STORAGE_KEY = 'vastu_cookie_consent';

  function hasConsent() {
    return localStorage.getItem(STORAGE_KEY) !== null;
  }

  function setConsent(value) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      value: value,
      timestamp: new Date().toISOString()
    }));
  }

  function createBanner() {
    var banner = document.createElement('div');
    banner.id = 'cookieBanner';
    banner.className = 'cookie-banner';
    banner.innerHTML = 
      '<div class="cookie-banner-title">🍪 Cookie Notice</div>' +
      '<div class="cookie-banner-text">' +
        'Hum cookies use karte hain aapka experience behtar banane ke liye. ' +
        'Essential cookies (login, security) mandatory hain. ' +
        'Analytics cookies optional hain. ' +
        'Read our <a href="/legal/cookies.html" target="_blank">Cookie Policy</a> aur ' +
        '<a href="/legal/privacy.html" target="_blank">Privacy Policy</a>.' +
      '</div>' +
      '<div class="cookie-banner-actions">' +
        '<button class="cookie-btn cookie-btn-accept" onclick="window.acceptCookies()">✅ Accept All</button>' +
        '<button class="cookie-btn cookie-btn-reject" onclick="window.rejectCookies()">Essential Only</button>' +
      '</div>';
    document.body.appendChild(banner);
    setTimeout(function() { banner.classList.add('show'); }, 500);
  }

  window.acceptCookies = function() {
    setConsent('all');
    var b = document.getElementById('cookieBanner');
    if (b) b.classList.remove('show');
    setTimeout(function() { if (b) b.remove(); }, 500);
    console.log('✅ All cookies accepted');
  };

  window.rejectCookies = function() {
    setConsent('essential');
    var b = document.getElementById('cookieBanner');
    if (b) b.classList.remove('show');
    setTimeout(function() { if (b) b.remove(); }, 500);
    console.log('✅ Only essential cookies');
  };

  if (!hasConsent()) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', createBanner);
    } else {
      createBanner();
    }
  }
})();
