from pathlib import Path

code = '''"""
VASTU ONE - Master Prediction Engine
Integrates all 6 layers of astrological analysis
"""

from datetime import datetime
from typing import Dict, Any

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, calculate_vimshottari_dasha
)
from engine.astro.planetary_deep_analysis import analyze_all_planets_deep
from engine.astro.complete_dasha_engine import CompleteVimshottariDasha
from engine.astro.complete_yoga_engine import detect_all_yogas_complete
from engine.astro.ashtakavarga_transit_engine import analyze_transit_with_ashtakavarga
from engine.astro.complete_varshphal_engine import calculate_varshphal_full
from engine.astro.nadi_bhrigu_engine import analyze_nadi_bhrigu_complete
from engine.astro.ashtakavarga_engine import analyze_ashtakavarga
from engine.astro.shadbala_engine import calculate_shadbala
from engine.astro.nakshatra_engine import analyze_nakshatra


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


def get_master_prediction(country: str = "India", target_date: datetime = None) -> Dict:
    """Get complete master prediction with all 6 layers"""
    if target_date is None:
        target_date = datetime.now()
    
    if country not in COUNTRY_CHARTS:
        return {"error": f"Country not found: {country}"}
    
    data = COUNTRY_CHARTS[country]
    y, m, d = data["date"]
    
    # Layer 0: Base chart
    chart = calculate_complete_chart(y, m, d, data["time"], data["lat"], data["lng"])
    birth = datetime(y, m, d)
    
    # Layer 1: Planetary Deep Analysis
    planetary_deep = analyze_all_planets_deep(chart)
    
    # Layer 2: Complete Dasha (5 levels)
    dasha_engine = CompleteVimshottariDasha(chart, birth)
    complete_dasha = dasha_engine.get_all_levels(target_date)
    
    # Layer 3: 100+ Yogas
    yogas_complete = detect_all_yogas_complete(chart)
    
    # Layer 4: Ashtakavarga + Transit
    transit_ashtaka = analyze_transit_with_ashtakavarga(chart, target_date)
    
    # Layer 5: Varshphal (3 years)
    varshphal_2026 = calculate_varshphal_full(chart, 2026)
    varshphal_2027 = calculate_varshphal_full(chart, 2027)
    varshphal_2028 = calculate_varshphal_full(chart, 2028)
    
    # Layer 6: Nadi/Bhrigu
    nadi_bhrigu = analyze_nadi_bhrigu_complete(chart)
    
    # Additional: Shadbala, Ashtakavarga, Nakshatra
    shadbala = calculate_shadbala(chart)
    ashtakavarga = analyze_ashtakavarga(chart)
    nakshatra = analyze_nakshatra(chart)
    
    return {
        "country": country,
        "date": target_date.strftime("%Y-%m-%d"),
        "birth_data": data,
        
        # Layer 0: Base
        "chart": {
            "ascendant": chart["ascendant"],
            "planets": chart["planets"],
            "birth": chart["birth"],
        },
        
        # Layer 1: Planetary Deep
        "planetary_deep": planetary_deep,
        
        # Layer 2: Complete Dasha
        "complete_dasha": complete_dasha,
        
        # Layer 3: Yogas
        "yogas_complete": yogas_complete,
        
        # Layer 4: Ashtakavarga + Transit
        "transit_ashtakavarga": transit_ashtaka,
        
        # Layer 5: Varshphal
        "varshphal": {
            "2026": varshphal_2026,
            "2027": varshphal_2027,
            "2028": varshphal_2028,
        },
        
        # Layer 6: Nadi/Bhrigu
        "nadi_bhrigu": nadi_bhrigu,
        
        # Additional
        "shadbala": shadbala,
        "ashtakavarga": {
            "total": ashtakavarga["total_points"],
            "strongest": ashtakavarga["strongest_signs"],
            "weakest": ashtakavarga["weakest_signs"],
        },
        "nakshatra": nakshatra,
        
        # Meta
        "total_predictions": (
            len(yogas_complete["yogas"]) +
            len(planetary_deep["planets"]) * 5 +
            len(complete_dasha["levels"]) * 3 +
            len(transit_ashtaka["transit_analysis"]) * 2 +
            len(nadi_bhrigu["karmic_debts"]) * 3
        ),
        "layers_analyzed": 6,
    }


if __name__ == "__main__":
    result = get_master_prediction("India")
    
    print("=" * 70)
    print("MASTER PREDICTION - INDIA")
    print("=" * 70)
    print(f"Date: {result['date']}")
    print(f"Total Predictions: {result['total_predictions']}")
    print(f"Layers Analyzed: {result['layers_analyzed']}")
    print()
    
    print("=== LAYER 1: PLANETARY DEEP ===")
    for planet, data in list(result["planetary_deep"]["planets"].items())[:3]:
        print(f"  {planet}: {data['rashi']} {data['degree']} deg | Avastha: {data['avastha']['state']} | Saptavargaja: {data['saptavargaja_bala']['percentage']}%")
    print()
    
    print("=== LAYER 2: COMPLETE DASHA (5 LEVELS) ===")
    for level_name, level in result["complete_dasha"]["levels"].items():
        print(f"  {level_name.upper()}: {level['planet']} | {level['start_date']} to {level['end_date']}")
    print()
    
    print("=== LAYER 3: YOGAS ===")
    print(f"  Total: {result['yogas_complete']['total_yogas']}")
    print(f"  Auspicious: {len(result['yogas_complete']['auspicious'])}")
    print(f"  Doshas: {len(result['yogas_complete']['doshas'])}")
    print()
    
    print("=== LAYER 4: ASHTAKAVARGA + TRANSIT ===")
    print(f"  Overall Verdict: {result['transit_ashtakavarga']['overall_verdict']}")
    print(f"  Positive: {result['transit_ashtakavarga']['positive_count']}")
    print(f"  Negative: {result['transit_ashtakavarga']['negative_count']}")
    print()
    
    print("=== LAYER 5: VARSHPHAL ===")
    for year, v in result["varshphal"].items():
        print(f"  {year}: Muntha {v['muntha']['rashi']} | Year Lord {v['year_lord']['planet']}")
    print()
    
    print("=== LAYER 6: NADI/BHRIGU ===")
    print(f"  Nadi: {result['nadi_bhrigu']['nadi_karma'].get('nadi', '')}")
    print(f"  Past Life: {result['nadi_bhrigu']['nadi_karma'].get('past_life', '')}")
    print(f"  Karmic Debts: {len(result['nadi_bhrigu']['karmic_debts'])}")
    print(f"  Spiritual Level: {result['nadi_bhrigu']['spiritual_evolution']['level']}")
'''

Path("engine/astro/master_prediction_engine.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/astro/master_prediction_engine.py").stat().st_size, "bytes")