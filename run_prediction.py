import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from prediction.predict import predict_image, predict_single_image, CLASS_NAMES, MODEL_PATHS
from prediction.gradcam import generate_gradcam
from prediction.preprocessing import preprocess_image


def find_latest_image():
    """Finds the most recently uploaded image in static/uploads for quick testing."""
    uploads_dir = PROJECT_ROOT / "static" / "uploads"
    if not uploads_dir.exists():
        return None
    images = [
        f for f in uploads_dir.glob("*.*")
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
    ]
    if not images:
        return None
    # Sort by modification time, descending
    images.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return images[0]


def main():
    parser = argparse.ArgumentParser(
        description="LUNG-AI CLI Prediction & Explainability Runner"
    )
    parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="Path to the histopathology image slide (defaults to latest uploaded image)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Custom CNN",
        choices=["Custom CNN", "MobileNetV2", "EfficientNetB0"],
        help="Target neural network architecture"
    )
    parser.add_argument(
        "--gradcam",
        action="store_true",
        help="Generate and save a Grad-CAM saliency overlay"
    )

    args = parser.parse_args()

    # Determine image path
    if args.image:
        image_path = Path(args.image)
        if not image_path.is_absolute():
            image_path = PROJECT_ROOT / image_path
    else:
        image_path = find_latest_image()
        if not image_path:
            print("❌ No image found in static/uploads/. Please specify an image using --image <path>.")
            sys.exit(1)
        print(f"📁 Using latest uploaded slide: {image_path.name}")

    if not image_path.exists():
        print(f"❌ Error: Image file does not exist at {image_path}")
        sys.exit(1)

    print("\n" + "=" * 55)
    print(" 🫁 LUNG-AI Diagnostic Inference")
    print(f" 🔬 Slide: {image_path.name}")
    print(f" 🧠 Model: {args.model}")
    print("=" * 55 + "\n")

    # Run prediction
    result = predict_image(image_path, model_name=args.model)

    print(f"🎯 Predicted Class:      {result['predicted_class']}")
    print(f"📊 Confidence Score:     {result['confidence']:.4f} ({result.get('confidence_percentage', result['confidence']*100):.2f}%)")
    
    if result["uncertain"]:
        print(f"⚠️  High Uncertainty:     YES (Confidence < {result['uncertainty_threshold']*100:.0f}%)")
        print("   ↳ Manual histological review by a pathologist recommended.")
    else:
        print(f"✅ High Uncertainty:     NO (Meets confidence threshold)")

    print("\n📈 Probability Distribution:")
    for class_name, prob in result["probabilities"].items():
        bar_len = int(prob * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        star = " ★" if class_name == result["predicted_class"] else "  "
        print(f"  {star} {class_name:<30} {bar} {prob*100:6.2f}%")

    # Optional Grad-CAM synthesis
    if args.gradcam:
        print("\n🔍 Synthesizing Grad-CAM Heatmap...")
        try:
            from prediction.predict import load_model
            model = load_model(args.model)
            batch_array, _ = preprocess_image(image_path)
            cam_out = PROJECT_ROOT / "static" / "heatmaps" / f"cli_cam_{image_path.stem}.jpg"
            generate_gradcam(model, batch_array, cam_out)
            print(f"✅ Heatmap saved to: {cam_out}")
        except Exception as e:
            print(f"⚠️ Grad-CAM synthesis note: {e}")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    main()

