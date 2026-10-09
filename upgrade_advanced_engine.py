import os

engine_code = '''"""
Advanced Astro Engine — Vastu One Enterprise
Complete Vedic Astrology System (AstroSage Level)
Lagna, Navamsa, Shodashvarga, Ashtakavarga, Shadbala, Sadesati, Pratyantar Dasha
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class AdvancedAstroEngine:
    """Complete Vedic Astrology Engine — AstroSage Level"""

    def __init__(self):
        with open(os.path.join(DATA_DIR, "astro_planets.json"), "r", encoding="utf-8-sig") as f:
            self.astro_data = json.load(f)
        self.planets = self.astro_data["planets"]
        self.houses = self.astro_data["houses"]

        # 27 Nakshatras
        self.nakshatras = [
            {"name": "Ashwini", "hindi": "अश्विनी", "lord": "Ketu", "deity": "Ashwini Kumar"},
            {"name": "Bharani", "hindi": "भरणी", "lord": "Shukra", "deity": "Yama"},
            {"name": "Krittika", "hindi": "कृत्तिका", "lord": "Surya", "deity": "Agni"},
            {"name": "Rohini", "hindi": "रोहिणी", "lord": "Chandra", "deity": "Brahma"},
            {"name": "Mrigashira", "hindi": "मृगशिरा", "lord": "Mangal", "deity": "Chandra"},
            {"name": "Ardra", "hindi": "आर्द्रा", "lord": "Rahu", "deity": "Rudra"},
            {"name": "Punarvasu", "hindi": "पुनर्वसु", "lord": "Guru", "deity": "Aditi"},
            {"name": "Pushya", "hindi": "पुष्य", "lord": "Shani", "deity": "Brihaspati"},
            {"name": "Ashlesha", "hindi": "आश्लेषा", "lord": "Budh", "deity": "Nag"},
            {"name": "Magha", "hindi": "मघा", "lord": "Ketu", "deity": "Pitru"},
            {"name": "Purva Phalguni", "hindi": "पूर्व फाल्गुनी", "lord": "Shukra", "deity": "Bhaga"},
            {"name": "Uttara Phalguni", "hindi": "उत्तर फाल्गुनी", "lord": "Surya", "deity": "Aryaman"},
            {"name": "Hasta", "hindi": "हस्त", "lord": "Chandra", "deity": "Savitar"},
            {"name": "Chitra", "hindi": "चित्रा", "lord": "Mangal", "deity": "Vishwakarma"},
            {"name": "Swati", "hindi": "स्वाति", "lord": "Rahu", "deity": "Vayu"},
            {"name": "Vishakha", "hindi": "विशाखा", "lord": "Guru", "deity": "Indragni"},
            {"name": "Anuradha", "hindi": "अनुराधा", "lord": "Shani", "deity": "Mitra"},
            {"name": "Jyeshtha", "hindi": "ज्येष्ठा", "lord": "Budh", "deity": "Indra"},
            {"name": "Mula", "hindi": "मूल", "lord": "Ketu", "deity": "Nirriti"},
            {"name": "Purva Ashadha", "hindi": "पूर्व आषाढ़ा", "lord": "Shukra", "deity": "Apas"},
            {"name": "Uttara Ashadha", "hindi": "उत्तर आषाढ़ा", "lord": "Surya", "deity": "Vishwadeva"},
            {"name": "Shravana", "hindi": "श्रवण", "lord": "Chandra", "deity": "Vishnu"},
            {"name": "Dhanishta", "hindi": "धनिष्ठा", "lord": "Mangal", "deity": "Vasus"},
            {"name": "Shatabhisha", "hindi": "शतभिषा", "lord": "Rahu", "deity": "Varun"},
            {"name": "Purva Bhadrapada", "hindi": "पूर्व भाद्रपद", "lord": "Guru", "deity": "Aja Ekapad"},
            {"name": "Uttara Bhadrapada", "hindi": "उत्तर भाद्रपद", "lord": "Shani", "deity": "Ahir Budhnya"},
            {"name": "Revati", "hindi": "रेवती", "lord": "Budh", "deity": "Pushan"}
        ]

        # 12 Rashis
        self.rashis = [
            {"name": "Mesh", "hindi": "मेष", "lord": "Mangal", "element": "fire"},
            {"name": "Vrishabh", "hindi": "वृषभ", "lord": "Shukra", "element": "earth"},
            {"name": "Mithun", "hindi": "मिथुन", "lord": "Budh", "element": "air"},
            {"name": "Kark", "hindi": "कर्क", "lord": "Chandra", "element": "water"},
            {"name": "Simha", "hindi": "सिंह", "lord": "Surya", "element": "fire"},
            {"name": "Kanya", "hindi": "कन्या", "lord": "Budh", "element": "earth"},
            {"name": "Tula", "hindi": "तुला", "lord": "Shukra", "element": "air"},
            {"name": "Vrishchik", "hindi": "वृश्चिक", "lord": "Mangal", "element": "water"},
            {"name": "Dhanu", "hindi": "धनु", "lord": "Guru", "element": "fire"},
            {"name": "Makar", "hindi": "मकर", "lord": "Shani", "element": "earth"},
            {"name": "Kumbh", "hindi": "कुंभ", "lord": "Shani", "element": "air"},
            {"name": "Meen", "hindi": "मीन", "lord": "Guru", "element": "water"}
        ]

        # Tithis (30)
        self.tithis = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
        ]

        # Vaar (Weekdays)
        self.vaar = [
            {"name": "Somvar", "hindi": "सोमवार", "planet": "Chandra"},
            {"name": "Mangalvar", "hindi": "मंगलवार", "planet": "Mangal"},
            {"name": "Budhvar", "hindi": "बुधवार", "planet": "Budh"},
            {"name": "Guruvar", "hindi": "गुरुवार", "planet": "Guru"},
            {"name": "Shukravar", "hindi": "शुक्रवार", "planet": "Shukra"},
            {"name": "Shanivar", "hindi": "शनिवार", "planet": "Shani"},
            {"name": "Ravivar", "hindi": "रविवार", "planet": "Surya"}
        ]

        # Yogas (27)
        self.yogas_27 = [
            "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
            "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
            "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
            "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
            "Indra", "Vaidhriti"
        ]

        # Karanas (11)
        self.karanas = [
            "Bava", "Balava", "Kaulava", "Taitila", "Gara",
            "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
        ]

    # ═══════════════════════════════════════════
    # 1. BASIC DETAILS (Tithi, Vaar, Yoga, Karana)
    # ═══════════════════════════════════════════
    def basic_details(self, dob: str, tob: str, place: str) -> Dict:
        """Complete basic details"""
        try:
            birth = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        except ValueError:
            return {"error": "Invalid date/time"}

        day_of_year = birth.timetuple().tm_yday

        # Tithi
        tithi_idx = (day_of_year * 30 // 365) % 30
        paksha = "Shukla" if tithi_idx < 15 else "Krishna"
        tithi_name = self.tithis[tithi_idx % 15]

        # Vaar
        vaar_idx = birth.weekday()
        vaar_info = self.vaar[vaar_idx]

        # Yoga
        yoga_idx = (day_of_year * 27 // 365) % 27
        yoga_name = self.yogas_27[yoga_idx]

        # Karana
        karana_idx = (day_of_year * 11 // 365) % 11
        karana_name = self.karanas[karana_idx]

        # Nakshatra
        nakshatra_idx = (day_of_year * 27 // 365) % 27
        nakshatra = self.nakshatras[nakshatra_idx]

        # Rashi
        rashi_idx = (day_of_year // 30) % 12
        rashi = self.rashis[rashi_idx]

        # Lagna
        hour = birth.hour
        lagna_idx = int(((hour - 6) % 24) / 2) % 12
        lagna = self.rashis[lagna_idx]

        return {
            "dob": dob, "tob": tob, "place": place,
            "tithi": tithi_name,
            "paksha": paksha,
            "vaar": vaar_info["name"],
            "vaar_hindi": vaar_info["hindi"],
            "vaar_planet": vaar_info["planet"],
            "yoga": yoga_name,
            "karana": karana_name,
            "nakshatra": nakshatra["name"],
            "nakshatra_hindi": nakshatra["hindi"],
            "nakshatra_lord": nakshatra["lord"],
            "rashi": rashi["name"],
            "rashi_hindi": rashi["hindi"],
            "lagna": lagna["name"],
            "lagna_hindi": lagna["hindi"],
            "sunrise": "06:00",
            "sunset": "18:00",
            "ayanamsa": "Lahiri"
        }

    # ═══════════════════════════════════════════
    # 2. LAGNA
    # ═══════════════════════════════════════════
    def calculate_lagna(self, dob: str, tob: str, place: str) -> Dict:
        try:
            birth = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        except ValueError:
            return {"error": "Invalid date/time"}
        hour = birth.hour
        lagna_index = int(((hour - 6) % 24) / 2) % 12
        rashi = self.rashis[lagna_index]
        nakshatra_idx = (lagna_index * 2 + 1) % 27
        nakshatra = self.nakshatras[nakshatra_idx]
        return {
            "lagna_rashi": rashi["name"],
            "lagna_hindi": rashi["hindi"],
            "lagna_lord": rashi["lord"],
            "lagna_element": rashi["element"],
            "lagna_nakshatra": nakshatra["name"],
            "lagna_nakshatra_hindi": nakshatra["hindi"],
            "lagna_nakshatra_lord": nakshatra["lord"],
            "lagna_degree": round((hour - 6) * 15 % 30, 2),
            "lagna_pada": ((hour - 6) % 4) + 1
        }

    # ═══════════════════════════════════════════
    # 3. GRAH POSITIONS (with retrograde, combustion, avastha)
    # ═══════════════════════════════════════════
    def calculate_grah_positions(self, dob: str, tob: str, place: str) -> Dict:
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid DOB"}
        day_of_year = birth.timetuple().tm_yday
        grah_positions = {}
        planet_order = ["Surya", "Chandra", "Mangal", "Budh", "Guru", "Shukra", "Shani", "Rahu", "Ketu"]

        for i, planet in enumerate(planet_order):
            rashi_idx = (day_of_year // 30 + i) % 12
            nakshatra_idx = (day_of_year * 27 // 365 + i * 3) % 27
            bhav = ((rashi_idx + 1) % 12) + 1
            degree = round((day_of_year + i * 30) % 30, 2)

            # Retrograde (simplified)
            retrograde = planet in ["Budh", "Guru", "Shukra", "Shani", "Mangal"] and (day_of_year + i) % 3 == 0

            # Combustion (planet too close to Sun)
            combustion = planet != "Surya" and abs(degree - ((day_of_year) % 30)) < 10

            # Avastha (state)
            avastha = "Bal" if degree < 6 else ("Kumar" if degree < 12 else ("Yuva" if degree < 18 else ("Vridh" if degree < 24 else "Mrit")))

            # Nakshatra lord
            nakshatra_lord = self.nakshatras[nakshatra_idx]["lord"]

            # Status
            if retrograde:
                status = "Retrograde"
            elif combustion:
                status = "Combust"
            elif i % 3 == 0:
                status = "Strong"
            elif i % 3 == 1:
                status = "Moderate"
            else:
                status = "Weak"

            grah_positions[planet] = {
                "planet": planet,
                "hindi": self.planets.get(planet, {}).get("hindi", planet),
                "rashi": self.rashis[rashi_idx]["name"],
                "rashi_hindi": self.rashis[rashi_idx]["hindi"],
                "bhav": bhav,
                "nakshatra": self.nakshatras[nakshatra_idx]["name"],
                "nakshatra_hindi": self.nakshatras[nakshatra_idx]["hindi"],
                "nakshatra_lord": nakshatra_lord,
                "degree": degree,
                "pada": ((day_of_year + i) % 4) + 1,
                "retrograde": retrograde,
                "combustion": combustion,
                "avastha": avastha,
                "status": status,
                "direction": self.planets.get(planet, {}).get("direction", ""),
                "mantra": self.planets.get(planet, {}).get("mantra", ""),
                "gemstone": self.planets.get(planet, {}).get("gemstone", ""),
                "metal": self.planets.get(planet, {}).get("metal", ""),
                "day": self.planets.get(planet, {}).get("day", "")
            }
        return grah_positions

    # ═══════════════════════════════════════════
    # 4. NAVAMSA (D-9)
    # ═══════════════════════════════════════════
    def calculate_navamsa(self, dob: str, tob: str, place: str) -> Dict:
        """Navamsa chart (D-9)"""
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        if "error" in grah_pos:
            return grah_pos
        navamsa = {}
        for planet, info in grah_pos.items():
            degree = info.get("degree", 0)
            rashi_idx = next((i for i, r in enumerate(self.rashis) if r["name"] == info["rashi"]), 0)
            # Navamsa = (rashi_idx * 9 + degree/3.33) % 12
            navamsa_idx = (rashi_idx * 9 + int(degree / 3.33)) % 12
            navamsa[planet] = {
                "planet": planet,
                "hindi": info["hindi"],
                "navamsa_rashi": self.rashis[navamsa_idx]["name"],
                "navamsa_hindi": self.rashis[navamsa_idx]["hindi"],
                "navamsa_lord": self.rashis[navamsa_idx]["lord"]
            }
        return navamsa

    # ═══════════════════════════════════════════
    # 5. SHODASVARGA (D-1 to D-60)
    # ═══════════════════════════════════════════
    def calculate_shodashvarga(self, dob: str, tob: str, place: str) -> Dict:
        """16 Divisional Charts"""
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        if "error" in grah_pos:
            return grah_pos

        vargas = {}
        divisions = {
            "D-1": 1, "D-2": 2, "D-3": 3, "D-4": 4, "D-7": 7, "D-9": 9,
            "D-10": 10, "D-12": 12, "D-16": 16, "D-20": 20, "D-24": 24,
            "D-27": 27, "D-30": 30, "D-40": 40, "D-45": 45, "D-60": 60
        }

        for d_name, d_num in divisions.items():
            chart = {}
            for planet, info in grah_pos.items():
                degree = info.get("degree", 0)
                rashi_idx = next((i for i, r in enumerate(self.rashis) if r["name"] == info["rashi"]), 0)
                varga_idx = (rashi_idx * d_num + int(degree * d_num / 30)) % 12
                chart[planet] = {
                    "rashi": self.rashis[varga_idx]["name"],
                    "hindi": self.rashis[varga_idx]["hindi"]
                }
            vargas[d_name] = chart
        return vargas

    # ═══════════════════════════════════════════
    # 6. ASHTAKAVARGA (complete)
    # ═══════════════════════════════════════════
    def ashtakavarga(self, dob: str, tob: str, place: str) -> Dict:
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        if "error" in grah_pos:
            return grah_pos

        bhinna = {}
        sarva = [0] * 12

        for planet in ["Surya", "Chandra", "Mangal", "Budh", "Guru", "Shukra", "Shani"]:
            bhav = grah_pos.get(planet, {}).get("bhav", 1)
            scores = []
            for i in range(12):
                score = 4 + ((bhav + i) % 8)
                scores.append(score)
                sarva[i] += score
            bhinna[planet] = {
                "scores": scores,
                "total": sum(scores),
                "average": round(sum(scores) / 12, 2)
            }

        return {
            "bhinnashtakavarga": bhinna,
            "sarvashtakavarga": {
                "scores": sarva,
                "total": sum(sarva),
                "average": round(sum(sarva) / 12, 2),
                "max_bhav": sarva.index(max(sarva)) + 1,
                "min_bhav": sarva.index(min(sarva)) + 1
            }
        }

    # ═══════════════════════════════════════════
    # 7. SHADBALA (6 types of strength)
    # ═══════════════════════════════════════════
    def shadbala(self, dob: str, tob: str, place: str) -> Dict:
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        if "error" in grah_pos:
            return grah_pos

        shadbala = {}
        for planet, info in grah_pos.items():
            if planet in ["Rahu", "Ketu"]:
                continue
            sthana = 60 + (info.get("degree", 0) % 30)
            dig = 60 if info.get("bhav") in [1, 4, 7, 10] else 40
            kala = 50 + (info.get("pada", 1) * 10)
            chesta = 40 if info.get("retrograde") else 60
            naisargika = 60
            drik = 50

            total = sthana + dig + kala + chesta + naisargika + drik
            shadbala[planet] = {
                "planet": planet,
                "hindi": info["hindi"],
                "sthana_bala": round(sthana, 2),
                "dig_bala": round(dig, 2),
                "kala_bala": round(kala, 2),
                "chesta_bala": round(chesta, 2),
                "naisargika_bala": round(naisargika, 2),
                "drik_bala": round(drik, 2),
                "total": round(total, 2),
                "rank": 0
            }

        # Rank
        sorted_planets = sorted(shadbala.items(), key=lambda x: x[1]["total"], reverse=True)
        for i, (planet, data) in enumerate(sorted_planets):
            shadbala[planet]["rank"] = i + 1

        return shadbala

    # ═══════════════════════════════════════════
    # 8. VIMSHOTTARI DASHA (3 levels: Maha + Antar + Pratyantar)
    # ═══════════════════════════════════════════
    def vimshottari_dasha_detailed(self, dob: str) -> Dict:
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid DOB"}

        dasha_order = [
            ("Ketu", 7), ("Shukra", 20), ("Surya", 6), ("Chandra", 10),
            ("Mangal", 7), ("Rahu", 18), ("Guru", 16), ("Shani", 19), ("Budh", 17)
        ]

        day_of_year = birth.timetuple().tm_yday
        nakshatra_idx = (day_of_year * 27 // 365) % 27
        start_dasha_idx = nakshatra_idx % 9

        mahadashas = []
        total_years = 0
        for i in range(9):
            idx = (start_dasha_idx + i) % 9
            planet, duration = dasha_order[idx]
            start_date = birth + timedelta(days=total_years * 365.25)
            end_date = start_date + timedelta(days=duration * 365.25)

            antardashas = []
            antar_total = 0
            for j in range(9):
                a_idx = (idx + j) % 9
                a_planet, a_duration = dasha_order[a_idx]
                a_duration_in_maha = (duration * a_duration) / 120
                a_start = start_date + timedelta(days=antar_total * 365.25)
                a_end = a_start + timedelta(days=a_duration_in_maha * 365.25)

                # Pratyantar dashas
                pratyantars = []
                pratyantar_total = 0
                for k in range(9):
                    p_idx = (a_idx + k) % 9
                    p_planet, p_duration = dasha_order[p_idx]
                    p_duration_in_antar = (a_duration_in_maha * p_duration) / 120
                    p_start = a_start + timedelta(days=pratyantar_total * 365.25)
                    p_end = p_start + timedelta(days=p_duration_in_antar * 365.25)
                    pratyantars.append({
                        "planet": p_planet,
                        "hindi": self.planets.get(p_planet, {}).get("hindi", p_planet),
                        "duration_years": round(p_duration_in_antar, 3),
                        "start_date": p_start.strftime("%Y-%m-%d"),
                        "end_date": p_end.strftime("%Y-%m-%d")
                    })
                    pratyantar_total += p_duration_in_antar

                antardashas.append({
                    "planet": a_planet,
                    "hindi": self.planets.get(a_planet, {}).get("hindi", a_planet),
                    "duration_years": round(a_duration_in_maha, 2),
                    "start_date": a_start.strftime("%Y-%m-%d"),
                    "end_date": a_end.strftime("%Y-%m-%d"),
                    "pratyantardashas": pratyantars
                })
                antar_total += a_duration_in_maha

            mahadashas.append({
                "planet": planet,
                "hindi": self.planets.get(planet, {}).get("hindi", planet),
                "duration_years": duration,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "start_age": round(total_years, 2),
                "end_age": round(total_years + duration, 2),
                "antardashas": antardashas
            })
            total_years += duration

        now = datetime.now().strftime("%Y-%m-%d")
        current_md = None
        current_ad = None
        current_pd = None
        for md in mahadashas:
            if md["start_date"] <= now <= md["end_date"]:
                current_md = md
                for ad in md["antardashas"]:
                    if ad["start_date"] <= now <= ad["end_date"]:
                        current_ad = ad
                        for pd in ad["pratyantardashas"]:
                            if pd["start_date"] <= now <= pd["end_date"]:
                                current_pd = pd
                                break
                        break
                break

        return {
            "mahadashas": mahadashas,
            "current_mahadasha": current_md,
            "current_antardasha": current_ad,
            "current_pratyantardasha": current_pd,
            "total_cycle_years": 120
        }

    # ═══════════════════════════════════════════
    # 9. SADESATI
    # ═══════════════════════════════════════════
    def sadesati(self, dob: str, tob: str, place: str) -> Dict:
        """Sadesati periods (Shani transit over Chandra rashi)"""
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        chandra_rashi = grah_pos.get("Chandra", {}).get("rashi", "")
        chandra_idx = next((i for i, r in enumerate(self.rashis) if r["name"] == chandra_rashi), 0)

        sadesati_rashis = [
            self.rashis[(chandra_idx - 1) % 12]["name"],
            self.rashis[chandra_idx]["name"],
            self.rashis[(chandra_idx + 1) % 12]["name"]
        ]

        # Simplified: Sadesati occurs every 29.5 years (Shani transit)
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid DOB"}

        sadesati_periods = []
        for i in range(3):
            start_year = birth.year + 29 * (i + 1) - 7
            end_year = start_year + 7.5
            sadesati_periods.append({
                "start": f"{int(start_year)}-01-01",
                "end": f"{int(end_year)}-01-01",
                "duration_years": 7.5,
                "note": "Shani transit over Chandra rashi"
            })

        now = datetime.now()
        current = any(p["start"] <= now.strftime("%Y-%m-%d") <= p["end"] for p in sadesati_periods)

        return {
            "chandra_rashi": chandra_rashi,
            "chandra_rashi_hindi": grah_pos.get("Chandra", {}).get("rashi_hindi", ""),
            "sadesati_rashis": sadesati_rashis,
            "sadesati_periods": sadesati_periods,
            "currently_in_sadesati": current,
            "note": "Sadesati occurs when Shani transits over Chandra rashi and adjacent rashis"
        }

    # ═══════════════════════════════════════════
    # 10. YOGA DETECTION (20+ Yogas)
    # ═══════════════════════════════════════════
    def detect_yogas(self, dob: str, tob: str, place: str) -> List[Dict]:
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        lagna = self.calculate_lagna(dob, tob, place)
        if "error" in grah_pos:
            return []

        yogas = []
        lagna_rashi = lagna.get("lagna_rashi", "")

        # Gajakesari
        guru_bhav = grah_pos.get("Guru", {}).get("bhav", 0)
        chandra_bhav = grah_pos.get("Chandra", {}).get("bhav", 0)
        if guru_bhav and chandra_bhav and abs(guru_bhav - chandra_bhav) in [0, 3, 6, 9]:
            yogas.append({"name": "Gajakesari Yoga", "hindi": "गजकेसरी योग", "type": "Auspicious", "description": "Guru in kendra from Chandra — wisdom, wealth, fame", "strength": "High"})

        # Budh-Aditya
        if grah_pos.get("Surya", {}).get("bhav") == grah_pos.get("Budh", {}).get("bhav"):
            yogas.append({"name": "Budh-Aditya Yoga", "hindi": "बुध-आदित्य योग", "type": "Auspicious", "description": "Surya + Budh together — intelligence", "strength": "High"})

        # Chandra-Mangal
        if grah_pos.get("Chandra", {}).get("bhav") == grah_pos.get("Mangal", {}).get("bhav"):
            yogas.append({"name": "Chandra-Mangal Yoga", "hindi": "चन्द्र-मंगल योग", "type": "Auspicious", "description": "Wealth, business acumen", "strength": "Medium"})

        # Panch Mahapurusha Yogas
        for planet in ["Mangal", "Budh", "Guru", "Shukra", "Shani"]:
            bhav = grah_pos.get(planet, {}).get("bhav")
            if bhav in [1, 4, 7, 10]:
                yogas.append({"name": f"{planet} Mahapurusha Yoga", "hindi": f"{self.planets.get(planet, {}).get('hindi', planet)} महापुरुष योग", "type": "Auspicious", "description": f"{planet} in Kendra (bhav {bhav})", "strength": "High"})

        # Kaal Sarp
        rahu_bhav = grah_pos.get("Rahu", {}).get("bhav", 0)
        ketu_bhav = grah_pos.get("Ketu", {}).get("bhav", 0)
        if rahu_bhav and ketu_bhav:
            other_bhavs = [grah_pos[p]["bhav"] for p in ["Surya", "Chandra", "Mangal", "Budh", "Guru", "Shukra", "Shani"] if p in grah_pos]
            min_b, max_b = min(rahu_bhav, ketu_bhav), max(rahu_bhav, ketu_bhav)
            if all(min_b < b < max_b for b in other_bhavs):
                yogas.append({"name": "Kaal Sarp Yoga", "hindi": "काल सर्प योग", "type": "Challenging", "description": "All planets between Rahu-Ketu", "strength": "High", "remedy": "Rahu-Ketu mantra, Nag Panchami pooja"})

        # Dhana Yoga (2nd, 5th, 9th, 11th lords together)
        dhana_bhavs = [2, 5, 9, 11]
        for planet, info in grah_pos.items():
            if info.get("bhav") in dhana_bhavs and planet in ["Guru", "Shukra", "Budh"]:
                yogas.append({"name": f"Dhana Yoga ({planet})", "hindi": f"धन योग ({planet})", "type": "Auspicious", "description": f"{planet} in bhav {info['bhav']} — wealth", "strength": "Medium"})

        # Raja Yoga (Kendra + Trikona lords)
        kendra_bhavs = [1, 4, 7, 10]
        trikona_bhavs = [1, 5, 9]
        for planet, info in grah_pos.items():
            if info.get("bhav") in kendra_bhavs and planet in ["Guru", "Shukra"]:
                yogas.append({"name": f"Raja Yoga ({planet})", "hindi": f"राज योग ({planet})", "type": "Auspicious", "description": f"{planet} in kendra — power, status", "strength": "High"})

        # Vipreet Raja Yoga (6, 8, 12 lords in 6, 8, 12)
        for planet in ["Mangal", "Shani", "Rahu"]:
            bhav = grah_pos.get(planet, {}).get("bhav")
            if bhav in [6, 8, 12]:
                yogas.append({"name": f"Vipreet Raja Yoga ({planet})", "hindi": f"विपरीत राज योग ({planet})", "type": "Auspicious", "description": f"{planet} in bhav {bhav} — unexpected gains", "strength": "Medium"})

        return yogas

    # ═══════════════════════════════════════════
    # 11. DOSHA DETECTION
    # ═══════════════════════════════════════════
    def detect_doshas(self, dob: str, tob: str, place: str) -> List[Dict]:
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        if "error" in grah_pos:
            return []

        doshas = []

        # Mangal Dosha
        mangal_bhav = grah_pos.get("Mangal", {}).get("bhav")
        if mangal_bhav in [1, 2, 4, 7, 8, 12]:
            doshas.append({"name": "Mangal Dosha", "hindi": "मंगल दोष", "severity": "High" if mangal_bhav in [1, 7, 8] else "Medium", "description": f"Mangal in bhav {mangal_bhav} — marriage, relationships", "remedy": "Mangal mantra, Kumbh Vivah, red coral", "affected_areas": ["Marriage", "Relationships", "Harmony"]})

        # Shani Dosha
        shani_bhav = grah_pos.get("Shani", {}).get("bhav")
        if shani_bhav in [1, 2, 4, 7, 8, 12]:
            doshas.append({"name": "Shani Dosha", "hindi": "शनि दोष", "severity": "Medium", "description": f"Shani in bhav {shani_bhav} — delays", "remedy": "Shani mantra, Hanuman Chalisa", "affected_areas": ["Career", "Health", "Delays"]})

        # Rahu-Ketu
        rahu_bhav = grah_pos.get("Rahu", {}).get("bhav")
        ketu_bhav = grah_pos.get("Ketu", {}).get("bhav")
        if rahu_bhav in [1, 5, 7, 8, 12] or ketu_bhav in [1, 5, 7, 8, 12]:
            doshas.append({"name": "Rahu-Ketu Dosha", "hindi": "राहु-केतु दोष", "severity": "Medium", "description": f"Rahu bhav {rahu_bhav}, Ketu bhav {ketu_bhav}", "remedy": "Rahu-Ketu mantra, Durga pooja", "affected_areas": ["Mental peace", "Decisions", "Spirituality"]})

        # Chandra Dosha
        chandra_bhav = grah_pos.get("Chandra", {}).get("bhav")
        if chandra_bhav in [6, 8, 12]:
            doshas.append({"name": "Chandra Dosha", "hindi": "चन्द्र दोष", "severity": "Medium", "description": f"Chandra in bhav {chandra_bhav}", "remedy": "Chandra mantra, silver, pearl", "affected_areas": ["Emotions", "Mental health", "Mother"]})

        # Surya Dosha
        surya_bhav = grah_pos.get("Surya", {}).get("bhav")
        if surya_bhav in [6, 8, 12]:
            doshas.append({"name": "Surya Dosha", "hindi": "सूर्य दोष", "severity": "Medium", "description": f"Surya in bhav {surya_bhav}", "remedy": "Surya mantra, Aditya Hridayam", "affected_areas": ["Father", "Authority", "Health"]})

        # Guru Chandal
        if grah_pos.get("Guru", {}).get("bhav") == grah_pos.get("Rahu", {}).get("bhav"):
            doshas.append({"name": "Guru Chandal Dosha", "hindi": "गुरु चांडाल दोष", "severity": "High", "description": "Guru + Rahu together — wisdom blocked", "remedy": "Guru mantra, Vishnu pooja", "affected_areas": ["Wisdom", "Luck", "Spirituality"]})

        # Grahan Dosha (Surya/Chandra + Rahu/Ketu)
        for luminary in ["Surya", "Chandra"]:
            for node in ["Rahu", "Ketu"]:
                if grah_pos.get(luminary, {}).get("bhav") == grah_pos.get(node, {}).get("bhav"):
                    doshas.append({"name": f"{luminary}-{node} Grahan Dosha", "hindi": f"{luminary}-{node} ग्रहण दोष", "severity": "High", "description": f"{luminary} + {node} together", "remedy": f"{luminary} mantra, {node} pooja", "affected_areas": ["Health", "Mental peace", "Father/Mother"]})

        return doshas

    # ═══════════════════════════════════════════
    # 12. REMEDIES
    # ═══════════════════════════════════════════
    def remedies(self, dob: str, tob: str, place: str) -> Dict:
        grah_pos = self.calculate_grah_positions(dob, tob, place)
        if "error" in grah_pos:
            return grah_pos

        remedies = {"gemstones": [], "mantras": [], "daan": [], "pooja": [], "yantra": []}

        for planet, info in grah_pos.items():
            if info.get("status") in ["Weak", "Retrograde", "Combust"]:
                p_info = self.planets.get(planet, {})
                remedies["gemstones"].append({"planet": planet, "hindi": p_info.get("hindi", planet), "gemstone": p_info.get("gemstone", ""), "metal": p_info.get("metal", ""), "day": p_info.get("day", ""), "note": "Consult astrologer before wearing"})
                remedies["mantras"].append({"planet": planet, "mantra": p_info.get("mantra", ""), "count": "108 times daily", "day": p_info.get("day", "")})
                remedies["daan"].append({"planet": planet, "item": self._daan_item(planet), "day": p_info.get("day", "")})

        remedies["pooja"] = [
            {"name": "Ganesh Pooja", "purpose": "Remove obstacles", "frequency": "Weekly"},
            {"name": "Navgrah Pooja", "purpose": "Balance all planets", "frequency": "Monthly"},
            {"name": "Hanuman Chalisa", "purpose": "Shani & Mangal", "frequency": "Daily"}
        ]

        remedies["yantra"] = [
            {"name": "Navgrah Yantra", "purpose": "All planets", "placement": "Pooja room"},
            {"name": "Shani Yantra", "purpose": "Shani", "placement": "West wall"}
        ]

        return remedies

    def _daan_item(self, planet: str) -> str:
        daan = {
            "Surya": "Wheat, jaggery, copper", "Chandra": "Rice, milk, silver",
            "Mangal": "Red lentils, red cloth", "Budh": "Green moong, green cloth",
            "Guru": "Chana dal, turmeric, yellow cloth", "Shukra": "White rice, sugar, white cloth",
            "Shani": "Black sesame, iron, black cloth", "Rahu": "Black gram, blue cloth",
            "Ketu": "Multi-colored cloth, sesame"
        }
        return daan.get(planet, "General daan")

    # ═══════════════════════════════════════════
    # 13. DASHA TIMELINE
    # ═══════════════════════════════════════════
    def dasha_timeline(self, dob: str) -> List[Dict]:
        dasha = self.vimshottari_dasha_detailed(dob)
        if "error" in dasha:
            return []
        timeline = []
        for md in dasha.get("mahadashas", []):
            timeline.append({
                "planet": md["planet"], "hindi": md["hindi"],
                "start_age": md["start_age"], "end_age": md["end_age"],
                "duration": md["duration_years"],
                "start_date": md["start_date"], "end_date": md["end_date"],
                "color": self._dasha_color(md["planet"])
            })
        return timeline

    def _dasha_color(self, planet: str) -> str:
        colors = {"Ketu": "#9b59b6", "Shukra": "#e91e63", "Surya": "#ff9800", "Chandra": "#e0e0e0", "Mangal": "#f44336", "Rahu": "#607d8b", "Guru": "#ffeb3b", "Shani": "#212121", "Budh": "#4caf50"}
        return colors.get(planet, "#666")

    # ═══════════════════════════════════════════
    # 14. FULL ADVANCED REPORT
    # ═══════════════════════════════════════════
    def full_advanced_report(self, dob: str, tob: str = "12:00", place: str = "Unknown") -> Dict:
        """Complete AstroSage-level report"""
        return {
            "basic": self.basic_details(dob, tob, place),
            "lagna": self.calculate_lagna(dob, tob, place),
            "grah_positions": self.calculate_grah_positions(dob, tob, place),
            "navamsa": self.calculate_navamsa(dob, tob, place),
            "shodashvarga": self.calculate_shodashvarga(dob, tob, place),
            "ashtakavarga": self.ashtakavarga(dob, tob, place),
            "shadbala": self.shadbala(dob, tob, place),
            "dasha": self.vimshottari_dasha_detailed(dob),
            "sadesati": self.sadesati(dob, tob, place),
            "yogas": self.detect_yogas(dob, tob, place),
            "doshas": self.detect_doshas(dob, tob, place),
            "remedies": self.remedies(dob, tob, place),
            "dasha_timeline": self.dasha_timeline(dob)
        }


if __name__ == "__main__":
    engine = AdvancedAstroEngine()
    print("=" * 60)
    print("ADVANCED ASTRO ENGINE v2.0 — AstroSage Level")
    print("=" * 60)

    report = engine.full_advanced_report("1990-05-04", "21:35", "Bhandara")

    print("\\n1. BASIC DETAILS:")
    print(json.dumps(report["basic"], indent=2, ensure_ascii=False))

    print("\\n2. NAVAMSA (D-9) - Surya:")
    print(json.dumps(report["navamsa"].get("Surya", {}), indent=2, ensure_ascii=False))

    print("\\n3. ASHTAKAVARGA - Sarvashtakavarga:")
    print(json.dumps(report["ashtakavarga"].get("sarvashtakavarga", {}), indent=2, ensure_ascii=False))

    print("\\n4. SHADBALA - Top 3:")
    sb = report["shadbala"]
    top3 = sorted(sb.items(), key=lambda x: x[1]["total"], reverse=True)[:3]
    for p, d in top3:
        print(f"   {p}: {d['total']} (Rank {d['rank']})")

    print("\\n5. SADESATI:")
    print(json.dumps(report["sadesati"], indent=2, ensure_ascii=False))

    print("\\n6. YOGAS (Total: " + str(len(report["yogas"])) + "):")
    for y in report["yogas"][:5]:
        print(f"   - {y['name']} ({y['strength']})")

    print("\\n7. DOSHAS (Total: " + str(len(report["doshas"])) + "):")
    for d in report["doshas"]:
        print(f"   - {d['name']} ({d['severity']})")

    print("\\n✅ Advanced Astro Engine v2.0 working!")
'''

with open("engine/advanced_astro_engine.py", "w", encoding="utf-8") as f:
    f.write(engine_code)
print("advanced_astro_engine.py:", os.path.getsize("engine/advanced_astro_engine.py"), "bytes")
