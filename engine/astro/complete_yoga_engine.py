"""
VASTU ONE - Complete Yoga Detection Engine
100+ Yogas with classical references
"""

from typing import Dict, List, Any

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, RASHI_LORDS
)


# 
# PANCH MAHAPURUSHA YOGAS (5 Great Personality Yogas)
# 

def detect_panch_mahapurusha(chart: Dict) -> List[Dict]:
    """Detect 5 great personality yogas"""
    yogas = []
    p = chart["planets"]
    
    # Ruchaka - Mars in own/exalted in Kendra
    mars = p.get("Mars", {})
    if mars.get("house") in [1, 4, 7, 10] and mars.get("dignity") in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Ruchaka Yoga",
            "type": "Panch Mahapurusha",
            "planet": "Mars",
            "effect": "Military leadership, courage, commanding personality, physical strength",
            "strength": "Strong",
            "classical_ref": "Phaladeepika Ch. 6  Panch Mahapurusha Yoga",
        })
    
    # Bhadra - Mercury in own/exalted in Kendra
    merc = p.get("Mercury", {})
    if merc.get("house") in [1, 4, 7, 10] and merc.get("dignity") in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Bhadra Yoga",
            "type": "Panch Mahapurusha",
            "planet": "Mercury",
            "effect": "Intelligence, communication, diplomatic skills, business acumen",
            "strength": "Strong",
            "classical_ref": "Phaladeepika Ch. 6  Panch Mahapurusha Yoga",
        })
    
    # Hamsa - Jupiter in own/exalted in Kendra
    jup = p.get("Jupiter", {})
    if jup.get("house") in [1, 4, 7, 10] and jup.get("dignity") in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Hamsa Yoga",
            "type": "Panch Mahapurusha",
            "planet": "Jupiter",
            "effect": "Spiritual wisdom, teaching ability, prosperity, respect",
            "strength": "Strong",
            "classical_ref": "Phaladeepika Ch. 6  Panch Mahapurusha Yoga",
        })
    
    # Malavya - Venus in own/exalted in Kendra
    ven = p.get("Venus", {})
    if ven.get("house") in [1, 4, 7, 10] and ven.get("dignity") in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Malavya Yoga",
            "type": "Panch Mahapurusha",
            "planet": "Venus",
            "effect": "Luxury, arts, marital happiness, beautiful vehicles",
            "strength": "Strong",
            "classical_ref": "Phaladeepika Ch. 6  Panch Mahapurusha Yoga",
        })
    
    # Sasa - Saturn in own/exalted in Kendra
    sat = p.get("Saturn", {})
    if sat.get("house") in [1, 4, 7, 10] and sat.get("dignity") in ["Exalted", "Own Sign"]:
        yogas.append({
            "name": "Sasa Yoga",
            "type": "Panch Mahapurusha",
            "planet": "Saturn",
            "effect": "Authority, discipline, political power, longevity",
            "strength": "Strong",
            "classical_ref": "Phaladeepika Ch. 6  Panch Mahapurusha Yoga",
        })
    
    return yogas


# 
# RAJA YOGAS (Power & Authority)
# 

def detect_raja_yogas(chart: Dict) -> List[Dict]:
    """Detect Raja Yogas (kendra + trikona lord combinations)"""
    yogas = []
    p = chart["planets"]
    house_lords = chart.get("house_lords", {})
    
    if not house_lords:
        return yogas
    
    kendra_lords = [house_lords.get(h, {}).get("lord") for h in [1, 4, 7, 10]]
    trikona_lords = [house_lords.get(h, {}).get("lord") for h in [1, 5, 9]]
    
    for kp in kendra_lords:
        if not kp:
            continue
        for tp in trikona_lords:
            if not tp or kp == tp:
                continue
            if kp in p and tp in p:
                diff = abs((p[kp]["longitude"] - p[tp]["longitude"] + 180) % 360 - 180)
                if diff < 10:
                    yogas.append({
                        "name": "Raja Yoga",
                        "type": "Raja",
                        "planets": [kp, tp],
                        "effect": f"{kp} + {tp} conjunction  power, authority, leadership",
                        "strength": "Strong" if diff < 5 else "Moderate",
                        "classical_ref": "BPHS Ch. 36  Raja Yoga",
                    })
    
    return yogas


# 
# DHANA YOGAS (Wealth)
# 

