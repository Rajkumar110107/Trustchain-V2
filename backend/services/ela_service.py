import os
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
from backend.config import settings

class ELAService:
    @staticmethod
    def generate_ela(image_path: str, quality: int = 90) -> dict:
        """
        Generates Error Level Analysis (ELA) heatmap image and calculates a normalized ELA score (0.0 to 1.0).
        Lower variance -> higher visual uniformity (score closer to 1.0).
        Higher variance -> localized compression anomalies (score closer to 0.0).
        """
        try:
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "score": 0.5,
                    "variance": 0.0,
                    "suspicious_pixel_ratio": 0.0,
                    "filename": None,
                    "ela_path": None,
                    "error": "Image file not found"
                }

            original = Image.open(image_path).convert("RGB")
            
            filename = "ela_" + os.path.basename(image_path)
            temp_path = os.path.join(settings.ELA_DIR, f"temp_{os.path.basename(image_path)}")
            ela_save_path = os.path.join(settings.ELA_DIR, filename)

            # Re-compress at specified JPEG quality (default 90%)
            original.save(temp_path, "JPEG", quality=quality)
            compressed = Image.open(temp_path)

            # Compute pixel-wise absolute difference
            diff = ImageChops.difference(original, compressed)

            extrema = diff.getextrema()
            max_diff = max([ex[1] for ex in extrema])

            scale = 255.0 / max_diff if max_diff != 0 else 1.0
            diff_enhanced = ImageEnhance.Brightness(diff).enhance(scale)
            diff_enhanced.save(ela_save_path)

            # Clean up temporary compressed file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            # Grayscale conversion & NumPy array variance
            gray_diff = diff_enhanced.convert("L")
            arr = np.array(gray_diff, dtype=np.float32)
            variance = float(np.var(arr))

            # Suspicious high-intensity pixel ratio (threshold > 128 in scaled difference)
            suspicious_pixels = np.count_nonzero(arr > 128.0)
            total_pixels = arr.size
            suspicious_ratio = float(suspicious_pixels / total_pixels) if total_pixels > 0 else 0.0

            # Bounded normalized ELA score (0.0 = high anomaly, 1.0 = uniform)
            # Empirical baseline: variance below 500 is pristine; variance above 2500 is highly anomalous.
            raw_anomaly_ratio = min(1.0, max(0.0, variance / 2500.0))
            normalized_score = round(1.0 - raw_anomaly_ratio, 4)

            return {
                "success": True,
                "score": normalized_score,
                "variance": round(variance, 2),
                "suspicious_pixel_ratio": round(suspicious_ratio, 4),
                "filename": filename,
                "ela_path": ela_save_path,
                "error": None
            }
        except Exception as e:
            print("[WARN] ELA Generation Exception:", e)
            return {
                "success": False,
                "score": 0.5,
                "variance": 0.0,
                "suspicious_pixel_ratio": 0.0,
                "filename": None,
                "ela_path": None,
                "error": str(e)
            }

ela_service = ELAService()
