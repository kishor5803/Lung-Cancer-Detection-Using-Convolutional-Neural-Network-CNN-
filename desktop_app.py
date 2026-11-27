"""
LUNGCARE AI / LUNG-AI — Native Windows Desktop Workstation
Provides offline CNN histopathology classification, Grad-CAM explainability,
calibrated tumor morphometry/segmentation, Cancer Stages (0-IV) Explorer,
Cancer Types reference, and one-click WebGL 3D Lung launcher.
"""

import os
import sys
import threading
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Ensure local imports work regardless of launch working directory
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import Config
from services.measurement_service import estimate_tumor_dimensions
from services.stages_service import get_all_stages
from services.cancer_types_service import get_all_cancer_types, get_imaging_modalities
from prediction.predict import predict_single_image


# Color Palette (Dark Medical Workstation)
BG_DARK = "#0b1120"
BG_PANEL = "#111827"
BG_CARD = "#1e293b"
BORDER_CLR = "#334155"
TEXT_PRIMARY = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_GOLD = "#d9b968"
ACCENT_CYAN = "#38bdf8"
ACCENT_GREEN = "#10b981"
ACCENT_RED = "#ef4444"


class LungCareDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LUNGCARE AI — Desktop Diagnostic & Oncology Workstation")
        self.geometry("1260x800")
        self.minsize(1040, 680)
        self.configure(bg=BG_DARK)

        # State
        self.current_image_path: Path | None = None
        self.last_prediction = None
        self.last_measurement = None
        self.photo_refs = []  # Keep references to avoid GC

        self._setup_styles()
        self._build_layout()
        self.show_frame("classify")

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=BG_CARD, background=BG_CARD,
                        foreground=TEXT_PRIMARY, bordercolor=BORDER_CLR)

    def _build_layout(self):
        # Top Header Bar
        header = tk.Frame(self, bg=BG_PANEL, height=58, highlightthickness=1, highlightbackground=BORDER_CLR)
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="🫁 LUNGCARE AI", font=("Segoe UI", 15, "bold"),
            fg=ACCENT_GOLD, bg=BG_PANEL
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header, text="CNN-Based Lung Cancer Analysis, Morphometry & Oncology Workstation",
            font=("Segoe UI", 10), fg=TEXT_MUTED, bg=BG_PANEL
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            header, text="🌐 Open 3D Lung Model (Web)", command=lambda: self._open_web("/lung3d"),
            bg="#0f2942", fg=ACCENT_CYAN, relief=tk.FLAT, font=("Segoe UI", 9, "bold"),
            padx=12, pady=6, cursor="hand2"
        ).pack(side=tk.RIGHT, padx=16)

        # Main Body Container
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar Navigation
        sidebar = tk.Frame(body, bg=BG_PANEL, width=230, highlightthickness=1, highlightbackground=BORDER_CLR)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="MODULES", font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED, bg=BG_PANEL
        ).pack(anchor="w", padx=18, pady=(18, 8))

        self.nav_buttons = {}
        nav_items = [
            ("classify", "🔬  CNN AI Analysis"),
            ("measure",  "📐  Tumor Measurement"),
            ("stages",   "📊  Stage Explorer (0–IV)"),
            ("types",    "🧬  Cancer Types Guide"),
            ("lung3d",   "🫁  3D Lung & Web Tools"),
        ]
        for key, label in nav_items:
            btn = tk.Button(
                sidebar, text=label, anchor="w", font=("Segoe UI", 10, "bold"),
                bg=BG_PANEL, fg=TEXT_PRIMARY, relief=tk.FLAT, padx=16, pady=11,
                cursor="hand2", command=lambda k=key: self.show_frame(k)
            )
            btn.pack(fill=tk.X, padx=8, pady=3)
            self.nav_buttons[key] = btn

        # Disclaimer Footer in Sidebar
        disc_frame = tk.Frame(sidebar, bg=BG_CARD, padx=10, pady=10, highlightthickness=1, highlightbackground=BORDER_CLR)
        disc_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=12)
        tk.Label(
            disc_frame,
            text="⚠️ Academic Prototype\nNot for standalone clinical diagnosis or staging.",
            font=("Segoe UI", 8), fg="#fbbf24", bg=BG_CARD, justify=tk.LEFT, wraplength=185
        ).pack(anchor="w")

        # Content Stack
        self.content_area = tk.Frame(body, bg=BG_DARK)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=18, pady=16)

        self.frames = {}
        self._build_classify_frame()
        self._build_measure_frame()
        self._build_stages_frame()
        self._build_types_frame()
        self._build_3d_frame()

    def show_frame(self, key: str):
        for k, f in self.frames.items():
            f.pack_forget()
            self.nav_buttons[k].configure(bg=BG_PANEL, fg=TEXT_PRIMARY)

        self.frames[key].pack(fill=tk.BOTH, expand=True)
        self.nav_buttons[key].configure(bg="#1e293b", fg=ACCENT_GOLD)

    # ------------------------------------------------------------------
    # TAB 1: CNN AI ANALYSIS & GRAD-CAM
    # ------------------------------------------------------------------
    def _build_classify_frame(self):
        frame = tk.Frame(self.content_area, bg=BG_DARK)
        self.frames["classify"] = frame

        # Top Control Bar
        ctrl = tk.Frame(frame, bg=BG_CARD, padx=16, pady=12, highlightthickness=1, highlightbackground=BORDER_CLR)
        ctrl.pack(fill=tk.X, pady=(0, 14))

        tk.Button(
            ctrl, text="📂 Load Medical Scan (PNG/JPG)", command=self._pick_image,
            bg=ACCENT_CYAN, fg="#081426", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, padx=14, pady=7, cursor="hand2"
        ).pack(side=tk.LEFT)

        tk.Label(ctrl, text="Model:", bg=BG_CARD, fg=TEXT_MUTED, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(18, 6))
        self.model_var = tk.StringVar(value="custom_cnn")
        model_cb = ttk.Combobox(
            ctrl, textvariable=self.model_var, state="readonly", width=18,
            values=["custom_cnn", "mobilenetv2", "resnet50"]
        )
        model_cb.pack(side=tk.LEFT)

        self.btn_run_ai = tk.Button(
            ctrl, text="⚡ Run CNN Classification & Grad-CAM", command=self._run_classification,
            bg=ACCENT_GOLD, fg="#081426", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, padx=16, pady=7, cursor="hand2"
        )
        self.btn_run_ai.pack(side=tk.RIGHT)

        self.lbl_file_status = tk.Label(
            frame, text="No scan loaded. Select a lung histopathology tile or scan image to begin.",
            bg=BG_DARK, fg=TEXT_MUTED, font=("Segoe UI", 9)
        )
        self.lbl_file_status.pack(anchor="w", pady=(0, 10))

        # Result Banner
        self.res_banner = tk.Frame(frame, bg=BG_CARD, padx=16, pady=12, highlightthickness=1, highlightbackground=BORDER_CLR)
        self.res_banner.pack(fill=tk.X, pady=(0, 14))

        self.lbl_pred_class = tk.Label(self.res_banner, text="Prediction: —", font=("Segoe UI", 14, "bold"), fg=ACCENT_GOLD, bg=BG_CARD)
        self.lbl_pred_class.pack(side=tk.LEFT)

        self.lbl_pred_conf = tk.Label(self.res_banner, text="Confidence: —  |  Risk: —", font=("Segoe UI", 11), fg=TEXT_PRIMARY, bg=BG_CARD)
        self.lbl_pred_conf.pack(side=tk.RIGHT)

        # Side-by-Side Image Panels
        img_row = tk.Frame(frame, bg=BG_DARK)
        img_row.pack(fill=tk.BOTH, expand=True)

        left_box = tk.Frame(img_row, bg=BG_CARD, padx=12, pady=12, highlightthickness=1, highlightbackground=BORDER_CLR)
        left_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        tk.Label(left_box, text="Original Input Image", font=("Segoe UI", 10, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD).pack(pady=(0, 8))
        self.lbl_orig_img = tk.Label(left_box, text="Image Preview", bg="#0f172a", fg=TEXT_MUTED)
        self.lbl_orig_img.pack(fill=tk.BOTH, expand=True)

        right_box = tk.Frame(img_row, bg=BG_CARD, padx=12, pady=12, highlightthickness=1, highlightbackground=BORDER_CLR)
        right_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))
        tk.Label(right_box, text="Grad-CAM Explainability Heatmap", font=("Segoe UI", 10, "bold"), fg=ACCENT_CYAN, bg=BG_CARD).pack(pady=(0, 8))
        self.lbl_cam_img = tk.Label(right_box, text="Grad-CAM Overlay", bg="#0f172a", fg=TEXT_MUTED)
        self.lbl_cam_img.pack(fill=tk.BOTH, expand=True)

    def _pick_image(self):
        path_str = filedialog.askopenfilename(
            title="Select Lung Scan / Histopathology Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif")]
        )
        if not path_str:
            return
        self.current_image_path = Path(path_str)
        self.lbl_file_status.configure(text=f"Loaded File: {self.current_image_path}")
        self._display_image_on_label(self.current_image_path, self.lbl_orig_img, (440, 380))
        self._display_image_on_label(self.current_image_path, self.lbl_meas_orig, (420, 340))

    def _display_image_on_label(self, img_path: Path, label_widget: tk.Label, max_size=(420, 360)):
        try:
            pil_img = Image.open(img_path)
            pil_img.thumbnail(max_size, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(pil_img)
            self.photo_refs.append(tk_img)
            label_widget.configure(image=tk_img, text="")
        except Exception as e:
            label_widget.configure(text=f"Preview Error: {e}", image="")

    def _run_classification(self):
        if not self.current_image_path or not self.current_image_path.exists():
            messagebox.showwarning("No Scan Loaded", "Please load a scan image first.")
            return

        self.btn_run_ai.configure(state=tk.DISABLED, text="Analyzing...")
        model_key = self.model_var.get()

        def worker():
            try:
                res = predict_single_image(self.current_image_path, model_key=model_key, generate_cam=True)
                self.after(0, lambda: self._on_classification_done(res))
            except Exception as err:
                self.after(0, lambda: messagebox.showerror("Inference Error", str(err)))
            finally:
                self.after(0, lambda: self.btn_run_ai.configure(state=tk.NORMAL, text="⚡ Run CNN Classification & Grad-CAM"))

        threading.Thread(target=worker, daemon=True).start()

    def _on_classification_done(self, res: dict):
        self.last_prediction = res
        pred_cls = res.get("predicted_class", "Unknown")
        conf = res.get("confidence_percentage", 0)
        risk = res.get("class_metadata", {}).get("risk_level", "N/A")

        self.lbl_pred_class.configure(text=f"Prediction: {pred_cls}")
        self.lbl_pred_conf.configure(text=f"Confidence: {conf}%  |  Risk: {risk}")

        heatmap_url = res.get("heatmap_url")
        if heatmap_url:
            cam_path = Config.HEATMAP_FOLDER / Path(heatmap_url).name
            if cam_path.exists():
                self._display_image_on_label(cam_path, self.lbl_cam_img, (440, 380))

    # ------------------------------------------------------------------
    # TAB 2: TUMOR SIZE ESTIMATION & SEGMENTATION
    # ------------------------------------------------------------------
    def _build_measure_frame(self):
        frame = tk.Frame(self.content_area, bg=BG_DARK)
        self.frames["measure"] = frame

        ctrl = tk.Frame(frame, bg=BG_CARD, padx=16, pady=12, highlightthickness=1, highlightbackground=BORDER_CLR)
        ctrl.pack(fill=tk.X, pady=(0, 12))

        tk.Label(ctrl, text="Spatial Scale (mm/px):", bg=BG_CARD, fg=TEXT_MUTED, font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.scale_var = tk.StringVar(value="0.70")
        scale_cb = ttk.Combobox(
            ctrl, textvariable=self.scale_var, width=22,
            values=["0.70", "0.50", "0.0005", "0.00025"]
        )
        scale_cb.pack(side=tk.LEFT, padx=8)

        tk.Label(ctrl, text="(0.70 = LDCT | 0.0005 = 20x H&E)", bg=BG_CARD, fg=TEXT_MUTED, font=("Segoe UI", 8)).pack(side=tk.LEFT)

        tk.Button(
            ctrl, text="📐 Segment & Measure Tumor", command=self._run_measurement,
            bg=ACCENT_CYAN, fg="#081426", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, padx=14, pady=6, cursor="hand2"
        ).pack(side=tk.RIGHT)

        # KPI Tiles Row
        kpi_row = tk.Frame(frame, bg=BG_DARK)
        kpi_row.pack(fill=tk.X, pady=(0, 12))

        self.kpi_labels = {}
        kpis = [
            ("dmax", "Max Diameter (D_max)", "— mm", ACCENT_GOLD),
            ("area", "Lesion Area", "— mm²", ACCENT_CYAN),
            ("compact", "Compactness Index", "—", TEXT_PRIMARY),
            ("tstage", "T-Size Bracket (CT)", "—", "#f59e0b"),
        ]
        for key, title, default, clr in kpis:
            box = tk.Frame(kpi_row, bg=BG_CARD, padx=14, pady=10, highlightthickness=1, highlightbackground=BORDER_CLR)
            box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
            tk.Label(box, text=title, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")
            lbl = tk.Label(box, text=default, font=("Segoe UI", 13, "bold"), fg=clr, bg=BG_CARD)
            lbl.pack(anchor="w", pady=(2, 0))
            self.kpi_labels[key] = lbl

        # Images Row
        img_row = tk.Frame(frame, bg=BG_DARK)
        img_row.pack(fill=tk.BOTH, expand=True)

        left_box = tk.Frame(img_row, bg=BG_CARD, padx=12, pady=12, highlightthickness=1, highlightbackground=BORDER_CLR)
        left_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        tk.Label(left_box, text="Input Scan", font=("Segoe UI", 10, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD).pack(pady=(0, 6))
        self.lbl_meas_orig = tk.Label(left_box, text="Load a scan in CNN Analysis tab", bg="#0f172a", fg=TEXT_MUTED)
        self.lbl_meas_orig.pack(fill=tk.BOTH, expand=True)

        right_box = tk.Frame(img_row, bg=BG_CARD, padx=12, pady=12, highlightthickness=1, highlightbackground=BORDER_CLR)
        right_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))
        tk.Label(right_box, text="Segmented Tumor Contour & Diameter Axis", font=("Segoe UI", 10, "bold"), fg=ACCENT_GOLD, bg=BG_CARD).pack(pady=(0, 6))
        self.lbl_meas_seg = tk.Label(right_box, text="Run segmentation to view contour", bg="#0f172a", fg=TEXT_MUTED)
        self.lbl_meas_seg.pack(fill=tk.BOTH, expand=True)

    def _run_measurement(self):
        if not self.current_image_path or not self.current_image_path.exists():
            messagebox.showwarning("No Scan Loaded", "Please load a scan image in the CNN AI Analysis tab first.")
            return
        try:
            scale = float(self.scale_var.get())
        except ValueError:
            messagebox.showerror("Invalid Scale", "Please enter a valid numeric mm/pixel scale.")
            return

        res = estimate_tumor_dimensions(self.current_image_path, pixel_scale_mm=scale)
        self.last_measurement = res
        self.kpi_labels["dmax"].configure(text=f"{res['max_diameter_mm']} mm")
        self.kpi_labels["area"].configure(text=f"{res['area_mm2']} mm²")
        self.kpi_labels["compact"].configure(text=f"{res['compactness_index']} ({res['margin_profile'].split()[0]})")
        self.kpi_labels["tstage"].configure(text=res["tnm_t_estimate"])

        seg_url = res.get("segmentation_image_url")
        if seg_url:
            seg_path = Config.HEATMAP_FOLDER / Path(seg_url).name
            if seg_path.exists():
                self._display_image_on_label(seg_path, self.lbl_meas_seg, (420, 340))

    # ------------------------------------------------------------------
    # TAB 3: CANCER STAGES EXPLORER (STAGE 0 - IV)
    # ------------------------------------------------------------------
    def _build_stages_frame(self):
        frame = tk.Frame(self.content_area, bg=BG_DARK)
        self.frames["stages"] = frame

        tk.Label(
            frame, text="Lung Cancer Stages Explorer (AJCC TNM 8th Edition)",
            font=("Segoe UI", 15, "bold"), fg=ACCENT_GOLD, bg=BG_DARK
        ).pack(anchor="w", pady=(0, 4))
        tk.Label(
            frame, text="Educational guide only. Clinical staging cannot be determined from a single image without CT/PET/Biopsy.",
            font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_DARK
        ).pack(anchor="w", pady=(0, 12))

        stages = get_all_stages()

        btn_bar = tk.Frame(frame, bg=BG_DARK)
        btn_bar.pack(fill=tk.X, pady=(0, 12))

        self.stage_detail_text = tk.Text(
            frame, bg=BG_CARD, fg=TEXT_PRIMARY, font=("Segoe UI", 10),
            padx=18, pady=16, wrap=tk.WORD, relief=tk.FLAT, highlightthickness=1, highlightbackground=BORDER_CLR
        )

        def show_stage(st):
            self.stage_detail_text.configure(state=tk.NORMAL)
            self.stage_detail_text.delete("1.0", tk.END)
            content = (
                f"{st['stage_label']} — {st['short_title']}\n"
                f"TNM Code: {st['tnm_code']}   |   5-Year Relative Survival: {st['survival_5yr']}\n"
                + "=" * 75 + "\n\n"
                f"OVERVIEW:\n{st['clinical_description']}\n\n"
                f"TUMOR & SPREAD CHARACTERISTICS:\n"
                f"• Tumor Size / Extent: {st['tumor_size']}\n"
                f"• Lymph Node Involvement: {st['lymph_nodes']}\n"
                f"• Distant Metastasis: {st['metastasis']}\n\n"
                f"COMMON SYMPTOMS:\n• " + "\n• ".join(st["symptoms"]) + "\n\n"
                f"TYPICAL CLINICAL MANAGEMENT:\n• " + "\n• ".join(st["treatment_overview"])
            )
            self.stage_detail_text.insert(tk.END, content)
            self.stage_detail_text.configure(state=tk.DISABLED)

        for st in stages:
            b = tk.Button(
                btn_bar, text=st["stage_label"], command=lambda s=st: show_stage(s),
                bg=BG_CARD, fg=ACCENT_CYAN, font=("Segoe UI", 10, "bold"),
                relief=tk.FLAT, padx=16, pady=8, cursor="hand2"
            )
            b.pack(side=tk.LEFT, padx=(0, 8))

        self.stage_detail_text.pack(fill=tk.BOTH, expand=True)
        if stages:
            show_stage(stages[0])

    # ------------------------------------------------------------------
    # TAB 4: CANCER TYPES & MODALITIES GUIDE
    # ------------------------------------------------------------------
    def _build_types_frame(self):
        frame = tk.Frame(self.content_area, bg=BG_DARK)
        self.frames["types"] = frame

        tk.Label(
            frame, text="Lung Cancer Subtypes & Diagnostic Modalities",
            font=("Segoe UI", 15, "bold"), fg=ACCENT_GOLD, bg=BG_DARK
        ).pack(anchor="w", pady=(0, 10))

        text_box = tk.Text(
            frame, bg=BG_CARD, fg=TEXT_PRIMARY, font=("Segoe UI", 10),
            padx=18, pady=16, wrap=tk.WORD, relief=tk.FLAT, highlightthickness=1, highlightbackground=BORDER_CLR
        )
        text_box.pack(fill=tk.BOTH, expand=True)

        lines = ["HISTOLOGICAL SUBTYPES (NSCLC, SCLC & BENIGN)\n" + "=" * 72 + "\n"]
        for ct in get_all_cancer_types():
            lines.append(
                f"\n▶ {ct['name']} ({ct['broad_category']}) — Incidence: {ct['frequency_percentage']}\n"
                f"  • Location: {ct['primary_location']}\n"
                f"  • Histopathology: {ct['histopathology']['cellular_architecture']}\n"
                f"  • Immunohistochemistry: {ct['histopathology']['immunohistochemistry']}\n"
                f"  • LDCT Presentation: {ct['radiology_presentation']['ldct_appearance']}\n"
                f"  • Interventions: {ct['preferred_interventions']}\n"
            )

        lines.append("\n\nIMAGING MODALITIES COMPARISON\n" + "=" * 72 + "\n")
        for mod in get_imaging_modalities():
            lines.append(
                f"\n▶ {mod['modality']} ({mod['category']})\n"
                f"  • Resolution: {mod['spatial_resolution']} | Dose: {mod['radiation_dose']}\n"
                f"  • Clinical Role: {mod['primary_clinical_role']}\n"
            )

        text_box.insert(tk.END, "\n".join(lines))
        text_box.configure(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # TAB 5: 3D LUNG & WEB TOOLS LAUNCHER
    # ------------------------------------------------------------------
    def _build_3d_frame(self):
        frame = tk.Frame(self.content_area, bg=BG_DARK)
        self.frames["lung3d"] = frame

        card = tk.Frame(frame, bg=BG_CARD, padx=28, pady=28, highlightthickness=1, highlightbackground=BORDER_CLR)
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            card, text="🫁 Interactive 3D Lung Anatomy & Web Suite",
            font=("Segoe UI", 16, "bold"), fg=ACCENT_GOLD, bg=BG_CARD
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            card,
            text="Launch the hardware-accelerated WebGL 3D Lung Visualization and full web platform in your default browser.",
            font=("Segoe UI", 10), fg=TEXT_MUTED, bg=BG_CARD
        ).pack(anchor="w", pady=(0, 20))

        links = [
            ("🫁  Open Interactive 3D Lung Model (WebGL)", "/lung3d", ACCENT_GREEN),
            ("📐  Open Web Tumor Measurement Studio", "/measure", ACCENT_CYAN),
            ("📊  Open Web Cancer Stages Explorer", "/stages", ACCENT_GOLD),
            ("🧬  Open Cancer Types & Modalities Guide", "/types", "#c084fc"),
            ("⚡  Open CNN Model Comparison Dashboard", "/dashboard", "#f59e0b"),
        ]
        for label, route, color in links:
            tk.Button(
                card, text=label, command=lambda r=route: self._open_web(r),
                bg="#0f172a", fg=color, font=("Segoe UI", 11, "bold"),
                relief=tk.FLAT, padx=18, pady=12, anchor="w", cursor="hand2",
                highlightthickness=1, highlightbackground=BORDER_CLR
            ).pack(fill=tk.X, pady=6)

    def _open_web(self, route: str):
        webbrowser.open(f"http://127.0.0.1:5000{route}")


if __name__ == "__main__":
    app = LungCareDesktopApp()
    app.mainloop()

