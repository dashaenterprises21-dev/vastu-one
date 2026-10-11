"""
VASTU ONE — Pitru Dosha Engine
Ancestral karma analysis
"""

from typing import Dict, List


class PitruDoshaEngine:
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    def __init__(self, positions: Dict):
        self.pos = positions

    def analyze_all(self) -> Dict:
        return {
            "has_dosha": self._has_dosha(),
            "reasons": self._reasons(),
            "effects": self._effects(),
            "remedies": self._remedies(),
        }

    def _has_dosha(self) -> bool:
        # Pitru Dosha check: Sun + Rahu/Ketu in 5th/9th, or Sun in 9th with Rahu, etc.
        surya = self.pos.get("Surya", {})
        rahu = self.pos.get("Rahu", {})
        ketu = self.pos.get("Ketu", {})
        shani = self.pos.get("Shani", {})
        surya_bhav = surya.get("bhav")
        rahu_bhav = rahu.get("bhav")
        ketu_bhav = ketu.get("bhav")
        shani_bhav = shani.get("bhav")

        reasons = []
        if surya_bhav in [5, 9] and (rahu_bhav in [5, 9] or ketu_bhav in [5, 9]):
            reasons.append("सूर्य + राहु/केतु 5वें/9वें भाव में")
        if surya_bhav == 9 and shani_bhav in [5, 9]:
            reasons.append("सूर्य + शनि 9वें भाव में")
        if rahu_bhav == 9 or ketu_bhav == 9:
            reasons.append("राहु/केतु 9वें भाव में")
        return len(reasons) > 0

    def _reasons(self) -> List[str]:
        if not self._has_dosha():
            return ["पितृ दोष नहीं है"]
        return [
            "पूर्वजों का अपमान",
            "पितृ पक्ष में श्राद्ध न करना",
            "गाय की हत्या",
            "ब्राह्मण का अपमान",
            "पितरों की अवहेलना",
        ]

    def _effects(self) -> List[str]:
        if not self._has_dosha():
            return ["कोई पितृ दोष नहीं"]
        return [
            "संतान प्राप्ति में बाधा",
            "आर्थिक समस्याएं",
            "पारिवारिक कलह",
            "स्वास्थ्य समस्याएं",
            "करियर में बाधाएं",
            "विवाह में विलंब",
            "बार-बार असफलता",
            "मानसिक अशांति",
        ]

    def _remedies(self) -> List[Dict]:
        if not self._has_dosha():
            return []
        return [
            {"remedy": "पितृ पक्ष में श्राद्ध करें", "type": "Pooja"},
            {"remedy": "गया/प्रयाग में पिंडदान", "type": "Tirth"},
            {"remedy": "ब्राह्मण भोजन कराएं", "type": "Daan"},
            {"remedy": "कौवे को खाना डालें", "type": "Seva"},
            {"remedy": "पीपल को जल चढ़ाएं", "type": "Seva"},
            {"remedy": "गाय को हरा चारा दें", "type": "Seva"},
            {"remedy": "पितृ मंत्र जाप", "type": "Mantra"},
            {"remedy": "महामृत्युंजय जाप", "type": "Mantra"},
        ]


def analyze_pitru_dosha(positions):
    return PitruDoshaEngine(positions).analyze_all()
