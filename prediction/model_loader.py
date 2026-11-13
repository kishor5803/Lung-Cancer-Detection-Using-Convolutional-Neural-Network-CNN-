from pathlib import Path
from typing import Dict, Any, Optional
from config import Config

try:
    import tensorflow as tf  # type: ignore
except ImportError:
    tf = None

_LOADED_MODELS: Dict[str, Any] = {}

def get_model(model_key: str = "custom_cnn"):
    """
    Retrieves or loads the requested neural network model from disk cache.
    Supports 'custom_cnn', 'mobilenetv2', and 'efficientnetb0'.
    """
    global _LOADED_MODELS

    if model_key not in Config.MODELS:
        model_key = "custom_cnn"

    if model_key in _LOADED_MODELS:
        return _LOADED_MODELS[model_key]

    model_info = Config.MODELS[model_key]
    model_path = Config.MODEL_DIR / model_info["file"]

    if tf is not None and model_path.exists():
        try:
            model = tf.keras.models.load_model(model_path)
            _LOADED_MODELS[model_key] = model
            print(f"Loaded trained model: {model_key} from {model_path}")
            return model
        except Exception as e:
            print(f"Warning: Could not load trained weights for {model_key} ({e}).")

    return None

