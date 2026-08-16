from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class AIResult(BaseModel):
    success: bool
    prediction: str
    confidence: float
    score: float

class ELAResult(BaseModel):
    success: bool
    score: float
    variance: float
    suspicious_pixel_ratio: float
    filename: Optional[str] = None

class OCRResult(BaseModel):
    success: bool
    text: str
    language: str
    confidence: float
    character_count: int
    word_count: int

class AnalysisResponse(BaseModel):
    document_hash: str
    hash: str
    result: str
    classification: str
    confidence: str
    authenticity_score: float
    final_confidence: float
    analysis_note: str
    explanations: List[str]
    evidence: List[str]
    ai: AIResult
    ela: ELAResult
    ocr: OCRResult
    ela_image: Optional[str] = None
    ela_variance: float
    extracted_text: str
    ocr_character_count: int
    disclaimer: Optional[str] = None
    blockchain_status: str
    blockchain_verified: bool
    transaction_hash: Optional[str] = None
    contract_address: Optional[str] = None
    registrant: Optional[str] = None
    timestamp: Optional[int] = None
