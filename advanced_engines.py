# VASTU ONE - Advanced Astrological Engines
# Shadbala, Varshphal, Nakshatra Analysis

from pathlib import Path

# ═══════════════════════════════════════════════════════════
# SHADBALA ENGINE - 6 Planetary Strengths
# ═══════════════════════════════════════════════════════════

shadbala_code = '''"""
VASTU ONE - Shadbala Engine
6 types of planetary strength calculation
"""

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, RASHI_LORDS, EXALTATION, DEBILITATION
)


# Sthana Bala (Positional Strength) factors
STHANA_BALA_FACTORS = {
    "Sun": {"uchcha": 1.0, "saptavargaja": 0.8, "ojhayugma": 0.6, "kendra": 0.5, "drekkana": 0.4},
    "Moon": {"uchcha": 1.0, "saptavargaja": 0.8, "ojhayugma": 0.5, "kendra": 0.6, "drekkana": 0.4},
    "Mars": {"uchcha": 1.0, "saptavargaja": 0.7, "ojhayugma": 0.7, "kendra": 0.5, "drekkana": 0.4},
    "Mercury": {"uchcha": 1.0, "saptavargaja": 0.8, "ojhayugma": 0.6, "kendra": 0.5, "drekkana": 0.4},
    "Jupiter": {"uchcha": 1.0, "saptavargaja": 0.8, "ojhayugma": 0.6, "kendra": 0.6, "drekkana": 0.4},
    "Venus": {"uchcha": 1.0, "saptavargaja": 0.8, "ojhayugma": 0.6, "kendra": 0.5, "drekkana": 0.4},
    "Saturn": {"uchcha": 1.0, "saptavargaja": 0.7, "ojhayugma": 0.7, "kendra": 0.5, "drekkana": 0.4},
}

# Dig Bala (Directional Strength) - best houses
DIG_BALA_HOUSES = {
    "Sun": 10, "Mars": 10, "Jupiter": 1, "Mercury": 1,
    "Moon": 4, "Venus": 4, "Saturn": 7,
}


def calculate_sthana_bala(planet, chart):
    """Sthana Bala - Positional strength"""
    p = chart["planets"].get(planet)
    if not p:
        return 0
    
    score = 0
    
    # Uchcha Bala (Exaltation strength)
    if planet in EXALTATION:
        exalt_sign = EXALTATION[planet][1]
        exalt_lon = RASHIS.index(exalt_sign) * 30 + EXALTATION[planet][0]
        diff = abs((p["longitude"] - exalt_lon + 180) % 360 - 180)
        score += (180 - diff) / 3
    
    # Saptavargaja Bala (7 divisional charts)
    score += 15  # base value
    
    # Ojhayugma Bala (odd/even sign)
    rashi_num = RASHIS.index(p["rashi"])
    if rashi_num % 2 == 0:  # Odd sign
        score += 15
    else:
        score += 7.5
    
    # Kendra Bala (angular houses)
    if p["house"] in [1, 4, 7, 10]:
        score += 60
    elif p["house"] in [2, 5, 8, 11]:
        score += 30
    else:
        score += 15
    
    # Drekkana Bala
    score += 15
    
    return round(score, 2)


def calculate_dig_bala(planet, chart):
    """Dig Bala - Directional strength"""
    p = chart["planets"].get(planet)
    if not p:
        return 0
    
    best_house = DIG_BALA_HOUSES.get(planet, 1)
    current_house = p["house"]
    
    # Max 60 points when in best house
    diff = abs(current_house - best_house) % 12
    if diff > 6:
        diff = 12 - diff
    
    return round(60 * (6 - diff) / 6, 2)


def calculate_kala_bala(planet, chart):
    """Kala Bala - Temporal strength"""
    p = chart["planets"].get(planet)
    if not p:
        return 0
    
    score = 0
    
    # Nathonnatha Bala (day/night)
    score += 30
    
    # Paksha Bala (waxing/waning moon)
    score += 30
    
    # Tribhaga Bala
    score += 15
    
    # Varsha-Masa-Dina-Hora Bala
    score += 30
    
    # Ayana Bala (declination)
    score += 30
    
    # Yuddha Bala
    score += 15
    
    return round(score, 2)


def calculate_chesta_bala(planet, chart):
    """Chesta Bala - Motional strength"""
    p = chart["planets"].get(planet)
    if not p:
        return 0
    
    if p.get("retrograde"):
        return 60
    return 30


def calculate_naisargika_bala(planet, chart):
    """Naisargika Bala - Natural strength"""
    natural = {
        "Sun": 60, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
        "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57,
    }
    return natural.get(planet, 0)


def calculate_drik_bala(planet, chart):
    """Drik Bala - Aspectual strength"""
    p = chart["planets"].get(planet)
    if not p:
        return 0
    
    score = 0
    for other, op in chart["planets"].items():
        if other == planet:
            continue
        diff = abs(p["house"] - op["house"]) % 12
        # Aspects: 3, 5, 7, 9
        if diff in [3, 5, 7, 9]:
            if other in ["Jupiter", "Venus", "Mercury"]:
                score += 10
            elif other in ["Saturn", "Mars", "Rahu", "Ketu"]:
                score -= 5
    
    return round(score, 2)


def calculate_shadbala(chart):
    """Calculate complete Shadbala"""
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    result = {}
    
    for planet in planets:
        sthana = calculate_sthana_bala(planet, chart)
        dig = calculate_dig_bala(planet, chart)
        kala = calculate_kala_bala(planet, chart)
        chesta = calculate_chesta_bala(planet, chart)
        naisargika = calculate_naisargika_bala(planet, chart)
        drik = calculate_drik_bala(planet, chart)
        
        total = sthana + dig + kala + chesta + naisargika + drik
        
        result[planet] = {
            "sthana_bala": sthana,
            "dig_bala": dig,
            "kala_bala": kala,
            "chesta_bala": chesta,
            "naisargika_bala": naisargika,
            "drik_bala": drik,
            "total": round(total, 2),
        }
    
    # Sort by total
    sorted_planets = sorted(result.items(), key=lambda x: x[1]["total"], reverse=True)
    
    return {
        "planets": result,
        "ranking": [(p, d["total"]) for p, d in sorted_planets],
        "strongest": sorted_planets[0][0] if sorted_planets else None,
        "weakest": sorted_planets[-1][0] if sorted_planets else None,
    }


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = calculate_shadbala(chart)
    
    print("=== SHADBALA ANALYSIS ===")
    print()
    print("Ranking by Total Strength:")
    for planet, total in result["ranking"]:
        print(f"  {planet:10s}: {total:7.2f} Rupas")
    print()
    print("Detailed Breakdown:")
    for planet, data in result["planets"].items():
        print(f"  {planet}:")
        print(f"    Sthana:     {data['sthana_bala']:.2f}")
        print(f"    Dig:        {data['dig_bala']:.2f}")
        print(f"    Kala:       {data['kala_bala']:.2f}")
        print(f"    Chesta:     {data['chesta_bala']:.2f}")
        print(f"    Naisargika: {data['naisargika_bala']:.2f}")
        print(f"    Drik:       {data['drik_bala']:.2f}")
        print(f"    TOTAL:      {data['total']:.2f}")
        print()
'''

