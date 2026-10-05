"""
VASTU ONE - Water Engine
Directional analysis of water features per Vastu Shastra.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class WaterFeature(str, Enum):
    UNDERGROUND_TANK = "underground_tank"
    OVERHEAD_TANK = "overhead_tank"
    RAINWATER_HARVEST = "rainwater_harvest"
    BOREWELL = "borewell"
    WELL = "well"
    SEPTIC_TANK = "septic_tank"
    DRAINAGE = "drainage"


class Direction(str, Enum):
    N = "N"; NE = "NE"; E = "E"; SE = "SE"
    S = "S"; SW = "SW"; W = "W"; NW = "NW"


WATER_MATRIX = {
    WaterFeature.UNDERGROUND_TANK: {
        "ideal": [Direction.NE, Direction.N, Direction.E],
        "bad": [Direction.SE, Direction.S, Direction.SW],
        "severity": "high", "guna_good": "Sattva", "guna_bad": "Tamas",
    },
    WaterFeature.OVERHEAD_TANK: {
        "ideal": [Direction.SW, Direction.W, Direction.S],
        "bad": [Direction.NE, Direction.N, Direction.E, Direction.SE],
        "severity": "high", "guna_good": "Rajas", "guna_bad": "Tamas",
    },
    WaterFeature.BOREWELL: {
        "ideal": [Direction.NE, Direction.N, Direction.E],
        "bad": [Direction.SW, Direction.S, Direction.SE],
        "severity": "critical", "guna_good": "Sattva", "guna_bad": "Tamas",
    },
    WaterFeature.SEPTIC_TANK: {
        "ideal": [Direction.NW, Direction.W],
        "bad": [Direction.NE, Direction.E, Direction.SE, Direction.S],
        "severity": "critical", "guna_good": "Mixed", "guna_bad": "Tamas",
    },
    WaterFeature.RAINWATER_HARVEST: {
        "ideal": [Direction.NE, Direction.N, Direction.E],
        "bad": [Direction.SW, Direction.S],
        "severity": "medium", "guna_good": "Sattva", "guna_bad": "Tamas",
    },
    WaterFeature.WELL: {
        "ideal": [Direction.NE, Direction.N, Direction.E],
        "bad": [Direction.SE, Direction.S, Direction.SW],
        "severity": "high", "guna_good": "Sattva", "guna_bad": "Tamas",
    },
    WaterFeature.DRAINAGE: {
        "ideal": [Direction.NW, Direction.W, Direction.N],
        "bad": [Direction.NE, Direction.SW, Direction.S],
        "severity": "medium", "guna_good": "Mixed", "guna_bad": "Tamas",
    },
}


@dataclass
class WaterFinding:
    feature: str
    direction: str
    status: str
    severity: str
    guna: str
    description: str
    remedy: str

    def to_dict(self): return asdict(self)


class WaterEngine:
    def analyze(self, feature, direction) -> WaterFinding:
        matrix = WATER_MATRIX[feature]
        if direction in matrix["ideal"]:
            return WaterFinding(feature.value, direction.value, "ideal",
                "informational", matrix["guna_good"],
                f"{feature.value} in {direction.value} - IDEAL", "No action")
        if direction in matrix["bad"]:
            return WaterFinding(feature.value, direction.value, "bad",
                matrix["severity"], matrix["guna_bad"],
                f"{feature.value} in {direction.value} - INAUSPICIOUS",
                f"Relocate to ideal direction")
        return WaterFinding(feature.value, direction.value, "ok",
            "low", "Mixed", f"{feature.value} in {direction.value} - acceptable", "Monitor")

    def analyze_all(self, placements):
        return [self.analyze(f, d) for f, d in placements.items()]
