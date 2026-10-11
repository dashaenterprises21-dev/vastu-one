/**
 * Vastu One — GPS Birth Place
 * Get exact location via browser GPS API
 * Reverse geocode to city name
 */

const GPS_STATE = {
  isLocating: false,
  lastLocation: null
};

/**
 * Get current location via browser GPS
 */
async function getCurrentLocation() {
  return new Promise(function(resolve, reject) {
    if (!navigator.geolocation) {
      reject(new Error('GPS not supported by this browser'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      function(pos) {
        resolve({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          accuracy: pos.coords.accuracy
        });
      },
      function(err) {
        let msg = 'Location error';
        if (err.code === 1) msg = 'Permission denied';
        else if (err.code === 2) msg = 'Position unavailable';
        else if (err.code === 3) msg = 'Timeout';
        reject(new Error(msg));
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
    );
  });
}

/**
 * Reverse geocode lat/lng to city name
 * Uses OpenStreetMap Nominatim (free, no API key)
 */
async function reverseGeocode(lat, lng) {
  const url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lng + '&zoom=10&addressdetails=1';
  try {
    const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) throw new Error('Geocode failed');
    const data = await res.json();
    const addr = data.address || {};
    const city = addr.city || addr.town || addr.village || addr.county || addr.state_district || '';
    const state = addr.state || '';
    const country = addr.country || '';
    return {
      city: city,
      state: state,
      country: country,
      displayName: data.display_name || (city + ', ' + state + ', ' + country),
      fullAddress: data.display_name || ''
    };
  } catch (e) {
    return {
      city: 'Unknown',
      state: '',
      country: '',
      displayName: lat.toFixed(4) + ', ' + lng.toFixed(4),
      fullAddress: lat.toFixed(4) + ', ' + lng.toFixed(4)
    };
  }
}

/**
 * Main handler — get location + reverse geocode + fill input
 */
async function useGPSLocation(inputId, buttonId, statusId) {
  if (GPS_STATE.isLocating) return;

  const input = document.getElementById(inputId);
  const button = document.getElementById(buttonId);
  const status = document.getElementById(statusId);
  if (!input || !button) return;

  GPS_STATE.isLocating = true;
  const originalText = button.innerHTML;

  try {
    button.innerHTML = '📍 Getting location...';
    button.disabled = true;
    if (status) {
      status.style.display = 'block';
      status.innerHTML = '⏳ GPS se location le rahe hain... Please allow permission.';
      status.style.color = '#D4AF37';
    }

    const loc = await getCurrentLocation();

    if (status) status.innerHTML = '🌐 Address dhundh rahe hain...';
    const geo = await reverseGeocode(loc.lat, loc.lng);

    // Fill input
    const placeValue = geo.city ? (geo.city + (geo.state ? ', ' + geo.state : '') + (geo.country ? ', ' + geo.country : '')) : geo.displayName;
    input.value = placeValue;

    // Store lat/lng as data attributes
    input.setAttribute('data-lat', loc.lat);
    input.setAttribute('data-lng', loc.lng);
    input.setAttribute('data-accuracy', loc.accuracy);

    GPS_STATE.lastLocation = { lat: loc.lat, lng: loc.lng, geo: geo };

    if (status) {
      status.innerHTML = '✅ Location set: ' + placeValue + ' <span style="color:#888;">(±' + Math.round(loc.accuracy) + 'm accuracy)</span>';
      status.style.color = '#22c55e';
      setTimeout(function() { status.style.display = 'none'; }, 5000);
    }

    button.innerHTML = '✅ ' + originalText.replace(/[^\w\s]/g, '').trim();
    setTimeout(function() {
      button.innerHTML = originalText;
      button.disabled = false;
    }, 2000);

  } catch (err) {
    if (status) {
      status.innerHTML = '❌ ' + err.message + '. Please type location manually.';
      status.style.color = '#ef4444';
      setTimeout(function() { status.style.display = 'none'; }, 6000);
    }
    button.innerHTML = originalText;
    button.disabled = false;
  } finally {
    GPS_STATE.isLocating = false;
  }
}

/**
 * Auto-detect GPS field in any form and inject button
 */
function injectGPSButton() {
  // Find all inputs that look like birth place
  const inputs = document.querySelectorAll('input');
  inputs.forEach(function(input) {
    const name = (input.name || '').toLowerCase();
    const id = (input.id || '').toLowerCase();
    const placeholder = (input.placeholder || '').toLowerCase();

    const isBirthPlace = (
      name.includes('place') || name.includes('pob') || name.includes('birth') ||
      id.includes('place') || id.includes('pob') || id.includes('birth') ||
      placeholder.includes('place') || placeholder.includes('birth') || placeholder.includes('जन्म स्थान')
    );

    if (isBirthPlace && !input.dataset.gpsInjected) {
      input.dataset.gpsInjected = 'true';

      const wrapper = document.createElement('div');
      wrapper.style.cssText = 'position:relative;display:flex;gap:8px;align-items:center;width:100%;';

      // Move input into wrapper
      input.parentNode.insertBefore(wrapper, input);
      wrapper.appendChild(input);
      input.style.flex = '1';

      // GPS button
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.id = 'gps-btn-' + (input.id || Math.random().toString(36).substr(2, 9));
      btn.innerHTML = '📍 GPS';
      btn.title = 'Use my current location';
      btn.style.cssText = 'background:linear-gradient(135deg,#D4AF37,#B8941F);color:#000;border:none;padding:12px 18px;border-radius:8px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap;transition:all 0.2s;flex-shrink:0;';
      btn.onmouseenter = function() { btn.style.transform = 'translateY(-1px)'; btn.style.boxShadow = '0 4px 12px rgba(212,175,55,0.4)'; };
      btn.onmouseleave = function() { btn.style.transform = 'translateY(0)'; btn.style.boxShadow = 'none'; };
      wrapper.appendChild(btn);

      // Status div
      const status = document.createElement('div');
      status.id = 'gps-status-' + (input.id || Math.random().toString(36).substr(2, 9));
      status.style.cssText = 'display:none;margin-top:6px;font-size:11px;padding:6px 10px;border-radius:6px;background:rgba(212,175,55,0.08);';
      wrapper.parentNode.insertBefore(status, wrapper.nextSibling);

      // Attach handler
      btn.onclick = function() {
        useGPSLocation(input.id, btn.id, status.id);
      };

      console.log('✅ GPS button injected for input:', input.id || input.name);
    }
  });
}

// Auto-inject DISABLED — manual GPS buttons only
// (document.readyState === 'loading') ? document.addEventListener('DOMContentLoaded', injectGPSButton) : injectGPSButton();

// Also expose to window
window.useGPSLocation = useGPSLocation;
window.injectGPSButton = injectGPSButton;
window.getCurrentLocation = getCurrentLocation;
window.reverseGeocode = reverseGeocode;
