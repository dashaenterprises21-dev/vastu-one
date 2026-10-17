from pathlib import Path

code = '''"""
VASTU ONE - Complete Varshphal Engine
Annual chart with Muntha, Year Lord, Mudda Dasha, month-wise predictions
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any

import swisseph as swe

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, RASHIS, RASHI_LORDS, get_rashi, get_house
)


# Muntha meanings by house
MUNTHA_MEANINGS = {
    1: "Self, health, personality, new beginnings",
    2: "Wealth, family, speech, resources",
    3: "Courage, siblings, communication, short travels",
    4: "Home, mother, property, emotional foundations",
    5: "Children, creativity, education, romance",
    6: "Enemies, health, service, competition",
    7: "Partnerships, marriage, business, public dealings",
    8: "Transformation, inheritance, occult, sudden events",
    9: "Luck, dharma, higher education, long travels",
    10: "Career, government, authority, public status",
    11: "Gains, friendships, aspirations, income",
    12: "Losses, foreign lands, spirituality, liberation",
}

# Mudda Dasha order (annual)
MUDDA_ORDER = [
    ("Sun", 30), ("Moon", 15), ("Mars", 7.5), ("Mercury", 7.5),
    ("Jupiter", 7.5), ("Venus", 7.5), ("Saturn", 7.5),
]

# Month lords (12 months)
MONTH_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]


def find_solar_return(birth_chart: Dict, target_year: int) -> datetime:
    """Find exact date when Sun returns to birth position"""
    birth_sun_lon = birth_chart["planets"]["Sun"]["longitude"]
    birth_data = birth_chart["birth"]
    
    approx_date = datetime(target_year, birth_data["month"], birth_data["day"])
    
    for _ in range(30):
        jd = swe.julday(approx_date.year, approx_date.month, approx_date.day, 12.0)
        pos, _ = swe.calc_ut(jd, swe.SUN)
        current_sun_lon = pos[0]
        
        diff = (current_sun_lon - birth_sun_lon + 180) % 360 - 180
        
        if abs(diff) < 0.0001:
            break
        
        days_to_adjust = diff / 0.9856
        approx_date = approx_date + timedelta(days=days_to_adjust)
    
    return approx_date


def calculate_varshphal_full(birth_chart: Dict, target_year: int) -> Dict:
    """Calculate complete Varshphal (annual chart)"""
    solar_return = find_solar_return(birth_chart, target_year)
    birth_data = birth_chart["birth"]
    
    # Calculate annual chart
    varsh_chart = calculate_complete_chart(
        solar_return.year, solar_return.month, solar_return.day,
        solar_return.hour, birth_data["lat"], birth_data["lng"]
    )
    
    # Muntha calculation
    years_completed = target_year - birth_data["year"]
    birth_asc_sign = int(birth_chart["ascendant"]["longitude"] / 30)
    muntha_sign = (birth_asc_sign + years_completed) % 12
    muntha_rashi = RASHIS[muntha_sign]
    
    # Muntha house in annual chart
    varsh_asc_sign = int(varsh_chart["ascendant"]["longitude"] / 30)
    muntha_house = (muntha_sign - varsh_asc_sign) % 12 + 1
    
    # Year Lord (Varsheshwara) - lord of the sign where Muntha is placed
    year_lord = RASHI_LORDS.get(muntha_rashi, "Sun")
    
    # Mudda Dasha (annual dasha)
    mudda = calculate_mudda_dasha(varsh_chart, solar_return)
    
    # Month-wise predictions
    month_predictions = calculate_month_predictions(varsh_chart, solar_return, year_lord)
    
    return {
        "year": target_year,
        "solar_return_date": solar_return.strftime("%Y-%m-%d %H:%M"),
        "age_completed": years_completed,
        "annual_chart": {
            "ascendant": varsh_chart["ascendant"],
            "planets": varsh_chart["planets"],
        },
        "muntha": {
            "rashi": muntha_rashi,
            "sign_num": muntha_sign + 1,
            "house": muntha_house,
            "meaning": MUNTHA_MEANINGS.get(muntha_house, "General effects"),
        },
        "year_lord": {
            "planet": year_lord,
            "rashi": muntha_rashi,
            "meaning": f"{year_lord} rules the year  {get_planet_meaning(year_lord)}",
        },
        "mudda_dasha": mudda,
        "month_predictions": month_predictions,
        "classical_ref": "BPHS Ch. 47  Varshphal (Annual Chart)",
    }


def calculate_mudda_dasha(varsh_chart: Dict, solar_return: datetime) -> List[Dict]:
    """Calculate Mudda Dasha for the year"""
    # Start from the lord of the ascendant of annual chart
    asc_sign = int(varsh_chart["ascendant"]["longitude"] / 30)
    asc_lord = RASHI_LORDS.get(RASHIS[asc_sign], "Sun")
    
    # Find position of asc lord in Mudda order
    start_idx = next((i for i, (p, _) in enumerate(MUDDA_ORDER) if p == asc_lord), 0)
    
    total_days = 365.25
    mudda_periods = []
    cum_days = 0
    
    for i in range(len(MUDDA_ORDER)):
        idx = (start_idx + i) % len(MUDDA_ORDER)
        planet, days = MUDDA_ORDER[idx]
        
        start_date = solar_return + timedelta(days=cum_days)
        end_date = start_date + timedelta(days=days)
        
        mudda_periods.append({
            "planet": planet,
            "days": days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "meaning": get_planet_meaning(planet),
        })
        
        cum_days += days
    
    return mudda_periods


def calculate_month_predictions(varsh_chart: Dict, solar_return: datetime, year_lord: str) -> List[Dict]:
    """Calculate month-wise predictions"""
    months = []
    
    for i in range(12):
        month_date = solar_return + timedelta(days=30.44 * i)
        month_lord = MONTH_LORDS[i % len(MONTH_LORDS)]
        
        # Find month lord position
        p = varsh_chart["planets"].get(month_lord, {})
        house = p.get("house", 1)
        
        months.append({
            "month_num": i + 1,
            "month_name": month_date.strftime("%B %Y"),
            "lord": month_lord,
            "house": house,
            "meaning": get_planet_meaning(month_lord),
            "house_meaning": get_house_meaning(house),
        })
    
    return months


def get_planet_meaning(planet: str) -> str:
    m = {
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
    return m.get(planet, "general effects")


def get_house_meaning(house: int) -> str:
    m = {
        1: "country, leadership", 2: "wealth, economy", 3: "communication, borders",
        4: "land, disasters", 5: "education, youth", 6: "war, enemies",
        7: "partnerships, alliances", 8: "crisis, transformation", 9: "religion, foreign",
        10: "government, politics", 11: "gains, alliances", 12: "losses, foreign",
    }
    return m.get(house, "general matters")


if __name__ == "__main__":
    birth = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    
    for year in [2026, 2027, 2028]:
        result = calculate_varshphal_full(birth, year)
        print("=" * 70)
        print(f"VARSHPHAL {year} - INDIA")
        print("=" * 70)
        print(f"Solar Return: {result['solar_return_date']}")
        print(f"Age: {result['age_completed']}")
        print()
        print("=== MUNTHA ===")
        print(f"  Rashi: {result['muntha']['rashi']}")
        print(f"  House: {result['muntha']['house']}")
        print(f"  Meaning: {result['muntha']['meaning']}")
        print()
        print("=== YEAR LORD ===")
        print(f"  Planet: {result['year_lord']['planet']}")
        print(f"  Meaning: {result['year_lord']['meaning']}")
        print()
        print("=== MUDDA DASHA ===")
        for m in result["mudda_dasha"]:
            print(f"  {m['planet']}: {m['start_date']} to {m['end_date']} ({m['days']} days)")
        print()
        print("=== MONTH PREDICTIONS ===")
        for mp in result["month_predictions"][:6]:
            print(f"  {mp['month_name']}: {mp['lord']} in House {mp['house']}")
            print(f"    {mp['meaning']}")
        print()
'''

Path("engine/astro/complete_varshphal_engine.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/astro/complete_varshphal_engine.py").stat().st_size, "bytes")