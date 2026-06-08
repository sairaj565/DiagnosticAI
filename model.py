import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import traceback

# ══════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════
MODEL_PATH = 'lung_cancer_model.h5'
model = None
try:
    model = load_model(MODEL_PATH, compile=False)
    print("[OK] Model loaded successfully.")
    # Pre-warm model with dummy prediction to trigger one-time library/graph init delays
    print("Pre-warming model...")
    dummy_input = np.zeros((1, 224, 224, 3), dtype=np.float32)
    model.predict(dummy_input, verbose=0)
    print("[OK] Model pre-warmed successfully.")
    print("-- Last 10 layers --")
    for layer in model.layers[-10:]:
        print(f"  {layer.name}  ({type(layer).__name__})")
except Exception as e:
    print(f"[ERROR] Model load error: {e}")


# ══════════════════════════════════════════════
# PREPROCESS
# Raw pixels only — model was trained on raw JPGs
# DO NOT apply CLAHE here — it will hurt accuracy
# ══════════════════════════════════════════════
def preprocess(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")
    img_rgb     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224))
    img_norm    = preprocess_input(img_resized.astype('float32'))
    return img, img_rgb, img_resized, np.expand_dims(img_norm, axis=0)


# NOTE: Grad-CAM, Heatmap, Bounding Box, and Tumor Localization
# all removed — Lung-RADS is the clinically reliable output.


# ══════════════════════════════════════════════
# LUNG-RADS
# Applied for BOTH results:
#   Tumor Detected → minimum Category 3 (enforced)
#   Normal         → Category 1 or 2 (guides screening interval)
# ══════════════════════════════════════════════
def calculate_lungrads(confidence, is_tumor=False):
    c = confidence / 100.0

    if is_tumor:
        if c >= 0.92:
            return {"category": "4B", "label": "Lung-RADS 4B — Very Suspicious",
                    "description": "High likelihood of malignancy. Immediate intervention required.",
                    "action": "Immediate biopsy. Urgent oncology referral.",
                    "color": "red", "badge": "#dc2626"}
        elif c >= 0.82:
            return {"category": "4A", "label": "Lung-RADS 4A — Suspicious",
                    "description": "Moderate malignancy probability. Intervention likely needed.",
                    "action": "3-month LDCT or PET-CT. Consider biopsy.",
                    "color": "red", "badge": "#ef4444"}
        else:
            return {"category": "3", "label": "Lung-RADS 3 — Probably Benign",
                    "description": "Malignancy signal detected. Clinical correlation required.",
                    "action": "6-month LDCT follow-up. Radiologist review advised.",
                    "color": "amber", "badge": "#f59e0b"}

    # Normal scan — Lung-RADS guides how soon next screening should be
    if c >= 0.92:
        return {"category": "1", "label": "Lung-RADS 1 — Negative",
                "description": "No nodules detected. Very low malignancy likelihood.",
                "action": "Continue annual screening. No further action needed.",
                "color": "green", "badge": "#10b981"}
    elif c >= 0.70:
        return {"category": "2", "label": "Lung-RADS 2 — Benign Appearance",
                "description": "Nodules with low likelihood of becoming malignant.",
                "action": "Annual LDCT in 12 months.",
                "color": "green", "badge": "#10b981"}
    else:
        return {"category": "2", "label": "Lung-RADS 2 — Benign Appearance",
                "description": "No significant findings. Routine follow-up recommended.",
                "action": "Annual LDCT in 12 months.",
                "color": "green", "badge": "#10b981"}


# ══════════════════════════════════════════════
# MAIN PREDICT
# ══════════════════════════════════════════════
def predict(image_path, age=0, smoking=''):
    if model is None:
        return {"error": "Model not loaded. Check lung_cancer_model.h5 exists."}
    try:
        img_bgr, img_rgb, img_resized, img_array = preprocess(image_path)

        raw_pred   = float(model.predict(img_array, verbose=0)[0][0])
        is_tumor   = raw_pred <= 0.5
        result     = "Tumor Detected" if is_tumor else "Normal"
        disease    = "Malignancy Detected" if is_tumor else "No Cancer Detected"
        confidence = round((1 - raw_pred) * 100, 2) if is_tumor else round(raw_pred * 100, 2)

        # Tumor Detected can NEVER show LOW RISK
        if is_tumor:
            risk = "HIGH" if confidence >= 85 else "MEDIUM"
        else:
            risk = "LOW"

        color = "#ef4444" if is_tumor else "#10b981"
        print(f"DEBUG >>> raw={raw_pred:.4f} | tumor={is_tumor} | conf={confidence}% | risk={risk}")

        lungrads = calculate_lungrads(confidence, is_tumor=is_tumor)
        print(f"DEBUG >>> Lung-RADS={lungrads['category']}")

        return {
            "result":      result,
            "disease":     disease,
            "confidence":  confidence,
            "risk":        risk,
            "color":       color,
            "raw_pred":    round(raw_pred, 4),
            "lungrads":    lungrads,
            "cancer_type": None,
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": f"Prediction failed: {str(e)}"}