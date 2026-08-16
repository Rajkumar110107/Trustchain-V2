from typing import Optional
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    hash: str = Field(..., min_length=64, max_length=64, description="64-character SHA-256 hexadecimal hash")

class VerifyRequest(BaseModel):
    hash: str = Field(..., min_length=64, max_length=64, description="64-character SHA-256 hexadecimal hash")

class BlockchainRegisterResponse(BaseModel):
    status: str
    success: bool
    tx_hash: Optional[str] = None
    block_number: Optional[int] = None
    message: str

class BlockchainVerifyResponse(BaseModel):
    status: str
    verified: bool
    registrant: Optional[str] = None
    timestamp: Optional[int] = None
    contract_address: Optional[str] = None
    message: str
