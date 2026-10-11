"""
VASTU ONE — Numerology Engine
Mulank, Bhagyank, Chaldean, Pythagorean
"""

from datetime import datetime
from typing import Dict, Any


class NumerologyEngine:
    # Chaldean number-letter mapping
    CHALDEAN = {
        'A':1,'I':1,'J':1,'Q':1,'Y':1,
        'B':2,'K':2,'R':2,
        'C':3,'G':3,'L':3,'S':3,
        'D':4,'M':4,'T':4,
        'E':5,'H':5,'N':5,'X':5,
        'U':6,'V':6,'W':6,
        'O':7,'Z':7,
        'F':8,'P':8
    }

    # Pythagorean mapping
    PYTHAGOREAN = {
        'A':1,'J':1,'S':1,
        'B':2,'K':2,'T':2,
        'C':3,'L':3,'U':3,
        'D':4,'M':4,'V':4,
        'E':5,'N':5,'W':5,
        'F':6,'O':6,'X':6,
        'G':7,'P':7,'Y':7,
        'H':8,'Q':8,'Z':8,
        'I':9,'R':9
    }

    NUMBER_MEANINGS = {
        1: {"name": "Sun", "hindi": "सूर्य", "traits": "Leadership, Independence, Ego", "color": "Red", "day": "Sunday", "gemstone": "Ruby"},
        2: {"name": "Moon", "hindi": "चंद्र", "traits": "Emotional, Intuitive, Caring", "color": "White", "day": "Monday", "gemstone": "Pearl"},
        3: {"name": "Jupiter", "hindi": "गुरु", "traits": "Wisdom, Expansion, Creativity", "color": "Yellow", "day": "Thursday", "gemstone": "Yellow Sapphire"},
        4: {"name": "Rahu", "hindi": "राहु", "traits": "Innovation, Unconventional, Sudden", "color": "Blue", "day": "Saturday", "gemstone": "Hessonite"},
        5: {"name": "Mercury", "hindi": "बुध", "traits": "Communication, Business, Intelligence", "color": "Green", "day": "Wednesday", "gemstone": "Emerald"},
        6: {"name": "Venus", "hindi": "शुक्र", "traits": "Love, Beauty, Luxury", "color": "White/Pink", "day": "Friday", "gemstone": "Diamond"},
        7: {"name": "Ketu", "hindi": "केतु", "traits": "Spiritual, Detached, Mystical", "color": "Grey", "day": "Tuesday", "gemstone": "Cat's Eye"},
        8: {"name": "Saturn", "hindi": "शनि", "traits": "Discipline, Karma, Delays", "color": "Black/Dark Blue", "day": "Saturday", "gemstone": "Blue Sapphire"},
        9: {"name": "Mars", "hindi": "मंगल", "traits": "Courage, Energy, Aggression", "color": "Red", "day": "Tuesday", "gemstone": "Red Coral"}
    }

    def __init__(self, name: str, dob: str):
        self.name = name.upper().replace(" ", "")
        self.dob = dob

    def analyze_all(self) -> Dict[str, Any]:
        return {
            "mulank": self._mulank(),
            "bhagyank": self._bhagyank(),
            "naamank_chaldean": self._naamank("chaldean"),
            "naamank_pythagorean": self._naamank("pythagorean"),
            "kua_number": self._kua_number(),
            "lucky_number": self._lucky_number(),
            "lucky_color": self._lucky_color(),
            "lucky_day": self._lucky_day(),
            "lucky_gemstone": self._lucky_gemstone(),
        }

    def _mulank(self) -> Dict:
        """Mulank (Birth number) = day of birth"""
        try:
            day = datetime.strptime(self.dob, "%Y-%m-%d").day
        except:
            day = 1
        mulank = self._reduce_to_single(day)
        return {
            "number": mulank,
            "day": day,
            "info": self.NUMBER_MEANINGS.get(mulank, {}),
        }

    def _bhagyank(self) -> Dict:
        """Bhagyank (Destiny number) = sum of all digits of DOB"""
        try:
            digits = self.dob.replace("-", "")
            total = sum(int(d) for d in digits)
        except:
            total = 1
        bhagyank = self._reduce_to_single(total)
        return {
            "number": bhagyank,
            "info": self.NUMBER_MEANINGS.get(bhagyank, {}),
        }

    def _naamank(self, system: str) -> Dict:
        """Name number using Chaldean or Pythagorean"""
        mapping = self.CHALDEAN if system == "chaldean" else self.PYTHAGOREAN
        total = 0
        for ch in self.name:
            if ch in mapping:
                total += mapping[ch]
        naamank = self._reduce_to_single(total)
        return {
            "system": system,
            "number": naamank,
            "total": total,
            "info": self.NUMBER_MEANINGS.get(naamank, {}),
        }

    def _kua_number(self) -> Dict:
        """Feng Shui Kua number"""
        try:
            year = int(self.dob[:4])
            total = sum(int(d) for d in str(year))
            kua = 11 - total if total < 10 else 11 - self._reduce_to_single(total)
            if kua > 9: kua -= 9
        except:
            kua = 1
        return {"number": kua}

    def _lucky_number(self) -> int:
        mulank = self._mulank()["number"]
        bhagyank = self._bhagyank()["number"]
        return self._reduce_to_single(mulank + bhagyank)

    def _lucky_color(self) -> str:
        return self.NUMBER_MEANINGS.get(self._mulank()["number"], {}).get("color", "")

    def _lucky_day(self) -> str:
        return self.NUMBER_MEANINGS.get(self._mulank()["number"], {}).get("day", "")

    def _lucky_gemstone(self) -> str:
        return self.NUMBER_MEANINGS.get(self._mulank()["number"], {}).get("gemstone", "")

    def _reduce_to_single(self, num: int) -> int:
        while num > 9:
            num = sum(int(d) for d in str(num))
        return num


def analyze_numerology(name, dob):
    return NumerologyEngine(name, dob).analyze_all()
