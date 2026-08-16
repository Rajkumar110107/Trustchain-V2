import os
import hashlib

findit_dir = "findit2"
all_findit_files = []

for root, dirs, files in os.walk(findit_dir):
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(root, file)
            all_findit_files.append((file, path))

print(f"Total FindIt2 image files found: {len(all_findit_files)}")

# Group by filename
by_name = {}
for name, path in all_findit_files:
    by_name.setdefault(name, []).append(path)

print(f"Unique filenames in FindIt2: {len(by_name)}")

different_hash_pairs = []

for name, paths in by_name.items():
    if len(paths) > 1:
        hashes = []
        for p in paths:
            with open(p, "rb") as f:
                hashes.append(hashlib.sha256(f.read()).hexdigest())
        if len(set(hashes)) > 1:
            different_hash_pairs.append((name, paths, hashes))

print(f"Filenames with DIFFERENT SHA-256 hashes across folders: {len(different_hash_pairs)}")
for item in different_hash_pairs[:10]:
    print("  File:", item[0])
    for p, h in zip(item[1], item[2]):
        print("    ", p, "-> SHA:", h[:12])
