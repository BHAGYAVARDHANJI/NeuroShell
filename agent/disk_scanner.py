import os

def scan_disk(path=".", top_n=5):

    file_sizes = []

    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                full_path = os.path.join(root, file)
                size = os.path.getsize(full_path)
                file_sizes.append((size, full_path))
            except:
                pass

    file_sizes.sort(reverse=True)

    return file_sizes[:top_n]