import os

engine_code = '''"""
Vastu Integration Engine v2.0 — Vastu One Enterprise
16-Zone Directional Audit • Element Balance • Room-wise • Property-Dasha Sync
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ENGINE_DIR = os.path.dirname(__file__)

import sys
sys.path.insert(0, ENGINE_DIR)
from advanced_astro_engine import AdvancedAstroEngine


class VastuAstroIntegrationV2:
    """Vastu + Astro Integration v2.0 — Complete Analysis"""

    def __init__(self):
        self.astro = AdvancedAstroEngine()

        # 16-zone mapping
        self.directions_16 = {
            "N": {"hindi": "उत्तर", "angle": 0, "planet": "Budh", "element": "water", "deity": "Kuber"},
            "NNE": {"hindi": "उत्तर-उत्तर-पूर्व", "angle": 22.5, "planet": "Budh", "element": "water", "deity": "Kuber"},
            "NE": {"hindi": "ईशान", "angle": 45, "planet": "Guru", "element": "space", "deity": "Ishaan"},
            "ENE": {"hindi": "पूर्व-उत्तर", "angle": 67.5, "planet": "Surya", "element": "fire", "deity": "Surya"},
            "E": {"hindi": "पूर्व", "angle": 90, "planet": "Surya", "element": "fire", "deity": "Indra"},
            "ESE": {"hindi": "पूर्व-दक्षिण", "angle": 112.5, "planet": "Mangal", "element": "fire", "deity": "Agni"},
            "SE": {"hindi": "आग्नेय", "angle": 135, "planet": "Shukra", "element": "fire", "deity": "Agni"},
            "SSE": {"hindi": "दक्षिण-पूर्व", "angle": 157.5, "planet": "Mangal", "element": "earth", "deity": "Yam"},
            "S": {"hindi": "दक्षिण", "angle": 180, "planet": "Mangal", "element": "earth", "deity": "Yam"},
            "SSW": {"hindi": "दक्षिण-पश्चिम", "angle": 202.5, "planet": "Rahu", "element": "earth", "deity": "Nairutti"},
            "SW": {"hindi": "नैऋत्य", "angle": 225, "planet": "Rahu", "element": "air", "deity": "Nairutti"},
            "WSW": {"hindi": "पश्चिम-दक्षिण", "angle": 247.5, "planet": "Shani", "element": "air", "deity": "Varun"},
            "W": {"hindi": "पश्चिम", "angle": 270, "planet": "Shani", "element": "air", "deity": "Varun"},
            "WNW": {"hindi": "पश्चिम-उत्तर", "angle": 292.5, "planet": "Vayu", "element": "air", "deity": "Vayu"},
            "NW": {"hindi": "वायव्य", "angle": 315, "planet": "Chandra", "element": "air", "deity": "Vayu"},
            "NNW": {"hindi": "उत्तर-पश्चिम", "angle": 337.5, "planet": "Budh", "element": "water", "deity": "Kuber"}
        }

        # Bhadhaka rules
        self.bhadhaka_rules = {
            "Mesh": "Shani", "Vrishabh": "Mangal", "Mithun": "Guru",
            "Kark": "Budh", "Simha": "Shukra", "Kanya": "Chandra",
            "Tula": "Surya", "Vrishchik": "Mangal", "Dhanu": "Guru",
            "Makar": "Budh", "Kumbh": "Shukra", "Meen": "Chandra"
        }

        # Planet directions
        self.planet_direction = {
            "Surya": "E", "Chandra": "NW", "Mangal": "S", "Budh": "N",
            "Guru": "NE", "Shukra": "SE", "Shani": "W", "Rahu": "SW", "Ketu": "NW"
        }

        # Room-wise recommendations
        self.room_rules = {
            "kitchen": {"best": ["SE"], "avoid": ["NE", "N", "NW"], "element": "fire"},
            "bedroom_master": {"best": ["SW"], "avoid": ["NE", "SE"], "element": "earth"},
            "bedroom_children": {"best": ["W", "NW"], "avoid": ["SW", "SE"], "element": "air"},
            "pooja": {"best": ["NE"], "avoid": ["SW", "S"], "element": "space"},
            "toilet": {"best": ["NW", "W"], "avoid": ["NE", "E", "SE"], "element": "air"},
            "living": {"best": ["N", "NE", "E"], "avoid": ["SW", "S"], "element": "water"},
            "dining": {"best": ["SE", "E", "W"], "avoid": ["NE", "SW"], "element": "fire"},
            "study": {"best": ["NE", "E", "N"], "avoid": ["SW", "S"], "element": "space"},
            "cash": {"best": ["N", "NE"], "avoid": ["S", "SW", "SE"], "element": "water"},
            "water_source": {"best": ["NE"], "avoid": ["SW", "SE"], "element": "water"},
            "staircase": {"best": ["SW", "S", "W"], "avoid": ["NE", "E", "N"], "element": "earth"}
        }

    # ═══════════════════════════════════════════
    # 1. BHADHAKA PLANET
    # ═══════════════════════════════════════════
    def calculate_bhadhaka(self, dob: str, tob: str, place: str) -> Dict:
        lagna = self.astro.calculate_lagna(dob, tob, place)
        if "error" in lagna:
            return lagna
        lagna_rashi = lagna.get("lagna_rashi", "")
        bhadhaka_planet = self.bhadhaka_rules.get(lagna_rashi, "Shani")
        bhadhaka_direction = self.planet_direction.get(bhadhaka_planet, "W")
        direction_info = self.directions_16.get(bhadhaka_direction, {})
        return {
            "lagna_rashi": lagna_rashi,
            "lagna_hindi": lagna.get("lagna_hindi", ""),
            "bhadhaka_planet": bhadhaka_planet,
            "bhadhaka_hindi": self.astro.planets.get(bhadhaka_planet, {}).get("hindi", bhadhaka_planet),
            "bhadhaka_direction": bhadhaka_direction,
            "bhadhaka_direction_hindi": direction_info.get("hindi", ""),
            "bhadhaka_element": direction_info.get("element", ""),
            "bhadhaka_deity": direction_info.get("deity", ""),
            "note": "Bhadhaka planet causes obstacles in its direction"
        }

    # ═══════════════════════════════════════════
    # 2. MAIN DOOR ANALYSIS (detailed)
    # ═══════════════════════════════════════════
    def analyze_main_door(self, main_door_direction: str) -> Dict:
        direction = main_door_direction.upper()
        info = self.directions_16.get(direction, {})
        if not info:
            return {"error": f"Invalid direction: {direction}"}

        # Door type (from entrance_padas)
        door_types = {
            "N": "Mukhya Dwar — Budh, wealth",
            "NE": "Ishaan Dwar — Guru, most auspicious",
            "E": "Surya Dwar — health, vitality",
            "SE": "Agni Dwar — fire, energy",
            "S": "Yam Dwar — discipline",
            "SW": "Nairutti Dwar — Rahu, obstacles",
            "W": "Varun Dwar — Shani, delays",
            "NW": "Vayu Dwar — Chandra, mental peace"
        }

        auspicious_dirs = ["N", "NE", "E", "NW", "NNE", "ENE", "NNW"]
        return {
            "direction": direction,
            "hindi": info.get("hindi", ""),
            "angle": info.get("angle", 0),
            "element": info.get("element", ""),
            "planet": info.get("planet", ""),
            "planet_hindi": self.astro.planets.get(info.get("planet", ""), {}).get("hindi", ""),
            "deity": info.get("deity", ""),
            "auspicious": direction in auspicious_dirs,
            "door_type": door_types.get(direction[:2] if direction[:2] in door_types else direction[0], ""),
            "note": self._door_note(direction)
        }

    def _door_note(self, direction: str) -> str:
        notes = {
            "N": "Auspicious — Budh, wealth and communication",
            "NE": "Most auspicious — Guru, wisdom and prosperity",
            "E": "Auspicious — Surya, health and vitality",
            "SE": "Acceptable — Shukra, but fire element",
            "S": "Acceptable — Mangal, but avoid if possible",
            "SW": "Avoid — Rahu, causes obstacles",
            "W": "Acceptable — Shani, but delays",
            "NW": "Auspicious — Chandra, mental peace"
        }
        return notes.get(direction, "Neutral")

    # ═══════════════════════════════════════════
    # 3. BHADHAKA vs MAIN DOOR
    # ═══════════════════════════════════════════
    def compare_bhadhaka_door(self, dob: str, tob: str, place: str, main_door_direction: str) -> Dict:
        bhadhaka = self.calculate_bhadhaka(dob, tob, place)
        door = self.analyze_main_door(main_door_direction)
        if "error" in bhadhaka or "error" in door:
            return {"error": "Invalid input"}

        bhadhaka_dir = bhadhaka.get("bhadhaka_direction", "")
        door_dir = door.get("direction", "")
        match = bhadhaka_dir == door_dir
        adjacent = self._is_adjacent(bhadhaka_dir, door_dir)

        if match:
            severity = "Critical"
            message = f"Bhadhaka planet ({bhadhaka['bhadhaka_planet']}) ki direction ({bhadhaka_dir}) mein main door hai — serious obstacle"
            remedy = f"Main door ko {self._alternative_direction(bhadhaka_dir)} direction mein shift karo, ya {bhadhaka['bhadhaka_planet']} ke liye Vastu remedy karo"
        elif adjacent:
            severity = "High"
            message = f"Bhadhaka direction ({bhadhaka_dir}) aur main door ({door_dir}) adjacent hain — moderate obstacle"
            remedy = f"{bhadhaka['bhadhaka_planet']} ke liye Vastu remedy karo, ya door ke paas {bhadhaka['bhadhaka_element']} element balance karo"
        else:
            severity = "Low"
            message = f"Bhadhaka direction ({bhadhaka_dir}) aur main door ({door_dir}) alag hain — koi major issue nahi"
            remedy = "Koi immediate remedy nahi chahiye"

        return {
            "bhadhaka": bhadhaka,
            "main_door": door,
            "match": match,
            "adjacent": adjacent,
            "severity": severity,
            "message": message,
            "remedy": remedy,
            "affected_areas": self._affected_areas(bhadhaka['bhadhaka_planet'])
        }

    def _is_adjacent(self, dir1: str, dir2: str) -> bool:
        directions = list(self.directions_16.keys())
        if dir1 in directions and dir2 in directions:
            i1, i2 = directions.index(dir1), directions.index(dir2)
            diff = abs(i1 - i2)
            return diff == 1 or diff == 15
        return False

    def _alternative_direction(self, direction: str) -> str:
        alternatives = {"N": "NE or E", "NE": "N or E", "E": "NE or N", "SE": "E or S", "S": "SE or SW", "SW": "S or W", "W": "SW or NW", "NW": "W or N"}
        return alternatives.get(direction, "NE")

    def _affected_areas(self, planet: str) -> List[str]:
        areas = {
            "Surya": ["Father", "Authority", "Health", "Career"],
            "Chandra": ["Mother", "Emotions", "Mental peace", "Travel"],
            "Mangal": ["Marriage", "Property", "Courage", "Siblings"],
            "Budh": ["Communication", "Business", "Education", "Friends"],
            "Guru": ["Wisdom", "Children", "Luck", "Wealth"],
            "Shukra": ["Marriage", "Luxury", "Creativity", "Vehicles"],
            "Shani": ["Career", "Longevity", "Discipline", "Delays"],
            "Rahu": ["Obstacles", "Foreign", "Technology", "Confusion"],
            "Ketu": ["Spirituality", "Detachment", "Health", "Past life"]
        }
        return areas.get(planet, [])

    # ═══════════════════════════════════════════
    # 4. DASHA ALERT
    # ═══════════════════════════════════════════
    def dasha_alert(self, dob: str, tob: str, place: str, main_door_direction: str = "N") -> Dict:
        dasha = self.astro.vimshottari_dasha_detailed(dob)
        if "error" in dasha:
            return dasha
        current_md = dasha.get("current_mahadasha", {})
        current_ad = dasha.get("current_antardasha", {})
        md_planet = current_md.get("planet", "")
        ad_planet = current_ad.get("planet", "")
        md_direction = self.planet_direction.get(md_planet, "")
        ad_direction = self.planet_direction.get(ad_planet, "")
        door_dir = main_door_direction.upper()
        md_match = md_direction == door_dir
        ad_match = ad_direction == door_dir

        alerts = []
        if md_match:
            alerts.append({"type": "Critical", "message": f"Mahadasha planet ({md_planet}) ki direction ({md_direction}) mein main door hai — problems", "remedy": f"{md_planet} ke liye Vastu remedy karo"})
        if ad_match:
            alerts.append({"type": "High", "message": f"Antardasha planet ({ad_planet}) ki direction ({ad_direction}) mein main door hai", "remedy": f"{ad_planet} ke liye remedy karo"})

        return {
            "current_mahadasha": {"planet": md_planet, "hindi": current_md.get("hindi", ""), "direction": md_direction, "direction_hindi": self.directions_16.get(md_direction, {}).get("hindi", ""), "period": f"{current_md.get('start_date', '')} → {current_md.get('end_date', '')}", "age": f"{current_md.get('start_age', 0)} - {current_md.get('end_age', 0)}"},
            "current_antardasha": {"planet": ad_planet, "hindi": current_ad.get("hindi", ""), "direction": ad_direction, "direction_hindi": self.directions_16.get(ad_direction, {}).get("hindi", ""), "period": f"{current_ad.get('start_date', '')} → {current_ad.get('end_date', '')}"},
            "main_door_direction": door_dir,
            "alerts": alerts,
            "overall_status": "Alert" if alerts else "Safe"
        }

    # ═══════════════════════════════════════════
    # 5. 16-ZONE DIRECTIONAL AUDIT
    # ═══════════════════════════════════════════
    def zone_audit_16(self, dob: str, tob: str, place: str, main_door_direction: str) -> Dict:
        """16-zone directional audit with planet strength"""
        grah_pos = self.astro.calculate_grah_positions(dob, tob, place)
        bhadhaka = self.calculate_bhadhaka(dob, tob, place)
        door_dir = main_door_direction.upper()
        bhadhaka_dir = bhadhaka.get("bhadhaka_direction", "")

        zones = {}
        for direction, info in self.directions_16.items():
            planet = info.get("planet", "")
            planet_info = grah_pos.get(planet, {})
            planet_status = planet_info.get("status", "Unknown")

            # Zone score
            score = 70
            if direction == bhadhaka_dir:
                score -= 30  # Bhadhaka direction
            if direction == door_dir:
                score -= 20 if not self.analyze_main_door(direction).get("auspicious") else 0
            if planet_status == "Strong":
                score += 15
            elif planet_status == "Weak":
                score -= 15

            score = max(0, min(100, score))

            zones[direction] = {
                "direction": direction,
                "hindi": info.get("hindi", ""),
                "angle": info.get("angle", 0),
                "planet": planet,
                "planet_hindi": self.astro.planets.get(planet, {}).get("hindi", planet),
                "planet_status": planet_status,
                "element": info.get("element", ""),
                "deity": info.get("deity", ""),
                "score": score,
                "status": "Strong" if score >= 70 else ("Moderate" if score >= 50 else "Weak"),
                "is_bhadhaka": direction == bhadhaka_dir,
                "is_main_door": direction == door_dir
            }

        avg = round(sum(z["score"] for z in zones.values()) / len(zones), 2)
        return {"zones": zones, "average_score": avg, "strong_zones": [d for d, z in zones.items() if z["score"] >= 70], "weak_zones": [d for d, z in zones.items() if z["score"] < 50]}

    # ═══════════════════════════════════════════
    # 6. 5-ELEMENT BALANCE
    # ═══════════════════════════════════════════
    def element_balance(self, dob: str, tob: str, place: str) -> Dict:
        """5-element balance analysis"""
        grah_pos = self.astro.calculate_grah_positions(dob, tob, place)
        elements = {"fire": [], "earth": [], "air": [], "water": [], "space": []}

        for direction, info in self.directions_16.items():
            element = info.get("element", "")
            planet = info.get("planet", "")
            planet_status = grah_pos.get(planet, {}).get("status", "Moderate")
            score = 75 if planet_status == "Strong" else (50 if planet_status == "Moderate" else 30)
            if element in elements:
                elements[element].append(score)

        result = {}
        for element, scores in elements.items():
            if scores:
                avg = round(sum(scores) / len(scores), 2)
                result[element] = {
                    "avg_score": avg,
                    "count": len(scores),
                    "status": "Balanced ✅" if 50 <= avg <= 85 else ("Excess ⚠️" if avg > 85 else "Deficient 🔴"),
                    "remedy": self._element_remedy(element, avg)
                }
        return result

    def _element_remedy(self, element: str, score: float) -> str:
        if score >= 50:
            return f"{element.title()} balanced — maintain"
        remedies = {
            "fire": "Add fire element — candles, red color",
            "earth": "Add earth element — heavy items, yellow",
            "air": "Add air element — wind chimes, white",
            "water": "Add water element — fountain, blue",
            "space": "Add space element — keep clean, yellow"
        }
        return remedies.get(element, "Balance element")

    # ═══════════════════════════════════════════
    # 7. ROOM-WISE RECOMMENDATIONS
    # ═══════════════════════════════════════════
    def room_recommendations(self, dob: str, tob: str, place: str, main_door_direction: str) -> Dict:
        """Room-wise Vastu recommendations"""
        recommendations = {}
        for room, rules in self.room_rules.items():
            best = rules["best"]
            avoid = rules["avoid"]
            recommendations[room] = {
                "room": room.replace("_", " ").title(),
                "best_directions": best,
                "avoid_directions": avoid,
                "element": rules["element"],
                "current_status": "Unknown (property input needed)",
                "remedy": f"Place {room} in {best[0]} direction, avoid {avoid[0]}"
            }
        return recommendations

    # ═══════════════════════════════════════════
    # 8. PROPERTY-DASHA SYNCHRONICITY
    # ═══════════════════════════════════════════
    def property_dasha_sync(self, dob: str, tob: str, place: str, main_door_direction: str) -> Dict:
        """Property direction + current dasha match"""
        dasha = self.astro.vimshottari_dasha_detailed(dob)
        if "error" in dasha:
            return dasha
        current_md = dasha.get("current_mahadasha", {})
        md_planet = current_md.get("planet", "")
        md_direction = self.planet_direction.get(md_planet, "")
        door_dir = main_door_direction.upper()
        match = md_direction == door_dir

        return {
            "current_mahadasha": md_planet,
            "md_direction": md_direction,
            "main_door": door_dir,
            "match": match,
            "synchronicity": "High ✅" if match else "Low ⚠️",
            "message": f"Mahadasha planet {md_planet} ki direction {md_direction} — main door {door_dir}" + (" — MATCH! Alert!" if match else " — No conflict")
        }

    # ═══════════════════════════════════════════
    # 9. PRIORITY REMEDIES
    # ═══════════════════════════════════════════
    def priority_remedies(self, dob: str, tob: str, place: str, main_door_direction: str) -> List[Dict]:
        """Priority-based remedies (High/Medium/Low)"""
        bhadhaka = self.calculate_bhadhaka(dob, tob, place)
        comparison = self.compare_bhadhaka_door(dob, tob, place, main_door_direction)
        dasha = self.dasha_alert(dob, tob, place, main_door_direction)

        remedies = []
        # Critical: Bhadhaka matches door
        if comparison.get("severity") == "Critical":
            remedies.append({"priority": "HIGH", "category": "Bhadhaka-Door Conflict", "remedy": comparison.get("remedy", ""), "cost": "High", "duration": "Immediate"})
        # High: Dasha alert
        if dasha.get("overall_status") == "Alert":
            for alert in dasha.get("alerts", []):
                remedies.append({"priority": "HIGH" if alert["type"] == "Critical" else "MEDIUM", "category": "Dasha Alert", "remedy": alert.get("remedy", ""), "cost": "Medium", "duration": "Current dasha"})
        # Medium: Bhadhaka remedies
        if bhadhaka.get("bhadhaka_planet"):
            remedies.append({"priority": "MEDIUM", "category": "Bhadhaka Planet Remedy", "remedy": f"{bhadhaka['bhadhaka_planet']} ke liye mantra, gemstone, daan", "cost": "Low-Medium", "duration": "Ongoing"})
        # Low: General
        remedies.append({"priority": "LOW", "category": "General Vastu", "remedy": "Keep all zones clean, maintain element balance", "cost": "Low", "duration": "Daily"})

        return remedies

    # ═══════════════════════════════════════════
    # 10. VASTU REMEDIES (detailed)
    # ═══════════════════════════════════════════
    def vastu_remedies(self, bhadhaka_planet: str, main_door_direction: str) -> Dict:
        direction = self.planet_direction.get(bhadhaka_planet, "")
        direction_info = self.directions_16.get(direction, {})
        element = direction_info.get("element", "")

        remedies = {
            "bhadhaka_planet": bhadhaka_planet,
            "bhadhaka_hindi": self.astro.planets.get(bhadhaka_planet, {}).get("hindi", bhadhaka_planet),
            "bhadhaka_direction": direction,
            "bhadhaka_direction_hindi": direction_info.get("hindi", ""),
            "element": element,
            "remedies": []
        }

        element_remedies = {
            "fire": ["Red/orange color in this zone", "Fire element items (candles, diya)", "Avoid water in this zone"],
            "earth": ["Yellow/brown color", "Heavy items, earth element", "Avoid water and fire"],
            "air": ["White/grey color", "Metal items, wind chimes", "Keep this zone clean and light"],
            "water": ["Blue/black color", "Water fountain, aquarium", "Avoid fire in this zone"],
            "space": ["Yellow color", "Keep clean and empty", "Guru mantra, yellow flowers"]
        }
        remedies["remedies"] = element_remedies.get(element, [])

        planet_remedies = {
            "Surya": ["Surya mantra", "Aditya Hridayam", "Ruby (consult astrologer)"],
            "Chandra": ["Chandra mantra", "Silver items", "Pearl (consult astrologer)"],
            "Mangal": ["Mangal mantra", "Hanuman Chalisa", "Red coral (consult astrologer)"],
            "Budh": ["Budh mantra", "Green items", "Emerald (consult astrologer)"],
            "Guru": ["Guru mantra", "Yellow items", "Yellow sapphire (consult astrologer)"],
            "Shukra": ["Shukra mantra", "White items", "Diamond (consult astrologer)"],
            "Shani": ["Shani mantra", "Hanuman Chalisa", "Blue sapphire (consult astrologer)"],
            "Rahu": ["Rahu mantra", "Durga pooja", "Hessonite (consult astrologer)"],
            "Ketu": ["Ketu mantra", "Ganesh pooja", "Cat's eye (consult astrologer)"]
        }
        remedies["planet_remedies"] = planet_remedies.get(bhadhaka_planet, [])

        door_info = self.analyze_main_door(main_door_direction)
        remedies["main_door"] = {
            "direction": main_door_direction,
            "hindi": door_info.get("hindi", ""),
            "planet": door_info.get("planet", ""),
            "auspicious": door_info.get("auspicious", False),
            "note": door_info.get("note", ""),
            "remedies": self._door_remedies(main_door_direction)
        }
        return remedies

    def _door_remedies(self, direction: str) -> List[str]:
        remedies = {
            "N": ["Water fountain near door", "Blue color", "Budh mantra"],
            "NE": ["Keep clean", "Yellow flowers", "Guru mantra"],
            "E": ["Sunrise visibility", "Red color", "Surya mantra"],
            "SE": ["Fire element", "Red/orange", "Shukra mantra"],
            "S": ["Red color", "Mangal mantra", "Avoid water"],
            "SW": ["Heavy items", "Earth element", "Rahu mantra"],
            "W": ["Metal items", "Grey color", "Shani mantra"],
            "NW": ["White color", "Air element", "Chandra mantra"]
        }
        base = direction[:2] if direction[:2] in remedies else direction[0]
        return remedies.get(base, ["Keep clean", "Auspicious items"])

    # ═══════════════════════════════════════════
    # 11. FULL INTEGRATION REPORT (v2.0)
    # ═══════════════════════════════════════════
    def full_integration_report(self, dob: str, tob: str, place: str, main_door_direction: str = "N") -> Dict:
        """Complete Vastu + Astro Integration Report v2.0"""
        bhadhaka = self.calculate_bhadhaka(dob, tob, place)
        door = self.analyze_main_door(main_door_direction)
        comparison = self.compare_bhadhaka_door(dob, tob, place, main_door_direction)
        alert = self.dasha_alert(dob, tob, place, main_door_direction)
        remedies = self.vastu_remedies(bhadhaka.get("bhadhaka_planet", ""), main_door_direction)
        zones = self.zone_audit_16(dob, tob, place, main_door_direction)
        elements = self.element_balance(dob, tob, place)
        rooms = self.room_recommendations(dob, tob, place, main_door_direction)
        sync = self.property_dasha_sync(dob, tob, place, main_door_direction)
        priority = self.priority_remedies(dob, tob, place, main_door_direction)

        # Integration score
        score = 100
        if comparison.get("severity") == "Critical": score -= 40
        elif comparison.get("severity") == "High": score -= 25
        elif comparison.get("severity") == "Low": score -= 5
        if alert.get("overall_status") == "Alert": score -= 20
        score = max(0, min(100, score))

        return {
            "bhadhaka": bhadhaka,
            "main_door": door,
            "comparison": comparison,
            "dasha_alert": alert,
            "remedies": remedies,
            "zone_audit": zones,
            "element_balance": elements,
            "room_recommendations": rooms,
            "property_dasha_sync": sync,
            "priority_remedies": priority,
            "integration_score": {"total_score": score, "grade": self._grade(score), "status": self._status(score)},
            "summary": {
                "bhadhaka_planet": bhadhaka.get("bhadhaka_planet", ""),
                "main_door": main_door_direction,
                "severity": comparison.get("severity", ""),
                "dasha_status": alert.get("overall_status", ""),
                "overall": self._status(score)
            }
        }

    def _grade(self, score: float) -> str:
        if score >= 85: return "A+ (Excellent)"
        if score >= 70: return "A (Good)"
        if score >= 55: return "B (Average)"
        if score >= 40: return "C (Below Average)"
        return "D (Poor)"

    def _status(self, score: float) -> str:
        if score >= 85: return "Excellent Integration ✅"
        if score >= 70: return "Good Integration ✅"
        if score >= 55: return "Average Integration ⚠️"
        if score >= 40: return "Needs Improvement ⚠️"
        return "Critical 🔴"


if __name__ == "__main__":
    engine = VastuAstroIntegrationV2()
    print("=" * 60)
    print("VASTU-ASTRO INTEGRATION ENGINE v2.0 — DETAILED")
    print("=" * 60)

    dob, tob, place = "1990-05-04", "21:35", "Bhandara"
    door = "SW"

    report = engine.full_integration_report(dob, tob, place, door)

    print("\\n1. INTEGRATION SCORE:")
    print(json.dumps(report["integration_score"], indent=2, ensure_ascii=False))

    print("\\n2. ZONE AUDIT (16 zones):")
    zones = report["zone_audit"]
    print(f"   Average: {zones['average_score']}")
    print(f"   Strong: {zones['strong_zones']}")
    print(f"   Weak: {zones['weak_zones']}")

    print("\\n3. ELEMENT BALANCE:")
    for e, d in report["element_balance"].items():
        print(f"   {e}: {d['avg_score']} — {d['status']}")

    print("\\n4. PROPERTY-DASHA SYNC:")
    print(json.dumps(report["property_dasha_sync"], indent=2, ensure_ascii=False))

    print("\\n5. PRIORITY REMEDIES:")
    for r in report["priority_remedies"]:
        print(f"   [{r['priority']}] {r['category']}: {r['remedy'][:60]}...")

    print("\\n✅ Vastu-Astro Integration Engine v2.0 working!")
'''

with open("engine/vastu_astro_integration.py", "w", encoding="utf-8") as f:
    f.write(engine_code)
print("vastu_astro_integration.py:", os.path.getsize("engine/vastu_astro_integration.py"), "bytes")
