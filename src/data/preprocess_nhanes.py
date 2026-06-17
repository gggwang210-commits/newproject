"""NHANES 2009-2010 preprocessing for back pain related signal analysis.

This script merges selected NHANES XPT files on SEQN, creates an education-only
self-reported low back pain label, recodes selected lifestyle/body variables,
and writes reproducible preprocessing summaries.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd

RAW_FILES = {
    "arq": "ARQ_F.XPT",
    "paq": "PAQ_F.XPT",
    "bmx": "BMX_F.XPT",
    "slq": "SLQ_F.XPT",
    "smq": "SMQ_F.XPT",
    "demo": "DEMO_F.XPT",
}

OUTPUT_COLUMNS = [
    "SEQN",
    "backpain_6w",
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

SPECIAL_MISSING_VALUES = {7, 9, 77, 99, 777, 999, 7777, 9999}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess NHANES data for back pain project.")
    parser.add_argument("--raw-dir", default="data/raw", help="Directory containing NHANES XPT files.")
    parser.add_argument("--processed-dir", default="data/processed", help="Directory for processed CSV output.")
    parser.add_argument("--outputs-dir", default="outputs", help="Directory for generated analysis outputs.")
    parser.add_argument("--reports-dir", default="reports", help="Directory for preprocessing summary reports.")
    return parser.parse_args()


def ensure_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_xpt(raw_dir: Path, filename: str) -> pd.DataFrame:
    path = raw_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_sas(path, format="xport")


def select_existing(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    existing = [col for col in columns if col in df.columns]
    return df[existing].copy()


def set_special_missing(series: pd.Series) -> pd.Series:
    return series.where(~series.isin(SPECIAL_MISSING_VALUES), np.nan)


def create_target(arq: pd.DataFrame) -> pd.DataFrame:
    target = select_existing(arq, ["SEQN", "ARQ010", "ARQ020D", "ARQ024D"])
    if "ARQ020D" not in target.columns:
        raise KeyError("ARQ020D not found in ARQ_F.XPT. Check source file and codebook.")

    target["ARQ020D_clean"] = set_special_missing(target["ARQ020D"])
    target["backpain_6w"] = np.where(target["ARQ020D_clean"] == 4, 1, 0)
    target.loc[target["ARQ020D_clean"].isna(), "backpain_6w"] = np.nan

    if "ARQ024D" in target.columns:
        target["ARQ024D_clean"] = set_special_missing(target["ARQ024D"])
        target["backpain_3m_sensitivity"] = np.where(target["ARQ024D_clean"] == 1, 1, 0)
        target.loc[target["ARQ024D_clean"].isna(), "backpain_3m_sensitivity"] = np.nan

    return target


def build_master(raw_dir: Path) -> pd.DataFrame:
    frames: Dict[str, pd.DataFrame] = {name: read_xpt(raw_dir, filename) for name, filename in RAW_FILES.items()}

    target = create_target(frames["arq"])
    paq = select_existing(frames["paq"], ["SEQN", "PAD680"])
    bmx = select_existing(frames["bmx"], ["SEQN", "BMXBMI", "BMXWAIST"])
    slq = select_existing(frames["slq"], ["SEQN", "SLD010H"])
    smq = select_existing(frames["smq"], ["SEQN", "SMQ020", "SMQ040"])
    demo = select_existing(frames["demo"], ["SEQN", "RIDAGEYR", "RIAGENDR", "DMDEDUC2", "INDFMPIR"])

    master = target
    for frame in [paq, bmx, slq, smq, demo]:
        master = master.merge(frame, on="SEQN", how="left")

    master = recode_features(master)
    return master


def recode_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["age"] = out.get("RIDAGEYR")
    out["sex_male"] = np.where(out.get("RIAGENDR") == 1, 1, np.where(out.get("RIAGENDR") == 2, 0, np.nan))
    out["bmi"] = out.get("BMXBMI")
    out["waist"] = out.get("BMXWAIST")
    out["sleep_hours"] = set_special_missing(out.get("SLD010H")) if "SLD010H" in out.columns else np.nan
    out["sedentary_minutes"] = set_special_missing(out.get("PAD680")) if "PAD680" in out.columns else np.nan
    out["education_level"] = set_special_missing(out.get("DMDEDUC2")) if "DMDEDUC2" in out.columns else np.nan
    out["income_poverty_ratio"] = out.get("INDFMPIR")

    if "SMQ020" in out.columns:
        smq020 = set_special_missing(out["SMQ020"])
        out["smoke_100_yes"] = np.where(smq020 == 1, 1, np.where(smq020 == 2, 0, np.nan))
    else:
        out["smoke_100_yes"] = np.nan

    if "sedentary_minutes" in out.columns:
        out.loc[out["sedentary_minutes"] > 1440, "sedentary_minutes"] = np.nan
    if "sleep_hours" in out.columns:
        out.loc[(out["sleep_hours"] <= 0) | (out["sleep_hours"] > 24), "sleep_hours"] = np.nan

    return out


def write_summaries(df: pd.DataFrame, reports_dir: Path, outputs_dir: Path) -> None:
    available_columns = [col for col in OUTPUT_COLUMNS if col in df.columns]
    model_df = df[available_columns].copy()

    before_n = len(model_df)
    after_target_n = int(model_df["backpain_6w"].notna().sum())
    after_complete_n = int(model_df.dropna(subset=["backpain_6w"]).shape[0])

    summary_rows = [
        {"metric": "rows_before_filter", "value": before_n},
        {"metric": "rows_with_target", "value": after_target_n},
        {"metric": "rows_after_target_filter", "value": after_complete_n},
    ]
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(reports_dir / "preprocessing_summary.csv", index=False, encoding="utf-8-sig")

    missing = model_df.isna().mean().reset_index()
    missing.columns = ["variable", "missing_rate"]
    missing.to_csv(reports_dir / "missing_rate.csv", index=False, encoding="utf-8-sig")

    target_dist = model_df["backpain_6w"].value_counts(dropna=False).rename_axis("backpain_6w").reset_index(name="count")
    target_dist.to_csv(reports_dir / "target_distribution.csv", index=False, encoding="utf-8-sig")

    model_df = model_df.dropna(subset=["backpain_6w"])
    model_df.to_csv(outputs_dir / "nhanes_backpain_processed.csv", index=False, encoding="utf-8-sig")


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    processed_dir = Path(args.processed_dir)
    outputs_dir = Path(args.outputs_dir)
    reports_dir = Path(args.reports_dir)
    ensure_dirs([processed_dir, outputs_dir, reports_dir])

    master = build_master(raw_dir)
    write_summaries(master, reports_dir=reports_dir, outputs_dir=outputs_dir)
    master.to_csv(processed_dir / "nhanes_backpain_master_debug.csv", index=False, encoding="utf-8-sig")
    print("Preprocessing complete.")
    print(f"Processed output: {outputs_dir / 'nhanes_backpain_processed.csv'}")
    print(f"Summary report: {reports_dir / 'preprocessing_summary.csv'}")


if __name__ == "__main__":
    main()
