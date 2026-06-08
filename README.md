# 🫁 DiagnosticAI — Clinical AI Detection Platform

DiagnosticAI is a premium, fully-responsive clinical assistant web application designed to help radiologists, pulmonologists, and oncologists perform early detection and risk classification of lung cancer nodules from CT and MRI scans. 

Utilizing a deep learning MobileNetV2 model, the platform delivers instantaneous nodule analysis (<3 seconds) alongside automated **Lung-RADS clinical categorization**, risk assessment scoring, longitudinal patient record tracking, and print-ready report generation.

## ⚡ Quick Start

```bash
pip install -r requirements.txt
python app.py
```

---

## ✨ Features

- **🧠 Deep Learning Nodule Detection**: Local MobileNetV2-based image classification (`lung_cancer_model.h5`) integrated into a Flask clinical workflow prototype for lung nodule risk assessment.
- **📊 Lung-RADS Nodule Classification**: Automatically groups findings based on malignancy thresholds matching American College of Radiology guidelines (Lung-RADS 1, 2, 3, 4A, 4B).
- **📱 Native Mobile Rear-Camera Capture**: Built-in Progressive HTML5 Capture (`accept="image/*" capture="environment"`) that directly hooks into mobile back-facing cameras for rapid scan uploads on phones, while falling back gracefully to the file system explorer on desktop viewports.
- **🎨 Responsive Glassmorphic UX**: A premium dark-mode interface built on modern CSS typography, layout systems, and CSS variables. The entire dashboard, metrics panels, tables, and settings pages reflow to single-columns on viewports under 768px, including a mobile sticky header and a slide-in side drawer.
- **🔒 Secure Offline Workflow**: Bypasses external network dependencies and cloud APIs. Includes a secure offline Verification Challenge (locating the Lungs 🫁) to perform password resets without configuration of SMTP mail relays.
- **📋 Exportable Reports**: Export patient cohorts and individual clinical records directly to **Excel (.xlsx)** or print-ready **PDFs** containing clinician signature lines.

---

## 🛠️ Technology Stack

- **Backend**: Python Flask, Werkzeug Security (hashing)
- **Machine Learning**: TensorFlow (v2), Keras, OpenCV-python, NumPy
- **Database**: SQLite3 (relational database engine)
- **Frontend**: Semantic HTML5, Vanilla CSS3 (Custom Glassmorphic design tokens), Javascript (ES6), Lucide Icons
- **Document Exporting**: OpenPyXL (Excel generation), ReportLab (PDF compiler)

---

## 📁 Repository Structure

```text
DiagnosticAI/
├── app.py                     # Main Flask routing, auth sessions, and exports
├── model.py                   # OpenCV pre-processing & MobileNetV2 model predictions
├── lung_cancer_model.h5       # Pre-trained deep learning weights
├── requirements.txt           # Python dependency declarations
├── database/
│   └── db.py                  # SQLite3 database initializer and table schemas
├── static/
│   ├── css/
│   │   └── style.css          # Main glassmorphic theme styling & mobile overrides
│   ├── js/
│   │   └── main.js            # Sidebar toggle animations and modal controls
│   └── uploads/               # Secure local directory for uploaded patient scans
└── templates/                 # UI HTML templates (extended from base.html)
    ├── base.html              # Layout structure with responsive mobile header
    ├── dashboard.html         # Main overview stats and recent activity
    ├── upload.html            # Progressive wizard with mobile camera capture
    ├── records.html           # Master patient registry table
    ├── reports.html           # Report list, export actions, and print preview
    ├── evaluation.html        # AI model accuracy metrics, CM, and ROC chart
    └── settings.html          # Doctor specification profiles
```

---

## 🚀 Running the Application

### 1. Clone the Repository

```bash
git clone https://github.com/sairaj565/DiagnosticAI.git
```

### 2. Navigate to the Project Directory

```bash
cd DiagnosticAI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Application

```bash
python app.py
```

### 5. Open in Browser

Once the server starts successfully, open:

```text
http://127.0.0.1:5000
```

The DiagnosticAI dashboard will load in your browser.

### Notes

* Python 3.8–3.10 recommended.
* The SQLite database is automatically initialized on first run.
* The pretrained model (`lung_cancer_model.h5`) is included in the repository.
* TensorFlow GPU warnings can be safely ignored on systems without NVIDIA CUDA support.
* First startup may take a few seconds while the model loads into memory.

---

## 🧪 Testing the Application

After launching the application:

1. Open `http://127.0.0.1:5000`
2. Create a physician account and log in.
3. Navigate to **Upload Scan**.
4. Select a CT/MRI image from your device or use mobile camera capture.
5. Click **Analyze Scan**.
6. Review the generated prediction, confidence score, Lung-RADS category, and patient report.

---

## 🧪 Sample Test Images

The repository includes a `sample_images` directory containing example CT scan images for quick testing.

After launching the application:

1. Log in to the platform.
2. Navigate to **Upload Scan**.
3. Select any image from the `sample_images` folder.
4. Click **Analyze Scan**.
5. Review the generated prediction and report.

Example files:

* `Normal case (1).jpg`
* `Normal case (2).jpg`
* `Malignant case (1).jpg`
* `Malignant case (2).jpg`

---

## 🔬 AI Inference Pipeline & Clinical Disclaimer

### 1. Nodule Prediction Pipeline
The diagnostic predictions are generated live by the TensorFlow model through the following pipeline:
- **Preprocessing**: Uploaded images are read using OpenCV, converted from BGR to RGB space, resized to `224×224` pixels, and normalized (`pixel / 255.0`) to match the network input structure.
- **Model Inference**: The system loads `lung_cancer_model.h5` and feeds it the processed input array to obtain a probability score (`raw_pred`).
- **Clinical Mapping**: If `raw_pred <= 0.5`, the scan is classified as **Tumor Detected**, mapping the confidence level to a corresponding **Lung-RADS Category (3, 4A, or 4B)**. Otherwise, it is classified as **Normal**, mapping to **Lung-RADS Category (1 or 2)**.

### ⚠️ Medical Disclaimer
> [!WARNING]
> **DiagnosticAI is designed to act as an assistant tool for radiologists and clinical researchers.** 
> While the MobileNetV2 deep learning model runs live math-based predictions, these results are intended for auxiliary diagnostic support, educational reference, and workflow triaging. They do not constitute final medical diagnoses. All clinical decisions and follow-up protocols must be verified by a certified healthcare professional.

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Upload Scan
![Upload Scan](screenshots/upload.png)

### Patient Records
![Patient Records](screenshots/records.png)

### Reports
![Reports](screenshots/reports.png)

### Model Evaluation
![Model Evaluation](screenshots/evaluation.png)

### Analytics
![Analytics](screenshots/analytics.png)
