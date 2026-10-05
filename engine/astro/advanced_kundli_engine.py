"""
Advanced Kundli Engine — Vastu One Enterprise
Page C — Advanced Kundli Analysis
Charts, Aspects, 50+ Yogas, 20+ Doshas, 5-Level Dasha, Transits, Predictions
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ENGINE_DIR = os.path.dirname(__file__)

import sys
sys.path.insert(0, ENGINE_DIR)
from advanced_astro_engine import AdvancedAstroEngine
from vastu_astro_integration import VastuAstroIntegrationV2


class AdvancedKundliEngine:
    """Advanced Kundli — Complete Analysis"""

    def __init__(self):
        self.astro = AdvancedAstroEngine()
        self.integration = VastuAstroIntegrationV2()

        # Nakshatra detailed attributes
        self.nakshatra_attributes = {
            "Ashwini": {"gana": "Deva", "yoni": "Horse", "nadi": "Vata", "varna": "Vaishya"},
            "Bharani": {"gana": "Manushya", "yoni": "Elephant", "nadi": "Pitta", "varna": "Mleccha"},
            "Krittika": {"gana": "Rakshasa", "yoni": "Sheep", "nadi": "Kapha", "varna": "Brahmin"},
            "Rohini": {"gana": "Manushya", "yoni": "Serpent", "nadi": "Kapha", "varna": "Shudra"},
            "Mrigashira": {"gana": "Deva", "yoni": "Serpent", "nadi": "Pitta", "varna": "Vaishya"},
            "Ardra": {"gana": "Manushya", "yoni": "Dog", "nadi": "Vata", "varna": "Butcher"},
            "Punarvasu": {"gana": "Deva", "yoni": "Cat", "nadi": "Vata", "varna": "Vaishya"},
            "Pushya": {"gana": "Deva", "yoni": "Sheep", "nadi": "Pitta", "varna": "Kshatriya"},
            "Ashlesha": {"gana": "Rakshasa", "yoni": "Cat", "nadi": "Kapha", "varna": "Mleccha"},
            "Magha": {"gana": "Rakshasa", "yoni": "Rat", "nadi": "Kapha", "varna": "Shudra"},
            "Purva Phalguni": {"gana": "Manushya", "yoni": "Rat", "nadi": "Pitta", "varna": "Brahmin"},
            "Uttara Phalguni": {"gana": "Manushya", "yoni": "Cow", "nadi": "Pitta", "varna": "Kshatriya"},
            "Hasta": {"gana": "Deva", "yoni": "Buffalo", "nadi": "Vata", "varna": "Vaishya"},
            "Chitra": {"gana": "Rakshasa", "yoni": "Tiger", "nadi": "Pitta", "varna": "Shudra"},
            "Swati": {"gana": "Deva", "yoni": "Buffalo", "nadi": "Vata", "varna": "Butcher"},
            "Vishakha": {"gana": "Rakshasa", "yoni": "Tiger", "nadi": "Kapha", "varna": "Mleccha"},
            "Anuradha": {"gana": "Deva", "yoni": "Deer", "nadi": "Pitta", "varna": "Shudra"},
            "Jyeshtha": {"gana": "Rakshasa", "yoni": "Deer", "nadi": "Vata", "varna": "Butcher"},
            "Mula": {"gana": "Rakshasa", "yoni": "Dog", "nadi": "Vata", "varna": "Butcher"},
            "Purva Ashadha": {"gana": "Manushya", "yoni": "Monkey", "nadi": "Pitta", "varna": "Brahmin"},
            "Uttara Ashadha": {"gana": "Manushya", "yoni": "Mongoose", "nadi": "Pitta", "varna": "Kshatriya"},
            "Shravana": {"gana": "Deva", "yoni": "Monkey", "nadi": "Kapha", "varna": "Mleccha"},
            "Dhanishta": {"gana": "Rakshasa", "yoni": "Lion", "nadi": "Kapha", "varna": "Butcher"},
            "Shatabhisha": {"gana": "Rakshasa", "yoni": "Horse", "nadi": "Vata", "varna": "Butcher"},
            "Purva Bhadrapada": {"gana": "Manushya", "yoni": "Lion", "nadi": "Vata", "varna": "Brahmin"},
            "Uttara Bhadrapada": {"gana": "Manushya", "yoni": "Cow", "nadi": "Pitta", "varna": "Kshatriya"},
            "Revati": {"gana": "Deva", "yoni": "Elephant", "nadi": "Kapha", "varna": "Shudra"}
        }

    # ═══════════════════════════════════════════
    # 1. VISUAL CHARTS (North/South Indian)
    # ═══════════════════════════════════════════
    def generate_charts(self, dob: str, tob: str, place: str) -> Dict:
        """Generate North and South Indian chart data"""
        grah_pos = self.astro.calculate_grah_positions(dob, tob, place)
        lagna = self.astro.calculate_lagna(dob, tob, place)
        if "error" in grah_pos:
            return grah_pos

        lagna_rashi = lagna.get("lagna_rashi", "Mesh")
        rashis = [r["name"] for r in self.astro.rashis]
        lagna_idx = rashis.index(lagna_rashi) if lagna_rashi in rashis else 0

        # North Indian chart: houses fixed, rashis move
        north_chart = {}
        for i, rashi in enumerate(rashis):
            bhav = ((i - lagna_idx) % 12) + 1
            north_chart[bhav] = {
                "rashi": rashi,
                "hindi": self.astro.rashis[i]["hindi"],
                "planets": [p for p, info in grah_pos.items() if info.get("rashi") == rashi]
            }

        # South Indian chart: rashis fixed, houses move
        south_chart = {}
        for i, rashi in enumerate(rashis):
            south_chart[rashi] = {
                "rashi": rashi,
                "hindi": self.astro.rashis[i]["hindi"],
                "bhav": ((i - lagna_idx) % 12) + 1,
                "planets": [p for p, info in grah_pos.items() if info.get("rashi") == rashi]
            }

        return {
            "lagna_rashi": lagna_rashi,
            "lagna_hindi": lagna.get("lagna_hindi", ""),
            "north_chart": north_chart,
            "south_chart": south_chart
        }

    # ═══════════════════════════════════════════
    # 2. PLANETARY ASPECTS (Grah Drishti)
    # ═══════════════════════════════════════════
    def planetary_aspects(self, dob: str, tob: str, place: str) -> List[Dict]:
        """Calculate planetary aspects (conjunctions, oppositions, etc.)"""
        grah_pos = self.astro.calculate_grah_positions(dob, tob, place)
        if "error" in grah_pos:
            return []

        aspects = []
        planets = list(grah_pos.keys())

        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                b1 = grah_pos[p1].get("bhav", 0)
                b2 = grah_pos[p2].get("bhav", 0)
                diff = abs(b1 - b2)

                aspect_type = None
                if diff == 0:
                    aspect_type = "Conjunction"
                elif diff == 6:
                    aspect_type = "Opposition"
                elif diff == 3:
                    aspect_type = "Square"
                elif diff in [4, 8]:
                    aspect_type = "Trine"

                if aspect_type:
                    aspects.append({
                        "planet1": p1,
                        "planet2": p2,
                        "planet1_hindi": grah_pos[p1]["hindi"],
                        "planet2_hindi": grah_pos[p2]["hindi"],
                        "bhav1": b1,
                        "bhav2": b2,
                        "aspect_type": aspect_type,
                        "strength": "High" if aspect_type in ["Conjunction", "Opposition"] else "Medium"
                    })

        return aspects

    # ═══════════════════════════════════════════
    # 3. 50+ YOGAS (Detailed)
    # ═══════════════════════════════════════════
    def detect_all_yogas(self, dob: str, tob: str, place: str) -> List[Dict]:
        """Detect 50+ Yogas"""
        # Get base yogas from advanced engine
        base_yogas = self.astro.detect_yogas(dob, tob, place)
        grah_pos = self.astro.calculate_grah_positions(dob, tob, place)

        all_yogas = list(base_yogas)

        # Additional yogas
        # 1. Sunapha Yoga (2nd from Chandra)
        chandra_bhav = grah_pos.get("Chandra", {}).get("bhav", 0)
        if chandra_bhav:
            bhav2 = (chandra_bhav % 12) + 1
            if any(info.get("bhav") == bhav2 for p, info in grah_pos.items() if p not in ["Chandra", "Surya"]):
                all_yogas.append({"name": "Sunapha Yoga", "hindi": "सुनफा योग", "type": "Auspicious", "description": "Planets in 2nd from Chandra — wealth", "strength": "Medium"})

        # 2. Anapha Yoga (12th from Chandra)
        bhav12 = ((chandra_bhav - 2) % 12) + 1
        if any(info.get("bhav") == bhav12 for p, info in grah_pos.items() if p not in ["Chandra", "Surya"]):
            all_yogas.append({"name": "Anapha Yoga", "hindi": "अनफा योग", "type": "Auspicious", "description": "Planets in 12th from Chandra — health", "strength": "Medium"})

        # 3. Kemadruma Yoga (no planets around Chandra)
        bhav2 = (chandra_bhav % 12) + 1
        bhav12 = ((chandra_bhav - 2) % 12) + 1
        has_around = any(info.get("bhav") in [bhav2, bhav12] for p, info in grah_pos.items() if p not in ["Chandra", "Surya"])
        if not has_around:
            all_yogas.append({"name": "Kemadruma Yoga", "hindi": "केमद्रुम योग", "type": "Challenging", "description": "No planets around Chandra — struggles", "strength": "High", "remedy": "Chandra mantra, silver"})

        # 4. Amala Yoga (10th from Chandra or Lagna)
        for ref_planet in ["Chandra"]:
            bhav10 = ((grah_pos.get(ref_planet, {}).get("bhav", 0) + 8) % 12) + 1
            if any(info.get("bhav") == bhav10 and p in ["Guru", "Shukra", "Budh"] for p, info in grah_pos.items()):
                all_yogas.append({"name": "Amala Yoga", "hindi": "अमल योग", "type": "Auspicious", "description": "Benefic in 10th from Chandra — fame", "strength": "High"})

        # 5. Chatussagara Yoga (all kendras occupied)
        kendras = [1, 4, 7, 10]
        occupied_kendras = set()
        for p, info in grah_pos.items():
            if info.get("bhav") in kendras:
                occupied_kendras.add(info.get("bhav"))
        if len(occupied_kendras) == 4:
            all_yogas.append({"name": "Chatussagara Yoga", "hindi": "चतुस्सागर योग", "type": "Auspicious", "description": "All kendras occupied — stable life", "strength": "High"})

        # 6. Vasumati Yoga (benefics in upachaya)
        upachaya = [3, 6, 10, 11]
        benefics_in_upachaya = [p for p in ["Guru", "Shukra", "Budh"] if grah_pos.get(p, {}).get("bhav") in upachaya]
        if benefics_in_upachaya:
            all_yogas.append({"name": "Vasumati Yoga", "hindi": "वसुमती योग", "type": "Auspicious", "description": "Benefics in upachaya — wealth", "strength": "Medium"})

        # 7. Shakata Yoga (Chandra and Guru in 6/8 from each other)
        guru_bhav = grah_pos.get("Guru", {}).get("bhav", 0)
        if abs(chandra_bhav - guru_bhav) in [5, 7]:
            all_yogas.append({"name": "Shakata Yoga", "hindi": "शकट योग", "type": "Challenging", "description": "Chandra-Guru in 6/8 — fluctuating fortune", "strength": "Medium"})

        # 8. Kendra Trikona Yoga (Raja Yoga combinations)
        kendra_lords = []
        trikona_lords = []
        # Simplified — check if same planet in both
        for p, info in grah_pos.items():
            if info.get("bhav") in [1, 4, 7, 10]:
                kendra_lords.append(p)
        if len(kendra_lords) >= 3:
            all_yogas.append({"name": "Kendra Trikona Yoga", "hindi": "केंद्र त्रिकोण योग", "type": "Auspicious", "description": "Strong kendras — leadership", "strength": "High"})

        # 9. Maha Bhagya Yoga (Guru in kendra from Lagna)
        lagna = self.astro.calculate_lagna(dob, tob, place)
        lagna_idx = next((i for i, r in enumerate(self.astro.rashis) if r["name"] == lagna.get("lagna_rashi")), 0)
        # Simplified

        # 10. Sarala Yoga (Rahu in 8th)
        if grah_pos.get("Rahu", {}).get("bhav") == 8:
            all_yogas.append({"name": "Sarala Yoga", "hindi": "सरल योग", "type": "Auspicious", "description": "Rahu in 8th — longevity", "strength": "Medium"})

        return all_yogas

    # ═══════════════════════════════════════════
    # 4. 20+ DOSHAS (Detailed)
    # ═══════════════════════════════════════════
    def detect_all_doshas(self, dob: str, tob: str, place: str) -> List[Dict]:
        """Detect 20+ Doshas"""
        base_doshas = self.astro.detect_doshas(dob, tob, place)
        grah_pos = self.astro.calculate_grah_positions(dob, tob, place)
        all_doshas = list(base_doshas)

        # Additional doshas
        # 1. Kaal Sarp (already in base)
        # 2. Shrapit Dosha (Shani + Rahu together)
        if grah_pos.get("Shani", {}).get("bhav") == grah_pos.get("Rahu", {}).get("bhav"):
            all_doshas.append({"name": "Shrapit Dosha", "hindi": "श्रापित दोष", "severity": "High", "description": "Shani + Rahu — ancestral curse", "remedy": "Shani mantra, Rahu mantra, pitru pooja", "affected_areas": ["Ancestral", "Health", "Obstacles"]})

        # 3. Kemdrum Dosha (no planets around Chandra)
        chandra_bhav = grah_pos.get("Chandra", {}).get("bhav", 0)
        bhav2 = (chandra_bhav % 12) + 1
        bhav12 = ((chandra_bhav - 2) % 12) + 1
        has_around = any(info.get("bhav") in [bhav2, bhav12] for p, info in grah_pos.items() if p not in ["Chandra", "Surya"])
        if not has_around:
            all_doshas.append({"name": "Kemdrum Dosha", "hindi": "केमद्रुम दोष", "severity": "Medium", "description": "No planets around Chandra — mental stress", "remedy": "Chandra mantra, silver", "affected_areas": ["Mental", "Emotions", "Mother"]})

        # 4. Pap Kartari (malefics in 2nd and 12th from Lagna)
        # Simplified

        # 5. Grahan Dosha (already in base)

        # 6. Guru Chandal (already in base)

        # 7. Shani Dosha (already in base)

        # 8. Mangal Dosha (already in base)

        # 9. Pitru Dosha (9th house afflicted)
        if grah_pos.get("Surya", {}).get("bhav") == 9 or grah_pos.get("Rahu", {}).get("bhav") == 9:
            all_doshas.append({"name": "Pitru Dosha", "hindi": "पितृ दोष", "severity": "Medium", "description": "9th house afflicted — ancestral issues", "remedy": "Pitru pooja, Shraddha, Tarpan", "affected_areas": ["Father", "Luck", "Ancestors"]})

        # 10. Nadi Dosha (for marriage)
        # Simplified

        # 11. Shani Sade Sati (already in Sadesati)

        # 12. Ashtama Shani (Shani in 8th)
        if grah_pos.get("Shani", {}).get("bhav") == 8:
            all_doshas.append({"name": "Ashtama Shani", "hindi": "अष्टम शनि", "severity": "High", "description": "Shani in 8th — health issues", "remedy": "Shani mantra, Hanuman Chalisa", "affected_areas": ["Health", "Longevity", "Obstacles"]})

        # 13. Kantaka Shani (Shani in 4th)
        if grah_pos.get("Shani", {}).get("bhav") == 4:
            all_doshas.append({"name": "Kantaka Shani", "hindi": "कंटक शनि", "severity": "Medium", "description": "Shani in 4th — domestic issues", "remedy": "Shani mantra, Shani pooja", "affected_areas": ["Home", "Mother", "Peace"]})

        # 14. Ardha Ashtama Shani (Shani in 7th)
        if grah_pos.get("Shani", {}).get("bhav") == 7:
            all_doshas.append({"name": "Ardha Ashtama Shani", "hindi": "अर्ध अष्टम शनि", "severity": "Medium", "description": "Shani in 7th — marriage delays", "remedy": "Shani mantra", "affected_areas": ["Marriage", "Partnership"]})

        return all_doshas

    # ═══════════════════════════════════════════
    # 5. 5-LEVEL DASHA
    # ═══════════════════════════════════════════
    def dasha_5_level(self, dob: str) -> Dict:
        """5-level Dasha: Maha → Antar → Pratyantar → Sookshma → Prana"""
        dasha = self.astro.vimshottari_dasha_detailed(dob)
        if "error" in dasha:
            return dasha

        # Get current MD, AD, PD
        current_md = dasha.get("current_mahadasha", {})
        current_ad = dasha.get("current_antardasha", {})
        current_pd = dasha.get("current_pratyantardasha", {})

        # Generate Sookshma and Prana (simplified)
        dasha_order = [("Ketu", 7), ("Shukra", 20), ("Surya", 6), ("Chandra", 10), ("Mangal", 7), ("Rahu", 18), ("Guru", 16), ("Shani", 19), ("Budh", 17)]

        # Sookshma from Pratyantar
        sookshma = []
        if current_pd:
            pd_planet = current_pd.get("planet", "")
            pd_duration = current_pd.get("duration_years", 1)
            pd_idx = next((i for i, (p, d) in enumerate(dasha_order) if p == pd_planet), 0)
            total = 0
            for i in range(9):
                idx = (pd_idx + i) % 9
                p, d = dasha_order[idx]
                duration = (pd_duration * d) / 120
                sookshma.append({"planet": p, "hindi": self.astro.planets.get(p, {}).get("hindi", p), "duration_years": round(duration, 3)})

        # Prana from Sookshma (first one)
        prana = []
        if sookshma:
            sk_planet = sookshma[0]["planet"]
            sk_duration = sookshma[0]["duration_years"]
            sk_idx = next((i for i, (p, d) in enumerate(dasha_order) if p == sk_planet), 0)
            for i in range(9):
                idx = (sk_idx + i) % 9
                p, d = dasha_order[idx]
                duration = (sk_duration * d) / 120
                prana.append({"planet": p, "hindi": self.astro.planets.get(p, {}).get("hindi", p), "duration_years": round(duration, 4)})

        return {
            "mahadasha": current_md,
            "antardasha": current_ad,
            "pratyantardasha": current_pd,
            "sookshma": sookshma,
            "prana": prana
        }

    # ═══════════════════════════════════════════
    # 6. TRANSIT (Gochar)
    # ═══════════════════════════════════════════
    def transit_gochar(self, dob: str, tob: str, place: str) -> Dict:
        """Current planetary transits"""
        now = datetime.now()
        transit_dob = now.strftime("%Y-%m-%d")
        transit_positions = self.astro.calculate_grah_positions(transit_dob, "12:00", "Delhi")

        # Natal positions
        natal_positions = self.astro.calculate_grah_positions(dob, tob, place)
        lagna = self.astro.calculate_lagna(dob, tob, place)
        lagna_rashi = lagna.get("lagna_rashi", "Mesh")

        transits = {}
        for planet, info in transit_positions.items():
            natal = natal_positions.get(planet, {})
            transit_rashi = info.get("rashi", "")
            natal_rashi = natal.get("rashi", "")
            transit_bhav = info.get("bhav", 0)
            natal_bhav = natal.get("bhav", 0)

            transits[planet] = {
                "planet": planet,
                "hindi": info.get("hindi", planet),
                "transit_rashi": transit_rashi,
                "transit_rashi_hindi": info.get("rashi_hindi", ""),
                "transit_bhav": transit_bhav,
                "natal_rashi": natal_rashi,
                "natal_bhav": natal_bhav,
                "same_rashi": transit_rashi == natal_rashi,
                "note": "Same as natal" if transit_rashi == natal_rashi else "Different from natal"
            }

        return {
            "transit_date": transit_dob,
            "lagna_rashi": lagna_rashi,
            "transits": transits
        }

    # ═══════════════════════════════════════════
    # 7. LIFE PREDICTIONS
    # ═══════════════════════════════════════════
    def life_predictions(self, dob: str, tob: str, place: str) -> Dict:
        """Career, Marriage, Health, Wealth predictions"""
        grah_pos = self.astro.calculate_grah_positions(dob, tob, place)
        dasha = self.astro.vimshottari_dasha_detailed(dob)
        if "error" in grah_pos:
            return grah_pos

        # Career (10th bhav)
        career_planets = [p for p, info in grah_pos.items() if info.get("bhav") == 10]
        career_score = 70 + len(career_planets) * 10

        # Marriage (7th bhav)
        marriage_planets = [p for p, info in grah_pos.items() if info.get("bhav") == 7]
        marriage_score = 70 + len(marriage_planets) * 10

        # Health (1st, 6th bhav)
        health_planets = [p for p, info in grah_pos.items() if info.get("bhav") in [1, 6]]
        health_score = 80 - len(health_planets) * 5

        # Wealth (2nd, 11th bhav)
        wealth_planets = [p for p, info in grah_pos.items() if info.get("bhav") in [2, 11]]
        wealth_score = 70 + len(wealth_planets) * 10

        # Children (5th bhav)
        children_planets = [p for p, info in grah_pos.items() if info.get("bhav") == 5]
        children_score = 70 + len(children_planets) * 10

        current_md = dasha.get("current_mahadasha", {})
        md_planet = current_md.get("planet", "")

        return {
            "career": {
                "score": min(100, career_score),
                "grade": self._prediction_grade(career_score),
                "planets_in_10th": career_planets,
                "prediction": f"10th bhav mein {len(career_planets)} planets — {'strong' if career_score >= 80 else 'moderate'} career",
                "current_dasha_effect": f"{md_planet} Mahadasha mein career {'growth' if md_planet in ['Guru', 'Shukra', 'Budh'] else 'challenges'}"
            },
            "marriage": {
                "score": min(100, marriage_score),
                "grade": self._prediction_grade(marriage_score),
                "planets_in_7th": marriage_planets,
                "prediction": f"7th bhav mein {len(marriage_planets)} planets — {'early' if marriage_score >= 80 else 'delayed'} marriage",
                "current_dasha_effect": f"{md_planet} Mahadasha mein marriage {'favorable' if md_planet in ['Guru', 'Shukra'] else 'needs patience'}"
            },
            "health": {
                "score": min(100, health_score),
                "grade": self._prediction_grade(health_score),
                "planets_in_1_6": health_planets,
                "prediction": f"1st/6th bhav mein {len(health_planets)} planets — {'good' if health_score >= 75 else 'moderate'} health",
                "current_dasha_effect": f"{md_planet} Mahadasha mein health {'good' if md_planet in ['Guru', 'Shukra', 'Budh', 'Chandra'] else 'needs care'}"
            },
            "wealth": {
                "score": min(100, wealth_score),
                "grade": self._prediction_grade(wealth_score),
                "planets_in_2_11": wealth_planets,
                "prediction": f"2nd/11th bhav mein {len(wealth_planets)} planets — {'strong' if wealth_score >= 80 else 'moderate'} wealth",
                "current_dasha_effect": f"{md_planet} Mahadasha mein wealth {'growth' if md_planet in ['Guru', 'Shukra'] else 'stable'}"
            },
            "children": {
                "score": min(100, children_score),
                "grade": self._prediction_grade(children_score),
                "planets_in_5th": children_planets,
                "prediction": f"5th bhav mein {len(children_planets)} planets — {'good' if children_score >= 80 else 'moderate'} progeny",
                "current_dasha_effect": f"{md_planet} Mahadasha mein children {'favorable' if md_planet in ['Guru', 'Chandra'] else 'stable'}"
            }
        }

    def _prediction_grade(self, score: float) -> str:
        if score >= 85: return "Excellent ✅"
        if score >= 70: return "Good ✅"
        if score >= 55: return "Average ⚠️"
        return "Needs Attention 🔴"

    # ═══════════════════════════════════════════
    # 8. NAKSHATRA DETAILED ATTRIBUTES
    # ═══════════════════════════════════════════
    def nakshatra_detailed(self, nakshatra_name: str) -> Dict:
        """Detailed Nakshatra attributes"""
        base = self.astro.nakshatra_details(nakshatra_name)
        if "error" in base:
            return base
        attrs = self.nakshatra_attributes.get(nakshatra_name, {})
        return {**base, **attrs}

    # ═══════════════════════════════════════════
    # 9. MUHURTA (Auspicious Timing)
    # ═══════════════════════════════════════════
    def muhurta(self, dob: str, tob: str, place: str) -> Dict:
        """Auspicious timing recommendations"""
        basic = self.astro.basic_details(dob, tob, place)
        vaar = basic.get("vaar", "")
        nakshatra = basic.get("nakshatra", "")
        tithi = basic.get("tithi", "")

        # Auspicious days
        auspicious_days = {
            "Somvar": ["Marriage", "New ventures", "Travel"],
            "Mangalvar": ["Property", "Construction", "Sports"],
            "Budhvar": ["Business", "Education", "Communication"],
            "Guruvar": ["Marriage", "Pooja", "Investments"],
            "Shukravar": ["Marriage", "Luxury", "Art"],
            "Shanivar": ["Long-term", "Discipline", "Service"],
            "Ravivar": ["Authority", "Government", "Health"]
        }

        return {
            "birth_vaar": vaar,
            "birth_nakshatra": nakshatra,
            "birth_tithi": tithi,
            "auspicious_activities": auspicious_days.get(vaar, []),
            "best_muhurta": {
                "marriage": "Guruvar + Shukra nakshatra",
                "business": "Budhvar + Pushya nakshatra",
                "property": "Mangalvar + Rohini nakshatra",
                "travel": "Shukravar + Hasta nakshatra",
                "pooja": "Guruvar + Punarvasu nakshatra"
            },
            "note": "Muhurta depends on multiple factors — consult astrologer for exact timing"
        }

    # ═══════════════════════════════════════════
    # 10. VASTU-ASTRO DEEP LINK
    # ═══════════════════════════════════════════
    def vastu_astro_link(self, dob: str, tob: str, place: str, main_door: str = "N") -> Dict:
        """Deep Vastu-Astro integration"""
        return self.integration.full_integration_report(dob, tob, place, main_door)

    # ═══════════════════════════════════════════
    # 11. FULL ADVANCED KUNDLI REPORT
    # ═══════════════════════════════════════════
    def full_advanced_kundli(self, dob: str, tob: str, place: str, main_door: str = "N") -> Dict:
        """Complete Advanced Kundli Report"""
        return {
            "basic": self.astro.basic_details(dob, tob, place),
            "lagna": self.astro.calculate_lagna(dob, tob, place),
            "charts": self.generate_charts(dob, tob, place),
            "grah_positions": self.astro.calculate_grah_positions(dob, tob, place),
            "aspects": self.planetary_aspects(dob, tob, place),
            "bhav_analysis": self.astro.calculate_bhav_analysis(dob, tob, place),
            "yogas": self.detect_all_yogas(dob, tob, place),
            "doshas": self.detect_all_doshas(dob, tob, place),
            "dasha_5_level": self.dasha_5_level(dob),
            "dasha_timeline": self.astro.dasha_timeline(dob),
            "transit": self.transit_gochar(dob, tob, place),
            "predictions": self.life_predictions(dob, tob, place),
            "nakshatra_attributes": self.nakshatra_attributes,
            "muhurta": self.muhurta(dob, tob, place),
            "navamsa": self.astro.calculate_navamsa(dob, tob, place),
            "ashtakavarga": self.astro.ashtakavarga(dob, tob, place),
            "shadbala": self.astro.shadbala(dob, tob, place),
            "sadesati": self.astro.sadesati(dob, tob, place),
            "remedies": self.astro.remedies(dob, tob, place),
            "vastu_astro_link": self.vastu_astro_link(dob, tob, place, main_door)
        }


if __name__ == "__main__":
    engine = AdvancedKundliEngine()
    print("=" * 60)
    print("ADVANCED KUNDLI ENGINE — Page C")
    print("=" * 60)

    report = engine.full_advanced_kundli("1990-05-04", "21:35", "Bhandara")

    print("\n1. CHARTS:")
    charts = report["charts"]
    print(f"   Lagna: {charts['lagna_hindi']} ({charts['lagna_rashi']})")
    print(f"   North Chart Bhav 1: {charts['north_chart'].get(1, {})}")
    print(f"   South Chart Mesh: {charts['south_chart'].get('Mesh', {})}")

    print("\n2. ASPECTS (Total: " + str(len(report["aspects"])) + "):")
    for a in report["aspects"][:5]:
        print(f"   {a['planet1']} - {a['planet2']}: {a['aspect_type']}")

    print("\n3. YOGAS (Total: " + str(len(report["yogas"])) + "):")
    for y in report["yogas"][:5]:
        print(f"   - {y['name']} ({y['strength']})")

    print("\n4. DOSHAS (Total: " + str(len(report["doshas"])) + "):")
    for d in report["doshas"][:5]:
        print(f"   - {d['name']} ({d['severity']})")

    print("\n5. DASHA 5-LEVEL:")
    d5 = report["dasha_5_level"]
    print(f"   MD: {d5['mahadasha'].get('planet')}")
    print(f"   AD: {d5['antardasha'].get('planet')}")
    print(f"   PD: {d5['pratyantardasha'].get('planet')}")
    print(f"   Sookshma: {d5['sookshma'][0] if d5['sookshma'] else 'N/A'}")
    print(f"   Prana: {d5['prana'][0] if d5['prana'] else 'N/A'}")

    print("\n6. TRANSIT:")
    t = report["transit"]
    print(f"   Date: {t['transit_date']}")
    for p, info in list(t["transits"].items())[:3]:
        print(f"   {p}: {info['transit_rashi']} (Bhav {info['transit_bhav']})")

    print("\n7. PREDICTIONS:")
    pred = report["predictions"]
    for area, data in pred.items():
        print(f"   {area.upper()}: {data['score']}/100 — {data['grade']}")

    print("\n✅ Advanced Kundli Engine working!")
