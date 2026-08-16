import sys
import os
import json
import hashlib
from PIL import Image

sys.path.insert(0, ".")

from backend.services.ai_service import ai_service
from backend.services.ela_service import ela_service
from backend.services.ocr_service import ocr_service
from backend.services.hybrid_engine import hybrid_engine

test_docs = [
    ("tests/test_documents/authentic/authentic_01.png", "AUTHENTIC"),
    ("tests/test_documents/authentic/authentic_02.png", "AUTHENTIC"),
    ("tests/test_documents/authentic/authentic_03.png", "AUTHENTIC"),
    ("tests/test_documents/authentic/authentic_04.png", "AUTHENTIC"),
    ("tests/test_documents/authentic/authentic_05.png", "AUTHENTIC"),
    ("tests/test_documents/forged/forged_01.png", "FORGED"),
    ("tests/test_documents/forged/forged_02.png", "FORGED"),
    ("tests/test_documents/forged/forged_03.png", "FORGED"),
    ("tests/test_documents/forged/forged_04.png", "FORGED"),
    ("tests/test_documents/forged/forged_05.png", "FORGED"),
]

results = []

print("--- EVALUATING CORRECTED 10-DOCUMENT DATASET BASELINE ---")

for path, expected in test_docs:
    filename = os.path.basename(path)
    
    with open(path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
        size = os.path.getsize(path)

    with Image.open(path) as img:
        dims = f"{img.width}x{img.height}"

    ai = ai_service.predict(path)
    ela = ela_service.generate_ela(path)
    ocr = ocr_service.extract_text(path, "multi")
    ev = hybrid_engine.evaluate(ai, ela, ocr)

    record = {
        "filename": filename,
        "path": path,
        "expected": expected,
        "sha256": sha,
        "size": size,
        "dimensions": dims,
        "ai_prediction": ai.get("label", "UNKNOWN"),
        "ai_confidence": ai.get("confidence", 0.0),
        "ela_score": ela.get("score", 0.0),
        "ela_variance": ela.get("variance", 0.0),
        "ocr_success": ocr.get("success", False),
        "ocr_confidence": round(ocr.get("confidence", 0.0) * 100.0, 2),
        "hybrid_confidence": round(ev.get("final_confidence", 0.0) * 100.0, 2),
        "final_classification": ev.get("classification")
    }
    results.append(record)

print(json.dumps(results, indent=2))

with open("scratch/corrected_10_docs_eval.json", "w") as f:
    json.dump(results, f, indent=2)
