"""
VASTU ONE - Plot Extension Engine
Analyzes plot extensions and reductions per Vastu Shastra.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class Direction(str, Enum):
    N = "N"; NE = "NE"; E = "E"; SE = "SE"
    S = "S"; SW = "SW"; W = "W"; NW = "NW"


# Extension per direction
EXTENSION_MATRIX = {
    Direction.N: {"verdict": "Good", "guna": "Sattva", "result": "Wealth & opportunities"},
    Direction.NE: {"verdict": "Excellent", "guna": "Sattva", "result": "Highly auspicious"},
    Direction.E: {"verdict": "Good", "guna": "Sattva", "result": "Growth & health"},
    Direction.SE: {"verdict": "Bad", "guna": "Tamas", "result": "Financial loss, disputes"},
    Direction.S: {"verdict": "Bad", "guna": "Tamas", "result": "Health issues, obstacles"},
    Direction.SW: {"verdict": "Bad", "guna": "Tamas", "result": "Serious problems"},
    Direction.W: {"verdict": "Good", "guna": "Rajas", "result": "Gains & profits"},
    Direction.NW: {"verdict": "Neutral", "guna": "Mixed", "result": "Neutral effect"},
}

# Reduction per direction
REDUCTION_MATRIX = {
    Direction.N: {"verdict": "Bad", "guna": "Tamas", "result": "Loss of wealth"},
    Direction.NE: {"verdict": "Critical", "guna": "Tamas", "result": "Very inauspicious"},
    Direction.E: {"verdict": "Bad", "guna": "Tamas", "result": "Growth blocked"},
    Direction.SE: {"verdict": "Good", "guna": "Sattva", "result": "Reduces fire dosha"},
    Direction.S: {"verdict": "Good", "guna": "Sattva", "result": "Reduces Yama dosha"},
    Direction.SW: {"verdict": "Good", "guna": "Sattva", "result": "Reduces heavy energy"},
    Direction.W: {"verdict": "Bad", "guna": "Tamas", "result": "Loss of gains"},
    Direction.NW: {"verdict": "Neutral", "guna": "Mixed", "result": "Neutral"},
}


@dataclass
class PlotExtensionFinding:
    change_type: str
    direction: str
    verdict: str
    guna: str
    severity: str
    result: str
    remedy: str

    def to_dict(self): return asdict(self)


class PlotExtensionEngine:
    def analyze_extension(self, direction):
        m = EXTENSION_MATRIX[direction]
        sev = "informational" if m["verdict"] in ("Good", "Excellent") else (
            "critical" if m["verdict"] == "Bad" else "medium")
        return PlotExtensionFinding("extension", direction.value, m["verdict"],
            m["guna"], sev, m["result"],
            "No action" if sev == "informational" else "Consider remedies for the cut corner")

    def analyze_reduction(self, direction):
        m = REDUCTION_MATRIX[direction]
        sev = "critical" if m["verdict"] == "Critical" else (
            "informational" if m["verdict"] == "Good" else "high")
        return PlotExtensionFinding("reduction", direction.value, m["verdict"],
            m["guna"], sev, m["result"],
            "No action" if sev == "informational" else "Remedies needed for missing zone")

    def full_analysis(self, extensions=None, reductions=None):
        results = []
        for d in (extensions or []):
            results.append(self.analyze_extension(d))
        for d in (reductions or []):
            results.append(self.analyze_reduction(d))
        return results
