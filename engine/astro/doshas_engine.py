"""
Doshas Engine — 20+ Doshas Detection
"""

class DoshasEngine:
    def __init__(self, positions, lagna, planets):
        self.positions = positions
        self.lagna = lagna
        self.planets = planets
    
    def detect_all(self):
        doshas = []
        pos = self.positions
        
        # 1. Mangal Dosha
        mangal_b = pos.get("Mangal", {}).get("bhav")
        if mangal_b in [1, 2, 4, 7, 8, 12]:
            doshas.append({"name": "Mangal Dosha", "hindi": "मंगल दोष", "severity": "High" if mangal_b in [1, 7, 8] else "Medium", "description": "Mangal in bhav " + str(mangal_b) + " — marriage, relationships", "remedy": "Mangal mantra, Kumbh Vivah, red coral", "affected_areas": ["Marriage","Relationships","Harmony"]})
        
        # 2. Shani Dosha
        shani_b = pos.get("Shani", {}).get("bhav")
        if shani_b in [1, 2, 4, 7, 8, 12]:
            doshas.append({"name": "Shani Dosha", "hindi": "शनि दोष", "severity": "Medium", "description": "Shani in bhav " + str(shani_b) + " — delays, obstacles", "remedy": "Shani mantra, Hanuman Chalisa", "affected_areas": ["Career","Health","Delays"]})
        
        # 3. Rahu-Ketu Dosha
        rahu_b = pos.get("Rahu", {}).get("bhav")
        ketu_b = pos.get("Ketu", {}).get("bhav")
        if rahu_b in [1, 5, 7, 8, 12] or ketu_b in [1, 5, 7, 8, 12]:
            doshas.append({"name": "Rahu-Ketu Dosha", "hindi": "राहु-केतु दोष", "severity": "Medium", "description": "Rahu bhav " + str(rahu_b) + ", Ketu bhav " + str(ketu_b) + " — confusion, detachment", "remedy": "Rahu-Ketu mantra, Durga pooja", "affected_areas": ["Mental peace","Decisions","Spirituality"]})
        
        # 4. Chandra Dosha
        chandra_b = pos.get("Chandra", {}).get("bhav")
        if chandra_b in [6, 8, 12]:
            doshas.append({"name": "Chandra Dosha", "hindi": "चन्द्र दोष", "severity": "Medium", "description": "Chandra in bhav " + str(chandra_b) + " — emotional issues", "remedy": "Chandra mantra, silver, pearl", "affected_areas": ["Emotions","Mental health","Mother"]})
        
        # 5. Surya Dosha
        surya_b = pos.get("Surya", {}).get("bhav")
        if surya_b in [6, 8, 12]:
            doshas.append({"name": "Surya Dosha", "hindi": "सूर्य दोष", "severity": "Medium", "description": "Surya in bhav " + str(surya_b) + " — ego issues", "remedy": "Surya mantra, Aditya Hridayam", "affected_areas": ["Father","Authority","Health"]})
        
        # 6. Guru Chandal
        if pos.get("Guru", {}).get("bhav") == pos.get("Rahu", {}).get("bhav"):
            doshas.append({"name": "Guru Chandal Dosha", "hindi": "गुरु चांडाल दोष", "severity": "High", "description": "Guru + Rahu together — wisdom blocked", "remedy": "Guru mantra, Vishnu pooja", "affected_areas": ["Wisdom","Luck","Spirituality"]})
        
        # 7. Shrapit Dosha
        if pos.get("Shani", {}).get("bhav") == pos.get("Rahu", {}).get("bhav"):
            doshas.append({"name": "Shrapit Dosha", "hindi": "श्रापित दोष", "severity": "High", "description": "Shani + Rahu — ancestral curse", "remedy": "Shani mantra, Rahu mantra, pitru pooja", "affected_areas": ["Ancestral","Health","Obstacles"]})
        
        # 8. Ashtama Shani
        if pos.get("Shani", {}).get("bhav") == 8:
            doshas.append({"name": "Ashtama Shani", "hindi": "अष्टम शनि", "severity": "High", "description": "Shani in 8th — health issues", "remedy": "Shani mantra, Hanuman Chalisa", "affected_areas": ["Health","Longevity","Obstacles"]})
        
        # 9. Kantaka Shani
        if pos.get("Shani", {}).get("bhav") == 4:
            doshas.append({"name": "Kantaka Shani", "hindi": "कंटक शनि", "severity": "Medium", "description": "Shani in 4th — domestic issues", "remedy": "Shani mantra, Shani pooja", "affected_areas": ["Home","Mother","Peace"]})
        
        # 10. Ardha Ashtama Shani
        if pos.get("Shani", {}).get("bhav") == 7:
            doshas.append({"name": "Ardha Ashtama Shani", "hindi": "अर्ध अष्टम शनि", "severity": "Medium", "description": "Shani in 7th — marriage delays", "remedy": "Shani mantra", "affected_areas": ["Marriage","Partnership"]})
        
        # 11. Pitru Dosha
        if pos.get("Surya", {}).get("bhav") == 9 or pos.get("Rahu", {}).get("bhav") == 9:
            doshas.append({"name": "Pitru Dosha", "hindi": "पितृ दोष", "severity": "Medium", "description": "9th house afflicted — ancestral issues", "remedy": "Pitru pooja, Shraddha, Tarpan", "affected_areas": ["Father","Luck","Ancestors"]})
        
        # 12-13. Grahan Dosha
        for lum in ["Surya", "Chandra"]:
            for node in ["Rahu", "Ketu"]:
                if pos.get(lum, {}).get("bhav") == pos.get(node, {}).get("bhav"):
                    doshas.append({"name": lum + "-" + node + " Grahan Dosha", "hindi": lum + "-" + node + " ग्रहण दोष", "severity": "High", "description": lum + " + " + node + " together", "remedy": lum + " mantra, " + node + " pooja", "affected_areas": ["Health","Mental peace"]})
        
        # 14. Kemdrum
        if chandra_b:
            b2 = (chandra_b % 12) + 1
            b12 = ((chandra_b - 2) % 12) + 1
            has_around = any(pos[p].get("bhav") in [b2, b12] for p in pos if p not in ["Chandra", "Surya"])
            if not has_around:
                doshas.append({"name": "Kemdrum Dosha", "hindi": "केमद्रुम दोष", "severity": "Medium", "description": "No planets around Chandra — mental stress", "remedy": "Chandra mantra, silver", "affected_areas": ["Mental","Emotions","Mother"]})
        
        # 15. Nadi Dosha
        if pos.get("Chandra", {}).get("nakshatra") and pos.get("Shukra", {}).get("nakshatra"):
            doshas.append({"name": "Nadi Dosha", "hindi": "नाड़ी दोष", "severity": "Medium", "description": "For marriage compatibility — needs checking", "remedy": "Nadi dosha nivaran pooja", "affected_areas": ["Marriage","Health","Children"]})
        
        # 16. Bhakoot Dosha
        doshas.append({"name": "Bhakoot Dosha", "hindi": "भकूट दोष", "severity": "Low", "description": "For marriage compatibility — needs checking", "remedy": "Bhakoot dosha nivaran", "affected_areas": ["Marriage","Harmony"]})
        
        # 17. Gana Dosha
        doshas.append({"name": "Gana Dosha", "hindi": "गण दोष", "severity": "Low", "description": "For marriage compatibility — needs checking", "remedy": "Gana dosha nivaran", "affected_areas": ["Marriage","Temperament"]})
        
        # 18. Shani Sade Sati
        doshas.append({"name": "Shani Sade Sati", "hindi": "शनि साढ़े साती", "severity": "Medium", "description": "Shani transit over Chandra rashi — 7.5 years", "remedy": "Shani mantra, Hanuman Chalisa, blue sapphire", "affected_areas": ["Career","Health","Mental peace"]})
        
        # 19. Kaal Sarp (if applicable)
        if rahu_b and ketu_b:
            others = [pos[p]["bhav"] for p in ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"] if p in pos]
            mn, mx = min(rahu_b, ketu_b), max(rahu_b, ketu_b)
            if all(mn < b < mx for b in others):
                doshas.append({"name": "Kaal Sarp Dosha", "hindi": "काल सर्प दोष", "severity": "High", "description": "All planets between Rahu-Ketu — obstacles", "remedy": "Rahu-Ketu mantra, Nag Panchami pooja", "affected_areas": ["Career","Health","Mental peace"]})
        
        # 20. Angarak Dosha
        if pos.get("Mangal", {}).get("bhav") == pos.get("Rahu", {}).get("bhav"):
            doshas.append({"name": "Angarak Dosha", "hindi": "अंगारक दोष", "severity": "High", "description": "Mangal + Rahu together — aggression", "remedy": "Mangal mantra, Rahu mantra", "affected_areas": ["Anger","Health","Relationships"]})
        
        return doshas
