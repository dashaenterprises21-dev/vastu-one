"""
VASTU ONE — Yogini Dasha Engine
8 Yogini periods (Mangala, Pingala, Dhanya, Bhramari, Bhadrika, Ulka, Siddha, Sankata)
"""

from datetime import datetime, timedelta
from typing import Dict, List


class YoginiDasha:
    YOGINIS = [
        {"name": "मंगला", "planet": "Chandra", "years": 1},
        {"name": "पिंगला", "planet": "Surya", "years": 2},
        {"name": "धान्या", "planet": "Guru", "years": 3},
        {"name": "भ्रामरी", "planet": "Mangal", "years": 4},
        {"name": "भद्रिका", "planet": "Budh", "years": 5},
        {"name": "उल्का", "planet": "Shani", "years": 6},
        {"name": "सिद्धा", "planet": "Shukra", "years": 7},
        {"name": "संकटा", "planet": "Rahu", "years": 8},
    ]

    def __init__(self, basic: Dict, positions: Dict):
        self.basic = basic
        self.pos = positions

    def analyze_all(self) -> Dict:
        return {
            "current_yogini": self._current(),
            "full_cycle": self._full_cycle(),
            "effects": self._effects(),
        }

    def _current(self) -> Dict:
        # Starting Yogini based on Moon nakshatra
        ch = self.pos.get("Chandra", {})
        nak_num = ch.get("nakshatra_number", 1) or 1
        start_idx = (nak_num - 1) % 8
        return self.YOGINIS[start_idx]

    def _full_cycle(self) -> List[Dict]:
        current = self._current()
        start_idx = self.YOGINIS.index(current)
        cycle = []
        now = datetime.now()
        cum_years = 0
        for i in range(16):  # 2 cycles
            y = self.YOGINIS[(start_idx + i) % 8]
            start_date = now + timedelta(days=365*cum_years)
            end_date = start_date + timedelta(days=365*y["years"])
            cycle.append({
                "yogini": y["name"],
                "planet": y["planet"],
                "years": y["years"],
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "is_current": i == 0,
            })
            cum_years += y["years"]
        return cycle

    def _effects(self) -> List[str]:
        return [
            "मंगला — मानसिक शांति, माता का सहयोग",
            "पिंगला — आत्मविश्वास, पिता का सहयोग",
            "धान्या — धन वृद्धि, ज्ञान",
            "भ्रामरी — साहस, संपत्ति",
            "भद्रिका — बुद्धि, व्यापार",
            "उल्का — कठिनाई, धैर्य",
            "सिद्धा — सफलता, ऐश्वर्य",
            "संकटा — बाधाएं, भ्रम",
        ]


def analyze_yogini_dasha(basic, positions):
    return YoginiDasha(basic, positions).analyze_all()
