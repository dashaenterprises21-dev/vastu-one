"""
Vastu One - YOLO Class Mapping
35 classes → Vastu room types with hindi, best/avoid directions
"""

CLASS_TO_ROOM = {
    # ═══ BEDROOM ═══
    "bed": {"room": "bedroom", "hindi": "शयनकक्ष", "best": ["SW", "S", "W"], "avoid": ["NE", "SE"], "icon": "🛏️"},
    "bedside_cupboard": {"room": "bedroom", "hindi": "शयनकक्ष", "best": ["SW", "S"], "avoid": ["NE"], "icon": "🗄️"},
    "wardrobe": {"room": "bedroom", "hindi": "शयनकक्ष", "best": ["SW", "S", "W"], "avoid": ["NE", "SE"], "icon": "🚪"},
    "chair": {"room": "living", "hindi": "कुर्सी", "best": ["W", "SW"], "avoid": ["NE"], "icon": "🪑"},

    # ═══ KITCHEN ═══
    "gas_stove": {"room": "kitchen", "hindi": "रसोई", "best": ["SE"], "avoid": ["NE", "SW"], "icon": "🔥"},
    "kitchen": {"room": "kitchen", "hindi": "रसोई", "best": ["SE"], "avoid": ["NE", "SW"], "icon": "🍳"},
    "sink": {"room": "kitchen", "hindi": "रसोई", "best": ["NE", "N", "E"], "avoid": ["SW", "SE"], "icon": "🚰"},
    "refrigerator": {"room": "kitchen", "hindi": "रसोई", "best": ["SW", "S", "W"], "avoid": ["NE"], "icon": "❄️"},
    "washing_machine": {"room": "utility", "hindi": "उपयोगिता", "best": ["NW", "W"], "avoid": ["NE", "SE"], "icon": "🧺"},
    "half_height_cabinet": {"room": "storage", "hindi": "भंडार", "best": ["SW", "S"], "avoid": ["NE"], "icon": "🗄️"},
    "high_cabinet": {"room": "storage", "hindi": "भंडार", "best": ["SW", "S"], "avoid": ["NE"], "icon": "🗄️"},

    # ═══ BATHROOM/TOILET ═══
    "bath": {"room": "bathroom", "hindi": "स्नानघर", "best": ["NW", "W"], "avoid": ["NE", "CENTER"], "icon": "🚿"},
    "bath_tub": {"room": "bathroom", "hindi": "स्नानघर", "best": ["NW", "W"], "avoid": ["NE", "CENTER"], "icon": "🛁"},
    "toilet": {"room": "toilet", "hindi": "शौचालय", "best": ["NW", "W", "S"], "avoid": ["NE", "CENTER"], "icon": "🚽"},
    "squat_toilet": {"room": "toilet", "hindi": "शौचालय", "best": ["NW", "W", "S"], "avoid": ["NE", "CENTER"], "icon": "🚽"},
    "urinal": {"room": "toilet", "hindi": "शौचालय", "best": ["NW", "W"], "avoid": ["NE", "SE"], "icon": "🚽"},

    # ═══ LIVING/DINING ═══
    "sofa": {"room": "living", "hindi": "बैठक", "best": ["E", "NE", "N"], "avoid": ["SW", "S"], "icon": "🛋️"},
    "table": {"room": "dining", "hindi": "भोजन कक्ष", "best": ["W", "SW", "S"], "avoid": ["NE"], "icon": "🍽️"},
    "tv_cabinet": {"room": "living", "hindi": "बैठक", "best": ["SE"], "avoid": ["NE", "SW"], "icon": "📺"},

    # ═══ ROOM TYPES (from OCR) ═══
    "bedroom": {"room": "bedroom", "hindi": "शयनकक्ष", "best": ["SW", "S", "W"], "avoid": ["NE", "SE"], "icon": "🛏️"},
    "living": {"room": "living", "hindi": "बैठक", "best": ["E", "NE", "N"], "avoid": ["SW", "S"], "icon": "🛋️"},
    "dining": {"room": "dining", "hindi": "भोजन कक्ष", "best": ["W", "SW", "S"], "avoid": ["NE"], "icon": "🍽️"},
    "store": {"room": "storage", "hindi": "भंडार", "best": ["SW", "S"], "avoid": ["NE"], "icon": "📦"},
    "storage": {"room": "storage", "hindi": "भंडार", "best": ["SW", "S"], "avoid": ["NE"], "icon": "📦"},
    "balcony": {"room": "balcony", "hindi": "बालकनी", "best": ["N", "E", "NE"], "avoid": ["S", "SW"], "icon": "🌿"},
    "entrance": {"room": "entrance", "hindi": "प्रवेश द्वार", "best": [], "avoid": [], "icon": "🚪"},
    "entry": {"room": "entrance", "hindi": "प्रवेश द्वार", "best": [], "avoid": [], "icon": "🚪"},
    "puja": {"room": "puja", "hindi": "पूजा कक्ष", "best": ["NE"], "avoid": ["S", "SW"], "icon": "🕉️"},
    "pooja": {"room": "puja", "hindi": "पूजा कक्ष", "best": ["NE"], "avoid": ["S", "SW"], "icon": "🕉️"},
    "study": {"room": "study", "hindi": "अध्ययन कक्ष", "best": ["NE", "E", "N"], "avoid": ["SW"], "icon": "📚"},
    "office": {"room": "study", "hindi": "कार्यालय", "best": ["NE", "E", "N"], "avoid": ["SW"], "icon": "💼"},

    # ═══ STRUCTURE ═══
    "wall": {"room": "wall", "hindi": "दीवार", "best": [], "avoid": [], "icon": "🧱"},
    "window": {"room": "window", "hindi": "खिड़की", "best": ["N", "E", "NE"], "avoid": ["S", "SW"], "icon": "🪟"},
    "single_door": {"room": "door", "hindi": "दरवाज़ा", "best": [], "avoid": [], "icon": "🚪"},
    "double_door": {"room": "door", "hindi": "दरवाज़ा", "best": [], "avoid": [], "icon": "🚪"},
    "sliding_door": {"room": "door", "hindi": "दरवाज़ा", "best": [], "avoid": [], "icon": "🚪"},
    "blind_window": {"room": "window", "hindi": "खिड़की", "best": ["N", "E"], "avoid": ["S", "SW"], "icon": "🪟"},
    "bay_window": {"room": "window", "hindi": "खिड़की", "best": ["N", "E", "NE"], "avoid": ["S"], "icon": "🪟"},
    "opening_symbol": {"room": "opening", "hindi": "द्वार", "best": [], "avoid": [], "icon": "🚪"},
    "railing": {"room": "railing", "hindi": "रेलिंग", "best": [], "avoid": [], "icon": "🛡️"},

    # ═══ BUILDING ═══
    "stair": {"room": "stair", "hindi": "सीढ़ी", "best": ["S", "SW", "W"], "avoid": ["NE", "CENTER"], "icon": "🪜"},
    "elevator": {"room": "elevator", "hindi": "लिफ्ट", "best": ["SW", "S"], "avoid": ["NE"], "icon": "🛗"},
    "escalator": {"room": "elevator", "hindi": "एस्केलेटर", "best": ["SW", "S"], "avoid": ["NE"], "icon": "🛗"},
    "parking": {"room": "parking", "hindi": "पार्किंग", "best": ["NW", "W", "SW"], "avoid": ["NE"], "icon": "🚗"},

    # ═══ UNKNOWN ═══
    "class_31": {"room": "unknown", "hindi": "अज्ञात", "best": [], "avoid": [], "icon": "❓"},
    "class_32": {"room": "unknown", "hindi": "अज्ञात", "best": [], "avoid": [], "icon": "❓"},
    "class_34": {"room": "unknown", "hindi": "अज्ञात", "best": [], "avoid": [], "icon": "❓"},
    "class_35": {"room": "unknown", "hindi": "अज्ञात", "best": [], "avoid": [], "icon": "❓"},
}


ROOM_GROUPING = {
    "bedroom": ["bed", "bedside_cupboard", "wardrobe"],
    "kitchen": ["gas_stove", "sink", "refrigerator"],
    "toilet": ["toilet", "squat_toilet", "bath", "bath_tub", "urinal"],
    "living": ["sofa", "tv_cabinet", "chair"],
    "dining": ["table", "chair"],
    "storage": ["half_height_cabinet", "high_cabinet"],
    "utility": ["washing_machine"],
    "stair": ["stair"],
    "parking": ["parking"],
}


def get_room_info(class_name):
    """Get room info from YOLO class name"""
    return CLASS_TO_ROOM.get(class_name.lower(), {
        "room": "unknown", "hindi": "अज्ञात",
        "best": [], "avoid": [], "icon": "❓"
    })


def get_objects_for_room(room_type):
    """Get list of YOLO objects for a room type"""
    return ROOM_GROUPING.get(room_type, [])


def get_all_room_types():
    """Get all unique room types"""
    return list(set(info["room"] for info in CLASS_TO_ROOM.values()))
