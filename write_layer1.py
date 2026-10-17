from pathlib import Path

code = '''"""
VASTU ONE - Planetary Deep Analysis Engine
Complete 20+ attributes per planet - Maha Guru Level
"""

import swisseph as swe
from datetime import datetime
from typing import Dict, List, Any

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, RASHI_LORDS, NAKSHATRAS,
    EXALTATION, DEBILITATION, PLANET_NAMES, get_rashi, get_nakshatra
)

swe.set_ephe_path(".")


# 
# CONSTANTS
# 

# Natural friendships (Naisargika Maitri)
NATURAL_FRIENDS = {
    "Sun": {"friends": ["Moon", "Mars", "Jupiter"], "enemies": ["Venus", "Saturn"], "neutral": ["Mercury"]},
    "Moon": {"friends": ["Sun", "Mercury"], "enemies": [], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"]},
    "Mars": {"friends": ["Sun", "Moon", "Jupiter"], "enemies": ["Mercury"], "neutral": ["Venus", "Saturn"]},
    "Mercury": {"friends": ["Sun", "Venus"], "enemies": ["Moon"], "neutral": ["Mars", "Jupiter", "Saturn"]},
    "Jupiter": {"friends": ["Sun", "Moon", "Mars"], "enemies": ["Mercury", "Venus"], "neutral": ["Saturn"]},
    "Venus": {"friends": ["Mercury", "Saturn"], "enemies": ["Sun", "Moon"], "neutral": ["Mars", "Jupiter"]},
    "Saturn": {"friends": ["Mercury", "Venus"], "enemies": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]},
    "Rahu": {"friends": ["Venus", "Saturn", "Mercury"], "enemies": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]},
    "Ketu": {"friends": ["Mars", "Venus", "Saturn"], "enemies": ["Sun", "Moon"], "neutral": ["Mercury", "Jupiter"]},
}

# Avastha (age states)
AVASTHA_NAMES = ["Baal (Infant)", "Kumar (Youth)", "Yuva (Adult)", "Vridh (Old)", "Mrit (Dead)"]

# Digbala houses (best direction)
DIGBALA_HOUSES = {"Sun": 10, "Mars": 10, "Jupiter": 1, "Mercury": 1, "Moon": 4, "Venus": 4, "Saturn": 7}

# Planet natural strength (Naisargika Bala)
NAISARGIKA_BALA = {"Sun": 60, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29, "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57}


# 
# PLANETARY DEEP ANALYSIS
# 

def get_avastha(planet_lon: float, planet: str) -> Dict:
    """Calculate Avastha (age state) of planet"""
    degree_in_sign = planet_lon % 30
    
    if planet in ["Sun", "Mars", "Jupiter", "Venus", "Saturn"]:
        # Odd signs (male planets)
        rashi_num = int(planet_lon / 30)
        if rashi_num % 2 == 0:
            if degree_in_sign < 6:
                avastha = 0
            elif degree_in_sign < 12:
                avastha = 1
            elif degree_in_sign < 18:
                avastha = 2
            elif degree_in_sign < 24:
                avastha = 3
            else:
                avastha = 4
        else:
            if degree_in_sign < 6:
                avastha = 4
            elif degree_in_sign < 12:
                avastha = 3
            elif degree_in_sign < 18:
                avastha = 2
            elif degree_in_sign < 24:
                avastha = 1
            else:
                avastha = 0
    else:
        # Even signs (female planets)
        if degree_in_sign < 6:
            avastha = 0
        elif degree_in_sign < 12:
            avastha = 1
        elif degree_in_sign < 18:
            avastha = 2
        elif degree_in_sign < 24:
            avastha = 3
        else:
            avastha = 4
    
    return {
        "state": AVASTHA_NAMES[avastha],
        "index": avastha,
        "degree_in_sign": round(degree_in_sign, 2),
    }


def get_saptavargaja_bala(planet_lon: float, planet: str) -> Dict:
    """Calculate Saptavargaja Bala (strength in 7 divisional charts)"""
    vargas = {
        "D1 (Rashi)": 1,
        "D2 (Hora)": 2,
        "D3 (Drekkana)": 3,
        "D4 (Chaturthamsa)": 4,
        "D7 (Saptamsa)": 7,
        "D9 (Navamsa)": 9,
        "D12 (Dwadashamsa)": 12,
    }
    
    results = {}
    total_score = 0
    
    for varga_name, divisor in vargas.items():
        # Calculate varga position
        sign_num = int(planet_lon / 30)
        degree_in_sign = planet_lon % 30
        varga_sign = int((sign_num * divisor + degree_in_sign * divisor / 30) % 12)
        
        # Get dignity in that varga
        varga_rashi = RASHIS[varga_sign]
        
        # Score based on dignity
        if planet in EXALTATION and EXALTATION[planet][1] == varga_rashi:
            score = 20
            dignity = "Exalted"
        elif planet in DEBILITATION and DEBILITATION[planet][1] == varga_rashi:
            score = 5
            dignity = "Debilitated"
        elif RASHI_LORDS.get(varga_rashi) == planet:
            score = 15
            dignity = "Own Sign"
        else:
            # Friend/Enemy check
            lord = RASHI_LORDS.get(varga_rashi, "Sun")
            if planet in NATURAL_FRIENDS:
                if lord in NATURAL_FRIENDS[planet]["friends"]:
                    score = 12
                    dignity = "Friend"
                elif lord in NATURAL_FRIENDS[planet]["enemies"]:
                    score = 8
                    dignity = "Enemy"
                else:
                    score = 10
                    dignity = "Neutral"
            else:
                score = 10
                dignity = "Neutral"
        
        results[varga_name] = {
            "rashi": varga_rashi,
            "dignity": dignity,
            "score": score,
        }
        total_score += score
    
    return {
        "vargas": results,
        "total_score": total_score,
        "max_score": 140,
        "percentage": round(total_score / 140 * 100, 2),
    }


def get_digbala(planet_lon: float, planet: str, asc_lon: float) -> Dict:
    """Calculate Digbala (directional strength)"""
    best_house = DIGBALA_HOUSES.get(planet, 1)
    current_house = (int(planet_lon / 30) - int(asc_lon / 30)) % 12 + 1
    
    # Distance from best house
    diff = abs(current_house - best_house) % 12
    if diff > 6:
        diff = 12 - diff
    
    # Max 60 points when in best house
    digbala = 60 * (6 - diff) / 6
    
    return {
        "best_house": best_house,
        "current_house": current_house,
        "digbala": round(digbala, 2),
        "max": 60,
    }


def get_ishta_kashta_phala(planet: str, shadbala_total: float, chesta_bala: float) -> Dict:
    """Calculate Ishta Phala (benefit) and Kashta Phala (harm)"""
    # Ishta = sqrt(uchcha_bala * chesta_bala)
    # Kashta = sqrt(neecha_bala * chesta_bala)
    
    # Simplified calculation
    ishta = (shadbala_total * chesta_bala) ** 0.5 / 10
    kashta = ((600 - shadbala_total) * chesta_bala) ** 0.5 / 10
    
    return {
        "ishta_phala": round(ishta, 2),
        "kashta_phala": round(kashta, 2),
        "ishta_meaning": "Benefic results this planet can give",
        "kashta_meaning": "Harmful results this planet can give",
    }


def get_planet_maitri(planet1: str, planet2: str, chart: Dict) -> Dict:
    """Calculate friendship between two planets"""
    # Natural friendship
    if planet1 in NATURAL_FRIENDS:
        if planet2 in NATURAL_FRIENDS[planet1]["friends"]:
            natural = "Friend"
        elif planet2 in NATURAL_FRIENDS[planet1]["enemies"]:
            natural = "Enemy"
        else:
            natural = "Neutral"
    else:
        natural = "Neutral"
    
    # Temporary friendship (based on house distance)
    p1 = chart["planets"].get(planet1, {})
    p2 = chart["planets"].get(planet2, {})
    
    if p1 and p2:
        house_diff = abs(p1.get("house", 1) - p2.get("house", 1))
        if house_diff in [0, 1, 2, 3, 9, 10, 11]:
            temporary = "Friend"
        else:
            temporary = "Enemy"
    else:
        temporary = "Neutral"
    
    # Combined (Panchadha Maitri)
    if natural == "Friend" and temporary == "Friend":
        combined = "Intimate Friend"
    elif natural == "Friend" and temporary == "Enemy":
        combined = "Neutral"
    elif natural == "Enemy" and temporary == "Friend":
        combined = "Neutral"
    elif natural == "Enemy" and temporary == "Enemy":
        combined = "Bitter Enemy"
    else:
        combined = "Neutral"
    
    return {
        "natural": natural,
        "temporary": temporary,
        "combined": combined,
    }


def analyze_planet_deep(planet: str, chart: Dict) -> Dict:
    """Complete deep analysis of one planet"""
    p = chart["planets"].get(planet, {})
    if not p:
        return {}
    
    lon = p["longitude"]
    asc_lon = chart["ascendant"]["longitude"]
    
    # Basic info
    result = {
        "planet": planet,
        "longitude": lon,
        "rashi": p["rashi"],
        "degree": p["degree"],
        "house": p["house"],
        "dignity": p.get("dignity", "Neutral"),
        "retrograde": p.get("retrograde", False),
        "combust": p.get("combust", False),
        "nakshatra": p.get("nakshatra", {}),
    }
    
    # 1. Avastha (age state)
    result["avastha"] = get_avastha(lon, planet)
    
    # 2. Saptavargaja Bala (7 divisional charts)
    result["saptavargaja_bala"] = get_saptavargaja_bala(lon, planet)
    
    # 3. Digbala (directional strength)
    result["digbala"] = get_digbala(lon, planet, asc_lon)
    
    # 4. Naisargika Bala (natural strength)
    result["naisargika_bala"] = {
        "value": NAISARGIKA_BALA.get(planet, 30),
        "max": 60,
    }
    
    # 5. Ishta/Kashta Phala
    shadbala_total = p.get("shadbala", 400)
    chesta = 60 if p.get("retrograde") else 30
    result["ishta_kashta"] = get_ishta_kashta_phala(planet, shadbala_total, chesta)
    
    # 6. Friendship with other planets
    friendships = {}
    for other in PLANET_NAMES:
        if other != planet:
            friendships[other] = get_planet_maitri(planet, other, chart)
    result["friendships"] = friendships
    
    # 7. Nakshatra deep info
    nak = p.get("nakshatra", {})
    if isinstance(nak, dict):
        result["nakshatra_lord"] = nak.get("lord", "")
        result["nakshatra_deity"] = nak.get("deity", "")
        result["nakshatra_shakti"] = nak.get("shakti", "")
        result["nakshatra_pada"] = nak.get("pada", 0)
    
    return result


def analyze_all_planets_deep(chart: Dict) -> Dict:
    """Analyze all 9 planets deeply"""
    results = {}
    for planet in PLANET_NAMES:
        if planet in chart["planets"]:
            results[planet] = analyze_planet_deep(planet, chart)
    
    return {
        "planets": results,
        "total_planets": len(results),
    }


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = analyze_all_planets_deep(chart)
    
    print("=" * 70)
    print("PLANETARY DEEP ANALYSIS - INDIA")
    print("=" * 70)
    
    for planet, data in result["planets"].items():
        print()
        print(f"=== {planet} ===")
        print(f"  Rashi: {data['rashi']} at {data['degree']} deg")
        print(f"  House: {data['house']}")
        print(f"  Dignity: {data['dignity']}")
        print(f"  Retrograde: {data['retrograde']}")
        print(f"  Combust: {data['combust']}")
        print(f"  Avastha: {data['avastha']['state']}")
        print(f"  Saptavargaja Bala: {data['saptavargaja_bala']['percentage']}%")
        print(f"  Digbala: {data['digbala']['digbala']}/60")
        print(f"  Naisargika Bala: {data['naisargika_bala']['value']}/60")
        print(f"  Ishta Phala: {data['ishta_kashta']['ishta_phala']}")
        print(f"  Kashta Phala: {data['ishta_kashta']['kashta_phala']}")
        print(f"  Nakshatra Lord: {data.get('nakshatra_lord', '')}")
        print(f"  Nakshatra Deity: {data.get('nakshatra_deity', '')}")
        print(f"  Nakshatra Shakti: {data.get('nakshatra_shakti', '')}")
'''

Path("engine/astro/planetary_deep_analysis.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/astro/planetary_deep_analysis.py").stat().st_size, "bytes")