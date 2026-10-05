"""
VASTU ONE - Colour Engine
Direction-to-colour mapping for Vastu compliance.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class Direction(str, Enum):
    N = "N"; NE = "NE"; E = "E"; SE = "SE"
    S = "S"; SW = "SW"; W = "W"; NW = "NW"; CENTER = "Center"


COLOUR_MATRIX = {
    Direction.N: {"ideal": ["White", "Cream", "Light Blue"], "avoid": ["Red", "Black"]},
    Direction.NE: {"ideal": ["White", "Light Yellow", "Cream"], "avoid": ["Red", "Black"]},
    Direction.E: {"ideal": ["White", "Light Green", "Light Yellow"], "avoid": ["Red", "Black"]},
    Direction.SE: {"ideal": ["Red", "Orange", "Pink"], "avoid": ["Blue", "Black"]},
    Direction.S: {"ideal": ["Red", "Pink", "Orange"], "avoid": ["Black", "Blue"]},
    Direction.SW: {"ideal": ["Peach", "Pink", "Light Brown"], "avoid": ["Blue", "Black"]},
    Direction.W: {"ideal": ["White", "Blue", "Grey"], "avoid": ["Red", "Orange"]},
    Direction.NW: {"ideal": ["White", "Grey", "Light Blue"], "avoid": ["Red"]},
    Direction.CENTER: {"ideal": ["Light Yellow", "White"], "avoid": ["Black"]},
}


@dataclass
class ColourFinding:
    direction: str
    colour: str
    status: str
    severity: str
    guna: str
    description: str
    suggested: list

    def to_dict(self): return asdict(self)


class ColourEngine:
    def check(self, direction, colour) -> ColourFinding:
        spec = COLOUR_MATRIX[direction]
        c = colour.strip().lower()
        ideal = [x.lower() for x in spec["ideal"]]
        avoid = [x.lower() for x in spec["avoid"]]
        if c in ideal:
            return ColourFinding(direction.value, colour, "ideal",
                "informational", "Sattva",
                f"{colour} IDEAL for {direction.value}", spec["ideal"])
        if c in avoid:
            return ColourFinding(direction.value, colour, "avoid",
                "medium", "Tamas",
                f"{colour} INAUSPICIOUS for {direction.value}", spec["ideal"])
        return ColourFinding(direction.value, colour, "neutral",
            "low", "Mixed", f"{colour} neutral for {direction.value}", spec["ideal"])

    def full_report(self, choices):
        return [self.check(d, c) for d, c in choices.items()]
