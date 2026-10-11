"""
VASTU ONE — Kaal Sarp Dosha Engine
12 types of Kaal Sarp Dosha detection
"""

from typing import Dict, List, Any


class KaalSarpEngine:
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]

    # 12 types of Kaal Sarp
    TYPES = [
        {"name": "अनंत", "from": "Mesh", "to": "Vrishabh"},
        {"name": "कुलिक", "from": "Vrishabh", "to": "Mithun"},
        {"name": "वासुकि", "from": "Mithun", "to": "Kark"},
        {"name": "शंखपाल", "from": "Kark", "to": "Simha"},
        {"name": "पद्म", "from": "Simha", "to": "Kanya"},
        {"name": "महापद्म", "from": "Kanya", "to": "Tula"},
        {"name": "तक्षक", "from": "Tula", "to": "Vrishchik"},
        {"name": "कर्कोटक", "from": "Vrishchik", "to": "Dhanu"},
        {"name": "शंखचूड़", "from": "Dhanu", "to": "Makar"},
        {"name": "घातक", "from": "Makar", "to": "Kumbh"},
        {"name": "विषधर", "from": "Kumbh", "to": "Meen"},
        {"name": "शेषनाग", "from": "Meen", "to": "Mesh"},
    ]

    def __init__(self, positions: Dict):
        self.pos = positions

    def analyze_all(self) -> Dict:
        return {
            "has_dosha": self._has_dosha(),
            "type": self._detect_type(),
            "effects": self._effects(),
            "remedies": self._remedies(),
        }

    def _get_planet_sign_idx(self, planet: str) -> int:
        pd = self.pos.get(planet, {})
        rashi = pd.get("rashi", "")
        return self.SIGNS.index(rashi) if rashi in self.SIGNS else -1

    def _has_dosha(self) -> bool:
        rahu_idx = self._get_planet_sign_idx("Rahu")
        ketu_idx = self._get_planet_sign_idx("Ketu")
        if rahu_idx < 0 or ketu_idx < 0:
            return False
        # All planets should be between Rahu and Ketu
        planets = ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"]
        for p in planets:
            p_idx = self._get_planet_sign_idx(p)
            if p_idx < 0: continue
            # Check if between Rahu and Ketu (going one way)
            if rahu_idx < ketu_idx:
                if not (rahu_idx < p_idx < ketu_idx):
                    return False
            else:
                if not (p_idx > rahu_idx or p_idx < ketu_idx):
                    return False
        return True

    def _detect_type(self) -> Dict:
        rahu_idx = self._get_planet_sign_idx("Rahu")
        if rahu_idx < 0: return {}
        ketu_idx = (rahu_idx + 6) % 12
        for t in self.TYPES:
            if self.SIGNS.index(t["from"]) == rahu_idx:
                return {
                    "name": t["name"],
                    "rahu_rashi": self.SIGNS_HINDI[rahu_idx],
                    "ketu_rashi": self.SIGNS_HINDI[ketu_idx],
                }
        return {}

    def _effects(self) -> List[str]:
        if not self._has_dosha():
            return ["काल सर्प दोष नहीं है — भाग्य अनुकूल है"]
        return [
            "जीवन में बार-बार बाधाएं",
            "आर्थिक अस्थिरता",
            "स्वास्थ्य समस्याएं",
            "विवाह में विलंब",
            "संतान संबंधी चिंताएं",
            "करियर में उतार-चढ़ाव",
            "मानसिक अशांति",
            "पितृ दोष का संकेत",
        ]

    def _remedies(self) -> List[Dict]:
        if not self._has_dosha():
            return []
        return [
            {"remedy": "नाग पंचमी पर नाग-नागिन की पूजा", "type": "Pooja"},
            {"remedy": "महामृत्युंजय मंत्र 1,25,000 बार जाप", "type": "Mantra"},
            {"remedy": "राहु-केतु मंत्र जाप (18,000 + 17,000)", "type": "Mantra"},
            {"remedy": "चांदी का नाग-नागिन घर में रखें", "type": "Yantra"},
            {"remedy": "त्र्यंबकेश्वर में जाकर पूजा", "type": "Tirth"},
            {"remedy": "सर्प दोष निवारण पूजा", "type": "Pooja"},
            {"remedy": "गोमेद रत्न धारण करें", "type": "Ratna"},
        ]


def analyze_kaal_sarp(positions):
    return KaalSarpEngine(positions).analyze_all()
