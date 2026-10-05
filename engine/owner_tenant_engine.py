"""
Owner/Tenant Engine — Vastu One Enterprise
Owner vs Tenant Layer — Different remedies, rights, scope
"""

import json
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class OwnerTenantEngine:
    """Owner/Tenant layer — who can do what remedies"""

    def __init__(self):
        # Ownership types with rights and remedy scope
        self.ownership_types = {
            "owner_occupied": {
                "hindi": "स्वामी-निवासी",
                "can_do": ["structural", "non_structural", "pooja", "occult", "gemstone", "renovation"],
                "cannot_do": [],
                "remedy_scope": "full",
                "permission_needed": False,
                "cost_bearer": "self"
            },
            "tenant_occupied": {
                "hindi": "किरायेदार-निवासी",
                "can_do": ["non_structural", "pooja", "portable", "color", "mantra"],
                "cannot_do": ["structural", "renovation", "demolition", "major_construction"],
                "remedy_scope": "limited",
                "permission_needed": True,
                "permission_from": "owner",
                "cost_bearer": "self"
            },
            "rented_out": {
                "hindi": "किराये पर दिया",
                "can_do": ["non_structural", "tenant_advisory", "pooja"],
                "cannot_do": ["structural", "tenant_forced_remedy"],
                "remedy_scope": "minimal",
                "permission_needed": True,
                "permission_from": "tenant",
                "cost_bearer": "owner_or_tenant"
            },
            "family_owned": {
                "hindi": "पारिवारिक स्वामित्व",
                "can_do": ["structural", "non_structural", "pooja", "consensus_based"],
                "cannot_do": ["unilateral_structural"],
                "remedy_scope": "shared",
                "permission_needed": True,
                "permission_from": "family_consensus",
                "cost_bearer": "shared"
            },
            "partnership": {
                "hindi": "साझेदारी",
                "can_do": ["non_structural", "pooja", "consensus_based"],
                "cannot_do": ["unilateral_structural", "partner_specific_remedy"],
                "remedy_scope": "shared",
                "permission_needed": True,
                "permission_from": "all_partners",
                "cost_bearer": "shared"
            },
            "landlord_tenant": {
                "hindi": "मकान मालिक-किरायेदार",
                "can_do": ["non_structural", "pooja", "communication"],
                "cannot_do": ["structural", "forced_remedy"],
                "remedy_scope": "negotiated",
                "permission_needed": True,
                "permission_from": "both_parties",
                "cost_bearer": "negotiated"
            }
        }

        # Remedy categories with owner/tenant applicability
        self.remedy_categories = {
            "structural": {"owner": True, "tenant": False, "cost": "high", "duration": "long"},
            "non_structural": {"owner": True, "tenant": True, "cost": "low", "duration": "short"},
            "pooja": {"owner": True, "tenant": True, "cost": "low", "duration": "daily"},
            "occult": {"owner": True, "tenant": True, "cost": "medium", "duration": "medium"},
            "gemstone": {"owner": True, "tenant": True, "cost": "high", "duration": "long"},
            "color": {"owner": True, "tenant": True, "cost": "low", "duration": "short"},
            "mantra": {"owner": True, "tenant": True, "cost": "free", "duration": "daily"},
            "portable": {"owner": True, "tenant": True, "cost": "low", "duration": "short"},
            "renovation": {"owner": True, "tenant": False, "cost": "very_high", "duration": "long"},
            "demolition": {"owner": True, "tenant": False, "cost": "very_high", "duration": "long"}
        }

    # ─────────────────────────────────────────
    # 1. OWNERSHIP ANALYSIS
    # ─────────────────────────────────────────
    def ownership_analysis(self, ownership_type: str) -> Dict:
        """Ownership type ka full analysis"""
        ownership_type = ownership_type.lower()
        if ownership_type not in self.ownership_types:
            return {"error": f"Ownership '{ownership_type}' not found. Options: {list(self.ownership_types.keys())}"}
        info = self.ownership_types[ownership_type]
        return {
            "ownership_type": ownership_type,
            "hindi": info["hindi"],
            "can_do": info["can_do"],
            "cannot_do": info["cannot_do"],
            "remedy_scope": info["remedy_scope"],
            "permission_needed": info["permission_needed"],
            "permission_from": info.get("permission_from", "none"),
            "cost_bearer": info["cost_bearer"]
        }

    # ─────────────────────────────────────────
    # 2. REMEDY PERMISSION CHECK
    # ─────────────────────────────────────────
    def remedy_permission(self, ownership_type: str, remedy_category: str) -> Dict:
        """Kya ye ownership type ye remedy kar sakti hai?"""
        ownership_type = ownership_type.lower()
        remedy_category = remedy_category.lower()

        if ownership_type not in self.ownership_types:
            return {"error": f"Ownership '{ownership_type}' not found"}
        if remedy_category not in self.remedy_categories:
            return {"error": f"Remedy '{remedy_category}' not found"}

        info = self.ownership_types[ownership_type]
        remedy_info = self.remedy_categories[remedy_category]

        # Determine if allowed
        if ownership_type == "owner_occupied":
            allowed = True
        elif ownership_type == "tenant_occupied":
            allowed = remedy_category in info["can_do"]
        elif ownership_type == "rented_out":
            allowed = remedy_category in info["can_do"]
        else:
            allowed = remedy_category in info["can_do"]

        return {
            "ownership_type": ownership_type,
            "remedy_category": remedy_category,
            "allowed": allowed,
            "permission_needed": info["permission_needed"] and not allowed,
            "permission_from": info.get("permission_from", "self"),
            "cost_bearer": info["cost_bearer"],
            "remedy_cost": remedy_info["cost"],
            "duration": remedy_info["duration"],
            "note": self._permission_note(ownership_type, remedy_category, allowed)
        }

    def _permission_note(self, ownership: str, remedy: str, allowed: bool) -> str:
        if allowed:
            return f"✅ {ownership} can do {remedy} remedy directly"
        return f"⚠️ {ownership} needs permission for {remedy} remedy"

    # ─────────────────────────────────────────
    # 3. REMEDY SUGGESTIONS BY OWNERSHIP
    # ─────────────────────────────────────────
    def suggested_remedies(self, ownership_type: str, issues: List[str]) -> List[Dict]:
        """Ownership ke hisaab se remedies suggest karo"""
        ownership_type = ownership_type.lower()
        if ownership_type not in self.ownership_types:
            return [{"error": f"Ownership '{ownership_type}' not found"}]

        info = self.ownership_types[ownership_type]
        suggestions = []

        for issue in issues:
            # Map issue to remedy category
            category = self._issue_to_category(issue)
            if category in info["can_do"]:
                suggestions.append({
                    "issue": issue,
                    "remedy_category": category,
                    "can_do": True,
                    "cost": self.remedy_categories.get(category, {}).get("cost", "medium"),
                    "priority": "HIGH"
                })
            else:
                suggestions.append({
                    "issue": issue,
                    "remedy_category": category,
                    "can_do": False,
                    "alternative": self._alternative_remedy(category, info["can_do"]),
                    "note": f"Need {info.get('permission_from', 'owner')} permission",
                    "priority": "MEDIUM"
                })
        return suggestions

    def _issue_to_category(self, issue: str) -> str:
        mapping = {
            "toilet_ne": "structural",
            "kitchen_se": "structural",
            "entrance_wrong": "structural",
            "bedroom_wrong": "non_structural",
            "cash_wrong": "non_structural",
            "pooja_wrong": "non_structural",
            "negative_energy": "occult",
            "health_issue": "pooja",
            "wealth_issue": "gemstone",
            "relationship_issue": "color"
        }
        return mapping.get(issue, "non_structural")

    def _alternative_remedy(self, category: str, can_do: List[str]) -> str:
        """Agar structural nahi kar sakte toh alternative"""
        if category == "structural" and "non_structural" in can_do:
            return "Use non-structural remedy (color, metal, mirror, plant)"
        if category == "renovation" and "non_structural" in can_do:
            return "Use portable remedy (yantra, gemstone, pooja)"
        return "Consult owner for permission"

    # ─────────────────────────────────────────
    # 4. OWNER-TENANT AGREEMENT
    # ─────────────────────────────────────────
    def agreement_template(self, ownership_type: str, issues: List[str]) -> Dict:
        """Owner-tenant agreement ke liye template"""
        ownership_type = ownership_type.lower()
        info = self.ownership_types.get(ownership_type, {})
        return {
            "ownership_type": ownership_type,
            "issues": issues,
            "responsibilities": {
                "owner": self._owner_responsibilities(ownership_type),
                "tenant": self._tenant_responsibilities(ownership_type)
            },
            "cost_sharing": self._cost_sharing(ownership_type),
            "permission_process": info.get("permission_from", "self"),
            "validity": "Until tenancy ends"
        }

    def _owner_responsibilities(self, ownership: str) -> List[str]:
        if ownership in ["owner_occupied", "family_owned"]:
            return ["All structural remedies", "Major renovations", "Pooja room setup"]
        return ["Structural remedies", "Permission for tenant remedies", "Major repairs"]

    def _tenant_responsibilities(self, ownership: str) -> List[str]:
        if ownership in ["tenant_occupied", "rented_out"]:
            return ["Non-structural remedies", "Daily pooja", "Cleanliness", "Mantra chanting"]
        return ["Maintain cleanliness", "Daily pooja", "Inform owner of issues"]

    def _cost_sharing(self, ownership: str) -> Dict:
        if ownership == "owner_occupied":
            return {"owner": "100%", "tenant": "0%"}
        elif ownership == "tenant_occupied":
            return {"owner": "structural", "tenant": "non_structural"}
        elif ownership == "rented_out":
            return {"owner": "structural + major", "tenant": "daily + minor"}
        return {"owner": "50%", "tenant": "50%", "note": "Negotiable"}

    # ─────────────────────────────────────────
    # 5. FULL REPORT
    # ─────────────────────────────────────────
    def full_report(self, ownership_type: str, issues: List[str]) -> Dict:
        """Complete owner/tenant report"""
        analysis = self.ownership_analysis(ownership_type)
        suggestions = self.suggested_remedies(ownership_type, issues)
        agreement = self.agreement_template(ownership_type, issues)
        return {
            "ownership_analysis": analysis,
            "suggested_remedies": suggestions,
            "agreement_template": agreement,
            "summary": {
                "can_do_count": len([s for s in suggestions if s.get("can_do")]),
                "needs_permission_count": len([s for s in suggestions if not s.get("can_do")]),
                "total_issues": len(issues)
            }
        }


