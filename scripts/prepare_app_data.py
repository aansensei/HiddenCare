# Script to pre-compute and export high-performance analytical data assets for HiddenCare app.

import sys
from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from hiddencare.models import predict_positive_risk
from hiddencare.config import PREDICTORS

def main():
    print("Preparing high-performance data assets for Hugging Face Spaces app...")
    
    # 1. Load trained models and holdout evaluation cohort.
    pipe_dx = joblib.load(PROJECT_ROOT / "outputs" / "models" / "model_dx.joblib")
    pipe_full = joblib.load(PROJECT_ROOT / "outputs" / "models" / "model_full.joblib")
    
    eval_df = pd.read_parquet(PROJECT_ROOT / "data" / "processed" / "eval_subset.parquet")
    n_eval = len(eval_df)
    n_cases = int(eval_df["potential_case"].sum())
    seqns = eval_df["seqn"].values
    true_cases = eval_df["potential_case"].values.astype(int)

    # 2. Compute probabilities and deterministic ranks.
    prob_dx = predict_positive_risk(pipe_dx, eval_df, PREDICTORS)
    prob_full = predict_positive_risk(pipe_full, eval_df, PREDICTORS)

    eval_df["prob_dx"] = prob_dx
    eval_df["prob_full"] = prob_full

    # In lexsort, lower values sort first. Negate probabilities so highest probability gets rank 1.
    order_dx = np.lexsort((seqns, -prob_dx))
    order_full = np.lexsort((seqns, -prob_full))

    rank_dx = np.empty(n_eval, dtype=int)
    rank_full = np.empty(n_eval, dtype=int)
    rank_dx[order_dx] = np.arange(1, n_eval + 1)
    rank_full[order_full] = np.arange(1, n_eval + 1)

    eval_df["rank_dx"] = rank_dx
    eval_df["rank_full"] = rank_full

    # Save primary holdout table.
    data_dir = PROJECT_ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    eval_df.to_parquet(data_dir / "holdout_2021_2023.parquet", index=False)
    print(f"Saved holdout_2021_2023.parquet ({len(eval_df)} rows).")

    # 3. Extract the 122 marginal patients at primary 20% capacity (K = 939).
    k_primary = int(np.floor(0.20 * n_eval))
    mask_only_a = (eval_df["rank_dx"] <= k_primary) & (eval_df["rank_full"] > k_primary)
    mask_only_b = (eval_df["rank_full"] <= k_primary) & (eval_df["rank_dx"] > k_primary)

    swap_a = eval_df.loc[mask_only_a].copy()
    swap_a["swap_group"] = "Model A Exclusive (Dropped by Label B)"

    swap_b = eval_df.loc[mask_only_b].copy()
    swap_b["swap_group"] = "Model B Exclusive (Rescued by Label B)"

    margin_swap_df = pd.concat([swap_b, swap_a], ignore_index=True)
    margin_swap_df.to_parquet(data_dir / "margin_swap_61.parquet", index=False)
    print(f"Saved margin_swap_61.parquet ({len(margin_swap_df)} rows; {len(swap_b)} rescued, {len(swap_a)} dropped).")

    # 4. Pre-compute capacity curve lookup table (k = 1% to 100%).
    lookup_rows = []
    for k_pct in range(1, 101):
        cap_frac = k_pct / 100.0
        k_pick = int(np.floor(cap_frac * n_eval))

        sel_dx = (rank_dx <= k_pick)
        sel_full = (rank_full <= k_pick)

        # Model A metrics
        found_a = int((sel_dx & (true_cases == 1)).sum())
        sens_a = found_a / n_cases
        ppv_a = found_a / k_pick if k_pick > 0 else 0.0
        nns_a = k_pick / found_a if found_a > 0 else np.nan

        # Model B metrics
        found_b = int((sel_full & (true_cases == 1)).sum())
        sens_b = found_b / n_cases
        ppv_b = found_b / k_pick if k_pick > 0 else 0.0
        nns_b = k_pick / found_b if found_b > 0 else np.nan

        # Random baseline
        exp_found = cap_frac * n_cases
        exp_sens = cap_frac
        exp_ppv = n_cases / n_eval
        exp_nns = n_eval / n_cases

        # Margin swap dynamics
        consensus_n = int((sel_dx & sel_full).sum())
        consensus_cases = int(((sel_dx & sel_full) & (true_cases == 1)).sum())
        only_a_n = int((sel_dx & (~sel_full)).sum())
        only_a_cases = int(((sel_dx & (~sel_full)) & (true_cases == 1)).sum())
        only_b_n = int(((~sel_dx) & sel_full).sum())
        only_b_cases = int((((~sel_dx) & sel_full) & (true_cases == 1)).sum())

        lookup_rows.append({
            "capacity_pct": k_pct,
            "k_screened": k_pick,
            # Model A
            "found_a": found_a,
            "sens_a": round(sens_a * 100, 2),
            "ppv_a": round(ppv_a * 100, 2),
            "nns_a": round(nns_a, 1) if not np.isnan(nns_a) else None,
            # Model B
            "found_b": found_b,
            "sens_b": round(sens_b * 100, 2),
            "ppv_b": round(ppv_b * 100, 2),
            "nns_b": round(nns_b, 1) if not np.isnan(nns_b) else None,
            # Random
            "found_rand": round(exp_found, 1),
            "sens_rand": round(exp_sens * 100, 2),
            "ppv_rand": round(exp_ppv * 100, 2),
            "nns_rand": round(exp_nns, 1),
            # Boundary Swaps
            "consensus_n": consensus_n,
            "consensus_cases": consensus_cases,
            "only_a_n": only_a_n,
            "only_a_cases": only_a_cases,
            "only_b_n": only_b_n,
            "only_b_cases": only_b_cases,
        })

    lookup_df = pd.DataFrame(lookup_rows)
    lookup_df.to_parquet(data_dir / "capacity_curve_lookup.parquet", index=False)
    print("Saved capacity_curve_lookup.parquet (100 pre-computed budget rows).")

    # 5. Convert data dictionary to JSON.
    dict_csv = PROJECT_ROOT / "reports" / "data_dictionary.csv"
    if dict_csv.exists():
        dict_df = pd.read_csv(dict_csv)
        dict_records = dict_df.to_dict(orient="records")
        with open(data_dir / "nhanes_dictionary.json", "w", encoding="utf-8") as f:
            json.dump(dict_records, f, indent=2)
        print("Saved nhanes_dictionary.json.")

    print("All app data assets successfully prepared.")

if __name__ == "__main__":
    main()
