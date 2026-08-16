import os
import csv
import hashlib

def load_ground_truth(file_path):
    records = []
    if not os.path.exists(file_path):
        return records
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 4:
                img_name = row[0].strip()
                is_forged = int(row[3].strip())
                records.append((img_name, is_forged))
    return records

gt_train = load_ground_truth("findit2/train.txt")
gt_val = load_ground_truth("findit2/val.txt")
gt_test = load_ground_truth("findit2/test.txt")

all_gt = gt_train + gt_val + gt_test
print(f"Total Ground Truth Records: {len(all_gt)}")

authentic_files = [(img, is_f) for img, is_f in all_gt if is_f == 0]
forged_files = [(img, is_f) for img, is_f in all_gt if is_f == 1]

print(f"Ground Truth Authentic (forged==0): {len(authentic_files)}")
print(f"Ground Truth Forged (forged==1): {len(forged_files)}")

# Find actual file paths for 5 Authentic and 5 Forged
def find_image_path(img_name):
    for root, dirs, files in os.walk("findit2"):
        if img_name in files:
            return os.path.join(root, img_name)
    return None

auth_samples = []
for img_name, _ in authentic_files:
    p = find_image_path(img_name)
    if p and os.path.exists(p):
        auth_samples.append((img_name, p))
    if len(auth_samples) == 5:
        break

forged_samples = []
for img_name, _ in forged_files:
    p = find_image_path(img_name)
    if p and os.path.exists(p):
        forged_samples.append((img_name, p))
    if len(forged_samples) == 5:
        break

print("\n--- Genuine Authentic Samples (forged==0) ---")
for name, p in auth_samples:
    print(f"  {name} -> {p}")

print("\n--- Genuine Forged Samples (forged==1) ---")
for name, p in forged_samples:
    print(f"  {name} -> {p}")
