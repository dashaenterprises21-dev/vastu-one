"""
VASTU ONE — Nakshatra Nadi Engine
Detailed 27 Nakshatras with Nadi coordinates
"""

from typing import Dict, List, Any


class NakshatraNadiEngine:
    NAKSHATRAS = [
        {"name":"अश्विनी","english":"Ashwini","lord":"Ketu","devta":"अश्विनी कुमार","gana":"देव","yoni":"अश्व","nadi":"आदि","varna":"वैश्य","vashya":"चतुष्पद","tara":1,"bhakoot":1,"pada":"चू-चे-चो-ला","element":"पृथ्वी"},
        {"name":"भरणी","english":"Bharani","lord":"Shukra","devta":"यम","gana":"मनुष्य","yoni":"गज","nadi":"मध्य","varna":"म्लेच्छ","vashya":"चतुष्पद","tara":2,"bhakoot":2,"pada":"ली-लू-ले-लो","element":"पृथ्वी"},
        {"name":"कृत्तिका","english":"Krittika","lord":"Surya","devta":"अग्नि","gana":"राक्षस","yoni":"मेष","nadi":"अन्त्य","varna":"ब्राह्मण","vashya":"चतुष्पद","tara":3,"bhakoot":3,"pada":"अ-ई-उ-ए","element":"अग्नि"},
        {"name":"रोहिणी","english":"Rohini","lord":"Chandra","devta":"ब्रह्मा","gana":"मनुष्य","yoni":"सर्प","nadi":"अन्त्य","varna":"वैश्य","vashya":"चतुष्पद","tara":4,"bhakoot":4,"pada":"ओ-वा-वी-वू","element":"पृथ्वी"},
        {"name":"मृगशिरा","english":"Mrigashira","lord":"Mangal","devta":"चंद्र","gana":"देव","yoni":"सर्प","nadi":"मध्य","varna":"कृषक","vashya":"चतुष्पद","tara":5,"bhakoot":5,"pada":"वे-वो-का-की","element":"पृथ्वी"},
        {"name":"आर्द्रा","english":"Ardra","lord":"Rahu","devta":"रुद्र","gana":"मनुष्य","yoni":"श्वान","nadi":"आदि","varna":"हंस","vashya":"मनुष्य","tara":6,"bhakoot":6,"pada":"कू-घ-ङ-छ","element":"जल"},
        {"name":"पुनर्वसु","english":"Punarvasu","lord":"Guru","devta":"अदिति","gana":"देव","yoni":"मार्जार","nadi":"आदि","varna":"ब्राह्मण","vashya":"मनुष्य","tara":7,"bhakoot":7,"pada":"के-को-हा-ही","element":"वायु"},
        {"name":"पुष्य","english":"Pushya","lord":"Shani","devta":"बृहस्पति","gana":"देव","yoni":"मेष","nadi":"मध्य","varna":"क्षत्रिय","vashya":"मनुष्य","tara":8,"bhakoot":8,"pada":"हू-हे-हो-डा","element":"जल"},
        {"name":"आश्लेषा","english":"Ashlesha","lord":"Budh","devta":"सर्प","gana":"राक्षस","yoni":"मार्जार","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"कीट","tara":9,"bhakoot":9,"pada":"डी-डू-डे-डो","element":"जल"},
        {"name":"मघा","english":"Magha","lord":"Ketu","devta":"पितृ","gana":"राक्षस","yoni":"मूषक","nadi":"अन्त्य","varna":"क्षत्रिय","vashya":"कीट","tara":10,"bhakoot":10,"pada":"मा-मी-मू-मे","element":"पृथ्वी"},
        {"name":"पूर्वा फाल्गुनी","english":"Purva Phalguni","lord":"Shukra","devta":"भग","gana":"मनुष्य","yoni":"मूषक","nadi":"मध्य","varna":"ब्राह्मण","vashya":"मनुष्य","tara":11,"bhakoot":11,"pada":"मो-टा-टी-टू","element":"पृथ्वी"},
        {"name":"उत्तरा फाल्गुनी","english":"Uttara Phalguni","lord":"Surya","devta":"अर्यमा","gana":"मनुष्य","yoni":"गौ","nadi":"अन्त्य","varna":"क्षत्रिय","vashya":"मनुष्य","tara":12,"bhakoot":12,"pada":"टे-टो-पा-पी","element":"पृथ्वी"},
        {"name":"हस्त","english":"Hasta","lord":"Chandra","devta":"सविता","gana":"देव","yoni":"महिष","nadi":"आदि","varna":"वैश्य","vashya":"मनुष्य","tara":13,"bhakoot":1,"pada":"पू-ष-ण-ठ","element":"पृथ्वी"},
        {"name":"चित्रा","english":"Chitra","lord":"Mangal","devta":"त्वष्टा","gana":"राक्षस","yoni":"व्याघ्र","nadi":"मध्य","varna":"कृषक","vashya":"कीट","tara":14,"bhakoot":2,"pada":"पे-पो-रा-री","element":"जल"},
        {"name":"स्वाती","english":"Swati","lord":"Rahu","devta":"वायु","gana":"देव","yoni":"महिष","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"मनुष्य","tara":15,"bhakoot":3,"pada":"रू-रे-रो-ता","element":"वायु"},
        {"name":"विशाखा","english":"Vishakha","lord":"Guru","devta":"इन्द्राग्नि","gana":"राक्षस","yoni":"व्याघ्र","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"मनुष्य","tara":16,"bhakoot":4,"pada":"ती-तू-ते-तो","element":"जल"},
        {"name":"अनुराधा","english":"Anuradha","lord":"Shani","devta":"मित्र","gana":"देव","yoni":"मृग","nadi":"आदि","varna":"वैश्य","vashya":"मनुष्य","tara":17,"bhakoot":5,"pada":"ना-नी-नू-ने","element":"जल"},
        {"name":"ज्येष्ठा","english":"Jyeshtha","lord":"Budh","devta":"इन्द्र","gana":"राक्षस","yoni":"मृग","nadi":"मध्य","varna":"कृषक","vashya":"मनुष्य","tara":18,"bhakoot":6,"pada":"नो-या-यी-यू","element":"जल"},
        {"name":"मूल","english":"Mula","lord":"Ketu","devta":"निरृति","gana":"राक्षस","yoni":"श्वान","nadi":"अन्त्य","varna":"कृषक","vashya":"मनुष्य","tara":19,"bhakoot":7,"pada":"ये-यो-भा-भी","element":"जल"},
        {"name":"पूर्वाषाढा","english":"Purva Ashadha","lord":"Shukra","devta":"आप","gana":"मनुष्य","yoni":"वानर","nadi":"अन्त्य","varna":"ब्राह्मण","vashya":"मनुष्य","tara":20,"bhakoot":8,"pada":"भू-धा-फा-ढा","element":"जल"},
        {"name":"उत्तराषाढा","english":"Uttara Ashadha","lord":"Surya","devta":"विश्वेदेव","gana":"मनुष्य","yoni":"नकुल","nadi":"आदि","varna":"क्षत्रिय","vashya":"मनुष्य","tara":21,"bhakoot":9,"pada":"भे-भो-जा-जी","element":"वायु"},
        {"name":"श्रवण","english":"Shravana","lord":"Chandra","devta":"विष्णु","gana":"देव","yoni":"वानर","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"मनुष्य","tara":22,"bhakoot":10,"pada":"खी-खू-खे-खो","element":"वायु"},
        {"name":"धनिष्ठा","english":"Dhanishtha","lord":"Mangal","devta":"वसु","gana":"राक्षस","yoni":"सिंह","nadi":"मध्य","varna":"कृषक","vashya":"चतुष्पद","tara":23,"bhakoot":11,"pada":"गा-गी-गू-गे","element":"वायु"},
        {"name":"शतभिषा","english":"Shatabhisha","lord":"Rahu","devta":"वरुण","gana":"राक्षस","yoni":"अश्व","nadi":"आदि","varna":"हंस","vashya":"चतुष्पद","tara":24,"bhakoot":12,"pada":"गो-सा-सी-सू","element":"वायु"},
        {"name":"पूर्वा भाद्रपद","english":"Purva Bhadrapada","lord":"Guru","devta":"अजैकपाद","gana":"मनुष्य","yoni":"सिंह","nadi":"आदि","varna":"ब्राह्मण","vashya":"चतुष्पद","tara":25,"bhakoot":1,"pada":"से-सो-दा-दी","element":"वायु"},
        {"name":"उत्तरा भाद्रपद","english":"Uttara Bhadrapada","lord":"Shani","devta":"अहिर्बुध्न्य","gana":"मनुष्य","yoni":"गौ","nadi":"मध्य","varna":"क्षत्रिय","vashya":"मनुष्य","tara":26,"bhakoot":2,"pada":"दू-थ-झ-ञ","element":"वायु"},
        {"name":"रेवती","english":"Revati","lord":"Budh","devta":"पूषन","gana":"देव","yoni":"गज","nadi":"अन्त्य","varna":"हंस","vashya":"मनुष्य","tara":27,"bhakoot":3,"pada":"दे-दो-चा-ची","element":"जल"},
    ]

    def __init__(self, positions: Dict):
        self.pos = positions

    def analyze_all(self) -> Dict:
        planets_data = {}
        for planet, pd in self.pos.items():
            nak_name = pd.get("nakshatra", "")
            pada = pd.get("pada", 1)
            nak_info = self._find_nakshatra(nak_name)
            planets_data[planet] = {
                "planet": planet,
                "hindi": pd.get("hindi", ""),
                "nakshatra": nak_info["name"],
                "nakshatra_english": nak_info["english"],
                "pada": pada,
                "pada_syllable": nak_info["pada"].split("-")[pada - 1] if pada and 1 <= pada <= 4 else "",
                "lord": nak_info["lord"],
                "devta": nak_info["devta"],
                "gana": nak_info["gana"],
                "yoni": nak_info["yoni"],
                "nadi": nak_info["nadi"],
                "varna": nak_info["varna"],
                "element": nak_info["element"],
            }
        return {
            "planets": planets_data,
            "all_nakshatras": self.NAKSHATRAS,
        }

    def _find_nakshatra(self, name: str) -> Dict:
        if not name:
            return self.NAKSHATRAS[0]
        for n in self.NAKSHATRAS:
            if n["name"] == name or n["english"].lower() == name.lower():
                return n
        return self.NAKSHATRAS[0]


def analyze_nakshatra_nadi(positions):
    return NakshatraNadiEngine(positions).analyze_all()
