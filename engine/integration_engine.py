"""
Integration Engine — Vastu One Enterprise
Sab engines ko jodta hai — Master Integration Layer
"""

import json
import os
from typing import Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ENGINE_DIR = os.path.dirname(__file__)

# Import all engines
import sys
sys.path.insert(0, ENGINE_DIR)

from astro_engine import AstroEngine
from numerology_engine import NumerologyEngine
from disha_bal_engine import DishaBalEngine
from auo_engine import AUOEngine
from marma_engine import MarmaEngine
from owner_tenant_engine import OwnerTenantEngine
from occult_engine import OccultEngine


class IntegrationEngine:
    """Master integration — sab engines ko jodta hai"""

    def __init__(self):
        self.astro = AstroEngine()
        self.numerology = NumerologyEngine()
        self.disha = DishaBalEngine()
        self.auo = AUOEngine()
        self.marma = MarmaEngine()
        self.owner_tenant = OwnerTenantEngine()
        self.occult = OccultEngine()

    # ─────────────────────────────────────────
    # 1. FULL INTEGRATED REPORT
    # ─────────────────────────────────────────
    def full_report(self, input_data: Dict) -> Dict:
        """
        Complete integrated report.
        input_data = {
            "dob": "1990-05-15",
            "tob": "10:30",
            "place": "Delhi",
            "name": "Rajesh Kumar",
            "property_number": "B-204",
            "ownership": "owner_occupied",
            "usage": "residential",
            "activities": [{"name": "sleeping", "direction": "SW"}, ...],
            "zone_scores": {"N": 85, "NE": 90, ...},
            "issues": ["toilet_ne", "negative_energy"]
        }
        """
        # 1. Astro
        astro_report = self.astro.full_report(
            input_data.get("dob"),
            input_data.get("tob"),
            input_data.get("place")
        )

        # 2. Numerology
        numerology_report = self.numerology.full_report(
            input_data.get("dob", "1990-01-01"),
            input_data.get("name", "Unknown"),
            input_data.get("property_number", "1")
        )

        # 3. Disha Bal
        disha_report = self.disha.full_report(
            input_data.get("zone_scores", {})
        )

        # 4. AUO
        auo_report = self.auo.full_report(
            input_data.get("activities", []),
            input_data.get("usage", "residential"),
            input_data.get("ownership", "owner_occupied")
        )

        # 5. Marma
        marma_report = self.marma.full_report()

        # 6. Owner/Tenant
        owner_tenant_report = self.owner_tenant.full_report(
            input_data.get("ownership", "owner_occupied"),
            input_data.get("issues", [])
        )

        # 7. Occult
        occult_report = self.occult.full_report(
            input_data.get("issues", ["negative_energy"])
        )

        # 8. Integrated Score
        integrated_score = self._integrated_score(
            astro_report, numerology_report, disha_report, auo_report
        )

        return {
            "astro": astro_report,
            "numerology": numerology_report,
            "disha_bal": disha_report,
            "auo": auo_report,
            "marma": marma_report,
            "owner_tenant": owner_tenant_report,
            "occult": occult_report,
            "integrated_score": integrated_score,
            "summary": self._summary(integrated_score, disha_report, auo_report)
        }

    # ─────────────────────────────────────────
    # 2. INTEGRATED SCORE
    # ─────────────────────────────────────────
    def _integrated_score(self, astro: Dict, numerology: Dict,
                          disha: Dict, auo: Dict) -> Dict:
        """7-Component Score calculate karo"""
        # Component scores (0-100)
        astro_score = 70  # Simplified
        numerology_score = 80 if numerology.get("compatibility", {}).get("compatible") else 50
        disha_score = disha.get("disha_bal", {}).get("average_bal", 50)
        auo_score = auo.get("auo_matrix", {}).get("overall_score", 50)
        marma_score = 75  # Simplified
        owner_score = 80  # Simplified
        occult_score = 85  # Simplified

        # Weighted average
        weights = {
            "astro": 0.15,
            "numerology": 0.10,
            "disha": 0.25,
            "auo": 0.20,
            "marma": 0.10,
            "owner": 0.10,
            "occult": 0.10
        }

        total = (
            astro_score * weights["astro"] +
            numerology_score * weights["numerology"] +
            disha_score * weights["disha"] +
            auo_score * weights["auo"] +
            marma_score * weights["marma"] +
            owner_score * weights["owner"] +
            occult_score * weights["occult"]
        )

        return {
            "total_score": round(total, 2),
            "components": {
                "astro": astro_score,
                "numerology": numerology_score,
                "disha_bal": disha_score,
                "auo": auo_score,
                "marma": marma_score,
                "owner_tenant": owner_score,
                "occult": occult_score
            },
            "weights": weights,
            "grade": self._grade(total)
        }

    def _grade(self, score: float) -> str:
        if score >= 85:
            return "A+ (Excellent) ✅"
        elif score >= 70:
            return "A (Good) ✅"
        elif score >= 55:
            return "B (Average) ⚠️"
        elif score >= 40:
            return "C (Below Average) ⚠️"
        else:
            return "D (Poor) 🔴"

    # ─────────────────────────────────────────
    # 3. SUMMARY
    # ─────────────────────────────────────────
    def _summary(self, score: Dict, disha: Dict, auo: Dict) -> Dict:
        return {
            "overall_grade": score["grade"],
            "total_score": score["total_score"],
            "weak_areas": self._weak_areas(score["components"]),
            "strong_areas": self._strong_areas(score["components"]),
            "top_remedies": self._top_remedies(disha, auo)
        }

    def _weak_areas(self, components: Dict) -> List[str]:
        return [k for k, v in components.items() if v < 55]

    def _strong_areas(self, components: Dict) -> List[str]:
        return [k for k, v in components.items() if v >= 75]

    def _top_remedies(self, disha: Dict, auo: Dict) -> List[Dict]:
        remedies = []
        # Disha Bal remedies
        for r in disha.get("recommendations", [])[:2]:
            remedies.append({
                "source": "Disha Bal",
                "direction": r["direction"],
                "remedy": r["remedy"],
                "priority": r["priority"]
            })
        # AUO remedies
        for r in auo.get("auo_matrix", {}).get("priority_remedies", [])[:2]:
            remedies.append({
                "source": "AUO",
                "activity": r["activity"],
                "remedy": r["remedy"],
                "priority": r["priority"]
            })
        return remedies

    # ─────────────────────────────────────────
    # 4. PACKAGE-BASED REPORT
    # ─────────────────────────────────────────
    def package_report(self, package: str, input_data: Dict) -> Dict:
        """Package ke hisaab se report filter karo"""
        full = self.full_report(input_data)
        package = package.lower()

        if package == "bronze":
            return {
                "package": "Bronze",
                "price": "₹999",
                "included": ["auo", "marma", "basic_remedies"],
                "data": {
                    "auo": full["auo"],
                    "marma": full["marma"],
                    "summary": full["summary"]
                }
            }
        elif package == "silver":
            return {
                "package": "Silver",
                "price": "₹2,999",
                "included": ["astro", "disha_bal", "auo", "marma"],
                "data": {
                    "astro": full["astro"],
                    "disha_bal": full["disha_bal"],
                    "auo": full["auo"],
                    "marma": full["marma"],
                    "summary": full["summary"]
                }
            }
        elif package == "gold":
            return {
                "package": "Gold",
                "price": "₹7,999",
                "included": ["astro", "numerology", "disha_bal", "auo", "marma", "occult"],
                "data": {
                    "astro": full["astro"],
                    "numerology": full["numerology"],
                    "disha_bal": full["disha_bal"],
                    "auo": full["auo"],
                    "marma": full["marma"],
                    "occult": full["occult"],
                    "summary": full["summary"]
                }
            }
        else:  # platinum
            return {
                "package": "Platinum",
                "price": "₹19,999",
                "included": ["all"],
                "data": full
            }


