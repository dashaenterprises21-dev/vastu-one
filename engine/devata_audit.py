"""
देवता ऑडिट इंजन - Full Status Report
हर 45 देवताओं का detailed analysis देता है
"""


class DevataAudit:
    def __init__(self, grid_81, devatas_json, shastra_rules):
        self.grid = grid_81
        self.shastra = shastra_rules
        self.devata_map = {}
        for d in devatas_json["outer_devatas"] + devatas_json["inner_devatas"]:
            self.devata_map[d["pada"]] = d
        self.issues = []
        self.positive_hits = []
        self.all_devatas_status = []  # हर देवता का status
        self.score = 100

    def audit_object(self, row, col, object_type):
        devata = self.grid.get_devata_at(row, col)
        if not devata:
            return None

        is_defect = object_type in devata.get("negative_objects", [])
        is_good = object_type in devata.get("positive_objects", [])

        status = {
            "pada": devata["pada"],
            "devata": devata["name"],
            "hindi": devata["hindi"],
            "direction": devata["direction"],
            "object": object_type,
            "domain": devata["domain"],
            "element": devata.get("element", "space"),
            "status": "defect" if is_defect else ("correct" if is_good else "neutral"),
        }

        if is_defect:
            rules = self.shastra.find_rules_for_object(
                object_type, devata["direction"], devata["name"]
            )
            severity = "high" if object_type in ["toilet", "fire", "heavy", "water"] else "medium"
            penalty = 8 if severity == "high" else 5

            issue = {
                "pada": devata["pada"],
                "devata": devata["name"],
                "hindi": devata["hindi"],
                "direction": devata["direction"],
                "object": object_type,
                "problem": f"{object_type} in {devata['name']} ({devata['hindi']}) zone",
                "severity": severity,
                "domain_affected": devata["domain"],
                "shastra_reference": rules[0] if rules else None,
                "penalty": penalty,
                "positive_objects": devata.get("positive_objects", []),
                "negative_objects": devata.get("negative_objects", []),
            }
            self.issues.append(issue)
            status["reason"] = issue["problem"]
            status["shastra_reference"] = issue["shastra_reference"]
            self.score -= penalty

        elif is_good:
            self.score += 2
            self.positive_hits.append(status)
            status["reason"] = f"{object_type} correct in {devata['hindi']}"

        self.all_devatas_status.append(status)
        return status

    def audit_plan(self, plan_data):
        for item in plan_data:
            self.audit_object(item["row"], item["col"], item["object"])

        return {
            "total_issues": len(self.issues),
            "total_correct": len(self.positive_hits),
            "issues": self.issues,
            "positive_hits": self.positive_hits,
            "all_devatas_status": self.all_devatas_status,
            "devata_score": max(0, min(100, self.score))
        }