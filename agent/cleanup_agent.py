import os
import shutil
from core.config import IGNORE_DIRS, JUNK_DIRS

def plan_cleanup():
    actions = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d.lower() not in IGNORE_DIRS]

        for d in dirs:
            if d.lower() in JUNK_DIRS:
                full = os.path.join(root, d)
                actions.append(full)

    return actions

def execute_cleanup(actions):
    total_deleted = 0
    for path in actions:
        try:
            shutil.rmtree(path)
            print(f"✔ Deleted → {path}")
            total_deleted += 1
        except Exception:
            print(f"✖ Failed → {path}")

    print(f"\nCleanup Finished. Removed {total_deleted} junk folders.")