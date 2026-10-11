"""
VASTU ONE — Marriage Compatibility & Life Engine
=================================================
Analyzes 7th house, Venus, Jupiter, Mangal Dosha, Dasha periods
for complete marriage guidance.
"""

from datetime import datetime
from typing import Dict, List, Any


class MarriageEngine:
    """Complete marriage analysis based on Vedic astrology."""

    SIGNS_HINDI = {
        "Mesh": "मेष", "Vrishabh": "वृषभ", "Mithun": "मिथुन", "Kark": "कर्क",
        "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchik": "वृश्चिक",
        "Dhanu": "धनु", "Makar": "मकर", "Kumbh": "कुंभ", "Meen": "मीन"
    }

    PLANETS_HINDI = {
        "Surya": "सूर्य", "Chandra": "चंद्र", "Mangal": "मंगल", "Budh": "बुध",
        "Guru": "गुरु", "Shukra": "शुक्र", "Shani": "शनि", "Rahu": "राहु", "Ketu": "केतु"
    }

    # 7th house rashi → spouse nature
    SPOUSE_BY_7TH_RASHI = {
        "Mesh": {"nature": "Energetic, bold, leadership quality, quick decisions", "profession": "Defense, sports, entrepreneurship, engineering", "appearance": "Athletic build, sharp features, aggressive look"},
        "Vrishabh": {"nature": "Patient, artistic, love luxury, food-lover, stubborn", "profession": "Artist, banking, finance, food industry", "appearance": "Pleasant face, well-built, beautiful eyes"},
        "Mithun": {"nature": "Talkative, intelligent, dual nature, social", "profession": "Communication, teaching, writing, IT", "appearance": "Youthful look, expressive face, tall"},
        "Kark": {"nature": "Emotional, caring, family-oriented, moody", "profession": "Doctor, teacher, nurse, hospitality", "appearance": "Soft features, round face, attractive"},
        "Simha": {"nature": "Royal, confident, egoistic, generous", "profession": "Government, leadership, entertainment", "appearance": "Impressive personality, broad shoulders"},
        "Kanya": {"nature": "Analytical, perfectionist, hardworking, critical", "profession": "Doctor, accountant, editor, researcher", "appearance": "Neat, slim, sharp features"},
        "Tula": {"nature": "Charming, balanced, artistic, diplomatic", "profession": "Lawyer, designer, business, fashion", "appearance": "Beautiful, attractive, well-groomed"},
        "Vrishchik": {"nature": "Intense, secretive, passionate, research-minded", "profession": "Research, occult, surgery, detective", "appearance": "Magnetic eyes, intense look"},
        "Dhanu": {"nature": "Philosophical, religious, optimistic, freedom-loving", "profession": "Teacher, priest, lawyer, travel", "appearance": "Tall, impressive, big forehead"},
        "Makar": {"nature": "Disciplined, ambitious, practical, hardworking", "profession": "Engineer, manager, politician, admin", "appearance": "Serious face, thin body, mature look"},
        "Kumbh": {"nature": "Unconventional, intellectual, humanitarian, detached", "profession": "Scientist, social worker, IT, astrologer", "appearance": "Unique style, expressive eyes"},
        "Meen": {"nature": "Spiritual, dreamy, compassionate, emotional", "profession": "Spiritual, artist, poet, healer", "appearance": "Soft features, dreamy eyes, attractive"}
    }

    MARRIAGE_DELAY_REASONS = {
        "Shani": "Shani 7th house mein — delay in marriage, mature partner needed",
        "Rahu": "Rahu 7th house mein — confusion in partner selection, foreign match possible",
        "Ketu": "Ketu 7th house mein — spiritual partner, past-life connection",
        "Mangal": "Mangal dosha — 7th/8th/12th house — Kuja dosha, delays + conflicts",
        "Surya": "Surya 7th house mein — ego issues, need adjustment",
    }

    def __init__(self, positions: Dict, lagna: Dict, dasha: Dict, bhava_chalit: Dict):
        self.pos = positions
        self.lagna = lagna
        self.dasha = dasha
        self.bhava = bhava_chalit

    def analyze_all(self) -> Dict[str, Any]:
        """Run complete marriage analysis."""
        return {
            "marriage_yoga": self._marriage_yoga(),
            "spouse_analysis": self._spouse_analysis(),
            "married_life": self._married_life(),
            "marital_harmony": self._marital_harmony(),
            "delay_analysis": self._delay_analysis(),
            "mangal_dosha": self._mangal_dosha(),
            "marriage_timing": self._marriage_timing(),
            "matching_guidance": self._matching_guidance(),
            "practical_rules": self._practical_rules(),
        }

    # ══════════════════════════════════════════
    # 1. MARRIAGE YOGA
    # ══════════════════════════════════════════
    def _marriage_yoga(self) -> Dict[str, Any]:
        """Analyze marriage yoga strength."""
        shukra = self.pos.get("Shukra", {})
        guru = self.pos.get("Guru", {})
        shani = self.pos.get("Shani", {})
        rahu = self.pos.get("Rahu", {})

        # 7th house (Marriage)
        seventh_lord_rashi = self._get_7th_lord()
        shukra_bhav = shukra.get("bhav")
        guru_bhav = guru.get("bhav")

        yoga_strength = "Average"
        if shukra_bhav in [1, 2, 4, 5, 7, 9, 11]:
            yoga_strength = "Strong"
        if shukra_bhav in [6, 8, 12]:
            yoga_strength = "Weak"

        return {
            "summary": f"Vivah yog {'strong' if yoga_strength == 'Strong' else 'moderate' if yoga_strength == 'Average' else 'weak'} hai.",
            "strength": yoga_strength,
            "shukra_bhav": shukra_bhav,
            "shukra_hindi": shukra.get("hindi", ""),
            "guru_bhav": guru_bhav,
            "seventh_lord": seventh_lord_rashi,
            "love_or_arranged": self._love_or_arranged(),
            "marriage_type": self._marriage_type(),
        }

    def _love_or_arranged(self) -> str:
        shukra = self.pos.get("Shukra", {})
        rahu = self.pos.get("Rahu", {})
        if shukra.get("bhav") in [5, 7, 11] and rahu.get("bhav") in [5, 7, 11]:
            return "Love marriage ke strong chances hain. 5th/7th/11th house active hain."
        elif shukra.get("bhav") in [5, 7]:
            return "Love ya arrange — dono ke chances hain. 5th house active hai."
        else:
            return "Arrange marriage zyada sambhavna hai. Family decision important rahega."

    def _marriage_type(self) -> str:
        shukra = self.pos.get("Shukra", {})
        rahu = self.pos.get("Rahu", {})
        if rahu.get("bhav") in [7, 9, 12]:
            return "Foreign ya different community se match ho sakta hai."
        if shukra.get("bhav") in [1, 7]:
            return "Same caste/community mein match zyada likely hai."
        return "Family background matching important rahegi."

    # ══════════════════════════════════════════
    # 2. SPOUSE ANALYSIS
    # ══════════════════════════════════════════
    def _spouse_analysis(self) -> Dict[str, Any]:
        """Analyze what spouse will be like."""
        seventh_lord = self._get_7th_lord()
        seventh_rashi = self._get_7th_house_rashi()
        info = self.SPOUSE_BY_7TH_RASHI.get(seventh_rashi, {})

        # If 7th house has planets, they influence spouse
        seventh_planets = [self.PLANETS_HINDI.get(p, p) for p, pd in self.pos.items() if pd.get("bhav") == 7]

        return {
            "summary": f"7th house {seventh_rashi} ({self.SIGNS_HINDI.get(seventh_rashi, seventh_rashi)}) mein hai. Aapka jeevansathi {info.get('nature', '')} nature ka hoga.",
            "seventh_rashi": seventh_rashi,
            "seventh_rashi_hindi": self.SIGNS_HINDI.get(seventh_rashi, ""),
            "seventh_lord": seventh_lord,
            "spouse_nature": info.get("nature", ""),
            "spouse_profession": info.get("profession", ""),
            "spouse_appearance": info.get("appearance", ""),
            "planets_in_7th": seventh_planets,
            "spouse_from_direction": self._spouse_direction(seventh_rashi),
            "spouse_age": self._spouse_age(),
        }

    def _get_7th_lord(self) -> str:
        seventh_rashi = self._get_7th_house_rashi()
        lords = {
            "Mesh": "Mangal", "Vrishabh": "Shukra", "Mithun": "Budh", "Kark": "Chandra",
            "Simha": "Surya", "Kanya": "Budh", "Tula": "Shukra", "Vrishchik": "Mangal",
            "Dhanu": "Guru", "Makar": "Shani", "Kumbh": "Shani", "Meen": "Guru"
        }
        return lords.get(seventh_rashi, "")

    def _get_7th_house_rashi(self) -> str:
        """Get rashi of 7th house from lagna."""
        lagna_rashi = self.lagna.get("lagna_rashi", "Mesh")
        signs = ["Mesh", "Vrishabh", "Mithun", "Kark", "Simha", "Kanya",
                 "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbh", "Meen"]
        lagna_idx = signs.index(lagna_rashi) if lagna_rashi in signs else 0
        return signs[(lagna_idx + 6) % 12]

    def _spouse_direction(self, rashi: str) -> str:
        directions = {
            "Mesh": "East", "Vrishabh": "South", "Mithun": "West", "Kark": "North",
            "Simha": "East", "Kanya": "South", "Tula": "West", "Vrishchik": "North",
            "Dhanu": "East", "Makar": "South", "Kumbh": "West", "Meen": "North"
        }
        return directions.get(rashi, "Unknown")

    def _spouse_age(self) -> str:
        shukra = self.pos.get("Shukra", {})
        shani = self.pos.get("Shani", {})
        if shani.get("bhav") in [7, 2, 12]:
            return "Jeevansathi aapse age mein bada (2-5 saal) ho sakta hai."
        if shukra.get("bhav") in [3, 5, 11]:
            return "Jeevansathi aapse age mein chhota ho sakta hai."
        return "Age difference kam (0-3 saal) rahega."

    # ══════════════════════════════════════════
    # 3. MARRIED LIFE
    # ══════════════════════════════════════════
    def _married_life(self) -> Dict[str, Any]:
        """Analyze married life overall."""
        # 7th house = spouse, 4th = domestic happiness, 2nd = family, 8th = longevity of marriage
        shukra = self.pos.get("Shukra", {})
        guru = self.pos.get("Guru", {})
        mangal = self.pos.get("Mangal", {})
        shani = self.pos.get("Shani", {})

        # Overall score
        score = 5  # neutral
        if shukra.get("bhav") in [1, 2, 4, 5, 7, 9, 11]: score += 2
        if guru.get("bhav") in [1, 2, 4, 5, 7, 9, 11]: score += 1
        if mangal.get("bhav") in [7, 8]: score -= 2
        if shani.get("bhav") in [7, 8]: score -= 1
        if mangal.get("bhav") in [1, 4, 7, 8, 12]: score -= 1

        if score >= 8:
            overall = "बहुत अच्छा (Excellent)"
            tone = "positive"
        elif score >= 6:
            overall = "अच्छा (Good)"
            tone = "positive"
        elif score >= 4:
            overall = "मध्यम (Average)"
            tone = "neutral"
        else:
            overall = "चुनौतीपूर्ण (Challenging)"
            tone = "negative"

        return {
            "summary": f"विवाहित जीवन {overall} रहेगा। Score: {score}/10",
            "score": score,
            "overall": overall,
            "tone": tone,
            "early_years": self._early_married_years(),
            "mid_years": self._mid_married_years(),
            "later_years": self._later_married_years(),
            "children_after_marriage": self._children_timing(),
            "financial_life_after_marriage": self._financial_after_marriage(),
            "challenges": self._married_challenges(),
            "strengths": self._married_strengths(),
        }

    def _early_married_years(self) -> str:
        return "Shaadi ke pehle 2-3 saal adjustment ke honge. Dono ko ek dusre ki nature samajhni hogi."

    def _mid_married_years(self) -> str:
        return "5-10 saal mein family expansion, children, property ke decisions honge. Career + family balance zaroori hai."

    def _later_married_years(self) -> str:
        return "15+ saal ke baad spiritual growth, children ki shaadi, retirement planning rahegi."

    def _children_timing(self) -> str:
        guru = self.pos.get("Guru", {})
        if guru.get("bhav") in [1, 2, 5, 9, 11]:
            return "Shaadi ke 1-3 saal mein santan yog hai."
        return "Shaadi ke 3-5 saal mein santan prapt ho sakti hai."

    def _financial_after_marriage(self) -> str:
        return "Shaadi ke baad financial growth hogi, lekin budgeting zaroori hai."

    def _married_challenges(self) -> List[str]:
        challenges = []
        mangal = self.pos.get("Mangal", {})
        shani = self.pos.get("Shani", {})
        rahu = self.pos.get("Rahu", {})

        if mangal.get("bhav") in [7, 8]:
            challenges.append("Mangal 7th/8th house mein — chhoti-moti ghar-grahak kalesh ho sakte hain")
        if shani.get("bhav") in [7, 8]:
            challenges.append("Shani 7th/8th house mein — emotional detachment, patience zaroori")
        if rahu.get("bhav") in [7, 8]:
            challenges.append("Rahu 7th/8th house mein — partner ki nature samajhne mein confusion")

        if not challenges:
            challenges.append("Bade challenges nahi hain — mutual understanding se sab theek rahega")
        return challenges

    def _married_strengths(self) -> List[str]:
        return [
            "Mutual respect se relationship mazboot hoga",
            "Financial growth partner ke saath hogi",
            "Family support milega",
            "Emotional bonding strong rahegi"
        ]

    # ══════════════════════════════════════════
    # 4. MARITAL HARMONY
    # ══════════════════════════════════════════
    def _marital_harmony(self) -> Dict[str, Any]:
        """Husband-wife relationship guidance."""
        return {
            "summary": "दांपत्य सुख के लिए कुछ सावधानियां और सुझाव।",
            "relationship_rules": [
                "एक दूसरे की भावनाओं का सम्मान करें",
                "छोटी बातों को बड़ा न बनाएं",
                "हर हफ्ते साथ में समय बिताएं",
                "पैसों के मामलों में पारदर्शिता रखें",
                "सास-ससुर के साथ संतुलन बनाएं",
                "बच्चों की परवरिश में साथ दें"
            ],
            "avoid": [
                "दूसरों के सामने शिकायत न करें",
                "पुरानी बातें न दोहराएं",
                "गुस्से में निर्णय न लें",
                "तुलना न करें",
            ],
            "remedies_for_harmony": self._harmony_remedies(),
        }

    def _harmony_remedies(self) -> List[str]:
        shukra = self.pos.get("Shukra", {})
        remedies = []
        if shukra.get("bhav") in [6, 8, 12]:
            remedies.append("शुक्र मजबूत करने के लिए शुक्रवार को सफेद फूल/मिठाई का दान करें")
        remedies.append("हर पूर्णिमा को भगवान शिव की पूजा करें")
        remedies.append("पति/पत्नी के साथ हर रविवार साथ में भोजन करें")
        return remedies

    # ══════════════════════════════════════════
    # 5. DELAY ANALYSIS
    # ══════════════════════════════════════════
    def _delay_analysis(self) -> Dict[str, Any]:
        """Why marriage is delayed."""
        reasons = []
        seventh_planets = [p for p, pd in self.pos.items() if pd.get("bhav") == 7]

        for p in seventh_planets:
            if p in self.MARRIAGE_DELAY_REASONS:
                reasons.append(self.MARRIAGE_DELAY_REASONS[p])

        shani = self.pos.get("Shani", {})
        rahu = self.pos.get("Rahu", {})
        if shani.get("bhav") in [1, 7, 8, 12]:
            reasons.append("शनि की स्थिति — विवाह में विलंब, धैर्य रखें")
        if rahu.get("bhav") in [1, 7, 8, 12]:
            reasons.append("राहु की स्थिति — भ्रम की स्थिति, सही निर्णय में समय लगेगा")

        if not reasons:
            reasons.append("विवाह में कोई विशेष विलंब नहीं, समय पर होगा")

        return {
            "summary": "विवाह विलंब के कारण और समाधान।",
            "reasons": reasons,
            "how_long": self._delay_duration(),
            "remedies": self._delay_remedies(),
        }

    def _delay_duration(self) -> str:
        maha = self.dasha.get("current_mahadasha", {})
        return f"Current mahadasha {maha.get('end_date', '')} tak delay ho sakta hai. Uske baad vivah yog active hoga."

    def _delay_remedies(self) -> List[str]:
        return [
            "शनिवार को शनि मंदिर में सरसों का तेल चढ़ाएं",
            "मंगलवार को हनुमान चालीसा पढ़ें",
            "गुरुवार को पीले वस्त्र दान करें",
            "शुक्रवार को सफेद मिठाई का दान",
            "सोमवार को शिवलिंग पर जल चढ़ाएं",
        ]

    # ══════════════════════════════════════════
    # 6. MANGAL DOSHA
    # ══════════════════════════════════════════
    def _mangal_dosha(self) -> Dict[str, Any]:
        """Mangal dosha analysis."""
        mangal = self.pos.get("Mangal", {})
        mangal_bhav = mangal.get("bhav")

        # Mangal dosha houses: 1, 4, 7, 8, 12
        dosha_houses = [1, 4, 7, 8, 12]
        has_dosha = mangal_bhav in dosha_houses

        # Dosha strength
        strength = "None"
        if has_dosha:
            if mangal_bhav in [1, 4, 7, 8, 12]:
                strength = "Moderate" if mangal_bhav == 1 else "Strong"

        return {
            "summary": f"मंगल दोष {'है' if has_dosha else 'नहीं है'}.",
            "has_dosha": has_dosha,
            "mangal_bhav": mangal_bhav,
            "mangal_hindi": mangal.get("hindi", ""),
            "mangal_rashi": mangal.get("rashi", ""),
            "strength": strength,
            "effects": self._mangal_effects(has_dosha),
            "cancellation": self._mangal_cancellation(),
            "remedies": self._mangal_remedies() if has_dosha else [],
            "matching_rule": "अगर मंगल दोष है तो साथी में भी मंगल दोष होना चाहिए, वरना मिलान में देखें।"
        }

    def _mangal_effects(self, has_dosha: bool) -> List[str]:
        if not has_dosha:
            return ["कोई मंगल दोष नहीं, विवाह में कोई बाधा नहीं"]
        return [
            "विवाह में विलंब हो सकता है",
            "दांपत्य जीवन में कलेश हो सकता है",
            "पति/पत्नी की सेहत का ध्यान रखें",
            "गुस्से पर नियंत्रण जरूरी है",
        ]

    def _mangal_cancellation(self) -> str:
        return "अगर मंगल मेष, वृश्चिक या कर्क राशि में हो तो दोष कम हो जाता है। कुंडली मिलान से पुष्टि करें।"

    def _mangal_remedies(self) -> List[str]:
        return [
            "मंगलवार को हनुमान जी की पूजा करें",
            "लाल मसूर दान करें",
            "मंगल ग्रह का मंत्र जप करें — ॐ अं अंगारकाय नमः",
            "शादी से पहले कुंडली मिलान जरूर करें",
        ]

    # ══════════════════════════════════════════
    # 7. MARRIAGE TIMING
    # ══════════════════════════════════════════
    def _marriage_timing(self) -> Dict[str, Any]:
        """When will marriage happen."""
        maha = self.dasha.get("mahadashas", [])
        current = self.dasha.get("current_mahadasha", {})
        current_planet = current.get("planet", "")

        # Planets favorable for marriage dasha
        favorable = ["Shukra", "Guru", "Chandra", "Budh"]
        timing_list = []

        for m in maha:
            planet = m.get("planet", "")
            if planet in favorable:
                timing_list.append({
                    "period": f"{m.get('start_date', '')} to {m.get('end_date', '')}",
                    "planet": self.PLANETS_HINDI.get(planet, planet),
                    "age": f"{m.get('start_age', 0):.0f}-{m.get('end_age', 0):.0f} years",
                    "reason": f"{self.PLANETS_HINDI.get(planet, planet)} दशा — विवाह के लिए शुभ",
                })

        # Best timing
        best = self._best_marriage_timing()

        return {
            "summary": "विवाह के शुभ समय की गणना।",
            "best_age": best,
            "favorable_periods": timing_list[:3],
            "current_planet": self.PLANETS_HINDI.get(current_planet, current_planet),
            "immediate_action": self._immediate_marriage_action(),
        }

    def _best_marriage_timing(self) -> str:
        shani = self.pos.get("Shani", {})
        rahu = self.pos.get("Rahu", {})
        if shani.get("bhav") in [7, 8] or rahu.get("bhav") in [7, 8]:
            return "विवाह २५-३० वर्ष की उम्र में होगा। जल्दबाजी न करें।"
        return "विवाह २२-२७ वर्ष की उम्र में संभव है।"

    def _immediate_marriage_action(self) -> str:
        return "अगर २८+ की उम्र है और विवाह नहीं हुआ, तो शुक्र और गुरु के उपाय करें। कुंडली मिलान में विशेष ध्यान दें।"

    # ══════════════════════════════════════════
    # 8. MATCHING GUIDANCE
    # ══════════════════════════════════════════
    def _matching_guidance(self) -> Dict[str, Any]:
        """Kundli matching guidance."""
        seventh_rashi = self._get_7th_house_rashi()
        compatible = self._compatible_rashis(seventh_rashi)

        return {
            "summary": "कुंडली मिलान के लिए दिशा-निर्देश।",
            "your_7th_rashi": seventh_rashi,
            "your_7th_rashi_hindi": self.SIGNS_HINDI.get(seventh_rashi, ""),
            "compatible_rashis": compatible,
            "recommended_nakshatras": self._recommended_nakshatras(),
            "avoid_if": self._avoid_matching(),
            "guna_milan_importance": "36 गुणों में से कम से कम 18 गुण मिलना जरूरी है।",
        }

    def _compatible_rashis(self, seventh_rashi: str) -> List[str]:
        compatible_map = {
            "Mesh": ["Simha", "Dhanu", "Mithun", "Kumbh"],
            "Vrishabh": ["Kanya", "Makar", "Kark", "Meen"],
            "Mithun": ["Tula", "Kumbh", "Mesh", "Simha"],
            "Kark": ["Vrishchik", "Meen", "Vrishabh", "Kanya"],
            "Simha": ["Mesh", "Dhanu", "Mithun", "Tula"],
            "Kanya": ["Vrishabh", "Makar", "Kark", "Vrishchik"],
            "Tula": ["Mithun", "Kumbh", "Simha", "Dhanu"],
            "Vrishchik": ["Kark", "Meen", "Kanya", "Makar"],
            "Dhanu": ["Mesh", "Simha", "Tula", "Kumbh"],
            "Makar": ["Vrishabh", "Kanya", "Vrishchik", "Meen"],
            "Kumbh": ["Mithun", "Tula", "Mesh", "Dhanu"],
            "Meen": ["Kark", "Vrishchik", "Vrishabh", "Makar"]
        }
        return compatible_map.get(seventh_rashi, [])

    def _recommended_nakshatras(self) -> str:
        return "रोहिणी, मृगशिरा, मघा, अनुराधा, रेवती — विवाह के लिए शुभ नक्षत्र।"

    def _avoid_matching(self) -> List[str]:
        return [
            "एक ही गोत्र में विवाह न करें",
            "मंगल दोष हो तो साथी में भी होना चाहिए",
            "नाड़ी दोष से बचें",
            "भकूट दोष से बचें",
            "36 में से 18 से कम गुण न हों",
        ]

    # ══════════════════════════════════════════
    # 9. PRACTICAL RULES
    # ══════════════════════════════════════════
    def _practical_rules(self) -> Dict[str, Any]:
        """Practical advice for happy married life."""
        return {
            "summary": "सुखी दांपत्य जीवन के लिए व्यावहारिक नियम।",
            "before_marriage": [
                "कुंडली मिलान जरूर करें",
                "साथी के परिवार को समझें",
                "आर्थिक स्थिति की पारदर्शिता रखें",
                "स्वास्थ्य की जांच करें",
                "मानसिक तैयारी करें"
            ],
            "after_marriage": [
                "पहले साल संयम रखें",
                "छोटी बातों को इग्नोर करें",
                "पति/पत्नी के परिवार का सम्मान करें",
                "हर हफ्ते एक-दूसरे के साथ समय बिताएं",
                "आर्थिक निर्णय साथ में लें",
                "बच्चों की परवरिश में साथ दें"
            ],
            "spiritual_practices": [
                "हर सोमवार शिवलिंग पर जल चढ़ाएं",
                "हर शुक्रवार देवी लक्ष्मी की पूजा",
                "हर पूर्णिमा को सत्यनारायण कथा",
                "साथ में गायत्री मंत्र जपें"
            ],
            "avoid": [
                "तुलना करना",
                "गुस्से में निर्णय लेना",
                "पुरानी बातें दोहराना",
                "दूसरों के सामने शिकायत करना"
            ]
        }


def analyze_marriage(positions, lagna, dasha, bhava_chalit):
    """Convenience function."""
    engine = MarriageEngine(positions, lagna, dasha, bhava_chalit)
    return engine.analyze_all()
