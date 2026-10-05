"""
Transit Engine — Current Planetary Transits
"""
from datetime import datetime

class TransitEngine:
    def __init__(self, engine, dob, tob):
        self.engine = engine
        self.dob = dob
        self.tob = tob
    
    def calculate(self):
        now = datetime.now().strftime("%Y-%m-%d")
        transit_pos = self.engine.calculate_positions(now, "12:00")
        natal_pos = self.engine.calculate_positions(self.dob, self.tob)
        
        if "error" in transit_pos or "error" in natal_pos:
            return {"error": "Calculation failed"}
        
        transits = {}
        for planet in transit_pos:
            t = transit_pos[planet]
            n = natal_pos.get(planet, {})
            transits[planet] = {
                "planet": planet,
                "hindi": t.get("hindi", ""),
                "transit_rashi": t.get("rashi", ""),
                "transit_rashi_hindi": t.get("rashi_hindi", ""),
                "natal_rashi": n.get("rashi", ""),
                "same_rashi": t.get("rashi") == n.get("rashi"),
                "note": "Same as natal" if t.get("rashi") == n.get("rashi") else "Different"
            }
        
        return {"transit_date": now, "transits": transits}
