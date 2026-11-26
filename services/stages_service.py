"""
LUNG-AI - Lung Cancer Stages (0–IV) Clinical & Educational Module
Provides authoritative staging criteria based on the AJCC / UICC TNM 8th & 9th Editions
for Non-Small Cell Lung Cancer (NSCLC: Adenocarcinoma & Squamous Cell Carcinoma).
"""

from typing import Dict, Any, List, Optional

STAGES_DATA: List[Dict[str, Any]] = [
    {
        "id": "stage-0",
        "stage_roman": "0",
        "name": "Stage 0",
        "subtitle": "Carcinoma in Situ (Hidden / Pre-invasive)",
        "one_liner": "Abnormal cells are limited to the lining of the airway.",
        "badge_class": "badge-stage-0",
        "badge_color": "#38bdf8",
        "tnm": {
            "t": "Tis (Carcinoma in situ)",
            "n": "N0 (No regional lymph node metastasis)",
            "m": "M0 (No distant metastasis)"
        },
        "description": (
            "In Stage 0 lung cancer, malignant or dysplastic cells are strictly confined to the innermost epithelial "
            "lining (mucosa) of the bronchus or airway. The tumor has not penetrated the basement membrane or invaded "
            "deeper into the lung parenchyma, lymph nodes, or adjacent organs."
        ),
        "tumor_size": "Microscopic; confined to the superficial airway lining without parenchymal invasion.",
        "lymph_nodes": "None (N0). No lymph node involvement.",
        "metastasis": "None (M0). Strictly localized.",
        "symptoms": [
            "Often completely asymptomatic",
            "Mild chronic dry cough or slight bronchial irritation",
            "Occasionally detected via routine sputum cytology or incidental bronchoscopy"
        ],
        "treatments": [
            "Conservative surgical resection (segmentectomy or wedge resection)",
            "Endobronchial therapies (photodynamic therapy, electrocautery, or cryotherapy)",
            "Active surveillance with high-resolution low-dose CT (LDCT)"
        ],
        "prognosis_5yr": "70% – 90% (curative potential if fully excised)",
        "key_takeaway": (
            "Stage 0 represents the earliest detectable neoplasm. Complete surgical resection or endobronchial ablation "
            "often results in complete cure before invasive transformation occurs."
        ),
        "illustration_title": "Carcinoma in Situ - Airway Lining Confined",
        "svg_accent": "#38bdf8"
    },
    {
        "id": "stage-1",
        "stage_roman": "I",
        "name": "Stage I",
        "subtitle": "Localized Invasive Pulmonary Cancer",
        "one_liner": "Cancer is limited to the lung without nearby lymph-node spread.",
        "badge_class": "badge-stage-1",
        "badge_color": "#10b981",
        "tnm": {
            "t": "T1a – T2a (Tumor ≤ 4 cm across)",
            "n": "N0 (No regional lymph node spread)",
            "m": "M0 (No distant metastasis)"
        },
        "description": (
            "In Stage I, an invasive malignant tumor has formed within the lung tissue but remains entirely isolated. "
            "It has not spread to any surrounding lymph nodes, pleura, chest wall, or distant anatomical locations. "
            "Stage I is subdivided into Stage IA (IA1: ≤1cm, IA2: 1-2cm, IA3: 2-3cm) and Stage IB (>3cm to ≤4cm)."
        ),
        "tumor_size": "Ranges from ≤ 1 cm (IA1) up to 4 cm (IB) in greatest diameter.",
        "lymph_nodes": "None (N0). Regional hilar, mediastinal, and supraclavicular nodes are clear.",
        "metastasis": "None (M0).",
        "symptoms": [
            "Persistent or worsening cough",
            "Mild shortness of breath upon routine physical exertion",
            "Localized dull chest discomfort",
            "Frequently identified incidentally on screening chest CT scans"
        ],
        "treatments": [
            "Surgical lobectomy or anatomical segmentectomy with lymph node dissection",
            "Stereotactic Body Radiation Therapy (SBRT / SABR) for medically inoperable candidates",
            "Adjuvant targeted therapy (e.g., Osimertinib for EGFR-mutated tumors in Stage IB)"
        ],
        "prognosis_5yr": "68% – 92% (Stage IA: ~80-92%, Stage IB: ~68%)",
        "key_takeaway": (
            "Early detection at Stage I provides the highest curative success rate. Surgical lobectomy is the standard "
            "of care, often achieving durable disease-free survival."
        ),
        "illustration_title": "Localized Nodule - Clear Lymph Nodes",
        "svg_accent": "#10b981"
    },
    {
        "id": "stage-2",
        "stage_roman": "II",
        "name": "Stage II",
        "subtitle": "Limited Regional Spread / Larger Primary",
        "one_liner": "Cancer may be larger or involve nearby lymph nodes or structures.",
        "badge_class": "badge-stage-2",
        "badge_color": "#f59e0b",
        "tnm": {
            "t": "T1b – T3 (Tumor up to 7 cm or invades chest wall/visceral pleura)",
            "n": "N0 – N1 (Spread to ipsilateral hilar/peribronchial lymph nodes)",
            "m": "M0 (No distant metastasis)"
        },
        "description": (
            "In Stage II, the cancer has progressed in size or begun to spread to nearby lymph nodes on the same side "
            "of the chest (ipsilateral hilar or peribronchial nodes). Alternatively, a larger tumor (>5 cm) without "
            "lymph node spread is also classified as Stage II. It is divided into Stage IIA and Stage IIB."
        ),
        "tumor_size": "Usually 3 cm to 7 cm, or smaller tumor with adjacent node invasion.",
        "lymph_nodes": "N1 (Ipsilateral peribronchial and/or hilar nodes) or N0 if tumor is larger (T3).",
        "metastasis": "None (M0).",
        "symptoms": [
            "Blood-streaked sputum or hemoptysis (coughing up blood)",
            "Frequent bouts of bronchitis, wheezing, or recurring pneumonia",
            "Deep chest ache or localized pleural pain that intensifies with deep breaths",
            "Noticeable unexplained weight loss and lethargy"
        ],
        "treatments": [
            "Comprehensive surgical resection (lobectomy or sleeve resection)",
            "Adjuvant platinum-based doublet chemotherapy (e.g., Cisplatin + Pemetrexed/Vinorelbine)",
            "Post-operative immunotherapy (e.g., Atezolizumab / Pembrolizumab) based on PD-L1 status",
            "Neoadjuvant chemo-immunotherapy prior to surgical intervention"
        ],
        "prognosis_5yr": "38% – 60% (Stage IIA: ~55-60%, Stage IIB: ~38-53%)",
        "key_takeaway": (
            "Stage II represents localized yet biologically aggressive disease. Multimodal therapy combining complete "
            "resection with systemic adjuvant therapy is vital to eliminate micro-metastatic seeds."
        ),
        "illustration_title": "Regional Node Spread - Ipsilateral Hilar Stations",
        "svg_accent": "#f59e0b"
    },
    {
        "id": "stage-3",
        "stage_roman": "III",
        "name": "Stage III",
        "subtitle": "Locally Advanced / Mediastinal Spread",
        "one_liner": "Cancer has spread more extensively within the chest.",
        "badge_class": "badge-stage-3",
        "badge_color": "#f97316",
        "tnm": {
            "t": "T1 – T4 (Invades mediastinum, heart, great vessels, trachea, or esophagus)",
            "n": "N1 – N3 (Spread to mediastinal, subcarinal, or contralateral/supraclavicular nodes)",
            "m": "M0 (No distant spread beyond thoracic cavity)"
        },
        "description": (
            "In Stage III (Locally Advanced), the cancer has spread extensively throughout thoracic structures. "
            "It commonly involves mediastinal lymph nodes (center of the chest), the carina, the trachea, the diaphragm, "
            "or lymph nodes on the opposite (contralateral) side of the neck/collarbone. Divided into IIIA, IIIB, and IIIC."
        ),
        "tumor_size": "Any size, frequently large (>7 cm) or multi-focal within the same pulmonary lobe.",
        "lymph_nodes": "N2 (Ipsilateral mediastinal/subcarinal) or N3 (Contralateral mediastinal or supraclavicular).",
        "metastasis": "None (M0). Extends widely within the thorax but not to distant organs.",
        "symptoms": [
            "Severe persistent chest, back, or shoulder pain",
            "Marked dyspnea (breathlessness even at rest)",
            "Hoarseness (due to recurrent laryngeal nerve compression)",
            "Difficulty swallowing (dysphagia due to esophageal compression)",
            "Superior Vena Cava (SVC) syndrome (facial and neck swelling)"
        ],
        "treatments": [
            "Definitive concurrent chemoradiation therapy (CRT)",
            "Consolidation immunotherapy with checkpoint inhibitors (e.g., Durvalumab for 12 months)",
            "Neoadjuvant chemo-immunotherapy followed by selective re-evaluation for radical surgery (Stage IIIA)",
            "Palliative radiation for airway obstruction and hemoptysis control"
        ],
        "prognosis_5yr": "13% – 36% (IIIA: ~36%, IIIB: ~26%, IIIC: ~13%)",
        "key_takeaway": (
            "Stage III is heterogeneous and complex, typically managed by a multidisciplinary tumor board (MDT). "
            "Consolidation immunotherapy has significantly improved long-term progression-free survival."
        ),
        "illustration_title": "Mediastinal & Subcarinal Nodal Infiltration",
        "svg_accent": "#f97316"
    },
    {
        "id": "stage-4",
        "stage_roman": "IV",
        "name": "Stage IV",
        "subtitle": "Advanced Metastatic / Distant Spread",
        "one_liner": "Cancer has spread to distant sites in the body.",
        "badge_class": "badge-stage-4",
        "badge_color": "#ef4444",
        "tnm": {
            "t": "Any T",
            "n": "Any N",
            "m": "M1a – M1c (Metastatic dissemination to distant organs)"
        },
        "description": (
            "Stage IV is advanced metastatic lung cancer. The primary tumor has disseminated via lymphatic or "
            "circulatory channels to the other lung, pleural or pericardial fluid, or distant organs including the "
            "brain, liver, bones, or adrenal glands. Subdivided into Stage IVA (oligometastatic) and Stage IVB (widespread)."
        ),
        "tumor_size": "Variable; primary tumor may range from small to massive with multi-organ dissemination.",
        "lymph_nodes": "Any N status (frequently extensive regional and distant nodal metastases).",
        "metastasis": "M1a (Malignant pleural/pericardial effusion or pleural nodules), M1b (Single distant metastasis), M1c (Multiple distant organ lesions).",
        "symptoms": [
            "Severe bone pain, fractures, or spinal cord compression",
            "Neurological symptoms: persistent headaches, seizures, visual changes, or motor deficits (brain metastases)",
            "Jaundice and abdominal pain (hepatic metastasis)",
            "Profound fatigue, cachexia (severe muscle and weight wasting), and malaise"
        ],
        "treatments": [
            "Precision molecular targeted therapies based on Next-Generation Sequencing (NGS) (EGFR, ALK, ROS1, BRAF, RET, MET, KRAS G12C inhibitors)",
            "Immune checkpoint inhibitor monotherapy or combination (Pembrolizumab, Nivolumab + Ipilimumab)",
            "Systemic chemotherapy (platinum doublets) for non-driver mutated cases",
            "Stereotactic Radiosurgery (Gamma Knife / CyberKnife) for brain metastases",
            "Palliative care for symptom relief, bone stabilization, and quality-of-life preservation"
        ],
        "prognosis_5yr": "6% – 10% (Significant improvements observed with targeted therapies: >30-50% in EGFR/ALK-positive cohorts)",
        "key_takeaway": (
            "Stage IV oncology has shifted from generalized chemotherapy to personalized precision medicine. "
            "Comprehensive genomic profiling (molecular biomarkers) enables highly targeted, long-term disease control."
        ),
        "illustration_title": "Distant Metastatic Dissemination (Brain, Bone, Liver)",
        "svg_accent": "#ef4444"
    }
]


