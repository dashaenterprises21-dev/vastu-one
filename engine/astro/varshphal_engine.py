"""
VASTU ONE — Varshphal Engine (Annual Chart)
Solar return chart + annual predictions
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


class VarshphalEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    def __init__(self, basic: Dict, positions: Dict):
        self.basic = basic
        self.pos = positions

    def analyze_all(self) -> Dict[str, Any]:
        return {
            "varsha_year": self._varsha_year(),
            "muntha": self._muntha(),
            "year_lord": self._year_lord(),
            "predictions": self._predictions(),
        }

    def _varsha_year(self) -> Dict:
        dob = self.basic.get("dob", "")
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
        except:
            birth = datetime(1990, 1, 1)
        now = datetime.now()
        # Varsha year = current year - birth year
        age = now.year - birth.year
        return {
            "varsha_number": age,
            "current_year": now.year,
            "birth_year": birth.year,
            "age": age,
        }

    def _muntha(self) -> Dict:
        """Muntha — annual ascendant progression"""
        dob = self.basic.get("dob", "")
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
        except:
            birth = datetime(1990, 1, 1)
        now = datetime.now()
        age = now.year - birth.year
        lagna_rashi = self.basic.get("lagna_rashi", "Mesh")
        lagna_idx = self.SIGNS.index(lagna_rashi) if lagna_rashi in self.SIGNS else 0
        # Muntha moves 1 sign per year
        muntha_idx = (lagna_idx + age) % 12
        return {
            "muntha_rashi": self.SIGNS[muntha_idx],
            "muntha_rashi_hindi": self.SIGNS_HINDI[muntha_idx],
            "age": age,
        }

    def _year_lord(self) -> Dict:
        """Year lord based on Muntha"""
        muntha = self._muntha()
        muntha_rashi = muntha["muntha_rashi"]
        lords = {"Mesh":"Mangal","Vrishabh":"Shukra","Mithun":"Budh","Kark":"Chandra","Simha":"Surya","Kanya":"Budh","Tula":"Shukra","Vrishchik":"Mangal","Dhanu":"Guru","Makar":"Shani","Kumbh":"Shani","Meen":"Guru"}
        lord = lords.get(muntha_rashi, "")
        return {
            "lord": lord,
            "lord_hindi": self.PLANETS_HINDI.get(lord, lord),
            "reason": f"मुंथा {muntha['muntha_rashi_hindi']} में — {self.PLANETS_HINDI.get(lord, lord)} वर्षेश",
        }

    def _predictions(self) -> List[str]:
        muntha = self._muntha()
        year_lord = self._year_lord()
        return [
            f"मुंथा: {muntha['muntha_rashi_hindi']}",
            f"वर्षेश: {year_lord['lord_hindi']}",
            f"इस वर्ष {year_lord['lord_hindi']} के क्षेत्रों में विशेष ध्यान दें",
            "मुंथा के अनुसार करियर और धन में परिवर्तन",
            "वर्षेश की स्थिति से वर्ष की दिशा तय होती है",
        ]


def analyze_varshphal(basic, positions):
    return VarshphalEngine(basic, positions).analyze_all()
