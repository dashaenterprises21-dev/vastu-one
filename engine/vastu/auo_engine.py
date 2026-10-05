"""
AUO Engine — Vastu One Enterprise
Activity-Usage-Ownership Analysis
"""

import json
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class AUOEngine:
    """Activity-Usage-Ownership analysis for Vastu"""

    def __init__(self):
        # Activity → Direction mapping (Vastu shastra)
        self.activity_map = {
            "sleeping":     {"best": ["SW", "S", "W"],        "avoid": ["NE", "E", "SE"],   "element": "earth"},
            "cooking":      {"best": ["SE", "E", "S"],        "avoid": ["NE", "N", "NW"],   "element": "fire"},
            "eating":       {"best": ["SE", "E", "W"],        "avoid": ["NE", "SW"],        "element": "fire"},
            "bathing":      {"best": ["NE", "E", "N"],        "avoid": ["SW", "SE"],        "element": "water"},
            "toilet":       {"best": ["NW", "W", "SSW"],      "avoid": ["NE", "E", "SE"],   "element": "air"},
            "study":        {"best": ["NE", "E", "N"],        "avoid": ["SW", "S"],         "element": "space"},
            "prayer":       {"best": ["NE", "E", "N"],        "avoid": ["SW", "S", "SE"],   "element": "space"},
            "business":     {"best": ["N", "NE", "E"],        "avoid": ["SW", "S"],         "element": "water"},
            "cash":         {"best": ["N", "NE"],             "avoid": ["S", "SW", "SE"],   "element": "water"},
            "storage":      {"best": ["SW", "W", "S"],        "avoid": ["NE", "E"],         "element": "earth"},
            "entertainment":{"best": ["SE", "E"],             "avoid": ["SW", "NE"],        "element": "fire"},
            "exercise":     {"best": ["E", "NE"],             "avoid": ["SW", "W"],         "element": "fire"},
            "meditation":   {"best": ["NE", "E", "N"],        "avoid": ["S", "SW"],         "element": "space"},
            "guest":        {"best": ["NW", "N"],             "avoid": ["SW", "SE"],        "element": "air"},
            "children":     {"best": ["W", "NW", "N"],        "avoid": ["SW", "SE"],        "element": "air"},
            "elderly":      {"best": ["SW", "S", "W"],        "avoid": ["NE", "E"],         "element": "earth"}
        }

        # Usage → Best direction
        self.usage_map = {
            "residential":   {"primary": ["SW", "S", "W"],    "secondary": ["N", "E"]},
            "commercial":    {"primary": ["N", "NE", "E"],    "secondary": ["SE", "W"]},
            "office":        {"primary": ["N", "NE", "E"],    "secondary": ["SE", "NW"]},
            "industrial":    {"primary": ["SW", "W", "S"],    "secondary": ["SE", "N"]},
            "educational":   {"primary": ["NE", "E", "N"],    "secondary": ["NW", "W"]},
            "healthcare":    {"primary": ["NE", "E", "N"],    "secondary": ["SE", "W"]},
            "hospitality":   {"primary": ["SE", "E", "N"],    "secondary": ["NW", "W"]},
            "storage":       {"primary": ["SW", "W", "S"],    "secondary": ["NW", "N"]},
            "worship":       {"primary": ["NE", "E", "N"],    "secondary": ["NW", "W"]}
        }

        # Ownership → Direction strength
        self.ownership_map = {
            "owner_occupied":  {"strength": "full",   "recommendation": "All remedies apply"},
            "tenant_occupied": {"strength": "partial","recommendation": "Non-structural remedies only"},
            "rented_out":      {"strength": "minimal","recommendation": "Basic remedies + tenant advisory"},
            "family_owned":    {"strength": "shared", "recommendation": "Consensus-based remedies"},
            "partnership":     {"strength": "shared", "recommendation": "Balance both partners' kundli"}
        }

    # ─────────────────────────────────────────
    # 1. ACTIVITY ANALYSIS
    # ─────────────────────────────────────────
    def activity_analysis(self, activity: str, direction: str) -> Dict:
        """Ek activity ka direction ke saath analysis"""
        activity = activity.lower()
        direction = direction.upper()
        if activity not in self.activity_map:
            return {"error": f"Activity '{activity}' not found"}
        info = self.activity_map[activity]
        if direction in info["best"]:
            status = "Ideal ✅"
            score = 95
        elif direction in info["avoid"]:
            status = "Avoid ⚠️"
            score = 25
        else:
            status = "Acceptable ⚠️"
            score = 60
        return {
            "activity": activity,
            "direction": direction,
            "best_directions": info["best"],
            "avoid_directions": info["avoid"],
            "element": info["element"],
            "status": status,
            "score": score
        }

    # ─────────────────────────────────────────
    # 2. USAGE ANALYSIS
    # ─────────────────────────────────────────
    def usage_analysis(self, usage: str, direction: str) -> Dict:
        """Property usage type ka direction analysis"""
        usage = usage.lower()
        direction = direction.upper()
        if usage not in self.usage_map:
            return {"error": f"Usage '{usage}' not found"}
        info = self.usage_map[usage]
        if direction in info["primary"]:
            status = "Ideal ✅"
            score = 90
        elif direction in info["secondary"]:
            status = "Good ✅"
            score = 70
        else:
            status = "Not Recommended ⚠️"
            score = 35
        return {
            "usage": usage,
            "direction": direction,
            "primary_directions": info["primary"],
            "secondary_directions": info["secondary"],
            "status": status,
            "score": score
        }

    # ─────────────────────────────────────────
    # 3. OWNERSHIP ANALYSIS
    # ─────────────────────────────────────────
    def ownership_analysis(self, ownership: str) -> Dict:
        """Ownership type ka analysis"""
        ownership = ownership.lower()
        if ownership not in self.ownership_map:
            return {"error": f"Ownership '{ownership}' not found"}
        info = self.ownership_map[ownership]
        return {
            "ownership": ownership,
            "strength": info["strength"],
            "recommendation": info["recommendation"],
            "remedy_scope": self._remedy_scope(ownership)
        }

    def _remedy_scope(self, ownership: str) -> List[str]:
        scope = {
            "owner_occupied": ["structural", "non_structural", "pooja", "occult", "gemstone"],
            "tenant_occupied": ["non_structural", "pooja", "portable"],
            "rented_out": ["non_structural", "tenant_advisory"],
            "family_owned": ["structural", "non_structural", "pooja"],
            "partnership": ["non_structural", "pooja", "consensus"]
        }
        return scope.get(ownership, [])

    # ─────────────────────────────────────────
    # 4. FULL AUO MATRIX
    # ─────────────────────────────────────────
    def auo_matrix(self, activities: List[Dict], usage: str, ownership: str) -> Dict:
        """
        Complete AUO matrix banao.
        activities = [{"name": "sleeping", "direction": "SW"}, ...]
        """
        activity_results = []
        total_score = 0
        for act in activities:
            res = self.activity_analysis(act["name"], act["direction"])
            if "error" not in res:
                activity_results.append(res)
                total_score += res["score"]

        avg_activity = round(total_score / len(activity_results), 2) if activity_results else 0
        usage_res = self.usage_analysis(usage, activities[0]["direction"] if activities else "N")
        ownership_res = self.ownership_analysis(ownership)

        return {
            "activities": activity_results,
            "activity_avg_score": avg_activity,
            "usage": usage_res,
            "ownership": ownership_res,
            "overall_score": round((avg_activity + usage_res.get("score", 0)) / 2, 2),
            "priority_remedies": self._priority_remedies(activity_results, ownership_res)
        }

    def _priority_remedies(self, activities: List[Dict], ownership: Dict) -> List[Dict]:
        """Weak activities ke liye priority remedies"""
        recs = []
        for act in activities:
            if act["score"] < 60:
                recs.append({
                    "activity": act["activity"],
                    "current_direction": act["direction"],
                    "issue": act["status"],
                    "suggested_direction": act["best_directions"][0],
                    "remedy": f"Shift {act['activity']} to {act['best_directions'][0]} or use {act['element']} element remedy",
                    "scope": ownership.get("strength", "full"),
                    "priority": "HIGH" if act["score"] < 35 else "MEDIUM"
                })
        return sorted(recs, key=lambda x: x["priority"], reverse=True)

    # ─────────────────────────────────────────
    # 5. FULL REPORT
    # ─────────────────────────────────────────
    def full_report(self, activities: List[Dict], usage: str, ownership: str) -> Dict:
        matrix = self.auo_matrix(activities, usage, ownership)
        return {
            "auo_matrix": matrix,
            "summary": {
                "total_activities": len(activities),
                "good_activities": len([a for a in matrix["activities"] if a["score"] >= 70]),
                "weak_activities": len([a for a in matrix["activities"] if a["score"] < 60]),
                "overall_score": matrix["overall_score"]
            }
        }


