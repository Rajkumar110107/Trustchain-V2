import os
import json
from web3 import Web3
from eth_account import Account
from backend.config import settings
from backend.services.hashing_service import hashing_service

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))
        self.contract_address = settings.CONTRACT_ADDRESS
        self.contract = None
        self._load_contract()

    def _load_contract(self):
        try:
            abi_path = settings.BASE_DIR / "backend" / "abi" / "DocumentRegistry.json"
            if os.path.exists(abi_path):
                with open(abi_path, "r") as f:
                    data = json.load(f)
                    abi = data.get("abi", [])
                    if data.get("address"):
                        self.contract_address = data.get("address")
            else:
                # Basic ABI fallback
                abi = [
                    {
                        "inputs": [{"name": "docHash", "type": "bytes32"}],
                        "name": "registerDocument",
                        "outputs": [],
                        "type": "function"
                    },
                    {
                        "inputs": [{"name": "docHash", "type": "bytes32"}],
                        "name": "verifyDocument",
                        "outputs": [
                            {"name": "isRegistered", "type": "bool"},
                            {"name": "registrant", "type": "address"},
                            {"name": "timestamp", "type": "uint256"}
                        ],
                        "type": "function"
                    }
                ]

            if self.contract_address and Web3.is_address(self.contract_address):
                checksum_addr = Web3.to_checksum_address(self.contract_address)
                self.contract = self.w3.eth.contract(address=checksum_addr, abi=abi)
        except Exception as e:
            print("[WARN] Failed to load blockchain contract:", e)
            self.contract = None

    def is_connected(self) -> bool:
        try:
            return self.w3.is_connected()
        except Exception:
            return False

    def get_account(self):
        """
        Gets wallet address. Prefers signing from PRIVATE_KEY if available in settings,
        falling back to local unlocked node account.
        """
        try:
            if not self.is_connected():
                return None
            
            if settings.PRIVATE_KEY and settings.PRIVATE_KEY.strip():
                acc = Account.from_key(settings.PRIVATE_KEY)
                return acc.address
            
            accounts = self.w3.eth.accounts
            return accounts[0] if accounts else None
        except Exception as e:
            print("[WARN] Error getting wallet account:", e)
            return None

    def verify_document(self, hex_hash: str) -> dict:
        """
        Queries smart contract for registration status of a 64-char SHA-256 hash.
        """
        if len(hex_hash) != 64:
            return {
                "status": "INVALID_HASH",
                "verified": False,
                "registrant": None,
                "timestamp": None,
                "contract_address": self.contract_address,
                "message": "Invalid hash length; SHA-256 digest must be 64 hex characters"
            }

        if not self.is_connected():
            return {
                "status": "BLOCKCHAIN_UNAVAILABLE",
                "verified": False,
                "registrant": None,
                "timestamp": None,
                "contract_address": self.contract_address,
                "message": f"Blockchain RPC node ({settings.RPC_URL}) is offline or unreachable"
            }

        if not self.contract:
            return {
                "status": "CONTRACT_ERROR",
                "verified": False,
                "registrant": None,
                "timestamp": None,
                "contract_address": self.contract_address,
                "message": "Smart contract ABI or address not initialized"
            }

        try:
            bytes32_hash = hashing_service.to_bytes32(hex_hash)
            result = self.contract.functions.verifyDocument(bytes32_hash).call()

            if isinstance(result, (list, tuple)):
                is_registered = result[0]
                registrant = result[1] if len(result) > 1 and result[1] != "0x0000000000000000000000000000000000000000" else None
                timestamp = int(result[2]) if len(result) > 2 and int(result[2]) > 0 else None
            else:
                is_registered = bool(result)
                registrant = None
                timestamp = None

            if is_registered:
                return {
                    "status": "VERIFIED",
                    "verified": True,
                    "registrant": registrant,
                    "timestamp": timestamp,
                    "contract_address": self.contract_address,
                    "message": "Document cryptographic fingerprint is registered and verified on-chain"
                }
            else:
                return {
                    "status": "NOT_REGISTERED",
                    "verified": False,
                    "registrant": None,
                    "timestamp": None,
                    "contract_address": self.contract_address,
                    "message": "Document cryptographic fingerprint not found on-chain"
                }
        except Exception as e:
            print("[ERROR] Verify Document Exception:", e)
            return {
                "status": "TRANSACTION_FAILED",
                "verified": False,
                "registrant": None,
                "timestamp": None,
                "contract_address": self.contract_address,
                "message": f"Blockchain query failed: {str(e)}"
            }

    def register_document(self, hex_hash: str) -> dict:
        """
        Registers a 64-char SHA-256 hash on the smart contract.
        Handles signing either via local node account or private key.
        """
        if len(hex_hash) != 64:
            return {
                "status": "INVALID_HASH",
                "success": False,
                "tx_hash": None,
                "message": "Invalid SHA-256 hash length"
            }

        if not self.is_connected():
            return {
                "status": "BLOCKCHAIN_UNAVAILABLE",
                "success": False,
                "tx_hash": None,
                "message": "RPC node is offline"
            }

        try:
            bytes32_hash = hashing_service.to_bytes32(hex_hash)

            if settings.PRIVATE_KEY and settings.PRIVATE_KEY.strip():
                # Private Key signing flow
                account = Account.from_key(settings.PRIVATE_KEY)
                nonce = self.w3.eth.get_transaction_count(account.address)
                tx_data = self.contract.functions.registerDocument(bytes32_hash).build_transaction({
                    "from": account.address,
                    "nonce": nonce,
                    "gasPrice": self.w3.eth.gas_price,
                    "chainId": settings.CHAIN_ID
                })
                signed_tx = self.w3.eth.account.sign_transaction(tx_data, private_key=settings.PRIVATE_KEY)
                tx_hash_bytes = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash_bytes)
            else:
                # Local node default unlocked account flow
                account_addr = self.get_account()
                if not account_addr:
                    return {
                        "status": "TRANSACTION_FAILED",
                        "success": False,
                        "tx_hash": None,
                        "message": "No unlocked Ethereum account available"
                    }
                tx_hash_bytes = self.contract.functions.registerDocument(bytes32_hash).transact({"from": account_addr})
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash_bytes)

            tx_hash_hex = receipt.transactionHash.hex()

            return {
                "status": "STORED",
                "success": True,
                "tx_hash": tx_hash_hex,
                "block_number": receipt.blockNumber,
                "message": "Document hash successfully registered on blockchain"
            }
        except Exception as e:
            print("[ERROR] Register Document Exception:", e)
            return {
                "status": "TRANSACTION_FAILED",
                "success": False,
                "tx_hash": None,
                "message": f"Transaction execution failed: {str(e)}"
            }

blockchain_service = BlockchainService()
