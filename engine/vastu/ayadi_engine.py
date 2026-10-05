"""
Vastu One - Ayadi Shadvarga Engine
Building fate math (Aya, Vyaya, Rksa, Yoni, Vara, Tithi)
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


class AyadiEngine:
    def __init__(self):
        with open(DATA / "ayadi_shadvarga.json", "r", encoding="utf-8") as f:
            self.ayadi = json.load(f)

    def calculate(self, length, breadth, height):
        """
        Calculate all 6 Ayadi values
        length, breadth, height: in feet
        """
        aya = (length * 8) / 12
        vyaya = (breadth * 9) / 10
        rksa = (length * 8) / 27
        yoni = (breadth * 3) / 8
        vara = (height * 9) / 7
        tithi = (height * 9) / 30

        # Aya vs Vyaya - most important
        aya_score = aya - vyaya

        if aya_score > 0:
            verdict = "✅ Prosperity (Aya > Vyaya)"
            grade = "good"
        elif aya_score < 0:
            verdict = "❌ Loss (Aya < Vyaya)"
            grade = "bad"
        else:
            verdict = "⚖️ Balanced"
            grade = "neutral"

        return {
            "aya": round(aya, 2),
            "vyaya": round(vyaya, 2),
            "rksa": round(rksa, 2),
            "yoni": round(yoni, 2),
            "vara": round(vara, 2),
            "tithi": round(tithi, 2),
            "aya_vs_vyaya": round(aya_score, 2),
            "verdict": verdict,
            "grade": grade,
            "interpretation": {
                "aya": "Income/Prosperity",
                "vyaya": "Loss/Expenses",
                "rksa": "Nakshatra influence",
                "yoni": "Energy/Vitality",
                "vara": "Weekday influence",
                "tithi": "Lunar day influence"
            }
        }

    def get_remedy(self, aya, vyaya):
        """Get remedy if Aya < Vyaya"""
        if aya >= vyaya:
            return None
        return {
            "problem": "Aya < Vyaya - Financial loss",
            "remedies": [
                "Add partition to change dimensions",
                "Place water fountain in North",
                "Place Kuber yantra",
                "Kuber puja + Laxmi puja",
                "Mantra: Om Shreem Hreem Shreem Kamale Kamalalaye Praseed Praseed"
            ]
        }


if __name__ == "__main__":
    engine = AyadiEngine()
    # Test: 40ft length, 30ft breadth, 10ft height
    result = engine.calculate(40, 30, 10)
    print("=== AYADI SHAVARGA TEST ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Test with loss
    result2 = engine.calculate(25, 40, 10)
    print("\n=== TEST 2 (Loss) ===")
    print(json.dumps(result2, indent=2, ensure_ascii=False))
    remedy = engine.get_remedy(result2["aya"], result2["vyaya"])
    if remedy:
        print("\nRemedy:")
        print(json.dumps(remedy, indent=2, ensure_ascii=False))