# ─────────────────────────────────────────
# CLI TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    engine = OwnerTenantEngine()
    print("=" * 60)
    print("OWNER/TENANT ENGINE TEST")
    print("=" * 60)

    print("\n1. OWNER-OCCUPIED ANALYSIS:")
    print(json.dumps(engine.ownership_analysis("owner_occupied"), indent=2, ensure_ascii=False))

    print("\n2. TENANT-OCCUPIED ANALYSIS:")
    print(json.dumps(engine.ownership_analysis("tenant_occupied"), indent=2, ensure_ascii=False))

    print("\n3. PERMISSION CHECK (Tenant + Structural):")
    print(json.dumps(engine.remedy_permission("tenant_occupied", "structural"), indent=2, ensure_ascii=False))

    print("\n4. PERMISSION CHECK (Tenant + Pooja):")
    print(json.dumps(engine.remedy_permission("tenant_occupied", "pooja"), indent=2, ensure_ascii=False))

    print("\n5. SUGGESTED REMEDIES (Tenant with issues):")
    issues = ["toilet_ne", "kitchen_se", "negative_energy", "health_issue"]
    print(json.dumps(engine.suggested_remedies("tenant_occupied", issues), indent=2, ensure_ascii=False))

    print("\n6. FULL REPORT SUMMARY (Tenant):")
    report = engine.full_report("tenant_occupied", issues)
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))

    print("\n✅ Owner/Tenant Engine working!")
