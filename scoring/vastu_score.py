"""
Vastu One - Final Vastu Score (7 Components)
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.entrance_audit import EntranceAudit
from engine.ayadi_engine import AyadiEngine


class VastuScore:
    def __init__(self):
        self.weights = {
            "devata_audit": 0.25,
            "element_balance": 0.15,
            "brahma_sthan": 0.15,
            "direction_strength": 0.10,
            "entrance_pada": 0.15,
            "ayadi_shadvarga": 0.10,
            "room_mapping": 0.10,
        }

    def calculate(
        self,
        devata_score=100,
        element_balance_score=100,
        brahma_score=100,
        direction_score=100,
        entrance_result=None,
        ayadi_result=None,
        room_mapping_score=100
    ):
        entrance_score = 100
        if entrance_result:
            if entrance_result.get("status") == "defect":
                severity = entrance_result.get("severity", "medium")
                entrance_score = {"high": 30, "medium": 60, "low": 80}.get(severity, 70)

        ayadi_score = 100
        if ayadi_result:
            grade = ayadi_result.get("grade", "good")
            ayadi_score = {"good": 100, "neutral": 70, "bad": 30}.get(grade, 50)

        total = (
            devata_score * self.weights["devata_audit"] +
            element_balance_score * self.weights["element_balance"] +
            brahma_score * self.weights["brahma_sthan"] +
            direction_score * self.weights["direction_strength"] +
            entrance_score * self.weights["entrance_pada"] +
            ayadi_score * self.weights["ayadi_shadvarga"] +
            room_mapping_score * self.weights["room_mapping"]
        )

        return {
            "total_score": round(total, 2),
            "grade": self.grade(total),
            "breakdown": {
                "devata_audit": devata_score,
                "element_balance": element_balance_score,
                "brahma_sthan": brahma_score,
                "direction_strength": direction_score,
                "entrance_pada": entrance_score,
                "ayadi_shadvarga": ayadi_score,
                "room_mapping": room_mapping_score
            }
        }

    def grade(self, score):
        if score >= 90: return "A+ (Excellent)"
        if score >= 80: return "A (Very Good)"
        if score >= 70: return "B (Good)"
        if score >= 60: return "C (Average)"
        if score >= 50: return "D (Below Average)"
        return "F (Poor - Immediate Remedy Needed)"


if __name__ == "__main__":
    import json
    scorer = VastuScore()
    audit = EntranceAudit()
    ayadi = AyadiEngine()

    entrance = audit.audit_entrance("East", 3)
    ayadi_res = ayadi.calculate(40, 30, 10)

    result = scorer.calculate(
        devata_score=85,
        element_balance_score=75,
        brahma_score=90,
        direction_score=80,
        entrance_result=entrance,
        ayadi_result=ayadi_res,
        room_mapping_score=88
    )

    print("=== FINAL VASTU SCORE (7 Components) ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
