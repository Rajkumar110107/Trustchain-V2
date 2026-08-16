import os
import hashlib

real_dir = "dataset/real"
fake_dir = "dataset/fake"

real_files = set(os.listdir(real_dir)) if os.path.exists(real_dir) else set()
fake_files = set(os.listdir(fake_dir)) if os.path.exists(fake_dir) else set()

common = real_files.intersection(fake_files)
print(f"Total Real files: {len(real_files)}")
print(f"Total Fake files: {len(fake_files)}")
print(f"Common filenames: {len(common)}")

identical_count = 0
different_count = 0
different_pairs = []

for fn in sorted(common):
    r_path = os.path.join(real_dir, fn)
    f_path = os.path.join(fake_dir, fn)
    
    with open(r_path, "rb") as f1, open(f_path, "rb") as f2:
        h1 = hashlib.sha256(f1.read()).hexdigest()
        h2 = hashlib.sha256(f2.read()).hexdigest()
        
    if h1 == h2:
        identical_count += 1
    else:
        different_count += 1
        different_pairs.append((fn, h1[:10], h2[:10]))

print(f"\nIdentical SHA-256 pairs (Invalid Forgeries): {identical_count}")
print(f"Different SHA-256 pairs (GENUINE Forgeries): {different_count}")

print("\nSample Genuine Forgery Pairs:")
for item in different_pairs[:10]:
    print(f"  Filename: {item[0]} | Real SHA: {item[1]}... | Fake SHA: {item[2]}...")
