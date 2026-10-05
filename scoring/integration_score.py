"""
Integration Score — Sab layers ko jodkar final score
"""

class IntegrationScore:
    """Master integration scoring"""

    def __init__(self):
        self.weights = {
            "vastu": 0.35,
            "astro": 0.20,
            "numerology": 0.15,
            "disha_bal": 0.10,
            "auo": 0.10,
            "marma": 0.05,
            "occult": 0.05
        }

    def calculate(self, components: dict) -> dict:
        """Calculate integrated score"""
        total = 0
        breakdown = {}
        for key, weight in self.weights.items():
            score = components.get(key, 60)
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
            "weak_areas": [k for k, v in components.items() if v < 55],
            "strong_areas": [k for k, v in components.items() if v >= 75],
            "recommendation": self._recommend(total)
        }

    def _grade(self, score: float) -> str:
        if score >= 85: return "A+ (Excellent)"
        if score >= 70: return "A (Good)"
        if score >= 55: return "B (Average)"
        if score >= 40: return "C (Below Average)"
        return "D (Poor)"

    def _recommend(self, score: float) -> str:
        if score >= 80: return "Property is excellent — maintain current Vastu"
        if score >= 65: return "Property is good — minor remedies suggested"
        if score >= 50: return "Moderate issues — full remedy plan needed"
        return "Critical issues — personal consultation recommended"


if __name__ == "__main__":
    import json
    scorer = IntegrationScore()
    components = {
        "vastu": 75.91,
        "astro": 73.5,
        "numerology": 78,
        "disha_bal": 60.31,
        "auo": 86.66,
        "marma": 80,
        "occult": 85
    }
    print(json.dumps(scorer.calculate(components), indent=2))
    print("\n✅ Integration Score working!")
