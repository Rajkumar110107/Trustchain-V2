# 🔌 TrustChain OpenAPI & Endpoint Documentation

## Base URL
`http://127.0.0.1:8000`

---

## Endpoints

### 1. `POST /api/analyze` (or `/analyze`)
Uploads document for multi-forensic analysis & auto-registration.

* **Content-Type**: `multipart/form-data`
* **Form Fields**:
  - `file`: Document file (`.jpg`, `.jpeg`, `.png`, `.webp`, max 10MB)
  - `lang`: Language code (`eng`, `tam`, `hin`, `mal`, `tel`, `multi`)

* **Response Schema (200 OK)**:
```json
{
  "document_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "result": "REAL",
  "classification": "AUTHENTIC",
  "confidence": "94.50%",
  "authenticity_score": 94.5,
  "analysis_note": "Document exhibits high integrity across visual, compression, and textual forensic signals.",
  "explanations": [
    "ResNet-18 model prediction: REAL with 95.0% confidence.",
    "ELA variance is low (420.5), indicating uniform JPEG compression.",
    "Extracted readable text structure (120 characters)."
  ],
  "ela_image": "http://127.0.0.1:8000/ela_outputs/ela_sample.jpg",
  "ela_variance": 420.5,
  "extracted_text": "SAMPLE DOCUMENT TEXT...",
  "ocr_character_count": 120,
  "blockchain_status": "VERIFIED",
  "blockchain_verified": true,
  "transaction_hash": "0x123...abc",
  "contract_address": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
  "registrant": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
  "timestamp": 1776345000
}
```

---

### 2. `POST /api/register`
Registers a 64-char SHA-256 document hash directly on-chain.

* **Content-Type**: `application/json`
* **Request Body**:
```json
{
  "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

---

### 3. `POST /api/verify`
Queries smart contract registration for a 64-char SHA-256 hash.

* **Content-Type**: `application/json`
* **Request Body**:
```json
{
  "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

---

### 4. `GET /health`
Returns backend service health status & connected subsystems.
