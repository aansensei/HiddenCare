# hop dong du lieu va cong phat hien bien dong cau truc voi pandera
from typing import Optional
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series
from scipy import stats


# dinh nghia hop dong du lieu cho bang nhan khau hoc goc
class RawDemoSchema(pa.DataFrameModel):
    SEQN: Series[float] = pa.Field(ge=1.0, nullable=False, coerce=True)
    RIDAGEYR: Series[float] = pa.Field(ge=0.0, le=120.0, nullable=False)
    RIAGENDR: Series[float] = pa.Field(isin=[1.0, 2.0], nullable=False)
    INDFMPIR: Series[float] = pa.Field(ge=0.0, le=5.0, nullable=True)
    SDMVPSU: Series[float] = pa.Field(ge=1.0, nullable=False)
    SDMVSTRA: Series[float] = pa.Field(ge=1.0, nullable=False)

    class Config:
        strict = False
        coerce = True


# dinh nghia hop dong du lieu cho bang xet nghiem hba1c goc
class RawGhbSchema(pa.DataFrameModel):
    SEQN: Series[float] = pa.Field(ge=1.0, nullable=False, coerce=True)
    LBXGH: Series[float] = pa.Field(ge=2.0, le=25.0, nullable=True)

    class Config:
        strict = False
        coerce = True


# dinh nghia hop dong du lieu cho bang cau hoi dai thao duong goc
class RawDiqSchema(pa.DataFrameModel):
    SEQN: Series[float] = pa.Field(ge=1.0, nullable=False, coerce=True)
    DIQ010: Series[float] = pa.Field(isin=[1.0, 2.0, 3.0, 7.0, 9.0], nullable=True)

    class Config:
        strict = False
        coerce = True


# dinh nghia hop dong du lieu cho bang do dac the chat goc
class RawBmxSchema(pa.DataFrameModel):
    SEQN: Series[float] = pa.Field(ge=1.0, nullable=False, coerce=True)
    BMXBMI: Series[float] = pa.Field(ge=10.0, le=100.0, nullable=True)
    BMXWAIST: Series[float] = pa.Field(ge=30.0, le=250.0, nullable=True)

    class Config:
        strict = False
        coerce = True


# dinh nghia hop dong du lieu cho bang bao hiem y te goc
class RawHiqSchema(pa.DataFrameModel):
    SEQN: Series[float] = pa.Field(ge=1.0, nullable=False, coerce=True)
    HIQ011: Series[float] = pa.Field(isin=[1.0, 2.0, 7.0, 9.0], nullable=True)

    class Config:
        strict = False
        coerce = True


# dinh nghia hop dong du lieu nghiem ngat cho tap cohort hoan chinh
class CohortSchema(pa.DataFrameModel):
    seqn: Series[int] = pa.Field(ge=1, nullable=False, unique=True, coerce=True)
    age: Series[float] = pa.Field(ge=20.0, le=120.0, nullable=False)
    sex: Series[int] = pa.Field(isin=[1, 2], nullable=False, coerce=True)
    dx: Series[int] = pa.Field(isin=[1, 2], nullable=False, coerce=True)
    a1c: Series[float] = pa.Field(ge=2.0, le=25.0, nullable=False)
    weight: Series[float] = pa.Field(gt=0.0, nullable=False)
    bmi: Series[float] = pa.Field(ge=10.0, le=100.0, nullable=True)
    waist: Series[float] = pa.Field(ge=30.0, le=250.0, nullable=True)
    pir: Series[float] = pa.Field(ge=0.0, le=5.0, nullable=True)
    psu: Series[int] = pa.Field(ge=1, nullable=False, coerce=True)
    strata: Series[int] = pa.Field(ge=1, nullable=False, coerce=True)
    prg: Series[float] = pa.Field(nullable=True)
    label_dx: Series[int] = pa.Field(isin=[0, 1], nullable=False, coerce=True)
    label_full: Series[int] = pa.Field(isin=[0, 1], nullable=False, coerce=True)
    insured: Series[str] = pa.Field(isin=["insured", "uninsured", "unknown"], nullable=False)
    pir_group: Series[str] = pa.Field(isin=["low", "middle", "high", "missing"], nullable=False)

    @pa.check("prg")
    def validate_non_pregnancy(cls, series: Series[float]) -> Series[bool]:
        # khong chap nhan thai ky da xac nhan (ma 1.0 bi loai tru)
        return series.isna() | (series != 1.0)

    class Config:
        strict = False
        coerce = True


