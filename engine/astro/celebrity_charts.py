"""
Celebrity Charts Engine — Famous Personalities
"""

CELEBRITIES = {
    "Narendra Modi": {
        "category": "Politician", "birth": "1950-09-17", "place": "Vadnagar, Gujarat",
        "sun_sign": "Virgo", "moon_sign": "Scorpio", "ascendant": "Cancer",
        "prediction": {"career": "Strong 10th house — leadership till 2029", "health": "Shani mahadasha — joint issues possible", "wealth": "Dhana yoga — stable finances", "critical_years": [2026, 2027, 2029]},
    },
    "Rahul Gandhi": {
        "category": "Politician", "birth": "1970-06-19", "place": "Delhi",
        "sun_sign": "Gemini", "moon_sign": "Leo", "ascendant": "Leo",
        "prediction": {"career": "Rahu mahadasha — rise 2026-2028", "health": "Good — Surya strong", "wealth": "Mixed — inheritance related", "critical_years": [2026, 2027]},
    },
    "Amit Shah": {
        "category": "Politician", "birth": "1964-10-22", "place": "Mumbai",
        "sun_sign": "Libra", "moon_sign": "Sagittarius", "ascendant": "Sagittarius",
        "prediction": {"career": "Guru mahadasha — powerful position", "health": "Watch 2027", "wealth": "Strong", "critical_years": [2027]},
    },
    "Shah Rukh Khan": {
        "category": "Actor", "birth": "1965-11-02", "place": "New Delhi",
        "sun_sign": "Scorpio", "moon_sign": "Cancer", "ascendant": "Leo",
        "prediction": {"career": "2026 — blockbuster year", "health": "Shani — back issues", "wealth": "Crorepati — growing", "critical_years": [2026, 2028]},
    },
    "Salman Khan": {
        "category": "Actor", "birth": "1965-12-27", "place": "Indore",
        "sun_sign": "Capricorn", "moon_sign": "Sagittarius", "ascendant": "Libra",
        "prediction": {"career": "Mixed — 2026 challenging", "health": "Watch 2026-2027", "wealth": "Stable", "critical_years": [2026, 2027]},
    },
    "Amitabh Bachchan": {
        "category": "Actor", "birth": "1942-10-11", "place": "Allahabad",
        "sun_sign": "Libra", "moon_sign": "Sagittarius", "ascendant": "Leo",
        "prediction": {"career": "Legendary — still going strong", "health": "Watch 2026", "wealth": "Massive", "critical_years": [2026]},
    },
    "Virat Kohli": {
        "category": "Cricketer", "birth": "1988-11-05", "place": "Delhi",
        "sun_sign": "Scorpio", "moon_sign": "Sagittarius", "ascendant": "Capricorn",
        "prediction": {"career": "2026 — farewell year?", "health": "Good", "wealth": "Massive — brand value high", "critical_years": [2026, 2027]},
    },
    "Sachin Tendulkar": {
        "category": "Cricketer", "birth": "1973-04-24", "place": "Mumbai",
        "sun_sign": "Taurus", "moon_sign": "Sagittarius", "ascendant": "Cancer",
        "prediction": {"career": "Post-retirement — stable", "health": "Good", "wealth": "Stable", "critical_years": [2027]},
    },
    "MS Dhoni": {
        "category": "Cricketer", "birth": "1981-07-07", "place": "Ranchi",
        "sun_sign": "Cancer", "moon_sign": "Scorpio", "ascendant": "Libra",
        "prediction": {"career": "Post-retirement — mentor role", "health": "Good", "wealth": "Stable", "critical_years": [2026]},
    },
    "Mukesh Ambani": {
        "category": "Businessman", "birth": "1957-04-19", "place": "Aden, Yemen",
        "sun_sign": "Aries", "moon_sign": "Sagittarius", "ascendant": "Cancer",
        "prediction": {"career": "Expansion 2026-2028", "health": "Watch 2027", "wealth": "Growing — top 10 global", "critical_years": [2027]},
    },
    "Ratan Tata": {
        "category": "Businessman", "birth": "1937-12-28", "place": "Mumbai",
        "sun_sign": "Capricorn", "moon_sign": "Aquarius", "ascendant": "Aries",
        "prediction": {"career": "Legacy — stable", "health": "Watch 2026", "wealth": "Stable", "critical_years": [2026]},
    },
    "Sadhguru": {
        "category": "Spiritual", "birth": "1957-09-03", "place": "Mysore",
        "sun_sign": "Virgo", "moon_sign": "Sagittarius", "ascendant": "Scorpio",
        "prediction": {"career": "Global influence growing", "health": "Good — yogic practices", "wealth": "Foundation growing", "critical_years": [2027]},
    },
    "Sri Sri Ravi Shankar": {
        "category": "Spiritual", "birth": "1956-05-13", "place": "Papanasam, TN",
        "sun_sign": "Taurus", "moon_sign": "Leo", "ascendant": "Cancer",
        "prediction": {"career": "Global peace initiatives", "health": "Good", "wealth": "Stable", "critical_years": [2026]},
    },
}


def get_all_celebrities():
    return [{"name": name, "category": d["category"], "sun_sign": d["sun_sign"], "moon_sign": d["moon_sign"]} for name, d in CELEBRITIES.items()]


def analyze_celebrity(name: str):
    if name not in CELEBRITIES:
        return {"error": f"Celebrity '{name}' not found", "available": list(CELEBRITIES.keys())}
    d = CELEBRITIES[name]
    return {
        "name": name, "category": d["category"], "birth": d["birth"], "place": d["place"],
        "chart": {"sun_sign": d["sun_sign"], "moon_sign": d["moon_sign"], "ascendant": d["ascendant"]},
        "prediction": d["prediction"],
        "disclaimer": "Yeh predictions classical astrology ke hisaab se hain. Educational purpose ke liye.",
    }


def get_celebrities_by_category(category: str):
    return [{"name": name, **d} for name, d in CELEBRITIES.items() if d["category"].lower() == category.lower()]
