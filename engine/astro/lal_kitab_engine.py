"""
VASTU ONE — Lal Kitab Engine
==============================
Unique Lal Kitab analysis + remedies (totke)
Based on: Lal Kitab 1952 (Rooplal Nagar)
"""

from typing import Dict, List, Any


class LalKitabEngine:
    """Lal Kitab analysis with unique remedies."""

    def __init__(self, positions: Dict, lagna: Dict):
        self.pos = positions
        self.lagna = lagna
        self.findings = []
        self.remedies = []

    def analyze_all(self) -> Dict[str, Any]:
        """Run complete Lal Kitab analysis — all planets, all bhavas."""
        # Mangal — all bhavas
        self._lal_kitab_planet("Mangal", "मंगल", {
            1: {"title": "Mangal in 1st", "detail": "Gussa, jaldi vivah nahi, joint family mein rehna chahiye.", "effects": ["Anger", "Late Marriage"], "remedies": [{"type": "Totka", "text": "Hanuman ji ko sindoor chadhaayein", "detail": "21 din Tuesday"}]},
            2: {"title": "Mangal in 2nd", "detail": "Dhan mein utar-chadhav, family mein kalesh.", "effects": ["Financial Issues", "Family Conflict"], "remedies": [{"type": "Totka", "text": "Kutton ko roti khilayein", "detail": "Tuesday"}]},
            3: {"title": "Mangal in 3rd", "detail": "Bhai-behen se madad, himmat, safalta.", "effects": ["Courage", "Success"], "remedies": [{"type": "Totka", "text": "Lal mirchi daan", "detail": "Tuesday"}]},
            4: {"title": "Mangal in 4th", "detail": "Ghar mein kalesh, maa ki sehat kharab.", "effects": ["Home Conflict", "Mother's Health"], "remedies": [{"type": "Totka", "text": "Ghar mein mehndi lagayein", "detail": "West"}]},
            5: {"title": "Mangal in 5th", "detail": "Santan mein pareshani, love failure.", "effects": ["Children Issues", "Love Failure"], "remedies": [{"type": "Totka", "text": "Mangalvar vrat", "detail": "21 Tuesday"}]},
            6: {"title": "Mangal in 6th", "detail": "Shatru nash, bimari se ladai.", "effects": ["Enemy Victory", "Health Fight"], "remedies": [{"type": "Totka", "text": "Kutton ko khana", "detail": "Tuesday"}]},
            7: {"title": "Mangal in 7th", "detail": "Vivah mein pareshani, separation.", "effects": ["Marriage Discord", "Separation"], "remedies": [{"type": "Totka", "text": "Kumbh Vivah", "detail": "Before marriage"}]},
            8: {"title": "Mangal in 8th", "detail": "Aayu mein sankat, accident.", "effects": ["Accident Risk", "Health"], "remedies": [{"type": "Totka", "text": "Hanuman Chalisa", "detail": "Daily"}]},
            9: {"title": "Mangal in 9th", "detail": "Bhagya uthan-chadhav, pita se door.", "effects": ["Luck Fluctuation", "Father Disconnect"], "remedies": [{"type": "Totka", "text": "Pita ka samman", "detail": "Daily"}]},
            10: {"title": "Mangal in 10th", "detail": "Career mein safalta, business.", "effects": ["Career Success", "Business"], "remedies": [{"type": "Totka", "text": "Hanuman puja", "detail": "Tuesday"}]},
            11: {"title": "Mangal in 11th", "detail": "Labh, mitron se madad.", "effects": ["Gains", "Friend Support"], "remedies": [{"type": "Totka", "text": "Lal mirchi daan", "detail": "Tuesday"}]},
            12: {"title": "Mangal in 12th", "detail": "Kharcha zyada, videsh yatra.", "effects": ["High Expenses", "Foreign Travel"], "remedies": [{"type": "Totka", "text": "Kutton ko khana", "detail": "Tuesday"}]},
        })

        # Shani — all bhavas
        self._lal_kitab_planet("Shani", "शनि", {
            1: {"title": "Shani in 1st", "detail": "Mehnati, jaldi budhapa, vivah der se.", "effects": ["Hard Work", "Late Marriage"], "remedies": [{"type": "Totka", "text": "Peepal ko jal dein", "detail": "Saturday"}]},
            2: {"title": "Shani in 2nd", "detail": "Dhan mein kami, family issues.", "effects": ["Financial Issues", "Family"], "remedies": [{"type": "Totka", "text": "Kale til daan", "detail": "Saturday"}]},
            3: {"title": "Shani in 3rd", "detail": "Bhai-behen se door, himmat.", "effects": ["Sibling Distance", "Courage"], "remedies": [{"type": "Totka", "text": "Shani mantra", "detail": "Saturday"}]},
            4: {"title": "Shani in 4th", "detail": "Maa ki sehat, ghar mein kalesh.", "effects": ["Mother's Health", "Home"], "remedies": [{"type": "Totka", "text": "Maa ka samman", "detail": "Daily"}]},
            5: {"title": "Shani in 5th", "detail": "Santan mein deri, education issues.", "effects": ["Children Delay", "Education"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            6: {"title": "Shani in 6th", "detail": "Shatru nash, bimari se ladai.", "effects": ["Enemy Victory", "Health"], "remedies": [{"type": "Totka", "text": "Hanuman Chalisa", "detail": "Saturday"}]},
            7: {"title": "Shani in 7th", "detail": "Vivah mein deri, age gap.", "effects": ["Late Marriage", "Age Gap"], "remedies": [{"type": "Totka", "text": "Shani Shanti Pooja", "detail": "Saturday"}]},
            8: {"title": "Shani in 8th", "detail": "Aayu, accident, inheritance issues.", "effects": ["Health Risk", "Inheritance"], "remedies": [{"type": "Totka", "text": "Shani mantra", "detail": "23000 times"}]},
            9: {"title": "Shani in 9th", "detail": "Bhagya, pita ki sehat.", "effects": ["Luck", "Father's Health"], "remedies": [{"type": "Totka", "text": "Pitru tarpan", "detail": "Amavasya"}]},
            10: {"title": "Shani in 10th", "detail": "Career mein safalta, service.", "effects": ["Career Success", "Service"], "remedies": [{"type": "Totka", "text": "Shani puja", "detail": "Saturday"}]},
            11: {"title": "Shani in 11th", "detail": "Labh, mitron se madad.", "effects": ["Gains", "Friends"], "remedies": [{"type": "Totka", "text": "Kale til daan", "detail": "Saturday"}]},
            12: {"title": "Shani in 12th", "detail": "Kharcha, videsh yatra.", "effects": ["High Expenses", "Foreign"], "remedies": [{"type": "Totka", "text": "Videsh yatra", "detail": "Shani dasha"}]},
        })

        # Rahu — all bhavas
        self._lal_kitab_planet("Rahu", "राहु", {
            1: {"title": "Rahu in 1st", "detail": "Dhokebaaz, jaldi vivah, toot jata hai.", "effects": ["Deception", "Broken Marriage"], "remedies": [{"type": "Totka", "text": "Nag Panchami puja", "detail": "Annual"}]},
            2: {"title": "Rahu in 2nd", "detail": "Dhan mein dhokha, family issues.", "effects": ["Financial Loss", "Family"], "remedies": [{"type": "Totka", "text": "Kali mirchi daan", "detail": "Saturday"}]},
            3: {"title": "Rahu in 3rd", "detail": "Bhai-behen se dhokha, himmat.", "effects": ["Sibling Betrayal", "Courage"], "remedies": [{"type": "Totka", "text": "Rahu mantra", "detail": "18000 times"}]},
            4: {"title": "Rahu in 4th", "detail": "Ghar mein kalesh, maa ki sehat.", "effects": ["Home Conflict", "Mother"], "remedies": [{"type": "Totka", "text": "Maa ka samman", "detail": "Daily"}]},
            5: {"title": "Rahu in 5th", "detail": "Santan mein problem, love failure.", "effects": ["Children Issues", "Love"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            6: {"title": "Rahu in 6th", "detail": "Shatru nash, bimari se ladai.", "effects": ["Enemy Victory", "Health"], "remedies": [{"type": "Totka", "text": "Durga puja", "detail": "Navratri"}]},
            7: {"title": "Rahu in 7th", "detail": "Vivah mein dhokha, foreign partner.", "effects": ["Marriage Deception", "Foreign Partner"], "remedies": [{"type": "Totka", "text": "Kumbh Vivah", "detail": "Before marriage"}]},
            8: {"title": "Rahu in 8th", "detail": "Accident, health risk.", "effects": ["Accident", "Health"], "remeges": [], "remedies": [{"type": "Totka", "text": "Rahu mantra", "detail": "Daily"}]},
            9: {"title": "Rahu in 9th", "detail": "Bhagya, pita ki sehat.", "effects": ["Luck", "Father"], "remedies": [{"type": "Totka", "text": "Pitru tarpan", "detail": "Amavasya"}]},
            10: {"title": "Rahu in 10th", "detail": "Career mein safalta, business.", "effects": ["Career", "Business"], "remedies": [{"type": "Totka", "text": "Rahu puja", "detail": "Saturday"}]},
            11: {"title": "Rahu in 11th", "detail": "Labh, mitron se dhokha.", "effects": ["Gains", "Friends"], "remedies": [{"type": "Totka", "text": "Kali mirchi daan", "detail": "Saturday"}]},
            12: {"title": "Rahu in 12th", "detail": "Videsh yatra, kharcha.", "effects": ["Foreign Travel", "Expenses"], "remedies": [{"type": "Totka", "text": "Rahu mantra", "detail": "Daily"}]},
        })

        # Ketu, Chandra, Surya, Guru, Shukra, Budh — similar pattern
        self._lal_kitab_planet("Ketu", "केतु", {
            1: {"title": "Ketu in 1st", "detail": "Spiritual, vivah der se.", "effects": ["Spirituality", "Late Marriage"], "remedies": [{"type": "Totka", "text": "Kutte ko khana", "detail": "Daily"}]},
            5: {"title": "Ketu in 5th", "detail": "Santan mein problem.", "effects": ["Children"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            7: {"title": "Ketu in 7th", "detail": "Vivah mein problem.", "effects": ["Marriage"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            9: {"title": "Ketu in 9th", "detail": "Bhagya, spiritual.", "effects": ["Luck", "Spiritual"], "remedies": [{"type": "Totka", "text": "Ketu mantra", "detail": "Daily"}]},
            12: {"title": "Ketu in 12th", "detail": "Moksha, spiritual.", "effects": ["Moksha", "Spiritual"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        self._lal_kitab_planet("Chandra", "चन्द्र", {
            1: {"title": "Chandra in 1st", "detail": "Bhavuk, maa se prem.", "effects": ["Emotional", "Mother Love"], "remedies": [{"type": "Totka", "text": "Shivling pe doodh", "detail": "Monday"}]},
            4: {"title": "Chandra in 4th", "detail": "Maa se prem, ghar sukh.", "effects": ["Mother", "Home"], "remedies": [{"type": "Totka", "text": "Chandi ka Chandra", "detail": "Puja room"}]},
            8: {"title": "Chandra in 8th", "detail": "Mansik pareshani, maa ki sehat.", "effects": ["Mental Stress", "Mother"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            12: {"title": "Chandra in 12th", "detail": "Mansik pareshani, kharcha.", "effects": ["Mental Stress", "Expenses"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        self._lal_kitab_planet("Surya", "सूर्य", {
            1: {"title": "Surya in 1st", "detail": "Netritva, pita se door.", "effects": ["Leadership", "Father"], "remedies": [{"type": "Totka", "text": "Surya arghya", "detail": "Daily"}]},
            10: {"title": "Surya in 10th", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Surya puja", "detail": "Sunday"}]},
            11: {"title": "Surya in 11th", "detail": "Labh, mitron se madad.", "effects": ["Gains"], "remedies": [{"type": "Totka", "text": "Gud daan", "detail": "Sunday"}]},
            7: {"title": "Surya in 7th", "detail": "Vivah mein problem.", "effects": ["Marriage"], "remedies": [{"type": "Totka", "text": "Surya arghya", "detail": "Daily"}]},
            12: {"title": "Surya in 12th", "detail": "Kharcha, pita ki sehat.", "effects": ["Expenses", "Father"], "remedies": [{"type": "Totka", "text": "Surya mantra", "detail": "Daily"}]},
        })

        self._lal_kitab_planet("Guru", "गुरु", {
            1: {"title": "Guru in 1st", "detail": "Dharmik, samman.", "effects": ["Spiritual", "Respect"], "remedies": [{"type": "Totka", "text": "Keshar tilak", "detail": "Daily"}]},
            5: {"title": "Guru in 5th", "detail": "Santan sukh, intelligent.", "effects": ["Children", "Intelligence"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            9: {"title": "Guru in 9th", "detail": "Bhagya, dharmik.", "effects": ["Luck", "Dharma"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            7: {"title": "Guru in 7th", "detail": "Vivah sukh, samman.", "effects": ["Marriage", "Respect"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            10: {"title": "Guru in 10th", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            12: {"title": "Guru in 12th", "detail": "Moksha, videsh.", "effects": ["Moksha", "Foreign"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        self._lal_kitab_planet("Shukra", "शुक्र", {
            1: {"title": "Shukra in 1st", "detail": "Sundar, prem.", "effects": ["Beauty", "Love"], "remedies": [{"type": "Totka", "text": "Safed phool", "detail": "Friday"}]},
            2: {"title": "Shukra in 2nd", "detail": "Dhan, family sukh.", "effects": ["Wealth", "Family"], "remedies": [{"type": "Totka", "text": "Lakshmi puja", "detail": "Friday"}]},
            4: {"title": "Shukra in 4th", "detail": "Ghar sukh, maa.", "effects": ["Home", "Mother"], "remedies": [{"type": "Totka", "text": "Lakshmi puja", "detail": "Friday"}]},
            7: {"title": "Shukra in 7th", "detail": "Sundar partner, sukh.", "effects": ["Partner", "Happiness"], "remedies": [{"type": "Totka", "text": "Shukra puja", "detail": "Friday"}]},
            10: {"title": "Shukra in 10th", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Shukra puja", "detail": "Friday"}]},
            12: {"title": "Shukra in 12th", "detail": "Vivah sukh, videsh.", "effects": ["Marriage", "Foreign"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        self._lal_kitab_planet("Budh", "बुध", {
            1: {"title": "Budh in 1st", "detail": "Buddhiman, vyapar.", "effects": ["Intelligence", "Business"], "remedies": [{"type": "Totka", "text": "Moong dal daan", "detail": "Wednesday"}]},
            3: {"title": "Budh in 3rd", "detail": "Buddhiman, bhai prem.", "effects": ["Intelligence", "Siblings"], "remedies": [{"type": "Totka", "text": "Moong dal daan", "detail": "Wednesday"}]},
            5: {"title": "Budh in 5th", "detail": "Buddhiman, santan sukh.", "effects": ["Intelligence", "Children"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            6: {"title": "Budh in 6th", "detail": "Shatru nash, vyapar.", "effects": ["Enemy Victory", "Business"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            10: {"title": "Budh in 10th", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            12: {"title": "Budh in 12th", "detail": "Videsh, kharcha.", "effects": ["Foreign", "Expenses"], "remedies": [{"type": "Totka", "text": "Budh mantra", "detail": "Wednesday"}]},
        })

        return {
            "findings": self.findings,
            "remedies": self.remedies,
            "total_findings": len(self.findings),
            "total_remedies": len(self.remedies),
        }

    def _lal_kitab_planet(self, planet_name: str, hindi: str, rules: Dict):
        """Apply Lal Kitab rules for a planet across all bhavas."""
        planet = self.pos.get(planet_name, {})
        bhav = planet.get("bhav")
        if not bhav:
            return
        rule = rules.get(bhav)
        if not rule:
            return
        finding = {
            "planet": planet_name,
            "hindi": hindi,
            "bhav": bhav,
            "title": rule["title"],
            "detail": rule["detail"],
            "effects": rule.get("effects", []),
            "remedies": rule.get("remedies", []),
            "source": "Lal Kitab 1952",
        }
        self.findings.append(finding)
        for r in rule.get("remedies", []):
            self.remedies.append({"planet": planet_name, **r})
        return {
            "findings": self.findings,
            "remedies": self.remedies,
            "total_findings": len(self.findings),
            "total_remedies": len(self.remedies),
        }

    # ══════════════════════════════════════════
    # MANGAL (Mars) — Lal Kitab 10th House Rules
    # ══════════════════════════════════════════

    def _lal_kitab_mangal(self):
        mangal = self.pos.get("Mangal", {})
        bhav = mangal.get("bhav")

        if bhav == 1:
            self.findings.append({
                "planet": "Mangal",
                "bhav": 1,
                "title": "Mangal in 1st — Lal Kitab",
                "detail": "Lal Kitab ke anusar, Mangal 1st house mein ho to vyakti bahut jaldi gussa karta hai. Iska vivaah jaldi nahi hota. Joint family mein rehna chahiye. Husband-wife mein frequency match nahi karti. Beti ke liye pareshaniyan aati hain. Aisa vyakti chhota bhai ho to uske saath masalah ho sakti hai.",
                "effects": ["Anger Issues", "Marriage Delay", "Joint Family Needed", "Father's Health"],
                "remedies": [
                    {"type": "Totka", "text": "Hanuman ji ko 21 din tak sindoor chadhaayein", "detail": "Tuesday se shuru karein"},
                    {"type": "Totka", "text": "Mangalvar ke din kutton ko roti khilayein", "detail": "Bina ghee ke"},
                    {"type": "Totka", "text": "Lal mirchi ka daan karein", "detail": "Tuesday, 21 mirchi"},
                    {"type": "Lal Kitab Upay", "text": "Mehndi ka ped ghar mein lagayein", "detail": "West direction"},
                ],
            })

        if bhav == 7:
            self.findings.append({
                "planet": "Mangal",
                "bhav": 7,
                "title": "Mangal in 7th — Lal Kitab",
                "detail": "Lal Kitab ke hisaab se, 7th house ka Mangal vivah mein bahut pareshani deta hai. Pati-patni mein jhagde hote hain. Separation ke chances hote hain. Aise log apne life partner ko thik se samajh nahi paate. Ek se zyada vivah ke chances hain. Ye log apne ghar mein sukh-shanti nahi le paate.",
                "effects": ["Marriage Discord", "Separation Risk", "Multiple Marriages", "Home Conflict"],
                "remedies": [
                    {"type": "Totka", "text": "Bhagwan Shiv ki puja karein", "detail": "Monday, 108 bel patri"},
                    {"type": "Totka", "text": "Kumbh Vivah karein", "detail": "Before actual marriage"},
                    {"type": "Lal Kitab Upay", "text": "Kutte ko ghar mein rakhein", "detail": "Black dog"},
                    {"type": "Lal Kitab Upay", "text": "Lal mirchi, gud ka daan", "detail": "Tuesday"},
                ],
            })

    # ══════════════════════════════════════════
    # SHANI (Saturn) — Lal Kitab Rules
    # ══════════════════════════════════════════

    def _lal_kitab_shani(self):
        shani = self.pos.get("Shani", {})
        bhav = shani.get("bhav")

        if bhav == 1:
            self.findings.append({
                "planet": "Shani",
                "bhav": 1,
                "title": "Shani in 1st — Lal Kitab",
                "detail": "Lal Kitab ke mutabik, 1st house ka Shani jatak ko bahut mehnati banata hai, par jaldi budhapa deta hai. Aise log apne bachpan mein bahut kashth uthate hain. Unka vivah der se hota hai. Aise log apne pita ke saath nahi reh paate. Unhe apne ghar se door jaana padta hai. Sharir mein kamzori aati hai.",
                "effects": ["Hard Work", "Early Aging", "Late Marriage", "Father Separation"],
                "remedies": [
                    {"type": "Totka", "text": "Shani var ko peepal ke ped ko jal dein", "detail": "Saturday, 21 din"},
                    {"type": "Totka", "text": "Kali chidiya ko khana khilayein", "detail": "Saturday"},
                    {"type": "Lal Kitab Upay", "text": "Loha ka ghoda ghar mein rakhein", "detail": "West wall"},
                    {"type": "Lal Kitab Upay", "text": "Kali mirchi, sarson ka tel daan", "detail": "Saturday"},
                ],
            })

    # ══════════════════════════════════════════
    # RAHU (North Node) — Lal Kitab
    # ══════════════════════════════════════════

    def _lal_kitab_rahu(self):
        rahu = self.pos.get("Rahu", {})
        bhav = rahu.get("bhav")

        if bhav == 1:
            self.findings.append({
                "planet": "Rahu",
                "bhav": 1,
                "title": "Rahu in 1st — Lal Kitab",
                "detail": "Lal Kitab ke anusar, 1st house ka Rahu vyakti ko dhokebaaz banata hai. Aise log apne mata-pita ki baat nahi maante. Unka vivah jaldi hota hai par toot jaata hai. Unhe apne jeevan mein bahut utar-chadhav dekhne padte hain. Aise logon ko apne gharon mein naga (snake) ki problem hoti hai. Unke bachche kamzor hote hain.",
                "effects": ["Deception", "Parental Disobedience", "Early Broken Marriage", "Snake Issues"],
                "remedies": [
                    {"type": "Totka", "text": "Nag Panchami pe nag devta ki puja", "detail": "Annual"},
                    {"type": "Totka", "text": "Kali mirchi, kala til daan", "detail": "Saturday"},
                    {"type": "Lal Kitab Upay", "text": "Chandi ka nag ghar mein rakhein", "detail": "Puja room"},
                    {"type": "Lal Kitab Upay", "text": "Ghar mein nariyal rakhein", "detail": "Replace every month"},
                ],
            })

    # ══════════════════════════════════════════
    # KETU (South Node) — Lal Kitab
    # ══════════════════════════════════════════

    def _lal_kitab_ketu(self):
        ketu = self.pos.get("Ketu", {})
        bhav = ketu.get("bhav")

        if bhav == 1:
            self.findings.append({
                "planet": "Ketu",
                "bhav": 1,
                "title": "Ketu in 1st — Lal Kitab",
                "detail": "Lal Kitab ke mutabik, 1st house ka Ketu jatak ko bhakti aur vairagya deta hai. Aise log bahut jaldi spiritual ho jate hain. Unka vivah der se hota hai ya nahi hota. Unhe apne parivar se koi support nahi milta. Sharir mein kai tarah ki bimariyan hoti hain.",
                "effects": ["Spirituality", "Late/No Marriage", "Family Disconnect", "Health Issues"],
                "remedies": [
                    {"type": "Totka", "text": "Kutte ko ghar mein rakhein", "detail": "Black dog"},
                    {"type": "Lal Kitab Upay", "text": "Ganesh ji ki puja", "detail": "Daily"},
                    {"type": "Lal Kitab Upay", "text": "Keshar ka tilak karein", "detail": "Forehead daily"},
                ],
            })

    # ══════════════════════════════════════════
    # CHANDRA (Moon) — Lal Kitab
    # ══════════════════════════════════════════

    def _lal_kitab_chandra(self):
        chandra = self.pos.get("Chandra", {})
        bhav = chandra.get("bhav")

        if bhav == 4:
            self.findings.append({
                "planet": "Chandra",
                "bhav": 4,
                "title": "Chandra in 4th — Lal Kitab",
                "detail": "Lal Kitab ke hisaab se, 4th house ka Chandra jatak ko apni maa se bahut prem karwata hai. Aise log apne ghar mein sukh-shanti chahte hain. Unki maa unke liye bahut important hoti hai. Unhe paani se related problem hoti hai. Ghar mein doodh, dahi ka istemal zyada hota hai.",
                "effects": ["Mother's Love", "Home Comfort", "Water Issues", "Emotional Nature"],
                "remedies": [
                    {"type": "Totka", "text": "Somvar ko Shivling pe doodh chadhaayein", "detail": "Monday"},
                    {"type": "Lal Kitab Upay", "text": "Ghar mein chandi ka Chandra rakhein", "detail": "Puja room"},
                    {"type": "Lal Kitab Upay", "text": "Safed cheezon ka daan", "detail": "Monday, rice/milk"},
                ],
            })

    # ══════════════════════════════════════════
    # SURYA (Sun) — Lal Kitab
    # ══════════════════════════════════════════

    def _lal_kitab_surya(self):
        surya = self.pos.get("Surya", {})
        bhav = surya.get("bhav")

        if bhav == 1:
            self.findings.append({
                "planet": "Surya",
                "bhav": 1,
                "title": "Surya in 1st — Lal Kitab",
                "detail": "Lal Kitab ke mutabik, 1st house ka Surya jatak ko netritva ki kshamta deta hai. Aise log apne parivar ke mukhiya bante hain. Unhe apne pita se koi sahayta nahi milti. Unka vivah jaldi hota hai. Unhe apne jeevan mein bahut sangharsh karna padta hai.",
                "effects": ["Leadership", "Father Disconnect", "Early Marriage", "Struggles"],
                "remedies": [
                    {"type": "Totka", "text": "Surya ko arghya dein", "detail": "Daily morning, copper vessel"},
                    {"type": "Lal Kitab Upay", "text": "Gud, gehu ka daan", "detail": "Sunday"},
                    {"type": "Lal Kitab Upay", "text": "Pipal ke ped mein jal dein", "detail": "Sunday"},
                ],
            })

    # ══════════════════════════════════════════
    # GURU (Jupiter) — Lal Kitab
    # ══════════════════════════════════════════

    def _lal_kitab_guru(self):
        guru = self.pos.get("Guru", {})
        bhav = guru.get("bhav")

        if bhav == 5:
            self.findings.append({
                "planet": "Guru",
                "bhav": 5,
                "title": "Guru in 5th — Lal Kitab",
                "detail": "Lal Kitab ke anusar, 5th house ka Guru jatak ko santan sukh deta hai. Aise log bahut intelligent hote hain. Unke bachche bahut aage badhte hain. Unhe apne jeevan mein bahut samman milta hai. Aise log bhagwan ke bahut bhakt hote hain.",
                "effects": ["Children Blessing", "Intelligence", "Respect", "Devotion"],
                "remedies": [
                    {"type": "Totka", "text": "Guruvar ko peele vastra daan", "detail": "Thursday"},
                    {"type": "Lal Kitab Upay", "text": "Keshar ka tilak", "detail": "Daily"},
                    {"type": "Lal Kitab Upay", "text": "Guru ki puja", "detail": "Thursday"},
                ],
            })

    # ══════════════════════════════════════════
    # SHUKRA (Venus) — Lal Kitab
    # ══════════════════════════════════════════

    def _lal_kitab_shukra(self):
        shukra = self.pos.get("Shukra", {})
        bhav = shukra.get("bhav")

        if bhav == 7:
            self.findings.append({
                "planet": "Shukra",
                "bhav": 7,
                "title": "Shukra in 7th — Lal Kitab",
                "detail": "Lal Kitab ke mutabik, 7th house ka Shukra jatak ko bahut sundar jeevansathi deta hai. Aise log apne partner se bahut prem karte hain. Unka vivah jaldi hota hai. Unhe apne jeevan mein bahut sukh milta hai. Unka jeevansathi bahut samajhdar hota hai.",
                "effects": ["Beautiful Partner", "Early Marriage", "Happy Married Life", "Understanding Spouse"],
                "remedies": [
                    {"type": "Totka", "text": "Shukravar ko safed phool daan", "detail": "Friday"},
                    {"type": "Lal Kitab Upay", "text": "Ghar mein chandi rakhein", "detail": "Puja room"},
                    {"type": "Lal Kitab Upay", "text": "Lakshmi ji ki puja", "detail": "Friday"},
                ],
            })

    # ══════════════════════════════════════════
    # BUDH (Mercury) — Lal Kitab
    # ══════════════════════════════════════════

    def _lal_kitab_budh(self):
        budh = self.pos.get("Budh", {})
        bhav = budh.get("bhav")

        if bhav == 3:
            self.findings.append({
                "planet": "Budh",
                "bhav": 3,
                "title": "Budh in 3rd — Lal Kitab",
                "detail": "Lal Kitab ke hisaab se, 3rd house ka Budh jatak ko bahut buddhiman banata hai. Aise log apne bhai-behno ke saath bahut pyaar karte hain. Unka vyapar bahut acha chalta hai. Unhe apne jeevan mein bahut safalta milti hai. Aise log apne kaam mein mahir hote hain.",
                "effects": ["Intelligence", "Sibling Love", "Business Success", "Skillful"],
                "remedies": [
                    {"type": "Totka", "text": "Budhvar ko hari sabzi daan", "detail": "Wednesday"},
                    {"type": "Lal Kitab Upay", "text": "Ganesh ji ki puja", "detail": "Wednesday"},
                    {"type": "Lal Kitab Upay", "text": "Moong dal ka daan", "detail": "Wednesday"},
                ],
            })


def analyze_lal_kitab(positions, lagna):
    """Convenience function."""
    engine = LalKitabEngine(positions, lagna)
    return engine.analyze_all()