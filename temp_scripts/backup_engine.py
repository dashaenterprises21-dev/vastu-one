from pathlib import Path

# Backup pehle
import shutil
from datetime import datetime
backup = f"engine/astro/deep_world_prediction.py.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
shutil.copy("engine/astro/deep_world_prediction.py", backup)
print(f"✅ Backup: {backup}")
