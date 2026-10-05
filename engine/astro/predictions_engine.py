"""
Predictions Engine — Career, Marriage, Health, Wealth
"""

class PredictionsEngine:
    def __init__(self, positions, dasha):
        self.positions = positions
        self.dasha = dasha
    
    def generate(self):
        pos = self.positions
        md = self.dasha.get("current_mahadasha", {}).get("planet", "")
        
        career_p = [p for p in pos if pos[p].get("bhav") == 10]
        marriage_p = [p for p in pos if pos[p].get("bhav") == 7]
        health_p = [p for p in pos if pos[p].get("bhav") in [1, 6]]
        wealth_p = [p for p in pos if pos[p].get("bhav") in [2, 11]]
        children_p = [p for p in pos if pos[p].get("bhav") == 5]
        
        return {
            "career": {
                "score": min(100, 70 + len(career_p) * 10),
                "planets_in_10th": career_p,
                "prediction": "10th bhav mein " + str(len(career_p)) + " planets — " + ("strong" if len(career_p) >= 2 else "moderate") + " career",
                "dasha_effect": md + " Mahadasha mein career " + ("growth" if md in ["Guru", "Shukra", "Budh"] else "challenges")
            },
            "marriage": {
                "score": min(100, 70 + len(marriage_p) * 10),
                "planets_in_7th": marriage_p,
                "prediction": "7th bhav mein " + str(len(marriage_p)) + " planets — " + ("early" if len(marriage_p) >= 2 else "delayed") + " marriage",
                "dasha_effect": md + " Mahadasha mein marriage " + ("favorable" if md in ["Guru", "Shukra"] else "needs patience")
            },
            "health": {
                "score": max(40, 85 - len(health_p) * 10),
                "planets_in_1_6": health_p,
                "prediction": "1st/6th bhav mein " + str(len(health_p)) + " planets — " + ("good" if len(health_p) <= 1 else "moderate") + " health",
                "dasha_effect": md + " Mahadasha mein health " + ("good" if md in ["Guru", "Shukra", "Budh", "Chandra"] else "needs care")
            },
            "wealth": {
                "score": min(100, 70 + len(wealth_p) * 10),
                "planets_in_2_11": wealth_p,
                "prediction": "2nd/11th bhav mein " + str(len(wealth_p)) + " planets — " + ("strong" if len(wealth_p) >= 2 else "moderate") + " wealth",
                "dasha_effect": md + " Mahadasha mein wealth " + ("growth" if md in ["Guru", "Shukra"] else "stable")
            },
            "children": {
                "score": min(100, 70 + len(children_p) * 10),
                "planets_in_5th": children_p,
                "prediction": "5th bhav mein " + str(len(children_p)) + " planets — " + ("good" if len(children_p) >= 2 else "moderate") + " progeny",
                "dasha_effect": md + " Mahadasha mein children " + ("favorable" if md in ["Guru", "Chandra"] else "stable")
            }
        }
