# Data Assets and Storage (`data/`)

This directory stores the analytical cohorts, lookup tables, and data dictionaries used by HiddenCare.

## Data Organization

* **Raw Data (`data/raw/`):** Original CDC NHANES SAS transport files (.XPT), tracked separately and excluded from git via `.gitignore`.
* **Processed Cohorts (`data/processed/`):** Cleaned, filtered Parquet cohorts with verified sample sizes.
* **Lookup Tables (`data/*.parquet`):** Precomputed evaluation tables enabling microsecond response times in the interactive web simulator.

## File Summary

| File / Subdirectory | Format | Role |
| :--- | :--- | :--- |
| `processed/cohort_train.parquet` | Parquet | Pre-pandemic training cohort (2017 to March 2020, N = 7,761) |
| `processed/eval_subset.parquet` | Parquet | Post-pandemic holdout evaluation cohort of undiagnosed adults (2021 to 2023, N = 4,698) |
| `capacity_curve_lookup.parquet` | Parquet | Precomputed screening metrics across capacity thresholds from 5% to 50% |
| `holdout_2021_2023.parquet` | Parquet | Patient-level holdout risk scores and true biomarker labels |
| `margin_swap_61.parquet` | Parquet | Micro-level records of the 61 individuals who swap triage priority at 20% budget |
| `nhanes_dictionary.json` | JSON | Machine-readable variable definitions and CDC codebook mappings |
| `verified_constants.py` | Python | Hardened sample size constants and analytical validation thresholds |
| `hiddencare.duckdb` | DuckDB | Embedded analytical lakehouse database (local storage, excluded from git) |

## Data Pipeline Flow

1. Raw CDC SAS files (.XPT) are downloaded into `data/raw/` or read via `hiddencare/lakehouse.py`.
2. Inclusion and exclusion criteria are applied, producing `data/processed/cohort_train.parquet` and `data/processed/eval_subset.parquet`.
3. Models are trained, and predictions on the holdout cohort are exported as lookup tables to power the web simulator without runtime latency.
