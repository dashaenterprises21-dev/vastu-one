"""
Numerology Engine — Vastu One Enterprise
Mulank, Bhagyank, Name Number (Chaldean + Pythagorean)
"""

import json
import os
from datetime import datetime
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class NumerologyEngine:
    """Numerology layer — Mulank, Bhagyank, Name, Chaldean"""

    def __init__(self):
        with open(os.path.join(DATA_DIR, "numerology_rules.json"), "r", encoding="utf-8-sig") as f:
            self.data = json.load(f)
        self.mulank_data = self.data["mulank"]
        self.chaldean = self.data["chaldean"]
        self.pythagorean = self.data["pythagorean"]

    def mulank(self, dob: str) -> Dict:
        try:
            day = int(dob.split("-")[2])
        except (IndexError, ValueError):
            return {"error": "DOB format: YYYY-MM-DD"}
        root = self._reduce_to_1_9(day)
        info = self.mulank_data.get(str(root), {})
        return {
            "mulank": root,
            "hindi": info.get("hindi", ""),
            "planet": info.get("planet", ""),
            "traits": info.get("traits", ""),
            "lucky_direction": info.get("lucky_direction", ""),
            "lucky_color": info.get("lucky_color", ""),
            "lucky_day": info.get("lucky_day", "")
        }

    def bhagyank(self, dob: str) -> Dict:
        try:
            digits = [int(d) for d in dob if d.isdigit()]
        except ValueError:
            return {"error": "Invalid DOB"}
        total = sum(digits)
        root = self._reduce_to_1_9(total)
        info = self.mulank_data.get(str(root), {})
        return {
            "bhagyank": root,
            "hindi": info.get("hindi", ""),
            "planet": info.get("planet", ""),
            "traits": info.get("traits", ""),
            "lucky_direction": info.get("lucky_direction", "")
        }

    def name_number(self, name: str, system: str = "chaldean") -> Dict:
        name = name.upper().replace(" ", "")
        table = self.chaldean if system == "chaldean" else self.pythagorean
        total = sum(table.get(ch, 0) for ch in name if ch.isalpha())
        root = self._reduce_to_1_9(total)
        info = self.mulank_data.get(str(root), {})
        return {
            "name": name,
            "system": system,
            "total": total,
            "name_number": root,
            "hindi": info.get("hindi", ""),
            "planet": info.get("planet", ""),
            "traits": info.get("traits", "")
        }

    def compatibility(self, num1: int, num2: int) -> Dict:
        friendly = {
            1: [1, 2, 3, 5, 6, 9], 2: [1, 3, 5], 3: [1, 2, 3, 5, 6, 7, 9],
            4: [1, 2, 5, 6, 7], 5: [1, 2, 3, 5, 6, 9], 6: [1, 3, 5, 6, 9],
            7: [1, 2, 3, 5, 6, 7], 8: [5, 6], 9: [1, 2, 3, 5, 6, 9]
        }
        is_friendly = num2 in friendly.get(num1, [])
        return {
            "num1": num1,
            "num2": num2,
            "compatible": is_friendly,
            "verdict": "Friendly ✅" if is_friendly else "Neutral/Challenging ⚠️",
            "remedy": "" if is_friendly else "Name correction or color remedy suggested"
        }

    def property_number_analysis(self, property_number: str) -> Dict:
        digits = [int(d) for d in str(property_number) if d.isdigit()]
        if not digits:
            return {"error": "No digits in property number"}
        total = sum(digits)
        root = self._reduce_to_1_9(total)
        info = self.mulank_data.get(str(root), {})
        return {
            "property_number": property_number,
            "numerology_number": root,
            "hindi": info.get("hindi", ""),
            "planet": info.get("planet", ""),
            "traits": info.get("traits", ""),
            "lucky_direction": info.get("lucky_direction", ""),
            "verdict": self._property_verdict(root)
        }

    def _property_verdict(self, n: int) -> str:
        good = [1, 3, 5, 6, 9]
        neutral = [2, 7]
        return "Auspicious ✅" if n in good else ("Neutral ⚠️" if n in neutral else "Needs Remedy 🔧")

    def vastu_integration(self, mulank: int, bhagyank: int, property_num: str) -> Dict:
        prop = self.property_number_analysis(property_num)
        comp = self.compatibility(mulank, prop.get("numerology_number", 0))
        return {
            "mulank": mulank,
            "bhagyank": bhagyank,
            "property": prop,
            "compatibility": comp,
            "vastu_remedy": self._vastu_remedy(mulank, prop.get("numerology_number", 0))
        }

    def _vastu_remedy(self, mulank: int, prop_num: int) -> str:
        info = self.mulank_data.get(str(mulank), {})
        direction = info.get("lucky_direction", "")
        return f"Strengthen {direction} zone with {info.get('lucky_color', '')} color"

    def full_report(self, dob: str, name: str, property_num: str) -> Dict:
        m = self.mulank(dob)
        b = self.bhagyank(dob)
        n = self.name_number(name)
        p = self.property_number_analysis(property_num)
        return {
            "mulank": m,
            "bhagyank": b,
            "name_number": n,
            "property_number": p,
            "compatibility": self.compatibility(m.get("mulank", 0), b.get("bhagyank", 0)),
            "vastu_integration": self.vastu_integration(m.get("mulank", 0), b.get("bhagyank", 0), property_num)
        }

    def _reduce_to_1_9(self, n: int) -> int:
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n if n > 0 else 9


if __name__ == "__main__":
    engine = NumerologyEngine()
    print("=" * 60)
    print("NUMEROLOGY ENGINE TEST")
    print("=" * 60)

    dob = "1990-05-15"
    name = "Rajesh Kumar"
    prop = "B-204"

    print(f"\nDOB: {dob} | Name: {name} | Property: {prop}")

    print("\n1. MULANK:")
    print(json.dumps(engine.mulank(dob), indent=2, ensure_ascii=False))

    print("\n2. BHAGYANK:")
    print(json.dumps(engine.bhagyank(dob), indent=2, ensure_ascii=False))

    print("\n3. NAME NUMBER (Chaldean):")
    print(json.dumps(engine.name_number(name), indent=2, ensure_ascii=False))

    print("\n4. PROPERTY NUMBER:")
    print(json.dumps(engine.property_number_analysis(prop), indent=2, ensure_ascii=False))

    print("\n5. FULL REPORT:")
    print(json.dumps(engine.full_report(dob, name, prop), indent=2, ensure_ascii=False))

    print("\n✅ Numerology Engine working!")


