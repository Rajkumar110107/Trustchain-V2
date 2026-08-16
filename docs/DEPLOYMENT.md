# 🚀 TrustChain Deployment Guide

## Prerequisites

- **Node.js**: v20+
- **Python**: v3.10+
- **Tesseract OCR**: Installed at `C:\Program Files\Tesseract-OCR\tesseract.exe` (or configured via `TESSERACT_CMD` in `.env`)

---

## 1. Local Hardhat Node Deployment

```bash
# Terminal 1: Launch Local Hardhat Node
cd blockchain
npx hardhat node
```

```bash
# Terminal 2: Deploy DocumentRegistry Smart Contract
cd blockchain
npm run deploy:local
```

---

## 2. Start Backend Service

```bash
# Terminal 3: Launch FastAPI Server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 3. Start Frontend Dashboard

```bash
# Terminal 4: Launch Vite React Application
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.
