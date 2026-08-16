import os
import pytesseract
from PIL import Image
import numpy as np
from backend.config import settings

# Configure Tesseract Binary Path
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

LANG_MAP = {
    "eng": "eng",
    "tam": "tam",
    "hin": "hin",
    "mal": "mal",
    "tel": "tel",
    "multi": "eng+tam+hin+mal+tel"
}

class OCRService:
    @staticmethod
    def extract_text(image_path: str, lang_code: str = "multi") -> dict:
        """
        Extracts text, language confidence, character count, and text density metrics using Tesseract OCR.
        """
        try:
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "text": "",
                    "character_count": 0,
                    "word_count": 0,
                    "confidence": 0.0,
                    "text_density": 0.0,
                    "language": lang_code,
                    "error": "Image file not found"
                }

            img = Image.open(image_path).convert("RGB")
            width, height = img.size
            total_pixels = width * height

            selected_lang = LANG_MAP.get(lang_code.lower(), "eng")

            # Perform OCR Text Extraction
            text = pytesseract.image_to_string(
                img,
                lang=selected_lang,
                config="--oem 3 --psm 6"
            ).strip()

            words = text.split()
            char_count = len(text)
            text_density = round(char_count / total_pixels, 6) if total_pixels > 0 else 0.0

            # Calculate Average OCR Confidence using image_to_data
            avg_confidence = 0.0
            try:
                data = pytesseract.image_to_data(img, lang=selected_lang, output_type=pytesseract.Output.DICT)
                confidences = [float(c) for c in data.get("conf", []) if isinstance(c, (int, float, str)) and str(c).replace('.', '', 1).isdigit() and float(c) > 0]
                if confidences:
                    avg_confidence = round(float(np.mean(confidences)) / 100.0, 4)
                else:
                    avg_confidence = 0.8 if char_count > 20 else 0.4
            except Exception as e:
                print("[WARN] OCR Confidence Data Exception:", e)
                avg_confidence = 0.7 if char_count > 20 else 0.3

            return {
                "success": True,
                "text": text,
                "character_count": char_count,
                "word_count": len(words),
                "confidence": avg_confidence,
                "text_density": text_density,
                "language": selected_lang,
                "error": None
            }
        except Exception as e:
            print("[WARN] OCR Extraction Exception:", e)
            return {
                "success": False,
                "text": "",
                "character_count": 0,
                "word_count": 0,
                "confidence": 0.0,
                "text_density": 0.0,
                "language": lang_code,
                "error": str(e)
            }

ocr_service = OCRService()
