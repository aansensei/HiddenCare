"""
Single Source of Truth: Verified CDC NHANES Empirical Findings for HiddenCare.
All numbers are derived directly from the executed NHANES 2017-2023 pipeline.
"""

COHORT_METRICS = {
    "dev_cohort": {
        "cycle": "2017–March 2020 (Pre-Pandemic)",
        "n_total": 7_761,
        "label_a_pos": 1_257,
        "label_a_prev": 0.1620,
        "label_b_pos": 1_484,
        "label_b_prev": 0.1912,
        "hidden_cases": 227,
    },
    "holdout_cohort": {
        "cycle": "2021–2023 (Strictly Undiagnosed Adults)",
        "n_total": 4_698,
        "latent_cases": 116,
        "latent_prev": 0.0247,
        "roc_auc_a": 0.7300,
        "roc_auc_b": 0.7410,
        "pr_auc_a": 0.0548,
        "pr_auc_b": 0.0566,
    },
    "benchmark_20pct": {
        "capacity_pct": 20,
        "k_screened": 939,
        "random": {"cases": 23.2, "sens": 0.200, "ppv": 0.0247, "nns": 40.5},
        "model_a": {"cases": 53, "sens": 0.457, "ppv": 0.0564, "nns": 17.7},
        "model_b": {"cases": 55, "sens": 0.474, "ppv": 0.0586, "nns": 17.1},
        "consensus": {"n": 878, "cases": 52, "ppv": 0.0592},
        "only_a": {"n": 61, "cases": 1, "ppv": 0.0164},
        "only_b": {"n": 61, "cases": 3, "ppv": 0.0492},
        "neither": {"n": 3_698, "cases": 60, "ppv": 0.0162},
    },
    "equity_20pct": {
        "insured": {
            "n_total": 4_268,
            "latent_cases": 102,
            "cases_a": 51,
            "sens_a": 0.500,
            "cases_b": 52,
            "sens_b": 0.510,
        },
        "uninsured": {
            "n_total": 422,
            "latent_cases": 13,
            "cases_a": 2,
            "sens_a": 0.154,
            "cases_b": 3,
            "sens_b": 0.231,
        },
        "unknown": {
            "n_total": 8,
            "latent_cases": 1,
            "cases_a": 0,
            "sens_a": 0.0,
            "cases_b": 0,
            "sens_b": 0.0,
        },
    },
}
