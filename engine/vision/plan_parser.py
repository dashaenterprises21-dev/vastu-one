"""
Vastu One - Advanced Floor Plan Parser v2.1
4-Layer System: YOLO + Tesseract OCR + Walls + Fusion
(EasyOCR removed to save RAM on Railway free tier)
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import base64
import io
import os
import platform

from engine.vision.class_mapping import CLASS_TO_ROOM, ROOM_GROUPING, get_room_info

# ═══ YOLO ═══
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("[WARNING] YOLO not available")

# ═══ TESSERACT OCR ═══
try:
    import pytesseract
    if platform.system() == "Windows":
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
        ]
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                print(f"[INFO] Tesseract path: {path}")
                break
    elif platform.system() == "Linux":
        # Railway pe Tesseract /usr/bin/tesseract pe hota hai
        if os.path.exists("/usr/bin/tesseract"):
            pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
            print("[INFO] Tesseract path: /usr/bin/tesseract")
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("[WARNING] pytesseract not available")

# EasyOCR disabled (RAM saving)
EASYOCR_AVAILABLE = False


MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "best.pt"

# OCR keywords → room type mapping
OCR_KEYWORDS = {
    "bedroom": ["bed room", "bedroom", "master bedroom", "bed"],
    "kitchen": ["kitchen", "kitchenette", "cook"],
    "toilet": ["toilet", "w.c", "wc", "bathroom", "bath", "washroom", "c.toilet", "c toilet"],
    "living": ["living", "hall", "drawing", "lounge", "sitting", "drg"],
    "dining": ["dining", "dining hall", "dining room"],
    "store": ["store", "storage", "store room"],
    "balcony": ["balcony", "sitout", "sit out", "verandah", "varandah"],
    "stair": ["stair", "staircase", "steps", "up"],
    "entrance": ["entry", "entrance", "main door", "foyer"],
    "parking": ["parking", "garage", "car"],
    "puja": ["puja", "pooja", "temple", "mandir"],
    "study": ["study", "office", "work"],
}


class PlanParser:
    """Advanced floor plan analysis: YOLO + Tesseract OCR + Walls + Fusion"""

    def __init__(self):
        self.plan_image = None
        self.detections = []
        self.ocr_results = []
        self.rooms_detected = []
        self.grid_81 = []
        self.yolo_model = None

        # Load YOLO
        if YOLO_AVAILABLE and MODEL_PATH.exists():
            try:
                self.yolo_model = YOLO(str(MODEL_PATH))
                print(f"[INFO] YOLO loaded: {MODEL_PATH.name}")
            except Exception as e:
                print(f"[ERROR] YOLO load failed: {e}")

    def load_plan(self, image_path):
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")

        h, w = img.shape[:2]
        max_dim = 1800  # Reduced for RAM
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        self.plan_image = img
        return img

    # ═══ LAYER 1: YOLO ═══
    def detect_with_yolo(self):
        if not self.yolo_model:
            return []

        try:
            results = self.yolo_model.predict(
                self.plan_image,
                conf=0.25,
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

    # ═══ LAYER 2: TESSERACT OCR ═══
    def detect_text_ocr(self):
        if self.plan_image is None:
            return []

        results = []

        if TESSERACT_AVAILABLE:
            try:
                # Upscale 1.5x for better OCR
                h, w = self.plan_image.shape[:2]
                scale = 1.5
                upscaled = cv2.resize(self.plan_image, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)
                gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)

                # Threshold for better text
                _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

                # Use psm 11 (sparse text)
                data = pytesseract.image_to_data(
                    thresh,
                    output_type=pytesseract.Output.DICT,
                    config='--psm 11'
                )

                for i, text in enumerate(data['text']):
                    text = text.strip()
                    if not text or len(text) < 3:
                        continue
                    conf = data['conf'][i]
                    if conf < 30:
                        continue
                    text_lower = text.lower()
                    room_type = self._match_text_to_room(text_lower)
                    if room_type:
                        x, y, ww, hh = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                        # Scale back to original
                        x, y = int(x/scale), int(y/scale)
                        ww, hh = int(ww/scale), int(hh/scale)
                        results.append({
                            "text": text,
                            "text_lower": text_lower,
                            "room_type": room_type,
                            "confidence": conf / 100.0,
                            "source": "tesseract",
                            "bbox": [x, y, x+ww, y+hh],
                            "center": [x + ww//2, y + hh//2],
                        })

                print(f"[INFO] Tesseract found {len(results)} labels")
            except Exception as e:
                print(f"[WARNING] Tesseract failed: {e}")

        self.ocr_results = results
        print(f"[INFO] OCR total: {len(results)} labels")
        return results

    def _match_text_to_room(self, text):
        for room_type, keywords in OCR_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    return room_type
        return None

    # ═══ LAYER 3: WALLS ═══
    def detect_walls(self):
        if self.plan_image is None:
            return []

        gray = cv2.cvtColor(self.plan_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        lines = cv2.HoughLinesP(thresh, rho=1, theta=np.pi/180, threshold=80, minLineLength=50, maxLineGap=10)

        wall_lines = []
        if lines is not None:
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

    # ═══ LAYER 4: FUSION ═══
    def fuse_rooms(self):
        rooms = []

        # OCR rooms (primary)
        for ocr in self.ocr_results:
            ocr_room = {
                "room_type": ocr["room_type"],
                "source": "ocr",
                "confidence": ocr["confidence"],
                "bbox": ocr["bbox"],
                "center": ocr["center"],
                "label": ocr["text"],
                "area": (ocr["bbox"][2]-ocr["bbox"][0]) * (ocr["bbox"][3]-ocr["bbox"][1]),
                "objects": [],
                "objects_count": 0,
            }

            # Match YOLO objects near this OCR label
            ox, oy = ocr["center"]
            for d in self.detections:
                if d["room_type"] in ["wall", "window", "door", "unknown"]:
                    continue
                dx, dy = d["center"]
                if abs(ox - dx) < 400 and abs(oy - dy) < 400:
                    ocr_room["objects"].append(d)
                    ocr_room["objects_count"] += 1

            rooms.append(ocr_room)

        self.rooms_detected = rooms
        print(f"[INFO] Fused {len(rooms)} rooms")
        return rooms

    # ═══ BOUNDARY + GRID ═══
    def detect_boundary(self):
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
                    "row": row, "col": col, "pada": row * 9 + col + 1,
                    "bbox": [cx, cy, cw, ch], "zone": zone,
                })

        # Draw OCR labels (orange)
        for ocr in self.ocr_results:
            x1, y1, x2, y2 = ocr["bbox"]
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 100, 0), 2)
            cv2.putText(overlay, ocr["text"][:20], (x1, y1-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 100, 0), 1)

        # Draw YOLO detections (cyan)
        for det in self.detections:
            if det["room_type"] in ["wall", "window", "door", "unknown"]:
                continue
            x1, y1, x2, y2 = det["bbox"]
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 200, 255), 2)

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
            _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 80])
            return base64.b64encode(buffer).decode('utf-8')
        return None

    def analyze(self, image_path):
        self.load_plan(image_path)
        detections = self.detect_with_yolo()
        ocr_results = self.detect_text_ocr()
        walls = self.detect_walls()
        rooms = self.fuse_rooms()
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