def get_all_stages() -> List[Dict[str, Any]]:
    """Returns the complete list of lung cancer stages (0 to IV)."""
    return STAGES_DATA


def get_stage_by_id(stage_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves metadata for a specific stage by ID (e.g., 'stage-1')."""
    for stage in STAGES_DATA:
        if stage["id"] == stage_id or stage["stage_roman"].lower() == stage_id.lower():
            return stage
    return None


def get_staging_education_for_prediction(predicted_class: str) -> Dict[str, Any]:
    """
    Generates educational clinical correlation between the AI histopathological finding
    and clinical cancer staging (0–IV).
    """
    is_malignant = ("Adenocarcinoma" in predicted_class) or ("Squamous" in predicted_class)
    
    if not is_malignant:
        return {
            "applicable": False,
            "title": "Non-Neoplastic Finding: Staging Not Applicable",
            "summary": (
                f"The histopathological scan was classified as '{predicted_class}'. Clinical cancer staging (TNM Stage 0–IV) "
                "applies exclusively to malignant epithelial neoplasms. Benign pulmonary parenchyma shows preserved "
                "alveolar architecture with no malignant staging pathway indicated."
            ),
            "recommendation": "Maintain routine pulmonary screening and clinical wellness evaluations as directed by your physician."
        }
        
    subtype_name = "Lung Adenocarcinoma" if "Adenocarcinoma" in predicted_class else "Lung Squamous Cell Carcinoma"
    subtype_acronym = "LUAD" if "Adenocarcinoma" in predicted_class else "LUSC"

    return {
        "applicable": True,
        "subtype_name": subtype_name,
        "subtype_acronym": subtype_acronym,
        "title": f"Clinical Staging Correlation for {subtype_name}",
        "summary": (
            f"The deep learning model classified the biopsy as {subtype_name} (NSCLC). Under oncology clinical guidelines, "
            "once microscopic histopathology confirms the cancer subtype, oncologists proceed to determine the clinical stage (0–IV) "
            "to formulate the treatment plan."
        ),
        "pathway_steps": [
            {
                "step": "Step 1: Histopathological Subtyping (Completed by AI/Pathology)",
                "desc": f"Microscopic identification of cellular architecture: confirmed as {subtype_name}."
            },
            {
                "step": "Step 2: Anatomical Radiological Staging (CT & PET-CT Scans)",
                "desc": "High-resolution contrast-enhanced chest CT and whole-body 18F-FDG PET-CT scan to calculate primary tumor size (T) and assess metabolic uptake."
            },
            {
                "step": "Step 3: Regional Lymph Node Sampling (N)",
                "desc": "Endobronchial Ultrasound (EBUS) transbronchial needle aspiration or mediastinoscopy to evaluate hilar and mediastinal lymph nodes."
            },
            {
                "step": "Step 4: Distant Metastatic Screening (M)",
                "desc": "Contrast-enhanced brain MRI and whole-body scan to rule out distant dissemination to brain, bones, or liver."
            },
            {
                "step": "Step 5: Final TNM Stage Assignment (Stage 0 to IV)",
                "desc": "Integrated staging determines whether the patient qualifies for curative surgery (Stage I–II), chemoradiation (Stage III), or systemic precision therapy (Stage IV)."
            }
        ],
        "disclaimer": (
            "Important Academic Notice: Microscopic histopathology classifies cellular tissue morphology only. "
            "It cannot determine clinical cancer stage (0–IV) because tumor physical diameter and multi-organ dissemination "
            "require radiographic scans and lymph-node staging."
        )
    }

