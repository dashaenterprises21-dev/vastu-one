"""
VASTU ONE - Guna Engine
Three Gunas (Tamas/Rajas/Sattva) scoring.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from enum import Enum


class Guna(str, Enum):
    TAMAS = "Tamas"; RAJAS = "Rajas"; SATTVA = "Sattva"; MIXED = "Mixed"


class HouseVerdict(str, Enum):
    NEGATIVE = "Negative House"
    NEUTRAL = "Neutral / Stable House"
    POSITIVE = "Positive House"


GUNA_WEIGHTS = {Guna.SATTVA: 1.0, Guna.RAJAS: 0.3, Guna.TAMAS: -1.0, Guna.MIXED: 0.0}

SEVERITY_MULT = {
    "critical": 3.0, "high": 2.0, "medium": 1.0, "low": 0.5, "informational": 0.1,
}


@dataclass
class GunaFinding:
    rule_id: str
    guna: Guna
    severity: str = "medium"
    description: str = ""
    direction: str = None
    affected_areas: list = field(default_factory=list)


@dataclass
class GunaProfile:
    tamas_score: float
    rajas_score: float
    sattva_score: float
    net_score: float
    dominant_guna: str
    verdict: str
    confidence: float
    top_issues: list
    top_strengths: list
    recommendation_tier: str

    def to_dict(self): return asdict(self)


class GunaEngine:
    POSITIVE_THRESHOLD = 0.35
    NEGATIVE_THRESHOLD = -0.35

    def evaluate(self, findings):
        findings = list(findings)
        if not findings:
            return self._empty()
        tamas = rajas = sattva = 0.0
        tamas_items, sattva_items = [], []
        for f in findings:
            weight = GUNA_WEIGHTS.get(f.guna, 0.0)
            sev = SEVERITY_MULT.get(f.severity, 1.0)
            bucket = {
                "rule_id": f.rule_id,
                "description": f.description,
                "severity": f.severity,
                "weight": round(weight * sev, 3),
            }
            if f.guna == Guna.TAMAS:
                tamas += sev
                tamas_items.append(bucket)
            elif f.guna == Guna.RAJAS:
                rajas += sev
            elif f.guna == Guna.SATTVA:
                sattva += sev
                sattva_items.append(bucket)
        total = tamas + rajas + sattva
        if total == 0:
            return self._empty()
        t_norm, r_norm, s_norm = tamas/total, rajas/total, sattva/total
        net = max(-1.0, min(1.0, s_norm * 1.0 + r_norm * 0.3 - t_norm * 1.0))
        dominant = max([(Guna.TAMAS, t_norm), (Guna.RAJAS, r_norm),
                       (Guna.SATTVA, s_norm)], key=lambda x: x[1])[0]
        if net >= self.POSITIVE_THRESHOLD:
            verdict = HouseVerdict.POSITIVE
        elif net <= self.NEGATIVE_THRESHOLD:
            verdict = HouseVerdict.NEGATIVE
        else:
            verdict = HouseVerdict.NEUTRAL
        tamas_items.sort(key=lambda x: -x["weight"])
        sattva_items.sort(key=lambda x: -x["weight"])
        return GunaProfile(
            tamas_score=round(t_norm, 3),
            rajas_score=round(r_norm, 3),
            sattva_score=round(s_norm, 3),
            net_score=round(net, 3),
            dominant_guna=dominant.value,
            verdict=verdict.value,
            confidence=round(min(0.95, 0.4 + 0.05 * len(findings)), 2),
            top_issues=tamas_items[:5],
            top_strengths=sattva_items[:5],
            recommendation_tier=self._tier(net),
        )

    def _tier(self, net):
        if net >= 0.6: return "A - Flourishing"
        if net >= 0.35: return "B - Positive"
        if net >= 0.0: return "C - Stable"
        if net >= -0.35: return "D - Weak"
        if net >= -0.6: return "E - Negative"
        return "F - Critical"

    def _empty(self):
        return GunaProfile(0, 0, 0, 0, "Mixed", "Neutral", 0, [], [], "N/A")
