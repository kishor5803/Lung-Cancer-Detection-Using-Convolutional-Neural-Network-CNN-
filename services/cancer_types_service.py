"""
LUNG-AI - Cancer Types & Diagnostic Modality Knowledge Service
Authoritative oncology knowledge base covering major histological classifications,
molecular biomarkers, and comparative radiological/histopathological imaging modalities.
"""

from typing import List, Dict, Any


def get_all_cancer_types() -> List[Dict[str, Any]]:
    """Returns detailed medical profiles of primary pulmonary neoplasm subtypes."""
    return [
        {
            "id": "adenocarcinoma",
            "name": "Lung Adenocarcinoma (LUAD)",
            "broad_category": "Non-Small Cell Lung Cancer (NSCLC)",
            "frequency_percentage": "40%",
            "primary_location": "Peripheral Lung Parenchyma (Subpleural)",
            "smoking_association": "Moderate (Most common type in non-smokers and women)",
            "key_color": "#d9b968",
            "histopathology": {
                "cellular_architecture": "Glandular, acinar, papillary, micropapillary, or solid patterns with mucin production.",
                "cytological_features": "Enlarged hyperchromatic nuclei, prominent nucleoli, abundant cytoplasm, signet-ring cells.",
                "immunohistochemistry": "TTF-1 (Thyroid Transcription Factor-1) positive (+), Napsin A positive (+), Cytokeratin 7 (+), p40 negative (-)."
            },
            "radiology_presentation": {
                "ldct_appearance": "Peripheral solitary pulmonary nodule, ground-glass opacity (GGO), or part-solid subpleural nodule with pleural retraction.",
                "lung_rads_category": "Lung-RADS 3 or 4 depending on solid component diameter and growth velocity.",
                "hounsfield_units": "-300 to +40 HU (mixed ground-glass to solid soft tissue density)."
            },
            "molecular_biomarkers": [
                {"gene": "EGFR", "frequency": "15-50%", "targeted_therapy": "Osimertinib, Gefitinib, Erlotinib (TKIs)"},
                {"gene": "KRAS (G12C)", "frequency": "25-30%", "targeted_therapy": "Sotorasib, Adagrasib"},
                {"gene": "ALK Translocation", "frequency": "5-7%", "targeted_therapy": "Alectinib, Brigatinib, Lorlatinib"},
                {"gene": "ROS1 Fusion", "frequency": "1-2%", "targeted_therapy": "Crizotinib, Entrectinib"},
                {"gene": "PD-L1", "frequency": "Variable", "targeted_therapy": "Pembrolizumab, Nivolumab (Checkpoint Inhibitors)"}
            ],
            "clinical_course": "Often asymptomatic in early stages. Later manifests with persistent dry cough, shortness of breath, pleuritic chest pain. Frequently metastasizes to bone, brain, adrenal glands, and liver.",
            "preferred_interventions": "Stage I-II: Video-Assisted Thoracoscopic (VATS) Lobectomy + Lymphadenectomy. Stage III: Chemo-immunotherapy + Radiotherapy. Stage IV: Targeted kinase inhibitors or immune checkpoint therapy based on molecular sequencing."
        },
        {
            "id": "squamous_cell",
            "name": "Squamous Cell Carcinoma (LUSC)",
            "broad_category": "Non-Small Cell Lung Cancer (NSCLC)",
            "frequency_percentage": "25–30%",
            "primary_location": "Central Endobronchial (Hilar / Main Bronchi)",
            "smoking_association": "Very Strong (>90% of cases correlated with cigarette smoking)",
            "key_color": "#38bdf8",
            "histopathology": {
                "cellular_architecture": "Concentric keratin pearls (whorls), intercellular bridging (desmosomes), sheets of polygonal cells.",
                "cytological_features": "Dense eosinophilic (pink) cytoplasm, hyperchromatic angulated pyknotic nuclei, extensive central necrosis.",
                "immunohistochemistry": "p40 positive (+), p63 positive (+), Cytokeratin 5/6 (+), TTF-1 negative (-), Napsin A negative (-)."
            },
            "radiology_presentation": {
                "ldct_appearance": "Centrally located hilar mass causing bronchial obstruction, post-obstructive atelectasis, or central cavitation with thick irregular walls.",
                "lung_rads_category": "Lung-RADS 4A or 4B (endobronchial component or rapid doubling time).",
                "hounsfield_units": "+35 to +60 HU (solid soft tissue with central low-density fluid attenuation in necrosis)."
            },
            "molecular_biomarkers": [
                {"gene": "FGFR1 Amplification", "frequency": "15-20%", "targeted_therapy": "Investigational FGFR inhibitors"},
                {"gene": "PIK3CA Mutation", "frequency": "10-15%", "targeted_therapy": "PI3K pathway inhibitors"},
                {"gene": "DDR2 Mutation", "frequency": "3-5%", "targeted_therapy": "Dasatinib"},
                {"gene": "PD-L1 Expression", "frequency": "40-60%", "targeted_therapy": "Pembrolizumab, Cemiplimab"}
            ],
            "clinical_course": "Early symptoms include hemoptysis (coughing blood), atelectasis, wheezing, and recurrent post-obstructive pneumonia due to bronchial airway stenosis. May cause hypercalcemia via ectopic PTHrP secretion.",
            "preferred_interventions": "Stage I-II: Sleeve lobectomy or pneumonectomy. Central location requires careful bronchial margin assessment. Systemic: Platinum-doublet chemotherapy (Cisplatin + Gemcitabine) combined with PD-1/PD-L1 immunotherapy."
        },
        {
            "id": "large_cell",
            "name": "Large Cell Carcinoma (LCC)",
            "broad_category": "Non-Small Cell Lung Cancer (NSCLC)",
            "frequency_percentage": "10–15%",
            "primary_location": "Mid-to-Peripheral Lung Parenchyma",
            "smoking_association": "Strongly Associated with Heavy Smoking",
            "key_color": "#a855f7",
            "histopathology": {
                "cellular_architecture": "Undifferentiated sheets and syncytia lacking definitive squamous or glandular differentiation by light microscopy.",
                "cytological_features": "Large polygonal cells, abundant cytoplasm, vesicular nuclei with prominent macronucleoli, frequent atypical mitoses.",
                "immunohistochemistry": "Diagnosis of exclusion; often null or weakly focal for lineage markers. Requires extensive panel to rule out lymphoma, melanoma, and sarcomatoid carcinoma."
            },
            "radiology_presentation": {
                "ldct_appearance": "Large, bulky, well-circumscribed peripheral soft-tissue mass, often measuring >4 cm at initial presentation, with frequent areas of internal low attenuation (necrosis).",
                "lung_rads_category": "Lung-RADS 4X (high suspicion of aggressive malignancy).",
                "hounsfield_units": "+30 to +50 HU with heterogenous enhancement."
            },
            "molecular_biomarkers": [
                {"gene": "TP53 Inactivation", "frequency": "60-70%", "targeted_therapy": "Supportive / Chemo combination"},
                {"gene": "RB1 Mutation", "frequency": "20-30%", "targeted_therapy": "Cell-cycle checkpoints"},
                {"gene": "PD-L1 High Expression", "frequency": "30-50%", "targeted_therapy": "Atezolizumab, Pembrolizumab"}
            ],
            "clinical_course": "Aggressive natural history with high proliferative rate (Ki-67 >50%). Early vascular invasion leads to widespread hematogenous metastasis to liver, brain, and bones before primary symptoms manifest.",
            "preferred_interventions": "Surgical resection only if detected in localized Stage I-II (uncommon). Usually requires multi-modal systemic chemotherapy and immunotherapy with stereotactic ablative radiotherapy."
        },
        {
            "id": "small_cell",
            "name": "Small Cell Lung Carcinoma (SCLC)",
            "broad_category": "Neuroendocrine Carcinoma (High-Grade)",
            "frequency_percentage": "13–15%",
            "primary_location": "Central Hilar / Mediastinal Infiltration",
            "smoking_association": "Extremely High (>98% history of heavy tobacco use)",
            "key_color": "#ef4444",
            "histopathology": {
                "cellular_architecture": "Sheets, clusters, and cords of small cells with scant cytoplasm; nuclear molding and Azzopardi effect (DNA incrustation in vessels).",
                "cytological_features": "Cells roughly 1.5–2x size of mature lymphocyte, salt-and-pepper chromatin, absent or inconspicuous nucleoli, very high mitotic rate (>10 mitoses/2 mm²).",
                "immunohistochemistry": "Synaptophysin (+), Chromogranin A (+), CD56 (+), INSM1 (+), Ki-67 index >80-100%."
            },
            "radiology_presentation": {
                "ldct_appearance": "Massive central mediastinal and hilar lymphadenopathy encasing major pulmonary vessels and superior vena cava (SVC), with relatively small primary bronchial lesion.",
                "lung_rads_category": "Lung-RADS 4B or 4X with mediastinal infiltration.",
                "hounsfield_units": "+40 to +65 HU with extensive vessel encasement."
            },
            "molecular_biomarkers": [
                {"gene": "TP53 & RB1 Co-loss", "frequency": ">90%", "targeted_therapy": "Standard platinum-etoposide backbone"},
                {"gene": "DLL3 (Delta-like ligand 3)", "frequency": "70-85%", "targeted_therapy": "Tarlatamab (BiTE - Bispecific T-cell engager)"},
                {"gene": "SLFN11 Expression", "frequency": "40-50%", "targeted_therapy": "PARP Inhibitors (Olaparib, Talazoparib)"}
            ],
            "clinical_course": "Most aggressive pulmonary neoplasm. Rapid doubling time (median 30 days). Often presents with Superior Vena Cava (SVC) Syndrome or paraneoplastic syndromes (SIADH, Cushing's syndrome, Lambert-Eaton myasthenic syndrome). Clinical staging is simplified into Limited Stage (confined to single radiation port) vs Extensive Stage.",
            "preferred_interventions": "Surgery is rarely indicated due to systemic micrometastases at presentation. First-line therapy: Concurrent Chemoradiotherapy (Cisplatin/Carboplatin + Etoposide) combined with PD-L1 inhibitors (Durvalumab or Atezolizumab) and Prophylactic Cranial Irradiation (PCI)."
        },
        {
            "id": "benign_tissue",
            "name": "Benign Pulmonary Parenchyma & Non-Malignant Lesions",
            "broad_category": "Non-Neoplastic / Benign",
            "frequency_percentage": "N/A (Reference Baseline)",
            "primary_location": "Any anatomical pulmonary zone",
            "smoking_association": "Not directly causative (though smoking induces anthracosis and emphysematous changes)",
            "key_color": "#10b981",
            "histopathology": {
                "cellular_architecture": "Intact delicate alveolar septa lined by type I and type II pneumocytes, ciliated pseudostratified columnar bronchial epithelium, absence of nuclear atypia.",
                "cytological_features": "Uniform round nuclei, low nuclear-to-cytoplasmic ratio, smooth nuclear contours, no mitotic figures, presence of alveolar macrophages (dust cells).",
                "immunohistochemistry": "Normal physiological lineage distribution without aberrant overexpression of proliferative or neuroendocrine antigens."
            },
            "radiology_presentation": {
                "ldct_appearance": "Clear pulmonary parenchymal aeration with uniform branching bronchovascular markings, sharp diaphragm and costophrenic sulci.",
                "lung_rads_category": "Lung-RADS 1 (Negative - No nodules or benign calcified granulomas).",
                "hounsfield_units": "-900 to -700 HU (normal aerated lung density)."
            },
            "molecular_biomarkers": [
                {"gene": "Genomic Integrity", "frequency": "Normal", "targeted_therapy": "No oncological intervention required"}
            ],
            "clinical_course": "Normal physiological pulmonary gas exchange. If benign nodule is present (e.g. hamartoma, calcified granuloma from prior fungal or tuberculosis infection), it remains stable across years without growth.",
            "preferred_interventions": "Periodic age-appropriate health screening. No invasive surgical resection or cytotoxic therapy indicated."
        }
    ]


