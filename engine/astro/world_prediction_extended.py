"""
World Prediction Extended — 15 More Countries
"""

EXTENDED_COUNTRIES = {
    "France": {"population": "68 million", "area": "643,801 sq km", "capital": "Paris", "neighbors": ["Germany", "Spain", "Italy", "Belgium", "Switzerland"], "risk_level": "Medium", "fault_lines": ["Rhine Graben", "Alpine Front"], "war_zones": ["None currently"]},
    "Brazil": {"population": "215 million", "area": "8.5 million sq km", "capital": "Brasília", "neighbors": ["Argentina", "Peru", "Colombia", "Venezuela"], "risk_level": "Medium", "fault_lines": ["Amazon Basin", "Andean Front"], "war_zones": ["None currently"]},
    "Australia": {"population": "26 million", "area": "7.7 million sq km", "capital": "Canberra", "neighbors": ["None (island continent)"], "risk_level": "Low", "fault_lines": ["Darling Fault", "Hyden Fault"], "war_zones": ["None currently"]},
    "Canada": {"population": "39 million", "area": "9.98 million sq km", "capital": "Ottawa", "neighbors": ["USA"], "risk_level": "Low", "fault_lines": ["Cascadia Subduction", "Charlevoix Seismic"], "war_zones": ["None currently"]},
    "Saudi Arabia": {"population": "36 million", "area": "2.15 million sq km", "capital": "Riyadh", "neighbors": ["Yemen", "Oman", "UAE", "Jordan", "Iraq", "Kuwait"], "risk_level": "Medium", "fault_lines": ["Red Sea Rift", "Dead Sea Transform"], "war_zones": ["Yemen border"]},
    "Iran": {"population": "88 million", "area": "1.65 million sq km", "capital": "Tehran", "neighbors": ["Iraq", "Turkey", "Afghanistan", "Pakistan"], "risk_level": "High", "fault_lines": ["Zagros Fold Belt", "Alborz Fault"], "war_zones": ["Israel tensions", "Proxy conflicts"]},
    "North Korea": {"population": "26 million", "area": "120,540 sq km", "capital": "Pyongyang", "neighbors": ["China", "South Korea", "Russia"], "risk_level": "Very High", "fault_lines": ["Korean Peninsula faults"], "war_zones": ["DMZ", "Nuclear tensions"]},
    "South Korea": {"population": "52 million", "area": "100,210 sq km", "capital": "Seoul", "neighbors": ["North Korea"], "risk_level": "Medium", "fault_lines": ["Yangsan Fault", "Ulsan Fault"], "war_zones": ["DMZ"]},
    "Nepal": {"population": "30 million", "area": "147,181 sq km", "capital": "Kathmandu", "neighbors": ["India", "China"], "risk_level": "Very High", "fault_lines": ["Himalayan Frontal Thrust", "Main Boundary Thrust"], "war_zones": ["None currently"]},
    "Sri Lanka": {"population": "22 million", "area": "65,610 sq km", "capital": "Colombo", "neighbors": ["India (across Palk Strait)"], "risk_level": "Low", "fault_lines": ["None major"], "war_zones": ["None currently"]},
    "Bangladesh": {"population": "170 million", "area": "147,570 sq km", "capital": "Dhaka", "neighbors": ["India", "Myanmar"], "risk_level": "High", "fault_lines": ["Dauki Fault", "Madhupur Fault"], "war_zones": ["None currently"]},
    "Afghanistan": {"population": "40 million", "area": "652,230 sq km", "capital": "Kabul", "neighbors": ["Pakistan", "Iran", "Turkmenistan", "Uzbekistan", "Tajikistan", "China"], "risk_level": "Very High", "fault_lines": ["Hindu Kush Seismic Zone", "Chaman Fault"], "war_zones": ["Internal conflicts"]},
    "Turkey": {"population": "85 million", "area": "783,562 sq km", "capital": "Ankara", "neighbors": ["Syria", "Iraq", "Iran", "Greece", "Bulgaria", "Georgia", "Armenia", "Azerbaijan"], "risk_level": "High", "fault_lines": ["North Anatolian Fault", "East Anatolian Fault"], "war_zones": ["Syria border", "Kurdish regions"]},
    "Egypt": {"population": "105 million", "area": "1 million sq km", "capital": "Cairo", "neighbors": ["Libya", "Sudan", "Israel", "Palestine"], "risk_level": "Medium", "fault_lines": ["Red Sea Rift", "Cairo-Suez Fault"], "war_zones": ["Sinai Peninsula"]},
    "South Africa": {"population": "60 million", "area": "1.22 million sq km", "capital": "Pretoria", "neighbors": ["Namibia", "Botswana", "Zimbabwe", "Mozambique", "Eswatini", "Lesotho"], "risk_level": "Medium", "fault_lines": ["Bushveld Complex", "Cape Fold Belt"], "war_zones": ["None currently"]},
}


def get_extended_countries():
    return list(EXTENDED_COUNTRIES.keys())


def analyze_extended_country(country: str):
    if country not in EXTENDED_COUNTRIES:
        return {"error": f"Country '{country}' not in extended list", "available": list(EXTENDED_COUNTRIES.keys())}
    d = EXTENDED_COUNTRIES[country]
    return {"country": country, "metadata": d, "prediction_summary": {"risk_level": d["risk_level"], "main_concerns": d["war_zones"], "fault_lines": d["fault_lines"]}}


def get_all_countries_25():
    original = ["India", "USA", "China", "Russia", "Pakistan", "UK", "Israel", "Ukraine", "Japan", "Germany"]
    extended = list(EXTENDED_COUNTRIES.keys())
    return original + extended
