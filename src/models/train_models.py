"""Train baseline models for NHANES back pain related signal analysis.

The script trains Logistic Regression and Random Forest models using a
reproducible scikit-learn pipeline, exports metrics, threshold comparison,
class-weight comparison, ablation results, and diagnostic plots.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

TARGET = "backpain_6w"
RANDOM_STATE = 42

BASE_FEATURES = [
    "age",
    "sex_male",
    "bmi",
    "waist",
    "sleep_hours",
    "sedentary_minutes",
    "smoke_100_yes",
    "education_level",
    "income_poverty_ratio",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train NHANES back pain classification models.")
    parser.add_argument("--input", default="data/processed/nhanes_backpain_processed.csv", help="Processed CSV path.")
    parser.add_argument("--outputs-dir", default="outputs", help="Directory for model outputs.")
    parser.add_argument("--reports-dir", default="reports", help="Directory for model reports.")
    return parser.parse_args()


def ensure_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def get_feature_columns(df: pd.DataFrame, drop_body_measures: bool = False) -> List[str]:
    features = [col for col in BASE_FEATURES if col in df.columns]
    if drop_body_measures:
        features = [col for col in features if col not in {"bmi", "waist"}]
    return features


def make_preprocessor(features: List[str]) -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    return ColumnTransformer(transformers=[("num", numeric_transformer, features)])


def make_pipeline(model_name: str, features: List[str], class_weight: Optional[str] = None) -> Pipeline:
    if model_name == "logistic_regression":
        model = LogisticRegression(max_iter=1000, class_weight=class_weight, random_state=RANDOM_STATE)
    elif model_name == "random_forest":
        model = RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=5,
            class_weight=class_weight,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
    else:
        raise ValueError(f"Unsupported model_name: {model_name}")

    return Pipeline(steps=[("preprocess", make_preprocessor(features)), ("model", model)])


def evaluate_at_threshold(y_true: pd.Series, y_score: np.ndarray, threshold: float) -> Dict[str, float]:
    y_pred = (y_score >= threshold).astype(int)
    return {
        "threshold": threshold,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_score),
    }


def plot_confusion_matrix(cm: np.ndarray, title: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm)
    ax.set_title(title)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_roc(y_true: pd.Series, scores_by_model: Dict[str, np.ndarray], path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    for model_name, scores in scores_by_model.items():
        fpr, tpr, _ = roc_curve(y_true, scores)
        auc = roc_auc_score(y_true, scores)
        ax.plot(fpr, tpr, label=f"{model_name} AUC={auc:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", label="baseline")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_pr(y_true: pd.Series, scores_by_model: Dict[str, np.ndarray], path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    for model_name, scores in scores_by_model.items():
        precision, recall, _ = precision_recall_curve(y_true, scores)
        ax.plot(recall, precision, label=model_name)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def train_and_evaluate(
    df: pd.DataFrame,
    features: List[str],
    class_weight: Optional[str],
    outputs_dir: Path,
) -> Tuple[pd.DataFrame, Dict[str, np.ndarray], Dict[str, Pipeline], pd.Series]:
    clean = df.dropna(subset=[TARGET]).copy()
    X = clean[features]
    y = clean[TARGET].astype(int)

    stratify = y if y.nunique() == 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=stratify,
    )

    metrics = []
    scores_by_model: Dict[str, np.ndarray] = {}
    fitted: Dict[str, Pipeline] = {}

    for model_name in ["logistic_regression", "random_forest"]:
        pipeline = make_pipeline(model_name=model_name, features=features, class_weight=class_weight)
        pipeline.fit(X_train, y_train)
        score = pipeline.predict_proba(X_test)[:, 1]
        pred = (score >= 0.5).astype(int)
        row = evaluate_at_threshold(y_test, score, threshold=0.5)
        row.update({"model": model_name, "class_weight": class_weight or "none", "n_features": len(features)})
        metrics.append(row)

        cm = confusion_matrix(y_test, pred)
        plot_confusion_matrix(cm, f"{model_name} confusion matrix", outputs_dir / f"confusion_matrix_{model_name}_{class_weight or 'none'}.png")

        scores_by_model[model_name] = score
        fitted[model_name] = pipeline
        joblib.dump(pipeline, outputs_dir / f"model_{model_name}_{class_weight or 'none'}.joblib")

    return pd.DataFrame(metrics), scores_by_model, fitted, y_test


def threshold_sweep(y_true: pd.Series, scores: np.ndarray, model_name: str) -> pd.DataFrame:
    rows = []
    for threshold in np.arange(0.1, 0.91, 0.05):
        row = evaluate_at_threshold(y_true, scores, threshold=float(round(threshold, 2)))
        row["model"] = model_name
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    outputs_dir = Path(args.outputs_dir)
    reports_dir = Path(args.reports_dir)
    ensure_dirs([outputs_dir, reports_dir])

    if not input_path.exists():
        raise FileNotFoundError(f"Processed CSV not found: {input_path}")

    df = pd.read_csv(input_path)
    features = get_feature_columns(df)
    if TARGET not in df.columns:
        raise KeyError(f"Target column not found: {TARGET}")
    if not features:
        raise ValueError("No feature columns found. Check preprocessing output.")

    all_metrics = []
    all_thresholds = []
    class_weight_rows = []

    for class_weight in [None, "balanced"]:
        metrics, scores_by_model, fitted, y_test = train_and_evaluate(df, features, class_weight, outputs_dir)
        all_metrics.append(metrics)
        for model_name, scores in scores_by_model.items():
            all_thresholds.append(threshold_sweep(y_test, scores, model_name=f"{model_name}_{class_weight or 'none'}"))
        class_weight_rows.append(metrics)

        if class_weight is None:
            plot_roc(y_test, scores_by_model, outputs_dir / "roc_curve.png")
            plot_pr(y_test, scores_by_model, outputs_dir / "pr_curve.png")

    performance = pd.concat(all_metrics, ignore_index=True)
    performance = performance[["model", "class_weight", "n_features", "threshold", "accuracy", "precision", "recall", "f1", "roc_auc"]]
    performance.to_csv(outputs_dir / "model_performance.csv", index=False, encoding="utf-8-sig")

    threshold_df = pd.concat(all_thresholds, ignore_index=True)
    threshold_df.to_csv(outputs_dir / "threshold_comparison.csv", index=False, encoding="utf-8-sig")

    class_weight_df = pd.concat(class_weight_rows, ignore_index=True)
    class_weight_df.to_csv(outputs_dir / "class_weight_comparison.csv", index=False, encoding="utf-8-sig")

    ablation_features = get_feature_columns(df, drop_body_measures=True)
    if len(ablation_features) < len(features):
        ablation_metrics, _, _, _ = train_and_evaluate(df, ablation_features, None, outputs_dir)
        ablation_metrics["ablation"] = "drop_bmi_waist"
        base_metrics = performance[(performance["class_weight"] == "none")].copy()
        base_metrics["ablation"] = "all_features"
        pd.concat([base_metrics, ablation_metrics], ignore_index=True).to_csv(
            outputs_dir / "body_measure_ablation.csv",
            index=False,
            encoding="utf-8-sig",
        )

    with open(reports_dir / "model_interpretation_notes.md", "w", encoding="utf-8") as f:
        f.write("# 모델 해석 노트\n\n")
        f.write("## 주의\n\n")
        f.write("본 결과는 자가보고 라벨 기반 분류 결과이며, 의학적 진단이나 인과관계 해석이 아닙니다.\n\n")
        f.write("## 생성 산출물\n\n")
        f.write("- `outputs/model_performance.csv`\n")
        f.write("- `outputs/threshold_comparison.csv`\n")
        f.write("- `outputs/class_weight_comparison.csv`\n")
        f.write("- `outputs/body_measure_ablation.csv`\n")
        f.write("- `outputs/roc_curve.png`\n")
        f.write("- `outputs/pr_curve.png`\n")

    print("Model training complete.")
    print(f"Performance: {outputs_dir / 'model_performance.csv'}")


if __name__ == "__main__":
    main()
