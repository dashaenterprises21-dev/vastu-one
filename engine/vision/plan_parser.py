"""
Vastu One - Advanced Floor Plan Parser v2.0
4-Layer System: YOLO + OCR + Walls + Fusion
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import base64
import io

from engine.vision.class_mapping import CLASS_TO_ROOM, ROOM_GROUPING, get_room_info

# YOLO imports
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("[WARNING] YOLO not available")

# OCR imports (optional)
try:
    import pytesseract
    import os as _os
    import platform as _platform
    if _platform.system() == "Windows":
        _tess_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
        ]
        for _tp in _tess_paths:
            if _os.path.exists(_tp):
                pytesseract.pytesseract.tesseract_cmd = _tp
                print(f"[INFO] Tesseract path: {_tp}")
                break
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "best.pt"

# OCR keywords → room type mapping
OCR_KEYWORDS = {
    "bedroom": ["bed room", "bedroom", "master bedroom", "bed room"],
    "kitchen": ["kitchen", "kitchenette", "cook"],
    "toilet": ["toilet", "w.c", "wc", "bathroom", "bath", "washroom"],
    "living": ["living", "hall", "drawing", "lounge", "sitting"],
    "dining": ["dining", "dining hall", "dining room"],
    "store": ["store", "storage", "store room"],
    "balcony": ["balcony", "sitout", "sit out", "verandah"],
    "stair": ["stair", "staircase", "steps", "up"],
    "entrance": ["entry", "entrance", "main door", "foyer"],
    "parking": ["parking", "garage", "car"],
    "puja": ["puja", "pooja", "temple", "mandir"],
    "study": ["study", "office", "work"],
}


class PlanParser:
    """Advanced floor plan analysis: YOLO + OCR + Walls + Fusion"""

    def __init__(self):
        self.plan_image = None
        self.detections = []
        self.ocr_results = []
        self.rooms_detected = []
        self.grid_81 = []
        self.yolo_model = None
        self.easyocr_reader = None

        # Load YOLO
        if YOLO_AVAILABLE and MODEL_PATH.exists():
            try:
                self.yolo_model = YOLO(str(MODEL_PATH))
                print(f"[INFO] YOLO loaded: {MODEL_PATH.name}")
            except Exception as e:
                print(f"[ERROR] YOLO load failed: {e}")

        # Load EasyOCR (lazy)
        if EASYOCR_AVAILABLE:
            try:
                self.easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
                print("[INFO] EasyOCR loaded")
            except Exception as e:
                print(f"[WARNING] EasyOCR failed: {e}")

    def load_plan(self, image_path):
        """Load and preprocess image"""
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")

        h, w = img.shape[:2]
        max_dim = 2000  # Higher for better detail
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        self.plan_image = img
        return img

    # ═══════════════════════════════════════════════════════════════
    # LAYER 1: YOLO DETECTION
    # ═══════════════════════════════════════════════════════════════
    def detect_with_yolo(self):
        """YOLO detection - 35 classes"""
        if not self.yolo_model:
            return []

        try:
            results = self.yolo_model.predict(
                self.plan_image,
                conf=0.20,  # Lower threshold for more detections
                iou=0.45,
                verbose=False
            )

            detections = []
            if results and len(results) > 0:
                result = results[0]
                boxes = result.boxes

                if boxes is not None:
                    for i, box in enumerate(boxes):
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        cls_name = result.names.get(cls_id, f"class_{cls_id}")

                        room_info = get_room_info(cls_name)

                        detections.append({
                            "id": i,
                            "class_name": cls_name,
                            "room_type": room_info["room"],
                            "hindi": room_info["hindi"],
                            "icon": room_info.get("icon", "❓"),
                            "confidence": round(conf, 3),
                            "bbox": [int(x1), int(y1), int(x2), int(y2)],
                            "center": [int((x1+x2)/2), int((y1+y2)/2)],
                            "width": int(x2-x1),
                            "height": int(y2-y1),
                            "area": int((x2-x1) * (y2-y1)),
                        })

            self.detections = detections
            print(f"[INFO] YOLO detected {len(detections)} objects")
            return detections

        except Exception as e:
            print(f"[ERROR] YOLO detection failed: {e}")
            return []

    # ═══════════════════════════════════════════════════════════════
    # LAYER 2: OCR TEXT DETECTION
    # ═══════════════════════════════════════════════════════════════
    def detect_text_ocr(self):
        """Detect text labels from plan using OCR"""
        if not self.plan_image is not None:
            return []

        results = []

        # Try EasyOCR first (better for plans)
        if self.easyocr_reader:
            try:
                # Upscale for better OCR
                h, w = self.plan_image.shape[:2]
                scale = 1.5
                upscaled = cv2.resize(self.plan_image, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)
                ocr_raw = self.easyocr_reader.readtext(upscaled)
                print(f"[DEBUG] EasyOCR raw results: {len(ocr_raw)}")
                for bbox, text, conf in ocr_raw:
                    if conf < 0.2:
                        continue
                    # Scale bbox back to original size
                    bbox = [[p[0]/scale, p[1]/scale] for p in bbox]
                    text_lower = text.lower().strip()
                    room_type = self._match_text_to_room(text_lower)
                    if room_type:
                        # Convert bbox to x1,y1,x2,y2
                        xs = [p[0] for p in bbox]
                        ys = [p[1] for p in bbox]
                        results.append({
                            "text": text,
                            "text_lower": text_lower,
                            "room_type": room_type,
                            "confidence": round(conf, 3),
                            "bbox": [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))],
                            "center": [int((min(xs)+max(xs))/2), int((min(ys)+max(ys))/2)],
                        })
            except Exception as e:
                print(f"[WARNING] EasyOCR failed: {e}")

        # Fallback to Tesseract
        if not results and TESSERACT_AVAILABLE:
            try:
                gray = cv2.cvtColor(self.plan_image, cv2.COLOR_BGR2GRAY)
                data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
                for i, text in enumerate(data['text']):
                    text = text.strip()
                    if not text or len(text) < 3:
                        continue
                    text_lower = text.lower()
                    room_type = self._match_text_to_room(text_lower)
                    if room_type:
                        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                        results.append({
                            "text": text,
                            "text_lower": text_lower,
                            "room_type": room_type,
                            "confidence": data['conf'][i] / 100.0 if data['conf'][i] > 0 else 0.5,
                            "bbox": [x, y, x+w, y+h],
                            "center": [x + w//2, y + h//2],
                        })
            except Exception as e:
                print(f"[WARNING] Tesseract failed: {e}")

        self.ocr_results = results
        print(f"[INFO] OCR detected {len(results)} text labels")
        return results

    def _match_text_to_room(self, text):
        """Match OCR text to room type"""
        for room_type, keywords in OCR_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    return room_type
        return None

    # ═══════════════════════════════════════════════════════════════
    # LAYER 3: WALL DETECTION (Hough Lines)
    # ═══════════════════════════════════════════════════════════════
    def detect_walls(self):
        """Detect walls using Hough Lines"""
        if self.plan_image is None:
            return []

        gray = cv2.cvtColor(self.plan_image, cv2.COLOR_BGR2GRAY)

        # Binarize
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        # Detect lines
        lines = cv2.HoughLinesP(
            thresh,
            rho=1,
            theta=np.pi / 180,
            threshold=80,
            minLineLength=50,
            maxLineGap=10
        )

        wall_lines = []
        if lines is not None:
            # Handle both possible return formats
            lines_flat = lines.reshape(-1, 4) if len(lines.shape) > 2 else lines
            for line in lines_flat:
                try:
                    x1, y1, x2, y2 = int(line[0]), int(line[1]), int(line[2]), int(line[3])
                    length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if length > 80:
                        wall_lines.append({
                            "start": [x1, y1],
                            "end": [x2, y2],
                            "length": int(length),
                        })
                except (ValueError, IndexError, TypeError):
                    continue

        print(f"[INFO] Detected {len(wall_lines)} wall lines")
        return wall_lines

    # ═══════════════════════════════════════════════════════════════
    # LAYER 4: FUSION - Combine YOLO + OCR + Walls
    # ═══════════════════════════════════════════════════════════════
    def fuse_rooms(self):
        """Combine YOLO + OCR to create final rooms"""
        rooms = []

        # STEP 1: OCR-based rooms (highest priority)
        ocr_rooms = []
        for ocr in self.ocr_results:
            ocr_rooms.append({
                "room_type": ocr["room_type"],
                "source": "ocr",
                "confidence": ocr["confidence"],
                "bbox": ocr["bbox"],
                "center": ocr["center"],
                "label": ocr["text"],
                "area": (ocr["bbox"][2]-ocr["bbox"][0]) * (ocr["bbox"][3]-ocr["bbox"][1]),
            })

        # STEP 2: YOLO-based grouping
        yolo_groups = self._group_yolo_by_room()

        # STEP 3: Merge OCR + YOLO
        # OCR rooms = primary, YOLO fills gaps
        used_yolo = set()

        # Add OCR rooms
        for ocr_room in ocr_rooms:
            # Find matching YOLO objects near this OCR label
            room_objects = []
            ox, oy = ocr_room["center"]
            for yg in yolo_groups:
                yx, yy = yg["center"]
                # Agar YOLO object OCR label ke paas hai (< 300px), toh same room
                if abs(ox - yx) < 300 and abs(oy - yy) < 300:
                    room_objects.append(yg)
                    used_yolo.add(yg["id"])

            ocr_room["objects"] = room_objects
            ocr_room["objects_count"] = len(room_objects)
            rooms.append(ocr_room)

        # Add YOLO rooms that weren't matched (no OCR label)
        for yg in yolo_groups:
            if yg["id"] not in used_yolo:
                rooms.append({
                    "room_type": yg["room_type"],
                    "source": "yolo",
                    "confidence": yg["confidence"],
                    "bbox": yg["bbox"],
                    "center": yg["center"],
                    "label": yg["class_name"],
                    "objects": [yg],
                    "objects_count": 1,
                    "area": yg["area"],
                })

        self.rooms_detected = rooms
        print(f"[INFO] Fused {len(rooms)} rooms (OCR: {len(ocr_rooms)}, YOLO: {len(yolo_groups)})")
        return rooms

    def _group_yolo_by_room(self):
        """Group YOLO objects into rooms"""
        if not self.detections:
            return []

        h, w = self.plan_image.shape[:2]
        total_area = h * w

        # Group by room type using ROOM_GROUPING
        room_objects = {}

        for d in self.detections:
            cls_name = d["class_name"]
            room_type = d["room_type"]

            # Skip structural elements
            if room_type in ["wall", "window", "door", "opening", "railing", "unknown"]:
                continue

            # Skip very small
            if d["area"] < total_area * 0.0001:
                continue

            # Group by room type
            if room_type not in room_objects:
                room_objects[room_type] = []
            room_objects[room_type].append(d)

        # Create grouped rooms
        grouped = []
        for i, (room_type, objects) in enumerate(room_objects.items()):
            # Merge bounding boxes
            x1 = min(o["bbox"][0] for o in objects)
            y1 = min(o["bbox"][1] for o in objects)
            x2 = max(o["bbox"][2] for o in objects)
            y2 = max(o["bbox"][3] for o in objects)

            room_info = CLASS_TO_ROOM.get(objects[0]["class_name"], {})

            grouped.append({
                "id": i,
                "room_type": room_type,
                "hindi": room_info.get("hindi", "अज्ञात"),
                "icon": room_info.get("icon", "❓"),
                "class_name": objects[0]["class_name"],
                "confidence": round(sum(o["confidence"] for o in objects) / len(objects), 3),
                "bbox": [x1, y1, x2, y2],
                "center": [(x1+x2)//2, (y1+y2)//2],
                "area": (x2-x1) * (y2-y1),
                "objects_count": len(objects),
            })

        return grouped

    # ═══════════════════════════════════════════════════════════════
    # BOUNDARY + GRID
    # ═══════════════════════════════════════════════════════════════
    def detect_boundary(self):
        """Detect outer boundary"""
        img = self.plan_image
        if img is None:
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        return {
            "bbox": [int(x), int(y), int(w), int(h)],
            "area": int(cv2.contourArea(largest)),
        }

    def overlay_81_grid(self):
        """Overlay 9x9 Vastu grid"""
        img = self.plan_image
        if img is None:
            return None

        boundary = self.detect_boundary()
        if not boundary:
            return None

        x, y, w, h = boundary["bbox"]
        overlay = img.copy()
        cell_w = w / 9
        cell_h = h / 9

        grid_cells = []
        for row in range(9):
            for col in range(9):
                cx = int(x + col * cell_w)
                cy = int(y + row * cell_h)
                cw = int(cell_w)
                ch = int(cell_h)

                cv2.rectangle(overlay, (cx, cy), (cx + cw, cy + ch), (0, 255, 100), 1)

                zone = self._get_zone(row, col)
                grid_cells.append({
                    "row": row,
                    "col": col,
                    "pada": row * 9 + col + 1,
                    "bbox": [cx, cy, cw, ch],
                    "zone": zone,
                })

        # Draw OCR labels
        for ocr in self.ocr_results:
            x1, y1, x2, y2 = ocr["bbox"]
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 100, 0), 2)
            cv2.putText(overlay, ocr["text"][:20], (x1, y1-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 100, 0), 1)

        # Draw YOLO detections
        for det in self.detections:
            if det["room_type"] in ["wall", "window", "door", "unknown"]:
                continue
            x1, y1, x2, y2 = det["bbox"]
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 200, 255), 2)
            label = f"{det['class_name']}"
            cv2.putText(overlay, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 200, 255), 1)

        result = cv2.addWeighted(overlay, 0.7, img, 0.3, 0)
        self.grid_81 = grid_cells
        return result

    def _get_zone(self, row, col):
        if row < 3 and col < 3: return "NE"
        if row < 3 and col > 5: return "NW"
        if row > 5 and col < 3: return "SE"
        if row > 5 and col > 5: return "SW"
        if row < 3: return "N"
        if row > 5: return "S"
        if col < 3: return "W"
        if col > 5: return "E"
        return "CENTER"

    def map_rooms_to_grid(self):
        """Map rooms to 81-pad grid"""
        if not self.grid_81:
            return []

        mappings = []
        for room in self.rooms_detected:
            cx, cy = room["center"]

            for cell in self.grid_81:
                gx, gy, gw, gh = cell["bbox"]
                if gx <= cx <= gx + gw and gy <= cy <= gy + gh:
                    mappings.append({
                        "room_type": room["room_type"],
                        "hindi": room.get("hindi", "अज्ञात"),
                        "icon": room.get("icon", "❓"),
                        "label": room.get("label", ""),
                        "source": room["source"],
                        "confidence": room["confidence"],
                        "pada": cell["pada"],
                        "row": cell["row"],
                        "col": cell["col"],
                        "zone": cell["zone"],
                        "bbox": room["bbox"],
                        "objects_count": room.get("objects_count", 0),
                    })
                    break

        return mappings

    def image_to_base64(self, image):
        if isinstance(image, np.ndarray):
            _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 85])
            return base64.b64encode(buffer).decode('utf-8')
        return None

    def analyze(self, image_path):
        """Complete 4-layer analysis"""
        self.load_plan(image_path)

        # Layer 1: YOLO
        detections = self.detect_with_yolo()

        # Layer 2: OCR
        ocr_results = self.detect_text_ocr()

        # Layer 3: Walls
        walls = self.detect_walls()

        # Layer 4: Fusion
        rooms = self.fuse_rooms()

        # Grid + mapping
        boundary = self.detect_boundary()
        grid_image = self.overlay_81_grid()
        mappings = self.map_rooms_to_grid()

        return {
            "yolo_available": self.yolo_model is not None,
            "ocr_available": len(self.ocr_results) > 0,
            "total_detections": len(detections),
            "detections": detections,
            "ocr_results": ocr_results,
            "wall_lines": walls,
            "rooms_detected": len(rooms),
            "rooms": rooms,
            "boundary": boundary,
            "grid_overlay_base64": self.image_to_base64(grid_image),
            "room_mappings": mappings,
        }
