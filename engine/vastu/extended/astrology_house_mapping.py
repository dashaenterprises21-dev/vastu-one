"""
VASTU ONE - Astrology House Mapping
Maps zodiac signs to Vastu directions for main gate analysis.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class Zodiac(str, Enum):
    ARIES = "Aries"; TAURUS = "Taurus"; GEMINI = "Gemini"
    CANCER = "Cancer"; LEO = "Leo"; VIRGO = "Virgo"
    LIBRA = "Libra"; SCORPIO = "Scorpio"; SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"; AQUARIUS = "Aquarius"; PISCES = "Pisces"


ZODIAC_GATE_MAP = {
    Zodiac.ARIES: {"direction": "E", "reason": "Mars-ruled, East for vitality"},
    Zodiac.TAURUS: {"direction": "S", "reason": "Venus-ruled, South for stability"},
    Zodiac.GEMINI: {"direction": "N", "reason": "Mercury-ruled, North for intellect"},
    Zodiac.CANCER: {"direction": "NE", "reason": "Moon-ruled, NE for emotional balance"},
    Zodiac.LEO: {"direction": "E", "reason": "Sun-ruled, East for authority"},
    Zodiac.VIRGO: {"direction": "N", "reason": "Mercury-ruled, North for analysis"},
    Zodiac.LIBRA: {"direction": "W", "reason": "Venus-ruled, West for relationships"},
    Zodiac.SCORPIO: {"direction": "S", "reason": "Mars-ruled, South for intensity"},
    Zodiac.SAGITTARIUS: {"direction": "NE", "reason": "Jupiter-ruled, NE for wisdom"},
    Zodiac.CAPRICORN: {"direction": "SW", "reason": "Saturn-ruled, SW for discipline"},
    Zodiac.AQUARIUS: {"direction": "W", "reason": "Saturn-ruled, West for innovation"},
    Zodiac.PISCES: {"direction": "NE", "reason": "Jupiter-ruled, NE for spirituality"},
}


@dataclass
class AstroGateRecommendation:
    zodiac: str
    ideal_direction: str
    reason: str
    evidence_level: str
    tradition: str

    def to_dict(self): return asdict(self)


class AstrologyHouseMapping:
    def recommend_gate(self, zodiac):
        info = ZODIAC_GATE_MAP[zodiac]
        return AstroGateRecommendation(zodiac.value, info["direction"],
            info["reason"], "B", "Classical Jyotish")

    def all_recommendations(self):
        return [self.recommend_gate(z) for z in ZODIAC_GATE_MAP.keys()]

    def match_gate_to_zodiac(self, gate_direction, zodiac):
        rec = self.recommend_gate(zodiac)
        matches = gate_direction == rec.ideal_direction
        return {
            "gate_direction": gate_direction,
            "ideal_direction": rec.ideal_direction,
            "match": matches,
            "verdict": "Auspicious" if matches else "Consider remedies",
            "reason": rec.reason,
        }
