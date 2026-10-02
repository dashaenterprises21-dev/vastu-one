"""
Vastu One - 32 Entrance Padas Audit
Check entrance position against 32 padas
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


class EntranceAudit:
    def __init__(self):
        with open(DATA / "entrance_padas_32.json", "r", encoding="utf-8") as f:
            self.padas = json.load(f)

    def get_pada(self, direction, pada_num):
        """Get specific pada by direction (1-8) and pada number (1-8)"""
        if direction not in self.padas["directions"]:
            return None
        padas_list = self.padas["directions"][direction]
        for p in padas_list:
            if p["pada"] == pada_num:
                return p
        return None

    def audit_entrance(self, entrance_direction, entrance_pada, entrance_degree=None):
        """
        Audit main entrance
        entrance_direction: 'East', 'South', 'West', 'North'
        entrance_pada: 1-8 (which pada within that direction)
        entrance_degree: optional exact degree
        """
        pada = self.get_pada(entrance_direction, entrance_pada)
        if not pada:
            return {"status": "error", "message": "Invalid pada"}

        is_best = pada["best"]
        status = "correct" if is_best else "defect"
        severity = "low" if is_best else ("high" if entrance_pada in [1, 8] else "medium")

        result = {
            "status": status,
            "severity": severity,
            "direction": entrance_direction,
            "pada": entrance_pada,
            "name": pada["name"],
            "hindi": pada["hindi"],
            "effect": pada["effect"],
            "shastra": pada["shastra"],
            "degree": entrance_degree,
            "verdict": "✅ Correct" if is_best else "❌ Defect",
            "message": f"Entrance in {pada['name']} pada - {pada['effect']}"
        }

        if not is_best:
            result["remedy"] = self._get_remedy(entrance_direction, entrance_pada)

        return result

    def _get_remedy(self, direction, pada_num):
        """Get remedy for wrong entrance"""
        remedies = {
            "virtual_entry": "Create alternate path or virtual entry",
            "mirror": "Place mirror to reflect entrance",
            "light": "Place bright light at entrance",
            "copper": "Place copper strip below door",
            "pooja": "Ganesh puja + Vastu Purush puja",
            "mantra": "Om Gan Ganpataye Namaha"
        }
        return remedies

    def list_all_padas(self):
        """Return all 32 padas"""
        result = []
        for direction, padas in self.padas["directions"].items():
            for p in padas:
                result.append({
                    "direction": direction,
                    "pada": p["pada"],
                    "name": p["name"],
                    "hindi": p["hindi"],
                    "best": p["best"],
                    "effect": p["effect"]
                })
        return result


if __name__ == "__main__":
    audit = EntranceAudit()
    print("=== 32 ENTRANCE PADAS TEST ===")
    # Test East pada 3 (Jayanta - BEST)
    result = audit.audit_entrance("East", 3, 95.5)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Test East pada 1 (Shikhi - WORST)
    result = audit.audit_entrance("East", 1)
    print(json.dumps(result, indent=2, ensure_ascii=False))
