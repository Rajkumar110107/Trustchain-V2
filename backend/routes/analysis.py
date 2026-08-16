import os
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks

from backend.config import settings
from backend.services.hashing_service import hashing_service
from backend.services.ela_service import ela_service
from backend.services.ocr_service import ocr_service
from backend.services.ai_service import ai_service
from backend.services.hybrid_engine import hybrid_engine
from backend.services.blockchain_service import blockchain_service
from backend.services.db_service import db_service
from backend.schemas.analysis import AnalysisResponse

router = APIRouter(tags=["Analysis"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def validate_file_metadata(file: UploadFile):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

def cleanup_file_path(file_path: str):
    """Background task to remove temporary uploads after processing."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"[WARN] Cleanup error for {file_path}:", e)

@router.post("/analyze", response_model=AnalysisResponse)
@router.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    lang: str = Form("multi")
):
    validate_file_metadata(file)

    # Read raw uploaded file bytes
    try:
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB"
            )
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty (0 bytes)")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file stream: {str(e)}")

    # Save uploaded file to disk for processing
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write upload file: {str(e)}")

    # Schedule background cleanup for uploaded file
    background_tasks.add_task(cleanup_file_path, file_path)

    # 1. SHA-256 Fingerprint calculation on raw original bytes
    doc_hash = hashing_service.generate_sha256(contents)

    # 2. ELA Image Generation & Variance Scoring
    ela_res = ela_service.generate_ela(file_path)

    # 3. OCR Text & Metadata Extraction
    ocr_res = ocr_service.extract_text(file_path, lang_code=lang)

    # 4. PyTorch ResNet-18 Model Inference
    ai_res = ai_service.predict(file_path)

    # 5. Hybrid Authenticity Assessment Engine
    eval_res = hybrid_engine.evaluate(
        ml_result=ai_res,
        ela_result=ela_res,
        ocr_result=ocr_res
    )

    # 6. Blockchain Verification & Auto-Registration
    bc_verify = blockchain_service.verify_document(doc_hash)

    blockchain_status = bc_verify["status"]
    blockchain_verified = bc_verify["verified"]
    tx_hash = None

    if blockchain_status == "NOT_REGISTERED" and eval_res["classification"] in ["AUTHENTIC", "SUSPICIOUS"]:
        reg_res = blockchain_service.register_document(doc_hash)
        if reg_res.get("success"):
            blockchain_status = "STORED"
            blockchain_verified = True
            tx_hash = reg_res.get("tx_hash")

    ela_url = f"http://{settings.HOST}:{settings.PORT}/ela_outputs/{ela_res['filename']}" if ela_res.get("filename") else None

    # Persist off-chain application metadata in database
    db_service.save_analysis(
        doc_hash=doc_hash,
        filename=file.filename,
        classification=eval_res["classification"],
        score=eval_res["authenticity_score"],
        ai_pred=eval_res["ai"]["prediction"],
        ela_var=ela_res.get("variance", 0.0),
        ocr_count=ocr_res.get("character_count", 0),
        bc_status=blockchain_status,
        tx_hash=tx_hash
    )

    return {
        "document_hash": doc_hash,
        "hash": doc_hash,
        "result": eval_res["ai"]["prediction"],
        "classification": eval_res["classification"],
        "confidence": eval_res["confidence_percentage"],
        "authenticity_score": eval_res["authenticity_score"],
        "final_confidence": eval_res["final_confidence"],
        "analysis_note": eval_res["recommendation"],
        "explanations": eval_res["evidence"],
        "evidence": eval_res["evidence"],
        "ai": eval_res["ai"],
        "ela": eval_res["ela"],
        "ocr": eval_res["ocr"],
        "ela_image": ela_url,
        "ela_variance": ela_res.get("variance", 0.0),
        "extracted_text": ocr_res.get("text", ""),
        "ocr_character_count": ocr_res.get("character_count", 0),
        "disclaimer": eval_res.get("disclaimer"),
        "blockchain_status": blockchain_status,
        "blockchain_verified": blockchain_verified,
        "transaction_hash": tx_hash,
        "contract_address": blockchain_service.contract_address,
        "registrant": bc_verify.get("registrant"),
        "timestamp": bc_verify.get("timestamp")
    }
