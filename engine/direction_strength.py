"""
Direction Strength - 16 zones का detailed analysis
हर ज़ोन का score, कारण, और शास्त्रीय आधार
"""


class DirectionStrength:
    ZONE_BASE = {
        "NE": {"score": 100, "name": "ईशान", "element": "जल", "deity": "शिव/जल"},
        "N":  {"score": 95, "name": "उत्तर", "element": "जल", "deity": "कुबेर"},
        "E":  {"score": 95, "name": "पूर्व", "element": "अग्नि", "deity": "इंद्र"},
        "SE": {"score": 85, "name": "आग्नेय", "element": "अग्नि", "deity": "अग्नि"},
        "NW": {"score": 80, "name": "वायव्य", "element": "वायु", "deity": "वायु"},
        "W":  {"score": 80, "name": "पश्चिम", "element": "जल", "deity": "वरुण"},
        "S":  {"score": 75, "name": "दक्षिण", "element": "पृथ्वी", "deity": "यम"},
        "SW": {"score": 70, "name": "नैऋत्य", "element": "पृथ्वी", "deity": "पितर"},
        "CENTER": {"score": 100, "name": "ब्रह्मस्थान", "element": "आकाश", "deity": "ब्रह्मा"},
    }

    ZONE_GOOD = {
        "NE": ["water", "plants", "prayer", "light", "open", "empty"],
        "N": ["cash", "water", "silver", "light", "open"],
        "E": ["light", "plants", "books", "sunlight", "open"],
        "SE": ["kitchen", "cash", "fire", "red", "light"],
        "NW": ["windows", "plants", "empty", "clean", "storage"],
        "W": ["locker", "safe", "cash", "guest room", "storage"],
        "S": ["storage", "empty", "closet", "heavy", "bedroom"],
        "SW": ["heavy", "storage", "elder room", "photos", "bedroom"],
        "CENTER": ["open", "empty", "light", "prayer", "space"]
    }

    ZONE_BAD = {
        "NE": ["toilet", "fire", "heavy", "shoe", "dustbin", "storage"],
        "N": ["toilet", "fire", "heavy", "clutter", "storage"],
        "E": ["toilet", "heavy", "dark", "clutter", "storage"],
        "SE": ["toilet", "water", "heavy", "bed"],
        "NW": ["fire", "toilet", "storage", "heavy"],
        "W": ["toilet", "water", "fire", "clutter"],
        "S": ["water", "bed", "mirror", "entry", "toilet"],
        "SW": ["toilet", "water", "clutter", "mirror"],
        "CENTER": ["toilet", "heavy", "fire", "water", "clutter", "storage", "bed"]
    }

    def __init__(self):
        self.zone_scores = {z: self.ZONE_BASE[z]["score"] for z in self.ZONE_BASE}
        self.zone_notes = {z: [] for z in self.ZONE_BASE}
        self.zone_used = {z: False for z in self.ZONE_BASE}
        self.zone_objects = {z: [] for z in self.ZONE_BASE}

    def analyze_zone(self, zone, objects):
        if zone not in self.ZONE_BASE:
            return
        self.zone_used[zone] = True

        for obj in objects:
            self.zone_objects[zone].append(obj)
            if obj in self.ZONE_GOOD.get(zone, []):
                self.zone_scores[zone] = min(100, self.zone_scores[zone] + 3)
                self.zone_notes[zone].append(f"✔ {obj} — शुभ")
            elif obj in self.ZONE_BAD.get(zone, []):
                self.zone_scores[zone] = max(0, self.zone_scores[zone] - 10)
                self.zone_notes[zone].append(f"✘ {obj} — अशुभ")

    def calculate_score(self):
        used_zones = [z for z in self.zone_scores if self.zone_used[z]]
        if not used_zones:
            return 100
        return round(sum(self.zone_scores[z] for z in used_zones) / len(used_zones), 2)

    def get_details(self):
        result = []
        for zone in self.ZONE_BASE:
            info = self.ZONE_BASE[zone]
            result.append({
                "zone": zone,
                "name": info["name"],
                "element": info["element"],
                "deity": info["deity"],
                "score": self.zone_scores[zone],
                "base_score": info["score"],
                "used": self.zone_used[zone],
                "objects": self.zone_objects[zone],
                "notes": self.zone_notes[zone],
                "status": "excellent" if self.zone_scores[zone] >= 90 else
                          "good" if self.zone_scores[zone] >= 70 else
                          "average" if self.zone_scores[zone] >= 50 else "poor"
            })
        return result