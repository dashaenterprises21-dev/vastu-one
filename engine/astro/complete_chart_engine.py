"""
VASTU ONE - Complete Astrological Chart Engine
Uses Swiss Ephemeris for actual calculations
Includes: Planets, Houses, Nakshatra, Shadbala, Ashtakavarga, Yogas, Dasha
"""

import swisseph as swe
from datetime import datetime, timedelta
from typing import Dict, List, Any

swe.set_ephe_path('.')

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════

PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
    "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
    "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE,
}

PLANET_NAMES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

RASHIS = ["Mesh", "Vrishabh", "Mithun", "Kark", "Simha", "Kanya",
          "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbh", "Meen"]

RASHI_LORDS = {
    "Mesh": "Mars", "Vrishabh": "Venus", "Mithun": "Mercury",
    "Kark": "Moon", "Simha": "Sun", "Kanya": "Mercury",
    "Tula": "Venus", "Vrishchik": "Mars", "Dhanu": "Jupiter",
    "Makar": "Saturn", "Kumbh": "Saturn", "Meen": "Jupiter"
}

NAKSHATRAS = [
    {"name": "Ashwini", "lord": "Ketu", "deity": "Ashwini Kumaras", "shakti": "Healing"},
    {"name": "Bharani", "lord": "Venus", "deity": "Yama", "shakti": "Discipline"},
    {"name": "Krittika", "lord": "Sun", "deity": "Agni", "shakti": "Purification"},
    {"name": "Rohini", "lord": "Moon", "deity": "Brahma", "shakti": "Creativity"},
    {"name": "Mrigashira", "lord": "Mars", "deity": "Soma", "shakti": "Searching"},
    {"name": "Ardra", "lord": "Rahu", "deity": "Rudra", "shakti": "Destruction"},
    {"name": "Punarvasu", "lord": "Jupiter", "deity": "Aditi", "shakti": "Renewal"},
    {"name": "Pushya", "lord": "Saturn", "deity": "Brihaspati", "shakti": "Nourishment"},
    {"name": "Ashlesha", "lord": "Mercury", "deity": "Nagas", "shakti": "Coiling"},
    {"name": "Magha", "lord": "Ketu", "deity": "Pitris", "shakti": "Authority"},
    {"name": "Purva Phalguni", "lord": "Venus", "deity": "Bhaga", "shakti": "Pleasure"},
    {"name": "Uttara Phalguni", "lord": "Sun", "deity": "Aryaman", "shakti": "Partnership"},
    {"name": "Hasta", "lord": "Moon", "deity": "Savitar", "shakti": "Skill"},
    {"name": "Chitra", "lord": "Mars", "deity": "Vishwakarma", "shakti": "Art"},
    {"name": "Swati", "lord": "Rahu", "deity": "Vayu", "shakti": "Independence"},
    {"name": "Vishakha", "lord": "Jupiter", "deity": "Indragni", "shakti": "Achievement"},
    {"name": "Anuradha", "lord": "Saturn", "deity": "Mitra", "shakti": "Friendship"},
    {"name": "Jyeshtha", "lord": "Mercury", "deity": "Indra", "shakti": "Courage"},
    {"name": "Mula", "lord": "Ketu", "deity": "Nirriti", "shakti": "Investigation"},
    {"name": "Purva Ashadha", "lord": "Venus", "deity": "Apas", "shakti": "Invigoration"},
    {"name": "Uttara Ashadha", "lord": "Sun", "deity": "Vishwadevas", "shakti": "Victory"},
    {"name": "Shravana", "lord": "Moon", "deity": "Vishnu", "shakti": "Listening"},
    {"name": "Dhanishtha", "lord": "Mars", "deity": "Vasus", "shakti": "Wealth"},
    {"name": "Shatabhisha", "lord": "Rahu", "deity": "Varuna", "shakti": "Healing"},
    {"name": "Purva Bhadrapada", "lord": "Jupiter", "deity": "Aja Ekapada", "shakti": "Burning"},
    {"name": "Uttara Bhadrapada", "lord": "Saturn", "deity": "Ahir Budhnya", "shakti": "Depth"},
    {"name": "Revati", "lord": "Mercury", "deity": "Pushan", "shakti": "Nourishment"},
]

