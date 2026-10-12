from pathlib import Path

p = Path("frontend/world-prediction.html")
c = p.read_text(encoding="utf-8")

if 'world-map.js?v=' not in c:
    c = c.replace(
        '<script src="/static/world-map.js"></script>',
        '<script src="/static/world-map.js?v=2"></script>'
    )
    p.write_text(c, encoding="utf-8")
    print("✅ Cache busting added — v=2")
else:
    print("ℹ️ Already has version")
