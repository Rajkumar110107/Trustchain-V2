import sys
sys.path.insert(0, ".")

from web3 import Web3
from backend.services.blockchain_service import BlockchainService

# Create a service instance with a non-existent offline RPC URL
offline_service = BlockchainService()
offline_service.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9999"))

doc_hash = "2ae5de886ad358c7e55d9dcd12e09cada74114f7689bc5e8399ba73f59b49713"

res = offline_service.verify_document(doc_hash)
print("--- BLOCKCHAIN OFFLINE FAILURE VERIFICATION ---")
print("RPC Connected:", offline_service.is_connected())
print("Returned Status:", res["status"])
print("Verified Value:", res["verified"])
print("Status is BLOCKCHAIN_UNAVAILABLE:", res["status"] == "BLOCKCHAIN_UNAVAILABLE")
print("Verified is False:", res["verified"] is False)
