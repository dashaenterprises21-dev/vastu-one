"""
VASTU ONE - Commercial Engine
Vastu analysis for commercial spaces.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class CommercialType(str, Enum):
    OFFICE = "office"; SHOP = "shop"; HOTEL = "hotel"
    RESTAURANT = "restaurant"; FACTORY = "factory"
    SCHOOL = "school"; HOSPITAL = "hospital"; BANK = "bank"


COMMERCIAL_RULES = {
    CommercialType.OFFICE: {"owner_seat": "SW", "cash": "N", "entrance": "N|E|NE", "reception": "NE|N|E", "meeting": "NW|W"},
    CommercialType.SHOP: {"owner_seat": "SW", "cash": "N", "entrance": "N|E|NE", "display": "N|E|NE", "storage": "SW|S"},
    CommercialType.HOTEL: {"reception": "NE|N|E", "kitchen": "SE", "dining": "W|NW", "manager": "SW", "parking": "NW|W"},
    CommercialType.RESTAURANT: {"kitchen": "SE", "dining": "W|NW|S", "cash": "N", "entrance": "N|E|NE", "manager": "SW"},
    CommercialType.FACTORY: {"machinery": "SW|S|W", "raw_material": "NW|W", "finished_goods": "N|NE", "admin": "NE|N|E"},
    CommercialType.SCHOOL: {"principal": "SW|S", "classrooms": "N|E|NE", "library": "NE|N", "playground": "N|E"},
    CommercialType.HOSPITAL: {"operation_theatre": "SE", "icu": "S|SW", "pharmacy": "N|E", "waiting": "NE|N"},
    CommercialType.BANK: {"vault": "SW|S", "cash_counter": "N", "manager": "SW", "entrance": "N|E|NE"},
}


@dataclass
class CommercialFinding:
    commercial_type: str
    element: str
    ideal_direction: str
    actual_direction: str
    status: str
    severity: str
    guna: str
    description: str

    def to_dict(self): return asdict(self)


class CommercialEngine:
    def analyze(self, commercial_type, elements):
        findings = []
        rules = COMMERCIAL_RULES[commercial_type]
        for element, direction in elements.items():
            ideal = rules.get(element, "")
            if not ideal:
                continue
            ideal_list = ideal.split("|")
            status = "ideal" if direction in ideal_list else "bad"
            severity = "informational" if status == "ideal" else "medium"
            guna = "Sattva" if status == "ideal" else "Tamas"
            findings.append(CommercialFinding(
                commercial_type.value, element, ideal, direction,
                status, severity, guna,
                f"{element} in {direction} - {'OK' if status == 'ideal' else 'should be ' + ideal}",
            ))
        return findings
