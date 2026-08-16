# 📐 TrustChain Architecture & Data Boundary Specifications

## System Topology & Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 React 19 Frontend Dashboard                 │
│            (Vite + Tailwind CSS + Framer Motion)            │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST API (JSON / FormData)
┌──────────────────────────────▼──────────────────────────────┐
│                      FastAPI Backend                        │
│            (Routes, Schemas, Config, Middleware)            │
└──────┬──────────────────────┬──────────────────────┬────────┘
       │                      │                      │
┌──────▼───────┐       ┌──────▼───────┐       ┌──────▼───────┐
│  AI Engine   │       │ Forensics    │       │   SHA-256    │
│ (ResNet-18)  │       │ (ELA + OCR)  │       │ Hashing Service│
└──────────────┘       └──────────────┘       └──────┬───────┘
                                                     │ 64-char Hex / bytes32
                                              ┌──────▼───────┐
                                              │ Blockchain   │
                                              │ Service      │
                                              └──────┬───────┘
                                                     │ JSON-RPC (:8545)
                                              ┌──────▼───────┐
                                              │ Smart        │
                                              │ Contract     │
                                              │(DocumentRegistry)│
                                              └──────┬───────┘
                                                     │ EVM
                                              ┌──────▼───────┐
                                              │ Ethereum     │
                                              │ Testnet      │
                                              └──────────────┘
```

---

## 🔒 Off-Chain vs On-Chain Data Boundary

To optimize gas consumption and guarantee privacy compliance, TrustChain strictly enforces data boundaries between off-chain storage and on-chain smart contracts.

### 📦 OFF-CHAIN STORAGE
The following data components are processed in-memory or stored locally and are **NEVER** transmitted to or stored on the blockchain:
* Raw uploaded document image files (`.jpg`, `.jpeg`, `.png`, `.webp`).
* Generated Error Level Analysis (ELA) heatmaps and temporary compression outputs.
* Extracted Tesseract OCR text strings, character metrics, and line details.
* PyTorch ResNet-18 raw logit vectors, softmax probabilities, and model weight binaries.
* Personal identifiable information (PII) or confidential document contents.

### ⛓️ ON-CHAIN STORAGE (`DocumentRegistry.sol`)
Only non-reversible cryptographic fingerprint metadata is stored in contract state:
* **Document Hash (`bytes32 docHash`)**: Deterministic 256-bit SHA-256 digest calculated from raw uploaded document bytes prior to any processing.
* **Registrant Address (`address registrant`)**: Ethereum wallet address (`msg.sender`) that signed the registration transaction.
* **Block Timestamp (`uint256 timestamp`)**: Immutable block timestamp (`block.timestamp`) recording exact registration time.

---

## 🧩 Component Responsibilities

1. **`backend/routes/`**: Handles endpoint routing (`analysis.py` for `/api/analyze`, `blockchain.py` for `/api/register`, `/api/verify`, `/api/document/{hash}`).
2. **`backend/schemas/`**: Pydantic input/output schemas ensuring strict API response contracts.
3. **`backend/services/hashing_service.py`**: Accepts original file bytes and returns deterministic 64-char hex digests and Solidity `bytes32` formats.
4. **`backend/services/blockchain_service.py`**: Web3.py wrapper communicating with `DocumentRegistry.sol`.
