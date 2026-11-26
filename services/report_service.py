from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from config import Config

try:
    from reportlab.lib import colors  # type: ignore
    from reportlab.lib.pagesizes import letter  # type: ignore
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # type: ignore
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage  # type: ignore
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_report(
    prediction_data: Dict[str, Any],
    original_image_path: Path,
    heatmap_image_path: Optional[Path] = None,
    case_id: Optional[str] = None
) -> str:
    """
    Generates a structured clinical and academic PDF report for a classification result.
    Returns relative path to the generated PDF.
    """
    Config.REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{case_id or timestamp_str}.pdf"
    pdf_full_path = Config.REPORT_FOLDER / report_filename

    if not REPORTLAB_AVAILABLE:
        # Fallback text/markdown report if reportlab is unavailable
        fallback_txt = pdf_full_path.with_suffix(".txt")
        with open(fallback_txt, "w", encoding="utf-8") as f:
            f.write(f"LUNG-AI CLINICAL DIAGNOSTIC REPORT\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Predicted Class: {prediction_data['predicted_class']}\n")
            f.write(f"Confidence: {prediction_data['confidence_percentage']}%\n")
            f.write(f"Model: {prediction_data['model_name']}\n\n")
            f.write(f"DISCLAIMER: {prediction_data.get('disclaimer', '')}\n")
        return f"reports/{fallback_txt.name}"

    doc = SimpleDocTemplate(
        str(pdf_full_path),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#081426"),
        alignment=1, # Center
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#4b6584"),
        alignment=1,
        spaceAfter=20
    )
    section_heading = ParagraphStyle(
        'SectionHead',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor("#081426"),
        spaceBefore=12,
        spaceAfter=6
    )
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Italic'],
        fontSize=8,
        textColor=colors.HexColor("#8492a6"),
        alignment=1,
        spaceBefore=15
    )

    story = []

    # Header
    story.append(Paragraph("LUNG-AI DIAGNOSTIC REPORT", title_style))
    story.append(Paragraph("Explainable Deep Learning Lung Histopathology Classification | MCA Project 2026-2027", subtitle_style))
    story.append(Spacer(1, 10))

    # Case Details Table
    conf_display = f"{prediction_data.get('confidence_percentage', 0)}%"
    if prediction_data.get("uncertain"):
        conf_display += " [HIGH UNCERTAINTY <60%]"

    case_info = [
        ["Report ID:", f"LUNG-{case_id or timestamp_str}", "Analysis Date:", datetime.now().strftime("%d %B %Y, %H:%M")],
        ["Model Evaluated:", prediction_data.get("model_name", "CNN"), "Inference Latency:", f"{prediction_data.get('inference_latency_ms', 0)} ms"],
        ["Primary Finding:", prediction_data.get("predicted_class", "N/A"), "Confidence Level:", conf_display]
    ]
    t_info = Table(case_info, colWidths=[110, 150, 110, 150])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#1e293b")),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 15))

    # Image & Heatmap Section
    story.append(Paragraph("Microscopic Histopathology & Grad-CAM Visual Explanation", section_heading))
    
    images_row = []
    if original_image_path.exists():
        images_row.append(RLImage(str(original_image_path), width=200, height=200))
    else:
        images_row.append(Paragraph("Original Scan", styles['Normal']))

    if heatmap_image_path and heatmap_image_path.exists():
        images_row.append(RLImage(str(heatmap_image_path), width=200, height=200))
    else:
        images_row.append(Paragraph("Grad-CAM Heatmap", styles['Normal']))

    t_imgs = Table([[images_row[0], images_row[1]], ["Original Tissue Sample", "Grad-CAM Saliency Overlay"]], colWidths=[260, 260])
    t_imgs.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Oblique'),
        ('FONTSIZE', (0,1), (-1,1), 9),
        ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor("#4b6584")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_imgs)
    story.append(Spacer(1, 15))

    # Class Probabilities Breakdown
    story.append(Paragraph("Detailed Multi-Class Probability Distribution", section_heading))
    prob_table_data = [["Subtype Category", "Score (Normalized)", "Confidence Percentage"]]
    for c_name, score in prediction_data.get("class_probabilities", {}).items():
        is_winner = c_name == prediction_data.get("predicted_class")
        prefix = "★ " if is_winner else ""
        prob_table_data.append([
            f"{prefix}{c_name}",
            f"{score:.4f}",
            f"{score * 100:.2f}%"
        ])
    t_probs = Table(prob_table_data, colWidths=[240, 140, 140])
    t_probs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#081426")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_probs)
    story.append(Spacer(1, 15))

    # Clinical Staging Correlation Note
    staging_note = (
        "<b>Clinical Oncology Staging Context (Stage 0–IV):</b> Histopathological subtyping establishes the "
        "cellular classification (NSCLC Adenocarcinoma, Squamous Cell, or Benign). Definitive clinical cancer staging "
        "(Stage 0–IV) requires radiographic anatomical correlation (Contrast Chest CT, 18F-FDG PET-CT, Brain MRI) and TNM evaluation "
        "by a certified oncology tumor board."
    )
    story.append(Paragraph(staging_note, styles['Normal']))
    story.append(Spacer(1, 15))

    # Academic Disclaimer
    disclaimer_text = (
        "ACADEMIC & RESEARCH DISCLAIMER: LUNG-AI is an experimental academic prototype developed for Master of Computer Applications (MCA) study. "
        "The automated outputs, probability distributions, and Grad-CAM activations are not certified medical diagnoses and must not be used to replace "
        "pathologist histological examinations or clinical decision-making."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(story)
    return f"reports/{report_filename}"

