"""
VASTU ONE — Transit Enhanced
12-month detailed transit with monthly predictions
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


class TransitEnhancedEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    MONTHS_HINDI = ["जनवरी","फरवरी","मार्च","अप्रैल","मई","जून","जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"]

    # Transit effects by house from Moon
    TRANSIT_EFFECTS = {
        "Surya": {1: "कमजोरी", 2: "धन लाभ", 3: "सफलता", 4: "मानसिक अशांति", 5: "संतान चिंता", 6: "शत्रु नाश", 7: "यात्रा", 8: "रोग", 9: "भाग्य", 10: "करियर", 11: "लाभ", 12: "हानि"},
        "Chandra": {1: "शुभ", 2: "धन", 3: "सफलता", 4: "मानसिक", 5: "शुभ", 6: "अशुभ", 7: "शुभ", 8: "अशुभ", 9: "शुभ", 10: "शुभ", 11: "लाभ", 12: "हानि"},
        "Mangal": {1: "क्रोध", 2: "धन हानि", 3: "विजय", 4: "अशांति", 5: "चिंता", 6: "शत्रु नाश", 7: "कलह", 8: "रोग", 9: "सफलता", 10: "लाभ", 11: "लाभ", 12: "हानि"},
        "Budh": {1: "चंचलता", 2: "धन", 3: "सफलता", 4: "मानसिक", 5: "शुभ", 6: "विवाद", 7: "शुभ", 8: "अशुभ", 9: "शुभ", 10: "शुभ", 11: "लाभ", 12: "हानि"},
        "Guru": {1: "शुभ", 2: "धन वृद्धि", 3: "सफलता", 4: "अशुभ", 5: "संतान", 6: "कठिनाई", 7: "शुभ", 8: "अशुभ", 9: "शुभ", 10: "सफलता", 11: "लाभ", 12: "हानि"},
        "Shukra": {1: "सुख", 2: "धन", 3: "सफलता", 4: "सुख", 5: "शुभ", 6: "कष्ट", 7: "शुभ", 8: "अशुभ", 9: "शुभ", 10: "शुभ", 11: "लाभ", 12: "हानि"},
        "Shani": {1: "कष्ट", 2: "धन हानि", 3: "सफलता", 4: "कष्ट", 5: "चिंता", 6: "शुभ", 7: "कष्ट", 8: "अशुभ", 9: "अशुभ", 10: "अशुभ", 11: "शुभ", 12: "कष्ट"},
        "Rahu": {1: "भ्रम", 2: "धन", 3: "सफलता", 4: "अशांति", 5: "चिंता", 6: "शत्रु नाश", 7: "अशुभ", 8: "अशुभ", 9: "शुभ", 10: "शुभ", 11: "लाभ", 12: "हानि"},
        "Ketu": {1: "अशुभ", 2: "धन हानि", 3: "सफलता", 4: "अशांति", 5: "चिंता", 6: "शुभ", 7: "अशुभ", 8: "शुभ", 9: "शुभ", 10: "अशुभ", 11: "अशुभ", 12: "मोक्ष"},
    }

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict:
        return {
            "current_transits": self._current(),
            "monthly_predictions": self._monthly_predictions(),
            "ingress_dates": self._ingress_dates(),
            "favorable_periods": self._favorable_periods(),
            "challenging_periods": self._challenging_periods(),
        }

    def _current(self) -> List[Dict]:
        results = []
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        lagna_idx = self.SIGNS.index(lagna_rashi) if lagna_rashi in self.SIGNS else 0
        chandra_rashi = self.pos.get("Chandra", {}).get("rashi", "Mesh")
        chandra_idx = self.SIGNS.index(chandra_rashi) if chandra_rashi in self.SIGNS else 0

        for p, info in self.PLANETS_HINDI.items():
            pd = self.pos.get(p, {})
            rashi = pd.get("rashi")
            if not rashi: continue
            rashi_idx = self.SIGNS.index(rashi) if rashi in self.SIGNS else 0
            from_lagna = ((rashi_idx - lagna_idx + 12) % 12) + 1
            from_chandra = ((rashi_idx - chandra_idx + 12) % 12) + 1

            effect_from_moon = self.TRANSIT_EFFECTS.get(p, {}).get(from_chandra, "")

            results.append({
                "planet": p,
                "planet_hindi": info,
                "rashi": rashi,
                "rashi_hindi": self.SIGNS_HINDI[rashi_idx],
                "from_lagna": from_lagna,
                "from_chandra": from_chandra,
                "effect_from_moon": effect_from_moon,
                "nature": "Favorable" if from_lagna in [1,2,3,5,9,10,11] else "Challenging",
            })
        return results

    def _monthly_predictions(self) -> List[Dict]:
        now = datetime.now()
        result = []
        for i in range(12):
            month_date = now + timedelta(days=30*i)
            result.append({
                "month": self.MONTHS_HINDI[month_date.month - 1] + " " + str(month_date.year),
                "month_num": month_date.month,
                "year": month_date.year,
                "highlights": self._month_highlights(month_date.month),
            })
        return result

    def _month_highlights(self, month: int) -> List[str]:
        # Simplified — actual calculation would use ephemeris
        highlights = []
        if month in [3, 4]:
            highlights.append("सूर्य मेष में — नई शुरुआत")
        if month in [6, 7]:
            highlights.append("गुरु का प्रभाव — धन लाभ")
        if month in [9, 10]:
            highlights.append("शनि का प्रभाव — धैर्य")
        if not highlights:
            highlights.append("सामान्य समय — संतुलित")
        return highlights

    def _ingress_dates(self) -> List[Dict]:
        """Approximate ingress dates for major planets"""
        return [
            {"planet": "सूर्य", "dates": "हर महीने 14-16 तारीख"},
            {"planet": "चंद्र", "dates": "हर 2.25 दिन"},
            {"planet": "मंगल", "dates": "हर 45 दिन"},
            {"planet": "बुध", "dates": "हर 25-30 दिन"},
            {"planet": "गुरु", "dates": "हर 12 महीने"},
            {"planet": "शुक्र", "dates": "हर 25-30 दिन"},
            {"planet": "शनि", "dates": "हर 30 महीने"},
            {"planet": "राहु", "dates": "हर 18 महीने"},
            {"planet": "केतु", "dates": "हर 18 महीने"},
        ]

    def _favorable_periods(self) -> List[Dict]:
        return [
            {"period": "सूर्य 3, 6, 10, 11 भाव में", "effect": "करियर, धन लाभ"},
            {"period": "गुरु 2, 5, 7, 9, 11 भाव में", "effect": "धन, संतान, विवाह"},
            {"period": "शुक्र 1, 2, 4, 5, 7, 9, 11 भाव में", "effect": "सुख, ऐश्वर्य"},
            {"period": "चंद्र 1, 2, 4, 5, 7, 9, 11 भाव में", "effect": "मानसिक शांति"},
        ]

    def _challenging_periods(self) -> List[Dict]:
        return [
            {"period": "शनि 1, 4, 7, 8, 12 भाव में", "effect": "विलंब, कष्ट"},
            {"period": "राहु 1, 5, 7, 9 भाव में", "effect": "भ्रम, बाधा"},
            {"period": "मंगल 1, 4, 7, 8, 12 भाव में", "effect": "कलह, दुर्घटना"},
            {"period": "सूर्य 4, 8, 12 भाव में", "effect": "अशांति"},
        ]


def analyze_transit_enhanced(positions, lagna):
    return TransitEnhancedEngine(positions, lagna).analyze_all()
