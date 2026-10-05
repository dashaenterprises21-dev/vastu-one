"""
शास्त्रीय नियम इंजन
हर दोष के लिए शास्त्र से प्रमाण और असर का वज़न।
"""

import json
from pathlib import Path


class ShastraRules:
    def __init__(self, rules_file):
        with open(rules_file, "r", encoding="utf-8-sig") as f:
            self.data = json.load(f)
        self.rules = self.data["rules"]

    def find_rules_for_object(self, object_type, zone, devata_name=None):
        """किसी object + zone के लिए शास्त्रीय नियम खोजो"""
        matched = []
        for rule in self.rules:
            rule_text = json.dumps(rule, ensure_ascii=False).lower()
            # Object match
            if object_type.lower() in rule_text:
                matched.append(rule)
                continue
            # Zone match
            if zone.lower() in rule_text:
                matched.append(rule)
                continue
            # Devata match
            if devata_name and devata_name.lower() in rule_text:
                matched.append(rule)
        return matched

    def get_rule_by_id(self, rule_id):
        for rule in self.rules:
            if rule["id"] == rule_id:
                return rule
        return None

    def get_all_sources(self):
        return self.data["sources"]