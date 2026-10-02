"""
Vastu One - Pooja & Mantra Engine
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


class PoojaEngine:
    def __init__(self):
        with open(DATA / "pooja_mantra.json", "r", encoding="utf-8") as f:
            self.poojas = json.load(f)

    def get_pooja(self, pooja_name):
        """Get specific pooja details"""
        if pooja_name not in self.poojas["poojas"]:
            return None
        return self.poojas["poojas"][pooja_name]

    def get_pooja_for_defect(self, defect_type):
        """Map defect to appropriate pooja"""
        mapping = {
            "toilet_NE": "Varuna_Pooja",
            "kitchen_NE": "Agni_Pooja",
            "brahma_blocked": "Brahma_Pooja",
            "entrance_wrong": "Ganesh_Pooja",
            "aya_lt_vyaya": "Ganesh_Pooja",
            "general": "Vastu_Purush_Pooja",
            "astro": "Navagrah_Shanti"
        }
        pooja_name = mapping.get(defect_type, "Ganesh_Pooja")
        return {
            "defect": defect_type,
            "pooja_name": pooja_name,
            "details": self.get_pooja(pooja_name)
        }

    def list_all_poojas(self):
        """List all available poojas"""
        return [
            {
                "key": k,
                "hindi": v["hindi"],
                "purpose": v["purpose"],
                "cost": v["cost"]
            }
            for k, v in self.poojas["poojas"].items()
        ]

    def generate_full_puja_plan(self, defects_list):
        """Generate complete puja plan for multiple defects"""
        plan = []
        for defect in defects_list:
            puja = self.get_pooja_for_defect(defect)
            if puja and puja["details"]:
                plan.append({
                    "defect": defect,
                    "pooja": puja["details"]["hindi"],
                    "mantra": puja["details"]["mantra"],
                    "count": puja["details"]["count"],
                    "samagri": puja["details"]["samagri"],
                    "direction": puja["details"]["direction"],
                    "timing": puja["details"]["timing"],
                    "cost": puja["details"]["cost"]
                })

        total = sum(int(p["cost"].replace("₹", "")) for p in plan)
        return {
            "total_poojas": len(plan),
            "total_cost": f"₹{total}",
            "plan": plan
        }


if __name__ == "__main__":
    engine = PoojaEngine()
    print("=== ALL POOJAS ===")
    for p in engine.list_all_poojas():
        print(f"  {p['key']:25} | {p['hindi']:20} | {p['purpose'][:40]}")

    print("\n=== POOJA FOR TOILET_NE ===")
    result = engine.get_pooja_for_defect("toilet_NE")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== FULL PUJA PLAN ===")
    plan = engine.generate_full_puja_plan(["toilet_NE", "kitchen_NE", "entrance_wrong"])
    print(json.dumps(plan, indent=2, ensure_ascii=False))
