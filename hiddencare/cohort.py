# Functions for cohort selection, label construction, and flow reporting.

import pandas as pd


# Build primary paired cohort and construct target and audit variables.
def build_cohort(
    df: pd.DataFrame,
    min_age: int = 20,
    a1c_threshold: float = 6.5,
    exclude_pregnancy_code: float = 1.0,
) -> pd.DataFrame:
    # Filter by age, explicit diagnosis response, valid HbA1c, positive weight, and non-pregnancy.
    mask = (
        (df["age"] >= min_age)
        & df["dx"].isin([1, 2])
        & df["a1c"].notna()
        & (df["weight"] > 0)
        & (df["prg"].isna() | (df["prg"] != exclude_pregnancy_code))
    )
    cohort = df.loc[mask].copy()

    # Define the two comparison outcomes.
    cohort["label_dx"] = (cohort["dx"] == 1).astype(int)
    cohort["label_full"] = ((cohort["dx"] == 1) | (cohort["a1c"] >= a1c_threshold)).astype(int)

    # Recode health insurance status for auditing.
    cohort["insured"] = "unknown"
    cohort.loc[cohort["hiq"] == 1, "insured"] = "insured"
    cohort.loc[cohort["hiq"] == 2, "insured"] = "uninsured"

    # Recode poverty income ratio into pre-declared categories.
    cohort["pir_group"] = "missing"
    cohort.loc[cohort["pir"].notna() & (cohort["pir"] < 1.30), "pir_group"] = "low"
    cohort.loc[
        cohort["pir"].notna() & (cohort["pir"] >= 1.30) & (cohort["pir"] <= 3.50), "pir_group"
    ] = "middle"
    cohort.loc[cohort["pir"].notna() & (cohort["pir"] > 3.50), "pir_group"] = "high"

    return cohort


# Calculate retention and exclusion counts through each screening step.
def get_cohort_flow(
    df: pd.DataFrame,
    min_age: int = 20,
    exclude_pregnancy_code: float = 1.0,
) -> list[dict]:
    step0 = len(df)
    step1 = int((df["age"] >= min_age).sum())
    step2 = int(((df["age"] >= min_age) & df["dx"].isin([1, 2])).sum())
    step3 = int(((df["age"] >= min_age) & df["dx"].isin([1, 2]) & df["a1c"].notna()).sum())
    step4 = int(
        (
            (df["age"] >= min_age)
            & df["dx"].isin([1, 2])
            & df["a1c"].notna()
            & (df["weight"] > 0)
        ).sum()
    )
    step5 = int(
        (
            (df["age"] >= min_age)
            & df["dx"].isin([1, 2])
            & df["a1c"].notna()
            & (df["weight"] > 0)
            & (df["prg"].isna() | (df["prg"] != exclude_pregnancy_code))
        ).sum()
    )

    return [
        {"step": "Initial participants in DEMO", "n_remaining": step0, "n_excluded": 0},
        {"step": "Adults aged 20 and older", "n_remaining": step1, "n_excluded": step0 - step1},
        {
            "step": "Explicit diagnosis answer (dx 1 or 2)",
            "n_remaining": step2,
            "n_excluded": step1 - step2,
        },
        {
            "step": "Observed venous HbA1c measurement",
            "n_remaining": step3,
            "n_excluded": step2 - step3,
        },
        {"step": "Positive survey analysis weight", "n_remaining": step4, "n_excluded": step3 - step4},
        {
            "step": "Exclude known pregnancy (final cohort)",
            "n_remaining": step5,
            "n_excluded": step4 - step5,
        },
    ]


# Extract previously undiagnosed adults for the holdout evaluation phase.
def get_evaluation_subset(
    cohort_df: pd.DataFrame,
    a1c_threshold: float = 6.5,
) -> pd.DataFrame:
    eval_df = cohort_df.loc[cohort_df["dx"] == 2].copy()
    eval_df["potential_case"] = (eval_df["a1c"] >= a1c_threshold).astype(int)
    return eval_df
