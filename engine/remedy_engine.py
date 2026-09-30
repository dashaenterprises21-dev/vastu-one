"""
हिडन रेमेडी जनरेटर
"""

class RemedyEngine:
    def __init__(self, devatas_json, elements_json):
        self.devata_map = {}
        for d in devatas_json["outer_devatas"] + devatas_json["inner_devatas"]:
            self.devata_map[d["name"]] = d
        self.elements = {e["name"]: e for e in elements_json["elements"]}

    def remedy_for_devata(self, devata_name):
        devata = self.devata_map.get(devata_name)
        if not devata:
            return None
        element = self.elements.get(devata["element"].capitalize())
        return {
            "devata": devata_name,
            "hindi": devata["hindi"],
            "direction": devata["direction"],
            "problem_domain": devata["domain"],
            "remedy": {
                "element_balance": element["remedies"] if element else [],
                "positive_objects": devata["positive_objects"],
                "avoid": devata["negative_objects"],
                "color": element["color"] if element else [],
                "mantra": f"Om {devata_name}aya Namaha",
                "puja_direction": devata["direction"]
            }
        }

    def remedy_for_element(self, element_name):
        element = self.elements.get(element_name)
        if not element:
            return None
        return {
            "element": element_name,
            "hindi": element["hindi"],
            "directions": element["directions"],
            "remedies": element["remedies"],
            "colors": element["color"],
            "avoid": element["negative_objects"]
        }
