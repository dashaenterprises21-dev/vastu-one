"""
VASTU ONE — Transit (Gochar) Engine
12-month planetary forecast
"""

from datetime import datetime, timedelta
from typing import Dict, List


class TransitEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    # Approximate transit years per sign (in months)
    TRANSIT_MONTHS = {
        "Surya": 1, "Chandra": 0.07, "Mangal": 1.5, "Budh": 1,
        "Guru": 12, "Shukra": 1, "Shani": 30, "Rahu": 18, "Ketu": 18,
    }

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict:
        return {
            "current_transits": self._current(),
            "next_12_months": self._next_12_months(),
            "favorable_periods": self._favorable(),
        }

    def _current(self) -> List[Dict]:
        results = []
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        lagna_idx = self.SIGNS.index(lagna_rashi) if lagna_rashi in self.SIGNS else 0
        for p, info in self.PLANETS_HINDI.items():
            pd = self.pos.get(p, {})
            rashi = pd.get("rashi")
            if not rashi: continue
            rashi_idx = self.SIGNS.index(rashi) if rashi in self.SIGNS else 0
            bhava = ((rashi_idx - lagna_idx + 12) % 12) + 1
            results.append({
                "planet": p,
                "planet_hindi": info,
                "rashi": rashi,
                "rashi_hindi": self.SIGNS_HINDI[rashi_idx],
                "bhava": bhava,
                "nature": "Favorable" if bhava in [1,2,3,5,9,10,11] else "Challenging",
            })
        return results

    def _next_12_months(self) -> List[Dict]:
        now = datetime.now()
        results = []
        for i in range(12):
            month = now + timedelta(days=30*i)
            results.append({
                "month": month.strftime("%B %Y"),
                "events": [
                    "Sun transit effects",
                    "Moon cycle effects",
                ],
            })
        return results

    def _favorable(self) -> Dict:
        return {
            "good_periods": [
                "Mars in 3rd, 6th, 11th house",
                "Jupiter in 2nd, 5th, 7th, 9th, 11th house",
                "Venus in 1st, 2nd, 4th, 5th, 7th, 9th, 11th house",
            ],
            "challenging_periods": [
                "Saturn in 1st, 4th, 7th, 8th, 12th house",
                "Rahu in 1st, 5th, 7th, 9th house",
                "Mars in 1st, 4th, 7th, 8th, 12th house",
            ],
        }


def analyze_transit(positions, lagna):
    return TransitEngine(positions, lagna).analyze_all()
