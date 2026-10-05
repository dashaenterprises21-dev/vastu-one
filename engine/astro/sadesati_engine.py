"""
Sadesati Engine — Shani Transit over Chandra Rashi
"""
from datetime import datetime

class SadesatiEngine:
    def __init__(self, positions, rashis):
        self.positions = positions
        self.rashis = rashis
    
    def calculate(self):
        chandra_rashi = self.positions.get("Chandra", {}).get("rashi", "")
        chandra_idx = next((i for i, r in enumerate(self.rashis) if r["name"] == chandra_rashi), 0)
        
        sadesati_rashis = [
            self.rashis[(chandra_idx - 1) % 12]["name"],
            self.rashis[chandra_idx]["name"],
            self.rashis[(chandra_idx + 1) % 12]["name"]
        ]
        
        periods = []
        for i in range(3):
            start_year = 1990 + 29 * (i + 1) - 7
            periods.append({
                "start": str(start_year) + "-01-01",
                "end": str(start_year + 7) + "-01-01",
                "duration_years": 7.5,
                "note": "Shani transit over Chandra rashi"
            })
        
        now = datetime.now().strftime("%Y-%m-%d")
        current = any(p["start"] <= now <= p["end"] for p in periods)
        
        return {
            "chandra_rashi": chandra_rashi,
            "sadesati_rashis": sadesati_rashis,
            "periods": periods,
            "currently_in_sadesati": current,
            "note": "Sadesati occurs when Shani transits over Chandra rashi and adjacent rashis"
        }
