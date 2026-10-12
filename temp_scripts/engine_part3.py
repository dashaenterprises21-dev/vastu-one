    def __init__(self, country: str = "India"):
        self.country = country
        self.chart_data = self.COUNTRIES.get(country, {})
        self.current_year = datetime.now().year

    def analyze_deep(self) -> Dict:
        """Complete deep research analysis with 200+ data points"""
        return {
            "country": self.country,
            "chart": self.chart_data,
            "current_period": self._get_current_dasha(),
            "earthquake_prediction": self._predict_earthquake(),
            "war_prediction": self._predict_war(),
            "political_change": self._predict_political_change(),
            "death_prediction": self._predict_deaths(),
            "natural_disaster": self._predict_natural_disaster(),
            "economic_analysis": self._predict_economic(),
            "pandemic_risk": self._predict_pandemic(),
            "remedies": self._predict_remedies(),
            "stock_market": self._predict_stock_market(),
            "weather_prediction": self._predict_weather(),
            "sports_prediction": self._predict_sports(),
            "tech_prediction": self._predict_tech(),
            "major_events_2026": self._events_2026(),
            "major_events_2027": self._events_2027(),
            "major_events_2028": self._events_2028(),
            "research_references": self._research_references(),
        }

    def _get_current_dasha(self) -> Dict:
        now = datetime.now()
        try:
            birth = datetime.strptime(self.chart_data.get("date", "1947-08-15"), "%Y-%m-%d")
        except Exception:
            birth = datetime(1947, 8, 15)
        age = (now - birth).days / 365.25

        return {
            "age_years": round(age, 1),
            "current_mahadasha": self._dasha_period(age),
            "next_mahadasha": self._dasha_period(age + 5),
            "current_antardasha": self._antardasha(age),
            "critical_years": [2026, 2027, 2028],
            "rashi": self.chart_data.get("rashi", "Unknown"),
            "nakshatra": self.chart_data.get("nakshatra", "Unknown"),
        }

    def _dasha_period(self, age: float) -> str:
        dashas = [("Ketu", 7), ("Shukra", 20), ("Surya", 6), ("Chandra", 10),
                  ("Mangal", 7), ("Rahu", 18), ("Guru", 16), ("Shani", 19), ("Budh", 17)]
        cum = 0
        for planet, years in dashas:
            if cum <= age % 120 < cum + years:
                return planet
            cum += years
        return "Unknown"

    def _antardasha(self, age: float) -> str:
        """Calculate antardasha (sub-period)"""
        maha = self._dasha_period(age)
        sub_planets = ["Ketu", "Shukra", "Surya", "Chandra", "Mangal", "Rahu", "Guru", "Shani", "Budh"]
        try:
            idx = sub_planets.index(maha)
            sub_idx = int(age * 10) % 9
            return f"{maha}-{sub_planets[sub_idx]}"
        except Exception:
            return "Unknown"

    # ═══════════════════════════════════════════════════════════
    # EARTHQUAKE PREDICTION — 10 zones with exact dates
    # ═══════════════════════════════════════════════════════════
    def _predict_earthquake(self) -> Dict:
        try:
            advanced = analyze_earthquake_advanced(self.country)
            if advanced and not advanced.get("error"):
                return advanced
        except Exception as e:
            print(f"Advanced earthquake error: {e}")

        zones = self.EARTHQUAKE_ZONES.get(self.country, [])
        formatted_zones = []
        for z in zones:
            formatted_zones.append({
                "zone": z["zone"],
                "main_fault": z["fault"],
                "cities_affected": z["cities"],
                "magnitude_range": z["mag"],
                "probability": "High (70-85%)",
                "exact_dates": self._get_earthquake_dates(),
                "damage_estimate": {
                    "level": "Severe",
                    "building_damage": "50-80%",
                    "casualties": "High (1,000-10,000)",
                    "economic_loss": "$1-10 billion",
                },
                "preparedness": [
                    "Early warning systems active",
                    "Emergency response teams ready",
                    "Public awareness campaigns",
                    "Building code enforcement",
                    "Evacuation routes identified",
                ],
            })

        return {
            "country": self.country,
            "total_zones": len(formatted_zones),
            "highest_risk_zone": formatted_zones[0] if formatted_zones else {},
            "zones": formatted_zones,
            "overall_risk": {
                "score": 4.2,
                "level": "High",
                "recommendation": "Immediate preparedness required",
            },
            "next_30_days": self._next_30_days(),
            "next_6_months": self._next_6_months(),
            "classical_reference": "BPHS Ch. 45 (Bhu-Kamp Yoga), Phaladeepika Ch. 15 (Bhu-Chalan)",
        }

    def _get_earthquake_dates(self) -> List[Dict]:
        """Exact earthquake risk dates"""
        return [
            {"month": "April 2026", "dates": ["Apr 1-5 (Amavasya)", "Apr 14-17 (Purnima)", "Apr 28-30 (Eclipse)"], "reason": "Chandra + Shani alignment"},
            {"month": "May 2026", "dates": ["May 1-4 (Amavasya)", "May 13-16 (Purnima)", "May 27-30"], "reason": "Rahu-Ketu axis"},
            {"month": "August 2026", "dates": ["Aug 1-5", "Aug 14-17", "Aug 28-30"], "reason": "Shani-Chandra"},
            {"month": "November 2026", "dates": ["Nov 1-4", "Nov 13-16", "Nov 27-30"], "reason": "Shani-Chandra"},
        ]

    def _next_30_days(self) -> List[Dict]:
        return [
            {"date": "Day 1-5", "risk": "Medium", "reason": "Amavasya + Shani"},
            {"date": "Day 14-17", "risk": "High", "reason": "Purnima + Chandra"},
            {"date": "Day 28-31", "risk": "Medium", "reason": "Eclipse period"},
        ]

    def _next_6_months(self) -> List[Dict]:
        return [
            {"month": "Month 1", "risk": "Medium", "top_zone": "Gujarat"},
            {"month": "Month 2", "risk": "High", "top_zone": "Nepal Border"},
            {"month": "Month 3", "risk": "Medium", "top_zone": "Uttarakhand"},
            {"month": "Month 4", "risk": "High", "top_zone": "North-East"},
            {"month": "Month 5", "risk": "Very High", "top_zone": "Gujarat"},
            {"month": "Month 6", "risk": "High", "top_zone": "Maharashtra"},
        ]

    # ═══════════════════════════════════════════════════════════
    # WAR PREDICTION — 8 periods
    # ═══════════════════════════════════════════════════════════
    def _predict_war(self) -> Dict:
        war_risk = "Low"
        conflict_zones = []

        if self.country in ["Ukraine", "Russia", "Israel", "Iran", "Pakistan", "China", "North Korea"]:
            war_risk = "High"
            conflict_zones = ["Border areas", "Disputed territories", "Strategic zones"]
        elif self.country in ["India", "USA", "Saudi Arabia", "Turkey"]:
            war_risk = "Medium"
            conflict_zones = ["Border regions", "Strategic areas"]

        return {
            "risk_level": war_risk,
            "potential_conflicts": conflict_zones,
            "trigger_periods": [
                {"period": "2026 Feb-Apr", "reason": "Mangal-Rahu conjunction", "probability": "High"},
                {"period": "2026 May-Jul", "reason": "Mangal-Shani combination", "probability": "Medium"},
                {"period": "2026 Aug-Oct", "reason": "Shani-Rahu aspect", "probability": "Medium"},
                {"period": "2026 Nov-Dec", "reason": "Surya-Mangal", "probability": "High"},
                {"period": "2027 Jan-Mar", "reason": "Mangal-Shani", "probability": "High"},
                {"period": "2027 Apr-Jun", "reason": "Guru-Mangal", "probability": "Medium"},
                {"period": "2027 Jul-Sep", "reason": "Rahu-Ketu axis", "probability": "High"},
                {"period": "2028 Jan-Mar", "reason": "Shani-Ketu", "probability": "Medium"},
            ],
            "involved_countries": self._get_war_countries(),
            "war_type": self._get_war_type(),
            "classical_reference": "Phaladeepika Ch. 15 — Mangal-Rahu yoga = Yuddha (war)",
            "impact": {
                "economic": "High — market crash, oil prices surge, currency devaluation",
                "humanitarian": "High — refugees, casualties, displacement",
                "political": "High — government change, emergency powers",
                "social": "Medium — civil unrest, protests",
            },
        }

    def _get_war_countries(self) -> List[str]:
        mapping = {
            "Ukraine": ["Ukraine", "Russia", "NATO countries"],
            "Israel": ["Israel", "Palestine", "Iran", "Lebanon", "Syria"],
            "India": ["India", "Pakistan", "China"],
            "Taiwan": ["Taiwan", "China", "USA"],
            "Russia": ["Russia", "Ukraine", "NATO"],
            "Iran": ["Iran", "Israel", "USA", "Saudi Arabia"],
            "Pakistan": ["Pakistan", "India", "Afghanistan"],
            "China": ["China", "Taiwan", "India", "USA"],
            "North Korea": ["North Korea", "South Korea", "USA", "Japan"],
            "USA": ["USA", "China", "Russia", "Iran"],
        }
        return mapping.get(self.country, [self.country, "Neighboring countries"])

    def _get_war_type(self) -> str:
        if self.country in ["Ukraine", "Israel"]:
            return "Active military conflict"
        if self.country in ["India", "Pakistan", "China"]:
            return "Border tension, possible limited war"
        if self.country in ["USA", "Russia"]:
            return "Proxy war, economic war"
        if self.country in ["North Korea", "South Korea"]:
            return "Nuclear tension, standoff"
        return "Regional tension"
