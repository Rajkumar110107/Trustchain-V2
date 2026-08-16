import urllib.request
import json

base_url = "http://127.0.0.1:8000"

print("--- BACKEND API ENDPOINT VERIFICATION ---")

# 1. Health Check
req_health = urllib.request.Request(f"{base_url}/health")
with urllib.request.urlopen(req_health) as res:
    data = json.loads(res.read().decode())
    print("GET /health ->", data)

# 2. Verify Document
req_verify = urllib.request.Request(
    f"{base_url}/api/verify",
    data=json.dumps({"hash": "2ae5de886ad358c7e55d9dcd12e09cada74114f7689bc5e8399ba73f59b49713"}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req_verify) as res:
    data = json.loads(res.read().decode())
    print("POST /api/verify -> status:", data.get("status"), "| verified:", data.get("verified"))

# 3. Register Document
req_register = urllib.request.Request(
    f"{base_url}/api/register",
    data=json.dumps({"hash": "36c9c052d17371def956e21a52acf5a0456507e6d6cad743c08dfc43d0774118"}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req_register) as res:
    data = json.loads(res.read().decode())
    print("POST /api/register -> status:", data.get("status"), "| success:", data.get("success"), "| tx_hash:", data.get("tx_hash"))
