"""
VASTU ONE - Feng Shui Engine
Comparative Feng Shui analysis as complement to Vastu.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class FSElement(str, Enum):
    WOOD = "Wood"; FIRE = "Fire"; EARTH = "Earth"
    METAL = "Metal"; WATER = "Water"


class Direction(str, Enum):
    N = "N"; NE = "NE"; E = "E"; SE = "SE"
    S = "S"; SW = "SW"; W = "W"; NW = "NW"; CENTER = "Center"


# Bagua map - Feng Shui area associations
BAGUA_MAP = {
    Direction.N: {"element": FSElement.WATER, "area": "Career", "color": "Black/Blue"},
    Direction.NE: {"element": FSElement.EARTH, "area": "Knowledge", "color": "Blue/Green"},
    Direction.E: {"element": FSElement.WOOD, "area": "Family", "color": "Green"},
    Direction.SE: {"element": FSElement.WOOD, "area": "Wealth", "color": "Purple/Green"},
    Direction.S: {"element": FSElement.FIRE, "area": "Fame", "color": "Red"},
    Direction.SW: {"element": FSElement.EARTH, "area": "Marriage", "color": "Pink/Red"},
    Direction.W: {"element": FSElement.METAL, "area": "Children", "color": "White/Gold"},
    Direction.NW: {"element": FSElement.METAL, "area": "Helpful People", "color": "Grey/White"},
    Direction.CENTER: {"element": FSElement.EARTH, "area": "Health", "color": "Yellow/Brown"},
}

# Element cycle - for generating/destroying relationships
ELEMENT_CYCLE = {
    "generating": {
        FSElement.WOOD: FSElement.FIRE, FSElement.FIRE: FSElement.EARTH,
        FSElement.EARTH: FSElement.METAL, FSElement.METAL: FSElement.WATER,
        FSElement.WATER: FSElement.WOOD,
    },
    "destroying": {
        FSElement.WOOD: FSElement.EARTH, FSElement.EARTH: FSElement.WATER,
        FSElement.WATER: FSElement.FIRE, FSElement.FIRE: FSElement.METAL,
        FSElement.METAL: FSElement.WOOD,
    },
}


@dataclass
class FSFinding:
    direction: str
    bagua_area: str
    element: str
    color: str
    harmony: str
    guna: str

    def to_dict(self): return asdict(self)


class FengShuiEngine:
    def analyze_direction(self, direction):
        info = BAGUA_MAP[direction]
        return FSFinding(direction.value, info["area"], info["element"].value,
            info["color"], "aligned", "Sattva")

    def full_analysis(self):
        return [self.analyze_direction(d) for d in BAGUA_MAP.keys()]

    def element_relationship(self, from_el, to_el):
        if ELEMENT_CYCLE["generating"].get(from_el) == to_el:
            return "generating (auspicious)"
        if ELEMENT_CYCLE["destroying"].get(from_el) == to_el:
            return "destroying (inauspicious)"
        return "neutral"
