"""
Vastu One - Chakra Analyzer
45 देवता + 81 पद + 15 Room शास्त्र Analysis
"""

import json
from pathlib import Path


DEVATAS = [
    "शिखी","पर्जन्य","जयन्त","इन्द्र","सूर्य","सत्य","भूष","आकाश","अनिल",
    "पूषा","वितथ","गृहक्षत","यम","गन्धर्व","भृंगराज","मृग","पितर","दौवारिक",
    "सुग्रीव","पुष्पदन्त","वरुण","असुर","शेष","राजयक्ष्मा","रोग","अहि","मुख्य",
    "भल्लाटक","सोम","सर्प","अदिति","दिति","आप","सावित्र","जय","रुद्र",
    "अर्यमा","सविता","विवस्वान","विबुधाधिप","ब्रह्मा","मित्र","राजयक्ष्मा","पृथ्वीधर","आपवत्स",
    "रोग","अहि","मुख्य","भल्लाटक","सोम","सर्प","अदिति","दिति","आप",
    "सावित्र","जय","रुद्र","अर्यमा","सविता","विवस्वान","विबुधाधिप","मित्र","पृथ्वीधर",
    "आपवत्स","सुग्रीव","पुष्पदन्त","वरुण","असुर","शेष","राजयक्ष्मा","रोग","अहि",
    "मुख्य","भल्लाटक","सोम","सर्प","अदिति","दिति","आप","सावित्री","ब्रह्मा"
]

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_FILE = BASE_DIR / "data" / "room_rules.json"


class ChakraAnalyzer:
    def __init__(self):
        with open(RULES_FILE, "r", encoding="utf-8-sig") as f:
            self.rules = json.load(f)["rules"]

    def analyze(self, rooms, property_type="house", floor="ground", plot_shape="square"):
        """
        rooms: list of {pada, row, col, zone, type, size, note}
        """
        results = []
        correct = 0
        defects = 0
        severe_defects = 0
        total_score = 0

        for room in rooms:
            room_type = room.get("type")
            zone = room.get("zone")
            pada = room.get("pada")

            rule = self.rules.get(room_type)
            if not rule:
                continue

            # Check correctness
            if zone in rule["best_directions"]:
                status = "correct"
                correct += 1
                score = 100
                verdict = "✅ सही स्थान"
            elif zone in rule["bad_directions"]:
                status = "defect"
                defects += 1
                # Severe if toilet in NE or brahma in center
                if room_type == "toilet" and zone == "NE":
                    severe_defects += 1
                    score = 20
                    verdict = "🔴 गंभीर दोष"
                elif zone == "CENTER":
                    severe_defects += 1
                    score = 30
                    verdict = "🔴 गंभीर दोष — ब्रह्मस्थान"
                else:
                    score = 40
                    verdict = "🟡 दोष"
            else:
                status = "neutral"
                score = 70
                verdict = "⚪ सामान्य"

            total_score += score

            results.append({
                "pada": pada,
                "devata": DEVATAS[pada - 1] if 0 < pada <= 81 else "—",
                "zone": zone,
                "room_type": room_type,
                "room_hindi": rule["hindi"],
                "room_icon": rule["icon"],
                "status": status,
                "verdict": verdict,
                "score": score,
                "best_directions": rule["best_directions"],
                "bad_directions": rule["bad_directions"],
                "shastra": rule["shastra"],
                "impact": rule["impact"],
                "remedies": rule["remedies"],
                "size": room.get("size", "medium"),
                "note": room.get("note", "")
            })

        # Calculate overall score
        avg_score = round(total_score / len(rooms), 2) if rooms else 0

        # Grade
        if avg_score >= 90:
            grade = "A+ (Excellent)"
        elif avg_score >= 80:
            grade = "A (Very Good)"
        elif avg_score >= 70:
            grade = "B (Good)"
        elif avg_score >= 60:
            grade = "C (Average)"
        elif avg_score >= 50:
            grade = "D (Below Average)"
        else:
            grade = "F (Poor — Immediate Remedy Needed)"

        # Zone-wise summary
        zone_summary = {}
        for r in results:
            z = r["zone"]
            if z not in zone_summary:
                zone_summary[z] = {"correct": 0, "defect": 0, "neutral": 0, "rooms": []}
            zone_summary[z][r["status"]] += 1
            zone_summary[z]["rooms"].append(r["room_hindi"])

        # Collect all remedies for defects
        all_remedies = []
        for r in results:
            if r["status"] == "defect":
                all_remedies.append({
                    "room": r["room_hindi"],
                    "room_icon": r["room_icon"],
                    "zone": r["zone"],
                    "pada": r["pada"],
                    "devata": r["devata"],
                    "shastra": r["shastra"],
                    "remedies": r["remedies"],
                    "impact": r["impact"]
                })

        return {
            "total_rooms": len(rooms),
            "correct_rooms": correct,
            "defects": defects,
            "severe_defects": severe_defects,
            "overall_score": avg_score,
            "grade": grade,
            "results": results,
            "zone_summary": zone_summary,
            "remedies": all_remedies,
            "property_info": {
                "type": property_type,
                "floor": floor,
                "plot_shape": plot_shape
            }
        }