# Data Engineering and Machine Learning Core (`hiddencare/`)

This directory contains the analytical data pipeline, machine learning models, statistical validation suite, and modern orchestration engine powering HiddenCare.

## Architecture Overview

HiddenCare evaluates algorithmic bias in population-level screening by contrasting two training label formulations on CDC NHANES data (N = 12,459 participants):
* **Model A (Administrative Proxy):** Trained solely on self-reported prior doctor diagnosis (`DIQ010 == 1`).
* **Model B (Biomarker Ground Truth):** Trained on confirmed clinical criteria (`DIQ010 == 1` OR laboratory venous HbA1c >= 6.5%).

Both models rely strictly on identical, non-invasive clinical predictors: Age, Sex, BMI, Waist Circumference, and Poverty Income Ratio (PIR). Biomarkers are strictly excluded from the feature set so models only use data available prior to screening blood draws.

## File Summary

| File | Primary Responsibility | Key Functionality |
| :--- | :--- | :--- |
| `cohort.py` | CDC NHANES cohort extraction and filtering | Applies standardized inclusion and exclusion criteria across survey cycles |
| `labels.py` | Screening target label definitions | Constructs Model A (proxy) and Model B (biomarker) supervision signals |
| `models.py` | Model training and hyperparameter configuration | Trains LightGBM / Gradient Boosting classifiers on non-invasive features |
| `metrics.py` | Clinical triage evaluation engine | Computes sensitivity, specificity, NNS, equity ratios, and decision curves |
| `plots.py` | Analytical figure generation | Produces publication-grade charts for research documentation |
| `lakehouse.py` | Embedded DuckDB data lakehouse | Ingests raw SAS transport files (.XPT) and exports columnar Parquet datasets |
| `contracts.py` | Pandera data contracts and drift monitoring | Enforces schema validation and monitors Population Stability Index (PSI) |
| `survey_stats.py` | CDC/NCHS complex survey variance estimation | Implements Taylor Series Linearization for national 95% confidence intervals |
| `robustness.py` | Multi-architecture robustness validation | Validates findings across Random Forest and HistGradientBoosting |
| `orchestration/pipeline.py` | Asset-based DAG orchestration engine | Executes data transformations as a software-defined dependency graph |

## Detailed File Guide

### `cohort.py` (Cohort Ingestion and Epidemiological Filtering)
* **What it does:** Extracts, merges, and filters cross-sectional CDC NHANES examination cycles: pre-pandemic 2017 to March 2020 and post-pandemic 2021 to 2023.
* **Exclusion rules:** Filters adults aged 20 and older, excludes missing biomarker or covariate values, removes pregnant participants, and validates positive examination sample weights (`WTMECPRP` and `WTPH2YR`).
* **Output:** Yields N = 7,761 training participants and N = 4,698 holdout evaluation participants (with 116 confirmed latent diabetes cases).

### `labels.py` (Supervision Label Construction)
* **What it does:** Defines the two competing targets representing the central research question:
  * **Model A Label:** Prior doctor diagnosis only (`DIQ010 == 1`).
  * **Model B Label:** Biological ground truth, combining prior diagnosis with verified laboratory HbA1c of 6.5% or higher (`LBXGH >= 6.5`).
* **Significance:** Illustrates how proxy administrative labels conflate healthcare access with biological disease.

### `models.py` (Non-Invasive Screening Classifiers)
* **What it does:** Configures, tunes, and trains gradient-boosted decision trees predicting screening priority.
* **Feature constraints:** Strictly limited to non-invasive clinical predictors (Age, Sex, BMI, Waist Circumference, PIR). All lab tests and healthcare utilization markers are barred from features.
* **Output:** Produces calibrated risk probability scores used to rank patients for testing priority.

### `metrics.py` (Screening Metrics and Economic Allocation)
* **What it does:** Simulates queue allocation under clinic capacity limits from 5% to 50% of the population.
* **Calculations:** Evaluates cumulative sensitivity, Number Needed to Screen (NNS), the health insurance sensitivity divide, and Decision Curve Net Monetary Benefit.

### `plots.py` (Publication Chart Generation)
* **What it does:** Generates high-resolution matplotlib/seaborn figures used in formal reports, including capacity trade-off curves, 61-patient margin swap distributions, and insurance subgroup audits.

### `lakehouse.py` (Embedded Analytical Lakehouse)
* **What it does:** Leverages DuckDB (`data/hiddencare.duckdb`) to process raw SAS transport files (.XPT) directly with vectorized SQL.
* **Capability:** Performs cohort joins, exclusion logic, and aggregations entirely in-engine, outputting ZSTD-compressed Parquet files in under 2 seconds without external database overhead.

### `contracts.py` (Data Contracts and Schema Drift Gate)
* **What it does:** Implements typed schema validation via Pandera `DataFrameModel` to catch data quality anomalies before pipeline execution.
* **Capabilities:**
  * Enforces biological boundaries (SEQN > 0, Age >= 20, Sex in [1, 2], HbA1c in [2.0, 25.0]).
  * Computes Kolmogorov-Smirnov test statistics and Population Stability Index (PSI) across survey cycles.
  * Verified that non-invasive predictors remained stable across pandemic cycles (PSI < 0.04).

### `survey_stats.py` (Complex Survey Variance Estimation)
* **What it does:** Implements CDC/NCHS Taylor Series Linearization for ratio estimators, accounting for primary sampling units (`SDMVPSU`) and survey strata (`SDMVSTRA`).
* **Significance:** Provides authentic national 95% confidence intervals with 15 degrees of freedom, showing Model B achieves 42.47% sensitivity (95% CI: [28.4%, 56.5%]) at a 20% budget.

### `robustness.py` (Multi-Architecture Validation)
* **What it does:** Evaluates whether findings depend on a specific machine learning model by replicating the triage with Random Forest and HistGradientBoosting.
* **Findings:** Under Random Forest, Model B detects 61 latent cases and boosts uninsured sensitivity from 30.77% to 46.15% (+15.38% equity dividend), proving proxy bias mitigation is algorithm-agnostic.

### `orchestration/pipeline.py` (Asset-Based Lineage DAG)
* **What it does:** Organizes data workflows into software-defined data assets with explicit dependencies, executing end-to-end lineage (raw files -> DuckDB lakehouse -> Pandera contracts -> survey stats -> robustness checks) topologically in 5.52 seconds.
