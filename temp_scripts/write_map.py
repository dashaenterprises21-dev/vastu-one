from pathlib import Path

js_content = """var WORLD_MAP = {
  map: null, markers: {}, countryData: {},
  riskColors: { "Very High": "#dc2626", "High": "#f59e0b", "Medium": "#eab308", "Low": "#10b981" }
};

var COUNTRY_COORDS = {
  "India": [28.6139, 77.2090], "USA": [38.9072, -77.0369], "China": [39.9042, 116.4074],
  "Russia": [55.7558, 37.6173], "Pakistan": [33.6844, 73.0479], "UK": [51.5074, -0.1278],
  "Israel": [31.7683, 35.2137], "Ukraine": [50.4501, 30.5234], "Japan": [35.6762, 139.6503],
  "Germany": [52.5200, 13.4050], "France": [48.8566, 2.3522], "Brazil": [-15.8267, -47.9218],
  "Australia": [-33.8688, 151.2093], "Canada": [45.4215, -75.6972],
  "Saudi Arabia": [24.7136, 46.6753], "Iran": [35.6892, 51.3890],
  "North Korea": [39.0392, 125.7625], "South Korea": [37.5665, 126.9780],
  "Nepal": [27.7172, 85.3240], "Sri Lanka": [6.9271, 79.8612],
  "Bangladesh": [23.8103, 90.4125], "Afghanistan": [34.5553, 69.2075],
  "Turkey": [39.9334, 32.8597], "Egypt": [30.0444, 31.2357], "South Africa": [-25.7479, 28.2293]
};

function initWorldMap() {
  if (WORLD_MAP.map) return WORLD_MAP.map;
  var container = document.getElementById("worldMap");
  if (!container) return null;
  var map = L.map("worldMap", { center: [20, 0], zoom: 2, minZoom: 2, maxZoom: 8, worldCopyJump: true });
  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: "OpenStreetMap", subdomains: "abcd", maxZoom: 19
  }).addTo(map);
  WORLD_MAP.map = map;
  return map;
}

async function loadMapCountries() {
  try {
    var res = await fetch("/api/world/master/countries");
    var data = await res.json();
    var countries = data.countries || [];
    var promises = countries.map(function(c) {
      return fetch("/api/world/master/predict/" + encodeURIComponent(c))
        .then(function(r) { return r.json(); })
        .catch(function() { return null; });
    });
    var results = await Promise.all(promises);
    countries.forEach(function(country, i) {
      var pred = results[i];
      if (!pred || !COUNTRY_COORDS[country]) return;
      WORLD_MAP.countryData[country] = pred;
      addCountryMarker(country, pred, COUNTRY_COORDS[country]);
    });
    console.log("Map loaded with", Object.keys(WORLD_MAP.markers).length, "markers");
  } catch (e) {
    console.error("Map load error:", e);
  }
}

function addCountryMarker(country, pred, coords) {
  var risk = (pred.metadata && pred.metadata.risk_level) || "Medium";
  var color = WORLD_MAP.riskColors[risk] || "#666";
  var marker = L.circleMarker(coords, {
    radius: 12, fillColor: color, color: "#fff", weight: 2, opacity: 1, fillOpacity: 0.8
  }).addTo(WORLD_MAP.map);
  var eq = pred.earthquake || {};
  var war = pred.war || {};
  var pol = pred.political || {};
  var popupHtml = "<div style=\\"min-width:240px;\\">" +
    "<div style=\\"font-size:16px;font-weight:700;color:" + color + ";margin-bottom:8px;\\">" + country + "</div>" +
    "<div style=\\"font-size:12px;margin-bottom:12px;\\">Risk: <strong style=\\"color:" + color + ";\\">" + risk + "</strong></div>" +
    (eq.highest_risk_zone ? "<div style=\\"font-size:12px;\\"><strong>Earthquake:</strong> " + eq.highest_risk_zone + "</div>" : "") +
    (war.risk ? "<div style=\\"font-size:12px;\\"><strong>War:</strong> " + war.risk + "</div>" : "") +
    (pol.probability ? "<div style=\\"font-size:12px;\\"><strong>Political:</strong> " + pol.probability + "</div>" : "") +
    "<button onclick=\\"openCountryFromMap('" + country + "')\\" style=\\"width:100%;margin-top:10px;padding:8px;background:#e0b968;color:#2a0810;border:none;border-radius:6px;font-weight:700;font-size:11px;cursor:pointer;\\">View Full Report</button>" +
    "</div>";
  marker.bindPopup(popupHtml, { maxWidth: 300 });
  marker.on("click", function() { marker.openPopup(); });
  WORLD_MAP.markers[country] = marker;
}

function openCountryFromMap(country) {
  if (typeof loadPrediction === "function") {
    loadPrediction(country);
    setTimeout(function() {
      var panel = document.getElementById("predictionPanel");
      if (panel) panel.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 300);
  }
}

window.initWorldMap = initWorldMap;
window.loadMapCountries = loadMapCountries;
window.openCountryFromMap = openCountryFromMap;
console.log("World Map loaded OK");
"""

p = Path("frontend/static/world-map.js")
p.write_text(js_content, encoding="utf-8")
print("SUCCESS - File written:", p.stat().st_size, "bytes")