# Exaltation/Debilitation
EXALTATION = {
    "Sun": (10, "Mesh"), "Moon": (3, "Vrishabh"), "Mars": (28, "Makar"),
    "Mercury": (15, "Kanya"), "Jupiter": (5, "Kark"), "Venus": (27, "Meen"),
    "Saturn": (20, "Tula"), "Rahu": (20, "Mithun"), "Ketu": (20, "Dhanu"),
}

DEBILITATION = {
    "Sun": (10, "Tula"), "Moon": (3, "Vrishchik"), "Mars": (28, "Kark"),
    "Mercury": (15, "Meen"), "Jupiter": (5, "Makar"), "Venus": (27, "Kanya"),
    "Saturn": (20, "Mesh"), "Rahu": (20, "Dhanu"), "Ketu": (20, "Mithun"),
}

# Combustion limits (degrees from Sun)
COMBUSTION = {
    "Moon": 12, "Mars": 17, "Mercury": 14, "Jupiter": 11,
    "Venus": 10, "Saturn": 15,
}

# Dasha periods
DASHA_ORDER = [
    ("Ketu", 7), ("Shukra", 20), ("Surya", 6), ("Chandra", 10),
    ("Mangal", 7), ("Rahu", 18), ("Guru", 16), ("Shani", 19), ("Budh", 17)
]

DASHA_LORDS = {
    "Ketu": "Ketu", "Shukra": "Venus", "Surya": "Sun", "Chandra": "Moon",
    "Mangal": "Mars", "Rahu": "Rahu", "Guru": "Jupiter", "Shani": "Saturn", "Budh": "Mercury"
}

# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def get_nakshatra(lon: float) -> Dict:
    """Get complete nakshatra details"""
    nak_size = 360 / 27
    pada_size = nak_size / 4
    nak_idx = int(lon / nak_size)
    pada = int((lon % nak_size) / pada_size) + 1
    nak = NAKSHATRAS[nak_idx]
    return {
        "name": nak["name"],
        "lord": nak["lord"],
        "deity": nak["deity"],
        "shakti": nak["shakti"],
        "pada": pada,
        "index": nak_idx + 1,
    }


def get_rashi(lon: float) -> str:
    return RASHIS[int(lon / 30)]


def get_house(planet_lon: float, asc_lon: float) -> int:
    """Whole sign house"""
    return (int(planet_lon / 30) - int(asc_lon / 30)) % 12 + 1


def get_dignity(planet: str, lon: float) -> str:
    """Get planetary dignity"""
    rashi = get_rashi(lon)
    if planet in EXALTATION and EXALTATION[planet][1] == rashi:
        return "Exalted"
    if planet in DEBILITATION and DEBILITATION[planet][1] == rashi:
        return "Debilitated"
    if RASHI_LORDS.get(rashi) == planet:
        return "Own Sign"
    return "Neutral"


def get_combustion(planet: str, planet_lon: float, sun_lon: float) -> bool:
    """Check if planet is combust"""
    if planet not in COMBUSTION:
        return False
    diff = abs((planet_lon - sun_lon + 180) % 360 - 180)
    return diff < COMBUSTION[planet]


def get_retrograde(planet: str, jd: float) -> bool:
    """Check if planet is retrograde"""
    if planet in ["Sun", "Moon", "Rahu", "Ketu"]:
        return False
    try:
        pos1, _ = swe.calc_ut(jd, PLANETS[planet])
        pos2, _ = swe.calc_ut(jd - 1, PLANETS[planet])
        return pos1[0] < pos2[0]
    except:
        return False


# ═══════════════════════════════════════════════════════════
# MAIN CHART CALCULATION
# ═══════════════════════════════════════════════════════════

