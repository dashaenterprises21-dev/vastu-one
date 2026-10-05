"""
Marma Engine — Vastu One Enterprise
Exact Marma Points for 81-Pad Grid
"""

import json
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class MarmaEngine:
    """Marma points — exact vital points in 81-pad grid"""

    def __init__(self):
        # 81 Pad Grid — 9x9 with marma points
        # Row 1 = North (top), Row 9 = South (bottom)
        # Col 1 = West (left), Col 9 = East (right)
        self.marma_points = {
            # Brahmasthan (Center) — Most sensitive
            (5, 5): {"name": "Brahmasthan", "hindi": "ब्रह्मस्थान", "type": "central", "element": "space",
                     "importance": "CRITICAL", "remedy": "Keep empty, no heavy items, no toilet"},

            # Main Entrances (Marma)
            (1, 1): {"name": "NW Entrance", "hindi": "वायव्य द्वार", "type": "entrance", "element": "air",
                     "importance": "HIGH", "remedy": "Metal items, white color"},
            (1, 5): {"name": "N Entrance", "hindi": "उत्तर द्वार", "type": "entrance", "element": "water",
                     "importance": "HIGH", "remedy": "Water fountain, blue color"},
            (1, 9): {"name": "NE Entrance", "hindi": "ईशान द्वार", "type": "entrance", "element": "space",
                     "importance": "HIGH", "remedy": "Keep clean, yellow color"},
            (5, 9): {"name": "E Entrance", "hindi": "पूर्व द्वार", "type": "entrance", "element": "fire",
                     "importance": "HIGH", "remedy": "Sunrise visibility, red color"},
            (9, 9): {"name": "SE Entrance", "hindi": "आग्नेय द्वार", "type": "entrance", "element": "fire",
                     "importance": "MEDIUM", "remedy": "Fire element, red/orange"},
            (9, 5): {"name": "S Entrance", "hindi": "दक्षिण द्वार", "type": "entrance", "element": "earth",
                     "importance": "MEDIUM", "remedy": "Red color, Mangal mantra"},
            (9, 1): {"name": "SW Entrance", "hindi": "नैऋत्य द्वार", "type": "entrance", "element": "air",
                     "importance": "MEDIUM", "remedy": "Heavy items, earth element"},
            (5, 1): {"name": "W Entrance", "hindi": "पश्चिम द्वार", "type": "entrance", "element": "air",
                     "importance": "MEDIUM", "remedy": "Metal items, grey color"},

            # Kitchen Marma (SE)
            (8, 8): {"name": "Kitchen Fire", "hindi": "रसोई अग्नि", "type": "kitchen", "element": "fire",
                     "importance": "HIGH", "remedy": "Fire in SE, cooking facing East"},

            # Toilet Marma (NW/W)
            (2, 2): {"name": "Toilet NW", "hindi": "शौचालय वायव्य", "type": "toilet", "element": "air",
                     "importance": "HIGH", "remedy": "Keep clean, exhaust, no NE toilet"},

            # Bedroom Marma (SW)
            (8, 2): {"name": "Master Bedroom", "hindi": "मुख्य शयनकक्ष", "type": "bedroom", "element": "earth",
                     "importance": "HIGH", "remedy": "Sleep head South, heavy furniture"},

            # Pooja Marma (NE)
            (2, 8): {"name": "Pooja Room", "hindi": "पूजा कक्ष", "type": "pooja", "element": "space",
                     "importance": "HIGH", "remedy": "NE corner, facing East/North"},

            # Cash Marma (N)
            (1, 4): {"name": "Cash Locker", "hindi": "तिजोरी", "type": "cash", "element": "water",
                     "importance": "HIGH", "remedy": "North, opening East/North"},

            # Water Marma (NE)
            (1, 8): {"name": "Water Source", "hindi": "जल स्रोत", "type": "water", "element": "water",
                     "importance": "HIGH", "remedy": "NE, underground tank"},

            # Staircase Marma (SW/S)
            (7, 1): {"name": "Staircase", "hindi": "सीढ़ी", "type": "staircase", "element": "earth",
                     "importance": "MEDIUM", "remedy": "Clockwise, SW to NE"}
        }

        # Marma types with importance
        self.marma_types = {
            "central": {"importance": "CRITICAL", "count": 1},
            "entrance": {"importance": "HIGH", "count": 8},
            "kitchen": {"importance": "HIGH", "count": 1},
            "toilet": {"importance": "HIGH", "count": 1},
            "bedroom": {"importance": "HIGH", "count": 1},
            "pooja": {"importance": "HIGH", "count": 1},
            "cash": {"importance": "HIGH", "count": 1},
            "water": {"importance": "HIGH", "count": 1},
            "staircase": {"importance": "MEDIUM", "count": 1}
        }

    # ─────────────────────────────────────────
    # 1. GET MARMA POINT
    # ─────────────────────────────────────────
    def get_marma(self, row: int, col: int) -> Dict:
        """Specific marma point nikalo (row 1-9, col 1-9)"""
        if not (1 <= row <= 9 and 1 <= col <= 9):
            return {"error": "Row and col must be 1-9"}
        point = self.marma_points.get((row, col))
        if not point:
            return {
                "row": row, "col": col,
                "name": "Normal Pad",
                "type": "normal",
                "importance": "LOW",
                "note": "No specific marma here"
            }
        return {
            "row": row, "col": col,
            **point
        }

    # ─────────────────────────────────────────
    # 2. ALL MARMA POINTS
    # ─────────────────────────────────────────
    def all_marma(self) -> List[Dict]:
        """Saare marma points ki list"""
        result = []
        for (row, col), info in self.marma_points.items():
            result.append({"row": row, "col": col, **info})
        return sorted(result, key=lambda x: x["importance"], reverse=True)

    # ─────────────────────────────────────────
    # 3. MARMA BY TYPE
    # ─────────────────────────────────────────
    def marma_by_type(self, marma_type: str) -> List[Dict]:
        """Type ke hisaab se marma points"""
        result = []
        for (row, col), info in self.marma_points.items():
            if info["type"] == marma_type:
                result.append({"row": row, "col": col, **info})
        return result

    # ─────────────────────────────────────────
    # 4. MARMA AFFECTED PADS
    # ─────────────────────────────────────────
    def affected_pads(self, row: int, col: int, radius: int = 1) -> List[Dict]:
        """
        Ek marma point ke aas-paas ke affected pads.
        radius = 1 means 3x3 area
        """
        affected = []
        for r in range(max(1, row - radius), min(10, row + radius + 1)):
            for c in range(max(1, col - radius), min(10, col + radius + 1)):
                if (r, c) == (row, col):
                    continue
                point = self.marma_points.get((r, c), {})
                affected.append({
                    "row": r, "col": c,
                    "name": point.get("name", "Normal Pad"),
                    "type": point.get("type", "normal"),
                    "distance": max(abs(r - row), abs(c - col))
                })
        return affected

    # ─────────────────────────────────────────
    # 5. MARMA REMEDY
    # ─────────────────────────────────────────
    def marma_remedy(self, row: int, col: int) -> Dict:
        """Marma point ke liye exact remedy"""
        point = self.get_marma(row, col)
        if "error" in point:
            return point
        if point.get("type") == "normal":
            return {
                "row": row, "col": col,
                "remedy": "No specific marma remedy needed",
                "general": "Maintain element balance in this zone"
            }
        return {
            "row": row, "col": col,
            "name": point["name"],
            "hindi": point.get("hindi", ""),
            "type": point["type"],
            "element": point.get("element", ""),
            "importance": point.get("importance", ""),
            "remedy": point.get("remedy", ""),
            "priority": "IMMEDIATE" if point.get("importance") == "CRITICAL" else "HIGH"
        }

    # ─────────────────────────────────────────
    # 6. FULL MARMA REPORT
    # ─────────────────────────────────────────
    def full_report(self) -> Dict:
        """Complete marma report"""
        all_m = self.all_marma()
        critical = [m for m in all_m if m["importance"] == "CRITICAL"]
        high = [m for m in all_m if m["importance"] == "HIGH"]
        medium = [m for m in all_m if m["importance"] == "MEDIUM"]
        return {
            "total_marma_points": len(all_m),
            "critical_points": critical,
            "high_priority_points": high,
            "medium_priority_points": medium,
            "summary": {
                "critical_count": len(critical),
                "high_count": len(high),
                "medium_count": len(medium)
            }
        }


# ─────────────────────────────────────────
# CLI TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    engine = MarmaEngine()
    print("=" * 60)
    print("MARMA ENGINE TEST")
    print("=" * 60)

    print("\n1. BRAHMASTHAN (Center 5,5):")
    print(json.dumps(engine.get_marma(5, 5), indent=2, ensure_ascii=False))

    print("\n2. NE ENTRANCE (1,9):")
    print(json.dumps(engine.get_marma(1, 9), indent=2, ensure_ascii=False))

    print("\n3. ALL ENTRANCE MARMA:")
    entrances = engine.marma_by_type("entrance")
    print(f"Total entrances: {len(entrances)}")
    for e in entrances:
        print(f"  ({e['row']},{e['col']}) {e['name']}")

    print("\n4. AFFECTED PADS around Brahmasthan (radius 1):")
    affected = engine.affected_pads(5, 5, radius=1)
    print(f"Total affected: {len(affected)}")

    print("\n5. KITCHEN REMEDY (8,8):")
    print(json.dumps(engine.marma_remedy(8, 8), indent=2, ensure_ascii=False))

    print("\n6. FULL REPORT SUMMARY:")
    report = engine.full_report()
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))

    print("\n✅ Marma Engine working!")
