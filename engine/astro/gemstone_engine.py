"""
VASTU ONE — Gemstone Report Engine
Ratna recommendations with weight, metal, finger, day, mantra
"""

from typing import Dict, List


class GemstoneEngine:
    PLANETS_HINDI = {"Surya":"सूर्य","Chandra":"चंद्र","Mangal":"मंगल","Budh":"बुध","Guru":"गुरु","Shukra":"शुक्र","Shani":"शनि","Rahu":"राहु","Ketu":"केतु"}

    GEMSTONES = {
        "Surya": {"name":"माणिक्य","english":"Ruby","metal":"सोना/तांबा","finger":"अनामिका","day":"रविवार","mantra":"ॐ घृणिः सूर्याय नमः","weight":"3-6 carat","color":"लाल"},
        "Chandra": {"name":"मोती","english":"Pearl","metal":"चांदी","finger":"अनामिका","day":"सोमवार","mantra":"ॐ सों सोमाय नमः","weight":"4-7 carat","color":"सफेद"},
        "Mangal": {"name":"मूंगा","english":"Red Coral","metal":"सोना/तांबा","finger":"अनामिका","day":"मंगलवार","mantra":"ॐ अं अंगारकाय नमः","weight":"5-8 carat","color":"लाल"},
        "Budh": {"name":"पन्ना","english":"Emerald","metal":"सोना/चांदी","finger":"कनिष्ठा","day":"बुधवार","mantra":"ॐ बुं बुधाय नमः","weight":"3-6 carat","color":"हरा"},
        "Guru": {"name":"पुखराज","english":"Yellow Sapphire","metal":"सोना","finger":"तर्जनी","day":"गुरुवार","mantra":"ॐ गुं गुरवे नमः","weight":"4-7 carat","color":"पीला"},
        "Shukra": {"name":"हीरा","english":"Diamond","metal":"चांदी/प्लेटिनम","finger":"मध्यमा","day":"शुक्रवार","mantra":"ॐ शुं शुक्राय नमः","weight":"0.5-1.5 carat","color":"सफेद"},
        "Shani": {"name":"नीलम","english":"Blue Sapphire","metal":"लोहा/चांदी","finger":"मध्यमा","day":"शनिवार","mantra":"ॐ शं शनैश्चराय नमः","weight":"4-7 carat","color":"नीला"},
        "Rahu": {"name":"गोमेद","english":"Hessonite","metal":"चांदी","finger":"मध्यमा","day":"शनिवार","mantra":"ॐ रां राहवे नमः","weight":"5-8 carat","color":"भूरा"},
        "Ketu": {"name":"लहसुनिया","english":"Cat's Eye","metal":"चांदी","finger":"अनामिका","day":"मंगलवार","mantra":"ॐ कें केतवे नमः","weight":"4-7 carat","color":"भूरा-हरा"},
    }

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna

    def analyze_all(self) -> Dict:
        return {
            "recommendations": self._recommend(),
            "life_stones": self._life_stones(),
            "lucky_stones": self._lucky_stones(),
        }

    def _recommend(self) -> List[Dict]:
        results = []
        for p, info in self.GEMSTONES.items():
            pd = self.pos.get(p, {})
            bhav = pd.get("bhav")
            if bhav in [1, 5, 9, 11] and not pd.get("debilitated"):
                results.append({
                    "planet": p,
                    "planet_hindi": self.PLANETS_HINDI[p],
                    "bhav": bhav,
                    "reason": f"शुभ भाव {bhav} में",
                    **info,
                })
        return results

    def _life_stones(self) -> List[Dict]:
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        lords = {"Mesh":"Mangal","Vrishabh":"Shukra","Mithun":"Budh","Kark":"Chandra","Simha":"Surya","Kanya":"Budh","Tula":"Shukra","Vrishchik":"Mangal","Dhanu":"Guru","Makar":"Shani","Kumbh":"Shani","Meen":"Guru"}
        lord = lords.get(lagna_rashi)
        if lord and lord in self.GEMSTONES:
            return [{"lord": lord, "hindi": self.PLANETS_HINDI[lord], **self.GEMSTONES[lord]}]
        return []

    def _lucky_stones(self) -> List[Dict]:
        results = []
        for p, info in self.GEMSTONES.items():
            pd = self.pos.get(p, {})
            if pd.get("bhav") in [2, 11]:
                results.append({"planet": p, "hindi": self.PLANETS_HINDI[p], **info})
        return results


def analyze_gemstones(positions, lagna):
    return GemstoneEngine(positions, lagna).analyze_all()
