"""
VASTU ONE — Life Prediction Engine
====================================
Deep personal life analysis based on:
- Lagna & Moon sign (personality)
- 10th house (career)
- 2nd/11th house (wealth)
- 7th house (marriage)
- 5th house (children, education)
- 4th house (property, mother)
- 9th house (luck, father, dharma)
- 12th house (foreign, moksha)

Predicts: Education, Career, Business, Marriage, Children, Location, Wealth, Dreams
"""

from typing import Dict, List, Any


class LifePredictionEngine:
    """Deep personal life prediction."""

    def __init__(self, positions: Dict, lagna: Dict, bhava_chalit: Dict, dasha: Dict = None):
        self.pos = positions
        self.lagna = lagna
        self.bhava = bhava_chalit
        self.dasha = dasha or {}
        self.predictions = {}

    def analyze_all(self) -> Dict[str, Any]:
        """Run complete life analysis."""
        return {
            "education": self._education_analysis(),
            "career": self._career_analysis(),
            "business": self._business_analysis(),
            "personal_life": self._personal_life_analysis(),
            "marriage": self._marriage_analysis(),
            "children": self._children_analysis(),
            "location": self._location_analysis(),
            "wealth": self._wealth_analysis(),
            "health": self._health_analysis(),
            "spiritual": self._spiritual_analysis(),
            "dreams": self._dreams_analysis(),
            "timing": self._timing_analysis(),
        }

    # ══════════════════════════════════════════
    # EDUCATION (5th House + Budh + Guru)
    # ══════════════════════════════════════════

    def _education_analysis(self) -> Dict[str, Any]:
        """Education field, timing, obstacles."""
        budh = self.pos.get("Budh", {})
        guru = self.pos.get("Guru", {})
        surya = self.pos.get("Surya", {})
        chandra = self.pos.get("Chandra", {})

        # Field determination
        field = "General"
        subjects = []
        if budh.get("bhav") in [1, 4, 5, 10]:
            subjects.append("Mathematics")
            subjects.append("Commerce")
        if guru.get("bhav") in [5, 9, 12]:
            subjects.append("Philosophy")
            subjects.append("Law")
            subjects.append("Teaching")
        if surya.get("bhav") in [1, 10]:
            subjects.append("Administration")
            subjects.append("Leadership")
        if chandra.get("bhav") in [4, 5]:
            subjects.append("Psychology")
            subjects.append("Arts")

        # Best field
        if guru.get("rashi") in ["Dhanu", "Meen"]:
            field = "Philosophy/Spiritual/Law"
        elif budh.get("rashi") in ["Mithun", "Kanya"]:
            field = "Commerce/Mathematics/Communication"
        elif surya.get("rashi") in ["Simha", "Mesh"]:
            field = "Administration/Leadership"
        elif chandra.get("rashi") in ["Kark", "Meen"]:
            field = "Creative Arts/Psychology"

        # Higher education abroad?
        foreign = self.pos.get("Rahu", {}).get("bhav") in [9, 12]
        higher_edu = "Abroad possible" if foreign else "India recommended"

        # Obstacles
        obstacles = []
        if self.pos.get("Shani", {}).get("bhav") in [4, 5, 9]:
            obstacles.append("Delays in education due to Shani")
        if self.pos.get("Mangal", {}).get("bhav") in [4, 5]:
            obstacles.append("Focus issues — Mangal")

        return {
            "best_field": field,
            "subjects": subjects[:5],
            "higher_education": higher_edu,
            "obstacles": obstacles or ["No major obstacles"],
            "recommendation": f"Focus on {field} — this aligns with your planetary strengths",
            "source": "BPHS Ch. 24 (Education), Phaladeepika 15"
        }

    # ══════════════════════════════════════════
    # CAREER (10th House + Surya + Shani)
    # ══════════════════════════════════════════

    def _career_analysis(self) -> Dict[str, Any]:
        """Career field, job vs business, timing."""
        surya = self.pos.get("Surya", {})
        shani = self.pos.get("Shani", {})
        mangal = self.pos.get("Mangal", {})
        guru = self.pos.get("Guru", {})

        # 10th house analysis
        career_field = "General"
        if shani.get("bhav") in [10, 6, 11]:
            career_field = "Service/Engineering/Government"
        elif surya.get("bhav") in [1, 10, 11]:
            career_field = "Administration/Leadership/Government"
        elif mangal.get("bhav") in [3, 6, 10]:
            career_field = "Army/Police/Sports/Surgery"
        elif guru.get("bhav") in [9, 10, 5]:
            career_field = "Teaching/Finance/Law/Consulting"
        elif self.pos.get("Budh", {}).get("bhav") in [3, 6, 10]:
            career_field = "IT/Communication/Commerce"
        elif self.pos.get("Shukra", {}).get("bhav") in [2, 7, 10]:
            career_field = "Business/Arts/Fashion"

        # Job vs Business
        mangal_bhav = mangal.get("bhav")
        if mangal_bhav in [3, 6, 10, 11]:
            recommendation = "Business is highly recommended"
        elif shani.get("bhav") in [6, 10, 11]:
            recommendation = "Job (service) is recommended"
        else:
            recommendation = "Mix of job + side business"

        # Timing
        maha = self.dasha.get("current_mahadasha", {})
        current_lord = maha.get("planet", "")
        timing = "Current dasha phase"
        if current_lord in ["Surya", "Mangal", "Shani"]:
            timing = "Career growth phase — good for business/expansion"

        return {
            "best_field": career_field,
            "job_vs_business": recommendation,
            "timing": timing,
            "recommendation": f"Focus on {career_field}. {recommendation}.",
            "source": "BPHS Ch. 45 (Career), Phaladeepika Ch. 15"
        }

    # ══════════════════════════════════════════
    # BUSINESS (2nd + 11th House + Budh)
    # ══════════════════════════════════════════

    def _business_analysis(self) -> Dict[str, Any]:
        """Business type, partner, location, expansion."""
        budh = self.pos.get("Budh", {})
        guru = self.pos.get("Guru", {})
        shukra = self.pos.get("Shukra", {})
        chandra = self.pos.get("Chandra", {})

        # Business type
        business_type = "Trading"
        if budh.get("rashi") in ["Mithun", "Kanya"]:
            business_type = "Trading, Communication, IT"
        elif shukra.get("rashi") in ["Vrishabh", "Tula"]:
            business_type = "Luxury, Fashion, Beauty, Real Estate"
        elif guru.get("rashi") in ["Dhanu", "Meen"]:
            business_type = "Consulting, Education, Finance"
        elif chandra.get("rashi") in ["Kark"]:
            business_type = "Food, Dairy, Hospitality"

        # Partner
        partner_recommendation = ""
        if self.pos.get("Mangal", {}).get("bhav") in [7, 2, 11]:
            partner_recommendation = "Partnership good — but choose carefully"
        elif self.pos.get("Rahu", {}).get("bhav") in [7, 2]:
            partner_recommendation = "Beware of partners — possible deception. Prefer alone."
        else:
            partner_recommendation = "Partnership or alone — both work"

        # Alone vs Partnership
        alone = "Alone is better" if self.pos.get("Rahu", {}).get("bhav") in [7, 2] else "Partnership recommended"

        # Partner nature
        partner_nature = "Similar age, business-minded"
        if self.pos.get("Shani", {}).get("bhav") in [7]:
            partner_nature = "Older partner (5-10 years) — reliable"
        elif self.pos.get("Budh", {}).get("bhav") in [7]:
            partner_nature = "Same age, intelligent, communicative"

        return {
            "best_business_type": business_type,
            "partner_or_alone": alone,
            "partner_nature": partner_nature,
            "recommendation": partner_recommendation,
            "expansion_timing": "Business expansion in Mangal/Surya dasha",
            "source": "BPHS Ch. 46 (Dhana Yoga), Phaladeepika"
        }

    # ══════════════════════════════════════════
    # PERSONAL LIFE (Lagna + Moon + Surya)
    # ══════════════════════════════════════════

    def _personal_life_analysis(self) -> Dict[str, Any]:
        """Personality, strengths, weaknesses."""
        lagna_rashi = self.lagna.get("lagna_rashi", "")
        chandra_rashi = self.pos.get("Chandra", {}).get("rashi", "")

        personality = "Balanced"
        strengths = []
        weaknesses = []

        if lagna_rashi in ["Mesh", "Simha", "Dhanu"]:
            personality = "Energetic, Leadership, Ambitious"
            strengths = ["Leadership", "Courage", "Initiative"]
            weaknesses = ["Anger", "Impatience"]
        elif lagna_rashi in ["Vrishabh", "Kanya", "Makar"]:
            personality = "Practical, Grounded, Patient"
            strengths = ["Discipline", "Hard Work", "Reliability"]
            weaknesses = ["Stubbornness", "Over-cautious"]
        elif lagna_rashi in ["Mithun", "Tula", "Kumbh"]:
            personality = "Intelligent, Social, Communicative"
            strengths = ["Communication", "Adaptability", "Networking"]
            weaknesses = ["Indecisiveness", "Restlessness"]
        elif lagna_rashi in ["Kark", "Vrishchik", "Meen"]:
            personality = "Emotional, Intuitive, Deep"
            strengths = ["Empathy", "Intuition", "Loyalty"]
            weaknesses = ["Over-sensitivity", "Mood swings"]

        return {
            "personality": personality,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendation": f"Your {personality.lower()} nature is your strength. Work on {', '.join(weaknesses).lower()}.",
            "source": "Saravali Ch. 4, BPHS Ch. 24"
        }

    # ══════════════════════════════════════════
    # MARRIAGE (7th House + Shukra)
    # ══════════════════════════════════════════

    def _marriage_analysis(self) -> Dict[str, Any]:
        """Marriage timing, partner, happiness."""
        shukra = self.pos.get("Shukra", {})
        guru = self.pos.get("Guru", {})
        mangal = self.pos.get("Mangal", {})

        # Timing based on Shukra
        shukra_bhav = shukra.get("bhav")
        timing = "25-30 years"
        if shukra_bhav in [1, 2, 4, 7, 10, 11]:
            timing = "22-28 years (early)"
        elif shukra_bhav in [6, 8, 12]:
            timing = "28-35 years (late)"

        # Love vs Arranged
        love_marriage = False
        if self.pos.get("Mangal", {}).get("bhav") in [5, 7] or self.pos.get("Rahu", {}).get("bhav") in [5, 7]:
            love_marriage = True
        marriage_type = "Love marriage possible" if love_marriage else "Arranged marriage likely"

        # Partner nature
        partner_nature = "Understanding, supportive"
        if shukra.get("rashi") in ["Vrishabh", "Tula"]:
            partner_nature = "Beautiful, artistic, luxury-loving"
        elif shukra.get("rashi") in ["Kark", "Meen"]:
            partner_nature = "Emotional, caring, homely"
        elif shukra.get("rashi") in ["Kanya", "Makar"]:
            partner_nature = "Practical, hardworking, disciplined"

        # Happiness
        happiness = "Happy married life"
        warnings = []
        if mangal.get("bhav") in [1, 2, 4, 7, 8, 12]:
            warnings.append("Mangal Dosha — needs Kumbh Vivah remedy")
            happiness = "Struggles possible — remedy needed"
        if self.pos.get("Shani", {}).get("bhav") in [7]:
            warnings.append("Shani in 7th — delays or age gap")
        if self.pos.get("Rahu", {}).get("bhav") in [7]:
            warnings.append("Rahu in 7th — foreign partner possible")

        return {
            "timing": timing,
            "marriage_type": marriage_type,
            "partner_nature": partner_nature,
            "happiness": happiness,
            "warnings": warnings or ["No major warnings"],
            "recommendation": f"Marriage at {timing}. {partner_nature}.",
            "source": "BPHS Ch. 17 (Marriage), Phaladeepika Ch. 15"
        }

    # ══════════════════════════════════════════
    # CHILDREN (5th House + Guru)
    # ══════════════════════════════════════════

    def _children_analysis(self) -> Dict[str, Any]:
        """Children count, timing, nature."""
        guru = self.pos.get("Guru", {})
        guru_bhav = guru.get("bhav")

        count = "1-2 children"
        if guru_bhav in [1, 5, 9, 11]:
            count = "2-3 children — blessed"
        elif guru_bhav in [6, 8, 12]:
            count = "1 child — possible delays"

        timing = "After marriage 2-5 years"

        nature = "Intelligent, well-behaved"
        if self.pos.get("Budh", {}).get("rashi") == guru.get("rashi"):
            nature = "Very intelligent, scholarly"

        warnings = []
        if self.pos.get("Shani", {}).get("bhav") in [5]:
            warnings.append("Shani in 5th — delays in children")
        if self.pos.get("Rahu", {}).get("bhav") in [5]:
            warnings.append("Rahu in 5th — medical support may be needed")

        return {
            "count": count,
            "timing": timing,
            "nature": nature,
            "warnings": warnings or ["No warnings"],
            "source": "BPHS Ch. 18 (Children)"
        }

    # ══════════════════════════════════════════
    # LOCATION (4th House + Rahu + 9th)
    # ══════════════════════════════════════════

    def _location_analysis(self) -> Dict[str, Any]:
        """Best city, country, direction."""
        rahu = self.pos.get("Rahu", {})
        chandra = self.pos.get("Chandra", {})
        surya = self.pos.get("Surya", {})

        # Direction
        best_direction = "North"
        if surya.get("bhav") in [1, 10]:
            best_direction = "East — for growth"
        elif chandra.get("bhav") in [4]:
            best_direction = "North — for peace"
        elif self.pos.get("Shukra", {}).get("bhav") in [7]:
            best_direction = "West — for luxury"
        elif self.pos.get("Mangal", {}).get("bhav") in [3, 6]:
            best_direction = "South — for courage"

        # Country
        country = "India"
        if rahu.get("bhav") in [9, 12] or self.pos.get("Shani", {}).get("bhav") in [12]:
            country = "Foreign country (abroad) — good for career"

        # City type
        city_type = "Medium city"
        if rahu.get("bhav") in [10] or self.pos.get("Budh", {}).get("bhav") in [10]:
            city_type = "Metro city (Mumbai, Delhi, Bangalore)"
        elif chandra.get("bhav") in [4]:
            city_type = "Home town or near family"

        return {
            "best_direction": best_direction,
            "best_country": country,
            "best_city_type": city_type,
            "recommendation": f"{country}, {city_type}, facing {best_direction}",
            "source": "BPHS Ch. 24, Jaimini Sutras"
        }

    # ══════════════════════════════════════════
    # WEALTH (2nd + 11th House + Guru)
    # ══════════════════════════════════════════

    def _wealth_analysis(self) -> Dict[str, Any]:
        """Wealth timing, source."""
        guru = self.pos.get("Guru", {})
        shukra = self.pos.get("Shukra", {})
        dhana_bhav = guru.get("bhav") in [2, 11] or shukra.get("bhav") in [2, 11]

        wealth_level = "Medium wealth"
        if guru.get("bhav") in [2, 11]:
            wealth_level = "Abundant wealth — Dhana Yoga"
        elif guru.get("bhav") in [6, 8, 12]:
            wealth_level = "Struggles then wealth"

        source = "Salary/Service"
        if shukra.get("bhav") in [2, 11]:
            source = "Business/Investment/Luxury goods"
        elif guru.get("bhav") in [2, 11]:
            source = "Consulting/Teaching/Finance"
        elif self.pos.get("Mangal", {}).get("bhav") in [2, 11]:
            source = "Real estate/Construction"

        timing = "After 30 years — Saturn maturity"
        if guru.get("bhav") in [2, 11]:
            timing = "30-45 years — Jupiter dasha"

        return {
            "wealth_level": wealth_level,
            "source": source,
            "timing": timing,
            "recommendation": f"{wealth_level} through {source}. Peak: {timing}.",
            "source_text": "BPHS Ch. 42 (Dhana Yogas)"
        }

    # ══════════════════════════════════════════
    # HEALTH (6th House + Lagna)
    # ══════════════════════════════════════════

    def _health_analysis(self) -> Dict[str, Any]:
        """Weak organs, health issues, prevention."""
        shani = self.pos.get("Shani", {})
        mangal = self.pos.get("Mangal", {})
        rahu = self.pos.get("Rahu", {})
        ketu = self.pos.get("Ketu", {})

        weak_organs = []
        preventions = []

        if shani.get("bhav") in [1, 6, 8]:
            weak_organs.append("Bones, joints, teeth")
            preventions.append("Regular calcium, Vitamin D, yoga")
        if mangal.get("bhav") in [1, 6, 8]:
            weak_organs.append("Blood, liver, injuries")
            preventions.append("Avoid red meat, anger control")
        if rahu.get("bhav") in [1, 6, 8]:
            weak_organs.append("Nervous system, skin")
            preventions.append("Meditation, avoid junk food")
        if ketu.get("bhav") in [1, 6, 8]:
            weak_organs.append("Stomach, mysterious ailments")
            preventions.append("Regular checkups, spiritual practice")

        return {
            "weak_organs": weak_organs or ["No major weaknesses"],
            "preventions": preventions or ["Regular exercise, balanced diet"],
            "recommendation": f"Focus on: {', '.join(weak_organs) if weak_organs else 'general health'}",
            "source": "BPHS Ch. 26, Phaladeepika Ch. 20"
        }

    # ══════════════════════════════════════════
    # SPIRITUAL (12th + 9th House)
    # ══════════════════════════════════════════

    def _spiritual_analysis(self) -> Dict[str, Any]:
        """Spiritual path, guru, moksha."""
        guru = self.pos.get("Guru", {})
        ketu = self.pos.get("Ketu", {})

        path = "Bhakti (Devotional)"
        if guru.get("bhav") in [9, 12]:
            path = "Gyana (Knowledge) + Bhakti"
        if ketu.get("bhav") in [9, 12]:
            path = "Dhyana (Meditation) — deep spiritual"

        return {
            "path": path,
            "guru": "Will find guru after 30",
            "practice": "Daily meditation + Gayatri Mantra",
            "source": "BPHS Ch. 25, Jaimini Sutras"
        }

    # ══════════════════════════════════════════
    # DREAMS (Timing — Dasha Based)
    # ══════════════════════════════════════════

    def _dreams_analysis(self) -> Dict[str, Any]:
        """When dreams will be fulfilled."""
        maha = self.dasha.get("current_mahadasha", {})
        current_lord = maha.get("planet", "")
        current_end = maha.get("end_date", "")

        dream_timing = "Next 3-5 years"
        if current_lord in ["Guru", "Shukra"]:
            dream_timing = f"Now till {current_end} — best period"
        elif current_lord in ["Shani", "Rahu"]:
            dream_timing = "Struggle period — patience needed"

        return {
            "best_period": dream_timing,
            "current_dasha": current_lord,
            "recommendation": f"Work on dreams in {dream_timing}",
            "source": "Vimshottari Dasha Phala"
        }

    # ══════════════════════════════════════════
    # TIMING (Overall)
    # ══════════════════════════════════════════

    def _timing_analysis(self) -> Dict[str, Any]:
        """Overall timing for major events."""
        maha = self.dasha.get("current_mahadasha", {})
        antar = self.dasha.get("current_antardasha", {})

        return {
            "current_mahadasha": f"{maha.get('hindi', '')} ({maha.get('start_date', '')} to {maha.get('end_date', '')})",
            "current_antardasha": f"{antar.get('hindi', '')} ({antar.get('start_date', '')} to {antar.get('end_date', '')})",
            "major_events": "Check individual sections for timing",
            "source": "Vimshottari Dasha"
        }


def analyze_life(positions, lagna, bhava_chalit, dasha=None):
    """Convenience function."""
    engine = LifePredictionEngine(positions, lagna, bhava_chalit, dasha)
    return engine.analyze_all()