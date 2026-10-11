"""
VASTU ONE — Ashtakoota Guna Milan Engine
36-point marriage matching
"""

from typing import Dict, List, Any


class AshtakootaEngine:
    NAKSHATRAS = [
        {"name":"अश्विनी","gana":"देव","yoni":"अश्व","nadi":"आदि","varna":"वैश्य","vashya":"चतुष्पद","tara":1,"bhakoot":1},
        {"name":"भरणी","gana":"मनुष्य","yoni":"गज","nadi":"मध्य","varna":"म्लेच्छ","vashya":"चतुष्पद","tara":2,"bhakoot":2},
        {"name":"कृत्तिका","gana":"राक्षस","yoni":"मेष","nadi":"अन्त्य","varna":"ब्राह्मण","vashya":"चतुष्पद","tara":3,"bhakoot":3},
        {"name":"रोहिणी","gana":"मनुष्य","yoni":"सर्प","nadi":"अन्त्य","varna":"वैश्य","vashya":"चतुष्पद","tara":4,"bhakoot":4},
        {"name":"मृगशिरा","gana":"देव","yoni":"सर्प","nadi":"मध्य","varna":"कृषक","vashya":"चतुष्पद","tara":5,"bhakoot":5},
        {"name":"आर्द्रा","gana":"मनुष्य","yoni":"श्वान","nadi":"आदि","varna":"हंस","vashya":"मनुष्य","tara":6,"bhakoot":6},
        {"name":"पुनर्वसु","gana":"देव","yoni":"मार्जार","nadi":"आदि","varna":"ब्राह्मण","vashya":"मनुष्य","tara":7,"bhakoot":7},
        {"name":"पुष्य","gana":"देव","yoni":"मेष","nadi":"मध्य","varna":"क्षत्रिय","vashya":"मनुष्य","tara":8,"bhakoot":8},
        {"name":"आश्लेषा","gana":"राक्षस","yoni":"मार्जार","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"कीट","tara":9,"bhakoot":9},
        {"name":"मघा","gana":"राक्षस","yoni":"मूषक","nadi":"अन्त्य","varna":"क्षत्रिय","vashya":"कीट","tara":10,"bhakoot":10},
        {"name":"पूर्वा फाल्गुनी","gana":"मनुष्य","yoni":"मूषक","nadi":"मध्य","varna":"ब्राह्मण","vashya":"मनुष्य","tara":11,"bhakoot":11},
        {"name":"उत्तरा फाल्गुनी","gana":"मनुष्य","yoni":"गौ","nadi":"अन्त्य","varna":"क्षत्रिय","vashya":"मनुष्य","tara":12,"bhakoot":12},
        {"name":"हस्त","gana":"देव","yoni":"महिष","nadi":"आदि","varna":"वैश्य","vashya":"मनुष्य","tara":13,"bhakoot":1},
        {"name":"चित्रा","gana":"राक्षस","yoni":"व्याघ्र","nadi":"मध्य","varna":"कृषक","vashya":"कीट","tara":14,"bhakoot":2},
        {"name":"स्वाती","gana":"देव","yoni":"महिष","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"मनुष्य","tara":15,"bhakoot":3},
        {"name":"विशाखा","gana":"राक्षस","yoni":"व्याघ्र","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"मनुष्य","tara":16,"bhakoot":4},
        {"name":"अनुराधा","gana":"देव","yoni":"मृग","nadi":"आदि","varna":"वैश्य","vashya":"मनुष्य","tara":17,"bhakoot":5},
        {"name":"ज्येष्ठा","gana":"राक्षस","yoni":"मृग","nadi":"मध्य","varna":"कृषक","vashya":"मनुष्य","tara":18,"bhakoot":6},
        {"name":"मूल","gana":"राक्षस","yoni":"श्वान","nadi":"अन्त्य","varna":"कृषक","vashya":"मनुष्य","tara":19,"bhakoot":7},
        {"name":"पूर्वाषाढा","gana":"मनुष्य","yoni":"वानर","nadi":"अन्त्य","varna":"ब्राह्मण","vashya":"मनुष्य","tara":20,"bhakoot":8},
        {"name":"उत्तराषाढा","gana":"मनुष्य","yoni":"नकुल","nadi":"आदि","varna":"क्षत्रिय","vashya":"मनुष्य","tara":21,"bhakoot":9},
        {"name":"श्रवण","gana":"देव","yoni":"वानर","nadi":"अन्त्य","varna":"म्लेच्छ","vashya":"मनुष्य","tara":22,"bhakoot":10},
        {"name":"धनिष्ठा","gana":"राक्षस","yoni":"सिंह","nadi":"मध्य","varna":"कृषक","vashya":"चतुष्पद","tara":23,"bhakoot":11},
        {"name":"शतभिषा","gana":"राक्षस","yoni":"अश्व","nadi":"आदि","varna":"हंस","vashya":"चतुष्पद","tara":24,"bhakoot":12},
        {"name":"पूर्वा भाद्रपद","gana":"मनुष्य","yoni":"सिंह","nadi":"आदि","varna":"ब्राह्मण","vashya":"चतुष्पद","tara":25,"bhakoot":1},
        {"name":"उत्तरा भाद्रपद","gana":"मनुष्य","yoni":"गौ","nadi":"मध्य","varna":"क्षत्रिय","vashya":"मनुष्य","tara":26,"bhakoot":2},
        {"name":"रेवती","gana":"देव","yoni":"गज","nadi":"अन्त्य","varna":"हंस","vashya":"मनुष्य","tara":27,"bhakoot":3},
    ]

    # Yoni compatibility matrix
    YONI_ENEMIES = {
        "अश्व": ["महिष"], "महिष": ["अश्व", "व्याघ्र"], "व्याघ्र": ["महिष", "मृग"],
        "मृग": ["व्याघ्र", "श्वान"], "श्वान": ["मृग", "सर्प"], "सर्प": ["श्वान", "मूषक"],
        "मूषक": ["सर्प", "मार्जार"], "मार्जार": ["मूषक", "गज"], "गज": ["मार्जार", "सिंह"],
        "सिंह": ["गज", "वानर"], "वानर": ["सिंह", "नकुल"], "नकुल": ["वानर"],
        "गौ": ["गौ"], "वानर": ["सिंह"],
    }

    def __init__(self):
        pass

    def calculate(self, boy_nakshatra: int, girl_nakshatra: int) -> Dict:
        """Calculate Ashtakoota score"""
        boy_nak = self.NAKSHATRAS[boy_nakshatra % 27]
        girl_nak = self.NAKSHATRAS[girl_nakshatra % 27]

        scores = {}
        total = 0

        # 1. Varna (1 point)
        varna_score = self._varna(boy_nak["varna"], girl_nak["varna"])
        scores["varna"] = {"max": 1, "score": varna_score, "boy": boy_nak["varna"], "girl": girl_nak["varna"]}
        total += varna_score

        # 2. Vashya (2 points)
        vashya_score = self._vashya(boy_nak["vashya"], girl_nak["vashya"])
        scores["vashya"] = {"max": 2, "score": vashya_score, "boy": boy_nak["vashya"], "girl": girl_nak["vashya"]}
        total += vashya_score

        # 3. Tara (3 points)
        tara_score = self._tara(boy_nak["tara"], girl_nak["tara"])
        scores["tara"] = {"max": 3, "score": tara_score, "boy": boy_nak["tara"], "girl": girl_nak["tara"]}
        total += tara_score

        # 4. Yoni (4 points)
        yoni_score = self._yoni(boy_nak["yoni"], girl_nak["yoni"])
        scores["yoni"] = {"max": 4, "score": yoni_score, "boy": boy_nak["yoni"], "girl": girl_nak["yoni"]}
        total += yoni_score

        # 5. Graha Maitri (5 points) - simplified
        maitri_score = 4 if boy_nak["gana"] == girl_nak["gana"] else 2
        scores["graha_maitri"] = {"max": 5, "score": maitri_score}
        total += maitri_score

        # 6. Gana (6 points)
        gana_score = self._gana(boy_nak["gana"], girl_nak["gana"])
        scores["gana"] = {"max": 6, "score": gana_score, "boy": boy_nak["gana"], "girl": girl_nak["gana"]}
        total += gana_score

        # 7. Bhakoot (7 points)
        bhakoot_score = self._bhakoot(boy_nak["bhakoot"], girl_nak["bhakoot"])
        scores["bhakoot"] = {"max": 7, "score": bhakoot_score, "boy": boy_nak["bhakoot"], "girl": girl_nak["bhakoot"]}
        total += bhakoot_score

        # 8. Nadi (8 points)
        nadi_score = self._nadi(boy_nak["nadi"], girl_nak["nadi"])
        scores["nadi"] = {"max": 8, "score": nadi_score, "boy": boy_nak["nadi"], "girl": girl_nak["nadi"]}
        total += nadi_score

        return {
            "boy_nakshatra": boy_nak["name"],
            "girl_nakshatra": girl_nak["name"],
            "scores": scores,
            "total": total,
            "max_total": 36,
            "percentage": round((total / 36) * 100, 1),
            "verdict": self._verdict(total),
        }

    def _varna(self, b, g):
        order = ["ब्राह्मण", "क्षत्रिय", "वैश्य", "म्लेच्छ", "कृषक", "हंस"]
        try:
            return 1 if order.index(b) <= order.index(g) else 0
        except:
            return 1

    def _vashya(self, b, g):
        if b == g: return 2
        groups = {"चतुष्पद": 1, "मनुष्य": 2, "कीट": 3}
        try:
            return 1 if groups.get(b) == groups.get(g) else 0
        except:
            return 1

    def _tara(self, b, g):
        diff = abs(b - g) % 9
        return 3 if diff in [1, 3, 5, 7] else 0

    def _yoni(self, b, g):
        if b == g: return 4
        if g in self.YONI_ENEMIES.get(b, []): return 0
        return 3

    def _gana(self, b, g):
        if b == g: return 6
        if (b == "देव" and g == "मनुष्य") or (b == "मनुष्य" and g == "देव"): return 5
        if (b == "राक्षस" and g == "मनुष्य") or (b == "मनुष्य" and g == "राक्षस"): return 1
        return 0

    def _bhakoot(self, b, g):
        diff = abs(b - g) % 12
        if diff in [0, 5, 7, 9]: return 7
        return 0

    def _nadi(self, b, g):
        return 0 if b == g else 8

    def _verdict(self, total):
        if total >= 32: return "उत्तम (Excellent) — विवाह के लिए आदर्श"
        elif total >= 25: return "अच्छा (Good) — विवाह संभव"
        elif total >= 18: return "सामान्य (Average) — विचार करें"
        else: return "अशुभ (Not Recommended) — विवाह न करें"


def calculate_guna_milan(boy_nak, girl_nak):
    return AshtakootaEngine().calculate(boy_nak, girl_nak)
