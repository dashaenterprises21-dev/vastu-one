from pathlib import Path
import shutil
from datetime import datetime

# Paths
parts_dir = Path("temp_scripts")
engine_file = Path("engine/astro/deep_world_prediction.py")

# Backup
backup = f"engine/astro/deep_world_prediction.py.backup-v2-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
shutil.copy(engine_file, backup)
print(f"✅ Backup: {backup}")

# Combine all parts
parts = [
    "engine_part1.py",
    "engine_part2.py",
    "engine_part3.py",
    "engine_part4.py",
    "engine_part5.py",
    "engine_part6.py",
]

combined = ""
for part in parts:
    part_path = parts_dir / part
    if part_path.exists():
        content = part_path.read_text(encoding="utf-8")
        combined += content + "\n\n"
        print(f"✅ Added: {part} ({len(content)} bytes)")
    else:
        print(f"❌ Missing: {part}")

# Write combined file
engine_file.write_text(combined, encoding="utf-8")
print(f"\n✅ Engine written: {engine_file}")
print(f"   Size: {engine_file.stat().st_size} bytes")
print(f"   Lines: {len(combined.splitlines())}")
