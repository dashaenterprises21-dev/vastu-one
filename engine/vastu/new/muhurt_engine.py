"""
VASTU ONE - Muhurt Engine
Timing analysis for construction milestones.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
from datetime import date


class Event(str, Enum):
    SHILANYAS = "shilanyas"; BORING = "boring"
    DIGGING = "digging"; GRIHA_PRAVESH = "griha_pravesh"
    VASTU_PUJAN = "vastu_pujan"


class Tithi(str, Enum):
    PRATIPADA = "Pratipada"; DWITIYA = "Dwitiya"; TRITIYA = "Tritiya"
    CHATURTHI = "Chaturthi"; PANCHAMI = "Panchami"; SHASHTHI = "Shashthi"
    SAPTAMI = "Saptami"; ASHTAMI = "Ashtami"; NAVAMI = "Navami"
    DASHAMI = "Dashami"; EKADASHI = "Ekadashi"; DWADASHI = "Dwadashi"
    TRAYODASHI = "Trayodashi"; CHATURDASHI = "Chaturdashi"
    PURNIMA = "Purnima"; AMAVASYA = "Amavasya"


TITHI_MATRIX = {
    Event.SHILANYAS: {
        "best": [Tithi.DWITIYA, Tithi.TRITIYA, Tithi.PANCHAMI, Tithi.SAPTAMI,
                 Tithi.DASHAMI, Tithi.EKADASHI, Tithi.TRAYODASHI],
        "avoid": [Tithi.CHATURTHI, Tithi.ASHTAMI, Tithi.NAVAMI, Tithi.AMAVASYA],
    },
    Event.BORING: {
        "best": [Tithi.TRITIYA, Tithi.PANCHAMI, Tithi.SAPTAMI, Tithi.DASHAMI],
        "avoid": [Tithi.AMAVASYA, Tithi.CHATURDASHI, Tithi.ASHTAMI],
    },
    Event.GRIHA_PRAVESH: {
        "best": [Tithi.DWITIYA, Tithi.TRITIYA, Tithi.PANCHAMI, Tithi.SHASHTHI,
                 Tithi.SAPTAMI, Tithi.DASHAMI, Tithi.EKADASHI, Tithi.PURNIMA],
        "avoid": [Tithi.CHATURTHI, Tithi.ASHTAMI, Tithi.NAVAMI, Tithi.AMAVASYA],
    },
}

WEEKDAY_MATRIX = {
    Event.SHILANYAS: ["Monday", "Wednesday", "Thursday", "Friday"],
    Event.BORING: ["Monday", "Wednesday", "Thursday"],
    Event.GRIHA_PRAVESH: ["Monday", "Wednesday", "Thursday", "Friday", "Saturday"],
    Event.VASTU_PUJAN: ["Monday", "Wednesday", "Thursday", "Friday"],
    Event.DIGGING: ["Monday", "Wednesday", "Thursday", "Friday"],
}

AUSPICIOUS_NAKSHATRAS = [
    "Rohini", "Mrigashira", "Pushya", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Anuradha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Uttara Bhadrapada", "Revati",
]

INAUSPICIOUS_NAKSHATRAS = [
    "Bharani", "Krittika", "Ardra", "Ashlesha", "Magha",
    "Purva Phalguni", "Vishakha", "Jyeshtha", "Mula",
    "Purva Ashadha", "Purva Bhadrapada",
]


@dataclass
class MuhurtReport:
    event: str
    proposed_date: Optional[str]
    tithi: Optional[str]
    weekday: Optional[str]
    nakshatra: Optional[str]
    verdict: str
    score: float
    reasons: list
    guna: str

    def to_dict(self): return asdict(self)


class MuhurtEngine:
    def evaluate(self, event, tithi=None, weekday=None, nakshatra=None,
                 proposed_date=None) -> MuhurtReport:
        reasons = []
        score = 0.5
        tithi_matrix = TITHI_MATRIX.get(event, {"best": [], "avoid": []})
        weekdays = WEEKDAY_MATRIX.get(event, [])
        if tithi:
            if tithi in tithi_matrix["best"]:
                score += 0.25
                reasons.append(f"Tithi {tithi.value} auspicious")
            elif tithi in tithi_matrix["avoid"]:
                score -= 0.35
                reasons.append(f"Tithi {tithi.value} inauspicious")
        if weekday:
            if weekday in weekdays:
                score += 0.15
                reasons.append(f"{weekday} favourable")
            else:
                score -= 0.15
                reasons.append(f"{weekday} not preferred")
        if nakshatra:
            if nakshatra in AUSPICIOUS_NAKSHATRAS:
                score += 0.2
                reasons.append(f"{nakshatra} auspicious")
            elif nakshatra in INAUSPICIOUS_NAKSHATRAS:
                score -= 0.3
                reasons.append(f"{nakshatra} inauspicious")
        score = max(0.0, min(1.0, score))
        if score >= 0.75:
            verdict, guna = "Auspicious - proceed", "Sattva"
        elif score >= 0.5:
            verdict, guna = "Acceptable with precautions", "Rajas"
        else:
            verdict, guna = "Inauspicious - reschedule", "Tamas"
        return MuhurtReport(event.value,
            proposed_date.isoformat() if proposed_date else None,
            tithi.value if tithi else None, weekday, nakshatra,
            verdict, round(score, 2), reasons, guna)
