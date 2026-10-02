"""Generate all missing data files for Vastu One"""
import json
from pathlib import Path

DATA = Path("data")
DATA.mkdir(exist_ok=True)

# ═══ FILE 1: 32 Entrance Padas ═══
entrance_padas = {
    "version": "1.0",
    "source": "Samarangana Sutradhara, Brihat Samhita 53",
    "total_padas": 32,
    "directions": {
        "East": [
            {"pada": 1, "name": "Shikhi", "hindi": "शिखी", "best": False, "effect": "Loss of wealth, obstacles", "shastra": "BS 53.70"},
            {"pada": 2, "name": "Parjanya", "hindi": "पर्जन्य", "best": False, "effect": "Health issues, fear", "shastra": "BS 53.70"},
            {"pada": 3, "name": "Jayanta", "hindi": "जयन्त", "best": True, "effect": "Victory, prosperity, all desires fulfilled", "shastra": "BS 53.71"},
            {"pada": 4, "name": "Indra", "hindi": "इन्द्र", "best": True, "effect": "Power, leadership, wealth", "shastra": "BS 53.71"},
            {"pada": 5, "name": "Surya", "hindi": "सूर्य", "best": True, "effect": "Fame, vitality, health", "shastra": "BS 53.71"},
            {"pada": 6, "name": "Satya", "hindi": "सत्य", "best": True, "effect": "Truth, clarity, success", "shastra": "BS 53.72"},
            {"pada": 7, "name": "Bhusha", "hindi": "भूष", "best": False, "effect": "Financial loss, theft", "shastra": "BS 53.72"},
            {"pada": 8, "name": "Akasha", "hindi": "आकाश", "best": False, "effect": "Loss of children, grief", "shastra": "BS 53.72"}
        ],
        "South": [
            {"pada": 1, "name": "Anila", "hindi": "अनिल", "best": False, "effect": "Fear of enemies, quarrel", "shastra": "BS 53.73"},
            {"pada": 2, "name": "Pusha", "hindi": "पूषा", "best": True, "effect": "Nourishment, peace, wealth", "shastra": "BS 53.73"},
            {"pada": 3, "name": "Vitatha", "hindi": "वितथ", "best": False, "effect": "Obstacles, poverty", "shastra": "BS 53.73"},
            {"pada": 4, "name": "Grihakshata", "hindi": "गृहक्षत", "best": True, "effect": "BEST - Good food, children, wealth", "shastra": "BS 53.74"},
            {"pada": 5, "name": "Yama", "hindi": "यम", "best": False, "effect": "Death, negativity, fear", "shastra": "BS 53.74"},
            {"pada": 6, "name": "Gandharva", "hindi": "गन्धर्व", "best": True, "effect": "Luxury, comfort, music", "shastra": "BS 53.74"},
            {"pada": 7, "name": "Bhrungaraja", "hindi": "भृंगराज", "best": False, "effect": "Fear, anxiety, quarrel", "shastra": "BS 53.75"},
            {"pada": 8, "name": "Mriga", "hindi": "मृग", "best": False, "effect": "Fear, weapons, accidents", "shastra": "BS 53.75"}
        ],
        "West": [
            {"pada": 1, "name": "Pitara", "hindi": "पितर", "best": False, "effect": "Ancestral issues, obstacles", "shastra": "BS 53.76"},
            {"pada": 2, "name": "Dauvarika", "hindi": "दौवारिक", "best": False, "effect": "Guests, hospitality issues", "shastra": "BS 53.76"},
            {"pada": 3, "name": "Sugriva", "hindi": "सुग्रीव", "best": True, "effect": "BEST - Money, profits, success", "shastra": "BS 53.76"},
            {"pada": 4, "name": "Pushpadanta", "hindi": "पुष्पदन्त", "best": True, "effect": "Finance, income, wealth", "shastra": "BS 53.77"},
            {"pada": 5, "name": "Varuna", "hindi": "वरुण", "best": True, "effect": "Rain, purification, water", "shastra": "BS 53.77"},
            {"pada": 6, "name": "Asura", "hindi": "असुर", "best": False, "effect": "Strength, fear, negativity", "shastra": "BS 53.77"},
            {"pada": 7, "name": "Shesha", "hindi": "शेष", "best": True, "effect": "Savings, serpent, wealth", "shastra": "BS 53.78"},
            {"pada": 8, "name": "Rajayakshma", "hindi": "राजयक्ष्मा", "best": False, "effect": "Disease, health issues", "shastra": "BS 53.78"}
        ],
        "North": [
            {"pada": 1, "name": "Roga", "hindi": "रोग", "best": False, "effect": "Disease, health issues", "shastra": "BS 53.79"},
            {"pada": 2, "name": "Ahi", "hindi": "अहि", "best": False, "effect": "Fear, serpent, anxiety", "shastra": "BS 53.79"},
            {"pada": 3, "name": "Mukhya", "hindi": "मुख्य", "best": True, "effect": "Career, clarity, success", "shastra": "BS 53.79"},
            {"pada": 4, "name": "Bhallataka", "hindi": "भल्लाटक", "best": True, "effect": "BEST - Career, growth, wealth", "shastra": "BS 53.80"},
            {"pada": 5, "name": "Soma", "hindi": "सोम", "best": True, "effect": "Wealth, prosperity, peace", "shastra": "BS 53.80"},
            {"pada": 6, "name": "Sarpa", "hindi": "सर्प", "best": False, "effect": "Fear, kundalini issues", "shastra": "BS 53.80"},
            {"pada": 7, "name": "Aditi", "hindi": "अदिति", "best": True, "effect": "Creativity, children, growth", "shastra": "BS 53.81"},
            {"pada": 8, "name": "Diti", "hindi": "दिति", "best": False, "effect": "Creativity issues, obstacles", "shastra": "BS 53.81"}
        ]
    }
}
(DATA / "entrance_padas_32.json").write_text(json.dumps(entrance_padas, ensure_ascii=False, indent=2), encoding="utf-8")
print("[OK] entrance_padas_32.json created")

