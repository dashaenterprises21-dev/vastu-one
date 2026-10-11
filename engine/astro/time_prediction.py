"""
VASTU ONE — Time-Based Prediction Engine
==========================================
Past Prediction + Present Situation + Future Prediction
Based on Vimshottari Dasha analysis
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


class TimePredictionEngine:
    """Past, Present, Future predictions based on Dasha."""

    # Dasha lords and their effects
    DASHA_EFFECTS = {
        "Surya": {
            "general": "Authority, leadership, government, father",
            "positive": "Promotion, recognition, authority, father's help",
            "negative": "Ego issues, father's health, government problems",
            "areas": ["Career", "Authority", "Father", "Health"],
        },
        "Chandra": {
            "general": "Emotions, mother, home, mental peace",
            "positive": "Mental peace, mother's help, property, marriage",
            "negative": "Mental stress, mother's health, emotional issues",
            "areas": ["Mind", "Mother", "Home", "Emotions"],
        },
        "Mangal": {
            "general": "Energy, courage, property, siblings",
            "positive": "Victory, property, courage, sibling help",
            "negative": "Accidents, anger, blood-related issues, conflicts",
            "areas": ["Courage", "Property", "Siblings", "Health"],
        },
        "Budh": {
            "general": "Communication, business, intelligence",
            "positive": "Business success, communication, education",
            "negative": "Mental stress, skin issues, communication problems",
            "areas": ["Education", "Business", "Communication", "Health"],
        },
        "Guru": {
            "general": "Wisdom, wealth, children, dharma",
            "positive": "Children, wealth, wisdom, spiritual growth",
            "negative": "Excess, weight gain, liver issues, religious conflicts",
            "areas": ["Children", "Wealth", "Wisdom", "Spiritual"],
        },
        "Shukra": {
            "general": "Love, marriage, luxury, arts",
            "positive": "Marriage, love, luxury, artistic success",
            "negative": "Relationship issues, excessive indulgence, health issues",
            "areas": ["Marriage", "Love", "Luxury", "Arts"],
        },
        "Shani": {
            "general": "Discipline, hard work, delays, karma",
            "positive": "Career growth, discipline, spiritual growth",
            "negative": "Delays, depression, chronic health, separation",
            "areas": ["Career", "Discipline", "Health", "Karma"],
        },
        "Rahu": {
            "general": "Illusion, foreign, technology, sudden changes",
            "positive": "Foreign travel, technology, sudden gains",
            "negative": "Deception, mental stress, sudden losses, addiction",
            "areas": ["Foreign", "Technology", "Sudden Events", "Mind"],
        },
        "Ketu": {
            "general": "Spirituality, detachment, moksha",
            "positive": "Spiritual growth, detachment, moksha",
            "negative": "Confusion, health issues, detachment from world",
            "areas": ["Spiritual", "Moksha", "Health", "Detachment"],
        },
    }

    def __init__(self, positions: Dict, lagna: Dict, dasha: Dict, bhava_chalit: Dict):
        self.pos = positions
        self.lagna = lagna
        self.dasha = dasha
        self.bhava = bhava_chalit

    def analyze_all(self) -> Dict[str, Any]:
        """Run complete time-based analysis."""
        return {
            "past_prediction": self._analyze_past(),
            "present_situation": self._analyze_present(),
            "future_prediction": self._analyze_future(),
            "dasha_timeline": self._build_timeline(),
            "karmic_analysis": self._analyze_karma(),
            "blocked_areas": self._identify_blocked_areas(),
            "timing_predictions": self._predict_timings(),
        }

    # ══════════════════════════════════════════
    # PAST PREDICTION (Last 20-30 Years)
    # ══════════════════════════════════════════

    def _analyze_past(self) -> Dict[str, Any]:
        """Analyze past 20-30 years based on dashas."""
        maha = self.dasha.get("mahadashas", [])
        current_date = datetime.now()

        past_events = []
        for m in maha:
            try:
                start = datetime.strptime(m.get("start_date", ""), "%Y-%m-%d")
                end = datetime.strptime(m.get("end_date", ""), "%Y-%m-%d")
            except:
                continue

            if end < current_date:
                # Past dasha
                planet = m.get("planet", "")
                effects = self.DASHA_EFFECTS.get(planet, {})

                # Age at the time
                age_start = m.get("start_age", 0)
                age_end = m.get("end_age", 0)

                past_events.append({
                    "period": f"{m.get('start_date', '')} to {m.get('end_date', '')}",
                    "planet": planet,
                    "hindi": m.get("hindi", ""),
                    "age": f"{age_start:.0f}-{age_end:.0f} years",
                    "what_happened": self._past_events(planet),
                    "why_happened": f"{planet} dasha ka prabhav — {effects.get('general', '')}",
                    "effect_type": "Positive" if age_start > 0 else "Negative",
                    "lessons": f"Is dasha mein seekha: {effects.get('positive', '')} aur {effects.get('negative', '')} ka balance.",
                })

        # Life milestones
        milestones = self._past_milestones()

        return {
            "summary": "Aapke pichle 20-30 saal ka analysis — dasha-based.",
            "dasha_periods": past_events[-5:] if len(past_events) > 5 else past_events,
            "life_milestones": milestones,
            "lessons_learned": self._past_lessons(),
            "karmic_debts": self._past_karma(),
            "what_could_have_been": self._past_alternative(),
        }

    def _past_events(self, planet: str) -> str:
        events = {
            "Surya": "Authority, recognition, father-related events. Government job ya promotion ke chances the.",
            "Chandra": "Emotional events, mother-related, home/property matters. Mental stress ya peace mila.",
            "Mangal": "Property, siblings, courage-related events. Conflicts ya victories.",
            "Budh": "Education, business, communication-related events. Success ya struggles.",
            "Guru": "Children, wealth, wisdom-related events. Growth ya expansion.",
            "Shukra": "Love, marriage, luxury-related events. Relationships ka prabhav.",
            "Shani": "Delays, hard work, career-related events. Struggle ya growth.",
            "Rahu": "Foreign, technology, sudden changes. Confusion ya gains.",
            "Ketu": "Spiritual, detachment, health-related events. Confusion ya moksha.",
        }
        return events.get(planet, "General events")

    def _past_milestones(self) -> List[Dict]:
        return [
            {"year": "Childhood", "event": "Basic education, family environment, health foundation", "dasha": "First Mahadasha"},
            {"year": "Teens", "event": "Higher education decision, career direction, first love", "dasha": "Second Mahadasha"},
            {"year": "20s", "event": "Career start, job/business decision, marriage", "dasha": "Third Mahadasha"},
            {"year": "30s", "event": "Career peak, family expansion, property", "dasha": "Fourth Mahadasha"},
        ]

    def _past_lessons(self) -> List[str]:
        return [
            "Har dasha mein kuch achha aur kuch bura hota hai — dono ko accept karein.",
            "Negative dashas mein patience aur positive dashas mein action zaroori hai.",
            "Karmic debts ko pichle janm ke karma se jodein.",
            "Remedies se dasha ka prabhav kam ho jata hai.",
        ]

    def _past_karma(self) -> str:
        return "Pichle janm ke karma ka prabhav is janm ki kundli mein dikhta hai. 5th house (Purva Punya) aur 9th house (Bhagya) se pata chalta hai."

    def _past_alternative(self) -> str:
        return "Agar pichli dashas mein remedies kiye hote, to negative prabhav kam ho sakta tha."

    # ══════════════════════════════════════════
    # PRESENT SITUATION (Current Dasha)
    # ══════════════════════════════════════════

    def _analyze_present(self) -> Dict[str, Any]:
        """Analyze current situation based on current dasha."""
        maha = self.dasha.get("current_mahadasha", {})
        antar = self.dasha.get("current_antardasha", {})
        pratyantar = self.dasha.get("current_pratyantardasha", {})

        maha_planet = maha.get("planet", "")
        antar_planet = antar.get("planet", "")
        maha_effects = self.DASHA_EFFECTS.get(maha_planet, {})
        antar_effects = self.DASHA_EFFECTS.get(antar_planet, {})

        return {
            "summary": f"Abhi {maha_planet} mahadasha aur {antar_planet} antardasha chal raha hai.",
            "current_mahadasha": {
                "planet": maha_planet,
                "period": f"{maha.get('start_date', '')} to {maha.get('end_date', '')}",
                "general_effects": maha_effects.get("general", ""),
                "areas_affected": maha_effects.get("areas", []),
            },
            "current_antardasha": {
                "planet": antar_planet,
                "period": f"{antar.get('start_date', '')} to {antar.get('end_date', '')}",
                "general_effects": antar_effects.get("general", ""),
            },
            "what_is_happening_now": self._present_events(maha_planet, antar_planet),
            "why_things_are_blocked": self._present_blocks(),
            "how_long_blocks_will_last": self._present_block_duration(),
            "immediate_actions": self._present_actions(),
            "current_opportunities": self._present_opportunities(),
            "current_warnings": self._present_warnings(),
        }

    def _present_events(self, maha: str, antar: str) -> str:
        return f"{maha} mahadasha mein {antar} antardasha chal raha hai. Iska prabhav aapke {', '.join(self.DASHA_EFFECTS.get(maha, {}).get('areas', []))} pe pad raha hai."

    def _present_blocks(self) -> List[str]:
        blocks = []
        for planet in ["Shani", "Rahu", "Ketu", "Mangal"]:
            p = self.pos.get(planet, {})
            if p.get("bhav") in [6, 8, 12]:
                blocks.append(f"{planet} {p.get('bhav')}th house mein hai — isliye {self.DASHA_EFFECTS.get(planet, {}).get('negative', '')} ka prabhav hai.")
        return blocks or ["Koi major block nahi hai — sab kuch normal hai."]

    def _present_block_duration(self) -> str:
        maha = self.dasha.get("current_mahadasha", {})
        return f"Current mahadasha {maha.get('end_date', '')} tak chalega. Tab tak kuch areas mein delays ho sakte hain."

    def _present_actions(self) -> List[str]:
        return [
            "Daily puja aur mantra jaap karein",
            "Patience rakhein — dasha change ka wait karein",
            "Negative planetary remedies karein",
            "Financial planning karein",
            "Health pe dhyan dein",
        ]

    def _present_opportunities(self) -> List[str]:
        return [
            "Current dasha mein agar positive prabhav hai to action lena chahiye",
            "Job change ya business ke liye timing dekh rahi hai",
            "Marriage ya relationship ke liye timing",
        ]

    def _present_warnings(self) -> List[str]:
        return [
            "Negative planets ke related areas mein dhyan rakhein",
            "Health checkups regular karein",
            "Financial risks se bachein",
        ]

    # ══════════════════════════════════════════
    # FUTURE PREDICTION (Next 5-10 Years)
    # ══════════════════════════════════════════

    def _analyze_future(self) -> Dict[str, Any]:
        """Analyze future 5-10 years based on upcoming dashas."""
        maha = self.dasha.get("mahadashas", [])
        current_date = datetime.now()

        future_events = []
        for m in maha:
            try:
                start = datetime.strptime(m.get("start_date", ""), "%Y-%m-%d")
            except:
                continue

            if start > current_date:
                planet = m.get("planet", "")
                effects = self.DASHA_EFFECTS.get(planet, {})

                future_events.append({
                    "period": f"{m.get('start_date', '')} to {m.get('end_date', '')}",
                    "planet": planet,
                    "hindi": m.get("hindi", ""),
                    "age": f"{m.get('start_age', 0):.0f}-{m.get('end_age', 0):.0f} years",
                    "what_will_happen": self._future_events(planet),
                    "opportunities": effects.get("positive", ""),
                    "warnings": effects.get("negative", ""),
                    "preparation": self._future_preparation(planet),
                })

        # Next 5 years events
        next_5_years = self._next_5_years()

        return {
            "summary": "Aapke agle 5-10 saal ka analysis — dasha-based.",
            "next_mahadashas": future_events[:5],
            "next_5_years": next_5_years,
            "big_opportunities": self._future_opportunities(),
            "warnings": self._future_warnings(),
            "preparation": self._future_preparation_all(),
        }

    def _future_events(self, planet: str) -> str:
        events = {
            "Surya": "Authority, promotion, recognition, father-related events.",
            "Chandra": "Emotional, mother, home, property matters.",
            "Mangal": "Property, siblings, courage, conflicts.",
            "Budh": "Education, business, communication.",
            "Guru": "Children, wealth, wisdom, spiritual.",
            "Shukra": "Love, marriage, luxury, arts.",
            "Shani": "Delays, hard work, career growth.",
            "Rahu": "Foreign, technology, sudden changes.",
            "Ketu": "Spiritual, detachment, health.",
        }
        return events.get(planet, "General events")

    def _future_preparation(self, planet: str) -> str:
        return f"{planet} dasha ke liye abhi se remedies shuru karein."

    def _next_5_years(self) -> List[Dict]:
        return [
            {"year": "Year 1", "prediction": "Dasha change — new phase start", "action": "Remedies shuru karein"},
            {"year": "Year 2", "prediction": "Career growth ya change", "action": "Job/business ke decisions"},
            {"year": "Year 3", "prediction": "Marriage ya relationship milestone", "action": "Rishta dekhna shuru"},
            {"year": "Year 4", "prediction": "Financial growth ya property", "action": "Investment planning"},
            {"year": "Year 5", "prediction": "Major life event", "action": "Preparation complete karein"},
        ]

    def _future_opportunities(self) -> List[str]:
        return [
            "Upcoming dasha mein agar positive prabhav hai to action lena chahiye",
            "Business expansion ke chances",
            "Marriage ke chances",
            "Property purchase ke chances",
        ]

    def _future_warnings(self) -> List[str]:
        return [
            "Negative dashas mein health aur finances pe dhyan",
            "Relationship issues ho sakte hain",
            "Career changes sudden ho sakte hain",
        ]

    def _future_preparation_all(self) -> List[str]:
        return [
            "Upcoming dasha ke remedies abhi se shuru karein",
            "Financial planning karein",
            "Health checkups regular karein",
            "Relationships pe dhyan dein",
        ]

    # ══════════════════════════════════════════
    # DASHA TIMELINE
    # ══════════════════════════════════════════

    def _build_timeline(self) -> Dict[str, Any]:
        """Build complete dasha timeline."""
        maha = self.dasha.get("mahadashas", [])
        current = self.dasha.get("current_mahadasha", {})

        timeline = []
        for m in maha:
            timeline.append({
                "planet": m.get("planet", ""),
                "hindi": m.get("hindi", ""),
                "start": m.get("start_date", ""),
                "end": m.get("end_date", ""),
                "duration": m.get("duration_years", 0),
                "age_start": m.get("start_age", 0),
                "age_end": m.get("end_age", 0),
                "is_current": m.get("planet") == current.get("planet"),
            })

        return {
            "total_years": 120,
            "current_position": current.get("planet", ""),
            "timeline": timeline,
            "key_periods": self._key_periods(),
        }

    def _key_periods(self) -> List[Dict]:
        return [
            {"period": "Childhood (0-12)", "focus": "Education, health, family"},
            {"period": "Youth (12-24)", "focus": "Education, career start, love"},
            {"period": "Young Adult (24-36)", "focus": "Career, marriage, family"},
            {"period": "Middle Age (36-48)", "focus": "Career peak, property, children"},
            {"period": "Late Middle (48-60)", "focus": "Retirement planning, spiritual"},
            {"period": "Senior (60+)", "focus": "Spiritual, moksha, legacy"},
        ]

    # ══════════════════════════════════════════
    # KARMIC ANALYSIS
    # ══════════════════════════════════════════

    def _analyze_karma(self) -> Dict[str, Any]:
        """Analyze karmic debts."""
        # 5th house (Purva Punya)
        guru_bhav = self.pos.get("Guru", {}).get("bhav")
        # 9th house (Bhagya)
        surya_bhav = self.pos.get("Surya", {}).get("bhav")

        return {
            "purva_punya": "5th house se pichle janm ke karma ka pata chalta hai.",
            "bhagya": "9th house se is janm ka bhagya ka pata chalta hai.",
            "karmic_debts": self._karmic_debts(),
            "past_life_hints": self._past_life_hints(),
            "how_to_clear": self._clear_karma(),
        }

    def _karmic_debts(self) -> List[str]:
        return [
            "Pitru Dosh — ancestral karma",
            "Mangal Dosha — past life relationships",
            "Shani Dosha — past life karmic debt",
            "Rahu-Ketu Dosha — past life attachments",
        ]

    def _past_life_hints(self) -> str:
        return "5th house (Purva Punya) aur 9th house (Bhagya) se pichle janm ke karma ka pata chalta hai."

    def _clear_karma(self) -> List[str]:
        return [
            "Pitru Dosh Nivaran Pooja",
            "Karmic remedies (Shani, Rahu-Ketu)",
            "Charity aur seva",
            "Daily puja aur mantra jaap",
        ]

    # ══════════════════════════════════════════
    # BLOCKED AREAS
    # ══════════════════════════════════════════

    def _identify_blocked_areas(self) -> List[Dict]:
        """Identify blocked areas and their duration."""
        blocks = []
        for planet in ["Shani", "Rahu", "Ketu", "Mangal"]:
            p = self.pos.get(planet, {})
            bhav = p.get("bhav")
            if bhav in [6, 8, 12]:
                blocks.append({
                    "planet": planet,
                    "hindi": p.get("hindi", ""),
                    "bhav": bhav,
                    "area": self._bhav_area(bhav),
                    "why_blocked": f"{planet} {bhav}th house mein hai — {self.DASHA_EFFECTS.get(planet, {}).get('negative', '')}",
                    "duration": "Current mahadasha end tak",
                    "remedy": f"{planet} mantra + {planet} remedies",
                })
        return blocks

    def _bhav_area(self, bhav: int) -> str:
        areas = {
            6: "Health, enemies, debt, service",
            8: "Longevity, inheritance, sudden events",
            12: "Loss, foreign, expenses, moksha",
        }
        return areas.get(bhav, "General")

    # ══════════════════════════════════════════
    # TIMING PREDICTIONS
    # ══════════════════════════════════════════

    def _predict_timings(self) -> Dict[str, Any]:
        """Predict timing for major life events."""
        current = self.dasha.get("current_mahadasha", {})
        current_planet = current.get("planet", "")
        current_end = current.get("end_date", "")

        return {
            "career": self._career_timing(current_planet, current_end),
            "marriage": self._marriage_timing(current_planet, current_end),
            "wealth": self._wealth_timing(current_planet, current_end),
            "children": self._children_timing(current_planet, current_end),
            "property": self._property_timing(current_planet, current_end),
            "health": self._health_timing(current_planet, current_end),
            "spiritual": self._spiritual_timing(current_planet, current_end),
        }

    def _career_timing(self, planet: str, end: str) -> str:
        if planet in ["Surya", "Mangal", "Shani"]:
            return f"Career growth: {end} tak peak hoga."
        return f"Career change: next 2-3 years mein possible."

    def _marriage_timing(self, planet: str, end: str) -> str:
        if planet in ["Shukra", "Guru", "Chandra"]:
            return f"Marriage: {end} tak chances hain."
        return f"Marriage: next 3-5 years mein possible."

    def _wealth_timing(self, planet: str, end: str) -> str:
        if planet in ["Guru", "Shukra", "Budh"]:
            return f"Wealth peak: {end} tak."
        return f"Wealth growth: next 3-5 years mein."

    def _children_timing(self, planet: str, end: str) -> str:
        if planet in ["Guru", "Chandra"]:
            return f"Children: {end} tak chances."
        return f"Children: next 3-5 years mein possible."

    def _property_timing(self, planet: str, end: str) -> str:
        if planet in ["Mangal", "Shukra", "Chandra"]:
            return f"Property: {end} tak mil sakti hai."
        return f"Property: next 5 years mein."

    def _health_timing(self, planet: str, end: str) -> str:
        if planet in ["Shani", "Rahu", "Ketu"]:
            return f"Health issues: {end} tak. Regular checkup karein."
        return f"Health: stable rahegi."

    def _spiritual_timing(self, planet: str, end: str) -> str:
        if planet in ["Ketu", "Guru", "Shani"]:
            return f"Spiritual growth: {end} tak peak."
        return f"Spiritual: gradual growth."


def analyze_time_predictions(positions, lagna, dasha, bhava_chalit):
    """Convenience function."""
    engine = TimePredictionEngine(positions, lagna, dasha, bhava_chalit)
    return engine.analyze_all()