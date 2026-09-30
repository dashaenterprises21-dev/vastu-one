"""
Vastu One - Vastu Analyzer
45 देवता + शास्त्र rules + Remedies
"""

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RULES_FILE = BASE_DIR / "data" / "room_rules.json"


class VastuAnalyzer:
    def __init__(self):
        with open(RULES_FILE, "r", encoding="utf-8-sig") as f:
            self.rules = json.load(f)["rules"]

    def analyze_plan(self, plan_data: dict) -> dict:
        """
        plan_data: Groq का output (rooms + doors + windows + compass)
        """
        rooms = plan_data.get("rooms", [])
        plan_info = plan_data.get("plan_info", {})
        doors = plan_data.get("doors", [])
        windows = plan_data.get("windows", [])

        results = []
        correct = 0
        defects = 0
        severe = 0
        total_score = 0

        for room in rooms:
            room_type = (room.get("type") or "").lower()
            direction = (room.get("approximate_direction") or "C").upper()

            rule = self.rules.get(room_type)
            if not rule:
                # Unknown room — skip
                continue

            # Check correctness
            if direction in rule["best_directions"]:
                status = "correct"
                correct += 1
                score = 100
                verdict = "✅ सही स्थान"
            elif direction in rule["bad_directions"]:
                status = "defect"
                defects += 1

                # Severe defect check
                if room_type == "toilet" and direction in ["NE", "C"]:
                    severe += 1
                    score = 15
                    verdict = "🔴 गंभीर दोष"
                elif room_type == "toilet" and direction in ["N", "SE"]:
                    severe += 1
                    score = 25
                    verdict = "🔴 गंभीर दोष"
                elif room_type == "kitchen" and direction in ["NE", "N"]:
                    severe += 1
                    score = 30
                    verdict = "🔴 गंभीर दोष"
                elif direction == "C":
                    severe += 1
                    score = 30
                    verdict = "🔴 गंभीर दोष — ब्रह्मस्थान"
                else:
                    score = 45
                    verdict = "🟡 दोष"
            else:
                status = "neutral"
                score = 70
                verdict = "⚪ सामान्य"

            total_score += score

            results.append({
                "name": room.get("name", room_type),
                "room_type": room_type,
                "room_hindi": rule["hindi"],
                "room_icon": rule["icon"],
                "direction": direction,
                "dimensions": room.get("dimensions"),
                "position": room.get("position"),
                "status": status,
                "verdict": verdict,
                "score": score,
                "best_directions": rule["best_directions"],
                "bad_directions": rule["bad_directions"],
                "shastra": rule["shastra"],
                "impact": rule["impact"],
                "remedies": rule["remedies"],
            })

        # Overall score
        avg_score = round(total_score / len(results), 2) if results else 0

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
            z = r["direction"]
            if z not in zone_summary:
                zone_summary[z] = {"correct": 0, "defect": 0, "neutral": 0, "rooms": []}
            zone_summary[z][r["status"]] += 1
            zone_summary[z]["rooms"].append(r["room_hindi"])

        # Collect remedies
        all_remedies = []
        for r in results:
            if r["status"] == "defect":
                all_remedies.append({
                    "room": r["name"],
                    "room_hindi": r["room_hindi"],
                    "room_icon": r["room_icon"],
                    "direction": r["direction"],
                    "shastra": r["shastra"],
                    "impact": r["impact"],
                    "remedies": r["remedies"],
                })

        # Main entrance analysis
        entry_analysis = None
        for door in doors:
            if door.get("type", "").lower() == "main entrance":
                entry_pos = door.get("position", "")
                # Extract direction from position
                entry_dir = "SW"  # default from Groq notes
                if "North" in entry_pos:
                    entry_dir = "N"
                elif "South" in entry_pos:
                    entry_dir = "S"
                elif "East" in entry_pos:
                    entry_dir = "E"
                elif "West" in entry_pos:
                    entry_dir = "W"
                elif "North-East" in entry_pos:
                    entry_dir = "NE"
                elif "North-West" in entry_pos:
                    entry_dir = "NW"
                elif "South-East" in entry_pos:
                    entry_dir = "SE"
                elif "South-West" in entry_pos:
                    entry_dir = "SW"

                rule = self.rules.get("main_entry", {})
                is_bad = entry_dir in rule.get("bad_directions", [])

                entry_analysis = {
                    "position": entry_pos,
                    "direction": entry_dir,
                    "status": "defect" if is_bad else "correct",
                    "shastra": rule.get("shastra", {}),
                    "remedies": rule.get("remedies", {}) if is_bad else None,
                }
                break

        return {
            "plan_info": plan_info,
            "total_rooms": len(results),
            "correct_rooms": correct,
            "defects": defects,
            "severe_defects": severe,
            "overall_score": avg_score,
            "grade": grade,
            "results": results,
            "zone_summary": zone_summary,
            "remedies": all_remedies,
            "entry_analysis": entry_analysis,
            "doors": doors,
            "windows": windows,
        }