"""
VASTU ONE - Real Transit Engine
Predictions based on actual planetary calculations
"""

from datetime import datetime
from engine.astro.real_chart_calculator import calculate_chart, get_rashi, get_nakshatra

# House meanings
HOUSE_MEANINGS = {
    1: "Country, leadership, national identity",
    2: "Wealth, economy, currency",
    3: "Communication, neighbors, borders",
    4: "Land, earthquakes, natural disasters",
    5: "Education, youth, creativity",
    6: "Enemies, war, disease, military",
    7: "Partnerships, alliances, war",
    8: "Death, transformations, sudden events",
    9: "Dharma, religion, foreign relations",
    10: "Government, politics, leadership",
    11: "Gains, alliances, economy",
    12: "Losses, foreign, spiritual",
}

PLANET_HOUSE_EFFECTS = {
    "Sun": {
        1: "Strong leadership, national pride, government authority",
        2: "Economic policy, wealth creation, banking reform",
        3: "Communication, media, border talks",
        4: "Political upheaval, land disputes, internal conflict",
        5: "Education reform, youth affairs, political succession",
        6: "Military strength, enemies defeated, health policy",
        7: "Diplomatic relations, partnerships, treaties",
        8: "Crisis, scandals, sudden political change",
        9: "Religious events, foreign policy, dharma",
        10: "Powerful government, authority, leadership",
        11: "Economic gains, alliances, income growth",
        12: "Foreign policy focus, espionage, losses",
    },
    "Moon": {
        1: "Public unrest, emotional events, mass movements",
        2: "Economic fluctuation, currency issues",
        3: "Communication, media, public announcements",
        4: "Earthquake, natural disaster, land issues",
        5: "Youth affairs, education, cultural events",
        6: "Disease, epidemics, public health crisis",
        7: "Diplomatic relations, public partnerships",
        8: "Death of leaders, secrets revealed, crisis",
        9: "Religious events, foreign relations",
        10: "Government change, public opinion shift",
        11: "Economic gains, public welfare",
        12: "Foreign issues, espionage, losses",
    },
    "Mars": {
        1: "Aggressive leadership, military action, coup risk",
        2: "Economic conflict, trade war, currency attack",
        3: "Border tension, skirmishes, military movement",
        4: "Earthquake, fire, land conflict",
        5: "Youth unrest, political violence",
        6: "War, military conflict, enemies defeated",
        7: "War with partner, alliance breakdown",
        8: "Violence, accidents, sudden death",
        9: "Religious conflict, foreign military action",
        10: "Military coup, aggressive politics",
        11: "Economic conflict, trade disputes",
        12: "Foreign military action, espionage",
    },
    "Mercury": {
        1: "Communication, diplomacy, intelligence",
        2: "Economic policy, trade negotiations",
        3: "Media, negotiations, border talks",
        4: "Land disputes, internal communication",
        5: "Education reform, youth communication",
        6: "Economic policy, trade war, health",
        7: "Diplomatic relations, treaties, negotiations",
        8: "Intelligence, secrets revealed, crisis",
        9: "Foreign policy, religious communication",
        10: "Political communication, policy announcements",
        11: "Economic gains, trade agreements",
        12: "Espionage, foreign communication",
    },
    "Jupiter": {
        1: "Growth, prosperity, spiritual awakening",
        2: "Economic growth, wealth creation",
        3: "Communication, media growth",
        4: "Land prosperity, internal peace",
        5: "Education reform, youth affairs",
        6: "Enemies defeated, health improvement",
        7: "Alliances, treaties, partnerships",
        8: "Transformation, inheritance, occult",
        9: "Religious events, foreign alliances, dharma",
        10: "Stable government, wise leadership",
        11: "Economic gains, alliances, income",
        12: "Foreign spiritual growth, losses minimized",
    },
    "Venus": {
        1: "Cultural events, diplomacy, harmony",
        2: "Economic growth, wealth creation",
        3: "Communication, media, arts",
        4: "Land prosperity, internal harmony",
        5: "Entertainment, creativity, youth",
        6: "Health improvement, enemies pacified",
        7: "Alliances, treaties, partnerships",
        8: "Inheritance, transformation, occult",
        9: "Religious harmony, foreign relations",
        10: "Political harmony, stable government",
        11: "Economic growth, alliances",
        12: "Foreign cultural exchange, spiritual",
    },
    "Saturn": {
        1: "Leadership crisis, slow progress, isolation",
        2: "Economic slowdown, currency devaluation",
        3: "Communication breakdown, border tension",
        4: "Earthquake, land issues, internal conflict",
        5: "Education crisis, youth unrest",
        6: "War, military losses, disease",
        7: "Alliance breakdown, war with partner",
        8: "Death, natural disaster, transformation",
        9: "Religious conflict, foreign policy challenges",
        10: "Government change, policy shift",
        11: "Economic losses, alliance breakdown",
        12: "Foreign conspiracies, espionage, losses",
    },
    "Rahu": {
        1: "Sudden change, scandal, transformation",
        2: "Economic manipulation, currency crisis",
        3: "Communication chaos, border tension",
        4: "Earthquake, land disputes, internal unrest",
        5: "Education scandal, youth unrest",
        6: "War, terrorism, disease",
        7: "Alliance breakdown, war, partnership crisis",
        8: "Sudden death, crisis, transformation",
        9: "Religious conflict, foreign conspiracy",
        10: "Government change, coup, revolution",
        11: "Economic manipulation, alliance changes",
        12: "Foreign conspiracy, espionage, losses",
    },
    "Ketu": {
        1: "Spiritual awakening, isolation, sudden change",
        2: "Economic losses, currency issues",
        3: "Communication breakdown, border issues",
        4: "Earthquake, hidden events, land issues",
        5: "Education crisis, youth unrest",
        6: "Sudden war, insurgency, disease",
        7: "Alliance breakdown, war, partnership crisis",
        8: "Death, occult, transformation",
        9: "Religious conflict, foreign conspiracy",
        10: "Leadership crisis, sudden change",
        11: "Economic losses, alliance breakdown",
        12: "Foreign spies, espionage, spiritual growth",
    },
}


