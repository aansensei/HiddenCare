# NHANES Cross-Cycle Data Quality & Schema Drift Audit

Audit Status: PASSED

## 1. Sample Sizes

* Pre-pandemic Development Cohort: N = 7,761
* Post-pandemic Evaluation Cohort: N = 4,698

## 2. Missingness Rate Comparison

| Feature | Pre-Pandemic (%) | Post-Pandemic (%) | Absolute Delta (%) | Warning |
| :--- | :--- | :--- | :--- | :--- |
| `bmi` | 1.62% | 1.21% | 0.41% | False |
| `waist` | 4.75% | 3.96% | 0.79% | False |
| `pir` | 13.59% | 12.79% | 0.8% | False |

## 3. Population Distribution Stability (PSI & KS Test)

| Feature | KS Stat | p-value | PSI Score | Stability Assessment |
| :--- | :--- | :--- | :--- | :--- |
| `age` | 0.0555 | 0.0 | 0.0309 | **STABLE** |
| `a1c` | 0.1489 | 0.0 | 0.275 | **SIGNIFICANT_SHIFT** |
| `bmi` | 0.0635 | 0.0 | 0.0195 | **STABLE** |
| `waist` | 0.0494 | 0.0 | 0.0175 | **STABLE** |
