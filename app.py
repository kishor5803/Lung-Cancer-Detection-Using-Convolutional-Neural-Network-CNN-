import os
import uuid
from pathlib import Path
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session, send_from_directory
)
from werkzeug.utils import secure_filename

from config import Config
from database.db import init_db
from services.auth_service import authenticate_user, register_user
from services.history_service import (
    save_prediction, get_user_history,
    get_all_predictions, get_dashboard_metrics
)
from services.report_service import generate_pdf_report
from prediction.predict import predict_single_image
from training.compare_models import generate_benchmark_metrics

app = Flask(__name__)
app.config.from_object(Config)

# Ensure essential directories exist
Config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
Config.HEATMAP_FOLDER.mkdir(parents=True, exist_ok=True)
Config.REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Initialize database schema and default admin
try:
    init_db()
except Exception as e:
    print(f"Database init notice: {e}")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Main diagnostic workspace for uploading and classifying histopathology scans."""
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    """Handles image upload, runs selected deep learning model and Grad-CAM."""
    if "file" not in request.files:
        flash("No file was uploaded.", "danger")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No image file selected.", "danger")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash(f"Invalid file format. Allowed formats: {', '.join(Config.ALLOWED_EXTENSIONS)}", "danger")
        return redirect(url_for("index"))

    model_key = request.form.get("model_key", "custom_cnn")
    generate_cam = bool(request.form.get("gradcam", 1))

    # Secure and unique filename
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex[:10]}_{secure_filename(file.filename)}"
    save_path = Config.UPLOAD_FOLDER / unique_name
    file.save(save_path)

    # Execute deep learning inference and Grad-CAM
    try:
        prediction_result = predict_single_image(
            save_path,
            model_key=model_key,
            generate_cam=generate_cam
        )
    except Exception as e:
        flash(f"Inference error: {str(e)}", "danger")
        return redirect(url_for("index"))

    # Generate Clinical PDF Report
    heatmap_full_path = (
        Config.HEATMAP_FOLDER / Path(prediction_result["heatmap_url"]).name
        if prediction_result.get("heatmap_url")
        else None
    )

    pdf_rel_path = ""
    try:
        pdf_rel_path = generate_pdf_report(
            prediction_result,
            original_image_path=save_path,
            heatmap_image_path=heatmap_full_path,
            case_id=unique_name.split("_")[0]
        )
    except Exception as e:
        print(f"PDF report generation note: {e}")

    # Persist in SQLite prediction history
    user_id = session.get("user_id")
    save_prediction(
        user_id=user_id,
        filename=unique_name,
        predicted_class=prediction_result["predicted_class"],
        confidence=prediction_result["confidence_score"],
        model_name=prediction_result["model_name"],
        heatmap_path=prediction_result.get("heatmap_url", ""),
        pdf_path=pdf_rel_path,
        class_probabilities=prediction_result.get("class_probabilities", {})
    )

    return render_template(
        "result.html",
        prediction=prediction_result,
        original_filename=unique_name,
        pdf_url=pdf_rel_path
    )


@app.route("/dashboard")
def dashboard():
    """Model Comparison Dashboard displaying comparative performance metrics."""
    metrics_path = Config.MODEL_DIR / "model_metrics.json"
    if metrics_path.exists():
        import json
        with open(metrics_path, "r", encoding="utf-8") as f:
            models_data = json.load(f)
    else:
        models_data = generate_benchmark_metrics()

    return render_template("dashboard.html", models=models_data)


@app.route("/history")
def history():
    """User's historical classification log and downloadable PDF reports."""
    user_id = session.get("user_id")
    if user_id:
        records = get_user_history(user_id)
    else:
        # Show general recent records if guest
        records = get_all_predictions(limit=15)
    return render_template("history.html", records=records)


@app.route("/reports/<path:filename>")
def download_report(filename):
    """Downloads or previews the generated PDF diagnostic report."""
    return send_from_directory(Config.REPORT_FOLDER, filename, as_attachment=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    """User and Administrator authentication."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = authenticate_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["user_role"] = user["role"]
            flash(f"Welcome back, {user['username']}!", "success")
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration for persistent case history tracking."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if len(username) < 3 or len(password) < 4:
            flash("Username must be at least 3 characters and password at least 4.", "warning")
            return render_template("login.html")

        ok, msg = register_user(username, password, role="user")
        if ok:
            flash("Account registered successfully. Please sign in.", "success")
            return redirect(url_for("login"))
        else:
            flash(msg, "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clears user session."""
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("index"))


@app.route("/admin")
def admin_dashboard():
    """Protected administrative panel for system monitoring and user tracking."""
    if session.get("user_role") != "admin":
        flash("Administrator access required.", "danger")
        return redirect(url_for("login"))

    metrics = get_dashboard_metrics()
    predictions = get_all_predictions(limit=50)
    return render_template("admin/dashboard.html", metrics=metrics, predictions=predictions)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(" 🫁 LUNG-AI Flask Application Running")
    print(" URL: http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
