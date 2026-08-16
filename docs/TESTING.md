# 🧪 TrustChain Testing Suite

## 1. Smart Contract Unit Tests

```bash
cd blockchain
npm test
```
Verifies contract compilation, event emissions, duplicate registration prevention, zero hash rejection, and timestamp storage.

## 2. Backend Service & AI Model Test

```bash
python -c "import backend.main; print('Backend service loaded successfully')"
```
Verifies FastAPI routing, model loading, and service module imports.

## 3. End-to-End Verification Test

```bash
# Upload sample document to analyze endpoint
curl -X POST "http://127.0.0.1:8000/api/analyze" -F "file=@temp.jpg" -F "lang=multi"
```
