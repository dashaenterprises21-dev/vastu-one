"""
Vastu One - Advanced Remedy Engine v2
3-Tier: Non-Demolition + Pooja + Demolition (last resort)
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


class RemedyEngineV2:
    def __init__(self):
        with open(DATA / "remedies_non_demolition.json", "r", encoding="utf-8") as f:
            self.remedies = json.load(f)
        with open(DATA / "pooja_mantra.json", "r", encoding="utf-8") as f:
            self.poojas = json.load(f)

    def get_remedy(self, defect_key):
        """Get 3-tier remedy for a defect"""
        if defect_key not in self.remedies["remedies"]:
            return None

        defect = self.remedies["remedies"][defect_key]
        remedies = defect.get("remedies", [])

        # Group by tier
        tier1_non_demolition = []
        tier2_pooja = []
        tier3_demolition = []

        for r in remedies:
            if r["type"] == "pooja":
                tier2_pooja.append(r)
            elif r["type"] == "action" and "partition" in r["action"].lower():
                tier3_demolition.append(r)
            else:
                tier1_non_demolition.append(r)

        total_cost = sum(
            int(r.get("cost", "0").replace("₹", "").replace(",", ""))
            for r in remedies
            if "cost" in r
        )

        return {
            "defect": defect["defect"],
            "severity": defect["severity"],
            "problem": defect["problem"],
            "mantra": defect.get("mantra", ""),
            "tier_1_non_demolition": {
                "title": "🟢 Non-Demolition Remedies (Try First)",
                "remedies": tier1_non_demolition,
                "count": len(tier1_non_demolition)
            },
            "tier_2_pooja": {
                "title": "🟡 Pooja & Mantra (If Tier 1 insufficient)",
                "remedies": tier2_pooja,
                "count": len(tier2_pooja)
            },
            "tier_3_demolition": {
                "title": "🔴 Last Resort (Only if absolutely necessary)",
                "remedies": tier3_demolition,
                "count": len(tier3_demolition)
            },
            "total_cost_estimate": f"₹{total_cost}",
            "recommendation": self._recommend(tier1_non_demolition, tier2_pooja, tier3_demolition)
        }

    def _recommend(self, t1, t2, t3):
        if t1:
            return "✅ Start with Tier 1 (non-demolition) remedies - 90% defects fix ho jate hain"
        if t2:
            return "✅ Pooja & mantra se defect fix karo"
        if t3:
            return "⚠️ Demolition last resort hai - pehle sab options try karo"
        return "✅ No remedy needed"

    def list_all_defects(self):
        """List all defect types"""
        return [
            {
                "key": k,
                "defect": v["defect"],
                "severity": v["severity"]
            }
            for k, v in self.remedies["remedies"].items()
        ]


if __name__ == "__main__":
    engine = RemedyEngineV2()
    print("=== ALL DEFECTS ===")
    for d in engine.list_all_defects():
        print(f"  [{d['severity']:6}] {d['key']:25} - {d['defect']}")

    print("\n=== TOILET_NE REMEDY (3-tier) ===")
    result = engine.get_remedy("toilet_NE")
    print(json.dumps(result, indent=2, ensure_ascii=False))