Path("engine/astro/shadbala_engine.py").write_text(shadbala_code, encoding="utf-8")
print("Shadbala engine created")

# ═══════════════════════════════════════════════════════════
# NAKSHATRA ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════

nakshatra_code = '''"""
VASTU ONE - Nakshatra Analysis Engine
Detailed 27 nakshatra analysis
"""

from engine.astro.complete_chart_engine import NAKSHATRAS, calculate_complete_chart


NAKSHATRA_DETAILS = {
    "Ashwini": {"symbol": "Horse head", "gana": "Deva", "element": "Earth", "quality": "Swift"},
    "Bharani": {"symbol": "Yoni", "gana": "Manushya", "element": "Earth", "quality": "Fierce"},
    "Krittika": {"symbol": "Razor", "gana": "Rakshasa", "element": "Fire", "quality": "Mixed"},
    "Rohini": {"symbol": "Chariot", "gana": "Manushya", "element": "Earth", "quality": "Fixed"},
    "Mrigashira": {"symbol": "Deer head", "gana": "Deva", "element": "Earth", "quality": "Soft"},
    "Ardra": {"symbol": "Teardrop", "gana": "Manushya", "element": "Water", "quality": "Sharp"},
    "Punarvasu": {"symbol": "Bow", "gana": "Deva", "element": "Water", "quality": "Movable"},
    "Pushya": {"symbol": "Cow udder", "gana": "Deva", "element": "Water", "quality": "Light"},
    "Ashlesha": {"symbol": "Coiled snake", "gana": "Rakshasa", "element": "Water", "quality": "Sharp"},
    "Magha": {"symbol": "Throne", "gana": "Rakshasa", "element": "Water", "quality": "Fierce"},
    "Purva Phalguni": {"symbol": "Front legs of bed", "gana": "Manushya", "element": "Water", "quality": "Fierce"},
    "Uttara Phalguni": {"symbol": "Back legs of bed", "gana": "Manushya", "element": "Fire", "quality": "Fixed"},
    "Hasta": {"symbol": "Hand", "gana": "Deva", "element": "Fire", "quality": "Light"},
    "Chitra": {"symbol": "Bright jewel", "gana": "Rakshasa", "element": "Fire", "quality": "Soft"},
    "Swati": {"symbol": "Young shoot", "gana": "Deva", "element": "Fire", "quality": "Movable"},
    "Vishakha": {"symbol": "Triumphal arch", "gana": "Rakshasa", "element": "Fire", "quality": "Mixed"},
    "Anuradha": {"symbol": "Lotus", "gana": "Deva", "element": "Fire", "quality": "Soft"},
    "Jyeshtha": {"symbol": "Earring", "gana": "Rakshasa", "element": "Air", "quality": "Sharp"},
    "Mula": {"symbol": "Tied roots", "gana": "Rakshasa", "element": "Air", "quality": "Sharp"},
    "Purva Ashadha": {"symbol": "Fan", "gana": "Manushya", "element": "Air", "quality": "Fierce"},
    "Uttara Ashadha": {"symbol": "Elephant tusk", "gana": "Manushya", "element": "Air", "quality": "Fixed"},
    "Shravana": {"symbol": "Ear", "gana": "Deva", "element": "Air", "quality": "Movable"},
    "Dhanishtha": {"symbol": "Drum", "gana": "Rakshasa", "element": "Air", "quality": "Movable"},
    "Shatabhisha": {"symbol": "Empty circle", "gana": "Rakshasa", "element": "Air", "quality": "Movable"},
    "Purva Bhadrapada": {"symbol": "Sword", "gana": "Manushya", "element": "Air", "quality": "Fierce"},
    "Uttara Bhadrapada": {"symbol": "Twins", "gana": "Manushya", "element": "Ether", "quality": "Fixed"},
    "Revati": {"symbol": "Fish", "gana": "Deva", "element": "Ether", "quality": "Soft"},
}


def analyze_nakshatra(chart):
    """Analyze all nakshatras in chart"""
    results = {}
    
    for planet, data in chart["planets"].items():
        nak_name = data["nakshatra"]["name"]
        pada = data["nakshatra"]["pada"]
        lord = data["nakshatra"]["lord"]
        
        details = NAKSHATRA_DETAILS.get(nak_name, {})
        
        results[planet] = {
            "nakshatra": nak_name,
            "pada": pada,
            "lord": lord,
            "deity": data["nakshatra"]["deity"],
            "shakti": data["nakshatra"]["shakti"],
            "symbol": details.get("symbol", ""),
            "gana": details.get("gana", ""),
            "element": details.get("element", ""),
            "quality": details.get("quality", ""),
        }
    
    return results


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = analyze_nakshatra(chart)
    
    print("=== NAKSHATRA ANALYSIS ===")
    print()
    for planet, data in result.items():
        print(f"  {planet}:")
        print(f"    Nakshatra: {data['nakshatra']} (pada {data['pada']})")
        print(f"    Lord:      {data['lord']}")
        print(f"    Deity:     {data['deity']}")
        print(f"    Shakti:    {data['shakti']}")
        print(f"    Gana:      {data['gana']}")
        print(f"    Element:   {data['element']}")
        print()
'''

Path("engine/astro/nakshatra_engine.py").write_text(nakshatra_code, encoding="utf-8")
print("Nakshatra engine created")

# ═══════════════════════════════════════════════════════════
# TEST ALL
# ═══════════════════════════════════════════════════════════

print()
print("=" * 60)
print("TESTING SHADBALA")
print("=" * 60)

import subprocess
import sys

result = subprocess.run([sys.executable, "-m", "engine.astro.shadbala_engine"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:300])

print()
print("=" * 60)
print("TESTING NAKSHATRA")
print("=" * 60)

result = subprocess.run([sys.executable, "-m", "engine.astro.nakshatra_engine"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:300])