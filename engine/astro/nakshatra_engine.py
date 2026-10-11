"""
VASTU ONE — Nakshatra Report Engine
27 Nakshatras full details — devta, gana, yoni, nadi, varna
"""

from typing import Dict, List


class NakshatraEngine:
    NAKSHATRAS = [
        {"name":"अश्विनी","english":"Ashwini","lord":"Ketu","devta":"अश्विनी कुमार","gana":"देव","yoni":"अश्व","nadi":"आदि","varna":"वैश्य","element":"पृथ्वी","nature":"क्षिप्र"},
        {"name":"भरणी","english":"Bharani","lord":"Shukra","devta":"यम","gana":"मनुष्य","yoni":"गज","nadi":"मध्य","varna":"म्लेच्छ","element":"पृथ्वी","nature":"उग्र"},
        {"name":"कृत्तिका","english":"Krittika","lord":"Surya","devta":"अग्नि","gana":"राक्षस","yoni":"मेष","nadi":"अन्त्य","varna":"ब्राह्मण","element":"अग्नि","nature":"मिश्र"},
        {"name":"रोहिणी","english":"Rohini","lord":"Chandra","devta":"ब्रह्मा","gana":"मनुष्य","yoni":"सर्प","nadi":"अन्त्य","varna":"वैश्य","element":"पृथ्वी","nature":"स्थिर"},
        {"name":"मृगशिरा","english":"Mrigashira","lord":"Mangal","devta":"चंद्र","gana":"देव","yoni":"सर्प","nadi":"मध्य","varna":"कृषक","element":"पृथ्वी","nature":"मृदु"},
        {"name":"आर्द्रा","english":"Ardra","lord":"Rahu","devta":"रुद्र","gana":"मनुष्य","yoni":"श्वान","nadi":"आदि","varna":"हंस","element":"जल","nature":"तीक्ष्ण"},
        {"name":"पुनर्वसु","english":"Punarvasu","lord":"Guru","devta":"अदिति","gana":"देव","yoni":"मार्जार","nadi":"आदि","varna":"ब्राह्मण","element":"वायु","nature":"चर"},
        {"name":"पुष्य","english":"Pushya","lord":"Shani","devta":"बृहस्पति","gana":"देव","yoni":"मेष","nadi":"मध्य","varna":"क्षत्रिय","element":"जल","nature":"लघु"},
        {"name":"आश्लेषा","english":"Ashlesha","lord":"Budh","devta":"सर्प","gana":"राक्षस","yoni":"मार्जार","nadi":"अन्त्य","varna":"म्लेच्छ","element":"जल","nature":"तीक्ष्ण"},
        {"name":"मघा","english":"Magha","lord":"Ketu","devta":"पितृ","gana":"राक्षस","yoni":"मूषक","nadi":"अन्त्य","varna":"क्षत्रिय","element":"पृथ्वी","nature":"उग्र"},
        {"name":"पूर्वा फाल्गुनी","english":"Purva Phalguni","lord":"Shukra","devta":"भग","gana":"मनुष्य","yoni":"मूषक","nadi":"मध्य","varna":"ब्राह्मण","element":"पृथ्वी","nature":"उग्र"},
        {"name":"उत्तरा फाल्गुनी","english":"Uttara Phalguni","lord":"Surya","devta":"अर्यमा","gana":"मनुष्य","yoni":"गौ","nadi":"अन्त्य","varna":"क्षत्रिय","element":"पृथ्वी","nature":"स्थिर"},
        {"name":"हस्त","english":"Hasta","lord":"Chandra","devta":"सविता","gana":"देव","yoni":"महिष","nadi":"आदि","varna":"वैश्य","element":"पृथ्वी","nature":"लघु"},
        {"name":"चित्रा","english":"Chitra","lord":"Mangal","devta":"त्वष्टा","gana":"राक्षस","yoni":"व्याघ्र","nadi":"मध्य","varna":"कृषक","element":"जल","nature":"मृदु"},
        {"name":"स्वाती","english":"Swati","lord":"Rahu","devta":"वायु","gana":"देव","yoni":"महिष","nadi":"अन्त्य","varna":"म्लेच्छ","element":"वायु","nature":"चर"},
        {"name":"विशाखा","english":"Vishakha","lord":"Guru","devta":"इन्द्राग्नि","gana":"राक्षस","yoni":"व्याघ्र","nadi":"अन्त्य","varna":"म्लेच्छ","element":"जल","nature":"मिश्र"},
        {"name":"अनुराधा","english":"Anuradha","lord":"Shani","devta":"मित्र","gana":"देव","yoni":"मृग","nadi":"आदि","varna":"वैश्य","element":"जल","nature":"मृदु"},
        {"name":"ज्येष्ठा","english":"Jyeshtha","lord":"Budh","devta":"इन्द्र","gana":"राक्षस","yoni":"मृग","nadi":"मध्य","varna":"कृषक","element":"जल","nature":"तीक्ष्ण"},
        {"name":"मूल","english":"Mula","lord":"Ketu","devta":"निरृति","gana":"राक्षस","yoni":"श्वान","nadi":"अन्त्य","varna":"कृषक","element":"जल","nature":"तीक्ष्ण"},
        {"name":"पूर्वाषाढा","english":"Purva Ashadha","lord":"Shukra","devta":"आप","gana":"मनुष्य","yoni":"वानर","nadi":"अन्त्य","varna":"ब्राह्मण","element":"जल","nature":"उग्र"},
        {"name":"उत्तराषाढा","english":"Uttara Ashadha","lord":"Surya","devta":"विश्वेदेव","gana":"मनुष्य","yoni":"नकुल","nadi":"आदि","varna":"क्षत्रिय","element":"वायु","nature":"स्थिर"},
        {"name":"श्रवण","english":"Shravana","lord":"Chandra","devta":"विष्णु","gana":"देव","yoni":"वानर","nadi":"अन्त्य","varna":"म्लेच्छ","element":"वायु","nature":"चर"},
        {"name":"धनिष्ठा","english":"Dhanishtha","lord":"Mangal","devta":"वसु","gana":"राक्षस","yoni":"सिंह","nadi":"मध्य","varna":"कृषक","element":"वायु","nature":"चर"},
        {"name":"शतभिषा","english":"Shatabhisha","lord":"Rahu","devta":"वरुण","gana":"राक्षस","yoni":"अश्व","nadi":"आदि","varna":"हंस","element":"वायु","nature":"चर"},
        {"name":"पूर्वा भाद्रपद","english":"Purva Bhadrapada","lord":"Guru","devta":"अजैकपाद","gana":"मनुष्य","yoni":"सिंह","nadi":"आदि","varna":"ब्राह्मण","element":"वायु","nature":"उग्र"},
        {"name":"उत्तरा भाद्रपद","english":"Uttara Bhadrapada","lord":"Shani","devta":"अहिर्बुध्न्य","gana":"मनुष्य","yoni":"गौ","nadi":"मध्य","varna":"क्षत्रिय","element":"वायु","nature":"स्थिर"},
        {"name":"रेवती","english":"Revati","lord":"Budh","devta":"पूषन","gana":"देव","yoni":"गज","nadi":"अन्त्य","varna":"हंस","element":"जल","nature":"मृदु"},
    ]

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict:
        return {
            "birth_nakshatra": self._birth_nakshatra(),
            "moon_nakshatra": self._planet_nakshatra("Chandra"),
            "all_planets": self._all_nakshatras(),
        }

    def _birth_nakshatra(self) -> Dict:
        # From lagna nakshatra
        lagna_nak = self.lagna.get("lagna_nakshatra", "")
        for n in self.NAKSHATRAS:
            if n["english"] == lagna_nak or n["name"] == lagna_nak:
                return n
        # Fallback: Chandra nakshatra
        ch = self.pos.get("Chandra", {})
        ch_nak = ch.get("nakshatra", "")
        for n in self.NAKSHATRAS:
            if n["english"] == ch_nak or n["name"] == ch_nak:
                return n
        return self.NAKSHATRAS[0]

    def _planet_nakshatra(self, planet: str) -> Dict:
        pd = self.pos.get(planet, {})
        nak = pd.get("nakshatra", "")
        for n in self.NAKSHATRAS:
            if n["english"] == nak or n["name"] == nak:
                return n
        return {}

    def _all_nakshatras(self) -> List[Dict]:
        return [self.NAKSHATRAS[i] for i in range(27)]


def analyze_nakshatra(positions, lagna):
    return NakshatraEngine(positions, lagna).analyze_all()
