"""Update remedy_engine_v2.py with 5-tier + MahaVastu"""
content = '''"""
Vastu One - Advanced Remedy Engine v3
5-Tier: Simple + Space Surgery + Pyramids + Pooja + Demolition
MahaVastu techniques integrated
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


class RemedyEngineV3:
    def __init__(self):
        with open(DATA / "remedies_non_demolition.json", "r", encoding="utf-8") as f:
            self.remedies = json.load(f)
        with open(DATA / "pooja_mantra.json", "r", encoding="utf-8") as f:
            self.poojas = json.load(f)
        with open(DATA / "mahavastu_techniques.json", "r", encoding="utf-8") as f:
            self.mahavastu = json.load(f)["techniques"]

    def get_5_tier_remedy(self, defect_key, zone="NE"):
        """Complete 5-tier remedy with MahaVastu"""
        if defect_key not in self.remedies["remedies"]:
            return None

        defect = self.remedies["remedies"][defect_key]
        remedies = defect.get("remedies", [])

        # Tier 1: Simple
        tier_1 = [r for r in remedies if r["type"] in ["element", "color", "metal", "plant"]]
        
        # Tier 2: Space Surgery
        tier_2 = self._get_space_surgery(zone, defect_key)
        
        # Tier 3: Pyramids
        tier_3 = self._get_pyramids(zone, defect_key)
        
        # Tier 4: Pooja
        tier_4 = [r for r in remedies if r["type"] == "pooja"]
        
        # Tier 5: Demolition
        tier_5 = [r for r in remedies if r["type"] == "action" and "partition" in r["action"].lower()]

        # Total cost
        costs = []
        for t in [tier_1, tier_4, tier_5]:
            for r in t:
                if "cost" in r:
                    try:
                        costs.append(int(r["cost"].replace("", "").replace(",", "")))
                    except:
                        pass
        if tier_2.get("allowed") and "cost_estimate" in tier_2:
            costs.append(1500)
        if "cost_estimate" in tier_3:
            try:
                costs.append(int(tier_3["cost_estimate"].replace("", "")))
            except:
                pass

        return {
            "defect": defect["defect"],
            "severity": defect["severity"],
            "problem": defect["problem"],
            "mantra": defect.get("mantra", ""),
            "zone": zone,
            "tier_1_simple": {
                "title": "🟢 Tier 1: Simple Fixes",
                "remedies": tier_1,
                "count": len(tier_1)
            },
            "tier_2_space_surgery": {
                "title": "🔵 Tier 2: Space Surgery (Metal Strips)",
                **tier_2
            },
            "tier_3_pyramids": {
                "title": "🟣 Tier 3: Pyramids (Amplifier)",
                **tier_3
            },
            "tier_4_pooja": {
                "title": "🟡 Tier 4: Pooja & Mantra",
                "remedies": tier_4,
                "count": len(tier_4)
            },
            "tier_5_demolition": {
                "title": "🔴 Tier 5: Demolition (Last Resort)",
                "remedies": tier_5,
                "count": len(tier_5)
            },
            "total_cost_estimate": f"{sum(costs)}",
            "recommendation": self._recommend(tier_1, tier_2, tier_3, tier_4, tier_5)
        }

    def _get_space_surgery(self, zone, defect_key):
        """Space Surgery suggestion"""
        tech = self.mahavastu["space_surgery"]
        
        # Marma zones check
        if zone in tech["not_allowed_in"]:
            return {
                "allowed": False,
                "reason": f"{zone} Marma zone hai - Space Surgery allowed nahi",
                "alternative": "Temporary tape use karo"
            }
        
        metal = tech["metals_by_zone"].get(zone, "Copper")
        return {
            "allowed": True,
            "metal": metal,
            "width": f"{tech['width_inch']} inch",
            "depth": f"{tech['depth_inch']} inch",
            "instructions": f"{metal} strip ko {zone} zone mein floor mein insert karo",
            "cost_estimate": "1500"
        }

    def _get_pyramids(self, zone, defect_key):
        """Pyramid suggestion"""
        tech = self.mahavastu["amplifier_pyramid"]
        
        # Default: Cut Corner remedy
        placement = {"count": 9, "material": "Copper"}
        
        return {
            "count": placement["count"],
            "material": placement["material"],
            "placement": f"{zone} zone mein {placement['count']} {placement['material']} pyramids",
            "cost_estimate": f"{placement['count'] * 500}",
            "not_valid": tech["not_valid"],
            "instructions": "Pyramids ko floor pe level karke place karo. Area clean rakhna."
        }

    def _recommend(self, t1, t2, t3, t4, t5):
        if t1:
            return "✅ Tier 1 (Simple) se shuru karo - 60% defects fix ho jate hain"
        if t2.get("allowed"):
            return "✅ Tier 2 (Space Surgery) use karo - deep defects ke liye"
        if t3:
            return "✅ Tier 3 (Pyramids) use karo - energy amplify ke liye"
        if t4:
            return "✅ Tier 4 (Pooja) se defect fix karo"
        return "⚠️ Tier 5 (Demolition) last resort hai"

    def get_marma_remedy(self, marma_zone):
        """Marma zone ke liye remedy"""
        tech = self.mahavastu["marma_technique"]
        point = tech["marma_points"].get(marma_zone, {})
        
        return {
            "zone": marma_zone,
            "effect": point.get("effect", "Serious issues"),
            "remedy": tech["remedy"],
            "not_allowed": tech["not_allowed"],
            "reason": tech["reason"]
        }


if __name__ == "__main__":
    engine = RemedyEngineV3()
    
    print("=== 5-TIER REMEDY (Toilet NE) ===")
    result = engine.get_5_tier_remedy("toilet_NE", "NE")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\\n=== MARMA REMEDY ===")
    marma = engine.get_marma_remedy("legs")
    print(json.dumps(marma, indent=2, ensure_ascii=False))
'''

with open('engine/remedy_engine_v2.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('remedy_engine_v2.py updated to 5-tier!')
