    # ═══════════════════════════════════════════════════════════
    # ECONOMIC — 12 sectors + stocks
    # ═══════════════════════════════════════════════════════════
    def _predict_economic(self) -> Dict:
        return {
            "market_outlook": self._get_market_outlook(),
            "recession_risk": "Medium" if self.country in ["USA", "China", "Germany"] else "Low",
            "currency": self._get_currency_prediction(),
            "sectors": {
                "technology": "Growth — AI, semiconductors, cloud",
                "energy": "Volatile — oil, gas, renewables",
                "agriculture": "Mixed — weather dependent",
                "real_estate": "Stable — long-term growth",
                "gold": "Bullish — safe haven demand",
                "banking": "Moderate — NPA concerns",
                "pharma": "Growth — aging population",
                "defense": "Strong — geopolitical tensions",
                "auto": "Mixed — EV transition",
                "textile": "Moderate — export dependent",
                "metals": "Volatile — China demand",
                "infrastructure": "Growth — government spending",
            },
            "timeline": [
                {"period": "2026 H1", "outlook": "Cautious optimism", "gdp": "6.5-7.0%"},
                {"period": "2026 H2", "outlook": "Volatility expected", "gdp": "6.0-6.5%"},
                {"period": "2027 H1", "outlook": "Recovery begins", "gdp": "6.5-7.0%"},
                {"period": "2027 H2", "outlook": "Growth momentum", "gdp": "7.0-7.5%"},
                {"period": "2028", "outlook": "Strong growth", "gdp": "7.0-8.0%"},
            ],
            "key_indicators": {
                "inflation": "Moderate (4-5%)",
                "interest_rate": "Stable to slightly down",
                "unemployment": "Stable",
                "gdp_growth": "6.5-7.5%",
            },
            "classical_reference": "BPHS Ch. 42 — Dhana Yoga predicts economic prosperity",
        }

    def _get_market_outlook(self) -> str:
        return "Positive long-term, volatile short-term. Gold and defense stocks good."

    def _get_currency_prediction(self) -> str:
        mapping = {
            "India": "Rupee — stable with slight depreciation expected",
            "USA": "Dollar — strong but volatile",
            "China": "Yuan — controlled depreciation",
            "Russia": "Ruble — volatile",
            "Japan": "Yen — weak trend",
            "UK": "Pound — stable",
            "Germany": "Euro — stable",
        }
        return mapping.get(self.country, "Stable")

    # ═══════════════════════════════════════════════════════════
    # PANDEMIC RISK — 5 risks
    # ═══════════════════════════════════════════════════════════
    def _predict_pandemic(self) -> Dict:
        return {
            "risk_level": "Low",
            "probability": "20%",
            "period": "2026-2027",
            "areas": ["Southeast Asia", "Africa", "South America"],
            "risks": [
                {"type": "Viral outbreak", "probability": "20%", "severity": "Medium"},
                {"type": "Bacterial infection", "probability": "15%", "severity": "Low"},
                {"type": "Fungal infection", "probability": "10%", "severity": "Low"},
                {"type": "Zoonotic disease", "probability": "25%", "severity": "Medium"},
                {"type": "Antibiotic-resistant", "probability": "30%", "severity": "High"},
            ],
            "triggers": [
                "Rahu-Ketu axis on 6th house",
                "Shani-Chandra combination",
                "Guru in 6th house of country chart",
            ],
            "preparedness": [
                "Vaccine stockpiling",
                "Healthcare infrastructure",
                "International cooperation",
                "Early warning systems",
            ],
            "classical_reference": "BPHS Ch. 6 — Rog Bhava (6th house) indicates disease",
        }

    # ═══════════════════════════════════════════════════════════
    # REMEDIES — 20+ upay
    # ═══════════════════════════════════════════════════════════
    def _predict_remedies(self) -> List[Dict]:
        return [
            {"risk": "Earthquake", "remedy": "Shani mantra, Hanuman Chalisa, donate black items", "planet": "Shani"},
            {"risk": "War", "remedy": "Mangal mantra, Hanuman worship, donate red items", "planet": "Mangal"},
            {"risk": "Political instability", "remedy": "Surya mantra, Aditya Hridayam, donate wheat", "planet": "Surya"},
            {"risk": "Flood", "remedy": "Chandra mantra, Shiva worship, donate milk", "planet": "Chandra"},
            {"risk": "Drought", "remedy": "Varun mantra, Jal abhishek, donate water", "planet": "Chandra"},
            {"risk": "Heatwave", "remedy": "Surya namaskar, donate jaggery, water to birds", "planet": "Surya"},
            {"risk": "Cyclone", "remedy": "Vayu mantra, Hanuman worship, donate black sesame", "planet": "Shani"},
            {"risk": "Pandemic", "remedy": "Mahamrityunjaya mantra, Ayurveda, donate medicines", "planet": "Rahu"},
            {"risk": "Economic crisis", "remedy": "Lakshmi mantra, Kubera worship, donate gold", "planet": "Guru"},
            {"risk": "Death of leaders", "remedy": "Mrityunjaya mantra, Kaal Bhairav worship", "planet": "Shani"},
            {"risk": "General protection", "remedy": "Gayatri mantra, Navagraha puja, Rudrabhishek", "planet": "All"},
            {"risk": "Mental peace", "remedy": "Vishnu Sahasranama, meditation, sattvic food", "planet": "Chandra"},
            {"risk": "Business growth", "remedy": "Ganesh worship, Kubera mantra, donate to needy", "planet": "Budh"},
            {"risk": "Health", "remedy": "Dhanvantari mantra, Ayurveda, yoga", "planet": "Surya"},
            {"risk": "Family harmony", "remedy": "Gauri-Shankar puja, donate to couples", "planet": "Shukra"},
            {"risk": "Education", "remedy": "Saraswati mantra, donate books", "planet": "Budh"},
            {"risk": "Career", "remedy": "Hanuman Chalisa, Shani mantra", "planet": "Shani"},
            {"risk": "Marriage", "remedy": "Katayayani mantra, Gauri puja", "planet": "Shukra"},
            {"risk": "Children", "remedy": "Santaan Gopal mantra, Bal Gopal puja", "planet": "Guru"},
            {"risk": "Property", "remedy": "Bhumi puja, Vastu shanti", "planet": "Mangal"},
        ]

    # ═══════════════════════════════════════════════════════════
    # STOCK MARKET — sector-wise
    # ═══════════════════════════════════════════════════════════
    def _predict_stock_market(self) -> Dict:
        return {
            "overall": "Bullish with volatility",
            "sensex_target": "85,000-90,000 (2026)",
            "nifty_target": "25,000-27,000 (2026)",
            "sectors": {
                "IT": {"outlook": "Positive", "reason": "AI boom, USD strength"},
                "Banking": {"outlook": "Moderate", "reason": "NPA concerns, credit growth"},
                "Pharma": {"outlook": "Positive", "reason": "Export growth, aging population"},
                "Defense": {"outlook": "Very Positive", "reason": "Geopolitical tensions, orders"},
                "Energy": {"outlook": "Volatile", "reason": "Oil prices, renewables transition"},
                "FMCG": {"outlook": "Stable", "reason": "Rural demand recovery"},
                "Auto": {"outlook": "Mixed", "reason": "EV transition, chip shortage"},
                "Real Estate": {"outlook": "Positive", "reason": "Affordable housing, REITs"},
                "Gold": {"outlook": "Very Positive", "reason": "Safe haven, central bank buying"},
                "Crypto": {"outlook": "Volatile", "reason": "Regulation, institutional adoption"},
            },
            "best_picks": ["Defense stocks", "IT large caps", "Gold ETFs", "Pharma"],
            "avoid": ["Speculative small caps", "Crypto (if risk-averse)"],
        }

    # ═══════════════════════════════════════════════════════════
    # WEATHER — monsoon + temperature
    # ═══════════════════════════════════════════════════════════
    def _predict_weather(self) -> Dict:
        return {
            "monsoon_2026": {
                "onset": "June 1-5",
                "withdrawal": "September 15-20",
                "rainfall": "Above normal (105-110% of LPA)",
                "regions": {
                    "North": "Normal to above",
                    "South": "Above normal",
                    "East": "Above normal",
                    "West": "Normal",
                    "Central": "Below normal",
                },
            },
            "summer_2026": {
                "temperature": "Above normal (+1-2°C)",
                "heatwave_days": "15-20 days",
                "worst_months": ["May", "June"],
            },
            "winter_2026_27": {
                "temperature": "Below normal (-1-2°C)",
                "cold_wave_days": "10-15 days",
                "worst_months": ["December", "January"],
            },
            "extreme_events": [
                {"type": "Heatwave", "probability": "80%", "period": "May-Jun 2026"},
                {"type": "Flood", "probability": "70%", "period": "Jul-Sep 2026"},
                {"type": "Cyclone", "probability": "60%", "period": "Apr-Jun, Oct-Dec 2026"},
                {"type": "Drought", "probability": "30%", "period": "Summer 2026"},
            ],
        }

    # ═══════════════════════════════════════════════════════════
    # SPORTS — cricket + Olympics
    # ═══════════════════════════════════════════════════════════
    def _predict_sports(self) -> Dict:
        return {
            "cricket": {
                "world_cup_2026": "India strong contender",
                "ipl_2026": "Mumbai Indians, CSK favorites",
                "key_players": ["Virat Kohli (farewell?)", "Rohit Sharma", "Jasprit Bumrah"],
                "emerging": ["Shubman Gill", "Yashasvi Jaiswal"],
            },
            "olympics_2028": {
                "india_medals": "15-20 expected",
                "top_sports": ["Shooting", "Wrestling", "Badminton", "Hockey"],
                "emerging": ["Archery", "Boxing", "Athletics"],
            },
            "football": {
                "world_cup_2026": "Brazil, France, Argentina favorites",
                "india": "Qualification unlikely",
            },
            "tennis": {
                "grand_slams": "Djokovic, Alcaraz, Sinner dominant",
                "india": "Doubles focus",
            },
        }

    # ═══════════════════════════════════════════════════════════
    # TECH — AI + semiconductor
    # ═══════════════════════════════════════════════════════════
    def _predict_tech(self) -> Dict:
        return {
            "ai": {
                "growth": "Exponential",
                "key_players": ["OpenAI", "Google", "Microsoft", "Meta"],
                "india_role": "AI talent hub, data center growth",
            },
            "semiconductor": {
                "growth": "Strong",
                "key_players": ["TSMC", "Samsung", "Intel", "NVIDIA"],
                "india_role": "New fab plants (Gujarat, Karnataka)",
            },
            "5g_6g": {
                "rollout": "5G mature by 2026, 6G trials 2027",
                "india_role": "Indigenous 5G stack",
            },
            "ev": {
                "growth": "Rapid",
                "key_players": ["Tesla", "BYD", "Tata", "Mahindra"],
                "india_role": "EV manufacturing hub",
            },
            "space": {
                "growth": "Strong",
                "key_players": ["SpaceX", "ISRO", "Blue Origin"],
                "india_role": "Gaganyaan, Chandrayaan follow-ups",
            },
            "quantum": {
                "growth": "Emerging",
                "india_role": "National Quantum Mission",
            },
        }