# ─────────────────────────────────────────
# CLI TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    engine = AUOEngine()
    print("=" * 60)
    print("AUO ENGINE TEST")
    print("=" * 60)

    # Sample activities
    activities = [
        {"name": "sleeping", "direction": "SW"},
        {"name": "cooking", "direction": "SE"},
        {"name": "study", "direction": "NE"},
        {"name": "toilet", "direction": "NW"},
        {"name": "cash", "direction": "S"},
        {"name": "prayer", "direction": "NE"}
    ]

    print("\n1. ACTIVITY ANALYSIS (Sleeping in SW):")
    print(json.dumps(engine.activity_analysis("sleeping", "SW"), indent=2, ensure_ascii=False))

    print("\n2. USAGE ANALYSIS (Residential in SW):")
    print(json.dumps(engine.usage_analysis("residential", "SW"), indent=2, ensure_ascii=False))

    print("\n3. OWNERSHIP ANALYSIS (Owner Occupied):")
    print(json.dumps(engine.ownership_analysis("owner_occupied"), indent=2, ensure_ascii=False))

    print("\n4. AUO MATRIX:")
    matrix = engine.auo_matrix(activities, "residential", "owner_occupied")
    print(f"Activity Avg Score: {matrix['activity_avg_score']}")
    print(f"Overall Score: {matrix['overall_score']}")
    print("\nPriority Remedies:")
    print(json.dumps(matrix["priority_remedies"], indent=2, ensure_ascii=False))

    print("\n5. FULL REPORT SUMMARY:")
    report = engine.full_report(activities, "residential", "owner_occupied")
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))

    print("\n✅ AUO Engine working!")
