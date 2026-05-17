import os
from core.config import IGNORE_DIRS, LARGE_FILE_BYTES

def organize_project():
    report = []
    seen = set()

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d.lower() not in IGNORE_DIRS]

        for d in dirs:
            full = os.path.join(root, d)
            name = d.lower()
            if name == "venv" and "venv" not in seen: 
                report.append(f"Virtual environment folder → {full}")
                seen.add("venv")

        for f in files:
            full = os.path.join(root, f)
            if f.endswith(".exe"):
                try:
                    size = os.path.getsize(full)
                    if size > LARGE_FILE_BYTES:
                        report.append(f"Large executable → {full}")
                except Exception:
                    pass

    if not report:
        report.append("Project looks clean.")

    return report