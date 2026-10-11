"""
VASTU ONE — Sade Sati Engine
Shani's 7.5 year transit over Moon sign
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


class SadeSatiEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]

    def __init__(self, positions: Dict, basic: Dict):
        self.pos = positions
        self.basic = basic

    def analyze_all(self) -> Dict:
        return {
            "current_status": self._current_status(),
            "phases": self._phases(),
            "effects": self._effects(),
            "remedies": self._remedies(),
            "timeline": self._timeline(),
        }

    def _moon_rashi(self):
        ch = self.pos.get("Chandra", {})
        return ch.get("rashi", "Mesh")

    def _current_status(self) -> Dict:
        moon_rashi = self._moon_rashi()
        # Current Shani transit (approx — should use ephemeris in production)
        shani = self.pos.get("Shani", {})
        shani_rashi = shani.get("rashi", "Makar")
        moon_idx = self.SIGNS.index(moon_rashi) if moon_rashi in self.SIGNS else 0
        shani_idx = self.SIGNS.index(shani_rashi) if shani_rashi in self.SIGNS else 0
        diff = (shani_idx - moon_idx + 12) % 12

        status = "Not in Sade Sati"
        phase = None
        if diff == 11:
            status = "Sade Sati — Rising Phase (1st)"
            phase = 1
        elif diff == 0:
            status = "Sade Sati — Peak Phase (2nd)"
            phase = 2
        elif diff == 1:
            status = "Sade Sati — Setting Phase (3rd)"
            phase = 3
        elif diff == 11:
            status = "Ashtama Shani (8th from Moon)"
        elif diff == 3:
            status = "Kantaka Shani (4th from Moon)"

        return {
            "moon_rashi": moon_rashi,
            "moon_rashi_hindi": self.SIGNS_HINDI[moon_idx],
            "shani_rashi": shani_rashi,
            "shani_rashi_hindi": self.SIGNS_HINDI[shani_idx] if shani_rashi in self.SIGNS else "",
            "status": status,
            "phase": phase,
            "in_sade_sati": phase is not None,
            "diff": diff,
        }

    def _phases(self) -> List[Dict]:
        moon_rashi = self._moon_rashi()
        moon_idx = self.SIGNS.index(moon_rashi) if moon_rashi in self.SIGNS else 0
        phases = []
        # Rising (12th from Moon)
        rising_rashi = self.SIGNS[(moon_idx - 1) % 12]
        peak_rashi = self.SIGNS[moon_idx]
        setting_rashi = self.SIGNS[(moon_idx + 1) % 12]
        phases.append({
            "phase": "Rising (1st)",
            "rashi": rising_rashi,
            "rashi_hindi": self.SIGNS_HINDI[(moon_idx - 1) % 12],
            "duration": "2.5 years",
            "effects": ["Financial pressure", "Health issues", "Mental stress", "Family problems"],
        })
        phases.append({
            "phase": "Peak (2nd)",
            "rashi": peak_rashi,
            "rashi_hindi": self.SIGNS_HINDI[moon_idx],
            "duration": "2.5 years",
            "effects": ["Maximum challenges", "Career obstacles", "Relationship stress", "Health concerns"],
        })
        phases.append({
            "phase": "Setting (3rd)",
            "rashi": setting_rashi,
            "rashi_hindi": self.SIGNS_HINDI[(moon_idx + 1) % 12],
            "duration": "2.5 years",
            "effects": ["Gradual relief", "Financial recovery", "Emotional healing", "New opportunities"],
        })
        return phases

    def _effects(self) -> List[str]:
        status = self._current_status()
        if not status["in_sade_sati"]:
            return ["Sade Sati nahi chal rahi — Shani ka prabhav normal hai"]
        effects = [
            "आर्थिक तंगी और खर्चों में वृद्धि",
            "स्वास्थ्य संबंधी समस्याएं",
            "मानसिक तनाव और चिंता",
            "करियर में बाधाएं",
            "रिश्तों में तनाव",
            "यात्रा और स्थान परिवर्तन",
            "पुराने रोगों का उभरना",
            "धैर्य और सहनशीलता की परीक्षा",
        ]
        return effects

    def _remedies(self) -> List[Dict]:
        return [
            {"remedy": "शनिवार को शनि मंदिर में सरसों का तेल चढ़ाएं", "type": "Pooja"},
            {"remedy": "हनुमान चालीसा नियमित पढ़ें", "type": "Path"},
            {"remedy": "काले तिल, लोहा, कंबल का दान करें", "type": "Daan"},
            {"remedy": "ॐ शं शनैश्चराय नमः — 23,000 बार जाप", "type": "Mantra"},
            {"remedy": "पीपल के पेड़ को जल चढ़ाएं", "type": "Seva"},
            {"remedy": "शनि यंत्र की स्थापना करें", "type": "Yantra"},
            {"remedy": "नीलम रत्न धारण करें (सलाह के बाद)", "type": "Ratna"},
        ]

    def _timeline(self) -> List[Dict]:
        # Approximate — should use ephemeris
        now = datetime.now()
        return [
            {"year": now.year - 2, "event": "Sade Sati शुरू (अनुमानित)"},
            {"year": now.year, "event": "Sade Sati चरम (अनुमानित)"},
            {"year": now.year + 2, "event": "Sade Sati समाप्त (अनुमानित)"},
        ]


def analyze_sade_sati(positions, basic):
    return SadeSatiEngine(positions, basic).analyze_all()
