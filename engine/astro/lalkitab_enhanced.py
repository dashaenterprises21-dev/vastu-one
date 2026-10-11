"""
VASTU ONE — Lal Kitab Enhanced
3 Teva Types, Varshphal Lal Kitab, Detailed Remedies
"""

from datetime import datetime
from typing import Dict, List, Any


class LalKitabEnhancedEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    # Lal Kitab planet-house remedies
    LALKITAB_REMEDIES = {
        "Surya": {
            1: "मां के आंचल में सूर्य को जल चढ़ाएं",
            2: "गेहूं का दान करें",
            3: "भाई के साथ मतभेद न करें",
            4: "मां की सेवा करें",
            5: "पुत्र को गुड़ खिलाएं",
            6: "पिता की सेवा करें",
            7: "जीवनसाथी का सम्मान करें",
            8: "तांबे का पात्र दान करें",
            9: "मंदिर में दीप दान करें",
            10: "सरकारी कार्यों में धैर्य",
            11: "सूर्य को अर्घ्य दें",
            12: "माता-पिता की सेवा करें",
        },
        "Chandra": {
            1: "दूध का दान करें",
            2: "माता की सेवा करें",
            3: "सफेद वस्त्र दान करें",
            4: "चांदी का पात्र दान करें",
            5: "सफेद मिठाई का दान",
            6: "मां की सेवा",
            7: "चांदी की चूड़ी धारण करें",
            8: "सोमवार व्रत",
            9: "शिवलिंग पर दूध चढ़ाएं",
            10: "सफेद वस्त्र दान",
            11: "चावल का दान",
            12: "माता का सम्मान",
        },
        "Mangal": {
            1: "लाल मसूर का दान",
            2: "भाई का सहयोग",
            3: "मंगलवार व्रत",
            4: "भूमि का दान",
            5: "लाल मिठाई का दान",
            6: "क्रोध पर नियंत्रण",
            7: "मंगलवार को लाल वस्त्र दान",
            8: "तांबे का दान",
            9: "हनुमान चालीसा",
            10: "साहस रखें",
            11: "लाल वस्त्र दान",
            12: "मंगल मंदिर दर्शन",
        },
        "Budh": {
            1: "हरे मूंग का दान",
            2: "बहन का सहयोग",
            3: "बुधवार व्रत",
            4: "गणेश पूजा",
            5: "हरे वस्त्र दान",
            6: "वाणी पर संयम",
            7: "व्यापार में ईमानदारी",
            8: "मूंग का दान",
            9: "गायत्री मंत्र",
            10: "व्यापार में सफलता",
            11: "हरे फल दान",
            12: "लेखन कार्य करें",
        },
        "Guru": {
            1: "पीली वस्त्र दान",
            2: "गुरुजन सेवा",
            3: "गुरुवार व्रत",
            4: "पीले फूल अर्पित करें",
            5: "संतान की शिक्षा",
            6: "गरीबों की सेवा",
            7: "पीली मिठाई दान",
            8: "सोना दान",
            9: "विष्णु पूजा",
            10: "धर्म में विश्वास",
            11: "हल्दी दान",
            12: "गुरु की सेवा",
        },
        "Shukra": {
            1: "सफेद वस्त्र दान",
            2: "पत्नी का सम्मान",
            3: "शुक्रवार व्रत",
            4: "सफेद फूल अर्पित",
            5: "सफेद मिठाई",
            6: "कन्या पूजन",
            7: "लक्ष्मी पूजा",
            8: "चांदी दान",
            9: "शुक्र मंत्र",
            10: "कला में रुचि",
            11: "दही का दान",
            12: "पत्नी की सेवा",
        },
        "Shani": {
            1: "काले तिल दान",
            2: "गरीबों की सेवा",
            3: "शनिवार व्रत",
            4: "पीपल को जल",
            5: "काले वस्त्र दान",
            6: "मजदूरों की सेवा",
            7: "शनि मंदिर दर्शन",
            8: "लोहा दान",
            9: "शनि चालीसा",
            10: "धैर्य रखें",
            11: "सरसों तेल दान",
            12: "बंदरों को खाना",
        },
        "Rahu": {
            1: "नारियल दान",
            2: "भैरव पूजा",
            3: "काली उड़द दान",
            4: "राहु मंत्र",
            5: "गोमेद धारण",
            6: "भैरव मंदिर दर्शन",
            7: "कंबल दान",
            8: "नारियल जल में डालें",
            9: "सर्प दोष पूजा",
            10: "विदेश यात्रा",
            11: "उड़द दाल दान",
            12: "शनि शांति",
        },
        "Ketu": {
            1: "कुत्ते को रोटी",
            2: "गणेश पूजा",
            3: "कंबल दान",
            4: "लहसुनिया धारण",
            5: "गणेश जी की मूर्ति",
            6: "गणेश चतुर्थी व्रत",
            7: "कुत्ते की सेवा",
            8: "तिल का दान",
            9: "गणेश अथर्वशीर्ष",
            10: "आध्यात्मिक मार्ग",
            11: "कंबल दान",
            12: "मोक्ष पथ",
        },
    }

    # Teva types
    TEVA_TYPES = {
        "lagna": "लग्न कुंडली — शरीर और व्यक्तित्व",
        "chandra": "चंद्र कुंडली — मन और भावनाएं",
        "surya": "सूर्य कुंडली — आत्मा और भाग्य",
    }

    def __init__(self, positions: Dict, lagna: Dict, doshas: List):
        self.pos = positions
        self.lagna = lagna
        self.doshas = doshas

    def analyze_all(self) -> Dict:
        return {
            "teva_analysis": self._teva_analysis(),
            "house_wise_remedies": self._house_wise_remedies(),
            "planet_remedies": self._planet_remedies(),
            "varshphal_lalkitab": self._varshphal_lalkitab(),
            "kudrati_upay": self._kudrati_upay(),
        }

    def _teva_analysis(self) -> List[Dict]:
        """Analyze 3 Teva types"""
        result = []
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        chandra_rashi = self.pos.get("Chandra", {}).get("rashi", "Mesh")
        surya_rashi = self.pos.get("Surya", {}).get("rashi", "Mesh")

        for teva, meaning in self.TEVA_TYPES.items():
            if teva == "lagna":
                rashi = lagna_rashi
            elif teva == "chandra":
                rashi = chandra_rashi
            else:
                rashi = surya_rashi

            rashi_idx = self.SIGNS.index(rashi) if rashi in self.SIGNS else 0
            result.append({
                "teva": teva,
                "teva_hindi": meaning.split(" — ")[0],
                "rashi": rashi,
                "rashi_hindi": self.SIGNS_HINDI[rashi_idx],
                "meaning": meaning.split(" — ")[1] if " — " in meaning else "",
            })
        return result

    def _house_wise_remedies(self) -> List[Dict]:
        """Get remedies based on planets in each house"""
        result = []
        for b in range(1, 13):
            planets_in_house = []
            for p, pd in self.pos.items():
                if pd.get("bhav") == b:
                    planets_in_house.append(p)

            if not planets_in_house:
                continue

            remedies = []
            for p in planets_in_house:
                remedy = self.LALKITAB_REMEDIES.get(p, {}).get(b, "")
                if remedy:
                    remedies.append({
                        "planet": p,
                        "planet_hindi": self.PLANETS_HINDI.get(p, p),
                        "remedy": remedy,
                    })

            if remedies:
                result.append({
                    "house": b,
                    "planets": [self.PLANETS_HINDI.get(p, p) for p in planets_in_house],
                    "remedies": remedies,
                })
        return result

    def _planet_remedies(self) -> List[Dict]:
        """Planet-specific Lal Kitab remedies"""
        result = []
        for p, pd in self.pos.items():
            b = pd.get("bhav")
            if not b: continue
            remedy = self.LALKITAB_REMEDIES.get(p, {}).get(b, "")
            if remedy:
                result.append({
                    "planet": p,
                    "planet_hindi": self.PLANETS_HINDI.get(p, p),
                    "bhava": b,
                    "remedy": remedy,
                })
        return result

    def _varshphal_lalkitab(self) -> Dict:
        """Annual Lal Kitab prediction"""
        now = datetime.now()
        return {
            "year": now.year,
            "remedies": [
                "हर अमावस्या को पीपल को जल दें",
                "पितृ पक्ष में श्राद्ध करें",
                "गाय को हरा चारा दें",
                "मंगलवार को हनुमान चालीसा पढ़ें",
                "शनिवार को सरसों का तेल दान करें",
            ],
            "specific_days": {
                "Monday": "शिवलिंग पर जल",
                "Tuesday": "हनुमान पूजा",
                "Wednesday": "गणेश पूजा",
                "Thursday": "विष्णु पूजा",
                "Friday": "लक्ष्मी पूजा",
                "Saturday": "शनि/हनुमान",
                "Sunday": "सूर्य अर्घ्य",
            },
        }

    def _kudrati_upay(self) -> List[str]:
        """Natural remedies from Lal Kitab"""
        return [
            "सूर्योदय से पहले उठें",
            "पानी को तांबे के पात्र में रखें",
            "कौवे, कुत्ते, गाय को खाना दें",
            "पीपल, तुलसी, नीम की सेवा करें",
            "झूठ न बोलें, चोरी न करें",
            "माता-पिता की सेवा करें",
            "गरीबों की सहायता करें",
            "हर रोज सूर्य को अर्घ्य दें",
            "अपमान सहन करें, बदले में कुछ न करें",
        ]


def analyze_lalkitab_enhanced(positions, lagna, doshas):
    return LalKitabEnhancedEngine(positions, lagna, doshas).analyze_all()
