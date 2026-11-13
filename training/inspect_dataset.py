import os
from pathlib import Path
from PIL import Image  # type: ignore
from config import Config

def inspect_dataset(dataset_dir=Config.DATASET_DIR):
    """
    Scans histopathology dataset folders, validates image integrity,
    and reports per-class sample counts.
    """
    dataset_dir = Path(dataset_dir)
    print("=" * 55)
    print("       LUNG-AI HISTOPATHOLOGY DATASET INSPECTION")
    print("=" * 55)
    print(f"Target Directory: {dataset_dir.resolve()}\n")

    if not dataset_dir.exists():
        print(f"[!] Dataset folder not found at: {dataset_dir}")
        print("Please place the LC25000 lung image folders into 'LUNG-AI/dataset/raw/'")
        return

    stats = {}
    total_images = 0
    sample_sizes = set()

    for class_folder in dataset_dir.rglob("*"):
        if class_folder.is_dir() and class_folder.name in Config.CLASS_LABELS:
            images = [f for f in class_folder.iterdir() if f.suffix.lower() in {".jpeg", ".jpg", ".png", ".tif"}]
            count = len(images)
            stats[class_folder.name] = count
            total_images += count
            
            # Inspect sample image dimensions
            if images:
                try:
                    with Image.open(images[0]) as img:
                        sample_sizes.add(img.size)
                except Exception:
                    pass

    print(f"Classes Discovered: {len(stats)}")
    for label in Config.CLASS_LABELS:
        count = stats.get(label, 0)
        readable = Config.CLASS_NAMES[Config.CLASS_LABELS.index(label)]
        print(f" - {label:<10} ({readable:<28}): {count:,} images")

    print("-" * 55)
    print(f"Total Lung Images: {total_images:,}")
    if sample_sizes:
        print(f"Detected Native Resolutions: {list(sample_sizes)}")
    print("=" * 55)

if __name__ == "__main__":
    inspect_dataset()

