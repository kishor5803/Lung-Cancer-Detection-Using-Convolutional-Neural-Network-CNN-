import sys
import importlib.metadata

print("=" * 50)
print("           LUNG-AI ENVIRONMENT CHECK")
print("   MCA Academic Project Architecture (2026-2027)")
print("=" * 50)
print(f"Operating System : Windows ({sys.platform})")
print(f"Python Executable: {sys.executable}")
print(f"Python Version   : {sys.version.split()[0]}")
print("-" * 50)

packages = [
    ("Flask", "flask"),
    ("NumPy", "numpy"),
    ("OpenCV", "opencv-python"),
    ("Scikit-learn", "scikit-learn"),
    ("Matplotlib", "matplotlib"),
    ("ReportLab", "reportlab"),
    ("Pillow", "pillow"),
    ("Pandas", "pandas"),
    ("Werkzeug", "werkzeug"),
    ("TensorFlow", "tensorflow"),
]

installed_count = 0
for display_name, pkg_name in packages:
    try:
        ver = importlib.metadata.version(pkg_name)
        print(f" [✓] {display_name:<16}: {ver}")
        installed_count += 1
    except importlib.metadata.PackageNotFoundError:
        print(f" [✗] {display_name:<16}: NOT INSTALLED")

print("-" * 50)
print(f"Package Status   : {installed_count}/{len(packages)} Core Libraries Verified")

try:
    import tensorflow as tf
    print("\nDeep Learning Hardware Acceleration:")
    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        print(f" [✓] GPU Detected: {gpus}")
    else:
        print(" [i] Compute Mode: CPU Execution (Recommended for initial training & inference)")
    x = tf.random.normal((2, 224, 224, 3))
    print(f" [✓] Tensor Allocation Test Passed: {x.shape}")
except Exception as e:
    print(f"\nTensorFlow Diagnostic Note: {e}")

print("=" * 50)
