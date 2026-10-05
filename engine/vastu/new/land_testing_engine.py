"""
VASTU ONE - Land Testing Engine
Bhumi Pariksha - purification, digging, atmosphere.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class LandType(str, Enum):
    BRAHMIN = "Brahmin"; KSHATRIYA = "Kshatriya"
    VAISHYA = "Vaishya"; SHUDRA = "Shudra"; MIXED = "Mixed"


class ObjectFound(str, Enum):
    BONES = "bones"; SKULL = "skull"; COINS = "coins"
    GOLD = "gold"; IRON = "iron"; WEAPONS = "weapons"
    SNAKES = "snakes"; ANTS = "ants"; WATER = "water"
    ASH = "ash"; HAIR = "hair"; NOTHING = "nothing"


class SleepingStage(str, Enum):
    AWAKE = "awake"; DROWSY = "drowsy"
    SLEEPING = "sleeping"; DEEP_SLEEP = "deep_sleep"


OBJECT_INTERPRETATION = {
    ObjectFound.BONES: ("critical", "Tamas", "Death energy - purify"),
    ObjectFound.SKULL: ("critical", "Tamas", "Very inauspicious"),
    ObjectFound.COINS: ("informational", "Sattva", "Prosperity"),
    ObjectFound.GOLD: ("informational", "Sattva", "Highly auspicious"),
    ObjectFound.IRON: ("low", "Mixed", "Neutral"),
    ObjectFound.WEAPONS: ("high", "Tamas", "Violence residue"),
    ObjectFound.SNAKES: ("critical", "Tamas", "Nag dosha"),
    ObjectFound.ANTS: ("low", "Mixed", "Neutral"),
    ObjectFound.WATER: ("informational", "Sattva", "Water present"),
    ObjectFound.ASH: ("high", "Tamas", "Cremation residue"),
    ObjectFound.HAIR: ("medium", "Tamas", "Impurity"),
    ObjectFound.NOTHING: ("informational", "Sattva", "Clean dig"),
}


@dataclass
class LandReport:
    land_type: str
    sleeping_stage: str
    atmosphere: str
    objects_found: list
    purification_needed: bool
    purification_steps: list
    verdict: str
    guna: str

    def to_dict(self): return asdict(self)


class LandTestingEngine:
    def evaluate(self, land_type, sleeping_stage=SleepingStage.AWAKE,
                 atmosphere="normal", objects_found=None):
        objects_found = objects_found or [ObjectFound.NOTHING]
        findings = []
        max_sev = "informational"
        sev_rank = {"informational": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        worst_guna = "Sattva"
        for obj in objects_found:
            sev, guna, msg = OBJECT_INTERPRETATION[obj]
            findings.append({"object": obj.value, "severity": sev, "message": msg})
            if sev_rank[sev] > sev_rank[max_sev]:
                max_sev = sev
                worst_guna = guna
        purify = (max_sev in ("high", "critical")
                  or sleeping_stage in (SleepingStage.SLEEPING, SleepingStage.DEEP_SLEEP)
                  or atmosphere == "negative")
        steps = []
        if purify:
            steps = [
                "Vastu Pujan with Homa",
                "Sprinkle Ganga jal across plot",
                "Bury Navaratna + copper vessel in NE",
                "Ganapati Homam before foundation",
            ]
        verdict_map = {
            "informational": "Land auspicious - proceed",
            "low": "Minor irregularity - light purification",
            "medium": "Moderate issue - Vastu Pujan required",
            "high": "Serious issue - extensive purification",
            "critical": "Land unsuitable - alternative advised",
        }
        return LandReport(land_type.value, sleeping_stage.value, atmosphere,
            findings, purify, steps, verdict_map[max_sev],
            worst_guna if purify else "Sattva")
