"""
VASTU ONE — Jaimini System Engine
Char Dasha, Karakamsha, Swamsha, Atmakaraka, Chara Karakas
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


class JaiminiEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    # Chara Karakas (order of importance based on degrees)
    CHARA_KARAKAS = [
        {"num": 1, "name": "Atmakaraka", "hindi": "आत्मकारक", "meaning": "Soul planet — main life purpose"},
        {"num": 2, "name": "Amatyakaraka", "hindi": "अमात्यकारक", "meaning": "Career, minister — profession"},
        {"num": 3, "name": "Bhratrikaraka", "hindi": "भ्रातृकारक", "meaning": "Siblings, guru"},
        {"num": 4, "name": "Matrikaraka", "hindi": "मातृकारक", "meaning": "Mother, education"},
        {"num": 5, "name": "Pitrikaraka", "hindi": "पितृकारक", "meaning": "Father, authority"},
        {"num": 6, "name": "Putrakaraka", "hindi": "पुत्रकारक", "meaning": "Children, disciples"},
        {"num": 7, "name": "Gnatikaraka", "hindi": "ज्ञातिकारक", "meaning": "Enemies, obstacles"},
        {"num": 8, "name": "Darakaraka", "hindi": "दारकारक", "meaning": "Spouse, marriage"},
    ]

    # Char Dasha order — based on Lagna sign
    CHARA_DASHA_ORDER = {
        "Mesh": ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"],
        "Vrishabh": ["Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen","Mesh"],
        "Mithun": ["Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen","Mesh","Vrishabh"],
        "Kark": ["Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen","Mesh","Vrishabh","Mithun"],
        "Simha": ["Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen","Mesh","Vrishabh","Mithun","Kark"],
        "Kanya": ["Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen","Mesh","Vrishabh","Mithun","Kark","Simha"],
        "Tula": ["Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen","Mesh","Vrishabh","Mithun","Kark","Simha","Kanya"],
        "Vrishchik": ["Vrishchik","Dhanu","Makar","Kumbh","Meen","Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula"],
        "Dhanu": ["Dhanu","Makar","Kumbh","Meen","Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik"],
        "Makar": ["Makar","Kumbh","Meen","Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu"],
        "Kumbh": ["Kumbh","Meen","Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar"],
        "Meen": ["Meen","Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh"],
    }

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict:
        return {
            "chara_karakas": self._chara_karakas(),
            "karakamsha": self._karakamsha(),
            "swamsha": self._swamsha(),
            "chara_dasha": self._chara_dasha(),
            "jaimini_predictions": self._predictions(),
        }

    def _chara_karakas(self) -> List[Dict]:
        """Calculate 8 Chara Karakas based on degrees"""
        planets_with_degrees = []
        # Only 7 planets (Rahu reversed)
        for p in ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani","Rahu"]:
            pd = self.pos.get(p, {})
            deg = pd.get("degree", 0)
            if p == "Rahu":
                deg = 30 - deg  # Rahu reverse
            planets_with_degrees.append({"planet": p, "degree": deg})

        # Sort by degree descending
        planets_with_degrees.sort(key=lambda x: x["degree"], reverse=True)

        result = []
        for i, karaka in enumerate(self.CHARA_KARAKAS):
            if i < len(planets_with_degrees):
                p = planets_with_degrees[i]
                result.append({
                    "num": karaka["num"],
                    "name": karaka["name"],
                    "hindi": karaka["hindi"],
                    "meaning": karaka["meaning"],
                    "planet": p["planet"],
                    "planet_hindi": self.PLANETS_HINDI.get(p["planet"], ""),
                    "degree": round(p["degree"], 2),
                })
        return result

    def _karakamsha(self) -> Dict:
        """Karakamsha — Navamsa of Atmakaraka"""
        karakas = self._chara_karakas()
        atmakaraka = next((k for k in karakas if k["name"] == "Atmakaraka"), None)
        if not atmakaraka:
            return {}
        ak_planet = atmakaraka["planet"]
        pd = self.pos.get(ak_planet, {})
        lon = pd.get("longitude", 0)
        # Navamsa sign = (lon * 9) / 30 % 12
        navamsa_idx = int((lon * 9) / 30) % 12
        return {
            "atmakaraka": ak_planet,
            "atmakaraka_hindi": atmakaraka["planet_hindi"],
            "karakamsha_rashi": self.SIGNS[navamsa_idx],
            "karakamsha_rashi_hindi": self.SIGNS_HINDI[navamsa_idx],
            "meaning": "आत्मकारक का नवांश — soul's purpose, dharma",
        }

    def _swamsha(self) -> Dict:
        """Swamsha — same as Karakamsha, spiritual path"""
        karakamsha = self._karakamsha()
        return {
            "swamsha_rashi": karakamsha.get("karakamsha_rashi", ""),
            "swamsha_rashi_hindi": karakamsha.get("karakamsha_rashi_hindi", ""),
            "meaning": "स्वांश — आध्यात्मिक मार्ग",
        }

    def _chara_dasha(self) -> List[Dict]:
        """Calculate Char Dasha (12-year cycle)"""
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        order = self.CHARA_DASHA_ORDER.get(lagna_rashi, self.CHARA_DASHA_ORDER["Mesh"])
        now = datetime.now()
        result = []
        for i, rashi in enumerate(order):
            start = now + timedelta(days=365 * i)
            end = start + timedelta(days=365)
            result.append({
                "rashi": rashi,
                "rashi_hindi": self.SIGNS_HINDI[self.SIGNS.index(rashi)],
                "year": i + 1,
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
                "is_current": i == 0,
            })
        return result

    def _predictions(self) -> List[str]:
        karakas = self._chara_karakas()
        karakamsha = self._karakamsha()
        ak = next((k for k in karakas if k["name"] == "Atmakaraka"), {})
        amk = next((k for k in karakas if k["name"] == "Amatyakaraka"), {})
        dk = next((k for k in karakas if k["name"] == "Darakaraka"), {})

        preds = []
        if ak:
            preds.append(f"आत्मकारक: {ak.get('planet_hindi','')} — आपके जीवन का मुख्य उद्देश्य")
        if amk:
            preds.append(f"अमात्यकारक: {amk.get('planet_hindi','')} — करियर और पेशा")
        if dk:
            preds.append(f"दारकारक: {dk.get('planet_hindi','')} — विवाह और जीवनसाथी")
        if karakamsha:
            preds.append(f"कारकांश: {karakamsha.get('karakamsha_rashi_hindi','')} — आत्मा का धर्म")
        preds.append("चर दशा: 12 वर्ष का चक्र — जीवन के चरण")
        return preds


def analyze_jaimini(positions, lagna):
    return JaiminiEngine(positions, lagna).analyze_all()
