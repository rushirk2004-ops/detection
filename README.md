# detection

# Guava Leaf & Fruit Disease Detection System 🌿🔬
**Final Year B.Tech / BE Academic Capstone Project (2026–2027)**

An enterprise-grade, Explainable Deep Learning and Agricultural Advisory System for real-time detection, classification, and treatment of Guava diseases.

---

## 📌 Project Overview
Guava (*Psidium guajava*) is a vital tropical commercial crop susceptible to debilitating fungal and algal diseases such as Canker, Dot, Mummification, and Rust. This project introduces a dual-panel web application:
1. **Farmer & User Portal**:
   - Touch-friendly, agricultural-first interface (English & Marathi localization).
   - High-confidence classification powered by deep neural networks.
   - Explainable AI (XAI) using Grad-CAM heatmaps showing affected leaf regions.
   - Comprehensive chemical spray schedules, bio-fungicides, organic remedies, and preventive cultivation guides.
   - 60% confidence safety uncertainty warning for blurry or out-of-focus images.
   - Strict privacy: user photos stay in-memory unless explicitly opted in for history recording.
2. **Admin & Research Portal**:
   - Secure PBKDF2-HMAC-SHA256 salted authentication.
   - Real-time hardware health telemetry (CPU, RAM, Disk, PyTorch CUDA acceleration).
   - Model checkpoint inspector (`ResNet-50` and `EfficientNet-B3`).
   - Controlled diagnostic testing with raw logit and softmax distribution inspection.
   - Verified evaluation reporting with real confusion matrices and classification metrics.
   - SQLite-backed audit trails and query history management.

---

## 🧠 Model Architectures & Performance

Both models were trained on a curated dataset of **4,598 images** across 5 categories (`Canker`, `Dot`, `Healthy`, `Mummification`, `Rust`) with an 80/10/10 train/val/test split.

| Model Architecture | Parameters | Input Resolution | Test Accuracy | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EfficientNet-B3** (Compound Scaled CNN) | ~10.7M | 224 × 224 | **96.26%** | **96.48%** | **96.26%** | **96.22%** |
| **ResNet-50** (Residual Network) | ~23.5M | 224 × 224 | **90.95%** | **91.55%** | **90.95%** | **90.58%** |

- **Leaf Classes**: `Canker`, `Dot`, `Healthy`, `Mummification`, `Rust`
- **Fruit Module Status**: Fruit classes configured in `config/settings.yaml`. The user interface displays a friendly under-construction notice for Fruit target until field fruit datasets are finalized.

---

## 📂 System Architecture & Folder Structure

```text
guava-leaf-disease-detection/
├── app.py                             # Master Streamlit entry point (Role-based portal router)
├── config/
│   └── settings.yaml                  # System parameters, uncertainty thresholds, classes
├── core/
│   ├── __init__.py
│   ├── inference.py                   # Unified AI inference engine (shared by both panels)
│   ├── preprocessing.py               # ImageNet RGB transform (224x224, normalization)
│   ├── model_loader.py                # Safe PyTorch loader with CUDA/CPU auto-detection
│   ├── gradcam.py                     # Layer-specific Grad-CAM (ResNet-50 & EfficientNet-B3)
│   └── validation.py                  # Format, corruption, size, and dimension validation
├── services/
│   ├── __init__.py
│   ├── authentication.py              # PBKDF2 password hashing & session management
│   ├── disease_service.py             # Agricultural treatments in English & Marathi
│   ├── history_service.py             # SQLite persistence & user privacy management
│   ├── system_service.py              # Hardware monitoring & GPU/CPU telemetry
│   ├── evaluation_service.py          # Confusion matrices & evaluation metrics
│   └── configuration_service.py       # Configuration reader & threshold updates
├── components/
│   ├── __init__.py
│   ├── farmer_ui.py                   # Farmer portal interface (English / Marathi)
│   └── admin_ui.py                    # Administrator dashboard & research portal
├── models/
│   └── saved_models/
│       ├── resnet50_best.pt           # Trained PyTorch ResNet-50 weights (~94 MB)
│       └── efficientnet_best.pt       # Trained PyTorch EfficientNet-B3 weights (~43 MB)
├── data/                              # Dataset splits (raw/train/val/test)
├── results/                           # Evaluation visualizations & confusion matrices
├── storage/
│   └── guava_system.db                # SQLite database for history and audit logs
├── tests/
│   └── test_system.py                 # 20 automated pytest test cases
├── requirements.txt                   # Production dependencies
└── README.md                          # Subfolder documentation
```

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- Python 3.10 – 3.14
- CUDA-compatible GPU (Optional; CPU mode is supported automatically)

### 2. Installation
Open a PowerShell / Command Prompt terminal:
```powershell
cd guava-leaf-disease-detection
pip install -r requirements.txt
```

### 3. Running the Application
Launch the web interface:
```powershell
streamlit run app.py
```

The system will start and open in your default browser at:
`http://localhost:8501`

---

## 🔑 Administrative Access

To access the **Admin & Research Management Portal**:
1. In the sidebar, select **🛡️ Admin & Research Portal**.
2. Enter the secure administrator credentials:
   - **Username**: `admin`
   - **Password**: `admin@guava2026`
3. Click **Authenticate & Access**.

*(Password is hashed using PBKDF2-HMAC-SHA256 with a secure salt and validated on the server side.)*

---

## 🧪 Automated Testing

A 20-point test suite is included in `guava-leaf-disease-detection/tests/test_system.py`:
- Valid JPG/PNG uploads
- Invalid file rejection (.pdf, .txt, .exe)
- Corrupted image handling
- Multi-mode RGB conversion (RGBA, Grayscale, CMYK)
- Tensor resizing and normalization
- Leaf and fruit class mappings
- Model checkpoint loading
- CPU and CUDA inference
- Softmax probability distribution
- 60% uncertainty warning safety trigger
- Grad-CAM heatmap generation
- Missing checkpoint handling
- Unauthenticated admin access protection
- Unauthorized admin action prevention
- Configuration schema validation
- SQLite database operations
- User privacy and zero-retention verification
- Unified inference pipeline consistency

To run the automated tests:
```powershell
cd guava-leaf-disease-detection
pytest tests/test_system.py -v
```

---

## 🌾 Academic Demonstration Highlights
- **Real weights**: Both `resnet50_best.pt` and `efficientnet_best.pt` are genuine, trained PyTorch weights.
- **Explainable AI**: Grad-CAM visualizes exact disease lesion areas rather than random background noise.
- **Farmer-Centric**: Supports Marathi (मराठी) and English with organic, chemical, and cultural disease remedies.
- **Ethical AI**: Adheres to data privacy standards; images are processed in-memory without persistent retention unless explicitly permitted by the user.
