"""
VASTU ONE — Shadvarga Charts Engine
6 Divisional Charts: D-1, D-2, D-3, D-4, D-7, D-9, D-10
"""

from typing import Dict, List, Any


class ShadvargaEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    VARGA_INFO = {
        "D-1": {"name": "Rashi", "meaning": "Body, General life", "divisor": 1},
        "D-2": {"name": "Hora", "meaning": "Wealth", "divisor": 2},
        "D-3": {"name": "Drekkana", "meaning": "Siblings, Courage", "divisor": 3},
        "D-4": {"name": "Chaturthamsa", "meaning": "Property, Fortune", "divisor": 4},
        "D-7": {"name": "Saptamsa", "meaning": "Children", "divisor": 7},
        "D-9": {"name": "Navamsa", "meaning": "Marriage, Dharma", "divisor": 9},
        "D-10": {"name": "Dashamsa", "meaning": "Career, Profession", "divisor": 10},
    }

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict:
        result = {}
        for varga, info in self.VARGA_INFO.items():
            result[varga] = self._calculate_varga(varga, info)
        return result

    def _calculate_varga(self, varga: str, info: Dict) -> Dict:
        divisor = info["divisor"]
        planets_in_varga = {}

        for planet, pd in self.pos.items():
            lon = pd.get("longitude", 0)
            # Calculate varga sign
            varga_sign_idx = int((lon * divisor) / 30) % 12
            varga_sign = self.SIGNS[varga_sign_idx]
            planets_in_varga[planet] = {
                "planet": planet,
                "hindi": self.PLANETS_HINDI.get(planet, planet),
                "varga_rashi": varga_sign,
                "varga_rashi_hindi": self.SIGNS_HINDI[varga_sign_idx],
                "original_longitude": round(lon, 4),
            }

        # Calculate varga lagna
        lagna_lon = self.lagna.get("lagna_longitude", 0)
        varga_lagna_idx = int((lagna_lon * divisor) / 30) % 12

        return {
            "name": info["name"],
            "meaning": info["meaning"],
            "divisor": divisor,
            "lagna": self.SIGNS[varga_lagna_idx],
            "lagna_hindi": self.SIGNS_HINDI[varga_lagna_idx],
            "planets": planets_in_varga,
        }


def analyze_shadvarga(positions, lagna):
    return ShadvargaEngine(positions, lagna).analyze_all()
