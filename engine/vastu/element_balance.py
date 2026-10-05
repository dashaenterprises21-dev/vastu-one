"""
5 तत्वों का बैलेंस चेक + स्कोरिंग
हर तत्व का असली स्कोर, वेटेज के साथ।
"""


class ElementBalance:
    # हर तत्व का वेटेज — कितना नुकसान होता है अगर कमज़ोर हो
    ELEMENT_WEIGHTS = {
        "Space": 30,   # सबसे ज़रूरी — ब्रह्मस्थान
        "Water": 20,   # धन, करियर
        "Fire": 20,    # ऊर्जा, फेम
        "Earth": 15,   # स्थिरता
        "Air": 15      # गति, संचार
    }

    def __init__(self, elements_json):
        self.elements = elements_json["elements"]
        self.balance = {e["name"]: 0 for e in self.elements}
        self.zone_hits = {e["name"]: [] for e in self.elements}

    def analyze_zone(self, direction, objects):
        """हर ज़ोन के objects को देखकर तत्व का बैलेंस बदलो"""
        for element in self.elements:
            if direction in element["directions"]:
                for obj in objects:
                    if obj in element["positive_objects"]:
                        self.balance[element["name"]] += 1
                        self.zone_hits[element["name"]].append(
                            f"+ {obj} in {direction}"
                        )
                    elif obj in element["negative_objects"]:
                        self.balance[element["name"]] -= 2
                        self.zone_hits[element["name"]].append(
                            f"- {obj} in {direction}"
                        )
        return self.balance

    def get_imbalance(self):
        """कौन-सा तत्व कमज़ोर/मज़बूत है"""
        weak = [k for k, v in self.balance.items() if v < 0]
        strong = [k for k, v in self.balance.items() if v > 3]
        return {"weak_elements": weak, "strong_elements": strong}

    def calculate_score(self):
        """
        असली स्कोर — हर कमज़ोर तत्व का वेटेज घटाओ।
        100 से शुरू, हर weak तत्व पर उसका वेटेज घटाओ।
        """
        score = 100
        for element, value in self.balance.items():
            if value < 0:
                # कमज़ोर तत्व — उसका वेटेज घटाओ
                score -= self.ELEMENT_WEIGHTS.get(element, 10)
            elif value > 3:
                # बहुत ज़्यादा — थोड़ा penalty
                score -= 5
        return max(0, score)

    def get_remedies(self):
        """कमज़ोर तत्वों के लिए रेमेडी"""
        remedies = []
        weak = self.get_imbalance()["weak_elements"]
        for element in self.elements:
            if element["name"] in weak:
                remedies.append({
                    "element": element["name"],
                    "hindi": element["hindi"],
                    "remedies": element["remedies"],
                    "colors": element["color"]
                })
        return remedies