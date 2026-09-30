"""
Room-wise Analysis
Kitchen, Bedroom, Bathroom, Living room के लिए specific analysis
"""


class RoomAnalysis:
    # हर room type के लिए शास्त्रीय नियम
    ROOM_RULES = {
        "kitchen": {
            "hindi": "रसोई",
            "best_directions": ["SE", "E", "S"],
            "bad_directions": ["NE", "N", "SW"],
            "shastra": "Samarangana Sutradhara: अग्नि कोण (SE) रसोई के लिए श्रेष्ठ",
            "reason": "रसोई में अग्नि तत्व — SE में अग्नि का वास"
        },
        "bedroom": {
            "hindi": "शयनकक्ष",
            "best_directions": ["SW", "S", "W"],
            "bad_directions": ["NE", "SE", "N"],
            "shastra": "Mayamata: गृहस्वामी का कक्ष दक्षिण-पश्चिम में शुभ",
            "reason": "SW में पृथ्वी तत्व — स्थिरता और नींद"
        },
        "bathroom": {
            "hindi": "शौचालय",
            "best_directions": ["NW", "W", "S"],
            "bad_directions": ["NE", "SE", "CENTER"],
            "shastra": "Brihat Samhita 53.67: ईशान में शौचालय = वंश नाश",
            "reason": "NW वायु तत्व — अपवाह के लिए उत्तम"
        },
        "living": {
            "hindi": "बैठक",
            "best_directions": ["N", "E", "NE", "NW"],
            "bad_directions": ["SW", "S"],
            "shastra": "Brihat Samhita: उत्तर-पूर्व बैठक में धन-वृद्धि",
            "reason": "N/E में जल तत्व — संवाद और समृद्धि"
        },
        "puja": {
            "hindi": "पूजा स्थल",
            "best_directions": ["NE", "E", "N"],
            "bad_directions": ["S", "SW", "W"],
            "shastra": "Vishwakarma Prakash: ईशान में पूजा = मोक्ष",
            "reason": "NE में जल तत्व — आध्यात्मिक ऊर्जा"
        },
        "cash": {
            "hindi": "तिजोरी",
            "best_directions": ["N", "NE", "W"],
            "bad_directions": ["SE", "S", "SW"],
            "shastra": "Samarangana Sutradhara: उत्तर में धन = कुबेर वास",
            "reason": "N में कुबेर — धन का देवता"
        },
        "water": {
            "hindi": "जल स्रोत",
            "best_directions": ["NE", "N", "E"],
            "bad_directions": ["SE", "SW", "S"],
            "shastra": "Mayamata: ईशान में जल = पुण्य",
            "reason": "NE जल तत्व का मूल"
        },
    }

    def __init__(self):
        self.rooms = []

    def identify_rooms(self, plan_data, grid):
        """हर object को उसके room type में categorize करो"""
        room_map = {
            "kitchen": "kitchen", "fire": "kitchen",
            "bed": "bedroom",
            "toilet": "bathroom",
            "cash": "cash", "locker": "cash",
            "water": "water",
            "prayer": "puja",
        }

        found = {}
        for p in plan_data:
            obj = p["object"]
            if obj in room_map:
                room_type = room_map[obj]
                zone = grid.get_zone(p["row"], p["col"])
                found.setdefault(room_type, []).append({
                    "zone": zone,
                    "row": p["row"],
                    "col": p["col"],
                    "object": obj
                })

        results = []
        for room_type, items in found.items():
            rule = self.ROOM_RULES.get(room_type, {})
            for item in items:
                zone = item["zone"]
                is_good = zone in rule.get("best_directions", [])
                is_bad = zone in rule.get("bad_directions", [])

                results.append({
                    "room_type": room_type,
                    "room_hindi": rule.get("hindi", room_type),
                    "zone": zone,
                    "object": item["object"],
                    "row": item["row"],
                    "col": item["col"],
                    "is_correct": is_good,
                    "is_defect": is_bad,
                    "best_directions": rule.get("best_directions", []),
                    "bad_directions": rule.get("bad_directions", []),
                    "shastra": rule.get("shastra", ""),
                    "reason": rule.get("reason", ""),
                    "status": "correct" if is_good else ("defect" if is_bad else "neutral")
                })

        self.rooms = results
        return results

    def get_summary(self):
        correct = sum(1 for r in self.rooms if r["status"] == "correct")
        defects = sum(1 for r in self.rooms if r["status"] == "defect")
        return {
            "total_rooms_analyzed": len(self.rooms),
            "correct_placements": correct,
            "defects": defects,
            "rooms": self.rooms
        }