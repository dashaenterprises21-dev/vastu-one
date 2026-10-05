"""
Vastu One - MahaVastu Engine
Space Surgery, Pyramids, Marma Technique
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


class MahaVastuEngine:
    def __init__(self):
        with open(DATA / "mahavastu_techniques.json", "r", encoding="utf-8") as f:
            self.techniques = json.load(f)["techniques"]

    def suggest_space_surgery(self, zone, defect_type):
        """Zone ke hisaab se metal strip suggest karo"""
        tech = self.techniques["space_surgery"]
        
        # Marma zone check
        if zone in tech["not_allowed_in"]:
            return {
                "allowed": False,
                "reason": f"{zone} Marma zone hai - Space Surgery allowed nahi",
                "alternative": "Temporary tape use karo"
            }
        
        metal = tech["metals_by_zone"].get(zone, "Copper")
        return {
            "allowed": True,
            "technique": "Space Surgery",
            "metal": metal,
            "width": f"{tech['width_inch']} inch",
            "depth": f"{tech['depth_inch']} inch",
            "instructions": f"{metal} strip ko {zone} zone mein floor mein insert karo",
            "when": tech["when_to_use"],
            "cost_estimate": "1000-2000"
        }

    def suggest_pyramids(self, zone, issue_type):
        """Pyramid count aur material suggest karo"""
        tech = self.techniques["amplifier_pyramid"]
        
        placement = tech["placement"].get(issue_type, {"count": 9, "material": "Copper"})
        
        return {
            "technique": "Amplifier (Pyramids)",
            "count": placement["count"],
            "material": placement["material"],
            "placement": f"{zone} zone mein {placement['count']} {placement['material']} pyramids",
            "cost_estimate": f"{placement['count'] * 500}",
            "not_valid": tech["not_valid"],
            "instructions": "Pyramids ko floor pe level karke place karo. Area clean rakhna."
        }

    def suggest_marma_remedy(self, marma_zone):
        """Marma zone ke liye remedy"""
        tech = self.techniques["marma_technique"]
        point = tech["marma_points"].get(marma_zone, {})
        
        return {
            "zone": marma_zone,
            "effect": point.get("effect", "Serious issues"),
            "remedy": tech["remedy"],
            "not_allowed": tech["not_allowed"],
            "reason": tech["reason"],
            "instructions": "Temporary tape se block karo. Space Surgery MAT karo."
        }

    def get_5_tier_remedy(self, defect_key, zone):
        """Complete 5-tier remedy"""
        return {
            "tier_1_simple": self._simple_remedies(defect_key),
            "tier_2_space_surgery": self.suggest_space_surgery(zone, defect_key),
            "tier_3_pyramids": self.suggest_pyramids(zone, "Cut_Corner"),
            "tier_4_pooja": self._pooja_remedies(defect_key),
            "tier_5_demolition": "Last resort - pehle sab options try karo"
        }

    def _simple_remedies(self, defect_key):
        return ["Sea salt", "Color therapy", "Copper wire", "Tulsi plant"]

    def _pooja_remedies(self, defect_key):
        return {
            "pooja": "Vastu Purush Pooja",
            "mantra": "Om Namo Bhagvati Vaastu Devtay Namah",
            "count": 108
        }


if __name__ == "__main__":
    engine = MahaVastuEngine()
    
    print("=== SPACE SURGERY (NE zone) ===")
    print(json.dumps(engine.suggest_space_surgery("NE", "toilet_block"), indent=2, ensure_ascii=False))
    
    print("\n=== PYRAMIDS (Brahmasthan) ===")
    print(json.dumps(engine.suggest_pyramids("CENTER", "Brahmasthan"), indent=2, ensure_ascii=False))
    
    print("\n=== MARMA REMEDY (SW) ===")
    print(json.dumps(engine.suggest_marma_remedy("legs"), indent=2, ensure_ascii=False))
