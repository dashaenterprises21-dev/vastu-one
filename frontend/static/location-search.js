/**
 * Vastu One — Location Search with Lat/Lng Display
 * Type city → search → show exact coordinates → auto-fill
 */

const LOC_SEARCH = {
  debounceTimer: null,
  activeDropdown: null,
  currentResults: []
};

function locDebounce(fn, delay) {
  return function() {
    const args = arguments, ctx = this;
    clearTimeout(LOC_SEARCH.debounceTimer);
    LOC_SEARCH.debounceTimer = setTimeout(function() { fn.apply(ctx, args); }, delay);
  };
}

async function searchLocation(query) {
  if (!query || query.length < 2) return [];
  const url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(query) + '&limit=8&addressdetails=1';
  try {
    const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) return [];
    const data = await res.json();
    return data.map(function(item) {
      const addr = item.address || {};
      const city = addr.city || addr.town || addr.village || addr.hamlet || addr.county || addr.state_district || '';
      const state = addr.state || '';
      const country = addr.country || '';
      let label = '';
      if (city) label += city;
      if (state && state !== city) label += (label ? ', ' : '') + state;
      if (country && country !== state) label += (label ? ', ' : '') + country;
      if (!label) label = item.display_name || '';
      return {
        label: label,
        display: item.display_name || label,
        lat: parseFloat(item.lat),
        lng: parseFloat(item.lon),
        city: city,
        state: state,
        country: country
      };
    });
  } catch (e) {
    return [];
  }
}

function removeDropdown() {
  if (LOC_SEARCH.activeDropdown && LOC_SEARCH.activeDropdown.parentNode) {
    LOC_SEARCH.activeDropdown.parentNode.removeChild(LOC_SEARCH.activeDropdown);
  }
  LOC_SEARCH.activeDropdown = null;
}

function renderDropdown(input, results) {
  removeDropdown();
  if (!results || results.length === 0) return;

  const rect = input.getBoundingClientRect();
  const dd = document.createElement('div');
  dd.id = 'loc-search-dropdown';
  dd.style.cssText = 'position:fixed;z-index:99999;background:#1a1a24;border:1px solid #D4AF37;border-radius:8px;max-height:340px;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.5);font-family:Inter,sans-serif;';
  dd.style.left = rect.left + 'px';
  dd.style.top = (rect.bottom + 4) + 'px';
  dd.style.width = Math.max(rect.width, 320) + 'px';

  results.forEach(function(r) {
    const item = document.createElement('div');
    item.style.cssText = 'padding:10px 14px;cursor:pointer;border-bottom:1px solid #333;font-size:13px;color:#fff;';
    item.innerHTML = '<div style="font-weight:600;color:#D4AF37;">' + r.label + '</div>' +
      '<div style="font-size:11px;color:#4ade80;margin-top:3px;font-family:monospace;">📍 ' + r.lat.toFixed(6) + ', ' + r.lng.toFixed(6) + '</div>';
    item.onmouseenter = function() { item.style.background = 'rgba(212,175,55,0.15)'; };
    item.onmouseleave = function() { item.style.background = 'transparent'; };
    item.onclick = function() {
      selectLocation(input, r);
      removeDropdown();
    };
    dd.appendChild(item);
  });

  document.body.appendChild(dd);
  LOC_SEARCH.activeDropdown = dd;
}

function selectLocation(input, loc) {
  input.value = loc.label;
  input.setAttribute('data-lat', loc.lat);
  input.setAttribute('data-lng', loc.lng);
  input.setAttribute('data-city', loc.city);
  input.setAttribute('data-state', loc.state);
  input.setAttribute('data-country', loc.country);
  input.dataset.userSelected = 'true';

  // Update coordinates display
  updateCoordDisplay(input, loc);
  input.dispatchEvent(new Event('change', { bubbles: true }));
}

