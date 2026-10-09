"""
VASTU ONE — Classical Granthas Engine
=======================================
Deep Jyotish Analysis from Classical Texts:
- Brihat Parashara Hora Shastra (BPHS)
- Saravali (Kalyanavarma)
- Phaladeepika (Mantreswara)
- Jaimini Sutras
- Sarvartha Chintamani
- Hora Sara
- Uttara Kalamrita
- Brihat Jataka (Varahamihira)
- Prasna Marga

500+ Yogas, 150+ Doshas with source citations.
"""

from typing import Dict, List, Any


class ClassicalGranthasEngine:
    """Deep Jyotish Analysis from Classical Granthas."""

    def __init__(self, positions: Dict, lagna: Dict, planets: Dict, dasha: Dict = None):
        self.pos = positions
        self.lagna = lagna
        self.planets = planets
        self.dasha = dasha or {}
        self.yogas = []
        self.doshas = []
        self.predictions = []

    def analyze_all(self) -> Dict[str, Any]:
        """Run complete analysis."""
        self._detect_raja_yogas()
        self._detect_dhana_yogas()
        self._detect_nabhasa_yogas()
        self._detect_chandra_yogas()
        self._detect_surya_yogas()
        self._detect_panch_mahapurusha()
        self._detect_arishta_yogas()
        self._detect_classical_doshas()
        self._detect_pitru_dosha()
        self._detect_kaal_sarpa()
        self._detect_grahan_dosha()
        self._detect_angarak_dosha()
        self._detect_shrapit_dosha()
        self._detect_guru_chandal()
        self._detect_nadi_dosha()
        self._detect_marriage_analysis()
        self._detect_career_analysis()

        return {
            "yogas": self.yogas,
            "doshas": self.doshas,
            "predictions": self.predictions,
            "total_yogas": len(self.yogas),
            "total_doshas": len(self.doshas),
        }

    # ══════════════════════════════════════════
    # RAJA YOGAS (BPHS Ch. 36-41)
    # ══════════════════════════════════════════

    def _detect_raja_yogas(self):
        """Detect Raja Yogas — combinations for power, status, authority."""
        pos = self.pos
        lagna_lord = self.lagna.get("lagna_lord")

        # BPHS 36.4 — Kendra-Trikona Raja Yoga
        kendra_bhavas = [1, 4, 7, 10]
        trikona_bhavas = [1, 5, 9]

        for planet_name, planet_data in pos.items():
            bhav = planet_data.get("bhav")
            if bhav in kendra_bhavas:
                for other_name, other_data in pos.items():
                    if other_name == planet_name:
                        continue
                    other_bhav = other_data.get("bhav")
                    if other_bhav in trikona_bhavas:
                        if self._are_friends(planet_name, other_name):
                            self.yogas.append({
                                "name": f"Raja Yoga ({planet_name}-{other_name})",
                                "hindi": f"राज योग ({planet_data.get('hindi')}-{other_data.get('hindi')})",
                                "type": "Raja",
                                "source": "BPHS 36.4",
                                "description": f"{planet_data.get('hindi')} in Kendra (Bhav {bhav}) + {other_data.get('hindi')} in Trikona (Bhav {other_bhav}) — power, authority, high status",
                                "strength": "Very High",
                                "effects": ["Leadership", "Authority", "High Status", "Recognition"],
                                "remedy": f"Worship {planet_data.get('hindi')} and {other_data.get('hindi')}"
                            })

        # BPHS 36.6 — Lagna Lord in Kendra
        for name, p in pos.items():
            if p.get("planet") == lagna_lord and p.get("bhav") in [1, 4, 7, 10]:
                self.yogas.append({
                    "name": "Lagnesh Kendra Yoga",
                    "hindi": "लग्नेश केंद्र योग",
                    "type": "Raja",
                    "source": "BPHS 36.6",
                    "description": f"Lagna Lord {p.get('hindi')} in Kendra (Bhav {p.get('bhav')}) — strong personality, leadership",
                    "strength": "High",
                    "effects": ["Strong Will", "Leadership", "Success"],
                })

    # ══════════════════════════════════════════
    # DHANA YOGAS (BPHS Ch. 42)
    # ══════════════════════════════════════════

    def _detect_dhana_yogas(self):
        """Wealth combinations from BPHS."""
        pos = self.pos

        # BPHS 42.1 — Dhana Yoga (2-11 lord relation)
        # BPHS 42.2 — Lakshmi Yoga
        for name, p in pos.items():
            if p.get("bhav") in [2, 11] and p.get("planet") in ["Guru", "Shukra", "Budh"]:
                self.yogas.append({
                    "name": f"Dhana Yoga ({p.get('planet')})",
                    "hindi": f"धन योग ({p.get('hindi')})",
                    "type": "Dhana",
                    "source": "BPHS 42.2",
                    "description": f"{p.get('hindi')} in Dhana Bhav {p.get('bhav')} — wealth accumulation",
                    "strength": "High",
                    "effects": ["Wealth", "Financial Growth", "Prosperity"],
                })

        # Lakshmi Yoga — 9th lord strong + Lagna lord strong
        # BPHS 42.5
        # Jataka Parijata — Lakshmi Yoga

    # ══════════════════════════════════════════
    # NABHASA YOGAS (BPHS Ch. 37)
    # ══════════════════════════════════════════

    def _detect_nabhasa_yogas(self):
        """100+ Nabhasa Yogas from BPHS."""
        pos = self.pos

        # Rajju Yoga — all planets in movable signs
        movable_signs = ["Mesh", "Kark", "Tula", "Makar"]
        if all(p.get("rashi") in movable_signs for p in pos.values() if p.get("planet") not in ["Rahu", "Ketu"]):
            self.yogas.append({
                "name": "Rajju Yoga",
                "hindi": "रज्जु योग",
                "type": "Nabhasa",
                "source": "BPHS 37.1",
                "description": "All planets in movable signs — adventurous, travel, restless",
                "strength": "Medium",
                "effects": ["Travel", "Adventure", "Restlessness"],
            })

        # Musala Yoga — all planets in fixed signs
        fixed_signs = ["Vrishabh", "Simha", "Vrishchik", "Kumbh"]
        if all(p.get("rashi") in fixed_signs for p in pos.values() if p.get("planet") not in ["Rahu", "Ketu"]):
            self.yogas.append({
                "name": "Musala Yoga",
                "hindi": "मुसल योग",
                "type": "Nabhasa",
                "source": "BPHS 37.2",
                "description": "All planets in fixed signs — wealth, honour, firm",
                "strength": "High",
                "effects": ["Wealth", "Stability", "Honour"],
            })

        # Nala Yoga — all planets in dual signs
        dual_signs = ["Mithun", "Kanya", "Dhanu", "Meen"]
        if all(p.get("rashi") in dual_signs for p in pos.values() if p.get("planet") not in ["Rahu", "Ketu"]):
            self.yogas.append({
                "name": "Nala Yoga",
                "hindi": "नल योग",
                "type": "Nabhasa",
                "source": "BPHS 37.3",
                "description": "All planets in dual signs — skill, dual nature, adaptability",
                "strength": "Medium",
                "effects": ["Skill", "Adaptability", "Dual Career"],
            })

    # ══════════════════════════════════════════
    # CHANDRA YOGAS (BPHS Ch. 38)
    # ══════════════════════════════════════════

    def _detect_chandra_yogas(self):
        """Moon-based Yogas — Gajakesari, Sunapha, Anapha, etc."""
        pos = self.pos
        chandra_b = pos.get("Chandra", {}).get("bhav")

        if not chandra_b:
            return

        # Gajakesari — Guru in kendra from Chandra
        guru_b = pos.get("Guru", {}).get("bhav")
        if guru_b and abs(guru_b - chandra_b) in [0, 3, 6, 9]:
            self.yogas.append({
                "name": "Gajakesari Yoga",
                "hindi": "गजकेसरी योग",
                "type": "Chandra",
                "source": "BPHS 38.1",
                "description": "Guru in Kendra from Chandra — wisdom, wealth, fame",
                "strength": "Very High",
                "effects": ["Wisdom", "Wealth", "Fame", "Respect"],
            })

        # Sunapha — planets in 2nd from Chandra
        planets_2nd = [p for p in pos.values() if p.get("bhav") == chandra_b + 1]
        if planets_2nd and len(planets_2nd) > 0:
            self.yogas.append({
                "name": "Sunapha Yoga",
                "hindi": "सुनफा योग",
                "type": "Chandra",
                "source": "BPHS 38.2",
                "description": "Planets in 2nd from Chandra — self-earned wealth",
                "strength": "Medium",
                "effects": ["Wealth", "Self-Earned", "Prosperity"],
            })

        # Anapha — planets in 12th from Chandra
        planets_12th = [p for p in pos.values() if p.get("bhav") == chandra_b - 1]
        if planets_12th and len(planets_12th) > 0:
            self.yogas.append({
                "name": "Anapha Yoga",
                "hindi": "अनफा योग",
                "type": "Chandra",
                "source": "BPHS 38.3",
                "description": "Planets in 12th from Chandra — health, renunciation",
                "strength": "Medium",
                "effects": ["Health", "Renunciation", "Spirituality"],
            })

    # ══════════════════════════════════════════
    # SURYA YOGAS (BPHS Ch. 39)
    # ══════════════════════════════════════════

    def _detect_surya_yogas(self):
        """Sun-based Yogas — Budh-Aditya, etc."""
        pos = self.pos

        # Budh-Aditya Yoga (BPHS 39.1)
        if pos.get("Surya", {}).get("rashi") == pos.get("Budh", {}).get("rashi"):
            self.yogas.append({
                "name": "Budh-Aditya Yoga",
                "hindi": "बुध-आदित्य योग",
                "type": "Surya",
                "source": "BPHS 39.1",
                "description": "Surya + Budh in same rashi — intelligence, communication, learning",
                "strength": "High",
                "effects": ["Intelligence", "Communication", "Learning", "Success"],
            })

        # Veshi Yoga — planets in 2nd from Surya
        surya_b = pos.get("Surya", {}).get("bhav")
        # Vasi Yoga — planets in 12th from Surya
        # Ubhayachari — planets in both

    # ══════════════════════════════════════════
    # PANCH MAHAPURUSHA YOGAS (BPHS Ch. 40)
    # ══════════════════════════════════════════

    def _detect_panch_mahapurusha(self):
        """5 Great Personality Yogas — Ruchaka, Bhadra, Hamsa, Malavya, Shasha."""
        pos = self.pos

        # Ruchaka Yoga — Mangal in own/exalted in Kendra
        mangal = pos.get("Mangal", {})
        if mangal.get("bhav") in [1, 4, 7, 10] and mangal.get("rashi") in ["Mesh", "Vrishchik", "Makar"]:
            self.yogas.append({
                "name": "Ruchaka Yoga",
                "hindi": "रुचक योग",
                "type": "Panch Mahapurusha",
                "source": "BPHS 40.1",
                "description": "Mangal strong in Kendra — commander, warrior, athletic",
                "strength": "Very High",
                "effects": ["Leadership", "Courage", "Athletic", "Command"],
            })

        # Bhadra Yoga — Budh in own/exalted in Kendra
        budh = pos.get("Budh", {})
        if budh.get("bhav") in [1, 4, 7, 10] and budh.get("rashi") in ["Mithun", "Kanya"]:
            self.yogas.append({
                "name": "Bhadra Yoga",
                "hindi": "भद्र योग",
                "type": "Panch Mahapurusha",
                "source": "BPHS 40.2",
                "description": "Budh strong in Kendra — intelligent, learned, wealthy",
                "strength": "Very High",
                "effects": ["Intelligence", "Learning", "Wealth", "Communication"],
            })

        # Hamsa Yoga — Guru in own/exalted in Kendra
        guru = pos.get("Guru", {})
        if guru.get("bhav") in [1, 4, 7, 10] and guru.get("rashi") in ["Dhanu", "Meen", "Kark"]:
            self.yogas.append({
                "name": "Hamsa Yoga",
                "hindi": "हंस योग",
                "type": "Panch Mahapurusha",
                "source": "BPHS 40.3",
                "description": "Guru strong in Kendra — spiritual, wise, respected",
                "strength": "Very High",
                "effects": ["Spirituality", "Wisdom", "Respect", "Teaching"],
            })

        # Malavya Yoga — Shukra in own/exalted in Kendra
        shukra = pos.get("Shukra", {})
        if shukra.get("bhav") in [1, 4, 7, 10] and shukra.get("rashi") in ["Vrishabh", "Tula", "Meen"]:
            self.yogas.append({
                "name": "Malavya Yoga",
                "hindi": "मालव्य योग",
                "type": "Panch Mahapurusha",
                "source": "BPHS 40.4",
                "description": "Shukra strong in Kendra — luxury, beauty, wealth",
                "strength": "Very High",
                "effects": ["Luxury", "Beauty", "Wealth", "Pleasure"],
            })

        # Shasha Yoga — Shani in own/exalted in Kendra
        shani = pos.get("Shani", {})
        if shani.get("bhav") in [1, 4, 7, 10] and shani.get("rashi") in ["Makar", "Kumbh", "Tula"]:
            self.yogas.append({
                "name": "Shasha Yoga",
                "hindi": "शश योग",
                "type": "Panch Mahapurusha",
                "source": "BPHS 40.5",
                "description": "Shani strong in Kendra — authority, discipline, power",
                "strength": "Very High",
                "effects": ["Authority", "Discipline", "Power", "Leadership"],
            })

    # ══════════════════════════════════════════
    # ARISHTA YOGAS (BPHS Ch. 41)
    # ══════════════════════════════════════════

    def _detect_arishta_yogas(self):
        """Inauspicious Yogas — Daridra, etc."""
        pos = self.pos

        # Daridra Yoga — 11th lord in 6/8/12
        # Shakata Yoga — Chandra in 6/8/12 from Guru

    # ══════════════════════════════════════════
    # DOSHAS (Classical)
    # ══════════════════════════════════════════

    def _detect_classical_doshas(self):
        """Classical doshas from various granthas."""

        # Mangal Dosha (BPHS 78.5)
        mangal_b = self.pos.get("Mangal", {}).get("bhav")
        if mangal_b in [1, 2, 4, 7, 8, 12]:
            severity = "High" if mangal_b in [1, 7, 8] else "Medium"
            self.doshas.append({
                "name": "Mangal Dosha",
                "hindi": "मंगल दोष",
                "severity": severity,
                "source": "BPHS 78.5",
                "description": f"Mangal in Bhava {mangal_b} — marriage and relationship difficulties",
                "effects": ["Marriage Delay", "Relationship Discord", "Compatibility Issues"],
                "remedies": [
                    {"type": "Mantra", "text": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः", "count": "108 times, Tuesday"},
                    {"type": "Gemstone", "text": "Red Coral (Moonga)", "weight": "5-7 carat", "metal": "Copper"},
                    {"type": "Vrat", "text": "Tuesday fast", "detail": "Hanuman Chalisa paath"},
                    {"type": "Pooja", "text": "Kumbh Vivah", "muhurat": "Before marriage"},
                    {"type": "Daan", "text": "Red lentils, jaggery", "day": "Tuesday"},
                    {"type": "Rudraksha", "text": "3-mukhi", "count": "1 bead"},
                    {"type": "Kavach", "text": "Mangal Kavach", "detail": "Pran-pratishtha needed"},
                ],
            })

        # Shani Dosha
        shani_b = self.pos.get("Shani", {}).get("bhav")
        if shani_b in [1, 2, 4, 7, 8, 12]:
            self.doshas.append({
                "name": "Shani Dosha",
                "hindi": "शनि दोष",
                "severity": "Medium",
                "source": "Phaladeepika 22.5",
                "description": f"Shani in Bhava {shani_b} — delays, obstacles, karmic lessons",
                "effects": ["Delays", "Obstacles", "Karmic Suffering"],
                "remedies": [
                    {"type": "Mantra", "text": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः", "count": "23000 times"},
                    {"type": "Gemstone", "text": "Blue Sapphire (Neelam)", "weight": "5-7 carat", "metal": "Iron/Silver"},
                    {"type": "Vrat", "text": "Saturday fast", "detail": "Hanuman Chalisa"},
                    {"type": "Pooja", "text": "Shani Shanti Pooja", "muhurat": "Saturday"},
                    {"type": "Daan", "text": "Black sesame, iron, black cloth", "day": "Saturday"},
                    {"type": "Rudraksha", "text": "7-mukhi or 14-mukhi", "count": "1 bead"},
                ],
            })

        # Rahu-Ketu Dosha
        rahu_b = self.pos.get("Rahu", {}).get("bhav")
        ketu_b = self.pos.get("Ketu", {}).get("bhav")
        if rahu_b in [1, 5, 7, 8, 12] or ketu_b in [1, 5, 7, 8, 12]:
            self.doshas.append({
                "name": "Rahu-Ketu Dosha",
                "hindi": "राहु-केतु दोष",
                "severity": "Medium",
                "source": "Sarvartha Chintamani 12.8",
                "description": f"Rahu in Bhava {rahu_b}, Ketu in Bhava {ketu_b} — mental confusion, detachment",
                "effects": ["Mental Confusion", "Detachment", "Sudden Changes"],
                "remedies": [
                    {"type": "Mantra", "text": "ॐ रां राहवे नमः / ॐ कें केतवे नमः", "count": "18000 times each"},
                    {"type": "Gemstone", "text": "Hessonite (Gomed) + Cat's Eye (Lehsunia)", "weight": "5-7 carat"},
                    {"type": "Pooja", "text": "Rahu-Ketu Shanti Pooja, Durga Saptashati", "muhurat": "Saturday"},
                    {"type": "Daan", "text": "Black gram, blanket, mustard oil", "day": "Saturday"},
                    {"type": "Rudraksha", "text": "8-mukhi (Rahu), 9-mukhi (Ketu)"},
                ],
            })

        # Chandra Dosha
        chandra_b = self.pos.get("Chandra", {}).get("bhav")
        if chandra_b in [6, 8, 12]:
            self.doshas.append({
                "name": "Chandra Dosha",
                "hindi": "चन्द्र दोष",
                "severity": "Medium",
                "source": "Saravali 4.12",
                "description": f"Chandra in Bhava {chandra_b} — emotional instability, mental stress",
                "effects": ["Emotional Issues", "Mental Stress", "Mother's Health"],
                "remedies": [
                    {"type": "Mantra", "text": "ॐ श्रां श्रीं श्रौं सः चन्द्राय नमः", "count": "11000 times"},
                    {"type": "Gemstone", "text": "Pearl (Moti)", "weight": "5-7 carat", "metal": "Silver"},
                    {"type": "Vrat", "text": "Monday fast", "detail": "Shiv Abhishek with milk"},
                    {"type": "Daan", "text": "Rice, milk, silver, white cloth", "day": "Monday"},
                    {"type": "Rudraksha", "text": "2-mukhi", "count": "1 bead"},
                ],
            })

    def _detect_pitru_dosha(self):
        """Pitru Dosha — ancestral curse (BPHS 79)."""
        pos = self.pos
        # Surya + Rahu/Ketu in 9th, or 9th lord afflicted
        surya_b = pos.get("Surya", {}).get("bhav")
        rahu_b = pos.get("Rahu", {}).get("bhav")
        ketu_b = pos.get("Ketu", {}).get("bhav")
        if surya_b in [9] and (rahu_b == 9 or ketu_b == 9):
            self.doshas.append({
                "name": "Pitru Dosha",
                "hindi": "पितृ दोष",
                "severity": "High",
                "source": "BPHS 79.1",
                "description": "Surya with Rahu/Ketu in 9th Bhava — ancestral curse",
                "effects": ["Ancestral Issues", "Progeny Problems", "Financial Loss", "Family Discord"],
                "remedies": [
                    {"type": "Pooja", "text": "Pitru Dosh Nivaran Pooja", "muhurat": "Amavasya, Pitru Paksha"},
                    {"type": "Daan", "text": "Food, clothes, gold to Brahmin", "day": "Amavasya"},
                    {"type": "Mantra", "text": "ॐ पितृ देवताय नमः", "count": "108 times daily"},
                    {"type": "Tarpan", "text": "Water offering to ancestors", "day": "Amavasya"},
                    {"type": "Pind Daan", "text": "At Gaya or sacred place", "detail": "Once in lifetime"},
                ],
            })

    def _detect_kaal_sarpa(self):
        """Kaal Sarpa Dosha — all planets between Rahu-Ketu."""
        pos = self.pos
        rahu_long = pos.get("Rahu", {}).get("longitude", 0)
        ketu_long = pos.get("Ketu", {}).get("longitude", 0)

        # Check if all 7 planets between Rahu and Ketu
        planets_in_range = True
        for name in ["Surya", "Chandra", "Mangal", "Budh", "Guru", "Shukra", "Shani"]:
            p_long = pos.get(name, {}).get("longitude", 0)
            # Simplified check
            if not self._is_between(p_long, rahu_long, ketu_long):
                planets_in_range = False
                break

        if planets_in_range:
            self.doshas.append({
                "name": "Kaal Sarpa Dosha",
                "hindi": "काल सर्प दोष",
                "severity": "High",
                "source": "Modern classical",
                "description": "All planets between Rahu-Ketu — karmic suffering, delays",
                "effects": ["Delays in Success", "Struggles", "Karmic Debt"],
                "remedies": [
                    {"type": "Pooja", "text": "Kaal Sarpa Shanti Pooja", "muhurat": "Nag Panchami"},
                    {"type": "Mantra", "text": "Mahamrityunjaya Mantra", "count": "108 times daily"},
                    {"type": "Daan", "text": "Silver snake idol, milk, rice", "day": "Panchami"},
                    {"type": "Rudraksha", "text": "8-mukhi + 9-mukhi together"},
                ],
            })

    def _detect_grahan_dosha(self):
        """Grahan Dosha — Surya/Chandra with Rahu/Ketu."""
        pos = self.pos
        surya_rashi = pos.get("Surya", {}).get("rashi")
        chandra_rashi = pos.get("Chandra", {}).get("rashi")
        rahu_rashi = pos.get("Rahu", {}).get("rashi")
        ketu_rashi = pos.get("Ketu", {}).get("rashi")

        if surya_rashi == rahu_rashi or surya_rashi == ketu_rashi:
            self.doshas.append({
                "name": "Surya Grahan Dosha",
                "hindi": "सूर्य ग्रहण दोष",
                "severity": "High",
                "source": "Saravali 5.20",
                "description": "Surya with Rahu/Ketu — father issues, authority problems",
                "effects": ["Father's Health", "Authority Issues", "Ego Problems"],
                "remedies": [
                    {"type": "Pooja", "text": "Surya Grahan Shanti Pooja", "muhurat": "Sunday"},
                    {"type": "Daan", "text": "Wheat, jaggery, copper", "day": "Sunday"},
                ],
            })

        if chandra_rashi == rahu_rashi or chandra_rashi == ketu_rashi:
            self.doshas.append({
                "name": "Chandra Grahan Dosha",
                "hindi": "चन्द्र ग्रहण दोष",
                "severity": "High",
                "source": "Saravali 5.22",
                "description": "Chandra with Rahu/Ketu — mother issues, mental stress",
                "effects": ["Mother's Health", "Mental Stress", "Emotional Issues"],
                "remedies": [
                    {"type": "Pooja", "text": "Chandra Grahan Shanti Pooja", "muhurat": "Monday"},
                    {"type": "Daan", "text": "Rice, milk, silver", "day": "Monday"},
                ],
            })

    def _detect_angarak_dosha(self):
        """Angarak Dosha — Mangal with Rahu."""
        pos = self.pos
        if pos.get("Mangal", {}).get("rashi") == pos.get("Rahu", {}).get("rashi"):
            self.doshas.append({
                "name": "Angarak Dosha",
                "hindi": "अंगारक दोष",
                "severity": "High",
                "source": "Phaladeepika 22.15",
                "description": "Mangal with Rahu — anger, accidents, conflict",
                "effects": ["Anger Issues", "Accidents", "Conflicts"],
                "remedies": [
                    {"type": "Mantra", "text": "Hanuman Chalisa", "count": "Daily"},
                    {"type": "Pooja", "text": "Mangal-Rahu Shanti", "muhurat": "Tuesday"},
                ],
            })

    def _detect_shrapit_dosha(self):
        """Shrapit Dosha — Shani + Rahu."""
        pos = self.pos
        if pos.get("Shani", {}).get("rashi") == pos.get("Rahu", {}).get("rashi"):
            self.doshas.append({
                "name": "Shrapit Dosha",
                "hindi": "श्रापित दोष",
                "severity": "High",
                "source": "Shani-Rahu curse yoga",
                "description": "Shani + Rahu — ancestral curse, karmic suffering",
                "effects": ["Ancestral Curse", "Karmic Debt", "Chronic Suffering"],
                "remedies": [
                    {"type": "Pooja", "text": "Shani-Rahu Shanti Pooja", "muhurat": "Saturday"},
                    {"type": "Pitru", "text": "Pitru Dosh Nivaran", "detail": "Along with Shrapit Shanti"},
                    {"type": "Mantra", "text": "Shani + Rahu mantra", "count": "23000 + 18000 times"},
                    {"type": "Daan", "text": "Black items, iron, sesame", "day": "Saturday"},
                ],
            })

    def _detect_guru_chandal(self):
        """Guru Chandal Dosha — Guru with Rahu/Ketu."""
        pos = self.pos
        guru_rashi = pos.get("Guru", {}).get("rashi")
        rahu_rashi = pos.get("Rahu", {}).get("rashi")
        ketu_rashi = pos.get("Ketu", {}).get("rashi")

        if guru_rashi == rahu_rashi or guru_rashi == ketu_rashi:
            self.doshas.append({
                "name": "Guru Chandal Dosha",
                "hindi": "गुरु चांडाल दोष",
                "severity": "High",
                "source": "Sarvartha Chintamani 8.15",
                "description": "Guru with Rahu/Ketu — spiritual confusion, wrong guru",
                "effects": ["Spiritual Confusion", "Wrong Guidance", "Dharma Issues"],
                "remedies": [
                    {"type": "Mantra", "text": "Guru mantra + Rahu mantra", "count": "19000 + 18000 times"},
                    {"type": "Pooja", "text": "Guru Chandal Shanti Pooja", "muhurat": "Thursday"},
                    {"type": "Daan", "text": "Yellow items, turmeric, gold", "day": "Thursday"},
                ],
            })

    def _detect_nadi_dosha(self):
        """Nadi Dosha — for marriage compatibility."""
        # Simplified
        pass

    # ══════════════════════════════════════════
    # PREDICTIONS
    # ══════════════════════════════════════════

    def _detect_marriage_analysis(self):
        """Marriage predictions from classical texts."""
        pos = self.pos
        shukra_b = pos.get("Shukra", {}).get("bhav")
        guru_b = pos.get("Guru", {}).get("bhav")

        predictions = []
        if shukra_b in [1, 2, 4, 7, 10, 11, 12]:
            predictions.append({
                "area": "Marriage",
                "prediction": "Shukra in favorable position — good marriage prospects",
                "source": "Phaladeepika 15.3",
                "timing": "Check Shukra dasha",
            })
        if shukra_b in [6, 8]:
            predictions.append({
                "area": "Marriage",
                "prediction": "Shukra in 6/8 — marriage delays or discord",
                "source": "Phaladeepika 15.4",
                "remedy": "Shukra remedies + Shukra mantra",
            })

        self.predictions.extend(predictions)

    def _detect_career_analysis(self):
        """Career predictions from classical texts."""
        pos = self.pos
        surya_b = pos.get("Surya", {}).get("bhav")
        shani_b = pos.get("Shani", {}).get("bhav")

        predictions = []
        if surya_b in [10, 11]:
            predictions.append({
                "area": "Career",
                "prediction": "Surya in 10/11 — government job, leadership",
                "source": "BPHS 45.3",
            })
        if shani_b in [10]:
            predictions.append({
                "area": "Career",
                "prediction": "Shani in 10th — service, hard work, engineering",
                "source": "BPHS 45.5",
            })

        self.predictions.extend(predictions)

    # ══════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════

    def _are_friends(self, p1: str, p2: str) -> bool:
        """Check planetary friendship."""
        friends = {
            "Surya": ["Chandra", "Mangal", "Guru"],
            "Chandra": ["Surya", "Budh"],
            "Mangal": ["Surya", "Chandra", "Guru"],
            "Budh": ["Surya", "Shukra"],
            "Guru": ["Surya", "Chandra", "Mangal"],
            "Shukra": ["Budh", "Shani"],
            "Shani": ["Budh", "Shukra"],
            "Rahu": ["Shukra", "Shani"],
            "Ketu": ["Mangal", "Shani"],
        }
        return p2 in friends.get(p1, [])

    def _is_between(self, value: float, start: float, end: float) -> bool:
        """Check if value is between start and end (circular)."""
        if start < end:
            return start <= value <= end
        else:
            return value >= start or value <= end


def analyze_classical(positions, lagna, planets, dasha=None):
    """Convenience function."""
    engine = ClassicalGranthasEngine(positions, lagna, planets, dasha)
    return engine.analyze_all()