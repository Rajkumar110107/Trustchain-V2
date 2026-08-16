import hashlib

class HashingService:
    @staticmethod
    def generate_sha256(file_bytes: bytes) -> str:
        """
        Computes SHA-256 hexadecimal hash string from raw document bytes.
        Only raw original uploaded file bytes should be passed to maintain determinism.
        """
        return hashlib.sha256(file_bytes).hexdigest()

    @staticmethod
    def to_bytes32(hex_hash: str) -> bytes:
        """
        Converts 64-character SHA-256 hex string into 32-byte binary representation required by Solidity bytes32 parameters.
        """
        clean_hex = hex_hash[2:] if hex_hash.startswith("0x") else hex_hash
        if len(clean_hex) != 64:
            raise ValueError("Invalid hash length: SHA-256 hash must be exactly 64 hexadecimal characters.")
        return bytes.fromhex(clean_hex)

hashing_service = HashingService()
