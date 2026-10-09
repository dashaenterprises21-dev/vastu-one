from pathlib import Path

files = [
    "frontend/static/auth.js",
    "frontend/static/chakra-form.js",
    "frontend/static/chakra-overlay.js",
    "frontend/static/dashboard.js",
    "frontend/static/pricing.js",
    "frontend/static/profile.js",
    "frontend/static/reports.js",
    "frontend/signup.html",
]

total = 0
for fp in files:
    p = Path(fp)
    if not p.exists():
        continue

    c = p.read_text(encoding="utf-8")
    before = c.count('"/login"')
    c = c.replace('"/login"', '"/login.html"')
    c = c.replace("'/login'", "'/login.html'")
    after = c.count('"/login"')
    fixed = before - after

    if fixed > 0:
        backup = Path(str(p) + ".backup-login-url")
        backup.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        p.write_text(c, encoding="utf-8")
        print(f"FIXED: {fp} ({fixed})")
        total += fixed
    else:
        print(f"CLEAN: {fp}")

print(f"\nTotal: {total}")