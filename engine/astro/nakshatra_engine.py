"""
VASTU ONE - Nakshatra Analysis Engine
Detailed 27 nakshatra analysis
"""

from engine.astro.complete_chart_engine import NAKSHATRAS, calculate_complete_chart


NAKSHATRA_DETAILS = {
    "Ashwini": {"symbol": "Horse head", "gana": "Deva", "element": "Earth", "quality": "Swift"},
    "Bharani": {"symbol": "Yoni", "gana": "Manushya", "element": "Earth", "quality": "Fierce"},
    "Krittika": {"symbol": "Razor", "gana": "Rakshasa", "element": "Fire", "quality": "Mixed"},
    "Rohini": {"symbol": "Chariot", "gana": "Manushya", "element": "Earth", "quality": "Fixed"},
    "Mrigashira": {"symbol": "Deer head", "gana": "Deva", "element": "Earth", "quality": "Soft"},
    "Ardra": {"symbol": "Teardrop", "gana": "Manushya", "element": "Water", "quality": "Sharp"},
    "Punarvasu": {"symbol": "Bow", "gana": "Deva", "element": "Water", "quality": "Movable"},
    "Pushya": {"symbol": "Cow udder", "gana": "Deva", "element": "Water", "quality": "Light"},
    "Ashlesha": {"symbol": "Coiled snake", "gana": "Rakshasa", "element": "Water", "quality": "Sharp"},
    "Magha": {"symbol": "Throne", "gana": "Rakshasa", "element": "Water", "quality": "Fierce"},
    "Purva Phalguni": {"symbol": "Front legs of bed", "gana": "Manushya", "element": "Water", "quality": "Fierce"},
    "Uttara Phalguni": {"symbol": "Back legs of bed", "gana": "Manushya", "element": "Fire", "quality": "Fixed"},
    "Hasta": {"symbol": "Hand", "gana": "Deva", "element": "Fire", "quality": "Light"},
    "Chitra": {"symbol": "Bright jewel", "gana": "Rakshasa", "element": "Fire", "quality": "Soft"},
    "Swati": {"symbol": "Young shoot", "gana": "Deva", "element": "Fire", "quality": "Movable"},
    "Vishakha": {"symbol": "Triumphal arch", "gana": "Rakshasa", "element": "Fire", "quality": "Mixed"},
    "Anuradha": {"symbol": "Lotus", "gana": "Deva", "element": "Fire", "quality": "Soft"},
    "Jyeshtha": {"symbol": "Earring", "gana": "Rakshasa", "element": "Air", "quality": "Sharp"},
    "Mula": {"symbol": "Tied roots", "gana": "Rakshasa", "element": "Air", "quality": "Sharp"},
    "Purva Ashadha": {"symbol": "Fan", "gana": "Manushya", "element": "Air", "quality": "Fierce"},
    "Uttara Ashadha": {"symbol": "Elephant tusk", "gana": "Manushya", "element": "Air", "quality": "Fixed"},
    "Shravana": {"symbol": "Ear", "gana": "Deva", "element": "Air", "quality": "Movable"},
    "Dhanishtha": {"symbol": "Drum", "gana": "Rakshasa", "element": "Air", "quality": "Movable"},
    "Shatabhisha": {"symbol": "Empty circle", "gana": "Rakshasa", "element": "Air", "quality": "Movable"},
    "Purva Bhadrapada": {"symbol": "Sword", "gana": "Manushya", "element": "Air", "quality": "Fierce"},
    "Uttara Bhadrapada": {"symbol": "Twins", "gana": "Manushya", "element": "Ether", "quality": "Fixed"},
    "Revati": {"symbol": "Fish", "gana": "Deva", "element": "Ether", "quality": "Soft"},
}


def analyze_nakshatra(chart):
    """Analyze all nakshatras in chart"""
    results = {}
    
    for planet, data in chart["planets"].items():
        nak_name = data["nakshatra"]["name"]
        pada = data["nakshatra"]["pada"]
        lord = data["nakshatra"]["lord"]
        
        details = NAKSHATRA_DETAILS.get(nak_name, {})
        
        results[planet] = {
            "nakshatra": nak_name,
            "pada": pada,
            "lord": lord,
            "deity": data["nakshatra"]["deity"],
            "shakti": data["nakshatra"]["shakti"],
            "symbol": details.get("symbol", ""),
            "gana": details.get("gana", ""),
            "element": details.get("element", ""),
            "quality": details.get("quality", ""),
        }
    
    return results


if __name__ == "__main__":
    chart = calculate_complete_chart(1947, 8, 15, 0.0, 28.6139, 77.2090)
    result = analyze_nakshatra(chart)
    
    print("=== NAKSHATRA ANALYSIS ===")
    print()
    for planet, data in result.items():
        print(f"  {planet}:")
        print(f"    Nakshatra: {data['nakshatra']} (pada {data['pada']})")
        print(f"    Lord:      {data['lord']}")
        print(f"    Deity:     {data['deity']}")
        print(f"    Shakti:    {data['shakti']}")
        print(f"    Gana:      {data['gana']}")
        print(f"    Element:   {data['element']}")
        print()