class RealTransitEngine:
    def __init__(self, country: str = "India"):
        self.country = country
        self.country_data = {
            "India": {"date": (1947, 8, 15), "time": 0.0, "lat": 28.6139, "lng": 77.2090},
            "USA": {"date": (1776, 7, 4), "time": 12.0, "lat": 39.9526, "lng": -75.1652},
            "China": {"date": (1949, 10, 1), "time": 15.0, "lat": 39.9042, "lng": 116.4074},
            "Russia": {"date": (1991, 12, 26), "time": 0.0, "lat": 55.7558, "lng": 37.6173},
            "Pakistan": {"date": (1947, 8, 14), "time": 9.5, "lat": 24.8607, "lng": 67.0011},
            "UK": {"date": (1801, 1, 1), "time": 0.0, "lat": 51.5074, "lng": -0.1278},
            "Israel": {"date": (1948, 5, 14), "time": 16.0, "lat": 32.0853, "lng": 34.7818},
            "Ukraine": {"date": (1991, 8, 24), "time": 17.5, "lat": 50.4501, "lng": 30.5234},
            "Japan": {"date": (1952, 4, 28), "time": 0.0, "lat": 35.6762, "lng": 139.6503},
            "Germany": {"date": (1990, 10, 3), "time": 0.0, "lat": 52.5200, "lng": 13.4050},
            "France": {"date": (1958, 10, 4), "time": 0.0, "lat": 48.8566, "lng": 2.3522},
            "Brazil": {"date": (1822, 9, 7), "time": 0.0, "lat": -23.5505, "lng": -46.6333},
            "Australia": {"date": (1901, 1, 1), "time": 0.0, "lat": -33.8688, "lng": 151.2093},
            "Canada": {"date": (1867, 7, 1), "time": 0.0, "lat": 45.4215, "lng": -75.6972},
            "Saudi Arabia": {"date": (1932, 9, 23), "time": 0.0, "lat": 24.7136, "lng": 46.6753},
            "Iran": {"date": (1979, 4, 1), "time": 0.0, "lat": 35.6892, "lng": 51.3890},
            "North Korea": {"date": (1948, 9, 9), "time": 0.0, "lat": 39.0392, "lng": 125.7625},
            "South Korea": {"date": (1948, 8, 15), "time": 0.0, "lat": 37.5665, "lng": 126.9780},
            "Nepal": {"date": (2008, 5, 28), "time": 0.0, "lat": 27.7172, "lng": 85.3240},
            "Sri Lanka": {"date": (1948, 2, 4), "time": 0.0, "lat": 6.9271, "lng": 79.8612},
            "Bangladesh": {"date": (1971, 3, 26), "time": 0.0, "lat": 23.8103, "lng": 90.4125},
            "Afghanistan": {"date": (1919, 8, 19), "time": 0.0, "lat": 34.5553, "lng": 69.2075},
            "Turkey": {"date": (1923, 10, 29), "time": 0.0, "lat": 39.9334, "lng": 32.8597},
            "Egypt": {"date": (1922, 2, 28), "time": 0.0, "lat": 30.0444, "lng": 31.2357},
            "South Africa": {"date": (1994, 4, 27), "time": 0.0, "lat": -25.7479, "lng": 28.2293},
        }

    def _get_house(self, planet_lon: float, asc_lon: float) -> int:
        """Calculate house from longitude (whole sign)"""
        planet_sign = int(planet_lon / 30)
        asc_sign = int(asc_lon / 30)
        house = (planet_sign - asc_sign) % 12 + 1
        return house

    def analyze_transit(self, target_date: datetime = None) -> dict:
        if target_date is None:
            target_date = datetime.now()

        data = self.country_data.get(self.country)
        if not data:
            return {"error": f"Country not found: {self.country}"}

        y, m, d = data["date"]
        birth = calculate_chart(y, m, d, data["time"], data["lat"], data["lng"])
        transit = calculate_chart(target_date.year, target_date.month, target_date.day,
                                  12.0, data["lat"], data["lng"])

        asc_lon = birth["ascendant"]["longitude"]

        # Analyze each planet's transit
        transit_effects = []
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            if planet not in transit["planets"]:
                continue
            p_lon = transit["planets"][planet]["longitude"]
            house = self._get_house(p_lon, asc_lon)
            effect = PLANET_HOUSE_EFFECTS.get(planet, {}).get(house, "General effects")
            transit_effects.append({
                "planet": planet,
                "rashi": transit["planets"][planet]["rashi"],
                "degree": transit["planets"][planet]["degree"],
                "house": house,
                "house_meaning": HOUSE_MEANINGS[house],
                "effect": effect,
            })

        # Detect yogas
        yogas = self._detect_yogas(transit, asc_lon)

        return {
            "country": self.country,
            "date": target_date.strftime("%Y-%m-%d"),
            "birth_chart": {
                "ascendant": birth["ascendant"],
                "sun": birth["planets"]["Sun"],
                "moon": birth["planets"]["Moon"],
            },
            "transit": transit_effects,
            "yogas": yogas,
        }

    def _detect_yogas(self, transit: dict, asc_lon: float) -> list:
        """Detect actual yoga combinations from transit"""
        yogas = []
        planets = transit["planets"]

        # Sun + Jupiter conjunction (within 10 deg)
        sun_jup_diff = abs((planets["Sun"]["longitude"] - planets["Jupiter"]["longitude"]) % 360)
        if sun_jup_diff < 10 or sun_jup_diff > 350:
            yogas.append({
                "name": "Guru-Surya Yoga",
                "effect": "Leadership growth, political stability, spiritual awakening",
                "strength": "Strong" if sun_jup_diff < 5 else "Moderate",
            })

        # Mars + Ketu conjunction
        mars_ketu_diff = abs((planets["Mars"]["longitude"] - planets["Ketu"]["longitude"]) % 360)
        if mars_ketu_diff < 10 or mars_ketu_diff > 350:
            yogas.append({
                "name": "Mangal-Ketu Yoga",
                "effect": "Sudden events, accidents, military action, war",
                "strength": "Strong" if mars_ketu_diff < 5 else "Moderate",
            })

        # Saturn + Moon (within 15 deg)
        sat_moon_diff = abs((planets["Saturn"]["longitude"] - planets["Moon"]["longitude"]) % 360)
        if sat_moon_diff < 15 or sat_moon_diff > 345:
            yogas.append({
                "name": "Shani-Chandra Yoga",
                "effect": "Earthquake, natural disaster, public unrest",
                "strength": "Strong" if sat_moon_diff < 8 else "Moderate",
            })

        # Rahu-Ketu axis with Mars
        rahu_ketu_axis = abs((planets["Rahu"]["longitude"] - planets["Ketu"]["longitude"]) % 360)
        if 175 < rahu_ketu_axis < 185:
            yogas.append({
                "name": "Rahu-Ketu Axis",
                "effect": "Major transformation, sudden political change",
                "strength": "Active",
            })

        # Mars + Saturn
        mars_sat_diff = abs((planets["Mars"]["longitude"] - planets["Saturn"]["longitude"]) % 360)
        if mars_sat_diff < 15 or mars_sat_diff > 345:
            yogas.append({
                "name": "Mangal-Shani Yoga",
                "effect": "War, military conflict, violence",
                "strength": "Strong" if mars_sat_diff < 8 else "Moderate",
            })

        # Sun + Saturn
        sun_sat_diff = abs((planets["Sun"]["longitude"] - planets["Saturn"]["longitude"]) % 360)
        if sun_sat_diff < 10 or sun_sat_diff > 350:
            yogas.append({
                "name": "Surya-Shani Yoga",
                "effect": "Leadership crisis, political upheaval, government change",
                "strength": "Strong" if sun_sat_diff < 5 else "Moderate",
            })

        return yogas


def analyze_real_transit(country: str = "India"):
    return RealTransitEngine(country).analyze_transit()


if __name__ == "__main__":
    result = analyze_real_transit("India")
    print("=== REAL TRANSIT ANALYSIS ===")
    print("Country:", result["country"])
    print("Date:", result["date"])
    print()
    print("Birth Chart:")
    print("  Ascendant:", result["birth_chart"]["ascendant"]["rashi"], result["birth_chart"]["ascendant"]["degree"], "deg")
    print()
    print("Transit Planets:")
    for t in result["transit"]:
        print(f"  {t['planet']}: {t['rashi']} {t['degree']} deg (House {t['house']})")
        print(f"      Effect: {t['effect']}")
    print()
    print("Yogas Detected:")
    for y in result["yogas"]:
        print(f"  {y['name']} ({y['strength']})")
        print(f"      {y['effect']}")