import tensorflow as tf
import numpy as np
import os
import cv2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

# ══════════════════════════════════════════════
# CONFIG — adjust paths if needed
# ══════════════════════════════════════════════
MODEL_PATH   = "lung_cancer_model.h5"
DATASET_PATH = "dataset"   # same folder used in train.py
IMG_SIZE     = 224

# ══════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
print("[OK] Model loaded")

# ══════════════════════════════════════════════
# LOAD ALL IMAGES + LABELS
# ══════════════════════════════════════════════
# Expects dataset/Normal/ and dataset/Tumor/ folders
# (or whatever your class folder names are)

X, y_true = [], []
class_folders = sorted(os.listdir(DATASET_PATH))
print(f"\nFound classes: {class_folders}")

# MobileNetV2 trained with binary_crossentropy
# flow_from_directory assigns labels alphabetically
# So class index 0 = first folder alphabetically, 1 = second
# Your train.py: prediction > 0.5 = Normal, <= 0.5 = Tumor
# So label 1 = Normal, label 0 = Tumor

for label_idx, folder in enumerate(class_folders):
    folder_path = os.path.join(DATASET_PATH, folder)
    if not os.path.isdir(folder_path):
        continue
    files = os.listdir(folder_path)
    print(f"  Loading {folder} ({len(files)} images) -> label {label_idx}")
    for fname in files:
        fpath = os.path.join(folder_path, fname)
        img = cv2.imread(fpath)
        if img is None:
            continue
        # Convert BGR (cv2 default) to RGB to match training channel order
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
        img_preprocessed = preprocess_input(img_resized.astype('float32'))
        X.append(img_preprocessed)
        y_true.append(label_idx)

X = np.array(X)
y_true = np.array(y_true)
print(f"\nTotal images loaded: {len(X)}")
print(f"Class distribution: {dict(zip(*np.unique(y_true, return_counts=True)))}")

# ══════════════════════════════════════════════
# RUN PREDICTIONS
# ══════════════════════════════════════════════
print("\nRunning predictions...")
y_prob = model.predict(X, verbose=1).flatten()

# Convert probabilities to binary labels
# >0.5 = Normal (label 1), <=0.5 = Tumor (label 0)
y_pred = (y_prob > 0.5).astype(int)

# ══════════════════════════════════════════════
# CALCULATE METRICS
# ══════════════════════════════════════════════
accuracy  = round(accuracy_score(y_true, y_pred) * 100, 2)
precision = round(precision_score(y_true, y_pred, zero_division=0) * 100, 2)
recall    = round(recall_score(y_true, y_pred, zero_division=0) * 100, 2)
f1        = round(f1_score(y_true, y_pred, zero_division=0) * 100, 2)
auc       = round(roc_auc_score(y_true, y_prob), 4)
cm        = confusion_matrix(y_true, y_pred)

# ══════════════════════════════════════════════
# PRINT RESULTS — COPY THESE INTO YOUR APP
# ══════════════════════════════════════════════
print("\n" + "="*50)
print("  DiagnosticAI - MODEL EVALUATION RESULTS")
print("="*50)
print(f"  Accuracy  : {accuracy}%")
print(f"  Precision : {precision}%")
print(f"  Recall    : {recall}%")
print(f"  F1 Score  : {f1}%")
print(f"  ROC-AUC   : {auc}")
print("="*50)
print(f"\nConfusion Matrix:")
print(f"  Classes: {class_folders}")
print(f"  {cm}")
print(f"\n  True Negatives  (TN): {cm[0][0]}")
print(f"  False Positives (FP): {cm[0][1]}")
print(f"  False Negatives (FN): {cm[1][0]}")
print(f"  True Positives  (TP): {cm[1][1]}")
print("\n[OK] Copy these numbers into your dashboard!")
print("="*50)