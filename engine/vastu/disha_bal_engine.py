"""
Disha Bal Engine — Vastu One Enterprise
16-Zone Directional Strength Analysis
"""

import json
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class DishaBalEngine:
    """16-zone directional strength (Disha Bal) analysis"""

    def __init__(self):
        # 16 directions with their properties
        self.directions = {
            "N":  {"hindi": "उत्तर",     "element": "water", "planet": "Budh",   "angle": 0,   "deity": "Kuber"},
            "NNE":{"hindi": "उत्तर-पूर्व", "element": "water", "planet": "Budh",   "angle": 22.5,"deity": "Kuber"},
            "NE": {"hindi": "ईशान",     "element": "space", "planet": "Guru",   "angle": 45,  "deity": "Ishaan"},
            "ENE":{"hindi": "पूर्व-उत्तर","element": "fire",  "planet": "Surya",  "angle": 67.5,"deity": "Surya"},
            "E":  {"hindi": "पूर्व",     "element": "fire",  "planet": "Surya",  "angle": 90,  "deity": "Indra"},
            "ESE":{"hindi": "पूर्व-दक्षिण","element": "fire","planet": "Mangal", "angle": 112.5,"deity": "Agni"},
            "SE": {"hindi": "आग्नेय",   "element": "fire",  "planet": "Shukra", "angle": 135, "deity": "Agni"},
            "SSE":{"hindi": "दक्षिण-पूर्व","element": "earth","planet": "Mangal","angle": 157.5,"deity": "Yam"},
            "S":  {"hindi": "दक्षिण",   "element": "earth", "planet": "Mangal", "angle": 180, "deity": "Yam"},
            "SSW":{"hindi": "दक्षिण-पश्चिम","element": "earth","planet": "Rahu","angle": 202.5,"deity": "Nairutti"},
            "SW": {"hindi": "नैऋत्य",   "element": "air",   "planet": "Rahu",   "angle": 225, "deity": "Nairutti"},
            "WSW":{"hindi": "पश्चिम-दक्षिण","element": "air","planet": "Shani", "angle": 247.5,"deity": "Varun"},
            "W":  {"hindi": "पश्चिम",   "element": "air",   "planet": "Shani",  "angle": 270, "deity": "Varun"},
            "WNW":{"hindi": "पश्चिम-उत्तर","element": "air", "planet": "Vayu",  "angle": 292.5,"deity": "Vayu"},
            "NW": {"hindi": "वायव्य",   "element": "air",   "planet": "Chandra","angle": 315, "deity": "Vayu"},
            "NNW":{"hindi": "उत्तर-पश्चिम","element": "water","planet": "Budh",  "angle": 337.5,"deity": "Kuber"}
        }

    # ─────────────────────────────────────────
    # 1. DIRECTION INFO
    # ─────────────────────────────────────────
    def direction_info(self, direction: str) -> Dict:
        """Ek direction ki puri info"""
        d = self.directions.get(direction.upper())
        if not d:
            return {"error": f"Direction {direction} not found (16 zones)"}
        return {
            "direction": direction.upper(),
            "hindi": d["hindi"],
            "element": d["element"],
            "planet": d["planet"],
            "angle": d["angle"],
            "deity": d["deity"]
        }

    # ─────────────────────────────────────────
    # 2. DISHA BAL (Directional Strength)
    # ─────────────────────────────────────────
    def disha_bal(self, zone_scores: Dict[str, float]) -> Dict:
        """
        Har zone ka score (0-100) input lo, Disha Bal calculate karo.
        zone_scores example: {"N": 80, "NE": 45, "E": 90, ...}
        """
        result = {}
        total_bal = 0
        for direction, score in zone_scores.items():
            d = self.directions.get(direction.upper())
            if not d:
                continue
            bal = self._calculate_bal(score)
            total_bal += bal["bal_score"]
            result[direction.upper()] = {
                "hindi": d["hindi"],
                "element": d["element"],
                "planet": d["planet"],
                "score": score,
                "bal_score": bal["bal_score"],
                "status": bal["status"],
                "remedy": bal["remedy"]
            }
        avg_bal = round(total_bal / len(result), 2) if result else 0
        return {
            "zones": result,
            "average_bal": avg_bal,
            "overall_status": self._overall_status(avg_bal),
            "weak_zones": [d for d, v in result.items() if v["bal_score"] < 40],
            "strong_zones": [d for d, v in result.items() if v["bal_score"] >= 70]
        }

    def _calculate_bal(self, score: float) -> Dict:
        """Score se bal calculate karo"""
        if score >= 85:
            return {"bal_score": 90, "status": "Excellent ✅", "remedy": "Maintain"}
        elif score >= 70:
            return {"bal_score": 75, "status": "Good ✅", "remedy": "Minor strengthening"}
        elif score >= 50:
            return {"bal_score": 55, "status": "Average ⚠️", "remedy": "Moderate remedy needed"}
        elif score >= 30:
            return {"bal_score": 35, "status": "Weak ⚠️", "remedy": "Strong remedy needed"}
        else:
            return {"bal_score": 15, "status": "Critical 🔴", "remedy": "Immediate correction"}

    def _overall_status(self, avg: float) -> str:
        if avg >= 75:
            return "Strong ✅"
        elif avg >= 50:
            return "Moderate ⚠️"
        else:
            return "Weak 🔴"

    # ─────────────────────────────────────────
    # 3. ZONE ELEMENT BALANCE
    # ─────────────────────────────────────────
    def element_balance(self, zone_scores: Dict[str, float]) -> Dict:
        """5 elements ka balance check karo"""
        element_scores = {"fire": [], "earth": [], "air": [], "water": [], "space": []}
        for direction, score in zone_scores.items():
            d = self.directions.get(direction.upper())
            if d:
                element_scores[d["element"]].append(score)
        result = {}
        for element, scores in element_scores.items():
            if scores:
                avg = round(sum(scores) / len(scores), 2)
                result[element] = {
                    "avg_score": avg,
                    "zones_count": len(scores),
                    "status": "Balanced ✅" if 50 <= avg <= 85 else ("Excess ⚠️" if avg > 85 else "Deficient 🔴")
                }
        return result

    # ─────────────────────────────────────────
    # 4. PLANET STRENGTH (from directions)
    # ─────────────────────────────────────────
    def planet_strength(self, zone_scores: Dict[str, float]) -> Dict:
        """Planets ki strength directions se nikalo"""
        planet_scores = {}
        for direction, score in zone_scores.items():
            d = self.directions.get(direction.upper())
            if d:
                planet = d["planet"]
                if planet not in planet_scores:
                    planet_scores[planet] = []
                planet_scores[planet].append(score)
        result = {}
        for planet, scores in planet_scores.items():
            avg = round(sum(scores) / len(scores), 2)
            result[planet] = {
                "avg_score": avg,
                "status": "Strong ✅" if avg >= 70 else ("Moderate ⚠️" if avg >= 50 else "Weak 🔴"),
                "directions": [d for d in zone_scores if self.directions.get(d.upper(), {}).get("planet") == planet]
            }
        return result

    # ─────────────────────────────────────────
    # 5. RECOMMENDATIONS
    # ─────────────────────────────────────────
    def recommendations(self, disha_result: Dict) -> List[Dict]:
        """Weak zones ke liye remedies"""
        recs = []
        for direction, info in disha_result.get("zones", {}).items():
            if info["bal_score"] < 50:
                d = self.directions.get(direction, {})
                recs.append({
                    "direction": direction,
                    "hindi": d.get("hindi", ""),
                    "element": d.get("element", ""),
                    "planet": d.get("planet", ""),
                    "issue": info["status"],
                    "remedy": self._zone_remedy(direction),
                    "priority": "HIGH" if info["bal_score"] < 35 else "MEDIUM"
                })
        return sorted(recs, key=lambda x: x["priority"], reverse=True)

    def _zone_remedy(self, direction: str) -> str:
        remedies = {
            "N": "Water fountain or blue color in North",
            "NE": "Keep clean, yellow color, Guru mantra",
            "E": "Sunrise visibility, red color, Surya mantra",
            "SE": "Fire element, red/orange, cash counter",
            "S": "Red color, Mangal mantra, avoid water",
            "SW": "Heavy items, earth element, avoid water",
            "W": "Metal items, grey color, Shani mantra",
            "NW": "Air element, white color, Chandra mantra"
        }
        base = direction[:2] if direction[:2] in remedies else direction[0]
        return remedies.get(base, f"Strengthen {direction} zone with appropriate element")

    # ─────────────────────────────────────────
    # 6. FULL REPORT
    # ─────────────────────────────────────────
    def full_report(self, zone_scores: Dict[str, float]) -> Dict:
        disha = self.disha_bal(zone_scores)
        return {
            "disha_bal": disha,
            "element_balance": self.element_balance(zone_scores),
            "planet_strength": self.planet_strength(zone_scores),
            "recommendations": self.recommendations(disha)
        }


