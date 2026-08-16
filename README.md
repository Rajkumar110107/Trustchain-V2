# 🛡️ TrustChain — AI Document Forgery Detection & Blockchain Verification Platform

**TrustChain** is an end-to-end multi-forensic document authentication platform combining **PyTorch (ResNet-18)**, **Error Level Analysis (ELA)**, **Multilingual OCR (Tesseract)**, and **Ethereum Smart Contracts**.

---

## 🌟 Key Features

- 🧠 **ResNet-18 Image Classification**: Deep learning authenticity assessment.
- 🔬 **Error Level Analysis (ELA)**: Dynamic JPEG re-compression difference heatmaps for visual forgery inspection.
- 🔤 **Multilingual OCR Engine**: Extraction for English, Tamil, Hindi, Malayalam, and Telugu documents.
- 🎯 **Explainable Hybrid Confidence Engine**: Transparent authenticity categories (`AUTHENTIC`, `SUSPICIOUS`, `LIKELY FORGED`, `UNABLE TO VERIFY`).
- ⛓️ **Ethereum Smart Contract Verification**: Cryptographic SHA-256 document hash registration and verification on-chain (`DocumentRegistry.sol`).
- 🎨 **Modern React Dashboard**: Responsive glassmorphism interface built with React 19, Vite, Tailwind CSS, and Framer Motion.

---

## 🏗️ Architecture & Documentation

- [📁 Architecture Guide](docs/ARCHITECTURE.md)
- [⛓️ Blockchain Specifications](docs/BLOCKCHAIN.md)
- [🔌 REST API Documentation](docs/API.md)
- [🚀 Deployment Guide](docs/DEPLOYMENT.md)
- [🔒 Security Specifications](docs/SECURITY.md)
- [🧪 Testing Guide](docs/TESTING.md)

---

## 🚀 Quick Start

```bash
# 1. Start Smart Contract Environment (Optional Local Blockchain)
cd blockchain
npx hardhat node

# 2. Start Backend API
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# 3. Start Frontend UI
cd frontend
npm run dev
```

Open `http://localhost:5173` to launch the application dashboard.
