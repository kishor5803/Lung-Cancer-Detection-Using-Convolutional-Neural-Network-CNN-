import io
from pathlib import Path
from typing import Tuple, Union
import numpy as np  # type: ignore
from PIL import Image  # type: ignore

DEFAULT_TARGET_SIZE: Tuple[int, int] = (224, 224)

def preprocess_image(
    image_input: Union[str, Path, bytes],
    target_size: Tuple[int, int] = DEFAULT_TARGET_SIZE
) -> Tuple[np.ndarray, Image.Image]:
    """
    Loads and preprocesses a lung histopathology image.
    Returns:
        (preprocessed_batch, original_pil_image)
    """
    if isinstance(image_input, (str, Path)):
        pil_image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, bytes):
        pil_image = Image.open(io.BytesIO(image_input)).convert("RGB")
    else:
        raise ValueError("Unsupported image input type.")
        
    # Resize to model input dimensions
    resized = pil_image.resize(target_size)
    
    # Scale pixel intensities to [0, 1]
    img_array = np.array(resized, dtype=np.float32) / 255.0
    
    # Expand to batch shape: (1, height, width, 3)
    batch_array = np.expand_dims(img_array, axis=0)
    
    return batch_array, pil_image