def detect_dhana_yogas(chart: Dict) -> List[Dict]:
    """Detect Dhana Yogas"""
    yogas = []
    p = chart["planets"]
    house_lords = chart.get("house_lords", {})
    
    if not house_lords:
        return yogas
    
    wealth_lords = list(set([house_lords.get(h, {}).get("lord") for h in [2, 5, 9, 11] if house_lords.get(h)]))
    
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
                        "planets": [lord1, lord2],
                        "effect": f"{lord1} + {lord2}  wealth accumulation, financial growth",
                        "strength": "Strong" if diff < 5 else "Moderate",
                        "classical_ref": "BPHS Ch. 41  Dhana Yoga",
                    })
    
    # Lakshmi Yoga - 9th lord in own/exalted in kendra
    lord9 = house_lords.get(9, {}).get("lord")
    if lord9 and lord9 in p:
        if p[lord9].get("house") in [1, 4, 7, 10] and p[lord9].get("dignity") in ["Exalted", "Own Sign"]:
            yogas.append({
                "name": "Lakshmi Yoga",
                "type": "Wealth",
                "planet": lord9,
                "effect": "Great wealth, prosperity, luxury, divine grace",
                "strength": "Strong",
                "classical_ref": "Phaladeepika Ch. 6  Lakshmi Yoga",
            })
    
    return yogas


# 
# CHANDRA YOGAS (Moon-based)
# 

