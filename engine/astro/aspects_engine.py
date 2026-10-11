"""
VASTU ONE — Planetary Aspects (Drishti) Engine
Full Vedic aspect table with strength
"""

from typing import Dict, List


class AspectsEngine:
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]

    # Standard Vedic aspects
    FULL_ASPECTS = {
        "Surya": [7],
        "Chandra": [7],
        "Mangal": [4, 7, 8],
        "Budh": [7],
        "Guru": [5, 7, 9],
        "Shukra": [7],
        "Shani": [3, 7, 10],
        "Rahu": [5, 7, 9],
        "Ketu": [5, 7, 9],
    }

    def __init__(self, positions: Dict):
        self.pos = positions

    def analyze_all(self) -> Dict:
        return {
            "aspects": self._compute_aspects(),
            "summary": self._summary(),
        }

    def _compute_aspects(self) -> List[Dict]:
        results = []
        for p, pd in self.pos.items():
            p_bhav = pd.get("bhav")
            if not p_bhav: continue
            aspects = self.FULL_ASPECTS.get(p, [7])
            for aspect in aspects:
                target_bhav = ((p_bhav - 1 + aspect - 1) % 12) + 1
                # Find planets in target bhava
                for q, qd in self.pos.items():
                    if q == p: continue
                    if qd.get("bhav") == target_bhav:
                        results.append({
                            "from": p,
                            "from_hindi": self.PLANETS_HINDI.get(p, p),
                            "to": q,
                            "to_hindi": self.PLANETS_HINDI.get(q, q),
                            "aspect": aspect,
                            "type": "Full",
                            "bhava": target_bhav,
                        })
        return results

    def _summary(self) -> List[Dict]:
        summary = {}
        for p in self.pos:
            summary[p] = {"hindi": self.PLANETS_HINDI.get(p, p), "aspects": []}
        for a in self._compute_aspects():
            summary[a["from"]]["aspects"].append({
                "to": a["to_hindi"],
                "aspect": a["aspect"],
            })
        return [{"planet": k, **v} for k, v in summary.items() if v["aspects"]]


def analyze_aspects(positions):
    return AspectsEngine(positions).analyze_all()
