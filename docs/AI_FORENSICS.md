# 🔬 TrustChain AI & Digital Forensics Specification

## 1. Deep Learning Classifier (PyTorch ResNet-18)

- **Architecture**: ResNet-18 Convolutional Neural Network backbone.
- **Classifier Layer**: Modified linear head `nn.Linear(512, 2)` mapping features to binary class outputs (`FAKE` at index 0, `REAL` at index 1).
- **Execution**: Evaluated in `eval()` mode using `torch.no_grad()` to prevent memory leaks. Automatically selects `cuda` if GPU acceleration is present, falling back gracefully to `cpu`.
- **Pre-processing Transforms**:
  - `Resize((224, 224))`
  - `ToTensor()`
  - `Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])`

---

## 2. Error Level Analysis (ELA) Engine

Error Level Analysis detects digital image manipulation by analyzing local compression variances in JPEG format images. When an image is modified, edited regions re-save at different quality compression levels compared to pristine areas.

### Methodology
1. Load raw original image and convert to `RGB`.
2. Resave to temporary storage at controlled JPEG quality ($90\%$).
3. Compute absolute pixel-wise difference: $\text{Diff} = |\text{Original} - \text{Compressed}|$.
4. Dynamically scale difference map brightness ($\text{Scale} = 255.0 / \text{MaxDiff}$).
5. Calculate grayscale difference map variance ($\sigma^2$) using NumPy (`np.var`).
6. Calculate ratio of suspicious high-difference pixels ($\text{Diff} > 128$).

### Normalized ELA Score Formula
The ELA score ($S_{\text{ELA}} \in [0.0, 1.0]$) is derived from the difference variance:

$$S_{\text{ELA}} = 1.0 - \min\left(1.0, \max\left(0.0, \frac{\sigma^2}{2500.0}\right)\right)$$

* **$S_{\text{ELA}} \ge 0.80$**: Low compression variance ($\sigma^2 < 500$), indicating uniform image compression.
* **$S_{\text{ELA}} < 0.50$**: Elevated variance ($\sigma^2 > 1250$), indicating localized compression anomalies.

---

## 3. Multilingual OCR Engine

- **Engine**: Tesseract OCR v5.5 (`pytesseract`).
- **Configuration**: `--oem 3 --psm 6` (Uniform block of text assumption).
- **Language Models**:
  - English (`eng`)
  - Tamil (`tam`)
  - Hindi (`hin`)
  - Malayalam (`mal`)
  - Telugu (`tel`)
  - Multilingual (`eng+tam+hin+mal+tel`)
- **Metrics Evaluated**:
  - `character_count`: Total extracted character count.
  - `text_density`: $\frac{\text{character\_count}}{\text{width} \times \text{height}}$.
  - `confidence`: Average word-level OCR confidence score ($0.0 - 1.0$) computed via `pytesseract.image_to_data()`.

---

## 4. Hybrid Confidence Engine & Classification

The hybrid engine combines evidence scores from AI, ELA, and OCR using a dynamically weighted formula:

$$\text{Hybrid Score} = \frac{w_{\text{AI}} \cdot S_{\text{AI}} + w_{\text{ELA}} \cdot S_{\text{ELA}} + w_{\text{OCR}} \cdot S_{\text{OCR}}}{\sum w_{\text{active}}}$$

### Default Component Weights
- $w_{\text{AI}} = 0.50$
- $w_{\text{ELA}} = 0.35$
- $w_{\text{OCR}} = 0.15$

If an optional component fails (e.g. OCR or ELA failure due to unreadable images), the system re-normalizes active weights so the total weight remains $1.0$.

### Classification States
- 🟢 **`AUTHENTIC`** ($\text{Hybrid Score} \ge 0.80$): High integrity across visual, compression, and textual forensic signals.
- 🟡 **`SUSPICIOUS`** ($0.55 \le \text{Hybrid Score} < 0.80$): Minor forensic anomalies or compression inconsistencies detected.
- 🔴 **`LIKELY_FORGED`** ($\text{Hybrid Score} < 0.55$): Multiple forgery indicators present.
- ⚪ **`INCONCLUSIVE`**: Unreadable document or multiple essential processing failures.

---

## ⚠️ Limitations & Disclaimers

> TrustChain provides automated AI-assisted digital forensic assessment indicators. Analysis results do not constitute a legal guarantee of authenticity or court-admissible forensic testimony.
