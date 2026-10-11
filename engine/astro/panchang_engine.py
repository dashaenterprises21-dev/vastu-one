"""
VASTU ONE — Panchang Engine
Complete Panchang: Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Choghadiya
"""

from datetime import datetime, timedelta
from typing import Dict, Any
import math


class PanchangEngine:
    TITHIS = ["प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी","एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","पूर्णिमा/अमावस्या"]
    NAKSHATRAS = ["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा","पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाती","विशाखा","अनुराधा","ज्येष्ठा","मूल","पूर्वाषाढा","उत्तराषाढा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"]
    YOGAS = ["विष्कुम्भ","प्रीति","आयुष्मान","सौभाग्य","शोभन","अतिगण्ड","सुकर्मा","धृति","शूल","गण्ड","वृद्धि","ध्रुव","व्याघात","हर्षण","वज्र","सिद्धि","व्यतिपात","वरीयान","परिघ","शिव","सिद्ध","साध्य","शुभ","शुक्ल","ब्रह्म","इन्द्र","वैधृति"]
    KARANAS = ["बव","बालव","कौलव","तैतिल","गर","वणिज","विष्टि","शकुनि","चतुष्पद","नाग","किंस्तुघ्न"]
    VAAR = ["रविवार","सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार"]
    RAHU_PARTS = {0:8, 1:2, 2:7, 3:5, 4:6, 5:4, 6:3}
    YAMAGANDA_PARTS = {0:5, 1:4, 2:3, 3:2, 4:1, 5:7, 6:6}
    GULIKA_PARTS = {0:7, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1}
    CHOGHADIYA = {
        0:["उद्वेग","चर","लाभ","अमृत","काल","शुभ","रोग","उद्वेग"],
        1:["अमृत","काल","शुभ","रोग","उद्वेग","चर","लाभ","अमृत"],
        2:["रोग","उद्वेग","चर","लाभ","अमृत","काल","शुभ","रोग"],
        3:["लाभ","अमृत","काल","शुभ","रोग","उद्वेग","चर","लाभ"],
        4:["शुभ","रोग","उद्वेग","चर","लाभ","अमृत","काल","शुभ"],
        5:["चर","लाभ","अमृत","काल","शुभ","रोग","उद्वेग","चर"],
        6:["काल","शुभ","रोग","उद्वेग","चर","लाभ","अमृत","काल"]
    }
    CHOGH_NATURE = {"उद्वेग":"bad","चर":"good","लाभ":"good","अमृत":"best","काल":"bad","शुभ":"good","रोग":"bad"}

    def __init__(self, target_date=None, lat=21.1458, lng=79.0882):
        self.date = target_date or datetime.now()
        self.lat = lat
        self.lng = lng

    def calculate_all(self) -> Dict[str, Any]:
        return {
            "date": self._date_info(),
            "sun_moon": self._sun_moon_times(),
            "panchang": self._five_ang(),
            "muhurta": self._muhurta_times(),
            "choghadiya": self._choghadiya(),
        }

    def _date_info(self):
        d = self.date
        dow = (d.weekday() + 1) % 7
        return {
            "date_iso": d.strftime("%Y-%m-%d"),
            "date_display": d.strftime("%d %B %Y"),
            "vaar": self.VAAR[dow],
            "day_of_week": dow,
        }

    def _sun_moon_times(self):
        d = self.date
        doy = d.timetuple().tm_yday
        decl = 23.45 * math.sin(math.radians(360 * (284 + doy) / 365))
        lat_r = math.radians(self.lat)
        decl_r = math.radians(decl)
        try:
            ha = math.degrees(math.acos(-math.tan(lat_r) * math.tan(decl_r)))
        except:
            ha = 90
        day_len = 2 * ha / 15
        solar_noon = 12.0 - (self.lng - 82.5) / 15
        sunrise = solar_noon - day_len / 2
        sunset = solar_noon + day_len / 2

        def fmt(h):
            hh = int(h); mm = int((h - hh) * 60)
            return f"{hh:02d}:{mm:02d}"

        return {"sunrise": fmt(sunrise), "sunset": fmt(sunset), "day_length": round(day_len, 2)}

    def _five_ang(self):
        d = self.date
        dow = (d.weekday() + 1) % 7
        days = (d - datetime(2000, 1, 6, 18, 14)).days % 29.53
        tithi_n = int(days / (29.53 / 30)) + 1
        paksha = "Shukla" if tithi_n <= 15 else "Krishna"
        tithi_i = (tithi_n - 1) % 15
        tithi_h = self.TITHIS[tithi_i]
        if tithi_i == 14:
            tithi_h = "पूर्णिमा" if paksha == "Shukla" else "अमावस्या"
        nak = int((days / 29.53) * 27) % 27
        yog = int((days / 29.53) * 27) % 27
        kar = int((days / 29.53) * 60) % 60

        return {
            "tithi": tithi_h,
            "tithi_number": tithi_n,
            "paksha": paksha,
            "paksha_hindi": "शुक्ल" if paksha == "Shukla" else "कृष्ण",
            "nakshatra": self.NAKSHATRAS[nak],
            "nakshatra_number": nak + 1,
            "yoga": self.YOGAS[yog],
            "karana": self.KARANAS[kar % 11],
            "vaar": self.VAAR[dow],
        }

    def _muhurta_times(self):
        d = self.date
        dow = (d.weekday() + 1) % 7
        sun = self._sun_moon_times()
        try:
            sh, sm = map(int, sun["sunrise"].split(":"))
            eh, em = map(int, sun["sunset"].split(":"))
        except:
            sh, sm, eh, em = 6, 0, 18, 0
        sr = sh * 60 + sm
        ss = eh * 60 + em
        part = (ss - sr) / 8

        def slot(p):
            s = sr + part * (p - 1); e = sr + part * p
            return f"{int(s//60):02d}:{int(s%60):02d} - {int(e//60):02d}:{int(e%60):02d}"

        return {
            "rahu_kaal": slot(self.RAHU_PARTS[dow]),
            "yamaganda": slot(self.YAMAGANDA_PARTS[dow]),
            "gulika_kaal": slot(self.GULIKA_PARTS[dow]),
        }

    def _choghadiya(self):
        d = self.date
        dow = (d.weekday() + 1) % 7
        sun = self._sun_moon_times()
        try:
            sh, sm = map(int, sun["sunrise"].split(":"))
            eh, em = map(int, sun["sunset"].split(":"))
        except:
            sh, sm, eh, em = 6, 0, 18, 0
        sr = sh * 60 + sm; ss = eh * 60 + em
        day_d = ss - sr; night_d = 24*60 - day_d
        dp = day_d / 8; np = night_d / 8
        ch = self.CHOGHADIYA[dow]
        day_slots = []
        for i, name in enumerate(ch):
            s = sr + dp * i; e = sr + dp * (i + 1)
            day_slots.append({"name": name, "nature": self.CHOGH_NATURE.get(name, "neutral"), "start": f"{int(s//60):02d}:{int(s%60):02d}", "end": f"{int(e//60):02d}:{int(e%60):02d}"})
        night_slots = []
        for i in range(8):
            name = ch[(i + 4) % 8]
            s = ss + np * i; e = ss + np * (i + 1)
            night_slots.append({"name": name, "nature": self.CHOGH_NATURE.get(name, "neutral"), "start": f"{int(s//60)%24:02d}:{int(s%60):02d}", "end": f"{int(e//60)%24:02d}:{int(e%60):02d}"})
        return {"day": day_slots, "night": night_slots}


def calculate_panchang(target_date=None, lat=21.1458, lng=79.0882):
    return PanchangEngine(target_date, lat, lng).calculate_all()
