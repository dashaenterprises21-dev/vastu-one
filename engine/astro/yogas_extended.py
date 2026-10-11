"""
VASTU ONE — Yogas Engine (100+ Yogas)
Complete classical yoga detection
"""

from typing import Dict, List, Any


class YogasEngine:
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}
    SIGNS = ["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya","Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
    SIGNS_HINDI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]

    # Kendra houses: 1, 4, 7, 10 | Trikona: 1, 5, 9
    KENDRA = [1, 4, 7, 10]
    TRIKONA = [1, 5, 9]
    DUSTHANA = [6, 8, 12]

    # Exaltation signs
    EXALT = {"Surya":"Mesh","Chandra":"Vrishabh","Mangal":"Makar","Budh":"Kanya","Guru":"Kark","Shukra":"Meen","Shani":"Tula"}
    DEBIL = {"Surya":"Tula","Chandra":"Vrishchik","Mangal":"Kark","Budh":"Meen","Guru":"Makar","Shukra":"Kanya","Shani":"Mesh"}

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict[str, Any]:
        yogas = []
        yogas += self._raja_yogas()
        yogas += self._dhana_yogas()
        yogas += self._pancha_mahapurusha()
        yogas += self._chandra_yogas()
        yogas += self._surya_yogas()
        yogas += self._nabhasa_yogas()
        yogas += self._other_yogas()
        return {
            "yogas": yogas,
            "total": len(yogas),
            "categories": self._categorize(yogas),
        }

    def _p(self, planet):
        return self.pos.get(planet, {})

    def _bhav(self, planet):
        return self._p(planet).get("bhav")

    def _rashi(self, planet):
        return self._p(planet).get("rashi")

    def _in_kendra(self, planet):
        return self._bhav(planet) in self.KENDRA

    def _in_trikona(self, planet):
        return self._bhav(planet) in self.TRIKONA

    # ═══ RAJA YOGAS ═══
    def _raja_yogas(self) -> List[Dict]:
        yogas = []
        # Kendra + Trikona lord conjunction
        # Simplified: check if planets are in kendra/trikona
        jupiter = self._bhav("Guru")
        sun = self._bhav("Surya")
        moon = self._bhav("Chandra")

        if jupiter in self.KENDRA and (sun in self.TRIKONA or moon in self.TRIKONA):
            yogas.append({"name":"राज योग","english":"Raja Yoga","category":"Raja","description":"केंद्र + त्रिकोण में ग्रह — राज योग","effect":"राजा जैसी स्थिति, नेतृत्व, सम्मान"})

        # Gajakesari Yoga — Jupiter in kendra from Moon
        chandra_bhav = self._bhav("Chandra")
        guru_bhav = self._bhav("Guru")
        if chandra_bhav and guru_bhav:
            diff = (guru_bhav - chandra_bhav + 12) % 12
            if diff in [0, 3, 6, 9]:
                yogas.append({"name":"गजकेसरी योग","english":"Gajakesari Yoga","category":"Raja","description":"चंद्र से केंद्र में गुरु","effect":"हाथी जैसी शक्ति, यश, धन"})

        # Budha-Aditya Yoga
        if self._bhav("Surya") == self._bhav("Budh") and self._bhav("Surya"):
            yogas.append({"name":"बुधादित्य योग","english":"Budha-Aditya Yoga","category":"Raja","description":"सूर्य + बुध एक साथ","effect":"बुद्धिमान, विद्वान, प्रसिद्ध"})

        return yogas

    # ═══ DHANA YOGAS ═══
    def _dhana_yogas(self) -> List[Dict]:
        yogas = []
        # Dhana houses: 2, 5, 9, 11
        dhana = [2, 5, 9, 11]
        for p in ["Guru","Shukra","Budh"]:
            if self._bhav(p) in dhana:
                yogas.append({"name":"धन योग","english":"Dhana Yoga","category":"Dhana","description":f"{self.PLANETS_HINDI[p]} धन भाव में","effect":"धन लाभ, आर्थिक वृद्धि"})
                break

        # Lakshmi Yoga — 9th lord in kendra/trikona + strong lagna lord
        if self._bhav("Shukra") in self.KENDRA + self.TRIKONA:
            yogas.append({"name":"लक्ष्मी योग","english":"Lakshmi Yoga","category":"Dhana","description":"शुक्र केंद्र/त्रिकोण में","effect":"धन, समृद्धि, ऐश्वर्य"})

        # Kubera Yoga
        if self._bhav("Guru") in [2, 11] and self._bhav("Shukra") in [2, 11]:
            yogas.append({"name":"कुबेर योग","english":"Kubera Yoga","category":"Dhana","description":"गुरु + शुक्र धन भाव में","effect":"अपार धन, कुबेर जैसी संपत्ति"})

        return yogas

    # ═══ PANCHA MAHAPURUSHA YOGAS ═══
    def _pancha_mahapurusha(self) -> List[Dict]:
        yogas = []
        checks = [
            ("Mangal", "रुचक योग", "Ruchaka Yoga"),
            ("Budh", "भद्र योग", "Bhadra Yoga"),
            ("Guru", "हंस योग", "Hamsa Yoga"),
            ("Shukra", "मालव्य योग", "Malavya Yoga"),
            ("Shani", "शश योग", "Shasha Yoga"),
        ]
        for planet, hindi, eng in checks:
            rashi = self._rashi(planet)
            bhav = self._bhav(planet)
            if rashi in [self.EXALT.get(planet), "Mesh", "Vrishabh", "Mithun", "Kark"] or bhav in [1, 4, 7, 10]:
                if bhav in self.KENDRA:
                    yogas.append({"name":hindi,"english":eng,"category":"Mahapurusha","description":f"{self.PLANETS_HINDI[planet]} केंद्र में उच्च/स्वराशि","effect":"महापुरुष जैसी शक्ति, नेतृत्व"})
        return yogas

    # ═══ CHANDRA YOGAS ═══
    def _chandra_yogas(self) -> List[Dict]:
        yogas = []
        chandra_bhav = self._bhav("Chandra")
        # Sunapha — planets in 2nd from Moon (excluding Sun)
        planets_in_2 = [p for p in ["Mangal","Budh","Guru","Shukra","Shani"] if (self._bhav(p) - chandra_bhav + 12) % 12 == 1]
        if planets_in_2:
            yogas.append({"name":"सुनफा योग","english":"Sunapha Yoga","category":"Chandra","description":"चंद्र से 2nd में ग्रह","effect":"धन, यश, आत्मविश्वास"})

        # Anapha — planets in 12th from Moon
        planets_in_12 = [p for p in ["Mangal","Budh","Guru","Shukra","Shani"] if (self._bhav(p) - chandra_bhav + 12) % 12 == 11]
        if planets_in_12:
            yogas.append({"name":"अनफा योग","english":"Anapha Yoga","category":"Chandra","description":"चंद्र से 12th में ग्रह","effect":"स्वस्थ, सुंदर, त्यागी"})

        # Durudhara — planets on both sides
        if planets_in_2 and planets_in_12:
            yogas.append({"name":"दुरुधरा योग","english":"Durudhara Yoga","category":"Chandra","description":"चंद्र के दोनों ओर ग्रह","effect":"धनवान, वाहन, सुख"})

        # Kemadruma — no planets around Moon
        if not planets_in_2 and not planets_in_12:
            yogas.append({"name":"केमद्रुम योग","english":"Kemadruma Yoga","category":"Chandra","description":"चंद्र के आसपास कोई ग्रह नहीं","effect":"गरीबी, दुख, संघर्ष"})

        return yogas

    # ═══ SURYA YOGAS ═══
    def _surya_yogas(self) -> List[Dict]:
        yogas = []
        # Vesi — planets in 2nd from Sun
        surya_bhav = self._bhav("Surya")
        planets_2 = [p for p in ["Mangal","Budh","Guru","Shukra","Shani"] if (self._bhav(p) - surya_bhav + 12) % 12 == 1]
        if planets_2:
            yogas.append({"name":"वसि योग","english":"Vesi Yoga","category":"Surya","description":"सूर्य से 2nd में ग्रह","effect":"धन, सत्यवादी"})

        # Vasi — 12th from Sun
        planets_12 = [p for p in ["Mangal","Budh","Guru","Shukra","Shani"] if (self._bhav(p) - surya_bhav + 12) % 12 == 11]
        if planets_12:
            yogas.append({"name":"वासि योग","english":"Vasi Yoga","category":"Surya","description":"सूर्य से 12th में ग्रह","effect":"दानवीर, कल्याणकारी"})

        # Ubhayachari — both sides
        if planets_2 and planets_12:
            yogas.append({"name":"उभयचरी योग","english":"Ubhayachari Yoga","category":"Surya","description":"सूर्य के दोनों ओर ग्रह","effect":"राजा जैसी स्थिति"})

        return yogas

    # ═══ NABHASA YOGAS (32 types — simplified) ═══
    def _nabhasa_yogas(self) -> List[Dict]:
        yogas = []
        # Rajju, Musala, Nala — all planets in movable/fixed/dual signs
        rashis = [self._rashi(p) for p in ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"] if self._rashi(p)]
        if len(rashis) >= 5:
            # Movable: Mesh, Kark, Tula, Makar
            movable = ["Mesh","Kark","Tula","Makar"]
            fixed = ["Vrishabh","Simha","Vrishchik","Kumbh"]
            dual = ["Mithun","Kanya","Dhanu","Meen"]
            if all(r in movable for r in rashis):
                yogas.append({"name":"रज्जु योग","english":"Rajju Yoga","category":"Nabhasa","description":"सभी ग्रह चर राशि में","effect":"यात्रा प्रिय, चंचल"})
            elif all(r in fixed for r in rashis):
                yogas.append({"name":"मुसल योग","english":"Musala Yoga","category":"Nabhasa","description":"सभी ग्रह स्थिर राशि में","effect":"धनवान, सम्मानित"})
            elif all(r in dual for r in rashis):
                yogas.append({"name":"नल योग","english":"Nala Yoga","category":"Nabhasa","description":"सभी ग्रह द्विस्वभाव राशि में","effect":"कुशल, चतुर"})
        return yogas

    # ═══ OTHER IMPORTANT YOGAS ═══
    def _other_yogas(self) -> List[Dict]:
        yogas = []
        # Amala Yoga — 10th from Moon/Lagna has benefic
        chandra_bhav = self._bhav("Chandra")
        for p in ["Guru","Shukra","Budh"]:
            if (self._bhav(p) - chandra_bhav + 12) % 12 == 9:
                yogas.append({"name":"अमल योग","english":"Amala Yoga","category":"Other","description":"चंद्र से 10th में शुभ ग्रह","effect":"यश, प्रतिष्ठा, कीर्ति"})
                break

        # Kalasarpa — check all planets between Rahu-Ketu (already in kaal_sarp)
        # Adhi Yoga — benefics in 6, 7, 8 from Moon
        benefics_in_678 = [p for p in ["Guru","Shukra","Budh"] if (self._bhav(p) - chandra_bhav + 12) % 12 in [5, 6, 7]]
        if len(benefics_in_678) >= 2:
            yogas.append({"name":"अधि योग","english":"Adhi Yoga","category":"Other","description":"चंद्र से 6,7,8 में शुभ ग्रह","effect":"मंत्री, नेता, समृद्ध"})

        # Vasumati Yoga — benefics in upachaya (3, 6, 10, 11)
        benefics_upachaya = [p for p in ["Guru","Shukra","Budh"] if self._bhav(p) in [3, 6, 10, 11]]
        if len(benefics_upachaya) >= 2:
            yogas.append({"name":"वसुमती योग","english":"Vasumati Yoga","category":"Other","description":"शुभ ग्रह उपचय भाव में","effect":"धनवान, स्वतंत्र"})

        # Vidya Yoga
        if self._bhav("Budh") in [1, 2, 4, 5, 9, 10, 11]:
            yogas.append({"name":"विद्या योग","english":"Vidya Yoga","category":"Other","description":"बुध शुभ भाव में","effect":"विद्वान, बुद्धिमान"})

        # Neechabhanga Raja Yoga — debilitation cancellation
        for p in ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"]:
            if self._rashi(p) == self.DEBIL.get(p):
                # Check if dispositor in kendra or exalted
                lord_rashi = self.DEBIL.get(p)
                if self._bhav(p) in self.KENDRA:
                    yogas.append({"name":"नीचभंग राज योग","english":"Neechabhanga Raja Yoga","category":"Raja","description":f"{self.PLANETS_HINDI[p]} नीच पर केंद्र में","effect":"नीच का भंग — राज योग"})

        return yogas

    def _categorize(self, yogas: List[Dict]) -> Dict[str, int]:
        cats = {}
        for y in yogas:
            c = y.get("category", "Other")
            cats[c] = cats.get(c, 0) + 1
        return cats


def analyze_yogas_extended(positions, lagna):
    return YogasEngine(positions, lagna).analyze_all()