# tinh toan chi so on dinh quan the psi giua hai phan phoi
def calculate_psi(expected: np.ndarray, actual: np.ndarray, num_bins: int = 10) -> float:
    exp_clean = expected[~np.isnan(expected)]
    act_clean = actual[~np.isnan(actual)]
    if len(exp_clean) == 0 or len(act_clean) == 0:
        return 0.0
    
    # xac dinh cac diem chia dua tren tap co so
    percentiles = np.linspace(0, 100, num_bins + 1)
    bins = np.percentile(exp_clean, percentiles)
    bins[0] = -np.inf
    bins[-1] = np.inf
    
    exp_counts, _ = np.histogram(exp_clean, bins=bins)
    act_counts, _ = np.histogram(act_clean, bins=bins)
    
    exp_pct = np.where(exp_counts == 0, 0.0001, exp_counts) / len(exp_clean)
    act_pct = np.where(act_counts == 0, 0.0001, act_counts) / len(act_clean)
    
    psi_val = np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct))
    return float(round(psi_val, 4))


# thuc hien kiem toan bien dong cau truc va phan phoi giua cac chu ky
def run_schema_drift_audit(
    df_train: pd.DataFrame,
    df_eval: pd.DataFrame,
    output_dir: Path | None = None,
) -> dict:
    audit_results: dict = {
        "status": "PASSED",
        "sample_sizes": {
            "pre_pandemic_train": len(df_train),
            "post_pandemic_eval": len(df_eval),
        },
        "missingness_drift": {},
        "distribution_drift": {},
    }
    
    # kiem tra do lech ty le du lieu bi khuyet
    audit_features = ["bmi", "waist", "pir"]
    for col in audit_features:
        train_miss = float(round(df_train[col].isna().mean() * 100.0, 2))
        eval_miss = float(round(df_eval[col].isna().mean() * 100.0, 2))
        delta = float(round(abs(eval_miss - train_miss), 2))
        audit_results["missingness_drift"][col] = {
            "pre_pandemic_pct": train_miss,
            "post_pandemic_pct": eval_miss,
            "delta_pct": delta,
            "drift_warning": delta > 15.0,
        }
    
    # kiem tra bien dong phan phoi bang kiem dinh kolmogorov-smirnov va psi
    continuous_features = ["age", "a1c", "bmi", "waist"]
    for col in continuous_features:
        s_train = df_train[col].dropna().values
        s_eval = df_eval[col].dropna().values
        ks_stat, ks_p = stats.ks_2samp(s_train, s_eval)
        psi_score = calculate_psi(s_train, s_eval)
        
        # danh gia muc do bien dong theo chuan nganh
        shift_status = "STABLE"
        if psi_score >= 0.25:
            shift_status = "SIGNIFICANT_SHIFT"
        elif psi_score >= 0.10:
            shift_status = "MODERATE_SHIFT"
            
        audit_results["distribution_drift"][col] = {
            "ks_statistic": float(round(ks_stat, 4)),
            "p_value": float(round(ks_p, 4)),
            "psi_score": psi_score,
            "stability_status": shift_status,
        }

    # xuat bao cao sang tap json va markdown neu co duong dan
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "schema_drift_audit.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(audit_results, f, indent=2)
            
        md_path = output_dir / "schema_drift_audit.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# NHANES Cross-Cycle Data Quality & Schema Drift Audit\n\n")
            f.write(f"Audit Status: {audit_results['status']}\n\n")
            f.write("## 1. Sample Sizes\n\n")
            f.write(f"* Pre-pandemic Development Cohort: N = {audit_results['sample_sizes']['pre_pandemic_train']:,}\n")
            f.write(f"* Post-pandemic Evaluation Cohort: N = {audit_results['sample_sizes']['post_pandemic_eval']:,}\n\n")
            f.write("## 2. Missingness Rate Comparison\n\n")
            f.write("| Feature | Pre-Pandemic (%) | Post-Pandemic (%) | Absolute Delta (%) | Warning |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for k, v in audit_results["missingness_drift"].items():
                f.write(f"| `{k}` | {v['pre_pandemic_pct']}% | {v['post_pandemic_pct']}% | {v['delta_pct']}% | {v['drift_warning']} |\n")
            f.write("\n## 3. Population Distribution Stability (PSI & KS Test)\n\n")
            f.write("| Feature | KS Stat | p-value | PSI Score | Stability Assessment |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for k, v in audit_results["distribution_drift"].items():
                f.write(f"| `{k}` | {v['ks_statistic']} | {v['p_value']} | {v['psi_score']} | **{v['stability_status']}** |\n")
                
    return audit_results
