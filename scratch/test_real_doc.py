import sys
sys.path.insert(0, ".")

from backend.services.ai_service import ai_service
from backend.services.ela_service import ela_service
from backend.services.ocr_service import ocr_service
from backend.services.hybrid_engine import hybrid_engine

ai = ai_service.predict("temp.jpg")
ela = ela_service.generate_ela("temp.jpg")
ocr = ocr_service.extract_text("temp.jpg", "multi")
ev = hybrid_engine.evaluate(ai, ela, ocr)

print("--- REAL DOCUMENT TEST RESULTS ---")
print("filename: temp.jpg")
print("expected class: REAL (Receipt Document)")
print("ResNet prediction:", ai.get("label", ai.get("prediction")))
print("AI confidence:", f"{ai.get('confidence', 0.0):.2f}%")
print("ELA score:", ela.get("score"))
print("OCR status:", "Success" if ocr.get("success") else "Failed")
print("OCR confidence:", f"{ocr.get('confidence', 0.0)*100:.2f}%")
print("hybrid confidence:", f"{ev.get('final_confidence', 0.0)*100:.2f}%")
print("final classification:", ev.get("classification"))
