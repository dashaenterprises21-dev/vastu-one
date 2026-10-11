"""
VASTU ONE — Lal Kitab Deep Elaborator
========================================
AstroSage-style detailed elaboration for Lal Kitab findings.
"""

from typing import Dict, List, Any


class LalKitabElaborator:
    """Deep elaboration for Lal Kitab findings."""

    BHAV_MEANINGS = {
        1: {"name": "Tanu Bhava", "hindi": "तनु भाव", "areas": ["Self", "Body", "Personality", "Health"]},
        2: {"name": "Dhan Bhava", "hindi": "धन भाव", "areas": ["Wealth", "Family", "Speech", "Food"]},
        3: {"name": "Sahodar Bhava", "hindi": "सहोदर भाव", "areas": ["Siblings", "Courage", "Communication"]},
        4: {"name": "Sukh Bhava", "hindi": "सुख भाव", "areas": ["Home", "Mother", "Property", "Peace"]},
        5: {"name": "Putra Bhava", "hindi": "पुत्र भाव", "areas": ["Children", "Education", "Intelligence", "Love"]},
        6: {"name": "Roga Bhava", "hindi": "रोग भाव", "areas": ["Health", "Enemies", "Debt", "Service"]},
        7: {"name": "Kalatra Bhava", "hindi": "कलत्र भाव", "areas": ["Marriage", "Partnership", "Business"]},
        8: {"name": "Ayu Bhava", "hindi": "आयु भाव", "areas": ["Longevity", "Inheritance", "Sudden Events"]},
        9: {"name": "Bhagya Bhava", "hindi": "भाग्य भाव", "areas": ["Luck", "Father", "Dharma", "Higher Learning"]},
        10: {"name": "Karma Bhava", "hindi": "कर्म भाव", "areas": ["Career", "Status", "Authority"]},
        11: {"name": "Labh Bhava", "hindi": "लाभ भाव", "areas": ["Gains", "Friends", "Elder Siblings"]},
        12: {"name": "Vyay Bhava", "hindi": "व्यय भाव", "areas": ["Loss", "Foreign", "Moksha", "Expenses"]},
    }

    PLANET_NATURES = {
        "Surya": {"nature": "Royal, Authoritative", "element": "Fire", "deity": "Surya Narayan"},
        "Chandra": {"nature": "Emotional, Nurturing", "element": "Water", "deity": "Shiv ji"},
        "Mangal": {"nature": "Aggressive, Energetic", "element": "Fire", "deity": "Hanuman ji"},
        "Budh": {"nature": "Intelligent, Communicative", "element": "Earth", "deity": "Ganesh ji"},
        "Guru": {"nature": "Wise, Benevolent", "element": "Ether", "deity": "Brihaspati"},
        "Shukra": {"nature": "Loving, Artistic", "element": "Water", "deity": "Lakshmi ji"},
        "Shani": {"nature": "Disciplined, Karmic", "element": "Air", "deity": "Shani Dev"},
        "Rahu": {"nature": "Deceptive, Ambitious", "element": "Air", "deity": "Durga ji"},
        "Ketu": {"nature": "Spiritual, Detached", "element": "Fire", "deity": "Ganesh ji"},
    }

    def __init__(self, findings: List[Dict], positions: Dict, lagna: Dict):
        self.findings = findings
        self.pos = positions
        self.lagna = lagna

    def elaborate_all(self) -> List[Dict]:
        """Elaborate each Lal Kitab finding."""
        elaborated = []
        for finding in self.findings:
            elaborated.append(self._elaborate_finding(finding))
        return elaborated

    def _elaborate_finding(self, finding: Dict) -> Dict:
        planet = finding.get("planet", "")
        bhav = finding.get("bhav", 0)
        hindi = finding.get("hindi", "")

        bhav_info = self.BHAV_MEANINGS.get(bhav, {})
        planet_info = self.PLANET_NATURES.get(planet, {})

        return {
            "planet": planet,
            "hindi": hindi,
            "bhav": bhav,
            "title": finding.get("title", ""),
            "summary": finding.get("detail", ""),
            "reason": self._get_reason(planet, bhav),
            "planet_nature": f"{planet} — {planet_info.get('nature', '')}. Element: {planet_info.get('element', '')}. Deity: {planet_info.get('deity', '')}",
            "bhav_info": f"{bhav_info.get('hindi', '')} ({bhav_info.get('name', '')}) — {', '.join(bhav_info.get('areas', []))}",
            "short_term_effect": self._short_term_effect(planet, bhav),
            "long_term_effect": self._long_term_effect(planet, bhav),
            "timing": self._get_timing(planet),
            "age_range": self._get_age_range(planet, bhav),
            "case_study": self._get_case_study(planet, bhav),
            "remedies": self._elaborate_remedies(finding.get("remedies", [])),
            "do_list": self._get_do_list(planet, bhav),
            "dont_list": self._get_dont_list(planet, bhav),
            "cost_estimate": self._estimate_cost(finding.get("remedies", [])),
            "success_rate": self._success_rate(planet, bhav),
            "urgency": self._get_urgency(planet, bhav),
        }

    def _get_reason(self, planet: str, bhav: int) -> str:
        reasons = {
            ("Mangal", 12): "12th house mein Mangal hai, isliye kharcha zyada hai. Aapka paisa kharch mein chala jata hai. Mangal ka prabhav aapki aayu aur videsh yatra pe bhi hai.",
            ("Shani", 11): "11th house mein Shani hai, isliye labh mein deri hoti hai. Aapke bade bhai se madad milti hai par dhire-dhire. Shani ka prabhav aapke mitron pe bhi hai.",
            ("Rahu", 11): "11th house mein Rahu hai, isliye mitron se dhokha milta hai. Aapke labh mein utar-chadhav rehta hai. Rahu ka prabhav aapke bade bhai pe bhi hai.",
            ("Ketu", 5): "5th house mein Ketu hai, isliye santan mein pareshani hai. Aapke bachche kamzor hote hain. Ketu ka prabhav aapki education pe bhi hai.",
            ("Chandra", 6): "6th house mein Chandra hai, isliye mansik pareshani hai. Aapki maa ki sehat kharab hoti hai. Chandra ka prabhav aapke shatru pe bhi hai.",
            ("Surya", 2): "2nd house mein Surya hai, isliye dhan mein utar-chadhav hai. Aapke pita se doori rehti hai. Surya ka prabhav aapke family pe bhi hai.",
            ("Guru", 4): "4th house mein Guru hai, isliye ghar sukh aur maa se prem milta hai. Guru ka prabhav aapki property pe bhi hai.",
            ("Shukra", 1): "1st house mein Shukra hai, isliye aap sundar aur prem karne wale hain. Shukra ka prabhav aapki personality pe bhi hai.",
            ("Budh", 2): "2nd house mein Budh hai, isliye aap buddhiman aur vyapar mein mahir hain. Budh ka prabhav aapke dhan pe bhi hai.",
        }
        return reasons.get((planet, bhav), f"{planet} {bhav}th house mein hai, isliye {self.BHAV_MEANINGS.get(bhav, {}).get('areas', ['related'])[0]} mein prabhav hai.")

    def _short_term_effect(self, planet: str, bhav: int) -> str:
        effects = {
            ("Mangal", 12): "1-3 saal mein kharcha zyada ho sakta hai. Accident ka risk hai. Videsh yatra ke chances hain.",
            ("Shani", 11): "1-3 saal mein labh mein deri. Bade bhai se madad mil sakti hai. Mitron se distance ho sakta hai.",
            ("Rahu", 11): "1-3 saal mein mitron se dhokha. Labh mein utar-chadhav. Mental stress ho sakta hai.",
            ("Ketu", 5): "1-3 saal mein santan mein pareshani. Education mein obstacle. Love failure ho sakta hai.",
            ("Chandra", 6): "1-3 saal mein mansik pareshani. Maa ki sehat kharab. Shatru se ladai.",
            ("Surya", 2): "1-3 saal mein dhan mein utar-chadhav. Pita se doori. Family kalesh.",
            ("Guru", 4): "1-3 saal mein ghar sukh. Maa se prem. Property ka labh.",
            ("Shukra", 1): "1-3 saal mein prem, beauty, aur sukh. Personality strong.",
            ("Budh", 2): "1-3 saal mein buddhi, vyapar, aur dhan. Family sukh.",
        }
        return effects.get((planet, bhav), "Short-term effects: 1-3 saal mein prabhav dikhega.")

    def _long_term_effect(self, planet: str, bhav: int) -> str:
        effects = {
            ("Mangal", 12): "5-10 saal mein financial stability aayegi. Videsh yatra ka fayda hoga. Accident se bachna.",
            ("Shani", 11): "5-10 saal mein labh mein sudhar. Bade bhai se madad. Mitron ka support.",
            ("Rahu", 11): "5-10 saal mein mitron se distance. Labh mein stability. Mental peace.",
            ("Ketu", 5): "5-10 saal mein santan sukh. Education mein success. Love life stable.",
            ("Chandra", 6): "5-10 saal mein mansik peace. Maa ki sehat mein sudhar. Shatru nash.",
            ("Surya", 2): "5-10 saal mein dhan stability. Pita se mel. Family sukh.",
            ("Guru", 4): "5-10 saal mein ghar sukh. Property ka labh. Maa se prem.",
            ("Shukra", 1): "5-10 saal mein prem, beauty, aur sukh. Personality strong.",
            ("Budh", 2): "5-10 saal mein buddhi, vyapar, aur dhan. Family sukh.",
        }
        return effects.get((planet, bhav), "Long-term effects: 5-10 saal mein prabhav dikhega.")

    def _get_timing(self, planet: str) -> str:
        timings = {
            "Surya": "Surya dasha (6 years)", "Chandra": "Chandra dasha (10 years)",
            "Mangal": "Mangal dasha (7 years)", "Budh": "Budh dasha (17 years)",
            "Guru": "Guru dasha (16 years)", "Shukra": "Shukra dasha (20 years)",
            "Shani": "Shani dasha (19 years)", "Rahu": "Rahu dasha (18 years)",
            "Ketu": "Ketu dasha (7 years)",
        }
        return timings.get(planet, "Dasha-based timing")

    def _get_age_range(self, planet: str, bhav: int) -> str:
        return f"{planet} dasha mein prabhav peak hoga. Approximate: 25-40 years."

    def _get_case_study(self, planet: str, bhav: int) -> str:
        cases = {
            ("Mangal", 12): "Similar case: Ek vyakti ki kundli mein Mangal 12th house mein tha. Usne Hanuman Chalisa daily ki. 3 saal mein uski financial condition sudhar gayi. Accident se bhi bach gaya.",
            ("Shani", 11): "Similar case: Ek vyakti ki kundli mein Shani 11th house mein tha. Usne Shani mantra 23000 baar kiya. 2 saal mein labh mein sudhar aaya.",
            ("Rahu", 11): "Similar case: Ek vyakti ki kundli mein Rahu 11th house mein tha. Usne Durga Saptashati ka paath kiya. 1 saal mein mitron se dhokha kam hua.",
            ("Ketu", 5): "Similar case: Ek vyakti ki kundli mein Ketu 5th house mein tha. Usne Ganesh puja ki. 2 saal mein santan sukh mila.",
            ("Chandra", 6): "Similar case: Ek vyakti ki kundli mein Chandra 6th house mein tha. Usne Shiv Abhishek kiya. 1 saal mein mansik peace mili.",
            ("Surya", 2): "Similar case: Ek vyakti ki kundli mein Surya 2nd house mein tha. Usne Surya Arghya daily diya. 3 saal mein dhan stability aayi.",
            ("Guru", 4): "Similar case: Ek vyakti ki kundli mein Guru 4th house mein tha. Usne Guru puja ki. 2 saal mein ghar sukh mila.",
            ("Shukra", 1): "Similar case: Ek vyakti ki kundli mein Shukra 1st house mein tha. Usne Lakshmi puja ki. 1 saal mein prem aur beauty mili.",
            ("Budh", 2): "Similar case: Ek vyakti ki kundli mein Budh 2nd house mein tha. Usne Ganesh puja ki. 2 saal mein vyapar mein safalta mili.",
        }
        return cases.get((planet, bhav), "Similar cases mein proper remedies se fayda hua hai.")

    def _elaborate_remedies(self, remedies: List[Dict]) -> List[Dict]:
        elaborated = []
        for r in remedies:
            elaborated.append({
                "type": r.get("type", "Totka"),
                "text": r.get("text", ""),
                "detail": r.get("detail", ""),
                "how_to": f"Yeh totka {r.get('detail', 'specified time')} pe karein.",
                "cost": self._remedy_cost(r),
                "time_required": self._remedy_time(r),
                "difficulty": self._remedy_difficulty(r),
                "expected_result": "2-3 mahine mein fayda dikhega.",
            })
        return elaborated

    def _remedy_cost(self, remedy: Dict) -> str:
        text = remedy.get("text", "").lower()
        if "mantra" in text or "chalisa" in text or "puja" in text:
            return "₹0 (free)"
        if "daan" in text:
            return "₹100-500"
        return "₹0-500"

    def _remedy_time(self, remedy: Dict) -> str:
        detail = remedy.get("detail", "").lower()
        if "daily" in detail:
            return "Daily, 5-10 minutes"
        if "21" in detail:
            return "21 days"
        if "108" in detail:
            return "108 times"
        return "As specified"

    def _remedy_difficulty(self, remedy: Dict) -> str:
        text = remedy.get("text", "").lower()
        if "mantra" in text or "chalisa" in text:
            return "Easy"
        if "daan" in text:
            return "Easy"
        return "Medium"

    def _get_do_list(self, planet: str, bhav: int) -> List[str]:
        return [
            "Regular puja aur mantra jaap karein",
            "Satyavadi rahein",
            "Gareebon ki madad karein",
            "Apne mata-pita ka samman karein",
            "Positive soch rakhein",
        ]

    def _get_dont_list(self, planet: str, bhav: int) -> List[str]:
        return [
            "Krodh na karein",
            "Jhooth na bolein",
            "Kisi ka ahit na karein",
            "Nasha na karein",
            "Apne dharm se na hatein",
        ]

    def _estimate_cost(self, remedies: List[Dict]) -> str:
        total = len(remedies) * 200
        return f"₹{total}-{total * 2} (approximate)"

    def _success_rate(self, planet: str, bhav: int) -> str:
        return "80-90% logon ko fayda hota hai agar regular karein"

    def _get_urgency(self, planet: str, bhav: int) -> str:
        urgent_combos = [
            ("Mangal", 1), ("Mangal", 7), ("Mangal", 8),
            ("Shani", 1), ("Shani", 8), ("Shani", 12),
            ("Rahu", 1), ("Rahu", 5), ("Rahu", 8),
            ("Ketu", 1), ("Ketu", 5), ("Ketu", 8),
        ]
        if (planet, bhav) in urgent_combos:
            return "HIGH — Turant remedies shuru karein"
        return "MEDIUM — 1-2 mahine mein shuru karein"


def elaborate_lal_kitab(findings, positions, lagna):
    """Convenience function."""
    elaborator = LalKitabElaborator(findings, positions, lagna)
    return elaborator.elaborate_all()