"""
VASTU ONE - Nadi/Bhrigu Techniques Engine
Karmic analysis, Bhrigu Samhita, Nadi leaf reading
"""

from datetime import datetime
from typing import Dict, List, Any

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, RASHI_LORDS, NAKSHATRAS
)


# 
# BHRIGU SAMHITA TECHNIQUES
# 

BHRIGU_PATTERNS = {
    "Rahu in 1st": {
        "karma": "Past life: Betrayal of trust, manipulation of others",
        "effect": "Sudden changes in identity, foreign connections, unconventional path",
        "remedy": "Rahu mantra, donate to outcasts, serve foreigners",
    },
    "Rahu in 10th": {
        "karma": "Past life: Misuse of power, corruption",
        "effect": "Government changes, political upheaval, career instability",
        "remedy": "Surya mantra, donate wheat, serve government officials",
    },
    "Ketu in 1st": {
        "karma": "Past life: Spiritual practices, renunciation",
        "effect": "Spiritual awakening, isolation, sudden insights",
        "remedy": "Ketu mantra, donate blankets, serve spiritual seekers",
    },
    "Ketu in 4th": {
        "karma": "Past life: Neglect of family, home",
        "effect": "Land disputes, earthquake, public unrest",
        "remedy": "Chandra mantra, donate milk, serve mothers",
    },
    "Saturn in 1st": {
        "karma": "Past life: Harshness, cruelty",
        "effect": "Leadership crisis, delays, chronic health issues",
        "remedy": "Shani mantra, donate black items, serve elderly",
    },
    "Saturn in 8th": {
        "karma": "Past life: Hidden sins, occult misuse",
        "effect": "Chronic illness, sudden death, transformation",
        "remedy": "Shani mantra, donate iron, serve handicapped",
    },
    "Mars in 1st": {
        "karma": "Past life: Violence, aggression",
        "effect": "Military action, accidents, conflict",
        "remedy": "Mangal mantra, donate red items, serve soldiers",
    },
    "Mars in 7th": {
        "karma": "Past life: Broken relationships",
        "effect": "Partnership conflicts, war, divorce",
        "remedy": "Mangal mantra, donate copper, serve couples",
    },
    "Jupiter in 4th": {
        "karma": "Past life: Religious service",
        "effect": "Land prosperity, spiritual home",
        "remedy": "Guru mantra, donate yellow items, serve teachers",
    },
    "Venus in 1st": {
        "karma": "Past life: Art, beauty, luxury",
        "effect": "Luxury, arts, relationships",
        "remedy": "Shukra mantra, donate white items, serve women",
    },
    "Sun in 1st": {
        "karma": "Past life: Leadership, authority",
        "effect": "Leadership, government focus, strong identity",
        "remedy": "Surya mantra, donate wheat, serve father",
    },
    "Moon in 1st": {
        "karma": "Past life: Emotional service",
        "effect": "Public support, emotional depth, water resources",
        "remedy": "Chandra mantra, donate rice, serve mother",
    },
    "Mercury in 1st": {
        "karma": "Past life: Communication, trade",
        "effect": "Intelligence, communication, business",
        "remedy": "Budh mantra, donate green items, serve students",
    },
}


# 
# NADI ASTROLOGY TECHNIQUES
# 

