class HybridConfidenceEngine:
    @staticmethod
    def evaluate(ml_result: dict, ela_result: dict, ocr_result: dict) -> dict:
        """
        Combines AI ResNet-18 evidence, ELA forensic score, and OCR textual evidence 
        into a weighted, explainable authenticity assessment and classification.
        """
        evidence_statements = []

        # 1. AI Evidence Score (0.0 to 1.0)
        ai_success = ml_result.get("success", True) and ml_result.get("error") is None
        ai_score = ml_result.get("score", 0.5)
        ai_label = ml_result.get("label", "UNKNOWN")
        ai_conf = ml_result.get("confidence", 50.0)

        if ai_success:
            evidence_statements.append(f"ResNet-18 model predicted {ai_label} with {ai_conf:.1f}% confidence.")
        else:
            evidence_statements.append(f"ResNet-18 model prediction unavailable: {ml_result.get('error')}")

        # 2. ELA Evidence Score (0.0 to 1.0)
        ela_success = ela_result.get("success", False) and ela_result.get("error") is None
        ela_score = ela_result.get("score", 0.5)
        ela_variance = ela_result.get("variance", 0.0)

        if ela_success:
            if ela_variance < 600.0:
                evidence_statements.append(f"ELA variance is low ({ela_variance:.1f}), indicating high JPEG compression uniformity.")
            elif ela_variance > 1800.0:
                evidence_statements.append(f"ELA variance is elevated ({ela_variance:.1f}), highlighting potential compression anomalies.")
            else:
                evidence_statements.append(f"ELA variance is moderate ({ela_variance:.1f}).")
        else:
            evidence_statements.append(f"ELA analysis unavailable: {ela_result.get('error')}")

        # 3. OCR Evidence Score (0.0 to 1.0)
        ocr_success = ocr_result.get("success", False) and ocr_result.get("error") is None
        ocr_char_count = ocr_result.get("character_count", 0)
        ocr_confidence = ocr_result.get("confidence", 0.0)

        if ocr_success:
            # Score based on OCR readability & character count
            if ocr_char_count > 40:
                ocr_score = min(1.0, 0.7 + ocr_confidence * 0.3)
                evidence_statements.append(f"OCR successfully extracted structured text ({ocr_char_count} chars, {ocr_confidence*100:.0f}% confidence).")
            elif ocr_char_count > 10:
                ocr_score = 0.6
                evidence_statements.append(f"OCR extracted moderate text content ({ocr_char_count} chars).")
            else:
                ocr_score = 0.4
                evidence_statements.append("OCR detected minimal text content.")
        else:
            ocr_score = 0.5
            evidence_statements.append(f"OCR text extraction unavailable: {ocr_result.get('error')}")

        # Dynamic Weight Re-normalization
        weights = {"ai": 0.50, "ela": 0.35, "ocr": 0.15}
        active_weights_sum = 0.0
        weighted_score_sum = 0.0

        if ai_success:
            active_weights_sum += weights["ai"]
            weighted_score_sum += weights["ai"] * ai_score
        if ela_success:
            active_weights_sum += weights["ela"]
            weighted_score_sum += weights["ela"] * ela_score
        if ocr_success:
            active_weights_sum += weights["ocr"]
            weighted_score_sum += weights["ocr"] * ocr_score

        if active_weights_sum > 0:
            final_hybrid_score = weighted_score_sum / active_weights_sum
        else:
            final_hybrid_score = 0.5

        final_hybrid_score = round(max(0.0, min(1.0, final_hybrid_score)), 4)
        score_pct = round(final_hybrid_score * 100.0, 2)

        # Classification Threshold Logic
        if not ai_success and not ela_success:
            classification = "INCONCLUSIVE"
            recommendation = "Insufficient forensic signals available to verify document."
        elif final_hybrid_score >= 0.80:
            classification = "AUTHENTIC"
            recommendation = "Document exhibits high integrity across visual, compression, and textual forensic signals."
        elif final_hybrid_score >= 0.55:
            classification = "SUSPICIOUS"
            recommendation = "Minor forensic anomalies or compression inconsistencies detected. Manual review recommended."
        else:
            classification = "LIKELY_FORGED"
            recommendation = "Multiple forgery indicators detected (compression mismatch or AI model forgery prediction)."

        return {
            "classification": classification,
            "final_confidence": final_hybrid_score,
            "authenticity_score": score_pct,
            "confidence_percentage": f"{score_pct:.2f}%",
            "ai_evidence_score": ai_score,
            "ela_evidence_score": ela_score,
            "ocr_evidence_score": ocr_score,
            "ai": {
                "success": ai_success,
                "prediction": ai_label,
                "confidence": ai_conf,
                "score": ai_score
            },
            "ela": {
                "success": ela_success,
                "score": ela_score,
                "variance": ela_variance,
                "suspicious_pixel_ratio": ela_result.get("suspicious_pixel_ratio", 0.0),
                "filename": ela_result.get("filename")
            },
            "ocr": {
                "success": ocr_success,
                "text": ocr_result.get("text", ""),
                "language": ocr_result.get("language", "multi"),
                "confidence": ocr_confidence,
                "character_count": ocr_char_count,
                "word_count": ocr_result.get("word_count", 0)
            },
            "evidence": evidence_statements,
            "recommendation": recommendation,
            "disclaimer": "This is an automated AI-assisted forensic assessment, not a legally binding guarantee of authenticity."
        }

hybrid_engine = HybridConfidenceEngine()