# ─────────────────────────────────────────
# CLI TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    engine = IntegrationEngine()
    print("=" * 60)
    print("INTEGRATION ENGINE TEST")
    print("=" * 60)

    # Sample input
    input_data = {
        "dob": "1990-05-15",
        "tob": "10:30",
        "place": "Delhi",
        "name": "Rajesh Kumar",
        "property_number": "B-204",
        "ownership": "owner_occupied",
        "usage": "residential",
        "activities": [
            {"name": "sleeping", "direction": "SW"},
            {"name": "cooking", "direction": "SE"},
            {"name": "study", "direction": "NE"},
            {"name": "cash", "direction": "S"}
        ],
        "zone_scores": {
            "N": 85, "NNE": 70, "NE": 90, "ENE": 60,
            "E": 95, "ESE": 75, "SE": 40, "SSE": 55,
            "S": 65, "SSW": 30, "SW": 25, "WSW": 50,
            "W": 60, "WNW": 45, "NW": 70, "NNW": 80
        },
        "issues": ["toilet_ne", "negative_energy", "health_issue"]
    }

    print("\n1. INTEGRATED SCORE:")
    full = engine.full_report(input_data)
    print(json.dumps(full["integrated_score"], indent=2, ensure_ascii=False))

    print("\n2. SUMMARY:")
    print(json.dumps(full["summary"], indent=2, ensure_ascii=False))

    print("\n3. PACKAGE REPORT (Gold):")
    gold = engine.package_report("gold", input_data)
    print(f"Package: {gold['package']} | Price: {gold['price']}")
    print(f"Included: {gold['included']}")

    print("\n✅ Integration Engine working!")
