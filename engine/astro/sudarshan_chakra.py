"""
VASTU ONE — Sudarshan Chakra Engine
Combined chart: Lagna + Chandra + Surya
"""

from typing import Dict, List, Any


class SudarshanChakra:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict[str, Any]:
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        chandra_rashi = self.pos.get("Chandra", {}).get("rashi", "Mesh")
        surya_rashi = self.pos.get("Surya", {}).get("rashi", "Mesh")

        return {
            "lagna_chakra": self._build_chakra(lagna_rashi, "Lagna"),
            "chandra_chakra": self._build_chakra(chandra_rashi, "Chandra"),
            "surya_chakra": self._build_chakra(surya_rashi, "Surya"),
            "combined": self._combined(lagna_rashi, chandra_rashi, surya_rashi),
        }

    def _build_chakra(self, base_rashi: str, name: str) -> Dict:
        base_idx = self.SIGNS.index(base_rashi) if base_rashi in self.SIGNS else 0
        houses = {}
        for b in range(1, 13):
            rashi_idx = (base_idx + b - 1) % 12
            rashi = self.SIGNS[rashi_idx]
            planets = [self.PLANETS_HINDI.get(p, p) for p, pd in self.pos.items() if pd.get("rashi") == rashi]
            houses[b] = {
                "rashi": rashi,
                "rashi_hindi": self.SIGNS_HINDI[rashi_idx],
                "planets": planets,
            }
        return {"name": name, "base_rashi": base_rashi, "houses": houses}

    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    def _combined(self, lagna_rashi, chandra_rashi, surya_rashi) -> List[Dict]:
        l_idx = self.SIGNS.index(lagna_rashi) if lagna_rashi in self.SIGNS else 0
        c_idx = self.SIGNS.index(chandra_rashi) if chandra_rashi in self.SIGNS else 0
        s_idx = self.SIGNS.index(surya_rashi) if surya_rashi in self.SIGNS else 0
        result = []
        for b in range(1, 13):
            result.append({
                "house": b,
                "from_lagna": self.SIGNS_HINDI[(l_idx + b - 1) % 12],
                "from_chandra": self.SIGNS_HINDI[(c_idx + b - 1) % 12],
                "from_surya": self.SIGNS_HINDI[(s_idx + b - 1) % 12],
            })
        return result


def analyze_sudarshan_chakra(positions, lagna):
    return SudarshanChakra(positions, lagna).analyze_all()
