"""
VASTU ONE — Medical Astrology Engine
Health vulnerabilities, weak organs, preventive care
"""

from typing import Dict, List, Any


class MedicalAstroEngine:
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    # Planets → body parts
    PLANET_BODY = {
        "Surya": ["हृदय", "आँख", "हड्डियां", "पित्त"],
        "Chandra": ["मन", "फेफड़े", "जल तत्व", "रक्त"],
        "Mangal": ["रक्त", "मांसपेशियां", "सिर", "अग्नि"],
        "Budh": ["त्वचा", "नसें", "वाणी", "मस्तिष्क"],
        "Guru": ["यकृत", "चर्बी", "कान", "वृद्धि"],
        "Shukra": ["गुर्दे", "प्रजनन", "नेत्र", "त्वचा"],
        "Shani": ["हड्डियां", "दांत", "नसें", "वात"],
        "Rahu": ["विष", "अचानक रोग", "मानसिक"],
        "Ketu": ["आंत", "संक्रमण", "अजीब रोग"],
    }

    # Houses → body parts
    BHAVA_BODY = {
        1: "शरीर, सिर, मस्तिष्क",
        2: "आँख, मुंह, दांत, जीभ",
        3: "कंधे, हाथ, फेफड़े",
        4: "हृदय, छाती",
        5: "पेट, यकृत",
        6: "आंत, गुर्दे",
        7: "मूत्र, प्रजनन",
        8: "गुप्त अंग, मलाशय",
        9: "कूल्हे, जांघ",
        10: "घुटने, जोड़",
        11: "पिंडली, टखने",
        12: "पैर, आँख",
    }

    def __init__(self, positions: Dict, lagna: Dict, doshas: List):
        self.pos = positions
        self.lagna = lagna
        self.doshas = doshas

    def analyze_all(self) -> Dict[str, Any]:
        return {
            "weak_planets": self._weak_planets(),
            "vulnerable_organs": self._vulnerable_organs(),
            "preventive_care": self._preventive_care(),
            "longevity": self._longevity(),
            "health_risks": self._health_risks(),
        }

    def _weak_planets(self) -> List[Dict]:
        weak = []
        for p, pd in self.pos.items():
            if p in ["Rahu","Ketu"]: continue
            bhav = pd.get("bhav")
            if bhav in [6, 8, 12]:
                weak.append({
                    "planet": p,
                    "planet_hindi": self.PLANETS_HINDI.get(p, p),
                    "bhav": bhav,
                    "reason": f"भाव {bhav} में — रोग कारक",
                })
        return weak

    def _vulnerable_organs(self) -> List[Dict]:
        organs = []
        for p, pd in self.pos.items():
            bhav = pd.get("bhav")
            if bhav in [6, 8, 12]:
                body = self.PLANET_BODY.get(p, [])
                organs.append({
                    "planet": self.PLANETS_HINDI.get(p, p),
                    "bhav": bhav,
                    "organs": body,
                    "bhava_area": self.BHAVA_BODY.get(bhav, ""),
                })
        return organs

    def _preventive_care(self) -> List[str]:
        care = [
            "नियमित स्वास्थ्य जांच कराएं",
            "संतुलित आहार लें",
            "प्रतिदिन व्यायाम करें",
            "पर्याप्त नींद लें",
            "तनाव से बचें",
            "जल का पर्याप्त सेवन करें",
        ]
        # Add specific based on weak planets
        for p, pd in self.pos.items():
            if pd.get("bhav") in [6, 8, 12]:
                if p == "Shani":
                    care.append("वात रोगों से बचाव करें — गर्म पानी पिएं")
                elif p == "Mangal":
                    care.append("रक्तचाप नियंत्रित रखें")
                elif p == "Chandra":
                    care.append("मानसिक स्वास्थ्य का ध्यान रखें")
                elif p == "Surya":
                    care.append("आँखों की जांच कराएं")
        return care

    def _longevity(self) -> Dict:
        # Simplified longevity calculation based on 3rd/8th house
        third = self.pos.get("Mangal", {})
        eighth_bhav_planets = [p for p, pd in self.pos.items() if pd.get("bhav") == 8]
        lagna_bhav_planets = [p for p, pd in self.pos.items() if pd.get("bhav") == 1]

        score = 50
        if lagna_bhav_planets: score += 10
        if third.get("bhav") in [3, 8, 11]: score += 10
        if eighth_bhav_planets: score += 5

        if score >= 70: duration = "दीर्घायु (70-100 वर्ष)"
        elif score >= 55: duration = "मध्यम आयु (50-70 वर्ष)"
        else: duration = "अल्पायु (30-50 वर्ष)"

        return {"score": score, "duration": duration}

    def _health_risks(self) -> List[str]:
        risks = []
        for d in self.doshas:
            name = d.get("name", "")
            if "मंगल" in name:
                risks.append("रक्त विकार, सर्जरी, दुर्घटना")
            elif "शनि" in name:
                risks.append("वात रोग, जोड़ों का दर्द, हड्डी")
            elif "राहु" in name:
                risks.append("मानसिक रोग, विष, अचानक")
            elif "केतु" in name:
                risks.append("आंत संक्रमण, त्वचा रोग")
        if not risks:
            risks = ["कोई विशेष स्वास्थ्य जोखिम नहीं"]
        return risks


def analyze_medical_astrology(positions, lagna, doshas):
    return MedicalAstroEngine(positions, lagna, doshas).analyze_all()
