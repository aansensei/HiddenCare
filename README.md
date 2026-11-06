---
title: HiddenCare - Population Screening & Label Bias Lab
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.31.0
app_file: app.py
pinned: true
license: mit
short_description: Empirical CDC NHANES study on proxy label bias in population screening
---

# HiddenCare

Evaluating Proxy Outcome Bias in Algorithmic Diabetes Screening Under Capacity Constraints

Author: An Nguyen (AanSensei)  
Institution: University of Wisconsin-Madison (B.S. Economics & Data Science)  
Target: Weill Cornell Biostatistics Summer Internship 2027  
Repository: https://github.com/aansensei/HiddenCare.git  
Interactive Platform: Hugging Face Spaces (Gradio 5.x/6.x Blocks)  

## Overview

In machine learning applications for public health, predictive models frequently train on self-reported clinical history or administrative diagnostic billing codes. These proxy outcomes confound biological risk with historic healthcare access.

HiddenCare demonstrates this phenomenon through a reproducible empirical experiment using public data from the CDC National Health and Nutrition Examination Survey (NHANES). We compare two regularized logistic regression models using identical baseline predictors (age, gender, BMI, waist circumference) on a pre-pandemic development cohort (2017 to March 2020; N = 7,761):
- Model A (Diagnosis Only): Trained on self-reported clinical diagnosis (Label A).
- Model B (Combined): Trained on self-reported diagnosis combined with laboratory HbA1c of 6.5 percent or higher (Label B).

Both models are evaluated on a locked, non-overlapping holdout of previously undiagnosed adults from the post-pandemic cycle (August 2021 to August 2023; N = 4,698; 116 potential cases with HbA1c >= 6.5%).

Under a primary fixed screening capacity of 20 percent (939 participants screened):
- Model A detects 53 potential cases (sensitivity 45.7%, PPV 5.64%).
- Model B detects 55 potential cases (sensitivity 47.4%, PPV 5.86%).
- Random allocation detects an expected 23.2 cases (95% simulation interval: 15 to 32 cases).
- Paired disagreement analysis reveals that participants prioritized exclusively by Model B have a threefold higher positivity yield (4.92%) than participants prioritized exclusively by Model A (1.64%).

## Repository Structure

```text
HiddenCare/
  README.md
  requirements.txt
  pytest.ini
  run.py
  hiddencare/
    __init__.py
    config.py
    data.py
    cohort.py
    models.py
    metrics.py
    plots.py
  tests/
    test_labels.py
    test_cohort.py
    test_metrics.py
  data/
    raw/
      pre_pandemic/
      post_pandemic/
    processed/
      cohort_train.parquet
      eval_subset.parquet
  outputs/
    tables/
      cohort_flow.csv
      tuning_summary.csv
      metrics_summary.csv
      random_baseline_summary.csv
      paired_overlap_20pct.csv
      subgroup_audit_20pct.csv
    figures/
      capacity_tradeoff.png
      paired_overlap_20pct.png
      subgroup_audit_insurance.png
      subgroup_audit_income.png
    models/
      model_dx.joblib
      model_full.joblib
  reports/
    protocol.md
    data_dictionary.csv
    sources.md
    brief.md
```

## Setup and Reproduction

### 1. Requirements

The project uses Python 3.10 or higher. Install the verified dependencies:

```bash
pip install -r requirements.txt
```

Core dependencies:
- pandas (>= 2.2)
- numpy (>= 1.26)
- scikit-learn (>= 1.5)
- matplotlib (>= 3.8)
- pytest (>= 8.0)

### 2. Running Unit Tests

Run the full test suite verifying cohort eligibility, label logic, allocation rules, tie breaking, and leakage assertions:

```bash
python -m pytest -v tests/
```

### 3. Running the Analysis Pipeline

Execute the end-to-end workflow:

```bash
python run.py
```

The pipeline automatically:
1. Downloads and validates all 10 raw NHANES SAS transport files from CDC servers.
2. Merges component tables and verifies participant sequence numbers.
3. Builds development and evaluation cohorts and records attrition flow.
4. Tunes and trains regularized Logistic Regression models using stratified cross-validation.
5. Evaluates models on the locked holdout across 10%, 20%, and 30% screening capacities.
6. Conducts paired policy concordance and sociodemographic subgroup audits.
7. Saves all summary tables to `outputs/tables/` and publication figures to `outputs/figures/`.

### 4. Launching the Interactive Policy Simulation Web Platform

To launch the interactive clinical research dashboard locally:

```bash
python app.py
```

Open `http://localhost:7860` in any modern web browser to interactively adjust screening capacity budgets (5% to 50%), inspect the 61-person marginal disagreement cohort, review health equity sensitivity gaps, and simulate Net Monetary Benefit (NMB) via Decision Curve Analysis.

When synced or pushed to Hugging Face Spaces, the platform launches automatically using the native Gradio SDK configuration defined in the repository header.

## Key Findings

### Screening Yield Under 20% Resource Capacity

| Model | Evaluated | Screened | True Cases | Found | Missed | Sensitivity | PPV | NNS | ROC AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Random Allocation | 4,698 | 939 | 116 | 23.2 | 92.8 | 20.0% | 2.47% | 40.5 | 0.5000 |
| Model A (Diagnosis Only) | 4,698 | 939 | 116 | 53 | 63 | 45.7% | 5.64% | 17.7 | 0.7300 |
| Model B (Combined) | 4,698 | 939 | 116 | 55 | 61 | 47.4% | 5.86% | 17.1 | 0.7410 |

### Paired Agreement and Disagreement at 20% Capacity

| Screening Decision Group | Participants | Potential Cases | Positivity Rate |
| :--- | :--- | :--- | :--- |
| Selected by Both Models | 878 | 52 | 5.92% |
| Selected Only by Diagnosis Model | 61 | 1 | 1.64% |
| Selected Only by Combined Model | 61 | 3 | 4.92% |
| Selected by Neither Model | 3,698 | 60 | 1.62% |

### Subgroup Audit by Insurance Status

| Group | Subgroup N | Total Cases | Model A Found (Sens) | Model B Found (Sens) |
| :--- | :--- | :--- | :--- | :--- |
| Insured | 4,268 | 102 | 51 (50.0%) | 52 (51.0%) |
| Uninsured | 422 | 13 | 2 (15.4%) | 3 (23.1%) |
| Unknown | 8 | 1 | 0 (0.0%) | 0 (0.0%) |

## Methodological Boundaries and Causal Limitations

1. Non-causal Observational Data: Observational differences in prioritization between models describe shifts in proxy learning. They do not demonstrate that health insurance or income causally causes elevated HbA1c or missed screening.
2. Screening Criterion vs Clinical Diagnosis: In cross-sectional surveys like NHANES, a single HbA1c measurement above 6.5 percent is an epidemiological screening criterion. Clinical diagnostic confirmation requires repeat laboratory testing.
3. Subgroup Sample Constraints: The uninsured evaluation cohort contains only 13 potential cases, and the unknown insurance group contains only 8 participants. These sample constraints must be transparently disclosed to avoid overbroad claims regarding algorithmic fairness.

## License

This project is prepared as an academic research study for student portfolio and internship application purposes.