# ─────────────────────────────────────────
# CLI TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    engine = DishaBalEngine()
    print("=" * 60)
    print("DISHA BAL ENGINE TEST")
    print("=" * 60)

    # Sample zone scores (0-100)
    zone_scores = {
        "N": 85, "NNE": 70, "NE": 90, "ENE": 60,
        "E": 95, "ESE": 75, "SE": 40, "SSE": 55,
        "S": 65, "SSW": 30, "SW": 25, "WSW": 50,
        "W": 60, "WNW": 45, "NW": 70, "NNW": 80
    }

    print("\n1. NORTH DIRECTION INFO:")
    print(json.dumps(engine.direction_info("N"), indent=2, ensure_ascii=False))

    print("\n2. DISHA BAL:")
    result = engine.disha_bal(zone_scores)
    print(f"Average Bal: {result['average_bal']}")
    print(f"Overall: {result['overall_status']}")
    print(f"Weak Zones: {result['weak_zones']}")
    print(f"Strong Zones: {result['strong_zones']}")

    print("\n3. ELEMENT BALANCE:")
    print(json.dumps(engine.element_balance(zone_scores), indent=2, ensure_ascii=False))

    print("\n4. PLANET STRENGTH:")
    print(json.dumps(engine.planet_strength(zone_scores), indent=2, ensure_ascii=False))

    print("\n5. RECOMMENDATIONS (Top 3):")
    recs = engine.recommendations(result)
    print(json.dumps(recs[:3], indent=2, ensure_ascii=False))

    print("\n✅ Disha Bal Engine working!")