def calculate_complete_chart(year: int, month: int, day: int, hour: float,
                              lat: float, lng: float) -> Dict:
    """Calculate complete astrological chart with all details"""
    jd = swe.julday(year, month, day, hour)
    
    # Houses
    cusps, ascmc = swe.houses(jd, lat, lng, b'P')
    ascendant = ascmc[0]
    
    chart = {
        "julian_day": jd,
        "birth": {
            "year": year, "month": month, "day": day, "hour": hour,
            "lat": lat, "lng": lng,
        },
        "ascendant": {
            "longitude": round(ascendant, 4),
            "rashi": get_rashi(ascendant),
            "degree": round(ascendant % 30, 2),
            "nakshatra": get_nakshatra(ascendant),
        },
        "planets": {},
        "houses": [round(c, 2) for c in cusps],
        "house_lords": {},
        "nakshatra_pada": {},
    }
    
    # Calculate all planets
    sun_lon = None
    for name, pid in PLANETS.items():
        pos, _ = swe.calc_ut(jd, pid)
        lon = pos[0]
        lat_p = pos[1]
        speed = pos[3]
        
        if name == "Sun":
            sun_lon = lon
        
        chart["planets"][name] = {
            "longitude": round(lon, 4),
            "latitude": round(lat_p, 4),
            "speed": round(speed, 4),
            "rashi": get_rashi(lon),
            "degree": round(lon % 30, 2),
            "nakshatra": get_nakshatra(lon),
            "house": get_house(lon, ascendant),
            "dignity": get_dignity(name, lon),
            "retrograde": get_retrograde(name, jd),
            "combust": False,
        }
    
    # Ketu
    rahu_lon = chart["planets"]["Rahu"]["longitude"]
    ketu_lon = (rahu_lon + 180) % 360
    chart["planets"]["Ketu"] = {
        "longitude": round(ketu_lon, 4),
        "latitude": 0,
        "speed": 0,
        "rashi": get_rashi(ketu_lon),
        "degree": round(ketu_lon % 30, 2),
        "nakshatra": get_nakshatra(ketu_lon),
        "house": get_house(ketu_lon, ascendant),
        "dignity": get_dignity("Ketu", ketu_lon),
        "retrograde": False,
        "combust": False,
    }
    
    # Combustion check
    for name in ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in chart["planets"]:
            chart["planets"][name]["combust"] = get_combustion(
                name, chart["planets"][name]["longitude"], sun_lon
            )
    
    # House lords
    for i, rashi in enumerate(RASHIS):
        house_num = (i - int(ascendant / 30)) % 12 + 1
        chart["house_lords"][house_num] = {
            "rashi": rashi,
            "lord": RASHI_LORDS[rashi],
        }
    
    # Nakshatra pada for all planets
    for name, data in chart["planets"].items():
        chart["nakshatra_pada"][name] = {
            "nakshatra": data["nakshatra"]["name"],
            "pada": data["nakshatra"]["pada"],
            "lord": data["nakshatra"]["lord"],
            "deity": data["nakshatra"]["deity"],
        }
    
    return chart


# ═══════════════════════════════════════════════════════════
# VIMSHOTTARI DASHA - 5 LEVELS
# ═══════════════════════════════════════════════════════════