NADI_NAKSHATRAS = {
    "Ashwini": {"nadi": "Aadi", "karma": "Healing, speed", "past_life": "Healer, doctor"},
    "Bharani": {"nadi": "Madhya", "karma": "Discipline, restraint", "past_life": "Judge, disciplinarian"},
    "Krittika": {"nadi": "Antya", "karma": "Purification, fire", "past_life": "Priest, firekeeper"},
    "Rohini": {"nadi": "Aadi", "karma": "Creativity, growth", "past_life": "Artist, creator"},
    "Mrigashira": {"nadi": "Madhya", "karma": "Searching, quest", "past_life": "Explorer, seeker"},
    "Ardra": {"nadi": "Antya", "karma": "Destruction, storm", "past_life": "Warrior, destroyer"},
    "Punarvasu": {"nadi": "Aadi", "karma": "Renewal, return", "past_life": "Teacher, guide"},
    "Pushya": {"nadi": "Madhya", "karma": "Nourishment, care", "past_life": "Nurturer, parent"},
    "Ashlesha": {"nadi": "Antya", "karma": "Coiling, poison", "past_life": "Serpent, healer"},
    "Magha": {"nadi": "Aadi", "karma": "Authority, throne", "past_life": "King, ruler"},
    "Purva Phalguni": {"nadi": "Madhya", "karma": "Pleasure, enjoyment", "past_life": "Artist, lover"},
    "Uttara Phalguni": {"nadi": "Antya", "karma": "Partnership, marriage", "past_life": "Spouse, partner"},
    "Hasta": {"nadi": "Aadi", "karma": "Skill, craftsmanship", "past_life": "Craftsman, artisan"},
    "Chitra": {"nadi": "Madhya", "karma": "Art, beauty", "past_life": "Architect, designer"},
    "Swati": {"nadi": "Antya", "karma": "Independence, wind", "past_life": "Trader, merchant"},
    "Vishakha": {"nadi": "Aadi", "karma": "Achievement, goal", "past_life": "Leader, achiever"},
    "Anuradha": {"nadi": "Madhya", "karma": "Friendship, devotion", "past_life": "Friend, companion"},
    "Jyeshtha": {"nadi": "Antya", "karma": "Courage, seniority", "past_life": "Elder, chief"},
    "Mula": {"nadi": "Aadi", "karma": "Root, investigation", "past_life": "Occultist, researcher"},
    "Purva Ashadha": {"nadi": "Madhya", "karma": "Invigoration, water", "past_life": "Healer, purifier"},
    "Uttara Ashadha": {"nadi": "Antya", "karma": "Victory, dharma", "past_life": "King, righteous ruler"},
    "Shravana": {"nadi": "Aadi", "karma": "Listening, learning", "past_life": "Scholar, listener"},
    "Dhanishtha": {"nadi": "Madhya", "karma": "Wealth, music", "past_life": "Musician, wealthy"},
    "Shatabhisha": {"nadi": "Antya", "karma": "Healing, mystery", "past_life": "Doctor, mystic"},
    "Purva Bhadrapada": {"nadi": "Aadi", "karma": "Burning, transformation", "past_life": "Ascetic, transformer"},
    "Uttara Bhadrapada": {"nadi": "Madhya", "karma": "Depth, wisdom", "past_life": "Sage, wise one"},
    "Revati": {"nadi": "Antya", "karma": "Nourishment, protection", "past_life": "Protector, guide"},
}


# 
# KARMIC ANALYSIS
# 

def analyze_bhrigu_karma(chart: Dict) -> List[Dict]:
    """Analyze Bhrigu Samhita karmic patterns"""
    results = []
    p = chart["planets"]
    
    for planet, data in p.items():
        house = data.get("house", 1)
        key = f"{planet} in {house}"
        
        if key in BHRIGU_PATTERNS:
            pattern = BHRIGU_PATTERNS[key]
            results.append({
                "planet": planet,
                "house": house,
                "karma": pattern["karma"],
                "effect": pattern["effect"],
                "remedy": pattern["remedy"],
                "classical_ref": "Bhrigu Samhita  Karmic Patterns",
            })
    
    return results


def analyze_nadi_karma(chart: Dict) -> Dict:
    """Analyze Nadi Astrology karmic patterns"""
    moon = chart["planets"].get("Moon", {})
    if not moon:
        return {}
    
    nak = moon.get("nakshatra", {})
    if isinstance(nak, dict):
        nak_name = nak.get("name", "")
    else:
        nak_name = str(nak)
    
    nadi_info = NADI_NAKSHATRAS.get(nak_name, {})
    
    return {
        "nakshatra": nak_name,
        "nadi": nadi_info.get("nadi", "Unknown"),
        "karma": nadi_info.get("karma", ""),
        "past_life": nadi_info.get("past_life", ""),
        "classical_ref": "Nadi Astrology  Jeeva Nadi",
    }


def analyze_karmic_debts(chart: Dict) -> List[Dict]:
    """Analyze karmic debts (Pitru, Matru, etc.)"""
    debts = []
    p = chart["planets"]
    
    # Pitru Dosha (ancestral)
    sun = p.get("Sun", {})
    rahu = p.get("Rahu", {})
    ketu = p.get("Ketu", {})
    
    if sun and rahu:
        diff = abs((sun["longitude"] - rahu["longitude"] + 180) % 360 - 180)
        if diff < 10:
            debts.append({
                "name": "Pitru Dosha",
                "type": "Ancestral Debt",
                "cause": "Unfulfilled duties to ancestors",
                "effect": "Family obstacles, delays in progress, health issues",
                "remedy": "Shraddha, Tarpan, donate to ancestors, feed crows",
                "classical_ref": "BPHS Ch. 8  Pitru Dosha",
            })
    
    # Matru Dosha (mother)
    moon = p.get("Moon", {})
    if moon and ketu:
        diff = abs((moon["longitude"] - ketu["longitude"] + 180) % 360 - 180)
        if diff < 10:
            debts.append({
                "name": "Matru Dosha",
                "type": "Maternal Debt",
                "cause": "Neglect of mother, maternal duties",
                "effect": "Emotional issues, mental stress, home problems",
                "remedy": "Serve mother, Chandra mantra, donate milk",
                "classical_ref": "BPHS Ch. 8  Matru Dosha",
            })
    
    # Kaal Sarpa (serpent debt)
    rahu_lon = rahu.get("longitude", 0)
    ketu_lon = ketu.get("longitude", 0)
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
        debts.append({
            "name": "Kaal Sarpa Dosha",
            "type": "Serpent Debt",
            "cause": "Past life harm to serpents, karmic cycle",
            "effect": "Struggle, delays, karmic challenges",
            "remedy": "Nag Panchami puja, Rahu-Ketu mantra, donate to snake charmers",
            "classical_ref": "BPHS Ch. 8  Kaal Sarpa Dosha",
        })
    
    # Guru Chandal (Jupiter + Rahu/Ketu)
    jup = p.get("Jupiter", {})
    if jup:
        for node in [rahu, ketu]:
            if node:
                diff = abs((jup["longitude"] - node["longitude"] + 180) % 360 - 180)
                if diff < 10:
                    debts.append({
                        "name": "Guru Chandal Dosha",
                        "type": "Spiritual Debt",
                        "cause": "Disrespect to teachers, misuse of knowledge",
                        "effect": "Wisdom blocked, spiritual confusion, bad advice",
                        "remedy": "Guru Puja, Jupiter mantra, serve teachers",
                        "classical_ref": "BPHS Ch. 8  Guru Chandal",
                    })
                    break
    
    return debts


