from pdf_engine.styles import FONT, FONT_BOLD
"""
Vastu AI - Charts
Score circle, bar charts, grid visualizations
"""

from reportlab.graphics.shapes import Drawing, Circle, Rect, String, Line, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors
from reportlab.lib.units import mm
from pdf_engine.styles import BRAND


def score_circle(score, size=60):
    """Animated-looking circular score gauge"""
    d = Drawing(size * mm, size * mm)
    cx, cy = size * mm / 2, size * mm / 2
    radius = (size * mm / 2) - 4 * mm

    # Background circle
    d.add(Circle(cx, cy, radius,
                 fillColor=BRAND["border"],
                 strokeColor=None))

    # Progress arc (as polygon approximation)
    # Simple approach: show as pie slice
    pct = min(100, max(0, score)) / 100

    # Colored circle (smaller, represents progress)
    inner_radius = radius * pct
    if pct > 0:
        d.add(Circle(cx, cy, inner_radius,
                     fillColor=BRAND["primary"],
                     strokeColor=None))

    # Score text
    d.add(String(cx, cy - 2 * mm,
                 f"{score:.1f}",
                 fontName=FONT_BOLD,
                 fontSize=18,
                 fillColor=colors.white,
                 textAnchor="middle"))

    d.add(String(cx, cy - 10 * mm,
                 "/ 100",
                 fontName=FONT,
                 fontSize=8,
                 fillColor=colors.white,
                 textAnchor="middle"))

    return d


def elements_bar_chart(balance_dict):
    """
    Bar chart of 5 elements balance
    balance_dict: {"Earth": 0, "Water": -2, ...}
    """
    d = Drawing(160 * mm, 60 * mm)

    chart = VerticalBarChart()
    chart.x = 10 * mm
    chart.y = 10 * mm
    chart.width = 140 * mm
    chart.height = 40 * mm

    names = list(balance_dict.keys())
    values = [list(balance_dict.values())]

    chart.data = values
    chart.categoryAxis.categoryNames = names
    chart.categoryAxis.labels.fontName = FONT
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.dy = -8

    # Color bars based on value
    for i, val in enumerate(values[0]):
        if val < 0:
            chart.bars[0].fillColor = BRAND["red"]
        elif val > 3:
            chart.bars[0].fillColor = BRAND["green"]
        else:
            chart.bars[0].fillColor = BRAND["primary"]
        break  # single series

    chart.valueAxis.valueMin = min(-5, min(values[0]) - 1)
    chart.valueAxis.valueMax = max(5, max(values[0]) + 1)
    chart.valueAxis.labels.fontName = FONT
    chart.valueAxis.labels.fontSize = 7

    chart.barWidth = 8 * mm
    chart.groupSpacing = 6

    d.add(chart)
    return d


def pada_grid_visual(grid_data):
    """
    Visual 9x9 grid of 81 padas with devatas
    grid_data: list of dicts with {row, col, devata, zone, has_defect}
    """
    cell = 15 * mm
    size = 9 * cell
    d = Drawing(size, size)

    zone_colors = {
        "NE": colors.HexColor("#10b981"),
        "N":  colors.HexColor("#3b82f6"),
        "E":  colors.HexColor("#f59e0b"),
        "SE": colors.HexColor("#ef4444"),
        "S":  colors.HexColor("#ea580c"),
        "SW": colors.HexColor("#d97706"),
        "W":  colors.HexColor("#8b5cf6"),
        "NW": colors.HexColor("#0ea5e9"),
        "CENTER": colors.HexColor("#fbbf24"),
    }

    for item in grid_data:
        r, c = item["row"], item["col"]
        x = c * cell
        y = (8 - r) * cell

        # Cell background
        fill = zone_colors.get(item.get("zone", "N"), colors.gray)
        if item.get("has_defect"):
            fill = BRAND["red"]

        d.add(Rect(x + 1, y + 1, cell - 2, cell - 2,
                   fillColor=fill,
                   strokeColor=colors.white,
                   strokeWidth=0.5))

        # Devata label
        devata_short = item.get("hindi", "")[:2] if item.get("hindi") else ""
        if devata_short:
            d.add(String(x + cell / 2, y + cell / 2 - 2,
                         devata_short,
                         fontName=FONT_BOLD,
                         fontSize=7,
                         fillColor=colors.white,
                         textAnchor="middle"))

    return d