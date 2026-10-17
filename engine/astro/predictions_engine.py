"""
VASTU ONE - Master Predictions Engine
100+ predictions from all astrological calculations
"""

from datetime import datetime
from engine.astro.complete_chart_engine import (
    calculate_complete_chart, calculate_vimshottari_dasha,
    calculate_transit, get_house, RASHIS
)
from engine.astro.yoga_detector import detect_all_yogas
from engine.astro.ashtakavarga_engine import analyze_ashtakavarga
from engine.astro.shadbala_engine import calculate_shadbala
from engine.astro.nakshatra_engine import analyze_nakshatra
from engine.astro.varshphal_engine import calculate_varshphal


COUNTRY_CHARTS = {
    "India": {"date": (1947, 8, 15), "time": 0.0, "lat": 28.6139, "lng": 77.2090, "name": "India"},
    "USA": {"date": (1776, 7, 4), "time": 12.0, "lat": 39.9526, "lng": -75.1652, "name": "USA"},
    "China": {"date": (1949, 10, 1), "time": 15.0, "lat": 39.9042, "lng": 116.4074, "name": "China"},
    "Russia": {"date": (1991, 12, 26), "time": 0.0, "lat": 55.7558, "lng": 37.6173, "name": "Russia"},
    "Pakistan": {"date": (1947, 8, 14), "time": 9.5, "lat": 24.8607, "lng": 67.0011, "name": "Pakistan"},
    "UK": {"date": (1801, 1, 1), "time": 0.0, "lat": 51.5074, "lng": -0.1278, "name": "UK"},
    "Israel": {"date": (1948, 5, 14), "time": 16.0, "lat": 32.0853, "lng": 34.7818, "name": "Israel"},
    "Ukraine": {"date": (1991, 8, 24), "time": 17.5, "lat": 50.4501, "lng": 30.5234, "name": "Ukraine"},
    "Japan": {"date": (1952, 4, 28), "time": 0.0, "lat": 35.6762, "lng": 139.6503, "name": "Japan"},
    "Germany": {"date": (1990, 10, 3), "time": 0.0, "lat": 52.5200, "lng": 13.4050, "name": "Germany"},
    "France": {"date": (1958, 10, 4), "time": 0.0, "lat": 48.8566, "lng": 2.3522, "name": "France"},
    "Brazil": {"date": (1822, 9, 7), "time": 0.0, "lat": -23.5505, "lng": -46.6333, "name": "Brazil"},
    "Australia": {"date": (1901, 1, 1), "time": 0.0, "lat": -33.8688, "lng": 151.2093, "name": "Australia"},
    "Canada": {"date": (1867, 7, 1), "time": 0.0, "lat": 45.4215, "lng": -75.6972, "name": "Canada"},
    "Saudi Arabia": {"date": (1932, 9, 23), "time": 0.0, "lat": 24.7136, "lng": 46.6753, "name": "Saudi Arabia"},
    "Iran": {"date": (1979, 4, 1), "time": 0.0, "lat": 35.6892, "lng": 51.3890, "name": "Iran"},
    "North Korea": {"date": (1948, 9, 9), "time": 0.0, "lat": 39.0392, "lng": 125.7625, "name": "North Korea"},
    "South Korea": {"date": (1948, 8, 15), "time": 0.0, "lat": 37.5665, "lng": 126.9780, "name": "South Korea"},
    "Nepal": {"date": (2008, 5, 28), "time": 0.0, "lat": 27.7172, "lng": 85.3240, "name": "Nepal"},
    "Sri Lanka": {"date": (1948, 2, 4), "time": 0.0, "lat": 6.9271, "lng": 79.8612, "name": "Sri Lanka"},
    "Bangladesh": {"date": (1971, 3, 26), "time": 0.0, "lat": 23.8103, "lng": 90.4125, "name": "Bangladesh"},
    "Afghanistan": {"date": (1919, 8, 19), "time": 0.0, "lat": 34.5553, "lng": 69.2075, "name": "Afghanistan"},
    "Turkey": {"date": (1923, 10, 29), "time": 0.0, "lat": 39.9334, "lng": 32.8597, "name": "Turkey"},
    "Egypt": {"date": (1922, 2, 28), "time": 0.0, "lat": 30.0444, "lng": 31.2357, "name": "Egypt"},
    "South Africa": {"date": (1994, 4, 27), "time": 0.0, "lat": -25.7479, "lng": 28.2293, "name": "South Africa"},
}


