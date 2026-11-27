import os
import uuid
from pathlib import Path
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session, send_from_directory, jsonify
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
from services.stages_service import get_all_stages, get_stage_by_id
from services.measurement_service import (
    estimate_tumor_dimensions, DEFAULT_MICRONS_PER_PIXEL, DEFAULT_MM_PER_PIXEL_CT
)
from services.cancer_types_service import get_all_cancer_types, get_imaging_modalities
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

    # Tumor size & morphometric segmentation
    measurement_data = None
    try:
        measurement_data = estimate_tumor_dimensions(
            save_path,
            heatmap_path=heatmap_full_path,
            pixel_scale_mm=0.0005  # Default 20x H&E optical scale (0.5 um/px)
        )
    except Exception as e:
        print(f"Measurement note: {e}")

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
        pdf_url=pdf_rel_path,
        measurement=measurement_data
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


@app.route("/stages")
def stages():
    """Lung Cancer Stage Explorer (Stage 0 to Stage IV) based on AJCC/UICC TNM classification."""
    all_stages = get_all_stages()
    return render_template("stages.html", stages=all_stages)


@app.route("/stages/<stage_id>")
def stage_detail(stage_id):
    """Direct deep link to a specific stage."""
    stage = get_stage_by_id(stage_id)
    if not stage:
        flash(f"Stage '{stage_id}' not found.", "warning")
        return redirect(url_for("stages"))
    return render_template("stages.html", stages=get_all_stages(), active_stage=stage_id)


@app.route("/measure", methods=["GET", "POST"])
def measure():
    """Tumor Size Estimation & Saliency Segmentation Studio."""
    measurement_result = None
    filename = request.args.get("image", "")
    pixel_scale_mm = float(request.form.get("pixel_scale_mm", request.args.get("scale", 0.7)))

    if request.method == "POST":
        if "file" in request.files and request.files["file"].filename != "":
            file = request.files["file"]
            if not allowed_file(file.filename):
                flash(f"Invalid file format. Allowed: {', '.join(Config.ALLOWED_EXTENSIONS)}", "danger")
                return redirect(url_for("measure"))
            unique_name = f"meas_{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            save_path = Config.UPLOAD_FOLDER / unique_name
            file.save(save_path)
            filename = unique_name
        else:
            filename = request.form.get("existing_image", "")

        if filename:
            img_path = Config.UPLOAD_FOLDER / filename
            if img_path.exists():
                try:
                    measurement_result = estimate_tumor_dimensions(
                        img_path,
                        pixel_scale_mm=pixel_scale_mm,
                        output_filename=f"seg_{uuid.uuid4().hex[:6]}_{Path(filename).stem}.jpg"
                    )
                except Exception as e:
                    flash(f"Segmentation error: {str(e)}", "danger")
            else:
                flash("Target image file not found on server.", "warning")
    elif filename:
        img_path = Config.UPLOAD_FOLDER / filename
        if img_path.exists():
            try:
                measurement_result = estimate_tumor_dimensions(
                    img_path,
                    pixel_scale_mm=pixel_scale_mm
                )
            except Exception as e:
                print(f"Auto-measure notice: {e}")

    return render_template(
        "measure.html",
        measurement=measurement_result,
        filename=filename,
        pixel_scale_mm=pixel_scale_mm
    )


@app.route("/api/measure", methods=["POST"])
def api_measure():
    """AJAX endpoint for real-time calibration scale recalculation."""
    data = request.get_json(silent=True) or {}
    filename = data.get("filename", "")
    pixel_scale_mm = float(data.get("pixel_scale_mm", 0.7))

    if not filename:
        return jsonify({"error": "No filename specified"}), 400

    img_path = Config.UPLOAD_FOLDER / filename
    if not img_path.exists():
        return jsonify({"error": "Image not found"}), 404

    try:
        res = estimate_tumor_dimensions(
            img_path,
            pixel_scale_mm=pixel_scale_mm,
            output_filename=f"seg_{Path(filename).stem}.jpg"
        )
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/lung3d")
def lung3d():
    """Interactive 3D Lung Anatomy & Tumor Localization Visualizer."""
    return render_template("lung3d.html")


@app.route("/types")
def cancer_types():
    """Lung Cancer Type Classification & Imaging Modality Knowledge Center."""
    types_data = get_all_cancer_types()
    modalities_data = get_imaging_modalities()
    return render_template(
        "cancer_types.html",
        cancer_types=types_data,
        modalities=modalities_data
    )


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


@app.route("/static/uploads/<path:filename>")
def custom_static_uploads(filename):
    """Serves uploaded slide images across local and serverless cloud environments."""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


@app.route("/static/heatmaps/<path:filename>")
def custom_static_heatmaps(filename):
    """Serves Grad-CAM heatmaps across local and serverless cloud environments."""
    return send_from_directory(Config.HEATMAP_FOLDER, filename)


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
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "=" * 50)
    print(" 🫁 LUNG-AI Flask Application Running")
    print(f" URL: http://0.0.0.0:{port}")
    print("=" * 50 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)
