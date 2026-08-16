import sys
sys.path.insert(0, ".")

from backend.services.blockchain_service import blockchain_service

doc_hash_A = "2ae5de886ad358c7e55d9dcd12e09cada74114f7689bc5e8399ba73f59b49713"
doc_hash_B = "36c9c052d17371def956e21a52acf5a0456507e6d6cad743c08dfc43d0774118"

print("--- LOCAL BLOCKCHAIN CONTRACT VERIFICATION ---")
print("Connected to RPC:", blockchain_service.is_connected())

if blockchain_service.is_connected():
    # 1. Verify before registration
    verify_pre = blockchain_service.verify_document(doc_hash_A)
    print("Pre-Registration Status:", verify_pre["status"])

    # 2. Register document hash A
    reg_res = blockchain_service.register_document(doc_hash_A)
    print("Registration Result:", reg_res)

    # 3. Verify after registration
    verify_post = blockchain_service.verify_document(doc_hash_A)
    print("Post-Registration Status:", verify_post["status"])
    print("Verified On-Chain:", verify_post["verified"])

    # 4. Duplicate registration attempt
    dup_res = blockchain_service.register_document(doc_hash_A)
    print("Duplicate Registration Status:", dup_res["status"], "(Expected: TRANSACTION_FAILED)")

    # 5. Verify tampered hash B
    verify_B = blockchain_service.verify_document(doc_hash_B)
    print("Tampered Hash B Status:", verify_B["status"])
    print("Tampered Hash B Verified:", verify_B["verified"])
else:
    print("Local RPC node is offline.")