def get_predictions(country: str = "India", target_date: datetime = None):
    """Generate 100+ predictions from all calculations"""
    if target_date is None:
        target_date = datetime.now()
    
    if country not in COUNTRY_CHARTS:
        return {"error": f"Country not found: {country}"}
    
    data = COUNTRY_CHARTS[country]
    y, m, d = data["date"]
    
    birth = datetime(y, m, d)
    chart = calculate_complete_chart(y, m, d, data["time"], data["lat"], data["lng"])
    from engine.astro.planetary_deep_analysis import analyze_all_planets_deep
    planetary_deep = analyze_all_planets_deep(chart)
    dasha = calculate_vimshottari_dasha(chart, birth, target_date)
    transit = calculate_transit(chart, target_date)
    yogas = detect_all_yogas(chart)
    ashtaka = analyze_ashtakavarga(chart)
    shadbala = calculate_shadbala(chart)
    nakshatra = analyze_nakshatra(chart)
    
    # Annual chart
    varshphal = calculate_varshphal(chart, target_date.year)
    
    # ═══ GENERATE PREDICTIONS ═══
    predictions = {
        "country": country,
        "date": target_date.strftime("%Y-%m-%d"),
        "chart": {
            "ascendant": chart["ascendant"],
            "sun": chart["planets"]["Sun"],
            "moon": chart["planets"]["Moon"],
            "planets": chart["planets"],
        },
        "planetary_deep": planetary_deep,
        "dasha": dasha,
        "yogas": yogas,
        "ashtakavarga": {
            "strongest": ashtaka["strongest_signs"],
            "weakest": ashtaka["weakest_signs"],
            "total": ashtaka["total_points"],
        },
        "shadbala": {
            "ranking": shadbala["ranking"],
            "strongest": shadbala["strongest"],
            "weakest": shadbala["weakest"],
        },
        "nakshatra": nakshatra,
        "varshphal": {
            "year": varshphal["year"],
            "ascendant": varshphal["annual_chart"]["ascendant"],
            "muntha": varshphal["muntha"],
            "year_lord": varshphal["year_lord"],
        },
        "transit": transit,
        "predictions": [],
    }
    
    # ═══ GENERATE 100+ PREDICTIONS ═══
    preds = []
    
    # 1. Dasha-based predictions
    maha = dasha["mahadasha"]["lord"]
    antar = dasha["antardasha"]["lord"]
    prat = dasha["pratyantardasha"]["lord"]
    
    preds.append({
        "category": "Dasha",
        "title": f"Mahadasha: {maha}",
        "prediction": f"{maha} mahadasha active — {_dasha_effect(maha)}",
        "confidence": "High",
        "period": f"Until age {dasha['mahadasha']['end_age']}",
    })
    preds.append({
        "category": "Dasha",
        "title": f"Antardasha: {antar}",
        "prediction": f"{maha}-{antar} period — {_dasha_effect(antar)}",
        "confidence": "High",
        "period": "Current sub-period",
    })
    preds.append({
        "category": "Dasha",
        "title": f"Pratyantardasha: {prat}",
        "prediction": f"{maha}-{antar}-{prat} — {_dasha_effect(prat)}",
        "confidence": "Medium",
        "period": "Current micro-period",
    })
    
    # 2. Yoga-based predictions
    for y in yogas["auspicious"]:
        preds.append({
            "category": "Yoga",
            "title": y["name"],
            "prediction": y["effect"],
            "confidence": y["strength"],
        })
    
    for y in yogas["doshas"]:
        preds.append({
            "category": "Dosha",
            "title": y["name"],
            "prediction": y["effect"],
            "confidence": y["strength"],
        })
    
    # 3. Transit predictions
    for t in transit["planets"]:
        preds.append({
            "category": "Transit",
            "title": f"{t['planet']} in House {t['house']}",
            "prediction": f"{t['planet']} transiting {t['rashi']} ({t['nakshatra']} pada {t['pada']}) in house {t['house']} — {_house_effect(t['planet'], t['house'])}",
            "confidence": "Medium",
        })
    
    # 4. Ashtakavarga predictions
    for rashi, score in ashtaka["strongest_signs"]:
        preds.append({
            "category": "Ashtakavarga",
            "title": f"Strong: {rashi} ({score} points)",
            "prediction": f"{rashi} rashi has {score} points — strong area for {_rashi_meaning(rashi)}",
            "confidence": "High",
        })
    
    for rashi, score in ashtaka["weakest_signs"]:
        preds.append({
            "category": "Ashtakavarga",
            "title": f"Weak: {rashi} ({score} points)",
            "prediction": f"{rashi} rashi has only {score} points — vulnerable area for {_rashi_meaning(rashi)}",
            "confidence": "High",
        })
    
    # 5. Shadbala predictions
    preds.append({
        "category": "Shadbala",
        "title": f"Strongest: {shadbala['strongest']}",
        "prediction": f"{shadbala['strongest']} is strongest planet — {_planet_meaning(shadbala['strongest'])}",
        "confidence": "High",
    })
    preds.append({
        "category": "Shadbala",
        "title": f"Weakest: {shadbala['weakest']}",
        "prediction": f"{shadbala['weakest']} is weakest planet — {_planet_meaning(shadbala['weakest'])}",
        "confidence": "High",
    })
    
    # 6. Nakshatra predictions
    for planet, nak in nakshatra.items():
        preds.append({
            "category": "Nakshatra",
            "title": f"{planet} in {nak['nakshatra']}",
            "prediction": f"{planet} in {nak['nakshatra']} pada {nak['pada']} (deity: {nak['deity']}, shakti: {nak['shakti']})",
            "confidence": "Medium",
        })
    
    # 7. Varshphal predictions
    preds.append({
        "category": "Varshphal",
        "title": f"Year {varshphal['year']} — Muntha in {varshphal['muntha']['rashi']}",
        "prediction": f"Annual chart shows Muntha in {varshphal['muntha']['rashi']} — focus on {_rashi_meaning(varshphal['muntha']['rashi'])}",
        "confidence": "High",
    })
    preds.append({
        "category": "Varshphal",
        "title": f"Year Lord: {varshphal['year_lord']['planet']}",
        "prediction": f"Year lord is {varshphal['year_lord']['planet']} — {_planet_meaning(varshphal['year_lord']['planet'])}",
        "confidence": "High",
    })
    
    predictions["predictions"] = preds
    predictions["total_predictions"] = len(preds)
    
    return predictions


