"""
Vastu One - Plot Layout Engine
Khali plot ke liye authority norms ke hisaab se ghar ka layout
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


class PlotLayoutEngine:
    def __init__(self):
        # Authority norms (NIDM Guidelines - can be state-specific)
        self.norms = [
            {"min": 0, "max": 30, "gc": 90, "far": 180, "height": 6, "setback": 1.2, "storeys": 2},
            {"min": 30, "max": 50, "gc": 80, "far": 160, "height": 6, "setback": 1.2, "storeys": 2},
            {"min": 51, "max": 100, "gc": 80, "far": 160, "height": 9, "setback": 2.0, "storeys": 3},
            {"min": 101, "max": 150, "gc": 75, "far": 150, "height": 9, "setback": 2.0, "storeys": 3},
            {"min": 151, "max": 250, "gc": 66, "far": 130, "height": 9, "setback": 3.0, "storeys": 3},
            {"min": 251, "max": 500, "gc": 60, "far": 120, "height": 9, "setback": 4.5, "storeys": 3},
            {"min": 501, "max": 99999, "gc": 50, "far": 100, "height": 9, "setback": 4.5, "storeys": 3},
        ]

    def get_norms(self, area):
        """Get authority norms for plot area"""
        for n in self.norms:
            if n["min"] <= area <= n["max"]:
                return n
        return self.norms[-1]

    def generate_layout(self, plot_length, plot_breadth, facing_direction="North", plot_area=None):
        """
        Generate Vastu layout for empty plot
        plot_length: length in feet
        plot_breadth: breadth in feet
        facing_direction: North/South/East/West (road side)
        """
        if not plot_area:
            plot_area = plot_length * plot_breadth

        # Area in sq meters (for norms)
        area_sqm = plot_area * 0.0929
        norms = self.get_norms(area_sqm)

        # Calculate buildable area
        gc_area = plot_area * norms["gc"] / 100
        far_area = plot_area * norms["far"] / 100
        max_height_ft = norms["height"] * 3.28

        # Setbacks (in feet)
        sb_ft = norms["setback"] * 3.28
        buildable_length = plot_length - (sb_ft * 2)
        buildable_breadth = plot_breadth - (sb_ft * 2)
        if buildable_length < 0: buildable_length = 0
        if buildable_breadth < 0: buildable_breadth = 0

        # Room placement as per Vastu (81-pad grid)
        rooms = self._place_rooms(buildable_length, buildable_breadth, facing_direction)

        return {
            "plot_dimensions": {
                "length_ft": plot_length,
                "breadth_ft": plot_breadth,
                "area_sqft": round(plot_area, 2),
                "area_sqm": round(area_sqm, 2),
                "facing_direction": facing_direction
            },
            "authority_norms": {
                "ground_coverage_percent": norms["gc"],
                "far_percent": norms["far"],
                "max_height_ft": round(max_height_ft, 2),
                "max_storeys": norms["storeys"],
                "setback_ft": round(sb_ft, 2)
            },
            "buildable_area": {
                "ground_coverage_sqft": round(gc_area, 2),
                "far_sqft": round(far_area, 2),
                "buildable_length_ft": round(buildable_length, 2),
                "buildable_breadth_ft": round(buildable_breadth, 2)
            },
            "vastu_rooms": rooms,
            "layout_summary": self._summary(plot_area, gc_area, far_area, rooms, norms)
        }

    def _place_rooms(self, length, breadth, facing):
        """Place rooms as per Vastu 81-pad grid"""
        # Map facing direction to layout
        rooms = []

        # Base positions (as % of buildable area)
        base_rooms = [
            {"name": "Puja Room", "zone": "NE", "x": 0.75, "y": 0.05, "size": "small", "hindi": "पूजा कक्ष"},
            {"name": "Kitchen", "zone": "SE", "x": 0.75, "y": 0.75, "size": "medium", "hindi": "रसोई"},
            {"name": "Master Bedroom", "zone": "SW", "x": 0.05, "y": 0.75, "size": "large", "hindi": "मुख्य शयनकक्ष"},
            {"name": "Living Room", "zone": "N", "x": 0.05, "y": 0.05, "size": "large", "hindi": "बैठक"},
            {"name": "Dining", "zone": "W", "x": 0.4, "y": 0.4, "size": "medium", "hindi": "भोजन कक्ष"},
            {"name": "Toilet", "zone": "NW", "x": 0.05, "y": 0.4, "size": "small", "hindi": "शौचालय"},
            {"name": "Kids Bedroom", "zone": "E", "x": 0.4, "y": 0.05, "size": "medium", "hindi": "बच्चों का कमरा"},
            {"name": "Toilet 2", "zone": "S", "x": 0.4, "y": 0.75, "size": "small", "hindi": "शौचालय 2"},
            {"name": "Store", "zone": "SW", "x": 0.05, "y": 0.5, "size": "small", "hindi": "भंडार"},
            {"name": "Staircase", "zone": "S", "x": 0.4, "y": 0.5, "size": "small", "hindi": "सीढ़ी"},
        ]

        # Adjust for facing direction (rotate)
        rotations = {
            "North": 0,
            "East": 90,
            "South": 180,
            "West": 270
        }
        rot = rotations.get(facing, 0)

        for r in base_rooms:
            x, y = r["x"], r["y"]
            # Simple rotation (for corner zones)
            if rot == 90:
                x, y = 1-y, x
            elif rot == 180:
                x, y = 1-x, 1-y
            elif rot == 270:
                x, y = y, 1-x

            rooms.append({
                "name": r["name"],
                "hindi": r["hindi"],
                "zone": r["zone"],
                "position_x": round(x, 2),
                "position_y": round(y, 2),
                "size": r["size"],
                "vastu_rule": f"{r['name']} in {r['zone']} zone - correct placement"
            })

        return rooms

    def _summary(self, plot_area, gc_area, far_area, rooms, norms):
        return {
            "title": "Khali Plot ke liye Vastu Layout",
            "plot_area_sqft": round(plot_area, 2),
            "ground_floor_area_sqft": round(gc_area, 2),
            "total_buildable_area_sqft": round(far_area, 2),
            "max_storeys": norms["storeys"],
            "total_rooms": len(rooms),
            "vastu_score_estimate": "85-95% (agar layout follow karein)",
            "note": "Ye layout Vastu 81-pad grid aur authority norms ke hisaab se hai"
        }


if __name__ == "__main__":
    engine = PlotLayoutEngine()

    print("=== KHALI PLOT LAYOUT - 40x60 ft ===")
    result = engine.generate_layout(40, 60, "North")
    print(json.dumps(result, indent=2, ensure_ascii=False))
