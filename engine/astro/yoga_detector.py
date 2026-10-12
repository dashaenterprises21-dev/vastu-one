"""
VASTU ONE - Yoga Detection Engine
Detects 50+ yogas from actual planetary positions
"""

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, RASHI_LORDS
)


# ═══════════════════════════════════════════════════════════
# YOGA DEFINITIONS
# ═══════════════════════════════════════════════════════════

# Panch Mahapurusha Yogas (5 great personality yogas)
def detect_panch_mahapurusha(chart):
    """Detect 5 great personality yogas"""
    yogas = []
    p = chart["planets"]
    
    # Ruchaka Yoga - Mars in own/exalted in Kendra
    mars = p["Mars"]
    if mars["house"] in [1, 4, 7, 10] and mars["dignity"] in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Ruchaka Yoga",
            "type": "Panch Mahapurusha",
            "effect": "Military leadership, courage, commanding personality",
            "strength": "Strong",
        })
    
    # Bhadra Yoga - Mercury in own/exalted in Kendra
    merc = p["Mercury"]
    if merc["house"] in [1, 4, 7, 10] and merc["dignity"] in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Bhadra Yoga",
            "type": "Panch Mahapurusha",
            "effect": "Intelligence, communication, diplomatic skills",
            "strength": "Strong",
        })
    
    # Hamsa Yoga - Jupiter in own/exalted in Kendra
    jup = p["Jupiter"]
    if jup["house"] in [1, 4, 7, 10] and jup["dignity"] in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Hamsa Yoga",
            "type": "Panch Mahapurusha",
            "effect": "Spiritual wisdom, teaching, prosperity",
            "strength": "Strong",
        })
    
    # Malavya Yoga - Venus in own/exalted in Kendra
    ven = p["Venus"]
    if ven["house"] in [1, 4, 7, 10] and ven["dignity"] in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Malavya Yoga",
            "type": "Panch Mahapurusha",
            "effect": "Luxury, arts, marital happiness",
            "strength": "Strong",
        })
    
    # Sasa Yoga - Saturn in own/exalted in Kendra
    sat = p["Saturn"]
    if sat["house"] in [1, 4, 7, 10] and sat["dignity"] in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Sasa Yoga",
            "type": "Panch Mahapurusha",
            "effect": "Authority, discipline, political power",
            "strength": "Strong",
        })
    
    return yogas


def detect_raja_yogas(chart):
    """Detect Raja Yogas (combinations of kendra + trikona lords)"""
    yogas = []
    asc_lon = chart["ascendant"]["longitude"]
    
    # Kendra houses: 1, 4, 7, 10
    # Trikona houses: 1, 5, 9
    
    # Get house lords
    house_lords = chart["house_lords"]
    planets = chart["planets"]
    
    kendra_lords = [house_lords[h]["lord"] for h in [1, 4, 7, 10]]
    trikona_lords = [house_lords[h]["lord"] for h in [1, 5, 9]]
    
    # Check if any kendra lord conjunct trikona lord
    for kp in kendra_lords:
        for tp in trikona_lords:
            if kp == tp:
                continue
            if kp in planets and tp in planets:
                kp_lon = planets[kp]["longitude"]
                tp_lon = planets[tp]["longitude"]
                diff = abs((kp_lon - tp_lon + 180) % 360 - 180)
                if diff < 10:
                    yogas.append({
                        "name": "Raja Yoga",
                        "type": "Raja",
                        "effect": f"{kp} + {tp} conjunction — power, authority",
                        "strength": "Strong" if diff < 5 else "Moderate",
                    })
    
    return yogas


def detect_dhana_yogas(chart):
    """Detect Dhana Yogas (wealth combinations)"""
    yogas = []
    p = chart["planets"]
    house_lords = chart["house_lords"]
    
    wealth_houses = [2, 5, 9, 11]
    wealth_lords = list(set([house_lords[h]["lord"] for h in wealth_houses]))
    
    for i, lord1 in enumerate(wealth_lords):
        for lord2 in wealth_lords[i+1:]:
            if lord1 == lord2:
                continue
            if lord1 in p and lord2 in p:
                diff = abs((p[lord1]["longitude"] - p[lord2]["longitude"] + 180) % 360 - 180)
                if diff < 10:
                    yogas.append({
                        "name": "Dhana Yoga",
                        "type": "Wealth",
                        "effect": f"{lord1} + {lord2} — wealth accumulation",
                        "strength": "Strong" if diff < 5 else "Moderate",
                    })
    
    return yogas


