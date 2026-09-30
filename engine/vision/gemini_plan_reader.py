"""
Vastu One - Gemini Plan Reader (NEW SDK)
AI-powered floor plan analysis using Google GenAI SDK
"""

import os
import json
import base64
import io
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
    from PIL import Image
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[WARNING] Gemini not available — install google-genai")

# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


FLOORPLAN_PROMPT = """You are a floor plan analysis expert. Analyze this floor plan image carefully.

Extract the following information in valid JSON format:

{
  "plan_info": {
    "compass_direction": "direction where compass arrow points (N/S/E/W or null)",
    "compass_angle": "compass degree if visible (0-360) or null",
    "latitude": "latitude if visible or null",
    "longitude": "longitude if visible or null",
    "total_area": "total area with units or null",
    "dimensions": "overall dimensions or null"
  },
  "rooms": [
    {
      "name": "Room name as labeled in plan",
      "type": "normalized: kitchen/bedroom/master_bedroom/living/dining/toilet/bathroom/pooja/balcony/store/staircase/entry/parking/other",
      "position": "top-left/top-center/top-right/center-left/center/center-right/bottom-left/bottom-center/bottom-right",
      "approximate_direction": "NE/N/NW/E/C/W/SE/S/SW",
      "dimensions": "room dimensions if visible",
      "area": "room area if visible",
      "features": ["windows", "doors", "attached bathroom", "balcony"]
    }
  ],
  "doors": [
    {
      "position": "position description",
      "direction": "which direction it opens",
      "type": "main entrance/interior door/bathroom door"
    }
  ],
  "windows": [
    {
      "position": "position description",
      "direction": "direction it faces"
    }
  ],
  "notes": "any other important observations"
}

RULES:
1. Return ONLY valid JSON, no other text
2. If a field is not visible, use null
3. Normalize room types to standard names
4. For approximate_direction, use 8 directions + CENTER based on position from plan center
5. Be precise with positions — this data will be used for Vastu analysis

Analyze the floor plan now and return the JSON."""


class GeminiPlanReader:
    """Reads floor plans using Google GenAI SDK"""

    def __init__(self):
        if not GEMINI_AVAILABLE:
            raise RuntimeError("Gemini library not installed")

        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY not found in .env")

        # NEW SDK: create client
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-flash-latest"

    def analyze_plan(self, image_path: str) -> dict:
        """Analyze floor plan image and extract structured data"""
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Load image
        image = Image.open(image_path)

        print(f"[INFO] Sending plan to Gemini: {image_path.name}")

        # NEW SDK: generate_content
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[FLOORPLAN_PROMPT, image],
        )

        # Parse response
        response_text = response.text.strip()

        # Clean up JSON
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        # Parse JSON
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse JSON: {e}")
            print(f"[DEBUG] Response: {response_text[:500]}")
            raise ValueError(f"Gemini returned invalid JSON: {e}")

        return data

    def analyze_plan_base64(self, image_base64: str) -> dict:
        """Analyze from base64 encoded image"""
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))

        print("[INFO] Sending plan to Gemini (base64)")

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[FLOORPLAN_PROMPT, image],
        )

        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        return json.loads(response_text.strip())


def map_to_chakra(rooms_data: list) -> list:
    """Map extracted rooms to 81-pad chakra grid"""

    DIRECTION_TO_PADA = {
        "NE": 3, "N": 5, "NW": 7,
        "E": 42, "C": 41, "W": 40,
        "SE": 75, "S": 77, "SW": 79,
    }

    TYPE_MAP = {
        "kitchen": "kitchen",
        "bedroom": "bedroom",
        "master bedroom": "master_bedroom",
        "master_bedroom": "master_bedroom",
        "living": "living",
        "living room": "living",
        "hall": "living",
        "dining": "dining",
        "dining room": "dining",
        "toilet": "toilet",
        "wc": "toilet",
        "bathroom": "bathroom",
        "bath": "bathroom",
        "pooja": "pooja",
        "puja": "pooja",
        "mandir": "pooja",
        "temple": "pooja",
        "balcony": "balcony",
        "store": "store",
        "store room": "store",
        "staircase": "staircase",
        "stairs": "staircase",
        "entry": "main_entry",
        "main entry": "main_entry",
        "entrance": "main_entry",
        "parking": "parking",
        "garage": "parking",
    }

    mapped_rooms = []
    for room in rooms_data:
        direction = (room.get("approximate_direction") or "C").upper()
        if direction not in DIRECTION_TO_PADA:
            direction = "C"

        room_type_raw = (room.get("type") or room.get("name") or "other").lower().strip()
        room_type = TYPE_MAP.get(room_type_raw, "other")

        if room_type == "other":
            continue

        pada = DIRECTION_TO_PADA[direction]
        row = (pada - 1) // 9
        col = (pada - 1) % 9

        mapped_rooms.append({
            "pada": pada,
            "row": row,
            "col": col,
            "zone": direction,
            "type": room_type,
            "name": room.get("name", room_type),
            "dimensions": room.get("dimensions"),
            "position": room.get("position"),
            "features": room.get("features", [])
        })

    return mapped_rooms


# ═══ TEST ═══
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python gemini_plan_reader.py <plan_image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        reader = GeminiPlanReader()
        print(f"\n📐 Analyzing: {image_path}\n")

        result = reader.analyze_plan(image_path)

        print("=" * 60)
        print("PLAN INFO:")
        print(json.dumps(result.get("plan_info", {}), indent=2, ensure_ascii=False))

        print("\n" + "=" * 60)
        print(f"ROOMS FOUND: {len(result.get('rooms', []))}")
        for room in result.get("rooms", []):
            print(f"  • {room.get('name')} ({room.get('type')}) — {room.get('approximate_direction')}")

        print("\n" + "=" * 60)
        print("CHAKRA MAPPING:")
        mapped = map_to_chakra(result.get("rooms", []))
        for r in mapped:
            print(f"  • Pada #{r['pada']} ({r['zone']}) — {r['type']}")

        output_file = Path(image_path).parent / "gemini_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Output saved: {output_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()