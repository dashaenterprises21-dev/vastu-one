"""
VASTU ONE - Ashtakavarga Engine
337 point system for planetary strength
"""

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, get_rashi
)


# Ashtakavarga contribution tables
# Each planet contributes points to specific houses from its position
ASHTAKAVARGA_TABLES = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [3, 4, 6, 10, 11, 12],
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 2, 4, 7, 8, 10, 11],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [3, 6, 10, 11],
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 3, 6, 10, 11],
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 2, 4, 6, 8, 10, 11],
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Ascendant": [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 4, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Ascendant": [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [1, 3, 4, 6, 10, 11],
    },
}


def calculate_bhinnashtakavarga(chart, planet):
    """Calculate Bhinnashtakavarga for one planet"""
    scores = {rashi: 0 for rashi in RASHIS}
    
    if planet not in ASHTAKAVARGA_TABLES:
        return scores
    
    table = ASHTAKAVARGA_TABLES[planet]
    asc_sign = int(chart["ascendant"]["longitude"] / 30)
    
    # For each contributor
    for contributor, houses in table.items():
        if contributor == "Ascendant":
            base_sign = asc_sign
        elif contributor in chart["planets"]:
            base_sign = int(chart["planets"][contributor]["longitude"] / 30)
        else:
            continue
        
        # Add points to houses
        for house in houses:
            target_sign = (base_sign + house - 1) % 12
            scores[RASHIS[target_sign]] += 1
    
    return scores


def calculate_sarvashtakavarga(chart):
    """Calculate total Sarvashtakavarga (337 points)"""
    total = {rashi: 0 for rashi in RASHIS}
    
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        bhinna = calculate_bhinnashtakavarga(chart, planet)
        for rashi, score in bhinna.items():
            total[rashi] += score
    
    return total


def analyze_ashtakavarga(chart):
    """Complete Ashtakavarga analysis"""
    bhinna_all = {}
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        bhinna_all[planet] = calculate_bhinnashtakavarga(chart, planet)
    
    sarva = calculate_sarvashtakavarga(chart)
    
    # Find strongest and weakest signs
    sorted_sarva = sorted(sarva.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "bhinnashtakavarga": bhinna_all,
        "sarvashtakavarga": sarva,
        "total_points": sum(sarva.values()),
        "strongest_signs": sorted_sarva[:3],
        "weakest_signs": sorted_sarva[-3:],
    }


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = analyze_ashtakavarga(chart)
    
    print("=== ASHTAKAVARGA ANALYSIS ===")
    print(f"Total Points: {result['total_points']} (expected 337)")
    print()
    print("Sarvashtakavarga (all planets combined):")
    for rashi, score in sorted(result["sarvashtakavarga"].items(), key=lambda x: x[1], reverse=True):
        bar = "=" * score
        print(f"  {rashi:12s}: {score:3d} {bar}")
    print()
    print("Top 3 Strongest Signs:")
    for rashi, score in result["strongest_signs"]:
        print(f"  {rashi}: {score} points")
    print()
    print("Top 3 Weakest Signs:")
    for rashi, score in result["weakest_signs"]:
        print(f"  {rashi}: {score} points")
