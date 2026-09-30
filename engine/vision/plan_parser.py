"""
Vastu One - Floor Plan Parser
Using YOLOv8 (FloorPlanCAD model) + OpenCV
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import base64
import io

# YOLO imports (graceful fallback)
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("[WARNING] YOLO not available — using basic detection")


# Model path
MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "best.pt"


# Room type mapping from FloorPlanCAD classes
ROOM_CLASS_MAP = {
    "wall": "wall",
    "window": "window",
    "door": "door",
    "bed": "bedroom",
    "sofa": "living",
    "table": "living",
    "chair": "living",
    "tv": "living",
    "toilet": "toilet",
    "sink": "kitchen",
    "kitchen": "kitchen",
    "stair": "stair",
    "elevator": "elevator",
    "bathtub": "bathroom",
    "shower": "bathroom",
}

# Map to Vastu room types
VASTU_ROOM_MAP = {
    "bedroom": "bedroom",
    "kitchen": "kitchen",
    "toilet": "toilet",
    "bathroom": "bathroom",
    "living": "living",
    "wall": "wall",
    "window": "window",
    "door": "door",
    "stair": "stair",
    "elevator": "elevator",
}


class PlanParser:
    """Floor plan analysis: YOLO detection + 81-pad grid"""

    def __init__(self):
        self.plan_image = None
        self.detections = []
        self.rooms_detected = []
        self.grid_81 = []
        self.north_angle = 0
        self.yolo_model = None

        # Load YOLO model if available
        if YOLO_AVAILABLE and MODEL_PATH.exists():
            try:
                self.yolo_model = YOLO(str(MODEL_PATH))
                print(f"[INFO] YOLO model loaded: {MODEL_PATH}")
            except Exception as e:
                print(f"[ERROR] YOLO load failed: {e}")
                self.yolo_model = None
        else:
            if not MODEL_PATH.exists():
                print(f"[WARNING] Model not found: {MODEL_PATH}")

    def load_plan(self, image_path):
        """Load plan image"""
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")

        # Resize if too large
        h, w = img.shape[:2]
        max_dim = 1600
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        self.plan_image = img
        return img

    def detect_with_yolo(self):
        """YOLO detection — rooms, walls, doors, windows"""
        if not self.yolo_model:
            print("[INFO] YOLO model not loaded — skipping")
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

                        # Map to Vastu room type
                        vastu_type = ROOM_CLASS_MAP.get(cls_name.lower(), "unknown")

                        detections.append({
                            "id": i,
                            "class_name": cls_name,
                            "room_type": vastu_type,
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

    def group_into_rooms(self, min_area_ratio=0.005):
        """Group detections into logical rooms by area"""
        if not self.detections:
            return []

        h, w = self.plan_image.shape[:2]
        total_area = h * w

        # Keep only large detections (rooms)
        rooms = []
        for d in self.detections:
            if d["area"] < total_area * min_area_ratio:
                continue
            if d["area"] > total_area * 0.5:
                continue

            # Skip walls, doors, windows for room grouping
            if d["room_type"] in ["wall", "window", "door"]:
                continue

            rooms.append({
                "room_type": d["room_type"],
                "class_name": d["class_name"],
                "confidence": d["confidence"],
                "bbox": d["bbox"],
                "center": d["center"],
                "area": d["area"],
            })

        self.rooms_detected = rooms
        return rooms

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

        # Draw YOLO detections on top
        for det in self.detections:
            x1, y1, x2, y2 = det["bbox"]
            color = (0, 200, 255) if det["room_type"] not in ["wall", "window", "door"] else (200, 200, 200)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 2)
            label = f"{det['class_name']} {det['confidence']:.2f}"
            cv2.putText(overlay, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

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
        """Map detected rooms to 81-pad grid"""
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
                        "class_name": room["class_name"],
                        "confidence": room["confidence"],
                        "pada": cell["pada"],
                        "row": cell["row"],
                        "col": cell["col"],
                        "zone": cell["zone"],
                        "bbox": room["bbox"],
                    })
                    break

        return mappings

    def image_to_base64(self, image):
        if isinstance(image, np.ndarray):
            _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 85])
            return base64.b64encode(buffer).decode('utf-8')
        return None

    def analyze(self, image_path):
        """Complete analysis"""
        self.load_plan(image_path)
        detections = self.detect_with_yolo()
        rooms = self.group_into_rooms()
        boundary = self.detect_boundary()
        grid_image = self.overlay_81_grid()
        mappings = self.map_rooms_to_grid()

        return {
            "yolo_available": self.yolo_model is not None,
            "total_detections": len(detections),
            "detections": detections,
            "rooms_detected": len(rooms),
            "rooms": rooms,
            "boundary": boundary,
            "grid_overlay_base64": self.image_to_base64(grid_image),
            "room_mappings": mappings,
        }