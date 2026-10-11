/**
 * Vastu One — Location Picker with Map
 */

const LOC_PICKER = { map: null, marker: null, debounceTimer: null };

function ensureLeaflet(callback) {
  if (window.L) { callback(); return; }
  if (!document.querySelector('link[href*="leaflet"]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
  }
  if (!document.querySelector('script[src*="leaflet"]')) {
    const s = document.createElement('script');
    s.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    s.onload = callback;
    document.head.appendChild(s);
  } else { setTimeout(callback, 500); }
}

function initMap(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const map = L.map(containerId).setView([21.1458, 79.0882], 5);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap', maxZoom: 19
  }).addTo(map);
  LOC_PICKER.map = map;
  return map;
}

function setMapLocation(lat, lng, label) {
  if (!LOC_PICKER.map) return;
  const map = LOC_PICKER.map;
  if (LOC_PICKER.marker) map.removeLayer(LOC_PICKER.marker);
  LOC_PICKER.marker = L.marker([lat, lng]).addTo(map)
    .bindPopup('<b>' + (label || 'Location') + '</b><br>' + lat.toFixed(4) + ', ' + lng.toFixed(4))
    .openPopup();
  map.setView([lat, lng], 12);
}

async function searchLocationMap(query) {
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
      return { label: label, lat: parseFloat(item.lat), lng: parseFloat(item.lon), city: city, state: state, country: country };
    });
  } catch (e) { return []; }
}

function renderSuggestions(input, results, onSelect) {
  const old = document.getElementById('loc-map-suggestions');
  if (old) old.remove();
  if (!results || results.length === 0) return;

  const rect = input.getBoundingClientRect();
  const dd = document.createElement('div');
  dd.id = 'loc-map-suggestions';
  dd.style.cssText = 'position:fixed;z-index:99999;background:#1a1a24;border:1px solid #D4AF37;border-radius:8px;max-height:300px;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.5);font-family:Inter,sans-serif;';
  dd.style.left = rect.left + 'px';
  dd.style.top = (rect.bottom + 4) + 'px';
  dd.style.width = Math.max(rect.width, 340) + 'px';

  results.forEach(function(r) {
    const item = document.createElement('div');
    item.style.cssText = 'padding:10px 14px;cursor:pointer;border-bottom:1px solid #333;font-size:13px;color:#fff;';
    item.innerHTML = '<div style="font-weight:600;color:#D4AF37;">' + r.label + '</div>' +
      '<div style="font-size:11px;color:#4ade80;margin-top:3px;font-family:monospace;">📍 ' + r.lat.toFixed(4) + ', ' + r.lng.toFixed(4) + '</div>';
    item.onmouseenter = function() { item.style.background = 'rgba(212,175,55,0.15)'; };
    item.onmouseleave = function() { item.style.background = 'transparent'; };
    item.onclick = function() { onSelect(r); dd.remove(); };
    dd.appendChild(item);
  });
  document.body.appendChild(dd);

  setTimeout(function() {
    document.addEventListener('click', function closeDD(e) {
      if (!dd.contains(e.target) && e.target !== input) {
        dd.remove();
        document.removeEventListener('click', closeDD);
      }
    });
  }, 100);
}

function setupLocationPicker(inputId, mapContainerId, coordDisplayId) {
  const input = document.getElementById(inputId);
  const mapContainer = document.getElementById(mapContainerId);
  const coordDisplay = document.getElementById(coordDisplayId);
  if (!input) return;

  input.autocomplete = 'off';

  ensureLeaflet(function() {
    if (mapContainer) initMap(mapContainerId);
  });

  const doSearch = function() {
    clearTimeout(LOC_PICKER.debounceTimer);
    LOC_PICKER.debounceTimer = setTimeout(async function() {
      const q = input.value.trim();
      if (q.length < 2) return;
      const results = await searchLocationMap(q);
      renderSuggestions(input, results, function(loc) {
        input.value = loc.label;
        input.setAttribute('data-lat', loc.lat);
        input.setAttribute('data-lng', loc.lng);
        input.setAttribute('data-city', loc.city);
        input.setAttribute('data-state', loc.state);
        input.setAttribute('data-country', loc.country);

        setMapLocation(loc.lat, loc.lng, loc.label);

        if (coordDisplay) {
          coordDisplay.style.display = 'block';
          coordDisplay.innerHTML = 
            '<div style="font-size:10px;color:#D4AF37;letter-spacing:1.5px;margin-bottom:6px;">📍 EXACT COORDINATES</div>' +
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">' +
            '<div><div style="font-size:10px;color:#888;">LATITUDE</div><div style="font-size:15px;color:#fff;font-weight:700;">' + loc.lat.toFixed(6) + '°</div></div>' +
            '<div><div style="font-size:10px;color:#888;">LONGITUDE</div><div style="font-size:15px;color:#fff;font-weight:700;">' + loc.lng.toFixed(6) + '°</div></div>' +
            '</div>' +
            '<a href="https://www.openstreetmap.org/?mlat=' + loc.lat + '&mlon=' + loc.lng + '#map=13/' + loc.lat + '/' + loc.lng + '" target="_blank" style="display:inline-block;margin-top:8px;font-size:11px;color:#D4AF37;text-decoration:none;">🗺️ View on Map →</a>';
        }
      });
    }, 400);
  };

  input.addEventListener('input', doSearch);
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      const first = document.querySelector('#loc-map-suggestions > div');
      if (first) first.click();
    }
  });
}

window.setupLocationPicker = setupLocationPicker;
window.initMap = initMap;
