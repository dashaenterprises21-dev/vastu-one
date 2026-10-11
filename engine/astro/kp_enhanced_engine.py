"""
VASTU ONE — KP System Enhanced
Sub-Sub Lord, Ruling Planets, Significators, Cuspal Analysis
"""

from typing import Dict, List, Any
from datetime import datetime


class KPEnhancedEngine:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    NAKSHATRA_LORDS = [
        "Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru",
        "Shani","Budh","Ketu","Shukra","Surya","Chandra","Mangal",
        "Rahu","Guru","Shani","Budh","Ketu","Shukra","Surya",
        "Chandra","Mangal","Rahu","Guru","Shani","Budh"
    ]

    NAKSHATRAS = ["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा","पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाती","विशाखा","अनुराधा","ज्येष्ठा","मूल","पूर्वाषाढा","उत्तराषाढा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"]

    DASHA_YEARS = {"Ketu":7,"Shukra":20,"Surya":6,"Chandra":10,"Mangal":7,"Rahu":18,"Guru":16,"Shani":19,"Budh":17}

    def __init__(self, positions: Dict, lagna: Dict, basic: Dict):
        self.pos = positions
        self.lagna = lagna
        self.basic = basic

    def analyze_all(self) -> Dict:
        return {
            "sub_sub_analysis": self._sub_sub_analysis(),
            "ruling_planets": self._ruling_planets(),
            "significators": self._significators(),
            "cuspal_analysis": self._cuspal_analysis(),
        }

    def _longitude_to_full_kp(self, lon: float) -> Dict:
        """Complete KP: Sign, Nakshatra, Sub, Sub-Sub"""
        # Sign
        sign_idx = int(lon / 30) % 12

        # Nakshatra (13°20' each)
        nak_num = int(lon / (360/27)) % 27
        nak_lord = self.NAKSHATRA_LORDS[nak_num]

        # Within nakshatra
        nak_start = nak_num * (360/27)
        pos_in_nak = (lon - nak_start) / (360/27)

        # Sub lord (9 divisions of nakshatra)
        sub_lord = self._get_sub_lord(nak_lord, pos_in_nak)

        # Sub-sub lord (further division)
        sub_start_frac, sub_end_frac = self._get_sub_range(nak_lord, pos_in_nak)
        pos_in_sub = (pos_in_nak - sub_start_frac) / (sub_end_frac - sub_start_frac) if sub_end_frac > sub_start_frac else 0
        sub_sub_lord = self._get_sub_lord(sub_lord, pos_in_sub)

        return {
            "sign": self.SIGNS[sign_idx],
            "sign_hindi": self.SIGNS_HINDI[sign_idx],
            "nakshatra": self.NAKSHATRAS[nak_num],
            "nakshatra_lord": self.PLANETS_HINDI.get(nak_lord, nak_lord),
            "nakshatra_lord_en": nak_lord,
            "sub_lord": self.PLANETS_HINDI.get(sub_lord, sub_lord),
            "sub_lord_en": sub_lord,
            "sub_sub_lord": self.PLANETS_HINDI.get(sub_sub_lord, sub_sub_lord),
            "sub_sub_lord_en": sub_sub_lord,
        }

    def _get_sub_lord(self, lord: str, fraction: float) -> str:
        order = ["Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budh"]
        total = sum(self.DASHA_YEARS.values())
        start_idx = order.index(lord)
        cum = 0
        for i in range(9):
            planet = order[(start_idx + i) % 9]
            portion = self.DASHA_YEARS[planet] / total
            if cum <= fraction < cum + portion:
                return planet
            cum += portion
        return lord

    def _get_sub_range(self, lord: str, fraction: float):
        order = ["Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budh"]
        total = sum(self.DASHA_YEARS.values())
        start_idx = order.index(lord)
        cum = 0
        for i in range(9):
            planet = order[(start_idx + i) % 9]
            portion = self.DASHA_YEARS[planet] / total
            if cum <= fraction < cum + portion:
                return cum, cum + portion
            cum += portion
        return 0, 1

    def _sub_sub_analysis(self) -> List[Dict]:
        result = []
        for planet, pd in self.pos.items():
            lon = pd.get("longitude", 0)
            kp = self._longitude_to_full_kp(lon)
            result.append({
                "planet": planet,
                "hindi": self.PLANETS_HINDI.get(planet, planet),
                "longitude": round(lon, 4),
                "bhava": pd.get("bhav", ""),
                **kp,
            })
        return result

    def _ruling_planets(self) -> Dict:
        """Ruling Planets for horary"""
        now = datetime.now()
        # Day lord (0=Sunday)
        day_lords = ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"]
        day_lord = day_lords[(now.weekday() + 1) % 7]

        # Moon details
        chandra = self.pos.get("Chandra", {})
        moon_sign = chandra.get("rashi", "")
        moon_nak = chandra.get("nakshatra", "")
        moon_nak_lord = self._nakshatra_lord(moon_nak)

        # Lagna details
        lagna_rashi = self.lagna.get("lagna_rashi", "")
        lagna_lord = self._sign_lord(lagna_rashi)
        lagna_nak = self.lagna.get("lagna_nakshatra", "")
        lagna_nak_lord = self._nakshatra_lord(lagna_nak)

        return {
            "day_lord": self.PLANETS_HINDI.get(day_lord, day_lord),
            "moon_sign": self.SIGNS_HINDI[self.SIGNS.index(moon_sign)] if moon_sign in self.SIGNS else "",
            "moon_sign_lord": self.PLANETS_HINDI.get(self._sign_lord(moon_sign), ""),
            "moon_nakshatra": moon_nak,
            "moon_star_lord": self.PLANETS_HINDI.get(moon_nak_lord, moon_nak_lord),
            "lagna_sign": self.SIGNS_HINDI[self.SIGNS.index(lagna_rashi)] if lagna_rashi in self.SIGNS else "",
            "lagna_sign_lord": self.PLANETS_HINDI.get(lagna_lord, lagna_lord),
            "lagna_nakshatra": lagna_nak,
            "lagna_star_lord": self.PLANETS_HINDI.get(lagna_nak_lord, lagna_nak_lord),
        }

    def _significators(self) -> Dict:
        """Planets signifying each house (A-B-C-D method)"""
        sigs = {}
        for b in range(1, 13):
            occupants = []
            aspecting = []
            for p, pd in self.pos.items():
                if pd.get("bhav") == b:
                    occupants.append(self.PLANETS_HINDI.get(p, p))
            sigs[b] = {
                "occupants": occupants,
                "house_lord": "",
                "aspects": aspecting,
            }
        return sigs

    def _cuspal_analysis(self) -> List[Dict]:
        """Analyze 12 cusps"""
        result = []
        for i in range(1, 13):
            cusp_lon = (i - 1) * 30  # Simplified (Placidus in real impl)
            kp = self._longitude_to_full_kp(cusp_lon)
            result.append({
                "cusp": i,
                "longitude": cusp_lon,
                **kp,
            })
        return result

    def _nakshatra_lord(self, nak_name: str) -> str:
        try:
            idx = self.NAKSHATRAS.index(nak_name)
            return self.NAKSHATRA_LORDS[idx]
        except:
            return ""

    def _sign_lord(self, rashi: str) -> str:
        lords = {"Mesh":"Mangal","Vrishabh":"Shukra","Mithun":"Budh","Kark":"Chandra","Simha":"Surya","Kanya":"Budh","Tula":"Shukra","Vrishchik":"Mangal","Dhanu":"Guru","Makar":"Shani","Kumbh":"Shani","Meen":"Guru"}
        return lords.get(rashi, "")


def analyze_kp_enhanced(positions, lagna, basic):
    return KPEnhancedEngine(positions, lagna, basic).analyze_all()
