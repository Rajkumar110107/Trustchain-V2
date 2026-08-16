# ⚠️ TrustChain System Limitations & Known Constraints

## 1. AI Model Limitations
- **Training Data Scope**: ResNet-18 feature extraction accuracy is bounded by the representative document domain present in prototype training datasets. Unseen image document formats may require fine-tuning.
- **Image Resolution**: Extremely low-resolution images (< 200x200 pixels) or severely degraded scans may yield inconclusive AI confidence scores.

## 2. Digital Forensics (ELA & OCR) Constraints
- **Error Level Analysis (ELA)**: ELA variance measurements provide digital image compression evidence, not court-admissible legal proof of forgery. High variance indicates localized compression anomalies, which can occasionally occur due to multiple social media uploads or web optimizations.
- **Tesseract OCR Engine**: OCR accuracy depends heavily on scan lighting, contrast, and font clarity. OCR text density is an evidence signal, and OCR failure does not inherently mean a document is forged.

## 3. Blockchain Data Boundary Constraints
- **Registration vs Authenticity**: Smart contract registration proves cryptographic hash continuity and timestamp registration on-chain. Blockchain registration **does not** prove that the underlying document content was original or authentic when registered.
- **Unregistered Hash Meaning**: An unregistered document hash indicates that the document hash was not previously submitted to the smart contract; it does not automatically imply the document is fraudulent.
- **Testnet Infrastructure**: Ethereum Sepolia testnet nodes depend on public RPC availability and faucet test ETH balances.
