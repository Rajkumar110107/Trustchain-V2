import os
import shutil
import hashlib

os.makedirs("tests/test_documents/authentic", exist_ok=True)
os.makedirs("tests/test_documents/forged", exist_ok=True)

auth_sources = [
    ("findit2/train/X00016469623.png", "authentic_01.png"),
    ("findit2/train/X00016469670.png", "authentic_02.png"),
    ("findit2/train/X00016469671.png", "authentic_03.png"),
    ("findit2/train/X00016469672.png", "authentic_04.png"),
    ("findit2/train/X51005200938.png", "authentic_05.png"),
]

forged_sources = [
    ("findit2/train/X00016469622.png", "forged_01.png"),
    ("findit2/train/X51005230617.png", "forged_02.png"),
    ("findit2/train/X51005361906.png", "forged_03.png"),
    ("findit2/train/X51005361946.png", "forged_04.png"),
    ("findit2/train/X51005365179.png", "forged_05.png"),
]

print("--- COPYING CORRECT GROUND TRUTH SAMPLES ---")

for src, dst_name in auth_sources:
    dst_path = os.path.join("tests/test_documents/authentic", dst_name)
    shutil.copy2(src, dst_path)
    with open(dst_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    print(f"Authentic: {dst_name} <- {src} | SHA: {sha[:16]}")

for src, dst_name in forged_sources:
    dst_path = os.path.join("tests/test_documents/forged", dst_name)
    shutil.copy2(src, dst_path)
    with open(dst_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    print(f"Forged:    {dst_name} <- {src} | SHA: {sha[:16]}")