function updateCoordDisplay(input, loc) {
  // Find or create coord display for this input
  let display = document.getElementById('coord-display-' + (input.id || 'x'));
  if (!display) {
    display = document.createElement('div');
    display.id = 'coord-display-' + (input.id || 'x');
    display.style.cssText = 'margin-top:10px;padding:12px 16px;background:linear-gradient(135deg,rgba(212,175,55,0.12),rgba(212,175,55,0.04));border:1px solid rgba(212,175,55,0.3);border-radius:8px;font-family:monospace;';
    const wrapper = input.closest('div') || input.parentNode;
    wrapper.parentNode.insertBefore(display, wrapper.nextSibling);
  }
  display.innerHTML = 
    '<div style="font-size:10px;color:#D4AF37;letter-spacing:1.5px;margin-bottom:6px;font-family:Inter,sans-serif;">�� EXACT COORDINATES</div>' +
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">' +
    '<div><div style="font-size:10px;color:#888;font-family:Inter,sans-serif;">LATITUDE</div><div style="font-size:16px;color:#fff;font-weight:700;">' + loc.lat.toFixed(6) + '°</div></div>' +
    '<div><div style="font-size:10px;color:#888;font-family:Inter,sans-serif;">LONGITUDE</div><div style="font-size:16px;color:#fff;font-weight:700;">' + loc.lng.toFixed(6) + '°</div></div>' +
    '</div>' +
    '<div style="margin-top:8px;font-size:11px;color:#888;font-family:Inter,sans-serif;">' + (loc.city || '') + (loc.state ? ', ' + loc.state : '') + (loc.country ? ', ' + loc.country : '') + '</div>' +
    '<a href="https://www.openstreetmap.org/?mlat=' + loc.lat + '&mlon=' + loc.lng + '#map=13/' + loc.lat + '/' + loc.lng + '" target="_blank" style="display:inline-block;margin-top:8px;font-size:11px;color:#D4AF37;text-decoration:none;font-family:Inter,sans-serif;">🗺️ View on Map →</a>';
  display.style.display = 'block';
}

function attachLocationSearch(input) {
  if (input.dataset.locSearchAttached) return;
  input.dataset.locSearchAttached = 'true';
  input.autocomplete = 'off';

  const doSearch = locDebounce(async function() {
    const q = input.value.trim();
    if (q.length < 2) { removeDropdown(); return; }
    if (input.dataset.userSelected === 'true') {
      input.dataset.userSelected = 'false';
      return;
    }
    const results = await searchLocation(q);
    LOC_SEARCH.currentResults = results;
    renderDropdown(input, results);
  }, 400);

  input.addEventListener('input', function() {
    input.dataset.userSelected = 'false';
    input.removeAttribute('data-lat');
    input.removeAttribute('data-lng');
    const display = document.getElementById('coord-display-' + (input.id || 'x'));
    if (display) display.style.display = 'none';
    doSearch();
  });

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') removeDropdown();
    if (e.key === 'Enter' && LOC_SEARCH.activeDropdown) {
      e.preventDefault();
      const first = LOC_SEARCH.activeDropdown.querySelector('div');
      if (first) first.click();
    }
  });

  document.addEventListener('click', function(e) {
    if (LOC_SEARCH.activeDropdown && !LOC_SEARCH.activeDropdown.contains(e.target) && e.target !== input) {
      removeDropdown();
    }
  });

  console.log('✅ Location search attached to:', input.id || input.name);
}

function injectLocationSearch() {
  document.querySelectorAll('input').forEach(function(input) {
    if (input.dataset.gpsInjected) return;
    if (input.dataset.locSearchAttached) return;

    const name = (input.name || '').toLowerCase();
    const id = (input.id || '').toLowerCase();
    const placeholder = (input.placeholder || '').toLowerCase();
    const isBirthPlace = (
      name.includes('place') || name.includes('pob') || name.includes('birth') || name.includes('city') ||
      id.includes('place') || id.includes('pob') || id.includes('birth') || id.includes('city') ||
      placeholder.includes('place') || placeholder.includes('birth') || placeholder.includes('city') || placeholder.includes('जन्म स्थान')
    );
    if (isBirthPlace) attachLocationSearch(input);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectLocationSearch);
} else {
  injectLocationSearch();
}

// Expose for backend use
window.searchLocation = searchLocation;
window.attachLocationSearch = attachLocationSearch;
window.getBirthLocation = function(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return null;
  return {
    place: input.value,
    lat: input.getAttribute('data-lat'),
    lng: input.getAttribute('data-lng'),
    city: input.getAttribute('data-city'),
    state: input.getAttribute('data-state'),
    country: input.getAttribute('data-country')
  };
};

// ══════════════════════════════════════════
// FORCE INJECT — DOM ready hone ka wait karo
// ══════════════════════════════════════════
(function() {
  function tryInject() {
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      setTimeout(function() {
        if (typeof injectLocationSearch === 'function') {
          try { injectLocationSearch(); console.log('✅ Location search auto-injected'); }
          catch(e) { console.error('Inject error:', e); }
        }
      }, 100);
    } else {
      document.addEventListener('DOMContentLoaded', tryInject);
    }
  }
  tryInject();
  window.addEventListener('load', function() {
    if (typeof injectLocationSearch === 'function') {
      try { injectLocationSearch(); } catch(e) {}
    }
  });
})();
