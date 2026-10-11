"""
VASTU ONE — Graha Maitri Chakra
Planetary friendships: Natural, Temporal, Five-fold
"""

from typing import Dict, List


class GrahaMaitri:
    PLANETS = ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि"}

    # Natural friendships (Naisargika)
    NATURAL_FRIENDS = {
        "Surya": ["Chandra","Mangal","Guru"],
        "Chandra": ["Surya","Budh"],
        "Mangal": ["Surya","Chandra","Guru"],
        "Budh": ["Surya","Shukra"],
        "Guru": ["Surya","Chandra","Mangal"],
        "Shukra": ["Budh","Shani"],
        "Shani": ["Budh","Shukra"],
    }

    NATURAL_ENEMIES = {
        "Surya": ["Shukra","Shani"],
        "Chandra": [],
        "Mangal": ["Budh"],
        "Budh": ["Chandra"],
        "Guru": ["Budh","Shukra"],
        "Shukra": ["Surya","Chandra"],
        "Shani": ["Surya","Chandra","Mangal"],
    }

    # Rashi lords for temporal friendship
    RASHI_LORDS = {
        "Mesh":"Mangal","Vrishabh":"Shukra","Mithun":"Budh","Kark":"Chandra",
        "Simha":"Surya","Kanya":"Budh","Tula":"Shukra","Vrishchik":"Mangal",
        "Dhanu":"Guru","Makar":"Shani","Kumbh":"Shani","Meen":"Guru"
    }

    def __init__(self, positions: Dict):
        self.pos = positions

    def analyze_all(self) -> Dict:
        return {
            "natural": self._natural(),
            "temporal": self._temporal(),
            "five_fold": self._five_fold(),
        }

    def _natural(self) -> Dict:
        result = {}
        for p in self.PLANETS:
            friends = self.NATURAL_FRIENDS.get(p, [])
            enemies = self.NATURAL_ENEMIES.get(p, [])
            neutral = [x for x in self.PLANETS if x != p and x not in friends and x not in enemies]
            result[p] = {
                "hindi": self.PLANETS_HINDI[p],
                "friends": [self.PLANETS_HINDI[f] for f in friends],
                "enemies": [self.PLANETS_HINDI[e] for e in enemies],
                "neutral": [self.PLANETS_HINDI[n] for n in neutral],
            }
        return result

    def _temporal(self) -> Dict:
        result = {}
        for p in self.PLANETS:
            pd = self.pos.get(p, {})
            p_rashi = pd.get("rashi")
            if not p_rashi: continue
            p_idx = list(self.RASHI_LORDS.keys()).index(p_rashi) if p_rashi in self.RASHI_LORDS else 0
            friends = []; enemies = []
            for q in self.PLANETS:
                if p == q: continue
                qd = self.pos.get(q, {})
                q_rashi = qd.get("rashi")
                if not q_rashi: continue
                q_idx = list(self.RASHI_LORDS.keys()).index(q_rashi) if q_rashi in self.RASHI_LORDS else 0
                diff = (q_idx - p_idx + 12) % 12
                if diff in [1, 2, 3, 4, 10, 11]:
                    friends.append(self.PLANETS_HINDI[q])
                elif diff in [0, 5, 6, 7, 8, 9]:
                    enemies.append(self.PLANETS_HINDI[q])
            result[p] = {"friends": friends, "enemies": enemies}
        return result

    def _five_fold(self) -> Dict:
        result = {}
        for p in self.PLANETS:
            nat_f = set(self.NATURAL_FRIENDS.get(p, []))
            nat_e = set(self.NATURAL_ENEMIES.get(p, []))
            temp = self._temporal().get(p, {})
            temp_f = set([k for k, v in self.PLANETS_HINDI.items() if v in temp.get("friends", [])])
            temp_e = set([k for k, v in self.PLANETS_HINDI.items() if v in temp.get("enemies", [])])
            friends = []; best = []; enemies = []; neutral = []
            for q in self.PLANETS:
                if p == q: continue
                nf = q in nat_f; ne = q in nat_e
                tf = q in temp_f; te = q in temp_e
                if (nf and tf) or (nf and not te):
                    best.append(self.PLANETS_HINDI[q])
                elif nf and tf:
                    best.append(self.PLANETS_HINDI[q])
                elif (ne and te) or (ne and not tf):
                    enemies.append(self.PLANETS_HINDI[q])
                elif nf:
                    friends.append(self.PLANETS_HINDI[q])
                elif ne:
                    enemies.append(self.PLANETS_HINDI[q])
                else:
                    neutral.append(self.PLANETS_HINDI[q])
            result[p] = {"best": best, "friends": friends, "neutral": neutral, "enemies": enemies}
        return result


def analyze_graha_maitri(positions):
    return GrahaMaitri(positions).analyze_all()
