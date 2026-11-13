import argparse
from pathlib import Path
from config import Config

try:
    import tensorflow as tf  # type: ignore
except ImportError:
    tf = None

def build_custom_cnn(input_shape=(224, 224, 3), num_classes=3):
    """Constructs the baseline 5-stage Custom CNN architecture."""
    inputs = tf.keras.Input(shape=input_shape)
    
    # Block 1
    x = tf.keras.layers.Conv2D(32, (3, 3), padding="same", activation="relu")(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    # Block 2
    x = tf.keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    # Block 3
    x = tf.keras.layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    # Block 4
    x = tf.keras.layers.Conv2D(256, (3, 3), padding="same", activation="relu")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    # Classification Head
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="Custom_CNN")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

def train(data_dir=Config.DATASET_DIR / "splits", epochs=20, batch_size=16):
    if tf is None:
        raise RuntimeError("TensorFlow is not installed in the environment.")
        
    data_dir = Path(data_dir)
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"
    
    print("=" * 55)
    print("       TRAINING MODEL 1: CUSTOM CNN")
    print("=" * 55)
    
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=Config.IMAGE_SIZE,
        batch_size=batch_size,
        label_mode="int",
        shuffle=True
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size=Config.IMAGE_SIZE,
        batch_size=batch_size,
        label_mode="int",
        shuffle=False
    )
    
    # Normalization layer
    rescaling = tf.keras.layers.Rescaling(1.0 / 255)
    train_ds = train_ds.map(lambda x, y: (rescaling(x), y)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (rescaling(x), y)).prefetch(tf.data.AUTOTUNE)
    
    model = build_custom_cnn()
    model.summary()
    
    Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)
    save_path = Config.MODEL_DIR / Config.MODELS["custom_cnn"]["file"]
    
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(filepath=str(save_path), monitor="val_accuracy", save_best_only=True)
    ]
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )
    
    model.save(save_path)
    print(f"\n[✓] Custom CNN model trained and saved to: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    train(epochs=args.epochs, batch_size=args.batch_size)

