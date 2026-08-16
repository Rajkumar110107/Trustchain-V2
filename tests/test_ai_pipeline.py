import unittest
import os
import tempfile
from PIL import Image

from backend.services.hashing_service import hashing_service
from backend.services.ai_service import ai_service
from backend.services.ela_service import ela_service
from backend.services.ocr_service import ocr_service
from backend.services.hybrid_engine import hybrid_engine
from backend.services.blockchain_service import blockchain_service
from backend.services.db_service import db_service

class TestAIPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_img_path = os.path.join(self.temp_dir, "test_doc.jpg")
        img = Image.new("RGB", (300, 300), color=(255, 255, 255))
        img.save(self.test_img_path, "JPEG")
        
        with open(self.test_img_path, "rb") as f:
            self.test_bytes = f.read()

    def tearDown(self):
        if os.path.exists(self.test_img_path):
            os.remove(self.test_img_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_hashing_determinism_and_tampering(self):
        # 1. Original file hash
        hash1 = hashing_service.generate_sha256(self.test_bytes)
        hash2 = hashing_service.generate_sha256(self.test_bytes)
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

        bytes32_val = hashing_service.to_bytes32(hash1)
        self.assertEqual(len(bytes32_val), 32)

        # 2. Tampered file hash (even 1 byte modification MUST yield different hash)
        tampered_bytes = self.test_bytes + b"TAMPERED_BYTE_0x123"
        hash3 = hashing_service.generate_sha256(tampered_bytes)
        self.assertNotEqual(hash1, hash3)

    def test_image_validation(self):
        valid, msg = ai_service.validate_image(self.test_img_path)
        self.assertTrue(valid)
        self.assertEqual(msg, "Valid")

        valid_fake, msg_fake = ai_service.validate_image("non_existent_file.jpg")
        self.assertFalse(valid_fake)

    def test_ela_service(self):
        ela_res = ela_service.generate_ela(self.test_img_path)
        self.assertTrue(ela_res["success"])
        self.assertIn("score", ela_res)
        self.assertGreaterEqual(ela_res["score"], 0.0)
        self.assertLessEqual(ela_res["score"], 1.0)
        self.assertIn("variance", ela_res)

        if ela_res.get("ela_path") and os.path.exists(ela_res["ela_path"]):
            os.remove(ela_res["ela_path"])

    def test_ocr_service(self):
        ocr_res = ocr_service.extract_text(self.test_img_path, lang_code="eng")
        self.assertTrue(ocr_res["success"])
        self.assertIn("text", ocr_res)
        self.assertIn("confidence", ocr_res)

    def test_ai_service_predict(self):
        ai_res = ai_service.predict(self.test_img_path)
        self.assertTrue(ai_res["success"])
        self.assertIn(ai_res["label"], ["REAL", "FAKE"])

    def test_hybrid_engine_eval(self):
        ml_mock = {"success": True, "label": "REAL", "score": 0.95, "confidence": 95.0, "error": None}
        ela_mock = {"success": True, "score": 0.85, "variance": 350.0, "suspicious_pixel_ratio": 0.01, "error": None}
        ocr_mock = {"success": True, "text": "Official Valid Document Text", "character_count": 80, "confidence": 0.92, "error": None}

        eval_res = hybrid_engine.evaluate(ml_mock, ela_mock, ocr_mock)
        self.assertEqual(eval_res["classification"], "AUTHENTIC")
        self.assertGreaterEqual(eval_res["final_confidence"], 0.80)

    def test_db_service_persistence(self):
        doc_hash = "1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff"
        db_service.save_analysis(
            doc_hash=doc_hash,
            filename="test.jpg",
            classification="AUTHENTIC",
            score=95.0,
            ai_pred="REAL",
            ela_var=300.0,
            ocr_count=50,
            bc_status="VERIFIED",
            tx_hash="0x1234567890abcdef"
        )

        record = db_service.get_analysis(doc_hash)
        self.assertIsNotNone(record)
        self.assertEqual(record["classification"], "AUTHENTIC")
        self.assertEqual(record["blockchain_status"], "VERIFIED")

    def test_blockchain_service_offline_graceful_handling(self):
        doc_hash = "222233334444555566667777888899990000aaaabbbbccccddddeeeeffff1111"
        res = blockchain_service.verify_document(doc_hash)
        self.assertIn("status", res)
        self.assertIn(res["status"], ["VERIFIED", "NOT_REGISTERED", "BLOCKCHAIN_UNAVAILABLE"])

if __name__ == "__main__":
    unittest.main()
