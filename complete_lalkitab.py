from pathlib import Path

# Complete Lal Kitab rules — all planets × all bhavas
LAL_KITAB_RULES = '''
    def analyze_all(self) -> Dict[str, Any]:
        """Run complete Lal Kitab analysis — all planets, all bhavas."""
        # Mangal — all bhavas
        self._lal_kitab_planet("Mangal", "मंगल", {
            1: {"title": "Mangal in 1st — Lal Kitab", "detail": "Mangal 1st house mein gussa, jaldi vivah nahi, joint family mein rehna chahiye. Aise log apne pita ke saath nahi reh paate.", "effects": ["Anger Issues", "Late Marriage", "Joint Family"], "remedies": [{"type": "Totka", "text": "Hanuman ji ko 21 din sindoor chadhaayein", "detail": "Tuesday se"}, {"type": "Totka", "text": "Kutton ko roti khilayein", "detail": "Tuesday"}]},
            2: {"title": "Mangal in 2nd — Lal Kitab", "detail": "Dhan mein utar-chadhav, family kalesh. Aise logon ka paisa tikta nahi.", "effects": ["Financial Issues", "Family Conflict"], "remedies": [{"type": "Totka", "text": "Kutton ko gud khilayein", "detail": "Tuesday"}, {"type": "Totka", "text": "Lal mirchi daan", "detail": "Tuesday"}]},
            3: {"title": "Mangal in 3rd — Lal Kitab", "detail": "Bhai-behen se madad, himmat, safalta. Aise log bahadur hote hain.", "effects": ["Courage", "Success", "Sibling Support"], "remedies": [{"type": "Totka", "text": "Lal mirchi daan", "detail": "Tuesday"}]},
            4: {"title": "Mangal in 4th — Lal Kitab", "detail": "Ghar mein kalesh, maa ki sehat kharab. Aise log apne ghar mein sukh nahi paate.", "effects": ["Home Conflict", "Mother's Health"], "remedies": [{"type": "Totka", "text": "Ghar mein mehndi lagayein", "detail": "West"}, {"type": "Totka", "text": "Maa ka samman karein", "detail": "Daily"}]},
            5: {"title": "Mangal in 5th — Lal Kitab", "detail": "Santan mein pareshani, love failure. Aise logon ke bachche kamzor hote hain.", "effects": ["Children Issues", "Love Failure"], "remedies": [{"type": "Totka", "text": "Mangalvar vrat", "detail": "21 Tuesday"}, {"type": "Totka", "text": "Hanuman Chalisa", "detail": "Daily"}]},
            6: {"title": "Mangal in 6th — Lal Kitab", "detail": "Shatru nash, bimari se ladai. Aise log apne dushmanon ko harate hain.", "effects": ["Enemy Victory", "Health Fight"], "remedies": [{"type": "Totka", "text": "Kutton ko khana", "detail": "Tuesday"}]},
            7: {"title": "Mangal in 7th — Lal Kitab", "detail": "Vivah mein pareshani, separation. Aise logon ke jeevansathi se jhagde hote hain.", "effects": ["Marriage Discord", "Separation Risk"], "remedies": [{"type": "Totka", "text": "Kumbh Vivah", "detail": "Before marriage"}, {"type": "Totka", "text": "Shiv puja", "detail": "Monday"}]},
            8: {"title": "Mangal in 8th — Lal Kitab", "detail": "Aayu mein sankat, accident. Aise logon ko accident ka risk hota hai.", "effects": ["Accident Risk", "Health"], "remedies": [{"type": "Totka", "text": "Hanuman Chalisa", "detail": "Daily"}, {"type": "Totka", "text": "Lal mirchi daan", "detail": "Tuesday"}]},
            9: {"title": "Mangal in 9th — Lal Kitab", "detail": "Bhagya uthan-chadhav, pita se door. Aise logon ka bhagya samay-samay pe badalta hai.", "effects": ["Luck Fluctuation", "Father Disconnect"], "remedies": [{"type": "Totka", "text": "Pita ka samman", "detail": "Daily"}]},
            10: {"title": "Mangal in 10th — Lal Kitab", "detail": "Career mein safalta, business. Aise log apne kaam mein mahir hote hain.", "effects": ["Career Success", "Business"], "remedies": [{"type": "Totka", "text": "Hanuman puja", "detail": "Tuesday"}]},
            11: {"title": "Mangal in 11th — Lal Kitab", "detail": "Labh, mitron se madad. Aise logon ko mitron se fayda hota hai.", "effects": ["Gains", "Friend Support"], "remedies": [{"type": "Totka", "text": "Lal mirchi daan", "detail": "Tuesday"}]},
            12: {"title": "Mangal in 12th — Lal Kitab", "detail": "Kharcha zyada, videsh yatra. Aise logon ka paisa kharch mein chala jata hai.", "effects": ["High Expenses", "Foreign Travel"], "remedies": [{"type": "Totka", "text": "Kutton ko khana", "detail": "Tuesday"}]},
        })

        # Shani — all 12 bhavas
        self._lal_kitab_planet("Shani", "शनि", {
            1: {"title": "Shani in 1st — Lal Kitab", "detail": "Mehnati, jaldi budhapa, vivah der se. Aise log bachpan mein kashth uthate hain.", "effects": ["Hard Work", "Early Aging", "Late Marriage"], "remedies": [{"type": "Totka", "text": "Peepal ko jal dein", "detail": "Saturday"}, {"type": "Totka", "text": "Kali chidiya ko khana", "detail": "Saturday"}]},
            2: {"title": "Shani in 2nd — Lal Kitab", "detail": "Dhan mein kami, family issues. Aise logon ka paisa ruk nahi paata.", "effects": ["Financial Issues", "Family"], "remedies": [{"type": "Totka", "text": "Kale til daan", "detail": "Saturday"}]},
            3: {"title": "Shani in 3rd — Lal Kitab", "detail": "Bhai-behen se door, himmat. Aise log apne bhaiyon se door rehte hain.", "effects": ["Sibling Distance", "Courage"], "remedies": [{"type": "Totka", "text": "Shani mantra", "detail": "Saturday"}]},
            4: {"title": "Shani in 4th — Lal Kitab", "detail": "Maa ki sehat kharab, ghar mein kalesh. Aise log apni maa ki sehat ke liye pareshan rehte hain.", "effects": ["Mother's Health", "Home"], "remedies": [{"type": "Totka", "text": "Maa ka samman", "detail": "Daily"}]},
            5: {"title": "Shani in 5th — Lal Kitab", "detail": "Santan mein deri, education issues. Aise logon ke bachche der se hote hain.", "effects": ["Children Delay", "Education"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            6: {"title": "Shani in 6th — Lal Kitab", "detail": "Shatru nash, bimari se ladai. Aise log apni bimari se ladte hain.", "effects": ["Enemy Victory", "Health"], "remedies": [{"type": "Totka", "text": "Hanuman Chalisa", "detail": "Saturday"}]},
            7: {"title": "Shani in 7th — Lal Kitab", "detail": "Vivah mein deri, age gap. Aise logon ka vivah der se hota hai.", "effects": ["Late Marriage", "Age Gap"], "remedies": [{"type": "Totka", "text": "Shani Shanti Pooja", "detail": "Saturday"}]},
            8: {"title": "Shani in 8th — Lal Kitab", "detail": "Aayu, accident, inheritance issues. Aise logon ko aayu ki chinta rehti hai.", "effects": ["Health Risk", "Inheritance"], "remedies": [{"type": "Totka", "text": "Shani mantra", "detail": "23000 times"}]},
            9: {"title": "Shani in 9th — Lal Kitab", "detail": "Bhagya, pita ki sehat. Aise logon ke pita ki sehat kharab hoti hai.", "effects": ["Luck", "Father's Health"], "remedies": [{"type": "Totka", "text": "Pitru tarpan", "detail": "Amavasya"}]},
            10: {"title": "Shani in 10th — Lal Kitab", "detail": "Career mein safalta, service. Aise log sarkari ya service field mein safal hote hain.", "effects": ["Career Success", "Service"], "remedies": [{"type": "Totka", "text": "Shani puja", "detail": "Saturday"}]},
            11: {"title": "Shani in 11th — Lal Kitab", "detail": "Labh, mitron se madad. Aise logon ko bade bhai se madad milti hai.", "effects": ["Gains", "Friends"], "remedies": [{"type": "Totka", "text": "Kale til daan", "detail": "Saturday"}]},
            12: {"title": "Shani in 12th — Lal Kitab", "detail": "Kharcha, videsh yatra. Aise logon ka paisa videsh mein kharch hota hai.", "effects": ["High Expenses", "Foreign"], "remedies": [{"type": "Totka", "text": "Videsh yatra", "detail": "Shani dasha"}]},
        })

        # Rahu — all 12 bhavas
        self._lal_kitab_planet("Rahu", "राहु", {
            1: {"title": "Rahu in 1st — Lal Kitab", "detail": "Dhokebaaz, jaldi vivah, toot jata hai. Aise log apne mata-pita ki baat nahi maante.", "effects": ["Deception", "Broken Marriage", "Snake Issues"], "remedies": [{"type": "Totka", "text": "Nag Panchami puja", "detail": "Annual"}, {"type": "Totka", "text": "Chandi ka nag", "detail": "Puja room"}]},
            2: {"title": "Rahu in 2nd — Lal Kitab", "detail": "Dhan mein dhokha, family issues. Aise logon ko paisa dhokhe se milta hai.", "effects": ["Financial Loss", "Family"], "remedies": [{"type": "Totka", "text": "Kali mirchi daan", "detail": "Saturday"}]},
            3: {"title": "Rahu in 3rd — Lal Kitab", "detail": "Bhai-behen se dhokha, himmat. Aise logon ke bhai dhokha dete hain.", "effects": ["Sibling Betrayal", "Courage"], "remedies": [{"type": "Totka", "text": "Rahu mantra", "detail": "18000 times"}]},
            4: {"title": "Rahu in 4th — Lal Kitab", "detail": "Ghar mein kalesh, maa ki sehat. Aise logon ki maa ki sehat kharab hoti hai.", "effects": ["Home Conflict", "Mother"], "remedies": [{"type": "Totka", "text": "Maa ka samman", "detail": "Daily"}]},
            5: {"title": "Rahu in 5th — Lal Kitab", "detail": "Santan mein problem, love failure. Aise logon ke bachche kamzor hote hain.", "effects": ["Children Issues", "Love"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            6: {"title": "Rahu in 6th — Lal Kitab", "detail": "Shatru nash, bimari se ladai. Aise log apne dushmanon ko harate hain.", "effects": ["Enemy Victory", "Health"], "remedies": [{"type": "Totka", "text": "Durga puja", "detail": "Navratri"}]},
            7: {"title": "Rahu in 7th — Lal Kitab", "detail": "Vivah mein dhokha, foreign partner. Aise logon ka jeevansathi videshi ho sakta hai.", "effects": ["Marriage Deception", "Foreign Partner"], "remedies": [{"type": "Totka", "text": "Kumbh Vivah", "detail": "Before marriage"}]},
            8: {"title": "Rahu in 8th — Lal Kitab", "detail": "Accident, health risk. Aise logon ko accident ka risk hota hai.", "effects": ["Accident", "Health"], "remedies": [{"type": "Totka", "text": "Rahu mantra", "detail": "Daily"}]},
            9: {"title": "Rahu in 9th — Lal Kitab", "detail": "Bhagya, pita ki sehat. Aise logon ke pita ki sehat kharab hoti hai.", "effects": ["Luck", "Father"], "remedies": [{"type": "Totka", "text": "Pitru tarpan", "detail": "Amavasya"}]},
            10: {"title": "Rahu in 10th — Lal Kitab", "detail": "Career mein safalta, business. Aise log apne career mein safal hote hain.", "effects": ["Career", "Business"], "remedies": [{"type": "Totka", "text": "Rahu puja", "detail": "Saturday"}]},
            11: {"title": "Rahu in 11th — Lal Kitab", "detail": "Labh, mitron se dhokha. Aise logon ko mitron se dhokha milta hai.", "effects": ["Gains", "Friends"], "remedies": [{"type": "Totka", "text": "Kali mirchi daan", "detail": "Saturday"}]},
            12: {"title": "Rahu in 12th — Lal Kitab", "detail": "Videsh yatra, kharcha. Aise logon ka paisa videsh mein kharch hota hai.", "effects": ["Foreign Travel", "Expenses"], "remedies": [{"type": "Totka", "text": "Rahu mantra", "detail": "Daily"}]},
        })

        # Ketu — all 12 bhavas
        self._lal_kitab_planet("Ketu", "केतु", {
            1: {"title": "Ketu in 1st — Lal Kitab", "detail": "Spiritual, vivah der se. Aise log jaldi spiritual ho jate hain.", "effects": ["Spirituality", "Late Marriage"], "remedies": [{"type": "Totka", "text": "Kutte ko khana", "detail": "Daily"}]},
            2: {"title": "Ketu in 2nd — Lal Kitab", "detail": "Dhan mein kami, family issues.", "effects": ["Financial Issues", "Family"], "remedies": [{"type": "Totka", "text": "Ketu mantra", "detail": "Daily"}]},
            3: {"title": "Ketu in 3rd — Lal Kitab", "detail": "Bhai-behen se door, himmat.", "effects": ["Sibling Distance", "Courage"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            4: {"title": "Ketu in 4th — Lal Kitab", "detail": "Ghar mein kalesh, maa ki sehat.", "effects": ["Home", "Mother"], "remedies": [{"type": "Totka", "text": "Maa ka samman", "detail": "Daily"}]},
            5: {"title": "Ketu in 5th — Lal Kitab", "detail": "Santan mein problem, love failure.", "effects": ["Children", "Love"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            6: {"title": "Ketu in 6th — Lal Kitab", "detail": "Shatru nash, bimari se ladai.", "effects": ["Enemy", "Health"], "remedies": [{"type": "Totka", "text": "Ketu mantra", "detail": "Daily"}]},
            7: {"title": "Ketu in 7th — Lal Kitab", "detail": "Vivah mein problem.", "effects": ["Marriage"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            8: {"title": "Ketu in 8th — Lal Kitab", "detail": "Accident, health risk.", "effects": ["Accident", "Health"], "remedies": [{"type": "Totka", "text": "Ketu mantra", "detail": "Daily"}]},
            9: {"title": "Ketu in 9th — Lal Kitab", "detail": "Bhagya, spiritual.", "effects": ["Luck", "Spiritual"], "remedies": [{"type": "Totka", "text": "Ketu mantra", "detail": "Daily"}]},
            10: {"title": "Ketu in 10th — Lal Kitab", "detail": "Career mein spiritual.", "effects": ["Career", "Spiritual"], "remedies": [{"type": "Totka", "text": "Ketu mantra", "detail": "Daily"}]},
            11: {"title": "Ketu in 11th — Lal Kitab", "detail": "Labh, mitron se madad.", "effects": ["Gains", "Friends"], "remedies": [{"type": "Totka", "text": "Ketu mantra", "detail": "Daily"}]},
            12: {"title": "Ketu in 12th — Lal Kitab", "detail": "Moksha, spiritual.", "effects": ["Moksha", "Spiritual"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        # Chandra — all 12 bhavas
        self._lal_kitab_planet("Chandra", "चन्द्र", {
            1: {"title": "Chandra in 1st — Lal Kitab", "detail": "Bhavuk, maa se prem.", "effects": ["Emotional", "Mother Love"], "remedies": [{"type": "Totka", "text": "Shivling pe doodh", "detail": "Monday"}]},
            2: {"title": "Chandra in 2nd — Lal Kitab", "detail": "Dhan mein sukh, family.", "effects": ["Wealth", "Family"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            3: {"title": "Chandra in 3rd — Lal Kitab", "detail": "Bhai-behen se prem.", "effects": ["Sibling Love"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            4: {"title": "Chandra in 4th — Lal Kitab", "detail": "Maa se prem, ghar sukh.", "effects": ["Mother", "Home"], "remedies": [{"type": "Totka", "text": "Chandi ka Chandra", "detail": "Puja room"}]},
            5: {"title": "Chandra in 5th — Lal Kitab", "detail": "Santan sukh.", "effects": ["Children"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            6: {"title": "Chandra in 6th — Lal Kitab", "detail": "Bimari, shatru.", "effects": ["Health", "Enemy"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            7: {"title": "Chandra in 7th — Lal Kitab", "detail": "Vivah sukh.", "effects": ["Marriage"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            8: {"title": "Chandra in 8th — Lal Kitab", "detail": "Mansik pareshani, maa ki sehat.", "effects": ["Mental Stress", "Mother"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            9: {"title": "Chandra in 9th — Lal Kitab", "detail": "Bhagya, maa.", "effects": ["Luck", "Mother"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            10: {"title": "Chandra in 10th — Lal Kitab", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Chandra puja", "detail": "Monday"}]},
            11: {"title": "Chandra in 11th — Lal Kitab", "detail": "Labh.", "effects": ["Gains"], "remedies": [{"type": "Totka", "text": "Chandra mantra", "detail": "Monday"}]},
            12: {"title": "Chandra in 12th — Lal Kitab", "detail": "Mansik pareshani, kharcha.", "effects": ["Mental Stress", "Expenses"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        # Surya — all 12 bhavas
        self._lal_kitab_planet("Surya", "सूर्य", {
            1: {"title": "Surya in 1st — Lal Kitab", "detail": "Netritva, pita se door.", "effects": ["Leadership", "Father Disconnect"], "remedies": [{"type": "Totka", "text": "Surya arghya", "detail": "Daily"}]},
            2: {"title": "Surya in 2nd — Lal Kitab", "detail": "Dhan, family.", "effects": ["Wealth", "Family"], "remedies": [{"type": "Totka", "text": "Gud daan", "detail": "Sunday"}]},
            3: {"title": "Surya in 3rd — Lal Kitab", "detail": "Bhai-behen se madad.", "effects": ["Sibling Support"], "remedies": [{"type": "Totka", "text": "Surya arghya", "detail": "Daily"}]},
            4: {"title": "Surya in 4th — Lal Kitab", "detail": "Ghar sukh, maa.", "effects": ["Home", "Mother"], "remedies": [{"type": "Totka", "text": "Surya arghya", "detail": "Daily"}]},
            5: {"title": "Surya in 5th — Lal Kitab", "detail": "Santan sukh.", "effects": ["Children"], "remedies": [{"type": "Totka", "text": "Surya puja", "detail": "Sunday"}]},
            6: {"title": "Surya in 6th — Lal Kitab", "detail": "Shatru nash.", "effects": ["Enemy"], "remedies": [{"type": "Totka", "text": "Surya puja", "detail": "Sunday"}]},
            7: {"title": "Surya in 7th — Lal Kitab", "detail": "Vivah mein problem.", "effects": ["Marriage"], "remedies": [{"type": "Totka", "text": "Surya arghya", "detail": "Daily"}]},
            8: {"title": "Surya in 8th — Lal Kitab", "detail": "Aayu, health.", "effects": ["Health"], "remedies": [{"type": "Totka", "text": "Surya mantra", "detail": "Daily"}]},
            9: {"title": "Surya in 9th — Lal Kitab", "detail": "Bhagya, pita.", "effects": ["Luck", "Father"], "remedies": [{"type": "Totka", "text": "Surya puja", "detail": "Sunday"}]},
            10: {"title": "Surya in 10th — Lal Kitab", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Surya puja", "detail": "Sunday"}]},
            11: {"title": "Surya in 11th — Lal Kitab", "detail": "Labh, mitron se madad.", "effects": ["Gains"], "remedies": [{"type": "Totka", "text": "Gud daan", "detail": "Sunday"}]},
            12: {"title": "Surya in 12th — Lal Kitab", "detail": "Kharcha, pita ki sehat.", "effects": ["Expenses", "Father"], "remedies": [{"type": "Totka", "text": "Surya mantra", "detail": "Daily"}]},
        })

        # Guru — all 12 bhavas
        self._lal_kitab_planet("Guru", "गुरु", {
            1: {"title": "Guru in 1st — Lal Kitab", "detail": "Dharmik, samman.", "effects": ["Spiritual", "Respect"], "remedies": [{"type": "Totka", "text": "Keshar tilak", "detail": "Daily"}]},
            2: {"title": "Guru in 2nd — Lal Kitab", "detail": "Dhan, family.", "effects": ["Wealth", "Family"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            3: {"title": "Guru in 3rd — Lal Kitab", "detail": "Bhai-behen se madad.", "effects": ["Sibling"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            4: {"title": "Guru in 4th — Lal Kitab", "detail": "Ghar sukh, maa.", "effects": ["Home", "Mother"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            5: {"title": "Guru in 5th — Lal Kitab", "detail": "Santan sukh, intelligent.", "effects": ["Children", "Intelligence"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            6: {"title": "Guru in 6th — Lal Kitab", "detail": "Shatru nash.", "effects": ["Enemy"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            7: {"title": "Guru in 7th — Lal Kitab", "detail": "Vivah sukh, samman.", "effects": ["Marriage", "Respect"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            8: {"title": "Guru in 8th — Lal Kitab", "detail": "Aayu, inheritance.", "effects": ["Health", "Inheritance"], "remedies": [{"type": "Totka", "text": "Guru mantra", "detail": "Thursday"}]},
            9: {"title": "Guru in 9th — Lal Kitab", "detail": "Bhagya, dharmik.", "effects": ["Luck", "Dharma"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            10: {"title": "Guru in 10th — Lal Kitab", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            11: {"title": "Guru in 11th — Lal Kitab", "detail": "Labh.", "effects": ["Gains"], "remedies": [{"type": "Totka", "text": "Guru puja", "detail": "Thursday"}]},
            12: {"title": "Guru in 12th — Lal Kitab", "detail": "Moksha, videsh.", "effects": ["Moksha", "Foreign"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        # Shukra — all 12 bhavas
        self._lal_kitab_planet("Shukra", "शुक्र", {
            1: {"title": "Shukra in 1st — Lal Kitab", "detail": "Sundar, prem.", "effects": ["Beauty", "Love"], "remedies": [{"type": "Totka", "text": "Safed phool", "detail": "Friday"}]},
            2: {"title": "Shukra in 2nd — Lal Kitab", "detail": "Dhan, family sukh.", "effects": ["Wealth", "Family"], "remedies": [{"type": "Totka", "text": "Lakshmi puja", "detail": "Friday"}]},
            3: {"title": "Shukra in 3rd — Lal Kitab", "detail": "Bhai-behen se prem.", "effects": ["Sibling"], "remedies": [{"type": "Totka", "text": "Shukra puja", "detail": "Friday"}]},
            4: {"title": "Shukra in 4th — Lal Kitab", "detail": "Ghar sukh, maa.", "effects": ["Home", "Mother"], "remedies": [{"type": "Totka", "text": "Lakshmi puja", "detail": "Friday"}]},
            5: {"title": "Shukra in 5th — Lal Kitab", "detail": "Santan sukh.", "effects": ["Children"], "remedies": [{"type": "Totka", "text": "Shukra puja", "detail": "Friday"}]},
            6: {"title": "Shukra in 6th — Lal Kitab", "detail": "Bimari.", "effects": ["Health"], "remedies": [{"type": "Totka", "text": "Shukra mantra", "detail": "Friday"}]},
            7: {"title": "Shukra in 7th — Lal Kitab", "detail": "Sundar partner, sukh.", "effects": ["Partner", "Happiness"], "remedies": [{"type": "Totka", "text": "Shukra puja", "detail": "Friday"}]},
            8: {"title": "Shukra in 8th — Lal Kitab", "detail": "Aayu, health.", "effects": ["Health"], "remedies": [{"type": "Totka", "text": "Shukra mantra", "detail": "Friday"}]},
            9: {"title": "Shukra in 9th — Lal Kitab", "detail": "Bhagya, prem.", "effects": ["Luck", "Love"], "remedies": [{"type": "Totka", "text": "Shukra puja", "detail": "Friday"}]},
            10: {"title": "Shukra in 10th — Lal Kitab", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Shukra puja", "detail": "Friday"}]},
            11: {"title": "Shukra in 11th — Lal Kitab", "detail": "Labh.", "effects": ["Gains"], "remedies": [{"type": "Totka", "text": "Lakshmi puja", "detail": "Friday"}]},
            12: {"title": "Shukra in 12th — Lal Kitab", "detail": "Vivah sukh, videsh.", "effects": ["Marriage", "Foreign"], "remedies": [{"type": "Totka", "text": "Dhyan", "detail": "Daily"}]},
        })

        # Budh — all 12 bhavas
        self._lal_kitab_planet("Budh", "बुध", {
            1: {"title": "Budh in 1st — Lal Kitab", "detail": "Buddhiman, vyapar.", "effects": ["Intelligence", "Business"], "remedies": [{"type": "Totka", "text": "Moong dal daan", "detail": "Wednesday"}]},
            2: {"title": "Budh in 2nd — Lal Kitab", "detail": "Dhan, vyapar.", "effects": ["Wealth", "Business"], "remedies": [{"type": "Totka", "text": "Moong dal daan", "detail": "Wednesday"}]},
            3: {"title": "Budh in 3rd — Lal Kitab", "detail": "Buddhiman, bhai prem.", "effects": ["Intelligence", "Siblings"], "remedies": [{"type": "Totka", "text": "Moong dal daan", "detail": "Wednesday"}]},
            4: {"title": "Budh in 4th — Lal Kitab", "detail": "Ghar sukh, maa.", "effects": ["Home", "Mother"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            5: {"title": "Budh in 5th — Lal Kitab", "detail": "Buddhiman, santan sukh.", "effects": ["Intelligence", "Children"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            6: {"title": "Budh in 6th — Lal Kitab", "detail": "Shatru nash, vyapar.", "effects": ["Enemy Victory", "Business"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            7: {"title": "Budh in 7th — Lal Kitab", "detail": "Vivah sukh, partner.", "effects": ["Marriage"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            8: {"title": "Budh in 8th — Lal Kitab", "detail": "Aayu, health.", "effects": ["Health"], "remedies": [{"type": "Totka", "text": "Budh mantra", "detail": "Wednesday"}]},
            9: {"title": "Budh in 9th — Lal Kitab", "detail": "Bhagya, vyapar.", "effects": ["Luck", "Business"], "remedies": [{"type": "Totka", "text": "Budh puja", "detail": "Wednesday"}]},
            10: {"title": "Budh in 10th — Lal Kitab", "detail": "Career mein safalta.", "effects": ["Career"], "remedies": [{"type": "Totka", "text": "Ganesh puja", "detail": "Wednesday"}]},
            11: {"title": "Budh in 11th — Lal Kitab", "detail": "Labh, vyapar.", "effects": ["Gains", "Business"], "remedies": [{"type": "Totka", "text": "Moong dal daan", "detail": "Wednesday"}]},
            12: {"title": "Budh in 12th — Lal Kitab", "detail": "Videsh, kharcha.", "effects": ["Foreign", "Expenses"], "remedies": [{"type": "Totka", "text": "Budh mantra", "detail": "Wednesday"}]},
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
'''

# Write complete engine
p = Path("engine/astro/lal_kitab_engine.py")

# Read original header (up to analyze_all)
original = p.read_text(encoding="utf-8")
header_end = original.find("    def analyze_all(self)")
if header_end == -1:
    print("ERROR: analyze_all not found")
else:
    header = original[:header_end]
    # Find _lal_kitab_planet old method end
    old_method_start = original.find("    def _lal_kitab_planet(self")
    old_method_end = -1
    if old_method_start != -1:
        # Find next def after this
        next_def = original.find("    def ", old_method_start + 10)
        if next_def != -1:
            old_method_end = next_def
        else:
            old_method_end = len(original)
    
    # New content
    new_content = header + LAL_KITAB_RULES
    p.write_text(new_content, encoding="utf-8")
    print("DONE - Lal Kitab engine completed!")
    print(f"File size: {len(new_content)} chars")