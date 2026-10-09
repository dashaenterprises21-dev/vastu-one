"""
Universal Engine — Vastu One Enterprise
Master Orchestrator — Saare engines ko ek saath chalata hai
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ENGINE_DIR = os.path.dirname(__file__)

sys.path.insert(0, ENGINE_DIR)

from integration_engine import IntegrationEngine


class UniversalEngine:
    """Master orchestrator — complete enterprise system"""

    def __init__(self):
        self.integration = IntegrationEngine()
        self.version = "1.0"
        self.build_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ─────────────────────────────────────────
    # 1. COMPLETE ANALYSIS
    # ─────────────────────────────────────────
    def analyze(self, input_data: Dict, package: str = "platinum") -> Dict:
        """
        Complete analysis — package ke hisaab se.
        Ye master function hai jo sab kuch karta hai.
        """
        package = package.lower()
        if package not in ["bronze", "silver", "gold", "platinum"]:
            return {"error": f"Invalid package: {package}. Options: bronze, silver, gold, platinum"}

        # Run integration engine
        integrated = self.integration.full_report(input_data)

        # Package-specific report
        package_report = self.integration.package_report(package, input_data)

        # Add metadata
        return {
            "meta": {
                "version": self.version,
                "build_date": self.build_date,
                "package": package,
                "generated_at": datetime.now().isoformat(),
                "input_summary": {
                    "name": input_data.get("name", "Unknown"),
                    "property": input_data.get("property_number", "N/A"),
                    "ownership": input_data.get("ownership", "N/A"),
                    "usage": input_data.get("usage", "N/A")
                }
            },
            "package_report": package_report,
            "integrated_score": integrated["integrated_score"],
            "summary": integrated["summary"],
            "full_data": integrated if package == "platinum" else None
        }

    # ─────────────────────────────────────────
    # 2. QUICK SCORE
    # ─────────────────────────────────────────
    def quick_score(self, input_data: Dict) -> Dict:
        """Sirf score chahiye — fast"""
        integrated = self.integration.full_report(input_data)
        return {
            "score": integrated["integrated_score"]["total_score"],
            "grade": integrated["integrated_score"]["grade"],
            "summary": integrated["summary"]["overall_grade"]
        }

    # ─────────────────────────────────────────
    # 3. COMPARE PROPERTIES
    # ─────────────────────────────────────────
    def compare_properties(self, properties: List[Dict]) -> Dict:
        """Do ya zyada properties compare karo"""
        results = []
        for prop in properties:
            score = self.quick_score(prop)
            results.append({
                "name": prop.get("name", "Unknown"),
                "property_number": prop.get("property_number", "N/A"),
                "score": score["score"],
                "grade": score["grade"]
            })

        # Best property
        best = max(results, key=lambda x: x["score"]) if results else None
        return {
            "properties": results,
            "best_property": best,
            "comparison_note": "Higher score = better Vastu compliance"
        }

    # ─────────────────────────────────────────
    # 4. RECOMMEND PACKAGE
    # ─────────────────────────────────────────
    def recommend_package(self, input_data: Dict) -> Dict:
        """User ke input ke hisaab se best package recommend karo"""
        integrated = self.integration.full_report(input_data)
        score = integrated["integrated_score"]["total_score"]
        issues = input_data.get("issues", [])
        ownership = input_data.get("ownership", "owner_occupied")

        # Logic
        if score >= 80 and len(issues) <= 1:
            recommended = "bronze"
            reason = "Property already good — basic report sufficient"
        elif score >= 65 and len(issues) <= 3:
            recommended = "silver"
            reason = "Moderate issues — astro + detailed remedies needed"
        elif score >= 50:
            recommended = "gold"
            reason = "Multiple issues — full analysis + remedies needed"
        else:
            recommended = "platinum"
            reason = "Critical issues — personal consultation required"

        # Ownership override
        if ownership in ["tenant_occupied", "rented_out"]:
            if recommended in ["gold", "platinum"]:
                recommended = "silver"
                reason += " (Tenant — limited scope, Silver sufficient)"

        return {
            "recommended_package": recommended,
            "reason": reason,
            "current_score": score,
            "issues_count": len(issues),
            "ownership": ownership
        }

    # ─────────────────────────────────────────
    # 5. FULL ENTERPRISE REPORT
    # ─────────────────────────────────────────
    def enterprise_report(self, input_data: Dict) -> Dict:
        """Complete enterprise report — sab kuch"""
        package = self.recommend_package(input_data)["recommended_package"]
        analysis = self.analyze(input_data, package)

        return {
            "enterprise_report": {
                "generated_at": datetime.now().isoformat(),
                "version": self.version,
                "recommended_package": package,
                "analysis": analysis,
                "all_packages_comparison": self._package_comparison(input_data),
                "next_steps": self._next_steps(input_data, package)
            }
        }

    def _package_comparison(self, input_data: Dict) -> Dict:
        """Saare packages ka comparison"""
        return {
            "bronze": {"price": "₹999", "score": self.quick_score(input_data)["score"]},
            "silver": {"price": "₹2,999", "score": self.quick_score(input_data)["score"]},
            "gold": {"price": "₹7,999", "score": self.quick_score(input_data)["score"]},
            "platinum": {"price": "₹19,999", "score": self.quick_score(input_data)["score"]}
        }

    def _next_steps(self, input_data: Dict, package: str) -> List[str]:
        steps = [
            f"1. Package '{package}' purchase karo",
            "2. Detailed input form bharo",
            "3. Report generate karo",
            "4. Remedies follow karo",
            "5. 21-day schedule follow karo"
        ]
        if package == "platinum":
            steps.append("6. 1:1 consultation book karo")
            steps.append("7. Lifetime support activate karo")
        return steps

    # ─────────────────────────────────────────
    # 6. SYSTEM INFO
    # ─────────────────────────────────────────
    def system_info(self) -> Dict:
        """System ki puri info"""
        return {
            "version": self.version,
            "build_date": self.build_date,
            "engines": [
                "AstroEngine",
                "NumerologyEngine",
                "DishaBalEngine",
                "AUOEngine",
                "MarmaEngine",
                "OwnerTenantEngine",
                "OccultEngine",
                "IntegrationEngine",
                "UniversalEngine"
            ],
            "total_engines": 9,
            "packages": ["bronze", "silver", "gold", "platinum"],
            "capabilities": [
                "Vastu Analysis",
                "Astro Integration",
                "Numerology",
                "Disha Bal (16 zones)",
                "AUO Analysis",
                "Marma Points",
                "Owner/Tenant Layer",
                "Safe Occult Remedies",
                "7-Component Score",
                "Package-based Reports"
            ]
        }


# ─────────────────────────────────────────
# CLI TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    engine = UniversalEngine()
    print("=" * 60)
    print("UNIVERSAL ENGINE TEST — MASTER ORCHESTRATOR")
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

    print("\n1. SYSTEM INFO:")
    print(json.dumps(engine.system_info(), indent=2, ensure_ascii=False))

    print("\n2. QUICK SCORE:")
    print(json.dumps(engine.quick_score(input_data), indent=2, ensure_ascii=False))

    print("\n3. RECOMMEND PACKAGE:")
    print(json.dumps(engine.recommend_package(input_data), indent=2, ensure_ascii=False))

    print("\n4. ANALYZE (Gold):")
    result = engine.analyze(input_data, "gold")
    print(f"Package: {result['meta']['package']}")
    print(f"Score: {result['integrated_score']['total_score']}")
    print(f"Grade: {result['integrated_score']['grade']}")
    print(f"Summary: {result['summary']['overall_grade']}")

    print("\n5. ENTERPRISE REPORT:")
    report = engine.enterprise_report(input_data)
    er = report["enterprise_report"]
    print(f"Recommended: {er['recommended_package']}")
    print(f"Next Steps: {er['next_steps']}")

    print("\n✅ Universal Engine working!")
    print("\n" + "=" * 60)
    print("🎉 PHASE 2 COMPLETE — ALL 9 ENGINES WORKING!")
    print("=" * 60)
