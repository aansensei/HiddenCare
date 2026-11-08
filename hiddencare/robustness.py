# kiem dinh do ben mo hinh qua cac kien truc random forest va gradient boosting
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from hiddencare.config import PATHS, PREDICTORS, PRIMARY_CAPACITY, SEED


# xay dung pipeline tien xu ly va phan loai cho cac kien truc phi tuyen
def create_model_pipeline(architecture: str = "rf") -> Pipeline:
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    
    if architecture == "rf":
        clf = RandomForestClassifier(
            n_estimators=150,
            max_depth=5,
            min_samples_split=20,
            random_state=SEED,
            n_jobs=-1,
        )
    elif architecture == "gb":
        clf = HistGradientBoostingClassifier(
            max_iter=100,
            max_depth=4,
            learning_rate=0.05,
            random_state=SEED,
        )
    else:
        raise ValueError(f"Unknown architecture: {architecture}")
        
    return Pipeline([("imputer", imputer), ("scaler", scaler), ("classifier", clf)])


# huan luyen va danh gia do ben tren holdout 2021 to 2023
def run_architecture_robustness_check(
    train_df: pd.DataFrame,
    eval_df: pd.DataFrame,
    output_tables_dir: Path,
    output_figures_dir: Path,
) -> pd.DataFrame:
    output_tables_dir.mkdir(parents=True, exist_ok=True)
    output_figures_dir.mkdir(parents=True, exist_ok=True)
    
    x_train = train_df[PREDICTORS]
    y_train_a = train_df["label_dx"].values
    y_train_b = train_df["label_full"].values
    
    x_eval = eval_df[PREDICTORS]
    y_eval = eval_df["potential_case"].values
    n_eval = len(eval_df)
    k_primary = int(np.floor(PRIMARY_CAPACITY * n_eval))
    
    results = []
    
    architectures = [
        ("rf", "Random Forest"),
        ("gb", "Gradient Boosting"),
    ]
    
    eval_cache: dict[str, dict] = {}
    
    for arch_key, arch_name in architectures:
        # huan luyen mo hinh a (diagnosis only)
        pipe_a = create_model_pipeline(arch_key)
        pipe_a.fit(x_train, y_train_a)
        scores_a = pipe_a.predict_proba(x_eval)[:, 1]
        
        # huan luyen mo hinh b (biomarker augmented)
        pipe_b = create_model_pipeline(arch_key)
        pipe_b.fit(x_train, y_train_b)
        scores_b = pipe_b.predict_proba(x_eval)[:, 1]
        
        # xac dinh hang uu tien va lua chon tai nguong 20%
        rank_a = np.argsort(-scores_a, kind="mergesort")
        rank_b = np.argsort(-scores_b, kind="mergesort")
        
        sel_a = np.zeros(n_eval, dtype=int)
        sel_a[rank_a[:k_primary]] = 1
        
        sel_b = np.zeros(n_eval, dtype=int)
        sel_b[rank_b[:k_primary]] = 1
        
        # so ca phat hien toan hang doi tai nguong 20%
        cases_a = int(np.sum(sel_a * y_eval))
        cases_b = int(np.sum(sel_b * y_eval))
        
        # xac dinh nhom hoan doi bien
        b_exclusive = (sel_b == 1) & (sel_a == 0)
        a_exclusive = (sel_a == 1) & (sel_b == 0)
        
        swap_count = int(np.sum(b_exclusive))
        swap_cases_b = int(np.sum(b_exclusive * y_eval))
        swap_cases_a = int(np.sum(a_exclusive * y_eval))
        
        # ty le do chinh xac tai bien
        prec_b = (swap_cases_b / swap_count * 100.0) if swap_count > 0 else 0.0
        prec_a = (swap_cases_a / swap_count * 100.0) if swap_count > 0 else 0.0
        prec_ratio = (prec_b / prec_a) if prec_a > 0 else 1.0
        
        # kiem toan do nhay nhom khong bao hiem
        uninsured_mask = (eval_df["insured"] == "uninsured").values
        unins_cases_total = int(np.sum(uninsured_mask * y_eval))
        unins_detected_a = int(np.sum(sel_a * uninsured_mask * y_eval))
        unins_detected_b = int(np.sum(sel_b * uninsured_mask * y_eval))
        
        unins_sens_a = (unins_detected_a / unins_cases_total * 100.0) if unins_cases_total > 0 else 0.0
        unins_sens_b = (unins_detected_b / unins_cases_total * 100.0) if unins_cases_total > 0 else 0.0
        unins_sens_delta = unins_sens_b - unins_sens_a
        
        eval_cache[arch_key] = {
            "scores_a": scores_a,
            "scores_b": scores_b,
            "cases_a": cases_a,
            "cases_b": cases_b,
        }
        
        results.append({
            "architecture": arch_name,
            "capacity": f"{int(PRIMARY_CAPACITY * 100)}%",
            "model_a_cases": cases_a,
            "model_b_cases": cases_b,
            "net_case_gain": cases_b - cases_a,
            "margin_swaps": swap_count,
            "margin_cases_b": swap_cases_b,
            "margin_cases_a": swap_cases_a,
            "margin_precision_ratio": round(prec_ratio, 2),
            "uninsured_sens_a": round(unins_sens_a, 2),
            "uninsured_sens_b": round(unins_sens_b, 2),
            "uninsured_sens_boost": round(unins_sens_delta, 2),
        })
        
    df_results = pd.DataFrame(results)
    csv_path = output_tables_dir / "robustness_model_comparison.csv"
    df_results.to_csv(csv_path, index=False)
    
    # ve bieu do so sanh do ben kien truc
    plt.figure(figsize=(9, 5), dpi=300)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    bar_width = 0.35
    x_indices = np.arange(len(df_results))
    
    val_a = df_results["model_a_cases"].values
    val_b = df_results["model_b_cases"].values
    
    bars1 = plt.bar(x_indices - bar_width / 2, val_a, bar_width, label="Model A (Diagnosis Only)", color="#94a3b8")
    bars2 = plt.bar(x_indices + bar_width / 2, val_b, bar_width, label="Model B (Biomarker Augmented)", color="#0284c7")
    
    plt.ylabel("Undiagnosed Cases Detected at 20% Budget Line", fontsize=11, fontweight=600, color="#0f172a")
    plt.title("Model Robustness: Case Detection Across Nonlinear Architectures", fontsize=13, fontweight=700, color="#0f172a", pad=14)
    plt.xticks(x_indices, df_results["architecture"], fontsize=11, fontweight=600)
    plt.ylim(0, max(max(val_a), max(val_b)) + 12)
    plt.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=10)
    
    # hien thi gia tri so tren dau cot
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1.2, f"{int(yval)}", ha="center", va="bottom", fontsize=10, fontweight=600, color="#475569")
    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1.2, f"{int(yval)}", ha="center", va="bottom", fontsize=10, fontweight=700, color="#0284c7")
        
    plt.tight_layout()
    fig_path = output_figures_dir / "robustness_comparison.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    return df_results
