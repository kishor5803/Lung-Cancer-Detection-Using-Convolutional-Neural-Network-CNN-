import argparse
from pathlib import Path
from config import Config

try:
    import tensorflow as tf  # type: ignore
except ImportError:
    tf = None

def build_mobilenet_v2(input_shape=(224, 224, 3), num_classes=3):
    """Constructs MobileNetV2 transfer learning model."""
    inputs = tf.keras.Input(shape=input_shape)
    
    # Preprocess matching MobileNet requirements ([-1, 1] range)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    
    base_model = tf.keras.applications.MobileNetV2(
        input_tensor=x,
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze pretrained feature extractor
    
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="MobileNetV2_Transfer")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=5e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

def train(data_dir=Config.DATASET_DIR / "splits", epochs=15, batch_size=16):
    if tf is None:
        raise RuntimeError("TensorFlow is not installed in the environment.")

    data_dir = Path(data_dir)
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"

    print("=" * 55)
    print("       TRAINING MODEL 2: MOBILENETV2 (TRANSFER LEARNING)")
    print("=" * 55)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=Config.IMAGE_SIZE,
        batch_size=batch_size,
        label_mode="int",
        shuffle=True
    ).prefetch(tf.data.AUTOTUNE)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size=Config.IMAGE_SIZE,
        batch_size=batch_size,
        label_mode="int",
        shuffle=False
    ).prefetch(tf.data.AUTOTUNE)

    model = build_mobilenet_v2()
    save_path = Config.MODEL_DIR / Config.MODELS["mobilenetv2"]["file"]

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(filepath=str(save_path), monitor="val_accuracy", save_best_only=True)
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )

    model.save(save_path)
    print(f"\n[✓] MobileNetV2 model trained and saved to: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    train(epochs=args.epochs, batch_size=args.batch_size)

