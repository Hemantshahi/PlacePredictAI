"""
models/train_model.py — ML Model Training Script
MCE Placement Prediction System
Run: python models/train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, roc_auc_score,
                             accuracy_score, f1_score, precision_score,
                             recall_score)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import xgboost as xgb
import joblib
import os
import json
import warnings

warnings.filterwarnings('ignore')


# ─────────────────────────────────────────────
#  1. GENERATE REALISTIC DATASET
# ─────────────────────────────────────────────
def generate_dataset(n=5000, seed=42):
    """
    Generate realistic MCE student placement dataset.
    Based on actual placement patterns of Bihar engineering colleges.
    """
    rng = np.random.default_rng(seed)

    # ── Academic Features ──────────────────────────────────────────────────────
    # CGPA: Most students between 6-8.5
    cgpa = np.clip(rng.normal(7.2, 1.1, n), 4.0, 10.0)

    # 10th marks: Most between 60-85%
    tenth = np.clip(rng.normal(72, 12, n), 45, 100)

    # 12th marks: Most between 55-80%
    twelfth = np.clip(rng.normal(68, 13, n), 40, 100)

    # Backlogs: Most have 0, some have 1-2
    backlogs_probs = [0.55, 0.25, 0.12, 0.05, 0.03]
    backlogs = rng.choice([0, 1, 2, 3, 4], n, p=backlogs_probs)

    # ── Experience Features ────────────────────────────────────────────────────
    # Internships: Most have 0-1
    intern_probs = [0.45, 0.35, 0.15, 0.05]
    internships = rng.choice([0, 1, 2, 3], n, p=intern_probs)

    # Projects: Most have 1-3
    project_probs = [0.10, 0.25, 0.35, 0.20, 0.07, 0.03]
    projects = rng.choice([0, 1, 2, 3, 4, 5], n, p=project_probs)

    # Certifications
    cert_probs = [0.20, 0.30, 0.25, 0.15, 0.07, 0.03]
    certifications = rng.choice([0, 1, 2, 3, 4, 5], n, p=cert_probs)

    # ── Skill Features ─────────────────────────────────────────────────────────
    communication = np.clip(rng.normal(5.5, 1.8, n), 1, 10).astype(int)
    coding_skill  = np.clip(rng.normal(5.0, 2.0, n), 1, 10).astype(int)
    aptitude      = np.clip(rng.normal(58, 18, n), 20, 100)
    technical     = np.clip(rng.normal(55, 17, n), 20, 100)
    extracurricular = rng.choice([0, 1, 2, 3, 4], n,
                                  p=[0.30, 0.35, 0.20, 0.10, 0.05])
    ats_score     = np.clip(rng.normal(55, 18, n), 15, 98)

    # ── Derived Features (Feature Engineering) ────────────────────────────────
    academic_score = (cgpa / 10) * 0.5 + (tenth / 100) * 0.25 + (twelfth / 100) * 0.25
    experience_score = (internships / 3) * 0.5 + (projects / 5) * 0.3 + (certifications / 5) * 0.2
    skill_score = (coding_skill / 10) * 0.4 + (communication / 10) * 0.3 + (aptitude / 100) * 0.3

    # ── Placement Logic (Realistic) ────────────────────────────────────────────
    # Base score with realistic weights
    base_score = (
        0.22 * (cgpa / 10) +
        0.07 * (tenth / 100) +
        0.07 * (twelfth / 100) +
        0.12 * np.exp(-0.8 * backlogs) +   # exponential penalty for backlogs
        0.12 * (internships / 3) +
        0.08 * (projects / 5) +
        0.06 * (certifications / 5) +
        0.11 * (communication / 10) +
        0.11 * (coding_skill / 10) +
        0.04 * (aptitude / 100) +
        0.04 * (technical / 100) +
        0.02 * (extracurricular / 4) +
        0.02 * (ats_score / 100)
    )

    # Add realistic noise
    noise = rng.normal(0, 0.04, n)
    final_score = np.clip(base_score + noise, 0, 1)

    # Threshold: ~55% placed (realistic for MCE-type college)
    threshold = np.percentile(final_score, 45)
    placed = (final_score > threshold).astype(int)

    df = pd.DataFrame({
        'cgpa':                  np.round(cgpa, 2),
        'tenth_percent':         np.round(tenth, 1),
        'twelfth_percent':       np.round(twelfth, 1),
        'backlogs':              backlogs,
        'internships':           internships,
        'projects':              projects,
        'certifications':        certifications,
        'communication_skill':   communication,
        'coding_skill':          coding_skill,
        'aptitude_score':        np.round(aptitude, 1),
        'technical_skill_score': np.round(technical, 1),
        'extracurricular':       extracurricular,
        'ats_score':             np.round(ats_score, 1),
        'academic_score':        np.round(academic_score, 4),
        'experience_score':      np.round(experience_score, 4),
        'skill_score':           np.round(skill_score, 4),
        'placed':                placed
    })

    print(f"📊 Dataset: {n} samples | Placed: {placed.sum()} ({placed.mean()*100:.1f}%)")
    return df


# ─────────────────────────────────────────────
#  2. FEATURE COLUMNS
# ─────────────────────────────────────────────
FEATURE_COLS = [
    'cgpa', 'tenth_percent', 'twelfth_percent',
    'backlogs', 'internships', 'projects', 'certifications',
    'communication_skill', 'coding_skill', 'aptitude_score',
    'technical_skill_score', 'extracurricular', 'ats_score',
    'academic_score', 'experience_score', 'skill_score'
]


# ─────────────────────────────────────────────
#  3. EVALUATION HELPER
# ─────────────────────────────────────────────
def evaluate_model(name, y_test, y_pred_proba):
    y_pred = (y_pred_proba > 0.5).astype(int)
    metrics = {
        'accuracy':  round(accuracy_score(y_test, y_pred), 4),
        'auc':       round(roc_auc_score(y_test, y_pred_proba), 4),
        'f1':        round(f1_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall':    round(recall_score(y_test, y_pred), 4),
    }
    print(f"\n{'='*50}")
    print(f"  {name} Results")
    print(f"{'='*50}")
    print(f"  Accuracy  : {metrics['accuracy']*100:.2f}%")
    print(f"  AUC-ROC   : {metrics['auc']:.4f}")
    print(f"  F1-Score  : {metrics['f1']:.4f}")
    print(f"  Precision : {metrics['precision']:.4f}")
    print(f"  Recall    : {metrics['recall']:.4f}")
    print(classification_report(y_test, y_pred,
                                target_names=['Not Placed', 'Placed']))
    return metrics


# ─────────────────────────────────────────────
#  4. TRAIN & SAVE
# ─────────────────────────────────────────────
def train_and_save(output_dir='models/saved'):
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "="*60)
    print("  PlacePredict AI — Model Training")
    print("  MCE Motihari T&P Cell")
    print("="*60)

    # Generate dataset
    print("\n📊 Generating training dataset...")
    df = generate_dataset(n=5000)
    df.to_csv(os.path.join(output_dir, 'training_data.csv'), index=False)
    print(f"✅ Dataset saved: {len(df)} rows, {len(FEATURE_COLS)} features")

    X = df[FEATURE_COLS]
    y = df['placed']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n📦 Train: {len(X_train)} | Test: {len(X_test)}")

    # SMOTE for class balance
    print("⚖️  Applying SMOTE for class balance...")
    smote = SMOTE(random_state=42, k_neighbors=5)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    print(f"   After SMOTE: {len(X_res)} samples")

    # Scaler
    scaler = StandardScaler()
    X_res_s  = scaler.fit_transform(X_res)
    X_test_s = scaler.transform(X_test)
    joblib.dump(scaler, os.path.join(output_dir, 'scaler.pkl'))
    print("✅ Scaler saved.")

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # ── Random Forest ──────────────────────────────────────────────────────────
    print("\n🌲 Training Random Forest with GridSearchCV...")
    rf_params = {
        'n_estimators':     [200, 300],
        'max_depth':        [10, 20, None],
        'min_samples_split':[2, 5],
        'min_samples_leaf': [1, 2],
        'max_features':     ['sqrt', 'log2'],
    }
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=42, class_weight='balanced'),
        rf_params, cv=cv, scoring='roc_auc', n_jobs=-1, verbose=0
    )
    rf_grid.fit(X_res_s, y_res)
    rf_best = rf_grid.best_estimator_
    print(f"   Best params: {rf_grid.best_params_}")

    rf_proba = rf_best.predict_proba(X_test_s)[:, 1]
    rf_metrics = evaluate_model("Random Forest", y_test, rf_proba)
    joblib.dump(rf_best, os.path.join(output_dir, 'random_forest.pkl'))
    results['random_forest'] = rf_metrics
    print("✅ Random Forest saved.")

    # ── XGBoost ────────────────────────────────────────────────────────────────
    print("\n⚡ Training XGBoost with GridSearchCV...")
    xgb_params = {
        'n_estimators':  [200, 300],
        'max_depth':     [4, 6, 8],
        'learning_rate': [0.05, 0.1, 0.15],
        'subsample':     [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 1.0],
        'reg_alpha':     [0, 0.1],
        'reg_lambda':    [1, 1.5],
    }
    xgb_grid = GridSearchCV(
        xgb.XGBClassifier(
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False
        ),
        xgb_params, cv=cv, scoring='roc_auc', n_jobs=-1, verbose=0
    )
    xgb_grid.fit(X_res_s, y_res)
    xgb_best = xgb_grid.best_estimator_
    print(f"   Best params: {xgb_grid.best_params_}")

    xgb_proba = xgb_best.predict_proba(X_test_s)[:, 1]
    xgb_metrics = evaluate_model("XGBoost", y_test, xgb_proba)
    joblib.dump(xgb_best, os.path.join(output_dir, 'xgboost.pkl'))
    results['xgboost'] = xgb_metrics
    print("✅ XGBoost saved.")

    # ── ANN ────────────────────────────────────────────────────────────────────
    print("\n🧠 Training ANN (Deep Neural Network)...")
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import (Dense, Dropout,
                                              BatchNormalization, LeakyReLU)
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
        from tensorflow.keras.optimizers import Adam
        from tensorflow.keras.regularizers import l2

        tf.random.set_seed(42)

        model = Sequential([
            Dense(256, input_shape=(len(FEATURE_COLS),),
                  kernel_regularizer=l2(0.001)),
            LeakyReLU(alpha=0.1),
            BatchNormalization(),
            Dropout(0.3),

            Dense(128, kernel_regularizer=l2(0.001)),
            LeakyReLU(alpha=0.1),
            BatchNormalization(),
            Dropout(0.25),

            Dense(64, kernel_regularizer=l2(0.001)),
            LeakyReLU(alpha=0.1),
            BatchNormalization(),
            Dropout(0.2),

            Dense(32),
            LeakyReLU(alpha=0.1),
            Dropout(0.1),

            Dense(1, activation='sigmoid')
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
        )

        callbacks = [
            EarlyStopping(patience=15, restore_best_weights=True,
                         monitor='val_auc', mode='max'),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                             patience=7, min_lr=1e-6)
        ]

        history = model.fit(
            X_res_s, y_res,
            epochs=150,
            batch_size=64,
            validation_split=0.15,
            callbacks=callbacks,
            verbose=1
        )

        ann_proba = model.predict(X_test_s, verbose=0).flatten()
        ann_metrics = evaluate_model("ANN", y_test, ann_proba)
        model.save(os.path.join(output_dir, 'ann_model.h5'))
        results['ann'] = ann_metrics
        print("✅ ANN saved.")

    except Exception as e:
        print(f"   ⚠️  ANN skipped: {e}")
        results['ann'] = {'auc': 0, 'accuracy': 0,
                          'f1': 0, 'precision': 0, 'recall': 0}

    # ── Ensemble Weights ───────────────────────────────────────────────────────
    print("\n🔀 Calculating ensemble weights...")
    rf_auc  = results['random_forest']['auc']
    xgb_auc = results['xgboost']['auc']
    ann_auc = results['ann']['auc']
    total   = rf_auc + xgb_auc + (ann_auc if ann_auc > 0 else 0)

    weights = {
        'rf':  round(rf_auc / total, 4)  if total > 0 else 0.4,
        'xgb': round(xgb_auc / total, 4) if total > 0 else 0.4,
        'ann': round(ann_auc / total, 4) if total > 0 and ann_auc > 0 else 0.2,
    }
    print(f"   RF weight:  {weights['rf']}")
    print(f"   XGB weight: {weights['xgb']}")
    print(f"   ANN weight: {weights['ann']}")

    # Ensemble prediction
    if ann_auc > 0:
        ensemble_proba = (
            weights['rf']  * rf_proba +
            weights['xgb'] * xgb_proba +
            weights['ann'] * ann_proba
        )
    else:
        w = weights['rf'] + weights['xgb']
        ensemble_proba = (
            (weights['rf']  / w) * rf_proba +
            (weights['xgb'] / w) * xgb_proba
        )

    ens_metrics = evaluate_model("Ensemble", y_test, ensemble_proba)
    results['ensemble'] = ens_metrics
    results['weights']  = weights

    # ── Feature Importance ─────────────────────────────────────────────────────
    print("\n📈 Feature Importance (Random Forest):")
    importance = pd.DataFrame({
        'feature':   FEATURE_COLS,
        'importance': rf_best.feature_importances_
    }).sort_values('importance', ascending=False)
    print(importance.to_string(index=False))
    importance.to_csv(
        os.path.join(output_dir, 'feature_importance.csv'), index=False
    )

    # ── Save metadata ──────────────────────────────────────────────────────────
    with open(os.path.join(output_dir, 'model_metrics.json'), 'w') as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(output_dir, 'feature_cols.json'), 'w') as f:
        json.dump(FEATURE_COLS, f)
    with open(os.path.join(output_dir, 'ensemble_weights.json'), 'w') as f:
        json.dump(weights, f, indent=2)

    # ── Final Summary ──────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("  FINAL RESULTS SUMMARY")
    print("="*60)
    for model_name, m in results.items():
        if model_name == 'weights':
            continue
        if isinstance(m, dict) and 'accuracy' in m:
            print(f"  {model_name:20s} | "
                  f"Acc: {m['accuracy']*100:.2f}% | "
                  f"AUC: {m['auc']:.4f} | "
                  f"F1: {m.get('f1', 0):.4f}")
    print("="*60)
    print(f"\n✅ All models saved to: {output_dir}")
    return results


if __name__ == '__main__':
    train_and_save()