"""
VASTU ONE — Varshphal Enhanced
5-year annual charts with Muntha, Year Lord, Predictions
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


class VarshphalEnhancedEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    # Year lord benefits
    YEAR_LORD_EFFECTS = {
        "Surya": "राजकीय सफलता, पिता का सहयोग, आत्मविश्वास",
        "Chandra": "मानसिक शांति, माता का सहयोग, यात्रा",
        "Mangal": "साहस, संपत्ति, भाई का सहयोग",
        "Budh": "बुद्धि, व्यापार, संवाद",
        "Guru": "धन, संतान, ज्ञान",
        "Shukra": "दांपत्य सुख, ऐश्वर्य, कला",
        "Shani": "करियर, अनुशासन, धैर्य",
        "Rahu": "अचानक लाभ, विदेश यात्रा",
        "Ketu": "आध्यात्मिक, मोक्ष",
    }

    def __init__(self, basic: Dict, positions: Dict, lagna: Dict):
        self.basic = basic
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict:
        return {
            "current_varshphal": self._current_varshphal(),
            "next_5_years": self._next_5_years(),
            "muntha_timeline": self._muntha_timeline(),
        }

    def _current_varshphal(self) -> Dict:
        return self._varshphal_for_year(datetime.now().year)

    def _varshphal_for_year(self, year: int) -> Dict:
        dob = self.basic.get("dob", "1990-01-01")
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
        except:
            birth = datetime(1990, 1, 1)
        age = year - birth.year

        # Muntha moves 1 sign per year from Lagna
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        lagna_idx = self.SIGNS.index(lagna_rashi) if lagna_rashi in self.SIGNS else 0
        muntha_idx = (lagna_idx + age) % 12
        muntha_rashi = self.SIGNS[muntha_idx]

        # Year lord based on Muntha sign
        lords = {"Mesh":"Mangal","Vrishabh":"Shukra","Mithun":"Budh","Kark":"Chandra","Simha":"Surya","Kanya":"Budh","Tula":"Shukra","Vrishchik":"Mangal","Dhanu":"Guru","Makar":"Shani","Kumbh":"Shani","Meen":"Guru"}
        year_lord = lords.get(muntha_rashi, "")

        # Predictions
        predictions = self._generate_predictions(muntha_rashi, year_lord)

        return {
            "year": year,
            "age": age,
            "muntha_rashi": muntha_rashi,
            "muntha_rashi_hindi": self.SIGNS_HINDI[muntha_idx],
            "year_lord": year_lord,
            "year_lord_hindi": self.PLANETS_HINDI.get(year_lord, ""),
            "year_lord_effects": self.YEAR_LORD_EFFECTS.get(year_lord, ""),
            "predictions": predictions,
        }

    def _next_5_years(self) -> List[Dict]:
        current_year = datetime.now().year
        result = []
        for i in range(5):
            year = current_year + i
            v = self._varshphal_for_year(year)
            result.append(v)
        return result

    def _muntha_timeline(self) -> List[Dict]:
        dob = self.basic.get("dob", "1990-01-01")
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
        except:
            birth = datetime(1990, 1, 1)
        current_year = datetime.now().year
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        lagna_idx = self.SIGNS.index(lagna_rashi) if lagna_rashi in self.SIGNS else 0

        result = []
        for i in range(5):
            year = current_year + i
            age = year - birth.year
            muntha_idx = (lagna_idx + age) % 12
            result.append({
                "year": year,
                "age": age,
                "muntha_rashi": self.SIGNS_HINDI[muntha_idx],
            })
        return result

    def _generate_predictions(self, muntha_rashi: str, year_lord: str) -> List[str]:
        preds = []
        preds.append(f"मुंथा {self.SIGNS_HINDI[self.SIGNS.index(muntha_rashi)]} में — इन क्षेत्रों में बदलाव")
        preds.append(f"वर्षेश {self.PLANETS_HINDI.get(year_lord, '')} — {self.YEAR_LORD_EFFECTS.get(year_lord, '')}")

        # Muntha specific
        muntha_effects = {
            "Mesh": "नई शुरुआत, साहस, यात्रा",
            "Vrishabh": "धन लाभ, पारिवारिक सुख",
            "Mithun": "संवाद, व्यापार, भाई-बहन",
            "Kark": "माता, गृह सुख, मानसिक शांति",
            "Simha": "राजकीय, पिता, सम्मान",
            "Kanya": "स्वास्थ्य, सेवा, बुद्धि",
            "Tula": "विवाह, साझेदारी, व्यापार",
            "Vrishchik": "गूढ़ विद्या, अचानक बदलाव",
            "Dhanu": "धर्म, यात्रा, ज्ञान",
            "Makar": "करियर, अनुशासन, परिश्रम",
            "Kumbh": "मित्र, समाज, नवीनता",
            "Meen": "आध्यात्मिक, मोक्ष, ध्यान",
        }
        preds.append(f"मुंथा प्रभाव: {muntha_effects.get(muntha_rashi, '')}")

        return preds


def analyze_varshphal_enhanced(basic, positions, lagna):
    return VarshphalEnhancedEngine(basic, positions, lagna).analyze_all()
