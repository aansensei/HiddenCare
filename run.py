# Main orchestration pipeline for HiddenCare analysis.

import sys
from pathlib import Path
import pandas as pd
import joblib

# Ensure repository root is on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from hiddencare.config import (
    PATHS,
    URLS,
    SEED,
    MIN_AGE,
    A1C_THRESHOLD,
    EXCLUDE_PREGNANCY_CODE,
    CAPACITIES,
    PRIMARY_CAPACITY,
    PREDICTORS,
    C_GRID,
    CV_FOLDS,
)
from hiddencare.data import (
    download_cycle_files,
    load_pre_pandemic_data,
    load_post_pandemic_data,
)
from hiddencare.cohort import (
    build_cohort,
    get_cohort_flow,
    get_evaluation_subset,
)
from hiddencare.models import (
    tune_and_fit_model,
    predict_positive_risk,
)
from hiddencare.metrics import (
    allocate_screening,
    compute_screening_metrics,
    compare_paired_policies,
    audit_by_subgroup,
    compute_random_baseline,
)
from hiddencare.plots import (
    plot_capacity_tradeoff,
    plot_paired_overlap,
    plot_subgroup_audit,
)


def run_pipeline():
    print("=" * 60)
    print("Starting HiddenCare Analysis Pipeline")
    print("=" * 60)

    # 1. Ensure directory structure exists.
    for p in PATHS.values():
        p.mkdir(parents=True, exist_ok=True)

    # 2. Download raw NHANES components if missing.
    print("\n[Step 1/6] Verifying and downloading raw NHANES data...")
    download_cycle_files(URLS["pre_pandemic"], PATHS["raw_pre"])
    download_cycle_files(URLS["post_pandemic"], PATHS["raw_post"])
    print("All raw components verified.")

    # 3. Load and merge component files.
    print("\n[Step 2/6] Loading and merging component tables...")
    raw_pre = load_pre_pandemic_data(PATHS["raw_pre"])
    raw_post = load_post_pandemic_data(PATHS["raw_post"])
    print(f"Pre-pandemic raw participants: {len(raw_pre):,}")
    print(f"Post-pandemic raw participants: {len(raw_post):,}")

    # 4. Build cohorts and compute attrition flow.
    print("\n[Step 3/6] Applying eligibility criteria and building cohorts...")
    flow_pre = get_cohort_flow(raw_pre, MIN_AGE, EXCLUDE_PREGNANCY_CODE)
    flow_post = get_cohort_flow(raw_post, MIN_AGE, EXCLUDE_PREGNANCY_CODE)

    flow_df = pd.DataFrame(
        [
            {**row, "cycle": "Pre-pandemic (2017 to March 2020)"}
            for row in flow_pre
        ]
        + [
            {**row, "cycle": "Post-pandemic (2021 to 2023)"}
            for row in flow_post
        ]
    )
    flow_df.to_csv(PATHS["tables"] / "cohort_flow.csv", index=False)
    print("Cohort flow table saved.")

    cohort_train = build_cohort(raw_pre, MIN_AGE, A1C_THRESHOLD, EXCLUDE_PREGNANCY_CODE)
    cohort_eval = build_cohort(raw_post, MIN_AGE, A1C_THRESHOLD, EXCLUDE_PREGNANCY_CODE)
    print(f"Final training cohort size: {len(cohort_train):,}")
    print(f"Final evaluation cohort size: {len(cohort_eval):,}")

    # Feasibility gate check.
    eval_subset = get_evaluation_subset(cohort_eval, A1C_THRESHOLD)
    n_potential_cases = int(eval_subset["potential_case"].sum())
    print(f"\nFeasibility Check on Evaluation Subset (Previously Undiagnosed):")
    print(f"Total previously undiagnosed adults: {len(eval_subset):,}")
    print(f"Potential undiagnosed cases (HbA1c >= 6.5%): {n_potential_cases:,} ({n_potential_cases / len(eval_subset) * 100:.2f}%)")

    # Save processed cohort data.
    cohort_train.to_parquet(PATHS["processed"] / "cohort_train.parquet", index=False)
    eval_subset.to_parquet(PATHS["processed"] / "eval_subset.parquet", index=False)

    # 5. Model training on development release only.
    print("\n[Step 4/6] Tuning and training models on pre-pandemic release...")
    print("Training Model A (Diagnosis Only, Label A)...")
    pipe_dx, tune_dx = tune_and_fit_model(
        cohort_train, "label_dx", PREDICTORS, C_GRID, CV_FOLDS, SEED
    )
    print(f"Model A Best C: {tune_dx['best_C']}, Best CV ROC AUC: {tune_dx['best_cv_roc_auc']:.4f}")

    print("Training Model B (Combined Diagnosis + Lab, Label B)...")
    pipe_full, tune_full = tune_and_fit_model(
        cohort_train, "label_full", PREDICTORS, C_GRID, CV_FOLDS, SEED
    )
    print(f"Model B Best C: {tune_full['best_C']}, Best CV ROC AUC: {tune_full['best_cv_roc_auc']:.4f}")

    joblib.dump(pipe_dx, PATHS["models"] / "model_dx.joblib")
    joblib.dump(pipe_full, PATHS["models"] / "model_full.joblib")

    tuning_df = pd.DataFrame(
        [
            {"model": "Diagnosis Only (Label A)", "best_C": tune_dx["best_C"], "cv_roc_auc": tune_dx["best_cv_roc_auc"]},
            {"model": "Combined (Label B)", "best_C": tune_full["best_C"], "cv_roc_auc": tune_full["best_cv_roc_auc"]},
        ]
    )
    tuning_df.to_csv(PATHS["tables"] / "tuning_summary.csv", index=False)

    # 6. Evaluate on locked holdout evaluation release.
    print("\n[Step 5/6] Evaluating on locked post-pandemic holdout...")
    eval_seqns = eval_subset["seqn"].values
    true_cases = eval_subset["potential_case"].values.astype(int)
    eval_weights = eval_subset["weight"].values

    prob_dx = predict_positive_risk(pipe_dx, eval_subset, PREDICTORS)
    prob_full = predict_positive_risk(pipe_full, eval_subset, PREDICTORS)

    eval_subset["prob_dx"] = prob_dx
    eval_subset["prob_full"] = prob_full

    metrics_records = []
    random_records = []

    for cap in CAPACITIES:
        # Screen with Model A.
        sel_dx = allocate_screening(prob_dx, eval_seqns, cap)
        m_dx = compute_screening_metrics(sel_dx, true_cases, prob_dx, eval_weights)
        metrics_records.append(
            {"model": "Diagnosis Only (Label A)", "capacity": cap, **m_dx}
        )

        # Screen with Model B.
        sel_full = allocate_screening(prob_full, eval_seqns, cap)
        m_full = compute_screening_metrics(sel_full, true_cases, prob_full, eval_weights)
        metrics_records.append(
            {"model": "Combined (Label B)", "capacity": cap, **m_full}
        )

        # Random baseline.
        rand_res = compute_random_baseline(true_cases, cap, n_sim=1000, seed=SEED)
        random_records.append({"capacity": cap, **rand_res})

    metrics_df = pd.DataFrame(metrics_records)
    random_df = pd.DataFrame(random_records)

    metrics_df.to_csv(PATHS["tables"] / "metrics_summary.csv", index=False)
    random_df.to_csv(PATHS["tables"] / "random_baseline_summary.csv", index=False)
    print("Metrics summary saved.")

    # 7. Paired overlap analysis and subgroup audit at primary 20% capacity.
    print(f"\n[Step 6/6] Conducting paired overlap and subgroup audit at primary {int(PRIMARY_CAPACITY*100)}% capacity...")
    sel_dx_20 = allocate_screening(prob_dx, eval_seqns, PRIMARY_CAPACITY)
    sel_full_20 = allocate_screening(prob_full, eval_seqns, PRIMARY_CAPACITY)

    overlap_df = compare_paired_policies(sel_dx_20, sel_full_20, true_cases)
    overlap_df.to_csv(PATHS["tables"] / "paired_overlap_20pct.csv", index=False)
    print("\nPolicy Overlap Table at 20% Capacity:")
    print(overlap_df.to_string(index=False))

    audit_ins_dx = audit_by_subgroup(eval_subset, sel_dx_20, "insured")
    audit_ins_dx["model"] = "Diagnosis Only (Label A)"

    audit_ins_full = audit_by_subgroup(eval_subset, sel_full_20, "insured")
    audit_ins_full["model"] = "Combined (Label B)"

    audit_pir_dx = audit_by_subgroup(eval_subset, sel_dx_20, "pir_group")
    audit_pir_dx["model"] = "Diagnosis Only (Label A)"

    audit_pir_full = audit_by_subgroup(eval_subset, sel_full_20, "pir_group")
    audit_pir_full["model"] = "Combined (Label B)"

    audit_all = pd.concat([audit_ins_dx, audit_ins_full, audit_pir_dx, audit_pir_full], ignore_index=True)
    audit_all.to_csv(PATHS["tables"] / "subgroup_audit_20pct.csv", index=False)

    # 8. Generate figures.
    plot_capacity_tradeoff(
        metrics_df, random_df, PATHS["figures"] / "capacity_tradeoff.png"
    )
    plot_paired_overlap(
        overlap_df, PATHS["figures"] / "paired_overlap_20pct.png"
    )
    plot_subgroup_audit(
        audit_ins_full, "insured", PATHS["figures"] / "subgroup_audit_insurance.png"
    )
    plot_subgroup_audit(
        audit_pir_full, "pir_group", PATHS["figures"] / "subgroup_audit_income.png"
    )
    print("All figures generated successfully.")

    print("\n" + "=" * 60)
    print("HiddenCare Pipeline Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
