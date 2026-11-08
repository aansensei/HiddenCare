# uoc luong phuong sai khao sat phuc hop theo phuong phap tuyen tinh hoa taylor
import numpy as np
import pandas as pd
from scipy import stats


# tinh toan ty le co trong so va sai so chuan tuyen tinh hoa taylor theo chuan cdc
def compute_survey_ratio_variance(
    df: pd.DataFrame,
    numerator_col: str,
    denominator_col: str,
    weight_col: str = "weight",
    strata_col: str = "strata",
    psu_col: str = "psu",
    alpha: float = 0.05,
) -> dict[str, float]:
    w = df[weight_col].values
    y = df[numerator_col].values.astype(float)
    x = df[denominator_col].values.astype(float)
    
    sum_w_x = np.sum(w * x)
    sum_w_y = np.sum(w * y)
    
    if sum_w_x == 0:
        return {
            "ratio": 0.0,
            "se": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "df": 0,
        }
        
    r_hat = sum_w_y / sum_w_x
    
    # tinh bien tuyen tinh hoa z_i cho tung ca nhan
    z = (w * (y - r_hat * x)) / sum_w_x
    
    df_calc = df[[strata_col, psu_col]].copy()
    df_calc["z"] = z
    
    # tinh tong z_hj cho tung don vi lay mau so cap psu trong tung tang
    psu_sums = df_calc.groupby([strata_col, psu_col])["z"].sum().reset_index()
    
    total_var = 0.0
    total_psus = len(psu_sums)
    total_strata = psu_sums[strata_col].nunique()
    df_degrees = max(1, total_psus - total_strata)
    
    # lap qua tung tang khao sat de tinh do lech giua cac psu
    for _, group in psu_sums.groupby(strata_col):
        n_h = len(group)
        if n_h > 1:
            z_vals = group["z"].values
            z_bar = np.mean(z_vals)
            s_h2 = np.sum((z_vals - z_bar) ** 2)
            total_var += (n_h / (n_h - 1)) * s_h2
        else:
            total_var += 0.0
            
    se = float(np.sqrt(total_var))
    
    # tinh khoang tin cay dua tren phan phoi t-student voi bac tu do khao sat
    t_crit = stats.t.ppf(1.0 - alpha / 2.0, df=df_degrees)
    ci_lower = max(0.0, float(r_hat - t_crit * se))
    ci_upper = min(1.0, float(r_hat + t_crit * se))
    
    return {
        "ratio": float(r_hat),
        "se": se,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "df": df_degrees,
    }


# tinh toan toan bo bang chi so khao sat phuc hop cho hai mo hinh tai cac muc ngan sach
def evaluate_survey_variance_summary(
    eval_df: pd.DataFrame,
    scores_a: np.ndarray,
    scores_b: np.ndarray,
    capacities: list[float] = [0.10, 0.20, 0.30],
) -> pd.DataFrame:
    records = []
    n_total = len(eval_df)
    
    df_eval = eval_df.copy()
    
    for cap in capacities:
        k = int(np.floor(cap * n_total))
        
        # lua chon uu tien sang loc cho mo hinh a
        rank_a = np.argsort(-scores_a, kind="mergesort")
        sel_a = np.zeros(n_total, dtype=int)
        sel_a[rank_a[:k]] = 1
        df_eval["sel_a"] = sel_a
        
        # lua chon uu tien sang loc cho mo hinh b
        rank_b = np.argsort(-scores_b, kind="mergesort")
        sel_b = np.zeros(n_total, dtype=int)
        sel_b[rank_b[:k]] = 1
        df_eval["sel_b"] = sel_b
        
        # tao cac bien tu so va mau so cho do nhay (sensitivity)
        df_eval["sens_num_a"] = df_eval["sel_a"] * df_eval["potential_case"]
        df_eval["sens_num_b"] = df_eval["sel_b"] * df_eval["potential_case"]
        df_eval["sens_denom"] = df_eval["potential_case"]
        
        # tao cac bien tu so va mau so cho gia tri tien doan duong (ppv)
        df_eval["ppv_num_a"] = df_eval["sel_a"] * df_eval["potential_case"]
        df_eval["ppv_denom_a"] = df_eval["sel_a"]
        df_eval["ppv_num_b"] = df_eval["sel_b"] * df_eval["potential_case"]
        df_eval["ppv_denom_b"] = df_eval["sel_b"]
        
        # tinh toan ty le va sai so cho mo hinh a
        sens_a = compute_survey_ratio_variance(df_eval, "sens_num_a", "sens_denom")
        ppv_a = compute_survey_ratio_variance(df_eval, "ppv_num_a", "ppv_denom_a")
        
        # tinh toan ty le va sai so cho mo hinh b
        sens_b = compute_survey_ratio_variance(df_eval, "sens_num_b", "sens_denom")
        ppv_b = compute_survey_ratio_variance(df_eval, "ppv_num_b", "ppv_denom_b")
        
        records.append({
            "capacity": cap,
            "budget_pct": f"{int(cap*100)}%",
            "model": "Model A (Diagnosis Only)",
            "weighted_sensitivity": round(sens_a["ratio"] * 100.0, 2),
            "sens_se": round(sens_a["se"] * 100.0, 2),
            "sens_ci_95": f"[{sens_a['ci_lower']*100:.1f}%, {sens_a['ci_upper']*100:.1f}%]",
            "weighted_ppv": round(ppv_a["ratio"] * 100.0, 2),
            "ppv_se": round(ppv_a["se"] * 100.0, 2),
            "ppv_ci_95": f"[{ppv_a['ci_lower']*100:.1f}%, {ppv_a['ci_upper']*100:.1f}%]",
            "survey_df": sens_a["df"],
        })
        
        records.append({
            "capacity": cap,
            "budget_pct": f"{int(cap*100)}%",
            "model": "Model B (Biomarker Augmented)",
            "weighted_sensitivity": round(sens_b["ratio"] * 100.0, 2),
            "sens_se": round(sens_b["se"] * 100.0, 2),
            "sens_ci_95": f"[{sens_b['ci_lower']*100:.1f}%, {sens_b['ci_upper']*100:.1f}%]",
            "weighted_ppv": round(ppv_b["ratio"] * 100.0, 2),
            "ppv_se": round(ppv_b["se"] * 100.0, 2),
            "ppv_ci_95": f"[{ppv_b['ci_lower']*100:.1f}%, {ppv_b['ci_upper']*100:.1f}%]",
            "survey_df": sens_b["df"],
        })
        
    return pd.DataFrame(records)
