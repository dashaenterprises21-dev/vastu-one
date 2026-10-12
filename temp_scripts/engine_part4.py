    # ═══════════════════════════════════════════════════════════
    # POLITICAL CHANGE — 12-month timeline
    # ═══════════════════════════════════════════════════════════
    def _predict_political_change(self) -> Dict:
        change_probability = "Medium"
        leadership_change = "Possible"

        if self.country in ["India", "USA", "Russia", "China"]:
            change_probability = "High"
            leadership_change = "Expected in 2026-2028"

        return {
            "change_probability": change_probability,
            "leadership_change": leadership_change,
            "type": self._get_political_type(),
            "timeline": [
                {"year": "2026 Q1", "event": "Policy shift, new alliances", "probability": "60%"},
                {"year": "2026 Q2", "event": "State elections, coalition talks", "probability": "70%"},
                {"year": "2026 Q3", "event": "Cabinet reshuffle possible", "probability": "50%"},
                {"year": "2026 Q4", "event": "Year-end political review", "probability": "80%"},
                {"year": "2027 Q1", "event": "Election preparation begins", "probability": "65%"},
                {"year": "2027 Q2", "event": "Alliance changes, new partners", "probability": "55%"},
                {"year": "2027 Q3", "event": "Major policy announcements", "probability": "70%"},
                {"year": "2027 Q4", "event": "Pre-election campaigning", "probability": "75%"},
                {"year": "2028 Q1", "event": "Election season", "probability": "85%"},
                {"year": "2028 Q2", "event": "Government formation", "probability": "80%"},
                {"year": "2028 Q3", "event": "New leadership settles", "probability": "70%"},
                {"year": "2028 Q4", "event": "Policy consolidation", "probability": "75%"},
            ],
            "key_leaders_at_risk": self._get_leaders_at_risk(),
            "coalition_math": self._get_coalition_math(),
            "classical_reference": "Bhrigu Samhita — Rahu 10th house indicates government change",
            "prediction": self._get_political_prediction(),
        }

    def _get_political_type(self) -> str:
        mapping = {
            "India": "Coalition government, state elections",
            "USA": "Presidential election 2028",
            "Russia": "Leadership transition",
            "China": "Communist Party congress",
            "UK": "General election 2029",
            "France": "Presidential 2027",
            "Germany": "Coalition government",
            "Japan": "LDP leadership",
            "Pakistan": "Military-civil balance",
            "Israel": "Coalition instability",
        }
        return mapping.get(self.country, "General political evolution")

    def _get_leaders_at_risk(self) -> List[Dict]:
        return [
            {"type": "Elderly political leaders", "risk": "Health issues", "period": "2026-2027", "probability": "High"},
            {"type": "Controversial leaders", "risk": "Scandal, legal issues", "period": "2026", "probability": "Medium"},
            {"type": "Military leaders", "risk": "Conflict-related", "period": "2026-2027", "probability": "High"},
            {"type": "Opposition leaders", "risk": "Legal challenges", "period": "2026-2028", "probability": "Medium"},
            {"type": "Regional leaders", "risk": "Corruption charges", "period": "2026-2027", "probability": "Medium"},
        ]

    def _get_coalition_math(self) -> Dict:
        if self.country == "India":
            return {
                "current_alliance": "NDA",
                "projected_2026": "NDA 280-300, INDIA 180-200",
                "projected_2028": "NDA 260-290, INDIA 200-230",
                "kingmaker": "Regional parties (TMC, DMK, BSP, SP)",
            }
        return {"projected": "Coalition likely"}

    def _get_political_prediction(self) -> str:
        return "2026-2028 mein major political changes expected. Rahu-Shani combination active hai — leadership instability, scandals, aur coalition politics."

    # ═══════════════════════════════════════════════════════════
    # DEATH PREDICTION — 8 categories
    # ═══════════════════════════════════════════════════════════
    def _predict_deaths(self) -> Dict:
        return {
            "risk_level": "Medium",
            "categories": [
                {"category": "Elderly political leaders", "risk": "High", "period": "2026-2027", "probability": "60%"},
                {"category": "Military personnel", "risk": "High", "period": "2026 (conflict zones)", "probability": "70%"},
                {"category": "Entertainment celebrities", "risk": "Medium", "period": "2026-2027", "probability": "40%"},
                {"category": "Business leaders", "risk": "Medium", "period": "2026-2028", "probability": "35%"},
                {"category": "Spiritual leaders", "risk": "Medium", "period": "2026-2027", "probability": "45%"},
                {"category": "Sports personalities", "risk": "Low", "period": "2026-2028", "probability": "25%"},
                {"category": "Journalists", "risk": "Medium", "period": "2026-2027", "probability": "30%"},
                {"category": "Judges/legal figures", "risk": "Low", "period": "2026-2028", "probability": "20%"},
            ],
            "triggers": [
                "Shani-Mangal on 1st house of country chart",
                "Rahu-Surya eclipse on leader's chart",
                "Ketu 8th house activation",
                "Ashtama Shani (Saturn in 8th)",
            ],
            "ethical_note": "Hum kisi specific person ka naam nahi le sakte. Yeh general astrological patterns hain.",
            "classical_reference": "BPHS Ch. 8 — Ashtama Shani indicates death of leaders",
        }

    # ═══════════════════════════════════════════════════════════
    # NATURAL DISASTER — 12 types
    # ═══════════════════════════════════════════════════════════
    def _predict_natural_disaster(self) -> Dict:
        return {
            "flood_risk": {
                "level": "High" if self.country in ["India", "Bangladesh", "China"] else "Medium",
                "areas": self._get_flood_areas(),
                "period": "2026 Jun-Sep (Monsoon)",
                "historical": "2024 Kerala, 2023 Himachal",
                "classical_reference": "Phaladeepika — Chandra-Mangal yoga = flood",
            },
            "cyclone_risk": {
                "level": "High" if self.country in ["India", "USA", "Japan", "Philippines", "Bangladesh"] else "Low",
                "areas": self._get_cyclone_areas(),
                "period": "2026 Apr-Jun, Oct-Dec",
                "historical": "2024 Cyclone Remal, 2023 Biparjoy",
            },
            "drought_risk": {
                "level": "Medium",
                "areas": self._get_drought_areas(),
                "period": "2026 Summer",
                "historical": "2015-16 drought",
            },
            "heatwave_risk": {
                "level": "High" if self.country in ["India", "Pakistan"] else "Medium",
                "areas": ["Central regions", "Northern plains"],
                "period": "2026 May-June",
                "historical": "2024 Delhi 50°C",
            },
            "landslide_risk": {
                "level": "High" if self.country in ["India", "Nepal", "China", "Japan"] else "Medium",
                "areas": ["Himalayan region", "Western Ghats"],
                "period": "2026 Jul-Sep",
            },
            "tsunami_risk": {
                "level": "Medium" if self.country in ["Japan", "India", "USA", "Indonesia"] else "Low",
                "areas": ["Coastal areas"],
                "period": "2026 (if earthquake >7.5)",
            },
            "wildfire_risk": {
                "level": "High" if self.country in ["USA", "Australia", "Brazil"] else "Medium",
                "areas": ["California", "Australia bushland", "Amazon"],
                "period": "2026 Jun-Sep",
            },
            "volcanic_risk": {
                "level": "Low",
                "areas": ["Japan", "Indonesia", "Iceland"],
                "period": "2026 (ongoing monitoring)",
            },
            "avalanche_risk": {
                "level": "High" if self.country in ["India", "Nepal"] else "Low",
                "areas": ["Himalayan region"],
                "period": "2026 Dec-2027 Feb",
            },
            "storm_risk": {
                "level": "Medium",
                "areas": ["Coastal regions"],
                "period": "2026 (monsoon season)",
            },
            "cold_wave_risk": {
                "level": "Medium",
                "areas": ["Northern regions"],
                "period": "2026 Dec-2027 Jan",
            },
            "dust_storm_risk": {
                "level": "Low",
                "areas": ["Rajasthan", "Middle East"],
                "period": "2026 May-June",
            },
        }

    def _get_flood_areas(self) -> List[str]:
        mapping = {
            "India": ["Mumbai", "Kerala", "Assam", "Bihar", "Chennai", "Uttarakhand"],
            "Bangladesh": ["Dhaka", "Chittagong", "Sylhet"],
            "China": ["Yangtze basin", "Guangdong"],
            "USA": ["Florida", "Louisiana", "Texas"],
        }
        return mapping.get(self.country, ["Coastal areas", "River basins"])

    def _get_cyclone_areas(self) -> List[str]:
        mapping = {
            "India": ["Odisha", "Andhra Pradesh", "West Bengal", "Gujarat"],
            "USA": ["Florida", "Louisiana", "Texas", "East Coast"],
            "Japan": ["Okinawa", "Kyushu", "Shikoku"],
            "Philippines": ["Luzon", "Visayas", "Mindanao"],
        }
        return mapping.get(self.country, ["Coastal regions"])

    def _get_drought_areas(self) -> List[str]:
        mapping = {
            "India": ["Marathwada", "Vidarbha", "Rajasthan", "Gujarat"],
            "USA": ["California", "Nevada", "Arizona"],
            "Australia": ["New South Wales", "Queensland"],
        }
        return mapping.get(self.country, ["Dry regions"])