def get_imaging_modalities() -> List[Dict[str, Any]]:
    """Returns comparative technical characteristics of pulmonary diagnostic imaging modalities."""
    return [
        {
            "modality": "Histopathological Biopsy (H&E Stain)",
            "category": "Cellular & Microscopic Gold Standard",
            "spatial_resolution": "0.25 to 0.50 micrometers (µm) per pixel",
            "radiation_dose": "0 mSv (In vitro slide analysis)",
            "primary_clinical_role": "Definitive microscopic confirmation, histological subtyping, immunohistochemistry (IHC) profiling, and targeted gene sequencing.",
            "advantages": [
                "Definitive cellular diagnosis distinguishing adenocarcinoma, squamous, and small cell carcinoma",
                "Enables molecular Next-Generation Sequencing (NGS) for targeted therapy selection",
                "Reveals micro-invasion, vascular invasion, and mitotic index directly"
            ],
            "limitations": [
                "Invasive tissue acquisition (Bronchoscopy, CT-guided core biopsy, or surgical wedge)",
                "Sample may suffer from spatial tumor heterogeneity or crush artifact",
                "Cannot assess whole-body metastatic dissemination alone"
            ],
            "typical_scale": "0.5 µm/px (at 20x objective)"
        },
        {
            "modality": "Low-Dose Computed Tomography (LDCT)",
            "category": "Cross-Sectional Screening & Volume Imaging",
            "spatial_resolution": "0.5 to 0.8 millimeters (mm) per voxel",
            "radiation_dose": "1.0 to 1.5 mSv (vs 7 mSv for standard chest CT)",
            "primary_clinical_role": "Annual screening for high-risk individuals (50-80 years, ≥20 pack-year smoking history), early detection of asymptomatic nodules.",
            "advantages": [
                "Reduces lung cancer mortality by 20% according to National Lung Screening Trial (NLST)",
                "Detects non-calcified pulmonary nodules as small as 2–4 mm",
                "Provides volumetric measurement and precise doubling-time doubling calculations"
            ],
            "limitations": [
                "High rate of benign false positives requiring serial follow-up scans",
                "Cumulative low radiation exposure across years",
                "Requires confirmatory tissue biopsy for suspicious Lung-RADS 4 nodules"
            ],
            "typical_scale": "0.7 mm/px"
        },
        {
            "modality": "High-Resolution Contrast CT (Chest/Abdomen)",
            "category": "Full Clinical Staging (TNM Anatomical Assessment)",
            "spatial_resolution": "0.4 to 0.6 mm per voxel with IV iodinated contrast",
            "radiation_dose": "5 to 8 mSv",
            "primary_clinical_role": "TNM staging: exact primary tumor size ($T$), chest wall invasion, mediastinal/hilar lymphadenopathy ($N$), and adrenal/liver metastases ($M$).",
            "advantages": [
                "Precise vascular contrast distinguishes lymph nodes from mediastinal vessels",
                "Evaluates chest wall, pericardial, and vertebral body invasion",
                "Direct surgical planning and vascular resection feasibility assessment"
            ],
            "limitations": [
                "Requires intravenous contrast with risk of allergic reaction or nephrotoxicity",
                "Cannot reliably determine microscopic lymph node involvement in normal-sized nodes (<1 cm)"
            ],
            "typical_scale": "0.5 mm/px"
        },
        {
            "modality": "Chest Radiography (Conventional X-Ray)",
            "category": "Initial Symptomatic First-Line Screening",
            "spatial_resolution": "0.1 to 0.2 mm (2D projection planar image)",
            "radiation_dose": "0.05 to 0.1 mSv",
            "primary_clinical_role": "Immediate evaluation of symptomatic presentation (cough, dyspnea, hemoptysis), detection of pneumonia, pleural effusion, or large masses.",
            "advantages": [
                "Inexpensive, universally available in primary healthcare clinics",
                "Extremely low radiation exposure, takes <1 minute to acquire",
                "Quick triage of alternative causes (pneumothorax, heart failure, consolidation)"
            ],
            "limitations": [
                "Poor sensitivity for early-stage nodules; frequently misses lesions <1 cm or those masked by ribs/mediastinum",
                "Two-dimensional overlap obscures retrocardiac and apical regions",
                "Not recommended as an independent cancer screening modality"
            ],
            "typical_scale": "0.15 mm/px"
        },
        {
            "modality": "18F-FDG Positron Emission Tomography (PET-CT)",
            "category": "Functional Metabolic & Whole-Body Staging",
            "spatial_resolution": "3.0 to 4.5 mm (Metabolic PET) fused with Sub-millimeter CT",
            "radiation_dose": "10 to 14 mSv (combined tracer + CT)",
            "primary_clinical_role": "Metabolic staging: differentiates benign from malignant nodules based on glucose consumption (SUVmax), detects distant occult metastases.",
            "advantages": [
                "High sensitivity for detecting occult distant metastases (bone, soft tissue, lymph nodes)",
                "Guides target volume delineation in curative radiation therapy planning",
                "Standard Uptake Value (SUVmax > 2.5) provides quantitative malignancy probability"
            ],
            "limitations": [
                "Expensive, requires cyclotron-produced radioactive fluorine-18 tracer",
                "False positives in inflammatory granulomas (active tuberculosis, sarcoidosis)",
                "Poor brain metastasis sensitivity due to high physiological cerebral glucose uptake (Brain MRI preferred)"
            ],
            "typical_scale": "2.0 mm/px (PET grid)"
        }
    ]

