from pathlib import Path

code = '''"""
VASTU ONE - Bhrigu Nandi Nadi (BNN) Hidden Gems Engine
Advanced techniques from BNN that most astrologers don't know
"""

from typing import Dict, List, Any

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, RASHI_LORDS, NAKSHATRAS
)


# 
# BNN HIDDEN GEMS
# 

# 1. 5-Degree Rule (BNN's most powerful conjunction rule)
def detect_5_degree_conjunctions(chart: Dict) -> List[Dict]:
    """BNN 5-degree rule  planets within 5 degrees are STRONGLY conjunct"""
    conjunctions = []
    planets = chart["planets"]
    planet_list = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    
    for i, p1 in enumerate(planet_list):
        if p1 not in planets:
            continue
        for p2 in planet_list[i+1:]:
            if p2 not in planets:
                continue
            
            lon1 = planets[p1]["longitude"]
            lon2 = planets[p2]["longitude"]
            diff = abs((lon1 - lon2 + 180) % 360 - 180)
            
            if diff < 5:
                strength = "Very Strong"
                bnn_effect = f"{p1} + {p2} = intense combined energy"
            elif diff < 10:
                strength = "Strong"
                bnn_effect = f"{p1} + {p2} = combined energy"
            else:
                continue
            
            conjunctions.append({
                "planets": [p1, p2],
                "degree_diff": round(diff, 2),
                "strength": strength,
                "bnn_effect": bnn_effect,
                "classical_ref": "Bhrigu Nandi Nadi  5-Degree Rule",
            })
    
    return conjunctions


# 2. Retrograde Reversal Rule (BNN's unique technique)
def detect_retrograde_reversal(chart: Dict) -> List[Dict]:
    """BNN: Retrograde planets give reverse effects"""
    reversals = []
    planets = chart["planets"]
    
    reverse_effects = {
        "Sun": "Leadership becomes internalized, authority questioned",
        "Moon": "Emotional detachment, public support reversed",
        "Mars": "Military action delayed, aggression turned inward",
        "Mercury": "Communication blocked, trade disrupted",
        "Jupiter": "Wisdom questioned, growth delayed",
        "Venus": "Luxury lost, relationships reversed",
        "Saturn": "Discipline questioned, delays reversed",
        "Rahu": "Illusion reversed, foreign influence blocked",
        "Ketu": "Spirituality blocked, isolation reversed",
    }
    
    for planet, data in planets.items():
        if data.get("retrograde"):
            reversals.append({
                "planet": planet,
                "rashi": data["rashi"],
                "house": data["house"],
                "bnn_effect": reverse_effects.get(planet, "Effects reversed"),
                "classical_ref": "Bhrigu Nandi Nadi  Retrograde Reversal",
            })
    
    return reversals


# 3. Trinal Rashi Combination (BNN's unique trine rule)
TRINAL_GROUPS = [[0, 4, 8], [1, 5, 9], [2, 6, 10], [3, 7, 11]]

def detect_trinal_combinations(chart: Dict) -> List[Dict]:
    """BNN: Planets in trinal rashis are considered combined"""
    combinations = []
    planets = chart["planets"]
    
    for i, (p1, d1) in enumerate(planets.items()):
        sign1 = int(d1["longitude"] / 30)
        for p2, d2 in list(planets.items())[i+1:]:
            sign2 = int(d2["longitude"] / 30)
            
            for group in TRINAL_GROUPS:
                if sign1 in group and sign2 in group:
                    combinations.append({
                        "planets": [p1, p2],
                        "rashis": [d1["rashi"], d2["rashi"]],
                        "trinal_group": group,
                        "bnn_effect": f"{p1} and {p2} act as combined force",
                        "classical_ref": "Bhrigu Nandi Nadi  Trinal Rashi Rule",
                    })
                    break
    
    return combinations


# 4. Nakshatra Pada Deep Analysis
PADA_MEANINGS = {
    1: "Dharma  Purpose, beginning, righteousness",
    2: "Artha  Wealth, struggle, material goals",
    3: "Kama  Desire, execution, fulfillment",
    4: "Moksha  Liberation, result, completion",
}

def analyze_nakshatra_pada(chart: Dict) -> List[Dict]:
    """BNN: Deep analysis of Nakshatra Pada"""
    results = []
    planets = chart["planets"]
    
    for planet, data in planets.items():
        nak = data.get("nakshatra", {})
        if isinstance(nak, dict):
            pada = nak.get("pada", 0)
            nak_name = nak.get("name", "")
        else:
            pada = 0
            nak_name = str(nak)
        
        results.append({
            "planet": planet,
            "nakshatra": nak_name,
            "pada": pada,
            "pada_meaning": PADA_MEANINGS.get(pada, ""),
            "bnn_effect": f"{planet} in {nak_name} pada {pada}  {PADA_MEANINGS.get(pada, '')}",
            "classical_ref": "Bhrigu Nandi Nadi  Nakshatra Pada",
        })
    
    return results


# 5. Karaka Analysis (Atmakaraka, Darakaraka, etc.)
KARAKA_NAMES = {
    "Atmakaraka": "Soul, self, primary life purpose",
    "Amatyakaraka": "Career, profession, advisor",
    "Bhratrikaraka": "Siblings, guru, father",
    "Matrikaraka": "Mother, home, education",
    "Putrakaraka": "Children, creativity, disciples",
    "Gnatikaraka": "Enemies, obstacles, disease",
    "Darakaraka": "Spouse, partnerships, business",
}

def analyze_karakas(chart: Dict) -> Dict:
    """BNN: Analyze 7 Karakas (Jaimini system)"""
    planets = chart["planets"]
    planet_list = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]
    
    # Sort by degree (highest to lowest)
    degrees = []
    for p in planet_list:
        if p in planets:
            deg = planets[p]["longitude"] % 30
            degrees.append((p, deg))
    
    degrees.sort(key=lambda x: x[1], reverse=True)
    
    karakas = {}
    karaka_order = ["Atmakaraka", "Amatyakaraka", "Bhratrikaraka", "Matrikaraka", "Putrakaraka", "Gnatikaraka", "Darakaraka"]
    
    for i, (planet, degree) in enumerate(degrees[:7]):
        if i < len(karaka_order):
            karakas[karaka_order[i]] = {
                "planet": planet,
                "degree": round(degree, 2),
                "meaning": KARAKA_NAMES.get(karaka_order[i], ""),
            }
    
    return {
        "karakas": karakas,
        "classical_ref": "Bhrigu Nandi Nadi  Karaka Analysis",
    }


# 6. BNN Dasha (Different from Vimshottari)
def calculate_bnn_dasha(chart: Dict, birth_date) -> Dict:
    """BNN uses a different dasha system based on Moon's nakshatra"""
    moon = chart["planets"].get("Moon", {})
    nak = moon.get("nakshatra", {})
    
    if isinstance(nak, dict):
        nak_name = nak.get("name", "")
        nak_lord = nak.get("lord", "")
    else:
        nak_name = str(nak)
        nak_lord = ""
    
    return {
        "moon_nakshatra": nak_name,
        "nakshatra_lord": nak_lord,
        "dasha_type": "BNN Nakshatra Dasha",
        "bnn_effect": f"BNN uses {nak_name} ({nak_lord}) as primary dasha",
        "classical_ref": "Bhrigu Nandi Nadi  Nakshatra Dasha",
    }


# 7. BNN Yoga Detection (specific to BNN)
def detect_bnn_yogas(chart: Dict) -> List[Dict]:
    """BNN-specific yogas"""
    yogas = []
    planets = chart["planets"]
    
    # BNN Yoga 1: Jupiter + Venus = Wealth Yoga
    jup = planets.get("Jupiter", {})
    ven = planets.get("Venus", {})
    if jup and ven:
        diff = abs((jup["longitude"] - ven["longitude"] + 180) % 360 - 180)
        if diff < 10:
            yogas.append({
                "name": "BNN Wealth Yoga",
                "planets": ["Jupiter", "Venus"],
                "effect": "Massive wealth, luxury, prosperity",
                "strength": "Strong" if diff < 5 else "Moderate",
                "classical_ref": "Bhrigu Nandi Nadi  Wealth Combination",
            })
    
    # BNN Yoga 2: Sun + Moon = Power Yoga
    sun = planets.get("Sun", {})
    moon = planets.get("Moon", {})
    if sun and moon:
        diff = abs((sun["longitude"] - moon["longitude"] + 180) % 360 - 180)
        if diff < 10:
            yogas.append({
                "name": "BNN Power Yoga",
                "planets": ["Sun", "Moon"],
                "effect": "Political power, authority, mass support",
                "strength": "Strong" if diff < 5 else "Moderate",
                "classical_ref": "Bhrigu Nandi Nadi  Power Combination",
            })
    
    # BNN Yoga 3: Mars + Saturn = War Yoga
    mars = planets.get("Mars", {})
    sat = planets.get("Saturn", {})
    if mars and sat:
        diff = abs((mars["longitude"] - sat["longitude"] + 180) % 360 - 180)
        if diff < 10:
            yogas.append({
                "name": "BNN War Yoga",
                "planets": ["Mars", "Saturn"],
                "effect": "Military conflict, war, bloodshed",
                "strength": "Strong" if diff < 5 else "Moderate",
                "classical_ref": "Bhrigu Nandi Nadi  War Combination",
            })
    
    return yogas


# 
# MASTER BNN ANALYZER
# 

def analyze_bnn_complete(chart: Dict, birth_date=None) -> Dict:
    """Complete BNN analysis"""
    return {
        "conjunctions_5_degree": detect_5_degree_conjunctions(chart),
        "retrograde_reversals": detect_retrograde_reversal(chart),
        "trinal_combinations": detect_trinal_combinations(chart),
        "nakshatra_pada": analyze_nakshatra_pada(chart),
        "karakas": analyze_karakas(chart),
        "bnn_dasha": calculate_bnn_dasha(chart, birth_date),
        "bnn_yogas": detect_bnn_yogas(chart),
        "classical_ref": "Bhrigu Nandi Nadi  Complete Hidden Gems Analysis",
    }


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = analyze_bnn_complete(chart)
    
    print("=" * 70)
    print("BNN HIDDEN GEMS ANALYSIS - INDIA")
    print("=" * 70)
    print()
    
    print("=== 5-DEGREE CONJUNCTIONS ===")
    for c in result["conjunctions_5_degree"]:
        print(f"  {c['planets'][0]} + {c['planets'][1]} ({c['degree_diff']})  {c['strength']}")
        print(f"    {c['bnn_effect']}")
    print()
    
    print("=== RETROGRADE REVERSALS ===")
    for r in result["retrograde_reversals"]:
        print(f"  {r['planet']} (Retrograde)  {r['bnn_effect']}")
    print()
    
    print("=== TRINAL COMBINATIONS ===")
    for t in result["trinal_combinations"][:5]:
        print(f"  {t['planets'][0]} + {t['planets'][1]} ({t['rashis'][0]} + {t['rashis'][1]})")
        print(f"    {t['bnn_effect']}")
    print()
    
    print("=== NAKSHATRA PADA ===")
    for n in result["nakshatra_pada"]:
        print(f"  {n['planet']} in {n['nakshatra']} pada {n['pada']}  {n['pada_meaning']}")
    print()
    
    print("=== KARAKAS ===")
    for k, v in result["karakas"]["karakas"].items():
        print(f"  {k}: {v['planet']} ({v['degree']})  {v['meaning']}")
    print()
    
    print("=== BNN YOGAS ===")
    for y in result["bnn_yogas"]:
        print(f"  {y['name']} ({y['strength']})  {y['effect']}")
'''

Path("engine/astro/bnn_hidden_gems.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/astro/bnn_hidden_gems.py").stat().st_size, "bytes")