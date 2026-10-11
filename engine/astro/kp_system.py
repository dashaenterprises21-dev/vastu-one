"""
VASTU ONE — KP System Engine
Sub-lord, Sub-sub-lord, Ruling Planets, Significators
"""

from typing import Dict, List, Any


class KPSystem:
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]

    # KP Nakshatra lords
    NAKSHATRA_LORDS = [
        "Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru",
        "Shani","Budh","Ketu","Shukra","Surya","Chandra","Mangal",
        "Rahu","Guru","Shani","Budh","Ketu","Shukra","Surya",
        "Chandra","Mangal","Rahu","Guru","Shani","Budh"
    ]

    NAKSHATRAS = ["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा","पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाती","विशाखा","अनुराधा","ज्येष्ठा","मूल","पूर्वाषाढा","उत्तराषाढा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"]

    # Vimshottari years for dasha
    DASHA_YEARS = {"Ketu":7,"Shukra":20,"Surya":6,"Chandra":10,"Mangal":7,"Rahu":18,"Guru":16,"Shani":19,"Budh":17}

    # KP Sub-lord calculation: each nakshatra = 13°20' = 800 min; each sub = 800/9
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict[str, Any]:
        return {
            "planets_kp": self._planet_kp(),
            "cusps_kp": self._cusps_kp(),
            "significators": self._significators(),
            "ruling_planets": self._ruling_planets(),
        }

    def _longitude_to_kp(self, lon: float) -> Dict:
        """Convert longitude to KP Nakshatra, Sub, Sub-sub"""
        nak_num = int(lon / (360/27)) % 27
        nak_lord = self.NAKSHATRA_LORDS[nak_num]

        # Within nakshatra
        nak_start = nak_num * (360/27)
        pos_in_nak = (lon - nak_start) / (360/27)  # 0 to 1

        # Sub lord — divide nakshatra into 9 parts based on Vimshottari
        sub_lord = self._get_sub_lord(nak_lord, pos_in_nak)

        return {
            "nakshatra": self.NAKSHATRAS[nak_num],
            "nakshatra_lord": self.PLANETS_HINDI.get(nak_lord, nak_lord),
            "sub_lord": self.PLANETS_HINDI.get(sub_lord, sub_lord),
            "sub_lord_en": sub_lord,
        }

    def _get_sub_lord(self, nak_lord: str, fraction: float) -> str:
        """Determine sub-lord based on Vimshottari sequence"""
        order = ["Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budh"]
        total_years = sum(self.DASHA_YEARS.values())  # 120
        start_idx = order.index(nak_lord)
        cumulative = 0
        for i in range(9):
            planet = order[(start_idx + i) % 9]
            years = self.DASHA_YEARS[planet]
            portion = years / total_years
            if cumulative <= fraction < cumulative + portion:
                return planet
            cumulative += portion
        return nak_lord

    def _planet_kp(self) -> List[Dict]:
        result = []
        for p, pd in self.pos.items():
            if p in ["Rahu","Ketu"]:
                # Rahu/Ketu use reverse longitude
                lon = pd.get("longitude", 0)
            else:
                lon = pd.get("longitude", 0)
            kp = self._longitude_to_kp(lon)
            result.append({
                "planet": self.PLANETS_HINDI.get(p, p),
                "planet_en": p,
                "longitude": round(lon, 4),
                "rashi": pd.get("rashi_hindi", ""),
                "bhava": pd.get("bhav", ""),
                "nakshatra": kp["nakshatra"],
                "nakshatra_lord": kp["nakshatra_lord"],
                "sub_lord": kp["sub_lord"],
                "sub_lord_en": kp["sub_lord_en"],
            })
        return result

    def _cusps_kp(self) -> List[Dict]:
        result = []
        for i in range(1, 13):
            cusp_lon = i * 30  # Approx; real cusps from Placidus
            kp = self._longitude_to_kp(cusp_lon)
            result.append({
                "house": i,
                "cusp_longitude": cusp_lon,
                "sign_lord": "",
                "star_lord": kp["nakshatra_lord"],
                "sub_lord": kp["sub_lord"],
            })
        return result

    def _significators(self) -> Dict:
        """Planets signifying each house"""
        sigs = {}
        for b in range(1, 13):
            sigs[b] = {
                "occupants": [self.PLANETS_HINDI.get(p, p) for p, pd in self.pos.items() if pd.get("bhav") == b],
                "aspects": [],
            }
        return sigs

    def _ruling_planets(self) -> Dict:
        """Ruling planets for horary"""
        day_lord = "Surya"
        chandra = self.pos.get("Chandra", {})
        chandra_nak = chandra.get("nakshatra", "")
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")

        return {
            "day_lord": self.PLANETS_HINDI.get(day_lord, day_lord),
            "moon_sign_lord": self.PLANETS_HINDI.get(self._sign_lord(self.pos.get("Chandra", {}).get("rashi")), ""),
            "moon_star_lord": "",
            "lagna_sign_lord": self.PLANETS_HINDI.get(self._sign_lord(lagna_rashi), ""),
            "lagna_star_lord": self.lagna.get("lagna_nakshatra", ""),
        }

    def _sign_lord(self, rashi: str) -> str:
        lords = {"Mesh":"Mangal","Vrishabh":"Shukra","Mithun":"Budh","Kark":"Chandra","Simha":"Surya","Kanya":"Budh","Tula":"Shukra","Vrishchik":"Mangal","Dhanu":"Guru","Makar":"Shani","Kumbh":"Shani","Meen":"Guru"}
        return lords.get(rashi, "")


def analyze_kp_system(positions, lagna):
    return KPSystem(positions, lagna).analyze_all()
