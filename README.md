# 🫁 LUNG-AI: Explainable Deep Learning-Based Lung Histopathological Image Classification

> **Master of Computer Applications (MCA) Academic Project | 2026–2027**  
> An explainable, multi-model deep learning platform for microscopic lung tissue biopsy classification, visual saliency explanations (Grad-CAM), and clinical report generation.

---

## 📑 Project Abstract

Histopathological examination of lung biopsy tissue via microscopic hematoxylin and eosin (H&E) staining is the gold standard for pulmonary neoplasm diagnosis. Differentiating between benign lung tissue, lung adenocarcinoma (ACA), and lung squamous cell carcinoma (SCC) is vital for prescribing targeted therapies and immunotherapy.

**LUNG-AI** improves conventional academic classifiers by introducing an **explainable multi-model comparative architecture**:
1. **Three Neural Network Architectures**: Custom 5-stage CNN vs. MobileNetV2 vs. EfficientNetB0.
2. **Explainable AI (XAI)**: Gradient-weighted Class Activation Mapping (Grad-CAM) to generate morphological visual heatmaps.
3. **Clinical Telemetry & Auditing**: SQLite prediction logging, confidence distributions, and downloadable automated PDF diagnostic reports.
4. **Administrative Governance**: Role-based access control (RBAC), user management, and real-time model comparison dashboards.

---

## 📂 System Architecture & Folder Directory

```
LUNG-AI/
│
├── app.py                            # Flask application core, routes & session management
├── config.py                         # Application configuration, model paths & constants
├── requirements.txt                  # Python runtime dependencies
├── check_environment.py              # Environment and hardware verification script
├── README.md                         # Complete project documentation
│
├── dataset/                          # Histopathology storage
│   ├── raw/                          # Original LC25000 lung image archives
│   ├── processed/                    # Normalized 224x224 RGB dataset
│   └── splits/                       # Stratified train (70%), val (15%), test (15%) splits
│
├── models/                           # Trained neural network weights & evaluation
│   ├── custom_cnn.keras              # Model 1: Baseline Sequential CNN
│   ├── mobilenetv2.keras             # Model 2: Lightweight Transfer Learning
│   ├── efficientnetb0.keras          # Model 3: Compound Scaled Transfer Learning
│   └── model_metrics.json            # Comparative performance metrics benchmark
│
├── training/                         # Deep learning training pipeline
│   ├── inspect_dataset.py            # Dataset validator, balancing & dimension check
│   ├── prepare_dataset.py            # Stratified & leakage-aware data partitioner
│   ├── train_cnn.py                  # Custom CNN training with EarlyStopping
│   ├── train_mobilenet.py            # MobileNetV2 fine-tuning pipeline
│   ├── train_efficientnet.py         # EfficientNetB0 fine-tuning pipeline
│   └── compare_models.py             # Multi-model evaluation on held-out test split
│
├── prediction/                       # Inference & Explainability
│   ├── predict.py                    # Inference coordinator & confidence scoring
│   ├── preprocessing.py              # Image decoding, RGB conversion & batching
│   ├── model_loader.py               # In-memory cached model provider
│   └── gradcam.py                    # Grad-CAM heatmap generation & Jet colormap overlay
│
├── services/                         # Business logic services
│   ├── auth_service.py               # Werkzeug password hashing & authentication
│   ├── history_service.py            # SQLite prediction logging & admin metrics
│   └── report_service.py             # ReportLab automated PDF clinical report generator
│
├── database/                         # Database layer
│   ├── db.py                         # SQLite connection & schema initialization
│   └── schema.sql                    # SQL tables (users, predictions, probabilities, models)
│
├── reports/                          # Stored generated PDF clinical reports
│
├── static/                           # Web assets
│   ├── css/style.css                 # Dark navy (#081426) & gold design system
│   ├── js/main.js                    # Drag-and-drop file upload handler
│   ├── uploads/                      # Uploaded histopathology biopsy slides
│   └── heatmaps/                     # Superimposed Grad-CAM saliency visualizations
│
└── templates/                        # Jinja2 HTML templates
    ├── base.html                     # Navigation bar, layout & medical disclaimer
    ├── index.html                    # Scan diagnosis workspace & model switcher
    ├── result.html                   # Side-by-side biopsy vs. Grad-CAM display
    ├── dashboard.html                # Model performance comparison dashboard
    ├── history.html                  # Historical classifications & PDF download table
    ├── login.html                    # User & Administrator login
    └── admin/
        └── dashboard.html            # System monitoring, user stats & global logs
```

---

## 📊 Dataset Specification (LC25000)

We utilize the 3 pulmonary subsets from the **LC25000 Histopathological Dataset**:

| Directory | Subtype Description | Clinical Pathology | Sample Count |
|---|---|---|---|
| `lung_n` | **Benign Lung Tissue** | Non-malignant healthy alveoli & bronchioles | 5,000 |
| `lung_aca` | **Lung Adenocarcinoma** | Malignant epithelial glandular neoplasm | 5,000 |
| `lung_scc` | **Squamous Cell Carcinoma** | Malignant keratinizing squamous neoplasm | 5,000 |
| **Total** | | | **15,000** |

---

## 🚀 Step-by-Step Setup and Execution

### Step 1: Environment Verification
```powershell
cd C:\Users\kisho\Downloads\loki\LUNG-AI
python check_environment.py
```

### Step 2: Initialize Database
```powershell
python database/db.py
```
* Generates SQLite database `database/lung_ai.db`.
* Creates default Administrator: `admin` / `admin123`.

### Step 3: Train Models (Optional if testing with pre-calibrated preview)
```powershell
# 1. Inspect raw dataset
python training/inspect_dataset.py

# 2. Partition into train / val / test splits
python training/prepare_dataset.py

# 3. Train models
python training/train_cnn.py --epochs 20
python training/train_mobilenet.py --epochs 15
python training/train_efficientnet.py --epochs 15

# 4. Generate comparison benchmark
python training/compare_models.py
```

### Step 4: Run the LUNG-AI Web Application
```powershell
python app.py
```
* **Web Portal**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
* **Default Admin**: `admin` / `admin123`

