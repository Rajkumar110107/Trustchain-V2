import os
import hashlib
from PIL import Image

test_files = [
    ("temp.jpg", "AUTHENTIC"),
    ("dataset/real/X00016469622.png", "AUTHENTIC"),
    ("dataset/real/X00016469623.png", "AUTHENTIC"),
    ("dataset/real/X51005200938.png", "AUTHENTIC"),
    ("dataset/real/X51005230617.png", "AUTHENTIC"),
    ("dataset/fake/X00016469622.png", "FORGED"),
    ("dataset/fake/X00016469623.png", "FORGED"),
    ("dataset/fake/X51005200938.png", "FORGED"),
    ("dataset/fake/X51005230617.png", "FORGED"),
    ("dataset/fake/X51005268200.png", "FORGED"),
]

print("--- DATASET INTEGRITY AUDIT ---")
records = []

for idx, (path, expected) in enumerate(test_files, 1):
    if not os.path.exists(path):
        print(f"ID {idx}: {path} NOT FOUND")
        continue

    with open(path, "rb") as f:
        data = f.read()
        sha = hashlib.sha256(data).hexdigest()
        size = len(data)

    with Image.open(path) as img:
        dims = f"{img.width}x{img.height}"
        fmt = img.format

    record = {
        "id": idx,
        "filename": os.path.basename(path),
        "path": os.path.abspath(path),
        "expected": expected,
        "sha256": sha,
        "size": size,
        "dimensions": dims
    }
    records.append(record)
    print(f"ID {idx:02d} | {expected:<9} | {record['filename']:<20} | SHA: {sha[:16]}... | {size}B | {dims}")

# Check duplicate pairs
print("\n--- DUPLICATE SHA-256 CHECK ---")
hashes = {}
for r in records:
    h = r["sha256"]
    if h in hashes:
        print(f"[DUPLICATE FOUND] ID {r['id']} ({r['filename']}, {r['expected']}) is IDENTICAL TO ID {hashes[h]['id']} ({hashes[h]['filename']}, {hashes[h]['expected']})")
    else:
        hashes[h] = r
