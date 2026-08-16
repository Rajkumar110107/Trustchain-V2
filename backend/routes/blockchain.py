from fastapi import APIRouter, HTTPException
from backend.schemas.blockchain import RegisterRequest, VerifyRequest, BlockchainRegisterResponse, BlockchainVerifyResponse
from backend.services.blockchain_service import blockchain_service

router = APIRouter(prefix="/api", tags=["Blockchain"])

@router.post("/register", response_model=BlockchainRegisterResponse)
async def register_document(req: RegisterRequest):
    if len(req.hash) != 64:
        raise HTTPException(status_code=400, detail="Invalid SHA-256 hash length. Must be 64 hexadecimal characters.")
    
    result = blockchain_service.register_document(req.hash)
    return result

@router.post("/verify", response_model=BlockchainVerifyResponse)
async def verify_document(req: VerifyRequest):
    if len(req.hash) != 64:
        raise HTTPException(status_code=400, detail="Invalid SHA-256 hash length. Must be 64 hexadecimal characters.")
    
    result = blockchain_service.verify_document(req.hash)
    return result

@router.get("/document/{hash}", response_model=BlockchainVerifyResponse)
async def get_document_record(hash: str):
    if len(hash) != 64:
        raise HTTPException(status_code=400, detail="Invalid SHA-256 hash length. Must be 64 hexadecimal characters.")
    
    result = blockchain_service.verify_document(hash)
    return result
