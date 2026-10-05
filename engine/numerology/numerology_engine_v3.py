"""
Numerology Engine V3 — Complete
Lo Shu Grid, Chaldean, Pythagorean, Name Correction
"""

class NumerologyEngineV3:
    def __init__(self):
        self.chaldean = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":8,"G":3,"H":5,"I":1,"J":1,"K":2,"L":3,"M":4,"N":5,"O":7,"P":8,"Q":1,"R":2,"S":3,"T":4,"U":6,"V":6,"W":6,"X":5,"Y":1,"Z":7}
        self.pythagorean = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":1,"K":2,"L":3,"M":4,"N":5,"O":6,"P":7,"Q":8,"R":9,"S":1,"T":2,"U":3,"V":4,"W":5,"X":6,"Y":7,"Z":8}
        self.planet_map = {1:"Surya",2:"Chandra",3:"Guru",4:"Rahu",5:"Budh",6:"Shukra",7:"Ketu",8:"Shani",9:"Mangal"}
    
    def _reduce(self, n):
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n if n > 0 else 9
    
    def mulank(self, dob):
        try: day = int(dob.split("-")[2])
        except: return {"error": "Invalid DOB"}
        r = self._reduce(day)
        return {"mulank": r, "planet": self.planet_map.get(r, "")}
    
    def bhagyank(self, dob):
        digits = [int(d) for d in dob if d.isdigit()]
        r = self._reduce(sum(digits))
        return {"bhagyank": r, "planet": self.planet_map.get(r, "")}
    
    def name_number(self, name, system="chaldean"):
        table = self.chaldean if system == "chaldean" else self.pythagorean
        total = sum(table.get(c, 0) for c in name.upper() if c.isalpha())
        r = self._reduce(total)
        return {"name_number": r, "planet": self.planet_map.get(r, ""), "system": system}
    
    def lo_shu_grid(self, dob):
        digits = [int(d) for d in dob if d.isdigit() and d != '0']
        grid = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        for d in digits:
            grid[d] = grid.get(d, 0) + 1
        return grid
    
    def full_report(self, dob, name):
        m = self.mulank(dob)
        b = self.bhagyank(dob)
        n = self.name_number(name)
        return {
            "mulank": m,
            "bhagyank": b,
            "name_number": n,
            "lo_shu_grid": self.lo_shu_grid(dob),
            "compatibility": self._compat(m.get("mulank", 0), b.get("bhagyank", 0))
        }
    
    def _compat(self, n1, n2):
        friendly = {1:[1,2,3,5,6,9],2:[1,3,5],3:[1,2,3,5,6,7,9],4:[1,2,5,6,7],5:[1,2,3,5,6,9],6:[1,3,5,6,9],7:[1,2,3,5,6,7],8:[5,6],9:[1,2,3,5,6,9]}
        return {"compatible": n2 in friendly.get(n1, []), "verdict": "Friendly" if n2 in friendly.get(n1, []) else "Neutral"}
