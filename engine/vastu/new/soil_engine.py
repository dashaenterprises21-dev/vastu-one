"""
VASTU ONE - Soil Engine
Classifies soil type, evaluates suitability for construction per Vastu Shastra.
Sources: Brihat Samhita Ch. 53, Vishvakarma Prakash, Mayamata Ch. 3
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
import json


class SoilColour(str, Enum):
    WHITE = "white"; RED = "red"; YELLOW = "yellow"
    BLACK = "black"; MIXED = "mixed"


class SoilTexture(str, Enum):
    SANDY = "sandy"; CLAY = "clay"; LOAMY = "loamy"
    GRAVEL = "gravel"; ROCKY = "rocky"


class SoilTaste(str, Enum):
    SWEET = "sweet"; PUNGENT = "pungent"; BITTER = "bitter"
    ASTRINGENT = "astringent"; SALTY = "salty"


class CasteClass(str, Enum):
    BRAHMIN = "Brahmin"; KSHATRIYA = "Kshatriya"
    VAISHYA = "Vaishya"; SHUDRA = "Shudra"; MIXED = "Mixed"


@dataclass
class SoilReport:
    colour: SoilColour
    texture: SoilTexture
    taste: Optional[SoilTaste]
    caste: CasteClass
    fertility: str
    water_retention: str
    construction_suitability: str
    verdict: str
    recommendation: str
    guna: str
    evidence_level: str = "A"

    def to_dict(self): return asdict(self)


SOIL_CASTE_MAP = {
    (SoilColour.WHITE, SoilTaste.SWEET): CasteClass.BRAHMIN,
    (SoilColour.RED, SoilTaste.PUNGENT): CasteClass.KSHATRIYA,
    (SoilColour.YELLOW, SoilTaste.BITTER): CasteClass.VAISHYA,
    (SoilColour.BLACK, SoilTaste.ASTRINGENT): CasteClass.SHUDRA,
}

CASTE_VERDICT = {
    CasteClass.BRAHMIN: ("Excellent", "Sattva", "Proceed - auspicious"),
    CasteClass.KSHATRIYA: ("Good", "Rajas", "Proceed - good for commercial"),
    CasteClass.VAISHYA: ("Average", "Mixed", "Proceed with remedies"),
    CasteClass.SHUDRA: ("Poor", "Tamas", "Purify before construction"),
    CasteClass.MIXED: ("Mixed", "Mixed", "Test at 5 spots"),
}


class SoilEngine:
    def evaluate(self, colour, texture, taste=None) -> SoilReport:
        caste = SOIL_CASTE_MAP.get((colour, taste), CasteClass.MIXED)
        verdict, guna, rec = CASTE_VERDICT[caste]
        fertility = {"loamy": "High", "clay": "Medium", "sandy": "Low",
                     "gravel": "Very Low", "rocky": "Unsuitable"}[texture.value]
        retention = {"clay": "High", "loamy": "Medium", "sandy": "Low",
                     "gravel": "Very Low", "rocky": "N/A"}[texture.value]
        suitability = "Suitable"
        if texture == SoilTexture.ROCKY:
            suitability = "Unsuitable"
        elif texture == SoilTexture.GRAVEL:
            suitability = "Poor - needs deep foundation"
        return SoilReport(colour, texture, taste, caste, fertility,
                          retention, suitability, verdict, rec, guna)


if __name__ == "__main__":
    eng = SoilEngine()
    print(json.dumps(eng.evaluate(SoilColour.WHITE, SoilTexture.LOAMY, SoilTaste.SWEET).to_dict(), indent=2))
