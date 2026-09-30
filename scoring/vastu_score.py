"""
फाइनल वास्तु स्कोर
देवता ऑडिट + तत्व बैलेंस + ब्रह्मस्थान + डायरेक्शन स्ट्रेंथ
"""


class VastuScore:
    def __init__(self):
        # नया असली वेटेज
        self.weights = {
            "devata_audit": 0.35,      # 45 देवता — सबसे ज़रूरी
            "element_balance": 0.20,   # 5 तत्व
            "brahma_sthan": 0.25,      # ब्रह्मस्थान — बहुत ज़रूरी
            "direction_strength": 0.20 # 16 ज़ोन
        }

    def calculate(self, devata_score, element_balance_score,
                  brahma_score, direction_score):
        total = (
            devata_score * self.weights["devata_audit"] +
            element_balance_score * self.weights["element_balance"] +
            brahma_score * self.weights["brahma_sthan"] +
            direction_score * self.weights["direction_strength"]
        )
        return {
            "total_score": round(total, 2),
            "grade": self.grade(total),
            "breakdown": {
                "devata_audit": devata_score,
                "element_balance": element_balance_score,
                "brahma_sthan": brahma_score,
                "direction_strength": direction_score
            },
            "weights": self.weights
        }

    def grade(self, score):
        if score >= 90: return "A+ (Excellent)"
        if score >= 80: return "A (Very Good)"
        if score >= 70: return "B (Good)"
        if score >= 60: return "C (Average)"
        if score >= 50: return "D (Below Average)"
        return "F (Poor - Immediate Remedy Needed)"