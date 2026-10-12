"""
VASTU ONE - Varshphal Engine
Annual chart (Solar Return) calculation
"""

from datetime import datetime, timedelta
from engine.astro.complete_chart_engine import (
    calculate_complete_chart, get_rashi, get_nakshatra, get_house,
    PLANET_NAMES, RASHIS
)
from engine.astro.yoga_detector import detect_all_yogas
import swisseph as swe


def find_solar_return(birth_chart, target_year):
    """Find exact date when Sun returns to birth position"""
    birth_sun_lon = birth_chart["planets"]["Sun"]["longitude"]
    birth_data = birth_chart["birth"]
    
    # Start from approximate birthday
    approx_date = datetime(target_year, birth_data["month"], birth_data["day"])
    
    # Binary search for exact return
    for _ in range(30):
        jd = swe.julday(approx_date.year, approx_date.month, approx_date.day, 12.0)
        pos, _ = swe.calc_ut(jd, swe.SUN)
        current_sun_lon = pos[0]
        
        diff = (current_sun_lon - birth_sun_lon + 180) % 360 - 180
        
        if abs(diff) < 0.0001:
            break
        
        # Adjust date
        days_to_adjust = diff / 0.9856  # Sun moves ~1 degree/day
        approx_date = approx_date + timedelta(days=days_to_adjust)
    
    return approx_date


def calculate_varshphal(birth_chart, target_year):
    """Calculate Varshphal (annual chart)"""
    # Find solar return date
    solar_return = find_solar_return(birth_chart, target_year)
    
    birth_data = birth_chart["birth"]
    
    # Calculate annual chart at solar return
    varsh_chart = calculate_complete_chart(
        solar_return.year, solar_return.month, solar_return.day,
        solar_return.hour, birth_data["lat"], birth_data["lng"]
    )
    
    # Detect yogas in annual chart
    varsh_yogas = detect_all_yogas(varsh_chart)
    
    # Calculate Muntha (annual progressed point)
    # Muntha = birth ascendant + years completed
    years_completed = target_year - birth_data["year"]
    birth_asc_sign = int(birth_chart["ascendant"]["longitude"] / 30)
    muntha_sign = (birth_asc_sign + years_completed) % 12
    
    # Year lord (Varsheshwara)
    varsh_asc_sign = int(varsh_chart["ascendant"]["longitude"] / 30)
    year_lord_rashi = RASHIS[varsh_asc_sign]
    year_lord = birth_chart["house_lords"].get(1, {}).get("lord", "Sun")
    
    return {
        "year": target_year,
        "solar_return_date": solar_return.strftime("%Y-%m-%d %H:%M"),
        "age_completed": years_completed,
        "annual_chart": {
            "ascendant": varsh_chart["ascendant"],
            "planets": varsh_chart["planets"],
        },
        "muntha": {
            "rashi": RASHIS[muntha_sign],
            "sign_num": muntha_sign + 1,
            "meaning": "Annual progress point — where focus will be",
        },
        "year_lord": {
            "planet": year_lord,
            "rashi": year_lord_rashi,
        },
        "yogas": varsh_yogas,
    }


if __name__ == "__main__":
    birth = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    
    for year in [2026, 2027, 2028]:
        result = calculate_varshphal(birth, year)
        print(f"=== VARSHPHAL {year} ===")
        print(f"Solar Return: {result['solar_return_date']}")
        print(f"Age: {result['age_completed']}")
        print(f"Ascendant: {result['annual_chart']['ascendant']['rashi']} {result['annual_chart']['ascendant']['degree']} deg")
        print(f"Muntha: {result['muntha']['rashi']}")
        print(f"Year Lord: {result['year_lord']['planet']}")
        print(f"Yogas: {result['yogas']['total_yogas']}")
        print()
        print("Annual Chart Planets:")
        for p, d in result["annual_chart"]["planets"].items():
            print(f"  {p}: {d['rashi']} {d['degree']} deg (House {d['house']})")
        print()
