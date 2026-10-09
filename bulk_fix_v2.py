from pathlib import Path
import re

files = [
    "frontend/static/auth.js",
    "frontend/static/chakra-form.js",
    "frontend/static/chakra-overlay.js",
    "frontend/static/dashboard.js",
    "frontend/static/pricing.js",
    "frontend/static/profile.js",
    "frontend/static/reports.js",
    "frontend/admin.html",
]

total = 0
for fp in files:
    p = Path(fp)
    if not p.exists():
        continue

    c = p.read_text(encoding="utf-8")
    # Find all vastu_token occurrences (with word boundary)
    matches = re.findall(r'\bvastu_token\b', c)
    count = len(matches)

    if count > 0:
        # Backup
        backup = Path(str(p) + ".backup-token-v2")
        backup.write_text(c, encoding="utf-8")

        # Replace (preserve quote style)
        c = c.replace('"vastu_token"', '"vastu_access_token"')
        c = c.replace("'vastu_token'", "'vastu_access_token'")
        # Also handle raw occurrences
        c = re.sub(r'\bvastu_token\b', 'vastu_access_token', c)

        p.write_text(c, encoding="utf-8")
        print(f"FIXED: {fp} ({count} occurrences)")
        total += count
    else:
        print(f"CLEAN: {fp}")

print(f"\nTotal: {total}")