"""
Numerology Score — Mulank, Bhagyank, Name, Property
"""

class NumerologyScore:
    """Numerology layer scoring"""

    def __init__(self):
        self.weights = {
            "mulank": 0.25,
            "bhagyank": 0.25,
            "name_number": 0.20,
            "property_number": 0.20,
            "compatibility": 0.10
        }

    def calculate(self, components: dict) -> dict:
        """Calculate numerology score"""
        total = 0
        breakdown = {}
        for key, weight in self.weights.items():
            score = components.get(key, 70)
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
            "status": self._status(total)
        }

    def _grade(self, score: float) -> str:
        if score >= 85: return "A+ (Excellent)"
        if score >= 70: return "A (Good)"
        if score >= 55: return "B (Average)"
        if score >= 40: return "C (Below Average)"
        return "D (Poor)"

    def _status(self, score: float) -> str:
        if score >= 85: return "Excellent ✅"
        if score >= 70: return "Good ✅"
        if score >= 55: return "Average ⚠️"
        return "Needs Remedy 🔧"


if __name__ == "__main__":
    import json
    scorer = NumerologyScore()
    components = {
        "mulank": 80,
        "bhagyank": 75,
        "name_number": 65,
        "property_number": 85,
        "compatibility": 90
    }
    print(json.dumps(scorer.calculate(components), indent=2))
    print("\n✅ Numerology Score working!")