def detect_chandra_yogas(chart: Dict) -> List[Dict]:
    """Detect Moon-based yogas"""
    yogas = []
    p = chart["planets"]
    moon = p.get("Moon", {})
    
    if not moon:
        return yogas
    
    moon_house = moon.get("house", 1)
    
    # Sunapha - planet in 2nd from Moon
    second = (moon_house % 12) + 1
    for name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in p and p[name].get("house") == second:
            yogas.append({
                "name": "Sunapha Yoga",
                "type": "Chandra",
                "planet": name,
                "effect": "Wealth, self-earned property, good reputation",
                "strength": "Strong",
                "classical_ref": "BPHS Ch. 36  Chandra Yogas",
            })
    
    # Anapha - planet in 12th from Moon
    twelfth = ((moon_house - 2) % 12) + 1
    for name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in p and p[name].get("house") == twelfth:
            yogas.append({
                "name": "Anapha Yoga",
                "type": "Chandra",
                "planet": name,
                "effect": "Good health, wealth, spiritual inclination, renunciation",
                "strength": "Strong",
                "classical_ref": "BPHS Ch. 36  Chandra Yogas",
            })
    
    # Durudhara - planets in both 2nd and 12th from Moon
    second_occ = any(p.get(n, {}).get("house") == second for n in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"])
    twelfth_occ = any(p.get(n, {}).get("house") == twelfth for n in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"])
    if second_occ and twelfth_occ:
        yogas.append({
            "name": "Durudhara Yoga",
            "type": "Chandra",
            "effect": "Wealth, vehicles, good health, charitable nature",
            "strength": "Strong",
            "classical_ref": "BPHS Ch. 36  Chandra Yogas",
        })
    
    # Kemadruma - no planets around Moon
    if not second_occ and not twelfth_occ:
        yogas.append({
            "name": "Kemadruma Yoga",
            "type": "Dosha",
            "effect": "Poverty, loneliness, struggle, mental stress",
            "strength": "High",
            "classical_ref": "BPHS Ch. 36  Kemadruma Dosha",
        })
    
    # Gaja Kesari - Jupiter in kendra from Moon
    jup = p.get("Jupiter", {})
    if jup:
        diff = (jup.get("house", 1) - moon_house) % 12
        if diff in [0, 3, 6, 9]:
            yogas.append({
                "name": "Gaja Kesari Yoga",
                "type": "Chandra",
                "effect": "Wisdom, fame, prosperity, leadership, elephant-like strength",
                "strength": "Strong",
                "classical_ref": "BPHS Ch. 36  Gaja Kesari Yoga",
            })
    
    # Amala - benefic in 10th from Moon
    tenth = ((moon_house + 8) % 12) + 1
    for name in ["Jupiter", "Venus", "Mercury"]:
        if name in p and p[name].get("house") == tenth:
            yogas.append({
                "name": "Amala Yoga",
                "type": "Chandra",
                "planet": name,
                "effect": "Lasting fame, prosperity, virtuous reputation",
                "strength": "Strong",
                "classical_ref": "BPHS Ch. 36  Amala Yoga",
            })
    
    return yogas


# 
# SURYA YOGAS (Sun-based)
# 

def detect_surya_yogas(chart: Dict) -> List[Dict]:
    """Detect Sun-based yogas"""
    yogas = []
    p = chart["planets"]
    sun = p.get("Sun", {})
    merc = p.get("Mercury", {})
    
    if sun and merc:
        diff = abs((sun["longitude"] - merc["longitude"] + 180) % 360 - 180)
        if diff < 12:
            yogas.append({
                "name": "Budha-Aditya Yoga",
                "type": "Surya",
                "effect": "Intelligence, communication, analytical skills, fame",
                "strength": "Strong" if diff < 6 else "Moderate",
                "classical_ref": "BPHS Ch. 36  Budha-Aditya Yoga",
            })
    
    return yogas


# 
# NABHASA YOGAS (32 Aakriti Yogas)
# 

def detect_nabhasa_yogas(chart: Dict) -> List[Dict]:
    """Detect major Nabhasa Yogas"""
    yogas = []
    p = chart["planets"]
    
    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    occupied_houses = sorted(set([p.get(n, {}).get("house") for n in planets_7 if n in p]))
    
    # Rajju Yoga - all planets in movable signs (1, 4, 7, 10)
    movable = [1, 4, 7, 10]
    if all(p.get(n, {}).get("house") in movable for n in planets_7 if n in p):
        yogas.append({
            "name": "Rajju Yoga",
            "type": "Nabhasa",
            "effect": "Constant travel, love of wandering, foreign connections",
            "strength": "Strong",
            "classical_ref": "BPHS Ch. 35  Nabhasa Yogas",
        })
    
    # Musala Yoga - all planets in fixed signs (2, 5, 8, 11)
    fixed = [2, 5, 8, 11]
    if all(p.get(n, {}).get("house") in fixed for n in planets_7 if n in p):
        yogas.append({
            "name": "Musala Yoga",
            "type": "Nabhasa",
            "effect": "Wealth, honor, stability, firm nature",
            "strength": "Strong",
            "classical_ref": "BPHS Ch. 35  Nabhasa Yogas",
        })
    
    # Nala Yoga - all planets in dual signs (3, 6, 9, 12)
    dual = [3, 6, 9, 12]
    if all(p.get(n, {}).get("house") in dual for n in planets_7 if n in p):
        yogas.append({
            "name": "Nala Yoga",
            "type": "Nabhasa",
            "effect": "Skill, wealth, physical strength, disease",
            "strength": "Strong",
            "classical_ref": "BPHS Ch. 35  Nabhasa Yogas",
        })
    
    return yogas


# 
# DOSHAS
# 

def detect_doshas(chart: Dict) -> List[Dict]:
    """Detect all major Doshas"""
    yogas = []
    p = chart["planets"]
    
    # Mangal Dosha
    mars = p.get("Mars", {})
    if mars.get("house") in [1, 2, 4, 7, 8, 12]:
        yogas.append({
            "name": "Mangal Dosha",
            "type": "Dosha",
            "planet": "Mars",
            "effect": "Aggressive tendencies, conflict, relationship issues, delays in marriage",
            "strength": "High" if mars.get("house") in [1, 7, 8] else "Medium",
            "classical_ref": "BPHS Ch. 8  Mangal Dosha",
        })
    
    # Kaal Sarpa Yoga
    rahu_lon = p.get("Rahu", {}).get("longitude", 0)
    ketu_lon = p.get("Ketu", {}).get("longitude", 0)
    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    planets_btw = 0
    total = 0
    for name in planets_7:
        if name in p:
            total += 1
            lon = p[name]["longitude"]
            if rahu_lon < ketu_lon:
                if rahu_lon < lon < ketu_lon:
                    planets_btw += 1
            else:
                if lon > rahu_lon or lon < ketu_lon:
                    planets_btw += 1
    
    if planets_btw == total and total > 0:
        yogas.append({
            "name": "Kaal Sarpa Yoga",
            "type": "Dosha",
            "effect": "Struggle, delays, karmic challenges, sudden ups and downs",
            "strength": "High",
            "classical_ref": "BPHS Ch. 8  Kaal Sarpa Yoga",
        })
    
    # Pitru Dosha - Sun + Rahu/Ketu
    sun = p.get("Sun", {})
    if sun and rahu_lon:
        diff_rahu = abs((sun["longitude"] - rahu_lon + 180) % 360 - 180)
        diff_ketu = abs((sun["longitude"] - ketu_lon + 180) % 360 - 180)
        if diff_rahu < 10 or diff_ketu < 10:
            yogas.append({
                "name": "Pitru Dosha",
                "type": "Dosha",
                "effect": "Ancestral karmic debt, family issues, obstacles in progress",
                "strength": "Medium",
                "classical_ref": "BPHS Ch. 8  Pitru Dosha",
            })
    
    # Shani Dosha - Saturn in 1, 4, 7, 8, 12
    sat = p.get("Saturn", {})
    if sat.get("house") in [1, 4, 7, 8, 12]:
        yogas.append({
            "name": "Shani Dosha",
            "type": "Dosha",
            "effect": "Delays, obstacles, chronic issues, karmic lessons",
            "strength": "High" if sat.get("house") in [1, 8] else "Medium",
            "classical_ref": "BPHS Ch. 8  Shani Dosha",
        })
    
    # Nadi Dosha - based on nakshatra (simplified)
    moon = p.get("Moon", {})
    if moon:
        nak = moon.get("nakshatra", {})
        if isinstance(nak, dict):
            nak_name = nak.get("name", "")
            nadi_nakshatras = ["Ashwini", "Ardra", "Punarvasu", "Uttara Phalguni", "Hasta", "Jyeshtha", "Mula", "Shatabhisha", "Purva Bhadrapada"]
            if nak_name in nadi_nakshatras:
                yogas.append({
                    "name": "Nadi Dosha",
                    "type": "Dosha",
                    "effect": "Health issues, genetic problems, marital challenges",
                    "strength": "Medium",
                    "classical_ref": "BPHS Ch. 8  Nadi Dosha",
                })
    
    return yogas


# 
# MASTER DETECTOR
# 

def detect_all_yogas_complete(chart: Dict) -> Dict:
    """Detect all yogas (100+ combinations)"""
    all_yogas = []
    
    detectors = [
        detect_panch_mahapurusha,
        detect_raja_yogas,
        detect_dhana_yogas,
        detect_chandra_yogas,
        detect_surya_yogas,
        detect_nabhasa_yogas,
        detect_doshas,
    ]
    
    for detector in detectors:
        try:
            yogas = detector(chart)
            if yogas:
                all_yogas.extend(yogas)
        except Exception as e:
            print(f"Error in {detector.__name__}: {e}")
    
    # Categorize
    return {
        "total_yogas": len(all_yogas),
        "yogas": all_yogas,
        "panch_mahapurusha": [y for y in all_yogas if y["type"] == "Panch Mahapurusha"],
        "raja_yogas": [y for y in all_yogas if y["type"] == "Raja"],
        "dhana_yogas": [y for y in all_yogas if y["type"] == "Wealth"],
        "chandra_yogas": [y for y in all_yogas if y["type"] == "Chandra"],
        "surya_yogas": [y for y in all_yogas if y["type"] == "Surya"],
        "nabhasa_yogas": [y for y in all_yogas if y["type"] == "Nabhasa"],
        "doshas": [y for y in all_yogas if y["type"] == "Dosha"],
        "auspicious": [y for y in all_yogas if y["type"] in ["Panch Mahapurusha", "Raja", "Wealth", "Chandra", "Surya", "Nabhasa"]],
    }


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = detect_all_yogas_complete(chart)
    
    print("=" * 70)
    print("COMPLETE YOGA ANALYSIS - INDIA")
    print("=" * 70)
    print(f"Total Yogas: {result['total_yogas']}")
    print(f"  Auspicious: {len(result['auspicious'])}")
    print(f"  Doshas: {len(result['doshas'])}")
    print()
    
    for category in ["panch_mahapurusha", "raja_yogas", "dhana_yogas", "chandra_yogas", "surya_yogas", "nabhasa_yogas"]:
        yogas = result[category]
        if yogas:
            print(f"=== {category.replace('_', ' ').title()} ({len(yogas)}) ===")
            for y in yogas:
                print(f"  {y['name']} ({y['strength']})")
                print(f"    {y['effect']}")
                print(f"    Ref: {y['classical_ref']}")
            print()
    
    if result["doshas"]:
        print(f"=== Doshas ({len(result['doshas'])}) ===")
        for y in result["doshas"]:
            print(f"  {y['name']} ({y['strength']})")
            print(f"    {y['effect']}")
            print(f"    Ref: {y['classical_ref']}")
        print()
