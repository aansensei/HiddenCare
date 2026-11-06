# High performance calculation engine for screening simulation and health economics.

from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Load pre-computed lookup tables and holdout predictions.
LOOKUP_DF = pd.read_parquet(DATA_DIR / "capacity_curve_lookup.parquet")
HOLDOUT_DF = pd.read_parquet(DATA_DIR / "holdout_2021_2023.parquet")
SWAP_DF = pd.read_parquet(DATA_DIR / "margin_swap_61.parquet")


# Instant O(1) lookup of screening performance metrics at any capacity percentage.
def evaluate_budget_capacity(capacity_pct: int) -> Dict[str, Any]:
    cap = max(1, min(100, int(capacity_pct)))
    row = LOOKUP_DF.loc[LOOKUP_DF["capacity_pct"] == cap].iloc[0].to_dict()
    return row


# Compute health economic metrics and incremental net monetary benefit.
def compute_economic_nmb(
    capacity_pct: int,
    cost_test: float = 25.0,
    benefit_early: float = 8500.0,
) -> Dict[str, Any]:
    metrics = evaluate_budget_capacity(capacity_pct)
    k_screened = metrics["k_screened"]
    found_a = metrics["found_a"]
    found_b = metrics["found_b"]
    found_rand = metrics["found_rand"]
    n_eval = 4698

    total_cost = k_screened * cost_test

    cost_per_case_a = (total_cost / found_a) if found_a > 0 else np.nan
    cost_per_case_b = (total_cost / found_b) if found_b > 0 else np.nan
    cost_per_case_rand = (total_cost / found_rand) if found_rand > 0 else np.nan

    nmb_a = (found_a * benefit_early) - total_cost
    nmb_b = (found_b * benefit_early) - total_cost
    nmb_rand = (found_rand * benefit_early) - total_cost

    incremental_cases = found_b - found_a
    incremental_nmb = incremental_cases * benefit_early

    # Standardize to a reference population of 10,000 undiagnosed adults.
    scale = 10000.0 / n_eval
    cases_rescued_10k = incremental_cases * scale
    nmb_gain_10k = incremental_nmb * scale

    return {
        "capacity_pct": capacity_pct,
        "k_screened": k_screened,
        "total_cost": total_cost,
        "cost_per_case_a": cost_per_case_a,
        "cost_per_case_b": cost_per_case_b,
        "cost_per_case_rand": cost_per_case_rand,
        "nmb_a": nmb_a,
        "nmb_b": nmb_b,
        "nmb_rand": nmb_rand,
        "incremental_cases": incremental_cases,
        "incremental_nmb": incremental_nmb,
        "cases_rescued_10k": cases_rescued_10k,
        "nmb_gain_10k": nmb_gain_10k,
    }


# Compute decision curve analysis comparing Model A and Model B across clinical risk thresholds.
def compute_decision_curve(
    p_t_range: np.ndarray = np.linspace(0.01, 0.12, 50),
) -> Dict[str, Any]:
    n = len(HOLDOUT_DF)
    y_true = HOLDOUT_DF["potential_case"].values
    prob_a = HOLDOUT_DF["prob_dx"].values
    prob_b = HOLDOUT_DF["prob_full"].values

    nb_a = []
    nb_b = []
    nb_all = []
    nb_none = np.zeros(len(p_t_range))

    n_pos = int(y_true.sum())
    n_neg = n - n_pos

    for pt in p_t_range:
        weight = pt / (1.0 - pt)

        # Model A
        pred_a = (prob_a >= pt)
        tp_a = int((pred_a & (y_true == 1)).sum())
        fp_a = int((pred_a & (y_true == 0)).sum())
        nb_a.append((tp_a / n) - (fp_a / n) * weight)

        # Model B
        pred_b = (prob_b >= pt)
        tp_b = int((pred_b & (y_true == 1)).sum())
        fp_b = int((pred_b & (y_true == 0)).sum())
        nb_b.append((tp_b / n) - (fp_b / n) * weight)

        # Treat All
        nb_all.append((n_pos / n) - (n_neg / n) * weight)

    return {
        "thresholds": p_t_range,
        "net_benefit_a": np.array(nb_a),
        "net_benefit_b": np.array(nb_b),
        "net_benefit_all": np.array(nb_all),
        "net_benefit_none": nb_none,
    }
