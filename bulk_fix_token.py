from pathlib import Path

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

total_fixes = 0
for file_path in files:
    p = Path(file_path)
    if not p.exists():
        print(f"SKIP: {file_path} (not found)")
        continue

    c = p.read_text(encoding="utf-8")
    before = c.count("vastu_token")
    c = c.replace('"vastu_token"', '"vastu_access_token"')
    c = c.replace("'vastu_token'", "'vastu_access_token'")
    after = c.count("vastu_token")
    fixed = before - after

    if fixed > 0:
        # Backup
        backup = p.with_suffix(p.suffix + ".backup-before-token-fix")
        backup.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")

        p.write_text(c, encoding="utf-8")
        print(f"FIXED: {file_path} ({fixed} occurrences)")
        total_fixes += fixed
    else:
        print(f"SKIP: {file_path} (already fixed or no match)")

print(f"\nTotal fixes: {total_fixes}")