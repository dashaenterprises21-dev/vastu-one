"""
Occult Engine — Vastu One Enterprise
Safe Occult Remedies Only — No black magic, no harm
"""

import json
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class OccultEngine:
    """Safe occult remedies — protection, cleansing, grounding"""

    def __init__(self):
        with open(os.path.join(DATA_DIR, "occult_safe_remedies.json"), "r", encoding="utf-8-sig") as f:
            self.data = json.load(f)
        self.safe_remedies = self.data["safe_remedies"]
        self.expert_guidance = self.data["expert_guidance"]
        self.avoid = self.data["avoid"]
        self.daily_practice = self.data["daily_practice"]

    # ─────────────────────────────────────────
    # 1. SAFE REMEDY INFO
    # ─────────────────────────────────────────
    def remedy_info(self, remedy_name: str) -> Dict:
        """Ek safe remedy ki puri info"""
        remedy_name = remedy_name.lower()
        if remedy_name not in self.safe_remedies:
            return {"error": f"Remedy '{remedy_name}' not found. Safe options: {list(self.safe_remedies.keys())}"}
        info = self.safe_remedies[remedy_name]
        return {
            "remedy": remedy_name,
            "hindi": info["hindi"],
            "use": info["use"],
            "purpose": info["purpose"],
            "method": info["method"],
            "cost": info["cost"],
            "safety": "SAFE ✅",
            "expert_needed": False
        }

    # ─────────────────────────────────────────
    # 2. REMEDIES BY PURPOSE
    # ─────────────────────────────────────────
    def remedies_by_purpose(self, purpose: str) -> List[Dict]:
        """Purpose ke hisaab se remedies"""
        purpose = purpose.lower()
        result = []
        for name, info in self.safe_remedies.items():
            if info["purpose"] == purpose:
                result.append({
                    "remedy": name,
                    "hindi": info["hindi"],
                    "method": info["method"],
                    "cost": info["cost"],
                    "use": info["use"]
                })
        return result

    # ─────────────────────────────────────────
    # 3. DAILY PRACTICE SCHEDULE
    # ─────────────────────────────────────────
    def daily_schedule(self) -> Dict:
        """Daily/weekly/monthly occult practice"""
        schedule = {}
        for frequency, remedies in self.daily_practice.items():
            schedule[frequency] = []
            for r in remedies:
                info = self.safe_remedies.get(r, {})
                schedule[frequency].append({
                    "remedy": r,
                    "hindi": info.get("hindi", ""),
                    "method": info.get("method", ""),
                    "cost": info.get("cost", "")
                })
        return schedule

    # ─────────────────────────────────────────
    # 4. EXPERT GUIDANCE
    # ─────────────────────────────────────────
    def expert_guidance_info(self, item: str) -> Dict:
        """Expert guidance wale items (kavach, yantra, gemstone, rudraksha)"""
        item = item.lower()
        if item not in self.expert_guidance:
            return {"error": f"Item '{item}' not found. Options: {list(self.expert_guidance.keys())}"}
        info = self.expert_guidance[item]
        return {
            "item": item,
            "hindi": info["hindi"],
            "purpose": info["purpose"],
            "note": info["note"],
            "cost": info["cost"],
            "safety": "EXPERT GUIDANCE NEEDED ⚠️",
            "expert_needed": True
        }

    # ─────────────────────────────────────────
    # 5. AVOID LIST
    # ─────────────────────────────────────────
    def avoid_list(self) -> Dict:
        """Kya avoid karna chahiye"""
        return {
            "avoid": self.avoid,
            "reason": "These can cause harm, are unethical, or are unsafe",
            "note": "Always prefer safe remedies and expert guidance"
        }

    # ─────────────────────────────────────────
    # 6. SAFE REMEDY PLAN
    # ─────────────────────────────────────────
    def safe_remedy_plan(self, issues: List[str]) -> Dict:
        """Issues ke liye safe remedy plan"""
        issue_to_purpose = {
            "negative_energy": "negative_energy_removal",
            "aura_cleansing": "aura_cleansing",
            "space_purification": "space_purification",
            "grounding": "grounding",
            "protection": "protection"
        }

        plan = {"daily": [], "weekly": [], "15_days": [], "expert": []}

        for issue in issues:
            purpose = issue_to_purpose.get(issue, issue)
            remedies = self.remedies_by_purpose(purpose)
            for r in remedies:
                info = self.safe_remedies[r["remedy"]]
                entry = {
                    "remedy": r["remedy"],
                    "hindi": r["hindi"],
                    "method": r["method"],
                    "cost": r["cost"],
                    "purpose": purpose,
                    "issue": issue
                }
                if info["use"] == "daily":
                    plan["daily"].append(entry)
                elif info["use"] == "weekly":
                    plan["weekly"].append(entry)
                elif info["use"] == "15_days":
                    plan["15_days"].append(entry)

        # Expert items for protection
        if "protection" in issues:
            plan["expert"].append(self.expert_guidance_info("kavach"))
            plan["expert"].append(self.expert_guidance_info("rudraksha"))

        return plan

    # ─────────────────────────────────────────
    # 7. FULL REPORT
    # ─────────────────────────────────────────
    def full_report(self, issues: List[str] = None) -> Dict:
        """Complete occult report"""
        if issues is None:
            issues = ["negative_energy", "aura_cleansing", "protection"]

        return {
            "safe_remedies": self.safe_remedies,
            "daily_schedule": self.daily_schedule(),
            "expert_guidance": self.expert_guidance,
            "avoid_list": self.avoid_list(),
            "safe_remedy_plan": self.safe_remedy_plan(issues),
            "disclaimer": "Ye sirf safe, non-harmful remedies hain. Koi bhi expert guidance wala item (kavach, yantra, gemstone) qualified expert se hi lein."
        }


# ─────────────────────────────────────────
# CLI TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    engine = OccultEngine()
    print("=" * 60)
    print("OCCULT ENGINE TEST (SAFE ONLY)")
    print("=" * 60)

    print("\n1. GUGGAL REMEDY INFO:")
    print(json.dumps(engine.remedy_info("guggal"), indent=2, ensure_ascii=False))

    print("\n2. REMEDIES BY PURPOSE (negative_energy_removal):")
    print(json.dumps(engine.remedies_by_purpose("negative_energy_removal"), indent=2, ensure_ascii=False))

    print("\n3. DAILY SCHEDULE:")
    print(json.dumps(engine.daily_schedule(), indent=2, ensure_ascii=False))

    print("\n4. EXPERT GUIDANCE (Kavach):")
    print(json.dumps(engine.expert_guidance_info("kavach"), indent=2, ensure_ascii=False))

    print("\n5. AVOID LIST:")
    print(json.dumps(engine.avoid_list(), indent=2, ensure_ascii=False))

    print("\n6. SAFE REMEDY PLAN:")
    issues = ["negative_energy", "aura_cleansing", "protection"]
    plan = engine.safe_remedy_plan(issues)
    print(f"Daily: {len(plan['daily'])} remedies")
    print(f"Weekly: {len(plan['weekly'])} remedies")
    print(f"Expert: {len(plan['expert'])} items")
    print(json.dumps(plan["daily"][:2], indent=2, ensure_ascii=False))

    print("\n✅ Occult Engine working!")