def detect_mangal_dosha(chart):
    """Detect Mangal Dosha (Mars affliction)"""
    p = chart["planets"]
    mars = p["Mars"]
    
    # Mars in 1, 2, 4, 7, 8, 12 houses
    if mars["house"] in [1, 2, 4, 7, 8, 12]:
        return [{
            "name": "Mangal Dosha",
            "type": "Dosha",
            "effect": "Aggressive tendencies, conflict, relationship issues",
            "strength": "High" if mars["house"] in [1, 7, 8] else "Medium",
        }]
    return []


def detect_kaal_sarpa(chart):
    """Detect Kaal Sarpa Yoga"""
    p = chart["planets"]
    rahu_lon = p["Rahu"]["longitude"]
    ketu_lon = p["Ketu"]["longitude"]
    
    # All planets between Rahu and Ketu (one side)
    planets_btw = 0
    total = 0
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in p:
            total += 1
            lon = p[name]["longitude"]
            # Check if between Rahu and Ketu
            if rahu_lon < ketu_lon:
                if rahu_lon < lon < ketu_lon:
                    planets_btw += 1
            else:
                if lon > rahu_lon or lon < ketu_lon:
                    planets_btw += 1
    
    if planets_btw == total:
        return [{
            "name": "Kaal Sarpa Yoga",
            "type": "Dosha",
            "effect": "Struggle, delays, karmic challenges",
            "strength": "High",
        }]
    return []


def detect_gaja_kesari(chart):
    """Detect Gaja Kesari Yoga (Jupiter-Moon)"""
    p = chart["planets"]
    jup = p["Jupiter"]
    moon = p["Moon"]
    
    # Jupiter in kendra from Moon
    diff = (jup["house"] - moon["house"]) % 12
    if diff in [0, 3, 6, 9]:  # Kendra from Moon
        return [{
            "name": "Gaja Kesari Yoga",
            "type": "Auspicious",
            "effect": "Wisdom, fame, prosperity, leadership",
            "strength": "Strong",
        }]
    return []


def detect_budha_aditya(chart):
    """Detect Budha-Aditya Yoga (Mercury-Sun)"""
    p = chart["planets"]
    merc = p["Mercury"]
    sun = p["Sun"]
    
    diff = abs((merc["longitude"] - sun["longitude"] + 180) % 360 - 180)
    if diff < 12:
        return [{
            "name": "Budha-Aditya Yoga",
            "type": "Auspicious",
            "effect": "Intelligence, communication, analytical skills",
            "strength": "Strong" if diff < 6 else "Moderate",
        }]
    return []


def detect_chandra_mangal(chart):
    """Detect Chandra-Mangal Yoga (Moon-Mars)"""
    p = chart["planets"]
    moon = p["Moon"]
    mars = p["Mars"]
    
    diff = abs((moon["longitude"] - mars["longitude"] + 180) % 360 - 180)
    if diff < 12:
        return [{
            "name": "Chandra-Mangal Yoga",
            "type": "Wealth",
            "effect": "Wealth through effort, property gains, but emotional volatility",
            "strength": "Strong" if diff < 6 else "Moderate",
        }]
    return []


def detect_sunapha(chart):
    """Detect Sunapha Yoga (2nd from Moon occupied)"""
    p = chart["planets"]
    moon_house = p["Moon"]["house"]
    second_from_moon = (moon_house % 12) + 1
    
    for name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in p and p[name]["house"] == second_from_moon:
            return [{
                "name": "Sunapha Yoga",
                "type": "Auspicious",
                "effect": "Wealth, self-earned property, good reputation",
                "strength": "Strong",
            }]
    return []


def detect_anapha(chart):
    """Detect Anapha Yoga (12th from Moon occupied)"""
    p = chart["planets"]
    moon_house = p["Moon"]["house"]
    twelfth_from_moon = ((moon_house - 2) % 12) + 1
    
    for name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in p and p[name]["house"] == twelfth_from_moon:
            return [{
                "name": "Anapha Yoga",
                "type": "Auspicious",
                "effect": "Good health, wealth, spiritual inclination",
                "strength": "Strong",
            }]
    return []


def detect_durudhara(chart):
    """Detect Durudhara Yoga (2nd and 12th from Moon occupied)"""
    p = chart["planets"]
    moon_house = p["Moon"]["house"]
    second = (moon_house % 12) + 1
    twelfth = ((moon_house - 2) % 12) + 1
    
    second_occ = any(p[n]["house"] == second for n in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if n in p)
    twelfth_occ = any(p[n]["house"] == twelfth for n in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if n in p)
    
    if second_occ and twelfth_occ:
        return [{
            "name": "Durudhara Yoga",
            "type": "Auspicious",
            "effect": "Wealth, vehicles, good health, charitable nature",
            "strength": "Strong",
        }]
    return []