def _dasha_effect(planet):
    effects = {
        "Sun": "leadership, authority, government focus",
        "Moon": "public emotions, water, mass movements",
        "Mars": "military action, conflict, courage",
        "Mercury": "diplomacy, communication, trade",
        "Jupiter": "growth, wisdom, prosperity",
        "Venus": "luxury, arts, diplomacy",
        "Saturn": "discipline, delays, structural change",
        "Rahu": "sudden change, transformation, foreign",
        "Ketu": "spiritual, isolation, sudden events",
    }
    return effects.get(planet, "general effects")


def _house_effect(planet, house):
    effects = {
        1: "leadership, country",
        4: "land, earthquake, public",
        6: "war, enemies, military",
        7: "partnerships, war",
        8: "crisis, transformation",
        10: "government, politics",
        12: "foreign, losses",
    }
    return effects.get(house, "general effects")


def _planet_meaning(planet):
    meanings = {
        "Sun": "leadership, authority, government",
        "Moon": "public, emotions, water",
        "Mars": "military, aggression, courage",
        "Mercury": "communication, trade, diplomacy",
        "Jupiter": "wisdom, growth, prosperity",
        "Venus": "luxury, diplomacy, arts",
        "Saturn": "discipline, delays, structures",
        "Rahu": "transformation, foreign, sudden change",
        "Ketu": "spirituality, isolation, sudden events",
    }
    return meanings.get(planet, "general")


def _rashi_meaning(rashi):
    meanings = {
        "Mesh": "leadership, military, initiative",
        "Vrishabh": "economy, wealth, stability",
        "Mithun": "communication, media, diplomacy",
        "Kark": "land, earthquake, public",
        "Simha": "government, authority",
        "Kanya": "analysis, service, health",
        "Tula": "diplomacy, alliances, trade",
        "Vrishchik": "crisis, transformation, secrets",
        "Dhanu": "religion, foreign, law",
        "Makar": "governance, structure, discipline",
        "Kumbh": "technology, innovation, masses",
        "Meen": "spirituality, foreign, compassion",
    }
    return meanings.get(rashi, "general")


if __name__ == "__main__":
    result = get_predictions("India")
    print(f"=== {result['country']} PREDICTIONS ===")
    print(f"Date: {result['date']}")
    print(f"Total Predictions: {result['total_predictions']}")
    print()
    print("By Category:")
    categories = {}
    for p in result["predictions"]:
        cat = p["category"]
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in categories.items():
        print(f"  {cat}: {count} predictions")
    print()
    print("Top 10 Predictions:")
    for p in result["predictions"][:10]:
        print(f"  [{p['category']}] {p['title']}")
        print(f"      {p['prediction'][:100]}")
