"""
Vastu AI - PDF Generator (v2)
Loads Noto Sans Devanagari from file:// path
"""

from pathlib import Path
from datetime import datetime
from jinja2 import Template
from playwright.sync_api import sync_playwright
from PIL import Image
import io
import base64

TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "report.html"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Windows font path
FONT_REGULAR = Path("C:/Windows/Fonts/NotoSansDevanagari-Regular.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/NotoSansDevanagari-Bold.ttf")


def get_font_css():
    """Noto Sans Devanagari को base64 से embed करो"""
    if not FONT_REGULAR.exists():
        print(f"[WARNING] Font not found: {FONT_REGULAR}")
        return ""

    reg_b64 = base64.b64encode(FONT_REGULAR.read_bytes()).decode()
    css = f"""
@font-face {{
    font-family: 'VastuFont';
    src: url(data:font/truetype;charset=utf-8;base64,{reg_b64}) format('truetype');
    font-weight: normal;
    font-style: normal;
}}
"""
    if FONT_BOLD.exists():
        bold_b64 = base64.b64encode(FONT_BOLD.read_bytes()).decode()
        css += f"""
@font-face {{
    font-family: 'VastuFont';
    src: url(data:font/truetype;charset=utf-8;base64,{bold_b64}) format('truetype');
    font-weight: bold;
    font-style: normal;
}}
"""
    return css


def build_chakra_cells(all_status, plan_data):
    status_map = {s["pada"]: s for s in all_status}
    plan_map = {}
    for p in plan_data:
        plan_map[(p["row"], p["col"])] = p["object"]

    cells = []
    for r in range(9):
        row = []
        for c in range(9):
            pada = r * 9 + c + 1
            status = status_map.get(pada, {})
            obj = plan_map.get((r, c), "")

            if r < 3 and c < 3: zc = "NE"
            elif r < 3 and c > 5: zc = "NW"
            elif r > 5 and c < 3: zc = "SE"
            elif r > 5 and c > 5: zc = "SW"
            elif r < 3: zc = "N"
            elif r > 5: zc = "S"
            elif c < 3: zc = "W"
            elif c > 5: zc = "E"
            else: zc = "brahma"

            hindi = status.get("hindi", "")[:2] if status.get("hindi") else ""
            obj_short = obj[:4] if obj else ""

            st = "neutral"
            if status.get("status") == "defect": st = "defect"
            elif status.get("status") == "correct": st = "correct"
            elif zc == "brahma": st = "brahma"

            row.append({
                "pada": pada,
                "hindi_short": hindi or "—",
                "object": obj,
                "object_short": obj_short,
                "zone_class": zc,
                "status": st,
            })
        cells.append(row)
    return cells


def build_all_padas_detail(raw_devatas, all_status):
    status_map = {s["pada"]: s for s in all_status}
    all_devatas = raw_devatas["outer_devatas"] + raw_devatas["inner_devatas"]

    result = []
    for d in all_devatas:
        status = status_map.get(d["pada"], {})
        result.append({
            "pada": d["pada"],
            "devata": d["name"],
            "hindi": d["hindi"],
            "direction": d["direction"],
            "status": status.get("status", "neutral"),
            "object": status.get("object", ""),
            "positive": d.get("positive_objects", [])[:3],
            "negative": d.get("negative_objects", [])[:3],
        })
    return result


class HTMLVastuReport:
    def __init__(self, output_path):
        self.output_path = output_path

    def generate(self, data, client_info=None, raw_devatas=None, plan_data=None):
        client_info = client_info or {}
        plan_data = plan_data or []

        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            template = Template(f.read())

        all_status = data.get("devata_audit", {}).get("all_devatas_status", [])
        chakra_cells = build_chakra_cells(all_status, plan_data)

        all_padas_detail = []
        if raw_devatas:
            all_padas_detail = build_all_padas_detail(raw_devatas, all_status)

        html_content = template.render(
            final_score=data["final_score"],
            devata_audit=data["devata_audit"],
            element_balance=data["element_balance"],
            brahma_audit=data.get("brahma_audit", {}),
            direction_strength=data.get("direction_strength", {"zones": []}),
            room_analysis=data.get("room_analysis", {"rooms": [], "total_rooms_analyzed": 0, "correct_placements": 0, "defects": 0}),
            remedies=data["remedies"],
            chakra_cells=chakra_cells,
            all_padas_details=all_padas_detail,
            all_padas_detail=all_padas_detail,
            client_name=client_info.get("name", "ग्राहक"),
            client_address=client_info.get("address", "—"),
            report_date=datetime.now().strftime("%d %B %Y"),
            report_id=f"VAI-{datetime.now().strftime('%Y%m%d%H%M')}",
            font_css=get_font_css(),
        )

        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=CHROME_PATH,
                headless=True,
                args=[
                    "--font-render-hinting=none",
                    "--disable-font-subpixel-positioning",
                    "--disable-lcd-text",
                    "--force-color-profile=srgb",
                ]
            )
            page = browser.new_page(viewport={"width": 794, "height": 1123})
            page.set_content(html_content, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # Font load confirm करो
            try:
                loaded = page.evaluate("() => document.fonts.check('16px \"VastuFont\"')")
                print(f"[INFO] VastuFont loaded: {loaded}")
            except Exception as e:
                print(f"[WARN] Font check failed: {e}")

            page.wait_for_timeout(2000)

            img_bytes = page.screenshot(full_page=True, type="png")
            browser.close()

        img = Image.open(io.BytesIO(img_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")

        width, height = img.size
        page_height = int(width * 1.414)

        pages = []
        top = 0
        while top < height:
            bottom = min(top + page_height, height)
            page_img = img.crop((0, top, width, bottom))
            if page_img.size[1] < page_height:
                padded = Image.new("RGB", (width, page_height), "white")
                padded.paste(page_img, (0, 0))
                page_img = padded
            pages.append(page_img)
            top += page_height

        if pages:
            pages[0].save(
                self.output_path,
                "PDF",
                resolution=150.0,
                save_all=True,
                append_images=pages[1:]
            )

        print(f"[INFO] PDF created: {self.output_path} ({len(pages)} pages)")
        return self.output_path