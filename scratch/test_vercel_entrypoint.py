import sys
sys.path.insert(0, ".")

from backend.index import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("--- TESTING VERCEL FASTAPI ENTRYPOINT ---")

res_root = client.get("/")
print("GET / -> Status:", res_root.status_code, "| Response:", res_root.json())

res_health = client.get("/health")
print("GET /health -> Status:", res_health.status_code, "| Response:", res_health.json())

assert res_root.status_code == 200
assert res_health.status_code == 200
assert res_health.json()["status"] == "healthy"

print("\n[OK] Local Vercel FastAPI entrypoint test PASSED successfully!")
