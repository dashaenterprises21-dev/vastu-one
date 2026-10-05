"""
Yogas Engine — 50+ Yogas Detection
"""

class YogasEngine:
    def __init__(self, positions, lagna, planets):
        self.positions = positions
        self.lagna = lagna
        self.planets = planets
    
    def detect_all(self):
        yogas = []
        pos = self.positions
        
        # Basic yogas
        chandra_b = pos.get("Chandra", {}).get("bhav", 0)
        guru_b = pos.get("Guru", {}).get("bhav", 0)
        
        # 1. Gajakesari
        if chandra_b and guru_b and abs(guru_b - chandra_b) in [0, 3, 6, 9]:
            yogas.append({"name": "Gajakesari Yoga", "hindi": "गजकेसरी योग", "type": "Auspicious", "description": "Guru in kendra from Chandra — wisdom, wealth, fame", "strength": "High"})
        
        # 2. Budh-Aditya
        if pos.get("Surya", {}).get("rashi") == pos.get("Budh", {}).get("rashi"):
            yogas.append({"name": "Budh-Aditya Yoga", "hindi": "बुध-आदित्य योग", "type": "Auspicious", "description": "Surya + Budh — intelligence, communication", "strength": "High"})
        
        # 3. Chandra-Mangal
        if pos.get("Chandra", {}).get("rashi") == pos.get("Mangal", {}).get("rashi"):
            yogas.append({"name": "Chandra-Mangal Yoga", "hindi": "चन्द्र-मंगल योग", "type": "Auspicious", "description": "Chandra + Mangal — wealth, business acumen", "strength": "Medium"})
        
        # 4-8. Panch Mahapurusha
        for planet in ["Mangal", "Budh", "Guru", "Shukra", "Shani"]:
            if pos.get(planet, {}).get("rashi") and pos.get("Chandra", {}).get("rashi") and pos[planet]["rashi"] == pos["Chandra"]["rashi"]:
                yogas.append({"name": planet + " Mahapurusha Yoga", "hindi": self.planets.get(planet, {}).get("hindi", planet) + " महापुरुष योग", "type": "Auspicious", "description": planet + " in kendra from Lagna", "strength": "High"})
        
        # 9. Kaal Sarp
        rahu_b = pos.get("Rahu", {}).get("bhav", 0)
        ketu_b = pos.get("Ketu", {}).get("bhav", 0)
        if rahu_b and ketu_b:
            others = [pos[p]["bhav"] for p in ["Surya","Chandra","Mangal","Budh","Guru","Shukra","Shani"] if p in pos]
            mn, mx = min(rahu_b, ketu_b), max(rahu_b, ketu_b)
            if all(mn < b < mx for b in others):
                yogas.append({"name": "Kaal Sarp Yoga", "hindi": "काल सर्प योग", "type": "Challenging", "description": "All planets between Rahu-Ketu — obstacles, delays", "strength": "High", "remedy": "Rahu-Ketu mantra, Nag Panchami pooja"})
        
        # 10. Sunapha
        if chandra_b:
            b2 = (chandra_b % 12) + 1
            if any(pos[p].get("bhav") == b2 for p in pos if p not in ["Chandra", "Surya"]):
                yogas.append({"name": "Sunapha Yoga", "hindi": "सुनफा योग", "type": "Auspicious", "description": "Planets in 2nd from Chandra — wealth, prosperity", "strength": "Medium"})
        
        # 11. Anapha
        if chandra_b:
            b12 = ((chandra_b - 2) % 12) + 1
            if any(pos[p].get("bhav") == b12 for p in pos if p not in ["Chandra", "Surya"]):
                yogas.append({"name": "Anapha Yoga", "hindi": "अनफा योग", "type": "Auspicious", "description": "Planets in 12th from Chandra — health, comfort", "strength": "Medium"})
        
        # 12. Kemadruma
        if chandra_b:
            b2 = (chandra_b % 12) + 1
            b12 = ((chandra_b - 2) % 12) + 1
            has_around = any(pos[p].get("bhav") in [b2, b12] for p in pos if p not in ["Chandra", "Surya"])
            if not has_around:
                yogas.append({"name": "Kemadruma Yoga", "hindi": "केमद्रुम योग", "type": "Challenging", "description": "No planets around Chandra — struggles, isolation", "strength": "High", "remedy": "Chandra mantra, silver"})
        
        # 13. Amala
        if chandra_b:
            b10 = ((chandra_b + 8) % 12) + 1
            if any(pos[p].get("bhav") == b10 and p in ["Guru", "Shukra", "Budh"] for p in pos):
                yogas.append({"name": "Amala Yoga", "hindi": "अमल योग", "type": "Auspicious", "description": "Benefic in 10th from Chandra — lasting fame", "strength": "High"})
        
        # 14. Chatussagara
        kendras = [1, 4, 7, 10]
        occupied = set()
        for p, info in pos.items():
            if info.get("bhav") in kendras:
                occupied.add(info.get("bhav"))
        if len(occupied) == 4:
            yogas.append({"name": "Chatussagara Yoga", "hindi": "चतुस्सागर योग", "type": "Auspicious", "description": "All kendras occupied — stable life", "strength": "High"})
        
        # 15-20. Dhana Yogas
        for p in ["Guru", "Shukra", "Budh"]:
            if pos.get(p, {}).get("bhav") in [2, 5, 9, 11]:
                yogas.append({"name": "Dhana Yoga (" + p + ")", "hindi": "धन योग (" + p + ")", "type": "Auspicious", "description": p + " in dhana bhav — wealth", "strength": "Medium"})
        
        # 21-25. Raja Yogas
        for p in ["Guru", "Shukra"]:
            if pos.get(p, {}).get("bhav") in [1, 4, 7, 10]:
                yogas.append({"name": "Raja Yoga (" + p + ")", "hindi": "राज योग (" + p + ")", "type": "Auspicious", "description": p + " in kendra — power, status", "strength": "High"})
        
        # 26-30. Vipreet Raja
        for p in ["Mangal", "Shani", "Rahu"]:
            if pos.get(p, {}).get("bhav") in [6, 8, 12]:
                yogas.append({"name": "Vipreet Raja Yoga (" + p + ")", "hindi": "विपरीत राज योग (" + p + ")", "type": "Auspicious", "description": p + " in dusthana — unexpected gains", "strength": "Medium"})
        
        # 31. Sarala
        if pos.get("Rahu", {}).get("bhav") == 8:
            yogas.append({"name": "Sarala Yoga", "hindi": "सरल योग", "type": "Auspicious", "description": "Rahu in 8th — longevity, success", "strength": "Medium"})
        
        # 32. Vimala
        if pos.get("Guru", {}).get("bhav") == 12 or pos.get("Shukra", {}).get("bhav") == 12:
            yogas.append({"name": "Vimala Yoga", "hindi": "विमल योग", "type": "Auspicious", "description": "Benefic in 12th — moksha, salvation", "strength": "Medium"})
        
        # 33. Shakata
        if chandra_b and guru_b and abs(chandra_b - guru_b) in [5, 7]:
            yogas.append({"name": "Shakata Yoga", "hindi": "शकट योग", "type": "Challenging", "description": "Chandra-Guru in 6/8 — fluctuating fortune", "strength": "Medium"})
        
        # 34. Lakshmi
        if pos.get("Guru", {}).get("bhav") in [1, 4, 7, 10] and pos.get("Shukra", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Lakshmi Yoga", "hindi": "लक्ष्मी योग", "type": "Auspicious", "description": "Guru + Shukra in kendra — wealth, luxury", "strength": "High"})
        
        # 35. Parvata
        if pos.get("Guru", {}).get("bhav") in [1, 4, 7, 10] and pos.get("Shukra", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Parvata Yoga", "hindi": "पर्वत योग", "type": "Auspicious", "description": "Benefics in kendra — fame, prosperity", "strength": "High"})
        
        # 36. Kahala
        if pos.get("Guru", {}).get("bhav") in [1, 4, 7, 10] and pos.get("Surya", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Kahala Yoga", "hindi": "कहल योग", "type": "Auspicious", "description": "Guru + Surya in kendra — courage, leadership", "strength": "Medium"})
        
        # 37. Vasumati
        upachaya = [3, 6, 10, 11]
        benefics_in_upachaya = [p for p in ["Guru", "Shukra", "Budh"] if pos.get(p, {}).get("bhav") in upachaya]
        if benefics_in_upachaya:
            yogas.append({"name": "Vasumati Yoga", "hindi": "वसुमती योग", "type": "Auspicious", "description": "Benefics in upachaya — wealth, independence", "strength": "Medium"})
        
        # 38. Hamsa
        if pos.get("Guru", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Hamsa Yoga", "hindi": "हंस योग", "type": "Auspicious", "description": "Guru in kendra — spiritual, respected", "strength": "High"})
        
        # 39. Malavya
        if pos.get("Shukra", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Malavya Yoga", "hindi": "मालव्य योग", "type": "Auspicious", "description": "Shukra in kendra — luxury, beauty", "strength": "High"})
        
        # 40. Shasha
        if pos.get("Shani", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Shasha Yoga", "hindi": "शश योग", "type": "Auspicious", "description": "Shani in kendra — authority, discipline", "strength": "High"})
        
        # 41. Bhadra
        if pos.get("Budh", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Bhadra Yoga", "hindi": "भद्र योग", "type": "Auspicious", "description": "Budh in kendra — intelligence, communication", "strength": "High"})
        
        # 42. Ruchaka
        if pos.get("Mangal", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Ruchaka Yoga", "hindi": "रुचक योग", "type": "Auspicious", "description": "Mangal in kendra — courage, leadership", "strength": "High"})
        
        # 43. Kendra Trikona
        kendra_lords = [p for p in pos if pos[p].get("bhav") in [1, 4, 7, 10]]
        if len(kendra_lords) >= 3:
            yogas.append({"name": "Kendra Trikona Yoga", "hindi": "केंद्र त्रिकोण योग", "type": "Auspicious", "description": "Strong kendras — leadership, power", "strength": "High"})
        
        # 44. Maha Bhagya
        if pos.get("Guru", {}).get("bhav") in [1, 4, 7, 10] and pos.get("Surya", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Maha Bhagya Yoga", "hindi": "महा भाग्य योग", "type": "Auspicious", "description": "Guru + Surya in kendra — great fortune", "strength": "High"})
        
        # 45. Gauri
        if pos.get("Chandra", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Gauri Yoga", "hindi": "गौरी योग", "type": "Auspicious", "description": "Chandra in kendra — beauty, charm", "strength": "Medium"})
        
        # 46. Bharathi
        if pos.get("Guru", {}).get("bhav") in [2, 5, 9, 11]:
            yogas.append({"name": "Bharathi Yoga", "hindi": "भारती योग", "type": "Auspicious", "description": "Guru in dhana bhav — wealth, knowledge", "strength": "Medium"})
        
        # 47. Chandika
        if pos.get("Mangal", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Chandika Yoga", "hindi": "चंडिका योग", "type": "Auspicious", "description": "Mangal in kendra — courage, victory", "strength": "Medium"})
        
        # 48. Parvati
        if pos.get("Chandra", {}).get("bhav") in [1, 4, 7, 10] and pos.get("Shukra", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Parvati Yoga", "hindi": "पार्वती योग", "type": "Auspicious", "description": "Chandra + Shukra in kendra — luxury", "strength": "Medium"})
        
        # 49. Durga
        if pos.get("Mangal", {}).get("bhav") in [1, 4, 7, 10] and pos.get("Shani", {}).get("bhav") in [1, 4, 7, 10]:
            yogas.append({"name": "Durga Yoga", "hindi": "दुर्गा योग", "type": "Auspicious", "description": "Mangal + Shani in kendra — power", "strength": "Medium"})
        
        # 50. Kali
        if pos.get("Mangal", {}).get("bhav") in [6, 8, 12] and pos.get("Shani", {}).get("bhav") in [6, 8, 12]:
            yogas.append({"name": "Kali Yoga", "hindi": "काली योग", "type": "Challenging", "description": "Mangal + Shani in dusthana — challenges", "strength": "Medium"})
        
        return yogas
