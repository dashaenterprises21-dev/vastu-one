"""
VASTU ONE - Ashtakavarga + Transit Integration Engine
Combines 337-point system with real-time transit for precise predictions
"""

from datetime import datetime
from typing import Dict, List, Any

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, get_rashi, get_house
)
from engine.astro.ashtakavarga_engine import (
    calculate_bhinnashtakavarga, calculate_sarvashtakavarga, analyze_ashtakavarga
)


# Ashtakavarga transit rules
TRANSIT_RULES = {
    "Sun": {
        "good_houses": [1, 3, 6, 10, 11],
        "bad_houses": [2, 4, 5, 7, 8, 9, 12],
    },
    "Moon": {
        "good_houses": [1, 3, 6, 7, 10, 11],
        "bad_houses": [2, 4, 5, 8, 9, 12],
    },
    "Mars": {
        "good_houses": [1, 3, 6, 11],
        "bad_houses": [2, 4, 5, 7, 8, 9, 10, 12],
    },
    "Mercury": {
        "good_houses": [1, 2, 4, 6, 8, 10, 11],
        "bad_houses": [3, 5, 7, 9, 12],
    },
    "Jupiter": {
        "good_houses": [1, 2, 5, 7, 9, 11],
        "bad_houses": [3, 4, 6, 8, 10, 12],
    },
    "Venus": {
        "good_houses": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "bad_houses": [6, 7, 10],
    },
    "Saturn": {
        "good_houses": [3, 6, 11],
        "bad_houses": [1, 2, 4, 5, 7, 8, 9, 10, 12],
    },
    "Rahu": {
        "good_houses": [3, 6, 10, 11],
        "bad_houses": [1, 2, 4, 5, 7, 8, 9, 12],
    },
    "Ketu": {
        "good_houses": [3, 6, 10, 11],
        "bad_houses": [1, 2, 4, 5, 7, 8, 9, 12],
    },
}

# Ashtakavarga point thresholds
BINDU_STRENGTH = {
    "excellent": 6,
    "very_good": 5,
    "good": 4,
    "average": 3,
    "weak": 2,
    "very_weak": 1,
}


def get_bindu_strength(bindu: int) -> str:
    """Get strength level from bindu count"""
    if bindu >= 6:
        return "Excellent"
    elif bindu >= 5:
        return "Very Good"
    elif bindu >= 4:
        return "Good"
    elif bindu >= 3:
        return "Average"
    elif bindu >= 2:
        return "Weak"
    else:
        return "Very Weak"


def analyze_transit_with_ashtakavarga(chart: Dict, target_date: datetime = None) -> Dict:
    """Analyze transit combined with Ashtakavarga"""
    if target_date is None:
        target_date = datetime.now()
    
    # Get Ashtakavarga
    ashtaka = analyze_ashtakavarga(chart)
    sarva = ashtaka["sarvashtakavarga"]
    
    # Get transit chart
    birth_data = chart["birth"]
    transit_chart = calculate_complete_chart(
        target_date.year, target_date.month, target_date.day,
        12.0, birth_data["lat"], birth_data["lng"]
    )
    
    # Analyze each planet's transit
    transit_analysis = []
    asc_lon = chart["ascendant"]["longitude"]
    
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        if planet not in transit_chart["planets"]:
            continue
        
        p = transit_chart["planets"][planet]
        house = get_house(p["longitude"], asc_lon)
        rashi = p["rashi"]
        bindu = sarva.get(rashi, 0)
        
        # Check if good or bad house
        rules = TRANSIT_RULES.get(planet, {})
        is_good = house in rules.get("good_houses", [])
        is_bad = house in rules.get("bad_houses", [])
        
        # Combined analysis
        if is_good and bindu >= 5:
            verdict = "Excellent  Highly favorable"
            verdict_type = "positive"
        elif is_good and bindu >= 3:
            verdict = "Good  Favorable"
            verdict_type = "positive"
        elif is_bad and bindu <= 2:
            verdict = "Very Challenging  Avoid major decisions"
            verdict_type = "negative"
        elif is_bad:
            verdict = "Challenging  Requires caution"
            verdict_type = "negative"
        else:
            verdict = "Mixed  Neutral effects"
            verdict_type = "neutral"
        
        transit_analysis.append({
            "planet": planet,
            "rashi": rashi,
            "degree": p["degree"],
            "house": house,
            "nakshatra": p["nakshatra"]["name"],
            "pada": p["nakshatra"]["pada"],
            "bindu": bindu,
            "bindu_strength": get_bindu_strength(bindu),
            "house_type": "Good" if is_good else ("Bad" if is_bad else "Neutral"),
            "verdict": verdict,
            "verdict_type": verdict_type,
        })
    
    # Sort by verdict type
    positive = [t for t in transit_analysis if t["verdict_type"] == "positive"]
    negative = [t for t in transit_analysis if t["verdict_type"] == "negative"]
    neutral = [t for t in transit_analysis if t["verdict_type"] == "neutral"]
    
    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "transit_analysis": transit_analysis,
        "positive_count": len(positive),
        "negative_count": len(negative),
        "neutral_count": len(neutral),
        "overall_verdict": "Favorable" if len(positive) > len(negative) else ("Challenging" if len(negative) > len(positive) else "Mixed"),
        "sarvashtakavarga": sarva,
        "strongest_signs": ashtaka["strongest_signs"],
        "weakest_signs": ashtaka["weakest_signs"],
    }


def get_transit_prediction(transit_analysis: Dict, planet: str) -> Dict:
    """Get detailed prediction for a specific planet transit"""
    for t in transit_analysis["transit_analysis"]:
        if t["planet"] == planet:
            return t
    return {}


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = analyze_transit_with_ashtakavarga(chart)
    
    print("=" * 70)
    print("ASHTAKAVARGA + TRANSIT ANALYSIS - INDIA")
    print("=" * 70)
    print(f"Date: {result['date']}")
    print(f"Overall Verdict: {result['overall_verdict']}")
    print(f"  Positive: {result['positive_count']}")
    print(f"  Negative: {result['negative_count']}")
    print(f"  Neutral: {result['neutral_count']}")
    print()
    
    print("=== TRANSIT ANALYSIS ===")
    for t in result["transit_analysis"]:
        print(f"  {t['planet']}: {t['rashi']} {t['degree']} deg (House {t['house']})")
        print(f"    Bindu: {t['bindu']}/8 ({t['bindu_strength']})")
        print(f"    House Type: {t['house_type']}")
        print(f"    Verdict: {t['verdict']}")
        print()
    
    print("=== STRONGEST SIGNS ===")
    for rashi, score in result["strongest_signs"]:
        print(f"  {rashi}: {score} bindus")
    
    print()
    print("=== WEAKEST SIGNS ===")
    for rashi, score in result["weakest_signs"]:
        print(f"  {rashi}: {score} bindus")
