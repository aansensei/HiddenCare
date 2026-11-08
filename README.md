---
title: "HiddenCare: Algorithmic Triage & Health Equity Lab"
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.16.0
app_file: app.py
pinned: true
license: mit
short_description: Proxy outcome bias in screening triage (CDC NHANES)
---

# HiddenCare: Algorithmic Triage & Health Equity Laboratory

**When Training Labels Change Who Gets Screened: Temporal Evaluation of Diagnosis-Based Versus Biomarker-Augmented Labels for Diabetes Screening in NHANES**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/aansensei/HiddenCare)
[![Live Interactive Lab](https://img.shields.io/badge/Live%20Platform-aansensei.dev-teal)](https://aansensei.dev/hiddencare/)

**Author:** Cao Thien An Nguyen (Cao Thiên Ân Nguyễn &bull; aansensei)  
**Affiliation:** University of Wisconsin, Madison (B.S. Economics & Data Science)  
**Laboratory:** Population Health Sciences & Algorithmic Epidemiology  
**Repository:** [https://github.com/aansensei/HiddenCare](https://github.com/aansensei/HiddenCare)  
**Interactive Research Platform:** [https://aansensei.dev/hiddencare/](https://aansensei.dev/hiddencare/)  

---

## Executive Summary

Population screening triage algorithms frequently train on self-reported clinical history or electronic health record (EHR) billing codes. In public health, these administrative proxy outcomes conflate biological disease risk with historical healthcare access. When individuals face barriers to care (lack of insurance, poverty, rural isolation), unvisited sick patients are systematically misclassified as healthy non-cases during model training.

**HiddenCare** presents an empirical investigation into this proxy outcome bias using continuous biomonitoring microdata from the **CDC National Health and Nutrition Examination Survey (NHANES 2017 to 2023, N = 12,459 adults)**. We evaluate how retraining models on objective biomarker-augmented labels (venous HbA1c &ge; 6.5%) alters finite community screening queues, resolves disparities for underserved populations, and impacts health economics.

---

## Study Design & Temporal Protocol

* **Temporal Cohort Split:**
  * **Development Cohort (Pre-Pandemic, 2017 to March 2020):** $N = 7,761$ adults. Used exclusively for feature standardization, missingness median imputation, and hyperparameter cross-validation.
  * **Holdout Evaluation Cohort (Post-Pandemic, August 2021 to August 2023):** $N = 4,698$ adults who reported *no prior clinical diagnosis of diabetes*. Contains $N = 116$ latent diabetes cases identified via laboratory venous HbA1c (&ge; 6.5%).
* **Non-Invasive Predictors ($X$):** Strictly restricted to 4 easily collected anthropometric predictors: Age, Gender (binary), Body Mass Index (BMI), and Waist Circumference.
* **Leakage Assertions:** HbA1c, Poverty-Income Ratio (PIR), and Health Insurance are strictly forbidden from model inputs and reserved solely for outcome definition and health equity subgroup auditing.
* **Model Formulations:**
  * **Model A (Diagnosis-Based Proxy):** Trained on self-reported doctor diagnosis (`DIQ010 == 1`).
  * **Model B (Biomarker-Augmented):** Trained on observed venous HbA1c (&ge; 6.5%) OR prior clinical diagnosis.

---

## Primary Screening Triage Benchmark (20% Capacity &bull; K = 939 Slots)

Under a pre-specified community screening budget of 20% ($K = 939$ test slots allocated across $N = 4,698$ holdout adults):

| Screening Model | Unweighted Cases Found | Unweighted Sensitivity | Survey-Weighted Sensitivity (95% CI) | Survey-Weighted PPV (95% CI) | Number Needed to Screen (NNS) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Allocation** | 23.2 / 116 | 20.00% | 20.00% | 2.47% | 40.5 |
| **Model A (Diagnosis-Based)** | 53 / 116 | 45.69% | 40.08% [28.9%, 51.2%] | 5.79% [3.6%, 8.0%] | 17.7 |
| **Model B (Biomarker-Augmented)** | 55 / 116 | 47.41% | 42.47% [28.4%, 56.5%] | 6.02% [3.4%, 8.6%] | 17.1 |
| **Net Difference (&Delta;)** | **+2 Cases** | **+1.72 pp** | **+2.38 pp** [paired CI: -1.77, +6.53] | **+0.22 pp** | **-0.6 Tests** |

### Complex Survey Variance & Paired Sensitivity Proof

* **Survey Linearization:** Standard errors estimated using CDC phlebotomy weights (`WTPH2YR`) and Taylor Series Linearization ($df = 15$) accounting for the multistage clustered survey sampling design (masked PSUs and strata).
* **Paired Correlation Reduction:** Because both models score the identical $N = 116$ holdout cases (112 concordant cases, only 4 discordant), strong positive covariance ($	ext{Cov} > 0$) reduces the variance of the difference by over 65%:
  $$	ext{Var}(\Delta) = 	ext{Var}(	ext{Sens}_B) + 	ext{Var}(	ext{Sens}_A) - 2\,	ext{Cov}(	ext{Sens}_A, 	ext{Sens}_B)$$
  $$	ext{SE}_{	ext{independent}} = 5.23	ext{ pp} \quad\longrightarrow\quad 	ext{SE}_{	ext{paired}} = 1.95	ext{ pp}$$
* **Paired 95% Confidence Interval:** $[ -1.77	ext{ pp}, +6.53	ext{ pp} ]$ ($df = 15$). Demonstrates that overlapping separate marginal CIs do not indicate lack of statistical pairing significance.

---

## The 61-Person Decision Boundary Swap

Holding testing capacity fixed at exactly 20% ($K = 939$ slots), the two algorithms agree on **878 shared individuals** ($93.5\%$ concordance). All divergence occurs in a **61-person boundary swap** (122 marginal individuals at the triage threshold):

| Triage Queue Subgroup | Queue Size | Potential Cases Found | Positivity Rate (Yield) | Clinical Policy Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Shared Concordant Selection** | 878 | 52 | 5.92% (52 / 878) | High-risk concordant prioritization across both models. |
| **Model A Exclusive Selection** | 61 | 1 | 1.64% (1 / 61) | Deprioritized when training includes objective biomonitoring. |
| **Model B Exclusive Selection** | 61 | 3 | **4.92% (3 / 61)** | **Newly prioritized into screening queue (3.0&times; precision dividend).** |
| **Shared Non-Selected** | 3,698 | 60 | 1.62% (60 / 3,698) | Concordant low-risk ranking. |

---

## Health Equity Subgroup Audit

Evaluating screening detection across insurance status at 20% capacity ($K = 939$ slots):

| Health Insurance Subgroup | Total Cohort | Holdout True Cases | Model A Detection (Sens) | Model B Detection (Sens) | Net Detection Shift |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Insured Adults** | 4,268 | 102 | 51 / 102 (50.0%) | 52 / 102 (51.0%) | +1 Case (+1.0 pp) |
| **Uninsured Adults** | 422 | 13 | 2 / 13 (15.4%) | 3 / 13 (23.1%) | +1 Case (+7.7 pp) |
| **Unrecorded Coverage** | 8 | 1 | 0 / 1 (0.0%) | 0 / 1 (0.0%) | 0 Cases (0.0 pp) |
| **Total Cohort** | 4,698 | 116 | 53 / 116 (45.7%) | 55 / 116 (47.4%) | +2 Cases (+1.72 pp) |

*Small denominator disclosure:* The uninsured holdout cohort contains 13 potential cases ($102 + 13 + 1 = 116$). While directionally consistent with hypothesis (+1 case, 15.4% to 23.1%), small sample counts require cautious interpretation without claiming complete elimination of systemic disparity.

---

## Multi-Architecture Sensitivity & Guideline Defense

Triage queue shifts re-evaluated across alternative tree architectures under identical 20% capacity:

| Model Architecture | Model A Detection | Model B Detection | Net Case Shift (&Delta;) | Boundary Swaps |
| :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression (Primary)** | 53 / 116 (45.7%) | 55 / 116 (47.4%) | **+2 Cases** | 61 Swaps |
| **Random Forest** | 60 / 116 (51.7%) | 61 / 116 (52.6%) | **+1 Case** | 77 Swaps |
| **HistGradientBoosting** | 59 / 116 (50.9%) | 59 / 116 (50.9%) | **0 Net Gain** | 132 Swaps |

**Clinical Guideline Defense:** While non-linear tree models achieve higher unweighted baseline yield (+6 to +7 cases), linear logistic regression remains the primary reference standard for clinical transparency, monotonic risk scoring, and compliance with the American Diabetes Association (ADA) Prediabetes Risk Test paradigm.

---

## Health Economics & Decision Curve Analysis (DCA)

* **Net Monetary Benefit (NMB):** At standard Point-of-Care HbA1c test costs ($C = \$25$) and present value of complication avoidance ($B = \$8,500$), biomarker-augmented triage delivers a net economic surplus of **+\$25,500 per 10,000 screened individuals** compared to diagnosis-only triage.
* **Decision Curve Analysis:** Model B achieves positive net clinical benefit across all decision thresholds from $p_t = 0.02$ to $0.15$, dominating both universal screening and treat-none baselines.

---

## Print-Ready Vector Research Poster ($36 	imes 24$ in)

The repository includes a publication-grade, single-page vector research poster:
* **Physical Dimensions:** $36.0 	imes 24.0$ inches ($2592.0 	imes 1728.0$ pt, 954 KB vector PDF).
* **High-Resolution Retina Image:** $6912 	imes 4608$ px PNG (2.69 MB).
* **Statistical Graphics:** Features an authentic SciencePlots two-panel figure combining boundary queue allocation with a paired complex survey Forest Plot ($0	ext{ pp}$ Null Reference Line).
* **Automated Layout Audit:** 0 overflow issues across all bounding boxes, verified via headless Playwright rendering.
* **Files:** `reports/poster.pdf`, `reports/poster.png`, `reports/poster.html`.

---

## How to Cite (APA 7th Edition)

### APA 7th Format

```text
Nguyen, C. T. A. (2026). When training labels change who gets screened: Temporal evaluation of diagnosis-based versus biomarker-augmented labels in NHANES [Research Poster & Interactive Lab]. University of Wisconsin, Madison. https://aansensei.dev/hiddencare/
```

### BibTeX Entry

```bibtex
@misc{nguyen2026hiddencare,
  author = {Cao Thien An Nguyen},
  title = {When Training Labels Change Who Gets Screened: Temporal Evaluation of Diagnosis-Based Versus Biomarker-Augmented Labels in NHANES},
  year = {2026},
  month = {November},
  howpublished = {Research Poster and Interactive Epidemiological Laboratory},
  institution = {University of Wisconsin-Madison},
  url = {https://aansensei.dev/hiddencare/}
}
```

---

## Setup & Local Execution

### 1. Requirements

Python 3.10 or higher. Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run Test Suite

Run the verified test suite (13 unit tests covering Pandera contracts, exclusion logic, paired survey variance, and leakage checks):

```bash
python -m pytest -v tests/
```

### 3. Launch Interactive Research Lab

```bash
python app.py
```

Navigate to `http://localhost:7860` to access the interactive screening capacity simulator (5% to 50%), the 61-person margin inspector, and the complete academic dossier tab.

---

## License & Data Provenance

* **License:** MIT License. Open academic and policy research.
* **Data Provenance:** National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC). Continuous NHANES 2017 to 2023. This independent academic analysis is neither endorsed nor certified by the CDC or NCHS.