def analyze_spiritual_evolution(chart: Dict) -> Dict:
    """Analyze spiritual evolution based on 9th and 12th houses"""
    p = chart["planets"]
    house_lords = chart.get("house_lords", {})
    
    lord9 = house_lords.get(9, {}).get("lord", "Sun")
    lord12 = house_lords.get(12, {}).get("lord", "Sun")
    
    # Check strength
    lord9_strong = lord9 in p and p[lord9].get("dignity") in ["Exalted", "Own Sign"]
    lord12_strong = lord12 in p and p[lord12].get("dignity") in ["Exalted", "Own Sign"]
    
    if lord9_strong and lord12_strong:
        level = "Advanced  Ready for moksha"
    elif lord9_strong or lord12_strong:
        level = "Intermediate  Spiritual growth active"
    else:
        level = "Beginner  Material focus dominant"
    
    return {
        "level": level,
        "lord_9th": lord9,
        "lord_12th": lord12,
        "9th_house": "Dharma, religion, higher learning",
        "12th_house": "Moksha, liberation, foreign",
        "classical_ref": "BPHS Ch. 24  Spiritual Evolution",
    }


# 
# MASTER ANALYZER
# 

def analyze_nadi_bhrigu_complete(chart: Dict) -> Dict:
    """Complete Nadi/Bhrigu analysis"""
    return {
        "bhrigu_karma": analyze_bhrigu_karma(chart),
        "nadi_karma": analyze_nadi_karma(chart),
        "karmic_debts": analyze_karmic_debts(chart),
        "spiritual_evolution": analyze_spiritual_evolution(chart),
        "classical_ref": "Bhrigu Samhita, Nadi Astrology, BPHS",
    }


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = analyze_nadi_bhrigu_complete(chart)
    
    print("=" * 70)
    print("NADI / BHRIGU ANALYSIS - INDIA")
    print("=" * 70)
    print()
    
    print("=== BHRIGU KARMIC PATTERNS ===")
    for k in result["bhrigu_karma"]:
        print(f"  {k['planet']} in {k['house']}th house")
        print(f"    Karma: {k['karma']}")
        print(f"    Effect: {k['effect']}")
        print(f"    Remedy: {k['remedy']}")
        print(f"    Ref: {k['classical_ref']}")
        print()
    
    print("=== NADI KARMIC ANALYSIS ===")
    nadi = result["nadi_karma"]
    if nadi:
        print(f"  Nakshatra: {nadi['nakshatra']}")
        print(f"  Nadi: {nadi['nadi']}")
        print(f"  Karma: {nadi['karma']}")
        print(f"  Past Life: {nadi['past_life']}")
        print(f"  Ref: {nadi['classical_ref']}")
        print()
    
    print("=== KARMIC DEBTS ===")
    for d in result["karmic_debts"]:
        print(f"  {d['name']} ({d['type']})")
        print(f"    Cause: {d['cause']}")
        print(f"    Effect: {d['effect']}")
        print(f"    Remedy: {d['remedy']}")
        print(f"    Ref: {d['classical_ref']}")
        print()
    
    print("=== SPIRITUAL EVOLUTION ===")
    se = result["spiritual_evolution"]
    print(f"  Level: {se['level']}")
    print(f"  9th Lord: {se['lord_9th']}")
    print(f"  12th Lord: {se['lord_12th']}")
    print(f"  Ref: {se['classical_ref']}")
