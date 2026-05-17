import os

def collect_project_files(base_path=".", limit=5):

    collected = []

    for root, dirs, files in os.walk(base_path):
        for file in files:

            if file.endswith(".py"):

                try:
                    full_path = os.path.join(root, file)

                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(2000)

                    collected.append((full_path, content))

                    if len(collected) >= limit:
                        return collected

                except:
                    pass

    return collected