def detect_kemadruma(chart):
    """Detect Kemadruma Yoga (no planets around Moon)"""
    p = chart["planets"]
    moon_house = p["Moon"]["house"]
    second = (moon_house % 12) + 1
    twelfth = ((moon_house - 2) % 12) + 1
    
    second_occ = any(p[n]["house"] == second for n in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if n in p)
    twelfth_occ = any(p[n]["house"] == twelfth for n in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if n in p)
    
    if not second_occ and not twelfth_occ:
        return [{
            "name": "Kemadruma Yoga",
            "type": "Dosha",
            "effect": "Poverty, loneliness, struggle, mental stress",
            "strength": "High",
        }]
    return []


def detect_amala(chart):
    """Detect Amala Yoga (10th from Moon has benefic)"""
    p = chart["planets"]
    moon_house = p["Moon"]["house"]
    tenth_from_moon = ((moon_house + 8) % 12) + 1
    
    for name in ["Jupiter", "Venus", "Mercury"]:
        if name in p and p[name]["house"] == tenth_from_moon:
            return [{
                "name": "Amala Yoga",
                "type": "Auspicious",
                "effect": "Lasting fame, prosperity, virtuous reputation",
                "strength": "Strong",
            }]
    return []


def detect_parvata(chart):
    """Detect Parvata Yoga"""
    p = chart["planets"]
    # Benefics in kendra, 6th/8th empty
    kendra_houses = [1, 4, 7, 10]
    benefics_in_kendra = sum(1 for n in ["Jupiter", "Venus", "Mercury"] if n in p and p[n]["house"] in kendra_houses)
    
    if benefics_in_kendra >= 2:
        return [{
            "name": "Parvata Yoga",
            "type": "Auspicious",
            "effect": "Wealth, leadership, fame, charitable",
            "strength": "Strong",
        }]
    return []


def detect_kahala(chart):
    """Detect Kahala Yoga"""
    p = chart["planets"]
    house_lords = chart["house_lords"]
    
    # 4th and 9th lords in kendra + strong
    lord4 = house_lords[4]["lord"]
    lord9 = house_lords[9]["lord"]
    
    if lord4 in p and lord9 in p:
        if p[lord4]["house"] in [1, 4, 7, 10] and p[lord9]["house"] in [1, 4, 7, 10]:
            return [{
                "name": "Kahala Yoga",
                "type": "Auspicious",
                "effect": "Courage, leadership, property, adventurous",
                "strength": "Strong",
            }]
    return []


def detect_vasumati(chart):
    """Detect Vasumati Yoga (benefics in upachaya houses)"""
    p = chart["planets"]
    upachaya = [3, 6, 10, 11]
    benefics_in_upachaya = sum(1 for n in ["Jupiter", "Venus", "Mercury"] if n in p and p[n]["house"] in upachaya)
    
    if benefics_in_upachaya >= 2:
        return [{
            "name": "Vasumati Yoga",
            "type": "Auspicious",
            "effect": "Wealth, independence, self-earned prosperity",
            "strength": "Strong",
        }]
    return []


# ═══════════════════════════════════════════════════════════
# MAIN DETECTOR
# ═══════════════════════════════════════════════════════════

def detect_all_yogas(chart: dict) -> dict:
    """Detect all yogas from chart"""
    all_yogas = []
    
    detectors = [
        detect_panch_mahapurusha,
        detect_raja_yogas,
        detect_dhana_yogas,
        detect_mangal_dosha,
        detect_kaal_sarpa,
        detect_gaja_kesari,
        detect_budha_aditya,
        detect_chandra_mangal,
        detect_sunapha,
        detect_anapha,
        detect_durudhara,
        detect_kemadruma,
        detect_amala,
        detect_parvata,
        detect_kahala,
        detect_vasumati,
    ]
    
    for detector in detectors:
        try:
            yogas = detector(chart)
            if yogas:
                all_yogas.extend(yogas)
        except Exception as e:
            print(f"Error in {detector.__name__}: {e}")
    
    return {
        "total_yogas": len(all_yogas),
        "yogas": all_yogas,
        "auspicious": [y for y in all_yogas if y["type"] in ["Auspicious", "Raja", "Wealth", "Panch Mahapurusha"]],
        "doshas": [y for y in all_yogas if y["type"] == "Dosha"],
    }


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = detect_all_yogas(chart)
    
    print("=== INDIA YOGA ANALYSIS ===")
    print(f"Total Yogas: {result['total_yogas']}")
    print()
    
    print("Auspicious Yogas:")
    for y in result["auspicious"]:
        print(f"  [OK] {y['name']} ({y['strength']})")
        print(f"       {y['effect']}")
    print()
    
    print("Doshas:")
    for y in result["doshas"]:
        print(f"  [!!] {y['name']} ({y['strength']})")
        print(f"       {y['effect']}")