"""
VASTU ONE - Pyramid Engine
Pyramid remedies for Vastu correction.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class PyramidType(str, Enum):
    COPPER = "copper"; CRYSTAL = "crystal"; WOOD = "wood"
    GLASS = "glass"; METAL = "metal"


class Direction(str, Enum):
    N = "N"; NE = "NE"; E = "E"; SE = "SE"
    S = "S"; SW = "SW"; W = "W"; NW = "NW"


PYRAMID_USES = {
    Direction.N: {"purpose": "Career growth, opportunities", "type": PyramidType.CRYSTAL},
    Direction.NE: {"purpose": "Wisdom, spiritual growth", "type": PyramidType.CRYSTAL},
    Direction.E: {"purpose": "Health, family harmony", "type": PyramidType.WOOD},
    Direction.SE: {"purpose": "Wealth, financial stability", "type": PyramidType.COPPER},
    Direction.S: {"purpose": "Fame, recognition", "type": PyramidType.COPPER},
    Direction.SW: {"purpose": "Relationships, stability", "type": PyramidType.COPPER},
    Direction.W: {"purpose": "Children, creativity", "type": PyramidType.METAL},
    Direction.NW: {"purpose": "Helpful people, travel", "type": PyramidType.METAL},
}


@dataclass
class PyramidRemedy:
    direction: str
    pyramid_type: str
    purpose: str
    placement: str
    size_cm: str
    caution: str

    def to_dict(self): return asdict(self)


class PyramidEngine:
    def recommend(self, direction, purpose=None):
        info = PYRAMID_USES[direction]
        return PyramidRemedy(
            direction.value, info["type"].value,
            purpose or info["purpose"],
            f"{direction.value} corner of the room/plot",
            "9 cm (standard)", "Avoid in Brahmasthan and Pooja room",
        )

    def all_recommendations(self):
        return [self.recommend(d) for d in PYRAMID_USES.keys()]

    def myths_facts(self):
        return {
            "myth": "Pyramids can instantly fix any Vastu dosha",
            "fact": "Pyramids are symbolic remedies - they complement, not replace, structural corrections",
            "verified_by": "occult_engine",
            "evidence_level": "C",
        }
