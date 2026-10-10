"""
VASTU ONE — Report Elaborator
================================
AstroSage-style detailed elaboration for each prediction.
Expands predictions into: Reason + Effect + Timing + Case Study + Detailed Remedies
"""

from typing import Dict, List, Any


class ReportElaborator:
    """Expand predictions into detailed AstroSage-style reports."""

    def __init__(self, positions: Dict, lagna: Dict, dasha: Dict, doshas: List = None, yogas: List = None):
        self.pos = positions
        self.lagna = lagna
        self.dasha = dasha
        self.doshas = doshas or []
        self.yogas = yogas or []

    def elaborate_all(self, life_predictions: Dict, lal_kitab: Dict = None) -> Dict[str, Any]:
        """Elaborate all predictions."""
        return {
            "elaborated_career": self._elaborate_career(life_predictions.get("career", {})),
            "elaborated_marriage": self._elaborate_marriage(life_predictions.get("marriage", {})),
            "elaborated_wealth": self._elaborate_wealth(life_predictions.get("wealth", {})),
            "elaborated_health": self._elaborate_health(life_predictions.get("health", {})),
            "elaborated_education": self._elaborate_education(life_predictions.get("education", {})),
            "elaborated_business": self._elaborate_business(life_predictions.get("business", {})),
            "elaborated_children": self._elaborate_children(life_predictions.get("children", {})),
            "elaborated_location": self._elaborate_location(life_predictions.get("location", {})),
            "elaborated_personal": self._elaborate_personal(life_predictions.get("personal_life", {})),
            "elaborated_doshas": self._elaborate_doshas(),
            "elaborated_remedies": self._elaborate_remedies(),
            "case_studies": self._generate_case_studies(),
        }

    # ══════════════════════════════════════════
    # CAREER ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_career(self, career: Dict) -> Dict[str, Any]:
        field = career.get("best_field", "General")
        return {
            "summary": f"Aapka career {field} mein hai. {career.get('recommendation', '')}",
            "reason": self._career_reason(field),
            "detailed_analysis": self._career_detail(field),
            "effect_short_term": "1-3 saal mein career direction clear hoga. Job change ya promotion ke chances hain.",
            "effect_long_term": "10-15 saal mein peak career phase. Leadership role milega.",
            "timing": self._career_timing(),
            "case_study": self._career_case_study(field),
            "do_and_dont": {
                "do": [
                    "Regular skill upgrade karein",
                    "Senior se guidance lein",
                    "Network build karein",
                    "Financial planning karein",
                ],
                "dont": [
                    "Jaldi job change na karein",
                    "Risky investments se bachein",
                    "Colleagues se jhagda na karein",
                    "Loan zyada na lein",
                ],
            },
            "remedies": self._career_remedies(),
        }

    def _career_reason(self, field: str) -> str:
        surya = self.pos.get("Surya", {})
        shani = self.pos.get("Shani", {})
        guru = self.pos.get("Guru", {})
        reason = f"Aapke 10th house (career) mein "
        if shani.get("bhav") == 10:
            reason += f"Shani baithe hain — isliye service, engineering, ya government field suitable hai. "
        if surya.get("bhav") == 10:
            reason += f"Surya baithe hain — administration, leadership, ya government job best hai. "
        if guru.get("bhav") == 10:
            reason += f"Guru baithe hain — teaching, finance, ya consulting best hai. "
        reason += f"Aapki kundli mein {field} ka strong indication hai."
        return reason

    def _career_detail(self, field: str) -> List[str]:
        return [
            f"10th house ka detailed analysis: Aapka {field} field aapke planetary yogon se match karta hai.",
            f"Career growth: 30-45 saal ke beech peak phase hoga.",
            f"Dasha-based timing: Current mahadasha ke hisaab se growth periods identify kiye ja sakte hain.",
            f"Job vs Business: Aapki kundli {field} mein dono options support karti hai.",
            f"Salary range: 25-35 saal mein 8-15 lakh annual, 35-45 saal mein 15-30 lakh, 45+ mein 30+ lakh.",
        ]

    def _career_timing(self) -> str:
        maha = self.dasha.get("current_mahadasha", {})
        return f"Current mahadasha: {maha.get('planet', '')} ({maha.get('start_date', '')} to {maha.get('end_date', '')}). Career peak: next 3-5 years."

    def _career_case_study(self, field: str) -> str:
        return f"Similar kundli wale log: {field} field mein 5-10 saal mein settle hote hain. 30 ke baad unhe bada break milta hai. 40 ke baad leadership role milta hai. Isi pattern ke hisaab se aapko bhi 30-45 ke beech major success milega."

    def _career_remedies(self) -> List[Dict]:
        return [
            {"name": "Surya Arghya", "when": "Daily morning", "duration": "5 minutes", "cost": "₹0", "difficulty": "Easy"},
            {"name": "Shani mantra", "when": "Saturday", "duration": "108 times", "cost": "₹0", "difficulty": "Easy"},
            {"name": "Guru mantra", "when": "Thursday", "duration": "108 times", "cost": "₹0", "difficulty": "Easy"},
            {"name": "Yellow sapphire", "when": "Thursday", "duration": "Lifetime", "cost": "₹10,000-30,000", "difficulty": "Medium"},
        ]

    # ══════════════════════════════════════════
    # MARRIAGE ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_marriage(self, marriage: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Vivah: {marriage.get('timing', 'Unknown')}. {marriage.get('marriage_type', '')}",
            "reason": self._marriage_reason(),
            "detailed_analysis": self._marriage_detail(),
            "partner_description": self._partner_description(),
            "effect_short_term": "1-3 saal mein rishta aane ke chances. Family discussions honge.",
            "effect_long_term": "Vivah ke baad 2-3 saal adjustment period. Phir happy married life.",
            "timing": marriage.get("timing", "25-30"),
            "case_study": "Similar Mangal Dosha wali kundli: 60% cases mein vivah 30 ke baad hota hai, par happy rehta hai.",
            "do_and_dont": {
                "do": [
                    "Family ki salah maanein",
                    "Partner ki family se milna",
                    "Kumbh Vivah karein (agar Mangal Dosha)",
                    "Mangal Shanti Pooja karein",
                ],
                "dont": [
                    "Jaldbaazi na karein",
                    "Partner ko compare na karein",
                    "Inter-caste mein soch samajh kar",
                    "Financial status na dekhein",
                ],
            },
            "remedies": [
                {"name": "Kumbh Vivah", "when": "Before marriage", "duration": "Once", "cost": "₹5,000-11,000", "difficulty": "Medium"},
                {"name": "Mangal mantra", "when": "Tuesday", "duration": "108 times × 21 days", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Hanuman Chalisa", "when": "Tuesday, Saturday", "duration": "Daily", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Red coral (Moonga)", "when": "Tuesday", "duration": "Lifetime", "cost": "₹3,000-8,000", "difficulty": "Easy"},
            ],
        }

    def _marriage_reason(self) -> str:
        shukra = self.pos.get("Shukra", {})
        mangal = self.pos.get("Mangal", {})
        reason = f"Aapke 7th house (marriage) mein "
        if shukra.get("bhav") in [6, 8, 12]:
            reason += "Shukra weak position mein hai — isliye vivah mein deri ho sakti hai. "
        if mangal.get("bhav") in [1, 2, 4, 7, 8, 12]:
            reason += "Mangal Dosha hai — isliye vivah mein pareshaniyan aa sakti hain. "
        return reason + "Vivah timing aur partner nature aapki kundli ke hisaab se decide hoti hai."

    def _marriage_detail(self) -> List[str]:
        return [
            "7th house analysis: Aapka partner nature, vivah timing, aur married life happiness 7th house se decide hoti hai.",
            "Shukra (Venus) analysis: Vivah ke liye Shukra strong hona zaroori hai.",
            "Mangal Dosha: Agar hai to Kumbh Vivah ya Mangal Shanti Pooja zaroori hai.",
            "Vivah ke baad 2-3 saal adjustment period: Yahan patience rakhna zaroori hai.",
            "Financial aur emotional compatibility: Vivah se pehle yeh check karein.",
        ]

    def _partner_description(self) -> str:
        shukra = self.pos.get("Shukra", {})
        if shukra.get("rashi") in ["Vrishabh", "Tula"]:
            return "Partner: Sundar, artistic, luxury-loving, sweet-natured"
        elif shukra.get("rashi") in ["Kark", "Meen"]:
            return "Partner: Emotional, caring, homely, family-oriented"
        elif shukra.get("rashi") in ["Kanya", "Makar"]:
            return "Partner: Practical, hardworking, disciplined, honest"
        return "Partner: Understanding, supportive, good-natured"

    # ══════════════════════════════════════════
    # WEALTH ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_wealth(self, wealth: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Wealth: {wealth.get('wealth_level', 'Unknown')}. Source: {wealth.get('source', '')}",
            "reason": self._wealth_reason(),
            "detailed_analysis": self._wealth_detail(),
            "effect_short_term": "3-5 saal mein income sources expand honge. Small investments achhe returns denge.",
            "effect_long_term": "15-20 saal mein property, gold, aur financial assets ka strong portfolio banega.",
            "timing": wealth.get("timing", "30+ years"),
            "case_study": "Similar Dhana Yoga wali kundli: 35 ke baad financial stability aati hai, 45 ke baad wealth peak.",
            "do_and_dont": {
                "do": [
                    "SIP aur mutual funds mein invest karein",
                    "Gold aur property mein invest karein",
                    "Emergency fund rakhein",
                    "Insurance zaroor lein",
                ],
                "dont": [
                    "Share market mein jaldi na karein",
                    "Loan zyada na lein",
                    "Black money na rakhein",
                    "Gambling se bachein",
                ],
            },
            "remedies": [
                {"name": "Lakshmi puja", "when": "Friday", "duration": "Weekly", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Shree Yantra", "when": "Friday", "duration": "Lifetime", "cost": "₹1,000-5,000", "difficulty": "Easy"},
                {"name": "Kuber mantra", "when": "Daily", "duration": "108 times", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Gold coin", "when": "Dhanteras", "duration": "Annual", "cost": "₹5,000+", "difficulty": "Easy"},
            ],
        }

    def _wealth_reason(self) -> str:
        guru = self.pos.get("Guru", {})
        shukra = self.pos.get("Shukra", {})
        reason = f"Aapki kundli mein "
        if guru.get("bhav") in [2, 11]:
            reason += "Guru strong position mein hai — Dhana Yoga banta hai. "
        if shukra.get("bhav") in [2, 11]:
            reason += "Shukra strong hai — wealth aur luxury ka yog hai. "
        return reason + "Isliye financial growth strong hai."

    def _wealth_detail(self) -> List[str]:
        return [
            "2nd house (Dhana Bhava): Aapki savings aur accumulated wealth ka analysis.",
            "11th house (Labha Bhava): Aapki income aur gains ka analysis.",
            "Dhana Yogas: Aapki kundli mein jo bhi wealth-combinations hain.",
            "Timing: Jupiter dasha mein wealth peak hoti hai.",
            "Sources: Salary, business, investment, inheritance — yeh sab sources ho sakte hain.",
        ]

    # ══════════════════════════════════════════
    # HEALTH ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_health(self, health: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Health: {health.get('recommendation', '')}",
            "reason": self._health_reason(),
            "detailed_analysis": self._health_detail(),
            "effect_short_term": "Agar precautions nahi liye to 1-2 saal mein health issues aa sakte hain.",
            "effect_long_term": "Regular exercise aur balanced diet se health stable rahegi.",
            "prevention": health.get("preventions", []),
            "case_study": "Similar kundli wale log: 40 ke baad health issues start hote hain agar prevention na karein.",
            "do_and_dont": {
                "do": [
                    "Daily 30 min exercise",
                    "Balanced diet",
                    "Regular health checkups",
                    "Meditation aur yoga",
                ],
                "dont": [
                    "Junk food se bachein",
                    "Smoking/alcohol se bachein",
                    "Late night sleep se bachein",
                    "Stress na lein",
                ],
            },
            "remedies": [
                {"name": "Dhanwantari mantra", "when": "Daily", "duration": "21 times", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Mahamrityunjaya mantra", "when": "Monday", "duration": "108 times", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Rudraksha (5-mukhi)", "when": "Lifetime", "duration": "Always", "cost": "₹500-2,000", "difficulty": "Easy"},
            ],
        }

    def _health_reason(self) -> str:
        shani = self.pos.get("Shani", {})
        mangal = self.pos.get("Mangal", {})
        reason = f"Aapki kundli mein "
        if shani.get("bhav") in [1, 6, 8]:
            reason += "Shani weak position mein hai — bones, joints, teeth weak ho sakte hain. "
        if mangal.get("bhav") in [1, 6, 8]:
            reason += "Mangal weak position mein hai — blood, liver, injuries ka risk hai. "
        return reason + "Regular checkups aur prevention zaroori hai."

    def _health_detail(self) -> List[str]:
        return [
            "6th house (Roga Bhava): Aapki overall health ka analysis.",
            "Lagna (1st house): Aapki body constitution aur immunity.",
            "Weak planets: Jo planets weak hain unke related organs weak ho sakte hain.",
            "Timing: Shani dasha mein health issues aa sakte hain.",
            "Prevention: Regular exercise, balanced diet, aur meditation zaroori hai.",
        ]

    # ══════════════════════════════════════════
    # EDUCATION ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_education(self, education: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Education: {education.get('best_field', 'General')}. {education.get('higher_education', '')}",
            "reason": self._education_reason(),
            "detailed_analysis": self._education_detail(),
            "effect_short_term": "Next 2-3 saal mein education complete hoga.",
            "effect_long_term": "Aapki education aapke career ki base banegi.",
            "obstacles": education.get("obstacles", []),
            "case_study": "Similar kundli wale log: Engineering/medical mein success milti hai.",
            "do_and_dont": {
                "do": [
                    "Apne interest ka field choose karein",
                    "Regular study schedule banayein",
                    "Teacher se guidance lein",
                    "Practical knowledge badhayein",
                ],
                "dont": [
                    "Peer pressure mein na aayein",
                    "Distractions se bachein",
                    "Comparison na karein",
                    "Backlogs na rakhein",
                ],
            },
            "remedies": [
                {"name": "Saraswati mantra", "when": "Daily", "duration": "108 times", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Ganesh puja", "when": "Wednesday", "duration": "Weekly", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Budh mantra", "when": "Wednesday", "duration": "108 times", "cost": "₹0", "difficulty": "Easy"},
            ],
        }

    def _education_reason(self) -> str:
        budh = self.pos.get("Budh", {})
        guru = self.pos.get("Guru", {})
        reason = f"Aapki kundli mein "
        if budh.get("bhav") in [1, 4, 5, 10]:
            reason += "Budh strong hai — Mathematics, Commerce, IT best hai. "
        if guru.get("bhav") in [5, 9, 12]:
            reason += "Guru strong hai — Philosophy, Law, Teaching best hai. "
        return reason

    def _education_detail(self) -> List[str]:
        return [
            "5th house: Aapki education aur intelligence ka analysis.",
            "Budh (Mercury): Communication, Mathematics, Commerce.",
            "Guru (Jupiter): Philosophy, Law, Teaching.",
            "Higher education: Foreign ke chances hain agar 9th/12th house strong ho.",
            "Obstacles: Shani aur Mangal agar 4/5/9 mein ho to education mein deri ho sakti hai.",
        ]

    # ══════════════════════════════════════════
    # BUSINESS ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_business(self, business: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Business: {business.get('best_business_type', 'General')}. {business.get('partner_or_alone', '')}",
            "reason": self._business_reason(),
            "detailed_analysis": self._business_detail(),
            "effect_short_term": "1-2 saal mein business start kar sakte hain.",
            "effect_long_term": "5-7 saal mein business stable hoga. 10+ saal mein peak.",
            "partner_advice": business.get("partner_nature", ""),
            "case_study": "Similar kundli wale log: Trading, IT, ya consulting mein success paate hain.",
            "do_and_dont": {
                "do": [
                    "Market research karein",
                    "Business plan banayein",
                    "Legal registration karayein",
                    "Backup fund rakhein",
                ],
                "dont": [
                    "Jaldi investment na karein",
                    "Loan zyada na lein",
                    "Trust issues na karein",
                    "Fraud se bachein",
                ],
            },
            "remedies": [
                {"name": "Ganesh puja", "when": "Wednesday", "duration": "Daily", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Lakshmi puja", "when": "Friday", "duration": "Weekly", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Kuber Yantra", "when": "Diwali", "duration": "Lifetime", "cost": "₹500-2,000", "difficulty": "Easy"},
            ],
        }

    def _business_reason(self) -> str:
        budh = self.pos.get("Budh", {})
        mangal = self.pos.get("Mangal", {})
        reason = f"Aapki kundli mein "
        if budh.get("bhav") in [3, 6, 10, 11]:
            reason += "Budh strong hai — trading, communication, IT ke liye best. "
        if mangal.get("bhav") in [3, 6, 10, 11]:
            reason += "Mangal strong hai — business aur expansion ke liye best. "
        return reason

    def _business_detail(self) -> List[str]:
        return [
            "2nd house: Business capital aur resources ka analysis.",
            "7th house: Partnership aur public dealing ka analysis.",
            "10th house: Business reputation aur authority ka analysis.",
            "11th house: Business gains aur networks ka analysis.",
            "Timing: Business start karne ke liye best time current dasha ke hisaab se.",
        ]

    # ══════════════════════════════════════════
    # CHILDREN ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_children(self, children: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Children: {children.get('count', 'Unknown')}. {children.get('nature', '')}",
            "reason": self._children_reason(),
            "detailed_analysis": self._children_detail(),
            "effect_short_term": "Vivah ke 2-3 saal baad children ke chances.",
            "effect_long_term": "Children aapki life ka important part honge.",
            "timing": children.get("timing", "After marriage 2-5 years"),
            "case_study": "Similar kundli wale log: 2-3 children hote hain, mostly intelligent.",
            "do_and_dont": {
                "do": [
                    "Regular health checkup",
                    "Balanced diet",
                    "Garbh Sanskar karein",
                    "Santan Gopal mantra jaap",
                ],
                "dont": [
                    "Stress na lein",
                    "Late night na karein",
                    "Smoking/alcohol se bachein",
                    "Junk food se bachein",
                ],
            },
            "remedies": [
                {"name": "Santan Gopal mantra", "when": "Daily", "duration": "108 times", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Ganesh puja", "when": "Wednesday", "duration": "Weekly", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Pradosh vrat", "when": "Monthly", "duration": "Lifetime", "cost": "₹0", "difficulty": "Medium"},
            ],
        }

    def _children_reason(self) -> str:
        guru = self.pos.get("Guru", {})
        reason = f"Aapki kundli mein 5th house (children) "
        if guru.get("bhav") == 5:
            reason += "Guru strong hai — santan sukh milega. "
        elif guru.get("bhav") in [6, 8, 12]:
            reason += "Guru weak hai — santan mein deri ho sakti hai. "
        return reason

    def _children_detail(self) -> List[str]:
        return [
            "5th house: Santan sukh aur children ke nature ka analysis.",
            "Guru (Jupiter): Putra karaka, santan ke liye important planet.",
            "Timing: Vivah ke baad 2-5 saal mein children ke chances.",
            "Nature: Aapke children intelligent, well-behaved honge.",
            "Precautions: Regular checkup, healthy lifestyle zaroori hai.",
        ]

    # ══════════════════════════════════════════
    # LOCATION ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_location(self, location: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Best location: {location.get('recommendation', '')}",
            "reason": self._location_reason(),
            "detailed_analysis": self._location_detail(),
            "best_direction": location.get("best_direction", "East"),
            "best_country": location.get("best_country", "India"),
            "best_city_type": location.get("best_city_type", "Medium city"),
            "case_study": "Similar kundli wale log: Metro cities mein zyada success paate hain.",
            "do_and_dont": {
                "do": [
                    "East-facing house lein",
                    "Home town ke paas rakhein",
                    "Vastu-compliant ghar lein",
                    "Family ke saath rehne ki koshish karein",
                ],
                "dont": [
                    "South-facing house se bachein",
                    "Industrial area ke paas na rahein",
                    "Cemetery ke paas na rahein",
                    "Jail ke paas na rahein",
                ],
            },
            "remedies": [
                {"name": "Vastu Dosh Nivaran", "when": "One time", "duration": "Once", "cost": "₹5,000-25,000", "difficulty": "Medium"},
                {"name": "Griha Pravesh Puja", "when": "New home", "duration": "Once", "cost": "₹3,000-11,000", "difficulty": "Medium"},
            ],
        }

    def _location_reason(self) -> str:
        rahu = self.pos.get("Rahu", {})
        chandra = self.pos.get("Chandra", {})
        reason = f"Aapki kundli mein "
        if rahu.get("bhav") in [9, 12]:
            reason += "Rahu strong hai — foreign ya distant city best. "
        if chandra.get("bhav") in [4]:
            reason += "Chandra strong hai — home town ya family ke paas best. "
        return reason

    def _location_detail(self) -> List[str]:
        return [
            "4th house: Home town, mother, property ka analysis.",
            "9th house: Long-distance travel aur foreign ka analysis.",
            "12th house: Foreign settlement ka analysis.",
            "Direction: East aur North direction best hai.",
            "City type: Metro cities mein zyada scope hai.",
        ]

    # ══════════════════════════════════════════
    # PERSONAL ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_personal(self, personal: Dict) -> Dict[str, Any]:
        return {
            "summary": f"Personality: {personal.get('personality', '')}",
            "reason": self._personal_reason(),
            "detailed_analysis": self._personal_detail(),
            "strengths": personal.get("strengths", []),
            "weaknesses": personal.get("weaknesses", []),
            "case_study": "Similar Lagna wale log: Leadership aur creative skills mein strong hote hain.",
            "do_and_dont": {
                "do": [
                    "Apni strengths pe focus karein",
                    "Weaknesses pe kaam karein",
                    "Daily meditation karein",
                    "Journaling karein",
                ],
                "dont": [
                    "Apni weaknesses se compare na karein",
                    "Gussa control na karein",
                    "Negativity na failayein",
                    "Overthinking se bachein",
                ],
            },
            "remedies": [
                {"name": "Gayatri mantra", "when": "Daily 3 times", "duration": "5 minutes", "cost": "₹0", "difficulty": "Easy"},
                {"name": "Meditation", "when": "Daily", "duration": "20 minutes", "cost": "₹0", "difficulty": "Medium"},
            ],
        }

    def _personal_reason(self) -> str:
        lagna = self.lagna.get("lagna_rashi", "")
        return f"Aapki Lagna {lagna} hai, isliye aapki personality aur nature aisi hai."

    def _personal_detail(self) -> List[str]:
        return [
            "Lagna (1st house): Aapki overall personality aur appearance.",
            "Chandra (Moon): Aapki emotional nature aur mental state.",
            "Surya (Sun): Aapka ego, confidence, aur leadership.",
            "Nakshatra: Aapki deep nature aur instincts.",
            "Timing: 28-35 ke beech personality peak hoti hai.",
        ]

    # ══════════════════════════════════════════
    # DOSHAS ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_doshas(self) -> List[Dict]:
        elaborated = []
        for dosha in self.doshas:
            elaborated.append({
                "name": dosha.get("name", ""),
                "hindi": dosha.get("hindi", ""),
                "severity": dosha.get("severity", "Medium"),
                "reason": f"Yeh dosha {dosha.get('description', '')} ki wajah se hai.",
                "effects": dosha.get("affected_areas", []),
                "remedies": self._dosha_remedies(dosha.get("name", "")),
                "case_study": f"Similar {dosha.get('name', '')} wale log: Proper remedies se dosha ka prabhav kam ho jata hai.",
            })
        return elaborated

    def _dosha_remedies(self, dosha_name: str) -> List[Dict]:
        remedy_map = {
            "Mangal Dosha": [
                {"name": "Kumbh Vivah", "cost": "₹5,000-11,000", "difficulty": "Medium", "time": "6 months"},
                {"name": "Mangal Shanti Pooja", "cost": "₹3,000-8,000", "difficulty": "Easy", "time": "1 day"},
                {"name": "Red coral", "cost": "₹3,000-8,000", "difficulty": "Easy", "time": "Lifetime"},
            ],
            "Shani Dosha": [
                {"name": "Shani Shanti Pooja", "cost": "₹3,000-11,000", "difficulty": "Easy", "time": "1 day"},
                {"name": "Hanuman Chalisa", "cost": "₹0", "difficulty": "Easy", "time": "Daily"},
                {"name": "Blue sapphire", "cost": "₹15,000-50,000", "difficulty": "Medium", "time": "Lifetime"},
            ],
            "Rahu-Ketu Dosha": [
                {"name": "Rahu-Ketu Shanti Pooja", "cost": "₹5,000-15,000", "difficulty": "Medium", "time": "1 day"},
                {"name": "Durga Saptashati Paath", "cost": "₹5,000-11,000", "difficulty": "Medium", "time": "9 days"},
            ],
            "Chandra Dosha": [
                {"name": "Chandra Shanti Pooja", "cost": "₹3,000-8,000", "difficulty": "Easy", "time": "1 day"},
                {"name": "Shiv Abhishek", "cost": "₹500-2,000", "difficulty": "Easy", "time": "Daily"},
            ],
        }
        return remedy_map.get(dosha_name, [])

    # ══════════════════════════════════════════
    # REMEDIES ELABORATION
    # ══════════════════════════════════════════

    def _elaborate_remedies(self) -> Dict[str, Any]:
        return {
            "immediate": [
                {"name": "Gayatri Mantra", "when": "Daily morning", "duration": "5 min", "cost": "₹0"},
                {"name": "Hanuman Chalisa", "when": "Tuesday/Saturday", "duration": "15 min", "cost": "₹0"},
                {"name": "Surya Arghya", "when": "Daily sunrise", "duration": "2 min", "cost": "₹0"},
            ],
            "weekly": [
                {"name": "Lakshmi Puja", "when": "Friday", "duration": "30 min", "cost": "₹100"},
                {"name": "Shani Puja", "when": "Saturday", "duration": "30 min", "cost": "₹100"},
                {"name": "Guru Puja", "when": "Thursday", "duration": "30 min", "cost": "₹100"},
            ],
            "monthly": [
                {"name": "Purnima Puja", "when": "Full moon", "duration": "1 hour", "cost": "₹500"},
                {"name": "Amavasya Tarpan", "when": "New moon", "duration": "1 hour", "cost": "₹500"},
            ],
            "yearly": [
                {"name": "Navratri Puja", "when": "September", "duration": "9 days", "cost": "₹5,000"},
                {"name": "Diwali Puja", "when": "November", "duration": "1 day", "cost": "₹2,000"},
                {"name": "Mahashivratri", "when": "February", "duration": "1 day", "cost": "₹1,000"},
            ],
        }

    # ══════════════════════════════════════════
    # CASE STUDIES
    # ══════════════════════════════════════════

    def _generate_case_studies(self) -> List[Dict]:
        return [
            {
                "title": "Case 1: Mangal Dosha wala vivah",
                "scenario": "Similar kundli wali ek mahila thi jiska vivah 32 saal mein hua.",
                "what_happened": "Family ne Kumbh Vivah karaya, phir vivah hua.",
                "result": "Happy married life. Ab 2 bachche hain.",
                "lesson": "Proper remedies se Mangal Dosha ka prabhav kam ho jata hai.",
            },
            {
                "title": "Case 2: Career mein safalta",
                "scenario": "Similar kundli wale ek vyakti thi jiska 10th house Shani se affected tha.",
                "what_happened": "Usne engineering ki, phir government job mein chala gaya.",
                "result": "Ab 45 saal mein senior position pe hai.",
                "lesson": "Shani 10th house mein service ya engineering field ke liye best hai.",
            },
            {
                "title": "Case 3: Wealth accumulation",
                "scenario": "Similar Dhana Yoga wali kundli thi.",
                "what_happened": "Usne 30 ke baad real estate mein invest kiya.",
                "result": "Ab 50 saal mein multi-crore property owner hai.",
                "lesson": "Dhana Yoga wale log 30+ ke baad real estate mein invest karein.",
            },
        ]


def elaborate_report(positions, lagna, dasha, life_predictions, doshas=None, yogas=None, lal_kitab=None):
    """Convenience function."""
    elaborator = ReportElaborator(positions, lagna, dasha, doshas, yogas)
    return elaborator.elaborate_all(life_predictions, lal_kitab)