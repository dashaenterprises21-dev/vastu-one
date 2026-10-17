"""
VASTU ONE - Complete Vimshottari Dasha Engine
5 Levels: Maha -> Antar -> Pratyantar -> Sookshma -> Prana
With exact dates, classical references, and effects
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any

from engine.astro.complete_chart_engine import (
    calculate_complete_chart, get_nakshatra, DASHA_ORDER, DASHA_LORDS
)


# Full Vimshottari Dasha sequence with years
DASHA_SEQUENCE = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10),
    ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
]

# Dasha effects (classical)
DASHA_EFFECTS = {
    "Sun": {
        "positive": "Leadership, authority, government favors, fame, father-related matters",
        "negative": "Ego conflicts, government issues, father's health, heart problems",
        "career": "Government jobs, politics, administration, medicine",
        "health": "Heart, eyes, bones, blood pressure",
        "classical_ref": "BPHS Ch. 46  Surya Dasha",
    },
    "Moon": {
        "positive": "Public support, emotional growth, mother-related matters, water resources",
        "negative": "Mental stress, emotional instability, water-related disasters",
        "career": "Public relations, hospitality, nursing, liquids",
        "health": "Mind, lungs, stomach, sleep",
        "classical_ref": "BPHS Ch. 46  Chandra Dasha",
    },
    "Mars": {
        "positive": "Courage, victory over enemies, military success, property gains",
        "negative": "Accidents, conflicts, war, land disputes, bloodshed",
        "career": "Military, police, engineering, surgery, sports",
        "health": "Blood, muscles, injuries, surgery",
        "classical_ref": "BPHS Ch. 46  Mangal Dasha",
    },
    "Mercury": {
        "positive": "Communication, trade, diplomacy, intelligence, writing",
        "negative": "Nervous tension, skin issues, trade disputes",
        "career": "Business, writing, teaching, IT, communication",
        "health": "Nervous system, skin, speech",
        "classical_ref": "BPHS Ch. 46  Budh Dasha",
    },
    "Jupiter": {
        "positive": "Wisdom, prosperity, spiritual growth, children, education",
        "negative": "Over-optimism, weight gain, liver issues",
        "career": "Teaching, law, religion, finance, counseling",
        "health": "Liver, weight, cholesterol",
        "classical_ref": "BPHS Ch. 46  Guru Dasha",
    },
    "Venus": {
        "positive": "Luxury, arts, relationships, wealth, vehicles",
        "negative": "Excess indulgence, kidney issues, relationship problems",
        "career": "Arts, entertainment, luxury goods, cosmetics",
        "health": "Kidneys, reproductive system, eyes",
        "classical_ref": "BPHS Ch. 46  Shukra Dasha",
    },
    "Saturn": {
        "positive": "Discipline, longevity, authority through hard work, spiritual growth",
        "negative": "Delays, obstacles, chronic illness, depression, losses",
        "career": "Labor, mining, construction, law, administration",
        "health": "Bones, joints, chronic diseases, teeth",
        "classical_ref": "BPHS Ch. 46  Shani Dasha",
    },
    "Rahu": {
        "positive": "Sudden gains, foreign travel, technology, unconventional success",
        "negative": "Confusion, deception, sudden losses, foreign conspiracies",
        "career": "Technology, foreign trade, research, aviation",
        "health": "Nervous system, skin, mysterious diseases",
        "classical_ref": "BPHS Ch. 46  Rahu Dasha",
    },
    "Ketu": {
        "positive": "Spiritual awakening, moksha, sudden insights, occult knowledge",
        "negative": "Isolation, losses, sudden events, confusion",
        "career": "Spiritual, occult, research, healing",
        "health": "Mysterious diseases, spiritual crisis",
        "classical_ref": "BPHS Ch. 46  Ketu Dasha",
    },
}


class CompleteVimshottariDasha:
    """Complete 5-level Vimshottari Dasha calculator"""
    
    def __init__(self, chart: Dict, birth_date: datetime):
        self.chart = chart
        self.birth_date = birth_date
        self.moon_lon = chart["planets"]["Moon"]["longitude"]
        self._calculate_base()
    
    def _calculate_base(self):
        """Calculate base dasha positions"""
        nak_size = 360 / 27
        self.nak_idx = int(self.moon_lon / nak_size)
        self.start_dasha_idx = self.nak_idx % 9
        self.progress_in_nak = (self.moon_lon % nak_size) / nak_size
        
        # First dasha years (balance)
        self.first_dasha_years = DASHA_SEQUENCE[self.start_dasha_idx][1] * (1 - self.progress_in_nak)
        
        # Build full timeline (120 years)
        self.timeline = []
        cum_days = 0
        cum_years = 0
        
        for i in range(9):
            idx = (self.start_dasha_idx + i) % 9
            planet, years = DASHA_SEQUENCE[idx]
            if i == 0:
                years = self.first_dasha_years
            
            days = years * 365.25
            start_date = self.birth_date + timedelta(days=cum_days)
            end_date = start_date + timedelta(days=days)
            
            self.timeline.append({
                "planet": planet,
                "lord": DASHA_LORDS.get(planet, planet),
                "years": years,
                "days": days,
                "start_date": start_date,
                "end_date": end_date,
                "start_age": cum_years,
                "end_age": cum_years + years,
            })
            
            cum_days += days
            cum_years += years
    
    def get_mahadasha(self, target_date: datetime = None) -> Dict:
        """Get current Mahadasha"""
        if target_date is None:
            target_date = datetime.now()
        
        for d in self.timeline:
            if d["start_date"] <= target_date < d["end_date"]:
                return d
        return self.timeline[-1]
    
    def get_antardasha(self, maha: Dict, target_date: datetime = None) -> Dict:
        """Get current Antardasha within Mahadasha"""
        if target_date is None:
            target_date = datetime.now()
        
        # Antardasha sequence starts from Mahadasha lord
        maha_idx = next(i for i, d in enumerate(DASHA_SEQUENCE) if d[0] == maha["planet"])
        maha_days = maha["days"]
        
        cum_days = 0
        for i in range(9):
            idx = (maha_idx + i) % 9
            planet, years = DASHA_SEQUENCE[idx]
            antar_days = (maha_days * years) / 120
            start = maha["start_date"] + timedelta(days=cum_days)
            end = start + timedelta(days=antar_days)
            
            if start <= target_date < end:
                return {
                    "planet": planet,
                    "lord": DASHA_LORDS.get(planet, planet),
                    "start_date": start,
                    "end_date": end,
                    "days": antar_days,
                    "years": antar_days / 365.25,
                }
            cum_days += antar_days
        
        return {"planet": "Unknown", "lord": "Unknown"}
    
    def get_pratyantardasha(self, maha: Dict, antar: Dict, target_date: datetime = None) -> Dict:
        """Get current Pratyantardasha within Antardasha"""
        if target_date is None:
            target_date = datetime.now()
        
        antar_idx = next(i for i, d in enumerate(DASHA_SEQUENCE) if d[0] == antar["planet"])
        antar_days = antar["days"]
        
        cum_days = 0
        for i in range(9):
            idx = (antar_idx + i) % 9
            planet, years = DASHA_SEQUENCE[idx]
            prat_days = (antar_days * years) / 120
            start = antar["start_date"] + timedelta(days=cum_days)
            end = start + timedelta(days=prat_days)
            
            if start <= target_date < end:
                return {
                    "planet": planet,
                    "lord": DASHA_LORDS.get(planet, planet),
                    "start_date": start,
                    "end_date": end,
                    "days": prat_days,
                    "years": prat_days / 365.25,
                }
            cum_days += prat_days
        
        return {"planet": "Unknown", "lord": "Unknown"}
    
    def get_sookshma(self, maha: Dict, antar: Dict, prat: Dict, target_date: datetime = None) -> Dict:
        """Get current Sookshma Dasha (4th level)"""
        if target_date is None:
            target_date = datetime.now()
        
        prat_idx = next(i for i, d in enumerate(DASHA_SEQUENCE) if d[0] == prat["planet"])
        prat_days = prat["days"]
        
        cum_days = 0
        for i in range(9):
            idx = (prat_idx + i) % 9
            planet, years = DASHA_SEQUENCE[idx]
            sook_days = (prat_days * years) / 120
            start = prat["start_date"] + timedelta(days=cum_days)
            end = start + timedelta(days=sook_days)
            
            if start <= target_date < end:
                return {
                    "planet": planet,
                    "lord": DASHA_LORDS.get(planet, planet),
                    "start_date": start,
                    "end_date": end,
                    "days": sook_days,
                    "hours": sook_days * 24,
                }
            cum_days += sook_days
        
        return {"planet": "Unknown", "lord": "Unknown"}
    
    def get_prana(self, maha: Dict, antar: Dict, prat: Dict, sook: Dict, target_date: datetime = None) -> Dict:
        """Get current Prana Dasha (5th level)"""
        if target_date is None:
            target_date = datetime.now()
        
        sook_idx = next(i for i, d in enumerate(DASHA_SEQUENCE) if d[0] == sook["planet"])
        sook_days = sook["days"]
        
        cum_days = 0
        for i in range(9):
            idx = (sook_idx + i) % 9
            planet, years = DASHA_SEQUENCE[idx]
            prana_days = (sook_days * years) / 120
            start = sook["start_date"] + timedelta(days=cum_days)
            end = start + timedelta(days=prana_days)
            
            if start <= target_date < end:
                return {
                    "planet": planet,
                    "lord": DASHA_LORDS.get(planet, planet),
                    "start_date": start,
                    "end_date": end,
                    "days": prana_days,
                    "hours": prana_days * 24,
                    "minutes": prana_days * 24 * 60,
                }
            cum_days += prana_days
        
        return {"planet": "Unknown", "lord": "Unknown"}
    
    def get_all_levels(self, target_date: datetime = None) -> Dict:
        """Get all 5 levels of Dasha"""
        if target_date is None:
            target_date = datetime.now()
        
        maha = self.get_mahadasha(target_date)
        antar = self.get_antardasha(maha, target_date)
        prat = self.get_pratyantardasha(maha, antar, target_date)
        sook = self.get_sookshma(maha, antar, prat, target_date)
        prana = self.get_prana(maha, antar, prat, sook, target_date)
        
        age = (target_date - self.birth_date).days / 365.25
        
        # Add effects for each planet
        for level in [maha, antar, prat, sook, prana]:
            p = level.get("planet", "")
            if p in DASHA_EFFECTS:
                level["effects"] = DASHA_EFFECTS[p]
        
        return {
            "target_date": target_date.strftime("%Y-%m-%d %H:%M"),
            "age_years": round(age, 2),
            "moon_nakshatra": self.chart["planets"]["Moon"]["nakshatra"]["name"],
            "moon_nakshatra_lord": self.chart["planets"]["Moon"]["nakshatra"]["lord"],
            "levels": {
                "mahadasha": {
                    "planet": maha["planet"],
                    "lord": maha["lord"],
                    "start_date": maha["start_date"].strftime("%Y-%m-%d"),
                    "end_date": maha["end_date"].strftime("%Y-%m-%d"),
                    "years": round(maha["years"], 2),
                    "effects": DASHA_EFFECTS.get(maha["planet"], {}),
                },
                "antardasha": {
                    "planet": antar["planet"],
                    "lord": antar["lord"],
                    "start_date": antar["start_date"].strftime("%Y-%m-%d"),
                    "end_date": antar["end_date"].strftime("%Y-%m-%d"),
                    "days": round(antar["days"], 1),
                    "effects": DASHA_EFFECTS.get(antar["planet"], {}),
                },
                "pratyantardasha": {
                    "planet": prat["planet"],
                    "lord": prat["lord"],
                    "start_date": prat["start_date"].strftime("%Y-%m-%d"),
                    "end_date": prat["end_date"].strftime("%Y-%m-%d"),
                    "days": round(prat["days"], 1),
                    "effects": DASHA_EFFECTS.get(prat["planet"], {}),
                },
                "sookshma": {
                    "planet": sook["planet"],
                    "lord": sook["lord"],
                    "start_date": sook["start_date"].strftime("%Y-%m-%d"),
                    "end_date": sook["end_date"].strftime("%Y-%m-%d"),
                    "hours": round(sook.get("hours", 0), 1),
                    "effects": DASHA_EFFECTS.get(sook["planet"], {}),
                },
                "prana": {
                    "planet": prana["planet"],
                    "lord": prana["lord"],
                    "start_date": prana["start_date"].strftime("%Y-%m-%d %H:%M"),
                    "end_date": prana["end_date"].strftime("%Y-%m-%d %H:%M"),
                    "hours": round(prana.get("hours", 0), 2),
                    "minutes": round(prana.get("minutes", 0), 0),
                    "effects": DASHA_EFFECTS.get(prana["planet"], {}),
                },
            },
            "full_timeline": [
                {
                    "planet": d["planet"],
                    "lord": d["lord"],
                    "start_date": d["start_date"].strftime("%Y-%m-%d"),
                    "end_date": d["end_date"].strftime("%Y-%m-%d"),
                    "years": round(d["years"], 2),
                    "start_age": round(d["start_age"], 2),
                    "end_age": round(d["end_age"], 2),
                }
                for d in self.timeline
            ],
        }


def get_complete_dasha(country: str = "India", target_date: datetime = None):
    """Convenience function"""
    from engine.astro.predictions_engine import COUNTRY_CHARTS
    
    if country not in COUNTRY_CHARTS:
        return {"error": f"Country not found: {country}"}
    
    data = COUNTRY_CHARTS[country]
    y, m, d = data["date"]
    
    chart = calculate_complete_chart(y, m, d, data["time"], data["lat"], data["lng"])
    birth = datetime(y, m, d)
    
    engine = CompleteVimshottariDasha(chart, birth)
    return engine.get_all_levels(target_date)


if __name__ == "__main__":
    result = get_complete_dasha("India")
    
    print("=" * 70)
    print("COMPLETE VIMSHOTTARI DASHA - INDIA")
    print("=" * 70)
    print(f"Date: {result['target_date']}")
    print(f"Age: {result['age_years']} years")
    print(f"Moon Nakshatra: {result['moon_nakshatra']} (Lord: {result['moon_nakshatra_lord']})")
    print()
    
    for level_name, level in result["levels"].items():
        print(f"=== {level_name.upper()} ===")
        print(f"  Planet: {level['planet']} ({level['lord']})")
        print(f"  Start: {level['start_date']}")
        print(f"  End: {level['end_date']}")
        if "years" in level:
            print(f"  Duration: {level['years']} years")
        elif "days" in level:
            print(f"  Duration: {level['days']} days")
        elif "hours" in level:
            print(f"  Duration: {level['hours']} hours")
        if level.get("effects"):
            print(f"  Positive: {level['effects'].get('positive', '')}")
            print(f"  Negative: {level['effects'].get('negative', '')}")
            print(f"  Reference: {level['effects'].get('classical_ref', '')}")
        print()
