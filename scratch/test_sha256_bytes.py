import sys
sys.path.insert(0, ".")

from backend.services.hashing_service import hashing_service

with open("temp.jpg", "rb") as f:
    raw_bytes_A = f.read()

# Hash original file twice
hash_A1 = hashing_service.generate_sha256(raw_bytes_A)
hash_A2 = hashing_service.generate_sha256(raw_bytes_A)

print("--- SHA-256 VERIFICATION ---")
print("Hash A1:", hash_A1)
print("Hash A2:", hash_A2)
print("Determinism Match (A1 == A2):", hash_A1 == hash_A2)

# Modify 1 single byte at the end of the byte array
raw_bytes_B = raw_bytes_A + b"\x00"
hash_B = hashing_service.generate_sha256(raw_bytes_B)

print("Hash B (1 byte appended):", hash_B)
print("Tamper Detection (A1 != B):", hash_A1 != hash_B)
