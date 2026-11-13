import shutil
import random
from pathlib import Path
from config import Config

def prepare_splits(
    source_dir=Config.DATASET_DIR / "raw",
    output_dir=Config.DATASET_DIR / "splits",
    train_ratio=0.70,
    val_ratio=0.15,
    test_ratio=0.15,
    seed=42
):
    """
    Performs stratified partition of lung histopathology images into train, validation, and test splits.
    """
    random.seed(seed)
    source_dir = Path(source_dir)
    output_dir = Path(output_dir)

    print(f"Preparing dataset splits from {source_dir} -> {output_dir}")
    
    for split in ["train", "val", "test"]:
        for label in Config.CLASS_LABELS:
            (output_dir / split / label).mkdir(parents=True, exist_ok=True)

    for label in Config.CLASS_LABELS:
        class_folder = None
        for candidate in source_dir.rglob(label):
            if candidate.is_dir():
                class_folder = candidate
                break

        if not class_folder:
            print(f"Warning: Folder for class '{label}' not found in {source_dir}. Skipping.")
            continue

        images = [f for f in class_folder.iterdir() if f.suffix.lower() in {".jpeg", ".jpg", ".png", ".tif"}]
        random.shuffle(images)

        n_total = len(images)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        train_imgs = images[:n_train]
        val_imgs = images[n_train:n_train + n_val]
        test_imgs = images[n_train + n_val:]

        splits_map = {
            "train": train_imgs,
            "val": val_imgs,
            "test": test_imgs
        }

        for split_name, img_list in splits_map.items():
            dest_dir = output_dir / split_name / label
            for img_path in img_list:
                shutil.copy2(img_path, dest_dir / img_path.name)

        print(f"[{label}] Total: {n_total} -> Train: {len(train_imgs)}, Val: {len(val_imgs)}, Test: {len(test_imgs)}")

    print("\nDataset preparation completed successfully.")

if __name__ == "__main__":
    prepare_splits()

