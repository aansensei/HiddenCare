# Screening decision policy, evaluation metrics, and subgroup auditing.

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score


# Allocate screening by ranking scores descending and breaking ties by sequence number ascending.
def allocate_screening(
    scores: np.ndarray,
    seqns: np.ndarray,
    capacity_frac: float,
) -> np.ndarray:
    n = len(scores)
    n_pick = int(np.floor(capacity_frac * n))

    # Construct structured array for stable sorting with deterministic tie-breaking.
    # Negate scores so sorting ascending yields highest scores first.
    sort_keys = np.lexsort((seqns, -scores))
    selected_indices = sort_keys[:n_pick]

    selected = np.zeros(n, dtype=bool)
    selected[selected_indices] = True
    return selected


# Compute standard screening metrics for unweighted and survey weighted samples.
def compute_screening_metrics(
    selected: np.ndarray,
    true_cases: np.ndarray,
    scores: Optional[np.ndarray] = None,
    weights: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    n_eval = len(true_cases)
    n_pick = int(selected.sum())
    n_case = int(true_cases.sum())
    n_found = int((selected & (true_cases == 1)).sum())
    n_missed = int(((~selected) & (true_cases == 1)).sum())

    sensitivity = n_found / n_case if n_case > 0 else np.nan
    ppv = n_found / n_pick if n_pick > 0 else np.nan
    nns = n_pick / n_found if n_found > 0 else np.nan

    metrics = {
        "n_eval": n_eval,
        "n_pick": n_pick,
        "n_case": n_case,
        "n_found": n_found,
        "n_missed": n_missed,
        "sensitivity": sensitivity,
        "ppv": ppv,
        "number_needed_to_screen": nns,
    }

    if scores is not None and n_case > 0 and n_case < n_eval:
        metrics["auc_roc"] = float(roc_auc_score(true_cases, scores))
        metrics["avg_precision"] = float(average_precision_score(true_cases, scores))
    else:
        metrics["auc_roc"] = np.nan
        metrics["avg_precision"] = np.nan

    if weights is not None:
        w_total = float(weights.sum())
        w_pick = float(weights[selected].sum())
        w_case = float(weights[true_cases == 1].sum())
        w_found = float(weights[selected & (true_cases == 1)].sum())
        w_missed = float(weights[(~selected) & (true_cases == 1)].sum())

        metrics["weighted_n_eval"] = w_total
        metrics["weighted_n_pick"] = w_pick
        metrics["weighted_n_case"] = w_case
        metrics["weighted_n_found"] = w_found
        metrics["weighted_n_missed"] = w_missed
        metrics["weighted_sensitivity"] = w_found / w_case if w_case > 0 else np.nan
        metrics["weighted_ppv"] = w_found / w_pick if w_pick > 0 else np.nan
        metrics["weighted_nns"] = w_pick / w_found if w_found > 0 else np.nan

    return metrics


# Compare policy overlap between Model A and Model B under identical capacity.
def compare_paired_policies(
    selected_dx: np.ndarray,
    selected_full: np.ndarray,
    true_cases: np.ndarray,
) -> pd.DataFrame:
    groups = {
        "Selected by Both Models": selected_dx & selected_full,
        "Selected Only by Diagnosis Model": selected_dx & (~selected_full),
        "Selected Only by Combined Model": (~selected_dx) & selected_full,
        "Selected by Neither Model": (~selected_dx) & (~selected_full),
    }

    rows = []
    for group_name, mask in groups.items():
        n_group = int(mask.sum())
        n_pos = int((mask & (true_cases == 1)).sum())
        pct_pos = (n_pos / n_group * 100) if n_group > 0 else 0.0
        rows.append(
            {
                "policy_group": group_name,
                "n_participants": n_group,
                "n_potential_cases": n_pos,
                "positivity_rate_pct": round(pct_pos, 2),
            }
        )
    return pd.DataFrame(rows)


# Audit screening performance across pre-declared sociodemographic subgroups.
def audit_by_subgroup(
    eval_df: pd.DataFrame,
    selected: np.ndarray,
    subgroup_col: str,
) -> pd.DataFrame:
    df = eval_df.copy()
    df["selected"] = selected
    true_cases = df["potential_case"].values

    rows = []
    for group_val, grp in df.groupby(subgroup_col, dropna=False):
        grp_selected = grp["selected"].values
        grp_cases = grp["potential_case"].values

        n_eval = len(grp)
        n_case = int(grp_cases.sum())
        n_pick = int(grp_selected.sum())
        n_found = int((grp_selected & (grp_cases == 1)).sum())
        n_missed = int(((~grp_selected) & (grp_cases == 1)).sum())

        sensitivity = (n_found / n_case) if n_case > 0 else np.nan
        ppv = (n_found / n_pick) if n_pick > 0 else np.nan

        rows.append(
            {
                "subgroup": subgroup_col,
                "category": str(group_val),
                "n_eval": n_eval,
                "n_case": n_case,
                "n_pick": n_pick,
                "n_found": n_found,
                "n_missed": n_missed,
                "sensitivity": sensitivity,
                "ppv": ppv,
            }
        )
    return pd.DataFrame(rows)


# Calculate expected and simulated baseline performance under random selection.
def compute_random_baseline(
    true_cases: np.ndarray,
    capacity_frac: float,
    n_sim: int = 1000,
    seed: int = 42,
) -> Dict[str, Any]:
    n_eval = len(true_cases)
    n_case = int(true_cases.sum())
    n_pick = int(np.floor(capacity_frac * n_eval))

    expected_found = capacity_frac * n_case
    expected_ppv = n_case / n_eval if n_eval > 0 else np.nan
    expected_sensitivity = capacity_frac

    rng = np.random.default_rng(seed)
    sim_found = []
    for _ in range(n_sim):
        sampled_indices = rng.choice(n_eval, size=n_pick, replace=False)
        sim_found.append(int(true_cases[sampled_indices].sum()))

    sim_found = np.array(sim_found)
    return {
        "n_eval": n_eval,
        "n_pick": n_pick,
        "n_case": n_case,
        "expected_found": expected_found,
        "expected_sensitivity": expected_sensitivity,
        "expected_ppv": expected_ppv,
        "sim_found_mean": float(sim_found.mean()),
        "sim_found_p025": float(np.percentile(sim_found, 2.5)),
        "sim_found_p975": float(np.percentile(sim_found, 97.5)),
    }
