from pathlib import Path
from typing import Tuple, Optional, Union
import numpy as np  # type: ignore
from PIL import Image  # type: ignore

try:
    import tensorflow as tf  # type: ignore
except ImportError:
    tf = None

try:
    import cv2  # type: ignore
except ImportError:
    cv2 = None


def find_last_conv_layer(model: "tf.keras.Model") -> str:
    """
    Identifies the name of the last convolutional layer in the model.
    Supports standard Conv2D layers as well as nested transfer learning backbones
    (MobileNetV2, EfficientNetB0).
    """
    if tf is not None:
        # First check direct Conv2D or DepthwiseConv2D layers
        for layer in reversed(model.layers):
            if isinstance(layer, (tf.keras.layers.Conv2D, tf.keras.layers.DepthwiseConv2D)):
                return layer.name
            # If backbone contains nested layers
            if hasattr(layer, "layers"):
                for sub_layer in reversed(layer.layers):
                    if isinstance(sub_layer, (tf.keras.layers.Conv2D, tf.keras.layers.DepthwiseConv2D)):
                        return f"{layer.name}/{sub_layer.name}"

    # Name-based fallback for standard models
    for layer in reversed(model.layers):
        if "conv" in layer.name.lower():
            return layer.name
        if hasattr(layer, "layers"):
            for sub_layer in reversed(layer.layers):
                if "conv" in sub_layer.name.lower():
                    return f"{layer.name}/{sub_layer.name}"

    raise ValueError("No Conv2D layer found in model")


def generate_gradcam(
    model: "tf.keras.Model",
    image_array: np.ndarray,
    output_path: Union[str, Path]
) -> str:
    """
    Generates a Grad-CAM saliency overlay on the input histopathology image
    and writes the composite image to output_path.
    
    Args:
        model: Trained tf.keras.Model classifier.
        image_array: Preprocessed image batch array with shape (1, 224, 224, 3) and values in [0, 1].
        output_path: Destination path for saving the Grad-CAM visualization.
    Returns:
        str: Path to the generated overlay image.
    """
    if tf is None or cv2 is None:
        raise RuntimeError("TensorFlow and OpenCV (cv2) are required for Grad-CAM generation.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    last_conv_layer = find_last_conv_layer(model)

    try:
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[
                model.get_layer(last_conv_layer).output,
                model.output
            ]
        )
    except Exception:
        # Fallback if layer is nested inside a functional/sequential container
        conv_layers = [l for l in model.layers if "conv" in l.name.lower()]
        target_layer = conv_layers[-1] if conv_layers else model.layers[-2]
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[target_layer.output, model.output]
        )

    with tf.GradientTape() as tape:
        conv_output, predictions = grad_model(
            image_array, training=False
        )
        class_index = tf.argmax(predictions[0])
        class_score = predictions[:, class_index]

    gradients = tape.gradient(class_score, conv_output)
    pooled_gradients = tf.reduce_mean(gradients, axis=(0, 1, 2))

    conv_output = conv_output[0]
    heatmap = tf.reduce_sum(conv_output * pooled_gradients, axis=-1)

    heatmap = tf.maximum(heatmap, 0)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)

    heatmap = heatmap.numpy()
    heatmap = cv2.resize(heatmap, (224, 224))
    heatmap = np.uint8(255 * heatmap)

    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    original = np.uint8(image_array[0] * 255)
    original = cv2.cvtColor(original, cv2.COLOR_RGB2BGR)

    overlay = cv2.addWeighted(original, 0.6, heatmap_color, 0.4, 0)

    cv2.imwrite(str(output_path), overlay)
    return str(output_path)


def make_gradcam_heatmap(
    img_array: np.ndarray,
    model: "tf.keras.Model",
    last_conv_layer_name: Optional[str] = None,
    pred_index: Optional[int] = None
) -> np.ndarray:
    """Computes normalized Grad-CAM activation heatmap array."""
    if tf is None:
        raise RuntimeError("TensorFlow is required for Grad-CAM computation.")

    if last_conv_layer_name is None:
        last_conv_layer_name = find_last_conv_layer(model)

    try:
        grad_model = tf.keras.models.Model(
            inputs=[model.inputs],
            outputs=[model.get_layer(last_conv_layer_name).output, model.output]
        )
    except Exception:
        conv_layers = [l for l in model.layers if "conv" in l.name.lower()]
        target_layer = conv_layers[-1] if conv_layers else model.layers[-2]
        grad_model = tf.keras.models.Model(
            inputs=[model.inputs],
            outputs=[target_layer.output, model.output]
        )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
    return heatmap.numpy()


def save_and_display_gradcam(
    original_pil: Image.Image,
    heatmap: np.ndarray,
    cam_path: Union[str, Path],
    alpha: float = 0.4
) -> str:
    """Superimposes Grad-CAM heatmap over original PIL image using OpenCV."""
    cam_path = Path(cam_path)
    cam_path.parent.mkdir(parents=True, exist_ok=True)

    if cv2 is None:
        original_pil.save(cam_path)
        return str(cam_path)

    img = np.array(original_pil)
    heatmap_uint8 = np.uint8(255 * heatmap)
    jet = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    jet = cv2.resize(jet, (img.shape[1], img.shape[0]))
    jet = cv2.cvtColor(jet, cv2.COLOR_BGR2RGB)

    superimposed_img = np.uint8(jet * alpha + img * (1.0 - alpha))
    result_image = Image.fromarray(superimposed_img)
    result_image.save(cam_path)

    return str(cam_path)
