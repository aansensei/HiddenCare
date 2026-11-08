# Automated Testing Suite (`tests/`)

This directory contains the unit tests and data verification suites that ensure statistical reproducibility, schema integrity, and model safety across HiddenCare.

## Testing Overview

* **Framework:** Standard `pytest` test suite with 12 unit tests.
* **Execution Time:** Runs locally and in automated pipelines in under 5 seconds.
* **Coverage Scope:** Covers cohort exclusion logic, supervision label definitions, screening arithmetic, feature leakage guards, DuckDB lakehouse queries, Pandera data contracts, and complex survey variance.

## Test Suite Summary

| Test File | Primary Scope | Critical Invariant Tested |
| :--- | :--- | :--- |
| `test_cohort.py` | Epidemiological cohort inclusion/exclusion | Rejection of minors, pregnancy exclusion, and valid survey weights |
| `test_labels.py` | Ground truth label assignment | Correct separation of administrative proxy vs biological biomarker targets |
| `test_metrics.py` | Capacity allocation and leakage protection | Arithmetic accuracy and strict assertion barring lab features from models |
| `test_lakehouse.py` | Embedded DuckDB SQL queries | In-memory query execution and schema integrity |
| `test_contracts.py` | Pandera schema validation and drift | Biological boundary checks, pregnancy rejection, and PSI accuracy |
| `test_survey_stats.py` | Taylor Series Linearization | Clustered survey variance calculation and degrees of freedom |

## Detailed File Guide

### `test_cohort.py` (Cohort Exclusion Logic)
* **What it tests:** Validates that CDC NHANES filtering functions correctly identify eligible participants on synthetic edge-case records.
* **Key test cases:**
  * `test_exclusion_criteria_on_synthetic_data`: Verifies participants younger than 20, individuals with missing lab tests, and pregnant individuals (code 1.0) are correctly removed.
  * `test_no_male_or_untested_female_exclusion`: Verifies that adult males and non-pregnant females pass through without erroneous drop-off.

### `test_labels.py` (Label Formulation Verification)
* **What it tests:** Verifies that synthetic records receive exact expected labels under Model A and Model B definitions.
* **Key test cases:**
  * Confirms an undiagnosed patient with an elevated HbA1c (>= 6.5%) receives `label_a = 0` (missed by proxy) but `label_b = 1` (detected by biomarker ground truth).
  * Confirms healthy participants receive 0 for both labels, and previously diagnosed participants receive 1 for both.

### `test_metrics.py` (Screening Metrics and Feature Safety Guard)
* **What it tests:** Validates ranking arithmetic, tie-breaking mechanisms, and feature set boundaries.
* **Key test cases:**
  * Checks cumulative sensitivity, specificity, and NNS calculations against manual baselines.
  * Verifies deterministic ranking and tie-breaking at capacity thresholds.
  * **Critical Safety Guard (`test_forbidden_predictor_assertion`):** Explicitly asserts that neither `a1c`, `glycohemoglobin`, nor diagnostic markers exist in the model predictor columns, preventing accidental data leakage during future development.

### `test_lakehouse.py` (DuckDB Lakehouse Verification)
* **What it tests:** Verifies SQL query compilation and data extraction in DuckDB.
* **Key test cases:**
  * Confirms that in-memory DuckDB connections create tables and aggregate metrics without errors.
  * Validates the schema and row integrity of health equity SQL aggregations across survey cycles.

### `test_contracts.py` (Pandera Data Contracts and Drift Metrics)
* **What it tests:** Validates schema models and statistical distribution drift calculations.
* **Key test cases:**
  * Checks valid cohorts against `NHANESCohortSchema`.
  * Verifies schema rejection when a record with pregnancy code 1.0 is introduced.
  * Asserts that `calculate_psi` returns exactly 0.0 for identical distributions.

### `test_survey_stats.py` (Complex Survey Variance Estimation)
* **What it tests:** Verifies CDC/NCHS Taylor Series Linearization variance calculations.
* **Key test cases:**
  * Tests survey ratio standard error estimation on synthetic multi-stage clustered survey data.
  * Verifies that degrees of freedom equal total primary sampling units minus total strata (`total_psus minus total_strata`).

## How to Run Tests

Execute the full suite from the repository root:
```powershell
pytest tests/ -v
```
All 12 tests should pass with exit code 0.
