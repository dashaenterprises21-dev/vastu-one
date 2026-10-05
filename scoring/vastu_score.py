"""
Vastu Score — 7-Component Scoring System
Vastu compliance score (0-100)
"""

class VastuScore:
    """Vastu compliance scoring — 7 components"""

    def __init__(self):
        # Weights for 7 components
        self.weights = {
            "disha_bal": 0.25,
            "auo": 0.20,
            "element_balance": 0.15,
            "marma": 0.15,
            "devata": 0.10,
            "brahma": 0.10,
            "shastra": 0.05
        }

    def calculate(self, components: dict) -> dict:
        """
        Calculate Vastu score from components.
        components = {
            "disha_bal": 60.31,
            "auo": 86.66,
            "element_balance": 75,
            "marma": 80,
            "devata": 70,
            "brahma": 90,
            "shastra": 85
        }
        """
        total = 0
        breakdown = {}

        for key, weight in self.weights.items():
            score = components.get(key, 50)  # default 50
            contribution = score * weight
            total += contribution
            breakdown[key] = {
                "score": score,
                "weight": weight,
                "contribution": round(contribution, 2)
            }

        total = round(total, 2)

        return {
            "total_score": total,
            "grade": self._grade(total),
            "breakdown": breakdown,
            "status": self._status(total),
            "weak_components": [k for k, v in components.items() if v < 55],
            "strong_components": [k for k, v in components.items() if v >= 75]
        }

    def _grade(self, score: float) -> str:
        if score >= 85: return "A+ (Excellent)"
        if score >= 70: return "A (Good)"
        if score >= 55: return "B (Average)"
        if score >= 40: return "C (Below Average)"
        return "D (Poor)"

    def _status(self, score: float) -> str:
        if score >= 85: return "Excellent Vastu ✅"
        if score >= 70: return "Good Vastu ✅"
        if score >= 55: return "Average Vastu ⚠️"
        if score >= 40: return "Needs Improvement ⚠️"
        return "Critical 🔴"


if __name__ == "__main__":
    import json
    scorer = VastuScore()
    components = {
        "disha_bal": 60.31,
        "auo": 86.66,
        "element_balance": 75,
        "marma": 80,
        "devata": 70,
        "brahma": 90,
        "shastra": 85
    }
    result = scorer.calculate(components)
    print(json.dumps(result, indent=2))
    print("\n✅ Vastu Score working!")
