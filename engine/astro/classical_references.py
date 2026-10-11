"""
VASTU ONE — Classical References Engine
BPHS shloka numbers, text references for each finding
"""

from typing import Dict, List, Any


class ClassicalReferences:
    REFERENCES = {
        "Surya_exalted": {"text": "BPHS", "chapter": "3", "shloka": "49", "ref": "सूर्य मेष में उच्च"},
        "Chandra_exalted": {"text": "BPHS", "chapter": "3", "shloka": "50", "ref": "चंद्र वृषभ में उच्च"},
        "Mangal_exalted": {"text": "BPHS", "chapter": "3", "shloka": "51", "ref": "मंगल मकर में उच्च"},
        "Budh_exalted": {"text": "BPHS", "chapter": "3", "shloka": "52", "ref": "बुध कन्या में उच्च"},
        "Guru_exalted": {"text": "BPHS", "chapter": "3", "shloka": "53", "ref": "गुरु कर्क में उच्च"},
        "Shukra_exalted": {"text": "BPHS", "chapter": "3", "shloka": "54", "ref": "शुक्र मीन में उच्च"},
        "Shani_exalted": {"text": "BPHS", "chapter": "3", "shloka": "55", "ref": "शनि तुला में उच्च"},

        "Kendradhipati_Dosha": {"text": "BPHS", "chapter": "34", "shloka": "12", "ref": "केंद्राधिपति दोष"},
        "Kuja_Dosha": {"text": "BPHS", "chapter": "34", "shloka": "15", "ref": "कुज दोष (मंगल दोष)"},
        "Sade_Sati": {"text": "BPHS", "chapter": "45", "shloka": "6", "ref": "शनि की साढ़े साती"},
        "Kaal_Sarp": {"text": "Saravali", "chapter": "20", "shloka": "15", "ref": "काल सर्प योग"},
        "Gajakesari": {"text": "BPHS", "chapter": "36", "shloka": "8", "ref": "गजकेसरी योग"},
        "Budha_Aditya": {"text": "BPHS", "chapter": "36", "shloka": "12", "ref": "बुधादित्य योग"},
        "Raja_Yoga": {"text": "BPHS", "chapter": "36", "shloka": "20", "ref": "राज योग"},
        "Dhana_Yoga": {"text": "BPHS", "chapter": "36", "shloka": "25", "ref": "धन योग"},
        "Lakshmi_Yoga": {"text": "Phaladeepika", "chapter": "6", "shloka": "18", "ref": "लक्ष्मी योग"},
        "Pancha_Mahapurusha": {"text": "BPHS", "chapter": "36", "shloka": "30", "ref": "पंच महापुरुष योग"},

        "Marriage_7th": {"text": "BPHS", "chapter": "17", "shloka": "1-15", "ref": "7वें भाव से विवाह"},
        "Career_10th": {"text": "BPHS", "chapter": "20", "shloka": "1-12", "ref": "10वें भाव से करियर"},
        "Wealth_2nd": {"text": "BPHS", "chapter": "15", "shloka": "1-10", "ref": "2रे भाव से धन"},
        "Children_5th": {"text": "BPHS", "chapter": "18", "shloka": "1-12", "ref": "5वें भाव से संतान"},
        "Health_6th": {"text": "BPHS", "chapter": "19", "shloka": "1-10", "ref": "6ठे भाव से स्वास्थ्य"},
        "Property_4th": {"text": "BPHS", "chapter": "16", "shloka": "1-10", "ref": "4थे भाव से संपत्ति"},
        "Education_4th_5th": {"text": "BPHS", "chapter": "16-17", "shloka": "1-10", "ref": "शिक्षा 4थे-5वें भाव से"},

        "Ashtakavarga_rule": {"text": "BPHS", "chapter": "66", "shloka": "1-20", "ref": "अष्टकवर्ग गणना"},
        "Shadbala_rule": {"text": "BPHS", "chapter": "27", "shloka": "1-25", "ref": "षड्बल गणना"},
        "Vimshottari_rule": {"text": "BPHS", "chapter": "46-47", "shloka": "1-30", "ref": "विंशोत्तरी दशा"},
        "Nakshatra_rule": {"text": "BPHS", "chapter": "2", "shloka": "1-15", "ref": "नक्षत्र विभाजन"},
    }

    def __init__(self, findings: List = None):
        self.findings = findings or []

    def get_reference(self, key: str) -> Dict:
        return self.REFERENCES.get(key, {
            "text": "BPHS",
            "chapter": "General",
            "shloka": "—",
            "ref": key,
        })

    def attach_references(self, yoga_name: str, dosha_name: str = "") -> Dict:
        key = yoga_name.replace(" ", "_").replace("-", "_")
        ref = self.REFERENCES.get(key, {})
        if not ref and dosha_name:
            key = dosha_name.replace(" ", "_").replace("-", "_")
            ref = self.REFERENCES.get(key, {})
        return ref

    def all_references(self) -> List[Dict]:
        return [{"key": k, **v} for k, v in self.REFERENCES.items()]


def get_classical_reference(key):
    return ClassicalReferences().get_reference(key)


def all_classical_references():
    return ClassicalReferences().all_references()
