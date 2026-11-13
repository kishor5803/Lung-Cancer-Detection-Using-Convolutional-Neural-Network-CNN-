import argparse
from pathlib import Path
from config import Config

try:
    import tensorflow as tf  # type: ignore
except ImportError:
    tf = None

def build_efficientnet_b0(input_shape=(224, 224, 3), num_classes=3):
    """Constructs EfficientNetB0 transfer learning architecture."""
    inputs = tf.keras.Input(shape=input_shape)
    
    # EfficientNet expects [0, 255] float input natively
    base_model = tf.keras.applications.EfficientNetB0(
        input_tensor=inputs,
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False
    
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="EfficientNetB0_Transfer")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=3e-4),
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
    print("       TRAINING MODEL 3: EFFICIENTNETB0 (TRANSFER LEARNING)")
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

    model = build_efficientnet_b0()
    save_path = Config.MODEL_DIR / Config.MODELS["efficientnetb0"]["file"]

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
    print(f"\n[✓] EfficientNetB0 model trained and saved to: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    train(epochs=args.epochs, batch_size=args.batch_size)