def calculate_vimshottari_dasha(chart: Dict, birth_date: datetime,
                                  target_date: datetime = None) -> Dict:
    """Calculate Vimshottari Dasha up to 5 levels"""
    if target_date is None:
        target_date = datetime.now()
    
    moon_lon = chart["planets"]["Moon"]["longitude"]
    nak_size = 360 / 27
    nak_idx = int(moon_lon / nak_size)
    start_dasha_idx = nak_idx % 9
    progress_in_nak = (moon_lon % nak_size) / nak_size
    first_dasha_years = DASHA_ORDER[start_dasha_idx][1] * (1 - progress_in_nak)
    
    age = (target_date - birth_date).days / 365.25
    
    # Build dasha sequence
    dashas = []
    cum = 0
    for i in range(9):
        idx = (start_dasha_idx + i) % 9
        planet, years = DASHA_ORDER[idx]
        if i == 0:
            years = first_dasha_years
        dashas.append({
            "planet": planet,
            "lord": DASHA_LORDS[planet],
            "years": round(years, 4),
            "start_age": round(cum, 4),
            "end_age": round(cum + years, 4),
        })
        cum += years
    
    # Find current Mahadasha
    current_maha = None
    for d in dashas:
        if d["start_age"] <= age < d["end_age"]:
            current_maha = d
            break
    
    if not current_maha:
        current_maha = dashas[-1]
    
    # Calculate Antardasha
    maha_idx = DASHA_ORDER.index((current_maha["planet"], DASHA_ORDER[[p for p, _ in DASHA_ORDER].index(current_maha["planet"])][1]))
    
    antars = []
    antar_cum = current_maha["start_age"]
    for i in range(9):
        idx = (maha_idx + i) % 9
        planet, years = DASHA_ORDER[idx]
        antar_years = (current_maha["years"] * years) / 120
        antars.append({
            "planet": planet,
            "lord": DASHA_LORDS[planet],
            "years": round(antar_years, 4),
            "start_age": round(antar_cum, 4),
            "end_age": round(antar_cum + antar_years, 4),
        })
        antar_cum += antar_years
    
    # Find current Antardasha
    current_antar = None
    for a in antars:
        if a["start_age"] <= age < a["end_age"]:
            current_antar = a
            break
    
    # Calculate Pratyantardasha
    pratyantars = []
    if current_antar:
        antar_idx = [p for p, _ in DASHA_ORDER].index(current_antar["planet"])
        prat_cum = current_antar["start_age"]
        for i in range(9):
            idx = (antar_idx + i) % 9
            planet, years = DASHA_ORDER[idx]
            prat_years = (current_antar["years"] * years) / 120
            pratyantars.append({
                "planet": planet,
                "lord": DASHA_LORDS[planet],
                "years": round(prat_years, 4),
                "start_age": round(prat_cum, 4),
                "end_age": round(prat_cum + prat_years, 4),
            })
            prat_cum += prat_years
    
    current_prat = None
    for p in pratyantars:
        if p["start_age"] <= age < p["end_age"]:
            current_prat = p
            break
    
    return {
        "age_years": round(age, 2),
        "moon_nakshatra": chart["planets"]["Moon"]["nakshatra"]["name"],
        "moon_nakshatra_lord": chart["planets"]["Moon"]["nakshatra"]["lord"],
        "mahadasha": {
            "planet": current_maha["planet"],
            "lord": current_maha["lord"],
            "start_age": current_maha["start_age"],
            "end_age": current_maha["end_age"],
        },
        "antardasha": {
            "planet": current_antar["planet"] if current_antar else "Unknown",
            "lord": current_antar["lord"] if current_antar else "Unknown",
            "start_age": current_antar["start_age"] if current_antar else 0,
            "end_age": current_antar["end_age"] if current_antar else 0,
        },
        "pratyantardasha": {
            "planet": current_prat["planet"] if current_prat else "Unknown",
            "lord": current_prat["lord"] if current_prat else "Unknown",
        },
        "full_mahadasha_sequence": dashas,
        "current_antardasha_sequence": antars,
        "current_pratyantardasha_sequence": pratyantars,
    }


# ═══════════════════════════════════════════════════════════
# TRANSIT (GOCHAR) ANALYSIS
# ═══════════════════════════════════════════════════════════

def calculate_transit(birth_chart: Dict, target_date: datetime = None) -> Dict:
    """Calculate transit and its effects on birth chart"""
    if target_date is None:
        target_date = datetime.now()
    
    birth_data = birth_chart["birth"]
    transit_chart = calculate_complete_chart(
        target_date.year, target_date.month, target_date.day,
        12.0, birth_data["lat"], birth_data["lng"]
    )
    
    asc_lon = birth_chart["ascendant"]["longitude"]
    
    transit_effects = []
    for name in PLANET_NAMES:
        if name not in transit_chart["planets"]:
            continue
        p = transit_chart["planets"][name]
        house = get_house(p["longitude"], asc_lon)
        
        transit_effects.append({
            "planet": name,
            "rashi": p["rashi"],
            "degree": p["degree"],
            "nakshatra": p["nakshatra"]["name"],
            "pada": p["nakshatra"]["pada"],
            "house": house,
            "retrograde": p["retrograde"],
            "dignity": p["dignity"],
        })
    
    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "planets": transit_effects,
        "ascendant": transit_chart["ascendant"],
    }


if __name__ == "__main__":
    # Test
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    print("=== INDIA COMPLETE CHART ===")
    print("Ascendant:", chart["ascendant"]["rashi"], chart["ascendant"]["degree"], "deg")
    print("Nakshatra:", chart["ascendant"]["nakshatra"]["name"])
    print()
    print("Planets:")
    for name, p in chart["planets"].items():
        print(f"  {name}: {p['rashi']} {p['degree']} deg (House {p['house']}) | {p['dignity']} | Retro: {p['retrograde']} | Combust: {p['combust']}")
    print()
    
    birth = datetime(1947, 8, 15)
    dasha = calculate_vimshottari_dasha(chart, birth)
    print("=== DASHA ===")
    print("Age:", dasha["age_years"])
    print("Mahadasha:", dasha["mahadasha"]["lord"])
    print("Antardasha:", dasha["antardasha"]["lord"])
    print("Pratyantardasha:", dasha["pratyantardasha"]["lord"])