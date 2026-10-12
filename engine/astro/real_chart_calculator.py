"""
VASTU ONE - Real Astrological Chart Calculator
Uses Swiss Ephemeris for actual planetary calculations
"""

import swisseph as swe
from datetime import datetime
from typing import Dict

swe.set_ephe_path('.')

PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
    "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
    "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE,
}

NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

RASHIS = ["Mesh", "Vrishabh", "Mithun", "Kark", "Simha", "Kanya",
    "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbh", "Meen"]


def get_nakshatra(lon):
    nak_size = 360 / 27
    pada_size = nak_size / 4
    nak_idx = int(lon / nak_size)
    pada = int((lon % nak_size) / pada_size) + 1
    return NAKSHATRAS[nak_idx], pada


def get_rashi(lon):
    return RASHIS[int(lon / 30)]


def calculate_chart(year, month, day, hour, lat, lng):
    jd = swe.julday(year, month, day, hour)
    cusps, ascmc = swe.houses(jd, lat, lng, b'P')
    ascendant = ascmc[0]

    chart = {
        "julian_day": jd,
        "ascendant": {
            "longitude": round(ascendant, 4),
            "rashi": get_rashi(ascendant),
            "degree": round(ascendant % 30, 2),
        },
        "planets": {},
        "houses": [round(c, 2) for c in cusps],
    }

    for name, pid in PLANETS.items():
        pos, _ = swe.calc_ut(jd, pid)
        lon = pos[0]
        nak, pada = get_nakshatra(lon)
        chart["planets"][name] = {
            "longitude": round(lon, 4),
            "rashi": get_rashi(lon),
            "degree": round(lon % 30, 2),
            "nakshatra": nak,
            "pada": pada,
        }

    rahu_lon = chart["planets"]["Rahu"]["longitude"]
    ketu_lon = (rahu_lon + 180) % 360
    nak, pada = get_nakshatra(ketu_lon)
    chart["planets"]["Ketu"] = {
        "longitude": round(ketu_lon, 4),
        "rashi": get_rashi(ketu_lon),
        "degree": round(ketu_lon % 30, 2),
        "nakshatra": nak,
        "pada": pada,
    }

    return chart


def calculate_vimshottari_dasha(chart, birth_date, target_date=None):
    if target_date is None:
        target_date = datetime.now()

    moon_lon = chart["planets"]["Moon"]["longitude"]
    dasha_order = [("Ketu", 7), ("Shukra", 20), ("Surya", 6), ("Chandra", 10),
        ("Mangal", 7), ("Rahu", 18), ("Guru", 16), ("Shani", 19), ("Budh", 17)]

    nak_size = 360 / 27
    nak_idx = int(moon_lon / nak_size)
    start_dasha_idx = nak_idx % 9
    progress_in_nak = (moon_lon % nak_size) / nak_size
    first_dasha_years = dasha_order[start_dasha_idx][1] * (1 - progress_in_nak)

    age = (target_date - birth_date).days / 365.25
    cum = 0
    current_maha = None
    current_antar = None

    for i in range(9):
        idx = (start_dasha_idx + i) % 9
        planet, years = dasha_order[idx]
        if i == 0:
            years = first_dasha_years
        if cum <= age < cum + years:
            current_maha = planet
            sub_years = years / 9
            antar_idx = int((age - cum) / sub_years)
            current_antar = dasha_order[(idx + antar_idx) % 9][0]
            break
        cum += years

    return {
        "age_years": round(age, 2),
        "current_mahadasha": current_maha or "Unknown",
        "current_antardasha": current_antar or "Unknown",
        "moon_nakshatra": chart["planets"]["Moon"]["nakshatra"],
    }


if __name__ == "__main__":
    india_chart = calculate_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    print("=== INDIA CHART ===")
    print("Ascendant:", india_chart["ascendant"])
    print()
    print("Planets:")
    for name, data in india_chart["planets"].items():
        print(f"  {name}: {data['rashi']} {data['degree']} deg ({data['nakshatra']} pada {data['pada']})")
    print()
    birth = datetime(1947, 8, 15)
    dasha = calculate_vimshottari_dasha(india_chart, birth)
    print("=== DASHA ===")
    print("Age:", dasha["age_years"])
    print("Mahadasha:", dasha["current_mahadasha"])
    print("Antardasha:", dasha["current_antardasha"])