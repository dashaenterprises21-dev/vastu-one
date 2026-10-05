"""
ब्रह्मस्थान ऑडिट — बृहत्संहिता अध्याय 53 के आधार पर
"""


class BrahmaAudit:
    """
    ब्रह्मस्थान (4,4) — 9 पदों का केंद्र
    बृहत्संहिता 53.67-68: वास्तु पुरुष का दाहिना हाथ/असमानता → धन-पत्नी नाश
    """

    # ब्रह्मस्थान में क्या होने पर क्या असर
    IMPACT_MAP = {
        "toilet": {"score": 15, "reason": "ब्रह्मस्थान में शौचालय → सर्वनाश (Samarangana 48.2 मध्य-प्रवा)"},
        "heavy": {"score": 20, "reason": "ब्रह्मस्थान में भारी वस्तु → वंश वृद्धि रुकती (BST 53.67)"},
        "fire": {"score": 25, "reason": "ब्रह्मस्थान में अग्नि → पावक पद दोष (SAM 48.8)"},
        "water": {"score": 40, "reason": "ब्रह्मस्थान में जल → ब्रह्मा का अपमान, रोग"},
        "clutter": {"score": 35, "reason": "ब्रह्मस्थान में अव्यवस्था → मनोदुःख"},
        "storage": {"score": 45, "reason": "ब्रह्मस्थान में भंडारण → धन रुकता"},
        "bed": {"score": 30, "reason": "ब्रह्मस्थान में शयन → स्वास्थ्य हानि"},
        "open": {"score": 100, "reason": "खुला ब्रह्मस्थान → सर्वोत्तम (Brihat Samhita)"},
        "empty": {"score": 100, "reason": "खाली ब्रह्मस्थान → शुभ"},
        "light": {"score": 95, "reason": "प्रकाश → शुभ"},
        "prayer": {"score": 100, "reason": "पूजा स्थल → सर्वश्रेष्ठ"}
    }

    def __init__(self):
        self.center_object = None
        self.score = 100
        self.issues = []
        self.shastra_ref = None

    def audit_center(self, row, col, object_type):
        if row == 4 and col == 4:
            self.center_object = object_type

            if object_type in self.IMPACT_MAP:
                impact = self.IMPACT_MAP[object_type]
                self.score = impact["score"]
                self.shastra_ref = impact["reason"]
                if impact["score"] < 100:
                    self.issues.append(impact["reason"])
            else:
                self.score = 70
                self.issues.append(f"⚠️ अज्ञात वस्तु {object_type} ब्रह्मस्थान में")

    def calculate_score(self):
        return self.score

    def get_details(self):
        return {
            "center_object": self.center_object,
            "score": self.score,
            "shastra_reason": self.shastra_ref,
            "issues": self.issues
        }