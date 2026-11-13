import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IS_VERCEL = bool(os.environ.get("VERCEL"))
STORAGE_DIR = Path("/tmp") if IS_VERCEL else BASE_DIR

class Config:
    """Application configuration settings for LUNG-AI."""
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get("SECRET_KEY", "mca-lung-ai-secure-key-2026")
    
    # Storage Paths
    DATABASE_PATH = (STORAGE_DIR / "lung_ai.db") if IS_VERCEL else (BASE_DIR / "database" / "lung_ai.db")
    UPLOAD_FOLDER = (STORAGE_DIR / "uploads") if IS_VERCEL else (BASE_DIR / "static" / "uploads")
    HEATMAP_FOLDER = (STORAGE_DIR / "heatmaps") if IS_VERCEL else (BASE_DIR / "static" / "heatmaps")
    REPORT_FOLDER = (STORAGE_DIR / "reports") if IS_VERCEL else (BASE_DIR / "reports")
    MODEL_DIR = BASE_DIR / "models"
    DATASET_DIR = BASE_DIR / "dataset"
    
    # Deep Learning & Classification Config
    IMAGE_SIZE = (224, 224)
    BATCH_SIZE = 16
    CLASS_NAMES = [
        "Benign Lung Tissue",
        "Lung Adenocarcinoma",
        "Lung Squamous Cell Carcinoma"
    ]
    CLASS_LABELS = ["lung_n", "lung_aca", "lung_scc"]
    
    # Upload limits (16 MB maximum)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "tif", "tiff"}

    # Available Models for Comparison
    MODELS = {
        "custom_cnn": {
            "name": "Custom CNN",
            "file": "custom_cnn.keras",
            "type": "Baseline CNN Architecture",
            "description": "5-layer sequential convolutional neural network built from scratch."
        },
        "mobilenetv2": {
            "name": "MobileNetV2",
            "file": "mobilenetv2.keras",
            "type": "Transfer Learning",
            "description": "Lightweight, inverted residual network pretrained on ImageNet."
        },
        "efficientnetb0": {
            "name": "EfficientNetB0",
            "file": "efficientnetb0.keras",
            "type": "Transfer Learning",
            "description": "Compound scaled neural network balancing depth, width, and resolution."
        }
    }