# ═══ FILE 2: Ayadi Shadvarga ═══
ayadi = {
    "version": "1.0",
    "description": "Building fate math - 6 formulas for house dimensions",
    "formulas": {
        "Aya": {
            "hindi": "आय (Income)",
            "formula": "(Length × 8) ÷ 12",
            "meaning": "Income, prosperity",
            "good_when": "Aya > Vyaya"
        },
        "Vyaya": {
            "hindi": "व्यय (Loss)",
            "formula": "(Breadth × 9) ÷ 10",
            "meaning": "Loss, expenses",
            "good_when": "Vyaya < Aya"
        },
        "Rksa": {
            "hindi": "ऋक्ष (Nakshatra)",
            "formula": "(Length × 8) ÷ 27",
            "meaning": "Nakshatra influence",
            "good_when": "Remainder 1-27"
        },
        "Yoni": {
            "hindi": "योनि (Energy)",
            "formula": "(Breadth × 3) ÷ 8",
            "meaning": "Energy, vitality",
            "good_when": "Remainder 1-8"
        },
        "Vara": {
            "hindi": "वार (Weekday)",
            "formula": "(Height × 9) ÷ 7",
            "meaning": "Weekday influence",
            "good_when": "Remainder 1-7"
        },
        "Tithi": {
            "hindi": "तिथि (Lunar Day)",
            "formula": "(Height × 9) ÷ 30",
            "meaning": "Lunar day influence",
            "good_when": "Remainder 1-30"
        }
    },
    "interpretation": {
        "Aya_gt_Vyaya": "Prosperity, growth, wealth accumulation",
        "Aya_lt_Vyaya": "Financial loss, need partition or water feature remedy",
        "Aya_eq_Vyaya": "Balance, stable life"
    }
}
(DATA / "ayadi_shadvarga.json").write_text(json.dumps(ayadi, ensure_ascii=False, indent=2), encoding="utf-8")
print("[OK] ayadi_shadvarga.json created")

# ═══ FILE 3: Non-Demolition Remedies ═══
remedies = {
    "version": "1.0",
    "description": "Non-demolition remedies - fix defects without breaking",
    "remedies": {
        "toilet_NE": {
            "defect": "Toilet in North-East",
            "severity": "high",
            "problem": "Water element in NE causes mental stress, financial loss",
            "remedies": [
                {"type": "element", "action": "Place sea salt in small bowl", "cost": "₹50", "time": "1 day"},
                {"type": "color", "action": "Paint toilet walls light yellow", "cost": "₹2000", "time": "2 days"},
                {"type": "metal", "action": "Place copper wire around toilet", "cost": "₹500", "time": "1 hour"},
                {"type": "plant", "action": "Keep tulsi plant outside", "cost": "₹100", "time": "1 day"},
                {"type": "pooja", "action": "Varuna devta puja + Om Varunaya Namaha", "cost": "₹500", "time": "1 day"}
            ],
            "mantra": "Om Varunaya Namaha"
        },
        "kitchen_SE": {
            "defect": "Kitchen in South-East",
            "severity": "low",
            "problem": "Correct as per Vastu - SE is best for kitchen",
            "remedies": [],
            "mantra": "Om Agnaye Namaha"
        },
        "kitchen_NE": {
            "defect": "Kitchen in North-East",
            "severity": "high",
            "problem": "Fire in NE causes agni dosh, health issues",
            "remedies": [
                {"type": "color", "action": "Paint kitchen walls light green", "cost": "₹3000", "time": "3 days"},
                {"type": "element", "action": "Place blue color mat at entrance", "cost": "₹300", "time": "1 day"},
                {"type": "mirror", "action": "Place mirror to reflect stove", "cost": "₹500", "time": "1 hour"},
                {"type": "pooja", "action": "Agni devta puja + havan", "cost": "₹1500", "time": "1 day"}
            ],
            "mantra": "Om Agnaye Namaha"
        },
        "brahma_blocked": {
            "defect": "Brahma sthan blocked (center)",
            "severity": "high",
            "problem": "Heavy object or toilet in center blocks energy flow",
            "remedies": [
                {"type": "action", "action": "Clear center, keep empty", "cost": "₹0", "time": "1 hour"},
                {"type": "light", "action": "Place bright light in center", "cost": "₹500", "time": "1 hour"},
                {"type": "crystal", "action": "Place clear quartz crystal", "cost": "₹200", "time": "5 min"},
                {"type": "pooja", "action": "Brahma puja + Om Brahmane Namaha", "cost": "₹1000", "time": "1 day"}
            ],
            "mantra": "Om Brahmane Namaha"
        },
        "entrance_wrong": {
            "defect": "Wrong entrance pada",
            "severity": "high",
            "problem": "Entrance in wrong pada causes financial and health issues",
            "remedies": [
                {"type": "action", "action": "Virtual entry - create alternate path", "cost": "₹2000", "time": "1 day"},
                {"type": "mirror", "action": "Place mirror to reflect entry", "cost": "₹1000", "time": "1 hour"},
                {"type": "light", "action": "Place bright light at entrance", "cost": "₹500", "time": "1 hour"},
                {"type": "metal", "action": "Place copper strip below door", "cost": "₹300", "time": "1 hour"},
                {"type": "pooja", "action": "Ganesh puja + Vastu Purush puja", "cost": "₹2000", "time": "1 day"}
            ],
            "mantra": "Om Gan Ganpataye Namaha"
        },
        "aya_lt_vyaya": {
            "defect": "Aya < Vyaya (Income < Loss)",
            "severity": "medium",
            "problem": "Building dimensions cause financial loss",
            "remedies": [
                {"type": "action", "action": "Add partition to change dimensions", "cost": "₹5000", "time": "1 week"},
                {"type": "element", "action": "Place water fountain in North", "cost": "₹1500", "time": "1 day"},
                {"type": "metal", "action": "Place Kuber yantra", "cost": "₹500", "time": "1 hour"},
                {"type": "pooja", "action": "Kuber puja + Laxmi puja", "cost": "₹2000", "time": "1 day"}
            ],
            "mantra": "Om Shreem Hreem Shreem Kamale Kamalalaye Praseed Praseed"
        }
    }
}
(DATA / "remedies_non_demolition.json").write_text(json.dumps(remedies, ensure_ascii=False, indent=2), encoding="utf-8")
print("[OK] remedies_non_demolition.json created")

