"""
Room-wise Analysis — Complete Vastu Rules
Kitchen, Bedroom, Bathroom, Living, Dining, Store, Balcony, Entrance, Stair, Puja
"""


class RoomAnalysis:
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
        "toilet": {
            "hindi": "शौचालय",
            "best_directions": ["NW", "W", "S"],
            "bad_directions": ["NE", "SE", "CENTER"],
            "shastra": "Brihat Samhita 53.67: ईशान में शौचालय = वंश नाश",
            "reason": "NW वायु तत्व — अपवाह के लिए उत्तम"
        },
        "bathroom": {
            "hindi": "स्नानघर",
            "best_directions": ["NW", "W", "S"],
            "bad_directions": ["NE", "SE", "CENTER"],
            "shastra": "Brihat Samhita 53.67: ईशान में स्नानघर = अशुभ",
            "reason": "NW वायु तत्व — जल के लिए उत्तम"
        },
        "living": {
            "hindi": "बैठक",
            "best_directions": ["N", "E", "NE", "NW"],
            "bad_directions": ["SW", "S"],
            "shastra": "Brihat Samhita: उत्तर-पूर्व बैठक में धन-वृद्धि",
            "reason": "N/E में जल तत्व — संवाद और समृद्धि"
        },
        "dining": {
            "hindi": "भोजन कक्ष",
            "best_directions": ["W", "SW", "S"],
            "bad_directions": ["NE", "SE", "N"],
            "shastra": "Mayamata: भोजन कक्ष पश्चिम में शुभ",
            "reason": "W में पृथ्वी तत्व — भोजन पचाने में सहायक"
        },
        "store": {
            "hindi": "भंडार",
            "best_directions": ["SW", "S", "W"],
            "bad_directions": ["NE", "SE", "N"],
            "shastra": "Samarangana Sutradhara: भंडार दक्षिण-पश्चिम में शुभ",
            "reason": "SW में पृथ्वी तत्व — भंडारण के लिए उत्तम"
        },
        "storage": {
            "hindi": "भंडार",
            "best_directions": ["SW", "S", "W"],
            "bad_directions": ["NE", "SE", "N"],
            "shastra": "Samarangana Sutradhara: भंडार दक्षिण-पश्चिम में शुभ",
            "reason": "SW में पृथ्वी तत्व — भंडारण के लिए उत्तम"
        },
        "balcony": {
            "hindi": "बालकनी",
            "best_directions": ["N", "E", "NE"],
            "bad_directions": ["S", "SW", "W"],
            "shastra": "Mayamata: बालकनी उत्तर-पूर्व में शुभ",
            "reason": "N/E में जल तत्व — प्रकाश और हवा"
        },
        "entrance": {
            "hindi": "प्रवेश द्वार",
            "best_directions": ["N", "E", "NE"],
            "bad_directions": ["S", "SW", "W"],
            "shastra": "Brihat Samhita 53.71: उत्तर-पूर्व प्रवेश शुभ",
            "reason": "N/E में जल तत्व — सकारात्मक ऊर्जा"
        },
        "puja": {
            "hindi": "पूजा स्थल",
            "best_directions": ["NE", "E", "N"],
            "bad_directions": ["S", "SW", "W"],
            "shastra": "Vishwakarma Prakash: ईशान में पूजा = मोक्ष",
            "reason": "NE में जल तत्व — आध्यात्मिक ऊर्जा"
        },
        "stair": {
            "hindi": "सीढ़ी",
            "best_directions": ["S", "SW", "W"],
            "bad_directions": ["NE", "CENTER", "N"],
            "shastra": "Mayamata: सीढ़ी दक्षिण में शुभ",
            "reason": "S में अग्नि तत्व — ऊर्जा का संचार"
        },
        "study": {
            "hindi": "अध्ययन कक्ष",
            "best_directions": ["NE", "E", "N"],
            "bad_directions": ["SW", "S", "W"],
            "shastra": "Brihat Samhita: अध्ययन कक्ष उत्तर-पूर्व में शुभ",
            "reason": "NE में जल तत्व — बुद्धि और ज्ञान"
        },
    }

    def __init__(self):
        self.rooms = []

    def analyze_room(self, room_type, zone):
        """Single room ka dosh check karo"""
        rule = self.ROOM_RULES.get(room_type, {})
        if not rule:
            return {
                "room_type": room_type,
                "status": "unknown",
                "is_defect": False,
                "is_correct": False,
                "zone": zone,
            }
        is_correct = zone in rule.get("best_directions", [])
        is_defect = zone in rule.get("bad_directions", [])
        return {
            "room_type": room_type,
            "room_hindi": rule.get("hindi", room_type),
            "zone": zone,
            "is_correct": is_correct,
            "is_defect": is_defect,
            "status": "correct" if is_correct else ("defect" if is_defect else "neutral"),
            "best_directions": rule.get("best_directions", []),
            "bad_directions": rule.get("bad_directions", []),
            "shastra": rule.get("shastra", ""),
            "reason": rule.get("reason", ""),
            "severity": "high" if is_defect and zone in ["NE", "CENTER"] else ("medium" if is_defect else "low")
        }

    def identify_rooms(self, plan_data, grid):
        """Har object ko uske room type mein categorize karo"""
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
                    "zone": zone, "row": p["row"], "col": p["col"], "object": obj
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
