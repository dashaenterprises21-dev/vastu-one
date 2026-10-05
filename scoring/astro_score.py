"""
Astro Score — Kundli, Planets, Dasha scoring
"""

class AstroScore:
    """Astro layer scoring"""

    def __init__(self):
        self.weights = {
            "kundli": 0.30,
            "planets": 0.30,
            "houses": 0.20,
            "dasha": 0.20
        }

    def calculate(self, components: dict) -> dict:
        """Calculate astro score"""
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
            "breakdown": breakdown
        }

    def _grade(self, score: float) -> str:
        if score >= 85: return "A+ (Excellent)"
        if score >= 70: return "A (Good)"
        if score >= 55: return "B (Average)"
        if score >= 40: return "C (Below Average)"
        return "D (Poor)"


if __name__ == "__main__":
    import json
    scorer = AstroScore()
    components = {"kundli": 75, "planets": 80, "houses": 70, "dasha": 65}
    print(json.dumps(scorer.calculate(components), indent=2))
    print("\n✅ Astro Score working!")