# ═══ FILE 4: Pooja & Mantra ═══
pooja = {
    "version": "1.0",
    "description": "Pooja & mantra database for Vastu remedies",
    "poojas": {
        "Ganesh_Pooja": {
            "hindi": "गणेश पूजा",
            "purpose": "Remove obstacles, start new work",
            "samagri": ["Modak", "Durva grass", "Red flowers", "Coconut", "Ganesh idol"],
            "direction": "North-East",
            "timing": "Morning, Chaturthi tithi",
            "mantra": "Om Gan Ganpataye Namaha",
            "count": 108,
            "cost": "₹500"
        },
        "Navagrah_Shanti": {
            "hindi": "नवग्रह शांति",
            "purpose": "Planetary peace, remove astro dosh",
            "samagri": ["9 grains", "9 colors cloth", "Navagraha yantra", "Ghee lamp"],
            "direction": "East",
            "timing": "Brahma muhurat",
            "mantra": "Om Navagrahaya Namaha",
            "count": 108,
            "cost": "₹2000"
        },
        "Vastu_Purush_Pooja": {
            "hindi": "वास्तु पुरुष पूजा",
            "purpose": "Vastu dosh nivaran",
            "samagri": ["Vastu Purush yantra", "45 devta idols", "Yellow cloth", "Havan samagri"],
            "direction": "Center",
            "timing": "Any auspicious day",
            "mantra": "Om Namo Bhagvati Vaastu Devtay Namah",
            "count": 108,
            "cost": "₹5000"
        },
        "Agni_Pooja": {
            "hindi": "अग्नि पूजा",
            "purpose": "Kitchen dosh nivaran",
            "samagri": ["Red flowers", "Copper vessel", "Ghee", "Havan samagri"],
            "direction": "South-East",
            "timing": "Sunrise",
            "mantra": "Om Agnaye Namaha",
            "count": 108,
            "cost": "₹1000"
        },
        "Varuna_Pooja": {
            "hindi": "वरुण पूजा",
            "purpose": "Water dosh nivaran, NE toilet",
            "samagri": ["Blue flowers", "Silver vessel", "Water", "Coconut"],
            "direction": "North-East",
            "timing": "Evening",
            "mantra": "Om Varunaya Namaha",
            "count": 108,
            "cost": "₹800"
        },
        "Brahma_Pooja": {
            "hindi": "ब्रह्मा पूजा",
            "purpose": "Center dosh nivaran",
            "samagri": ["White flowers", "White cloth", "Ghee lamp", "Crystal"],
            "direction": "Center",
            "timing": "Brahma muhurat",
            "mantra": "Om Brahmane Namaha",
            "count": 108,
            "cost": "₹1500"
        }
    }
}
(DATA / "pooja_mantra.json").write_text(json.dumps(pooja, ensure_ascii=False, indent=2), encoding="utf-8")
print("[OK] pooja_mantra.json created")

print("\n[DONE] All 4 data files created in data/")
