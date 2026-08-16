import sys
import os
import json
sys.path.insert(0, ".")

from backend.services.ai_service import ai_service
from backend.services.ela_service import ela_service
from backend.services.ocr_service import ocr_service
from backend.services.hybrid_engine import hybrid_engine

test_docs = [
    {"path": "temp.jpg", "expected": "AUTHENTIC"},
    {"path": "dataset/real/X00016469622.png", "expected": "AUTHENTIC"},
    {"path": "dataset/real/X00016469623.png", "expected": "AUTHENTIC"},
    {"path": "dataset/real/X51005200938.png", "expected": "AUTHENTIC"},
    {"path": "dataset/real/X51005230617.png", "expected": "AUTHENTIC"},
    {"path": "dataset/fake/X00016469622.png", "expected": "FORGED"},
    {"path": "dataset/fake/X00016469623.png", "expected": "FORGED"},
    {"path": "dataset/fake/X51005200938.png", "expected": "FORGED"},
    {"path": "dataset/fake/X51005230617.png", "expected": "FORGED"},
    {"path": "dataset/fake/X51005268200.png", "expected": "FORGED"},
]

results = []

for doc in test_docs:
    path = doc["path"]
    expected = doc["expected"]
    filename = os.path.basename(path)

    if not os.path.exists(path):
        print(f"[WARN] File not found: {path}")
        continue

    ai = ai_service.predict(path)
    ela = ela_service.generate_ela(path)
    ocr = ocr_service.extract_text(path, "multi")
    ev = hybrid_engine.evaluate(ai, ela, ocr)

    # Compute text density
    text_len = ocr.get("character_count", 0)
    # Estimate density based on character count
    ocr_density = round(text_len / 1000.0, 4)

    record = {
        "filename": filename,
        "path": path,
        "expected": expected,
        "ai_prediction": ai.get("label", "UNKNOWN"),
        "ai_confidence": ai.get("confidence", 0.0),
        "ela_score": ela.get("score", 0.0),
        "ela_variance": ela.get("variance", 0.0),
        "ela_suspicious_ratio": ela.get("suspicious_pixel_ratio", 0.0),
        "ocr_success": ocr.get("success", False),
        "ocr_confidence": round(ocr.get("confidence", 0.0) * 100.0, 2),
        "ocr_text_density": ocr_density,
        "hybrid_confidence": round(ev.get("final_confidence", 0.0) * 100.0, 2),
        "final_classification": ev.get("classification")
    }
    results.append(record)

print(json.dumps(results, indent=2))

with open("scratch/10_docs_eval.json", "w") as f:
    json.dump(results, f, indent=2)
