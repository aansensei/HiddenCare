# Graduate Fellowship & Research Statement: Technical Defense Draft

**Candidate:** Cao Thien An Nguyen (AanSensei)  
**Institution:** University of Wisconsin, Madison (B.S. Economics & Data Science)  
**GitHub:** [github.com/aansensei](https://github.com/aansensei)  
**Project Portfolio:** HiddenCare ([aansensei.dev/hiddencare](https://aansensei.dev/hiddencare/) | [github.com/aansensei/HiddenCare](https://github.com/aansensei/HiddenCare))  
**Copyright:** Copyright 2026 Cao Thien An Nguyen. All rights reserved.  
**Scope:** Universal technical statement and research defense for graduate fellowships, research laboratories, and biostatistics appointments.  

---

## 1. Statement of Research Interest & Scientific Motivation

In health economics and population health surveillance, predictive algorithms increasingly determine who receives preventive outreach and diagnostic testing under finite clinical budgets. However, machine learning models trained on electronic health record billing codes (ICD-10) or self-reported diagnostic history do not merely learn biological pathology: they implicitly learn healthcare utilization. 

As an Economics and Data Science student at UW, Madison, I investigate how institutional access barriers distort observable data. When an algorithm is supervised with prior clinical diagnoses, patients who lack health insurance or cannot afford clinic visits are misclassified as healthy baselines. In my independent investigation, **HiddenCare**, I formulated a pre-registered protocol examining whether augmenting administrative training labels with objective biomonitoring (venous HbA1c &ge; 6.5%) rectifies triage priorities for undiagnosed Americans under capacity limits.

---

## 2. Quantitative Methodology & Biostatistical Rigor

Rather than training naive models on unvalidated random splits, I structured HiddenCare to mirror rigorous epidemiological standards:

* **Temporal Holdout Validation:** Developed models on pre-pandemic CDC NHANES (2017 to March 2020; N = 7,761) and evaluated them on a strictly non-overlapping holdout of post-pandemic adults (August 2021 to August 2023; N = 4,698 undiagnosed individuals).
* **Leakage Control & Anthropometric Feasibility:** Restricted predictors entirely to non-invasive demographics (age, sex, BMI, waist circumference). Strictly excluded diagnostic questions, medications, glucose measures, and socioeconomic status from model inputs to prevent target leakage.
* **Complex Survey Variance Estimation:** To avoid the trap of treating clustered survey data as independent observations, I implemented Taylor Series Linearization for ratio estimators across masked strata and primary sampling units (WTPH2YR weights, df = 15), calculating valid 95% national confidence intervals for sensitivity and positive predictive values.
* **Modern Health Data Engineering:** Implemented an in-process DuckDB analytical lakehouse with zero-copy Parquet partitions, paired with declarative Pandera data quality contracts to trap schema drift and anomalous values.

---

## 3. Empirical Breakthroughs & Policy Findings

Across 4,698 undiagnosed participants in the 2021 to 2023 holdout cohort (representing 116 true latent diabetes cases):

1. **The 61-Patient Proof:** At a realistic 20% outreach budget (K = 939 test slots), switching supervision from Model A (Diagnosis Only) to Model B (Biomarker Augmented) actively swaps 61 borderline individuals into the screening queue. Model B's swapped segment yields a 4.92% hit rate (3 / 61 true cases) compared to Model A's 1.64% (1 / 61), tripling precision with zero marginal test expenditure.
2. **Eliminating the Uninsured Sensitivity Deficit:** Under Model A, insured adults achieve 41.5% sensitivity while uninsured adults achieve only 32.9% (an 8.6% access penalty). Model B eliminates this gap without taking insurance as a feature, raising uninsured sensitivity to 41.8%. Under Random Forest validation, uninsured sensitivity surges by +15.38% (from 30.77% to 46.15%).
3. **Health Economic Value:** In decision curve analysis, Model B provides superior Net Monetary Benefit across risk thresholds from 2% to 15%, yielding +$25,500 net economic value per 10,000 screened individuals under standard screening economics ($25 test cost, $8,500 early intervention complication savings).

---

## 4. Multi-Architecture Algorithmic Robustness

To verify that the health equity dividend is not an artifact of LightGBM hyperparameter choices, I replicated the entire triage pipeline across alternative architectures:

* **Random Forest Classifier (150 trees, max depth 6):** Model B captures 61 latent cases, swapping 77 patients at the margin and boosting uninsured sensitivity by +15.38%.
* **HistGradientBoosting Classifier:** Model B identifies 59 latent cases, swapping 132 individuals at the margin and maintaining consistent positive net benefit.

This confirms that decoupling disease detection from healthcare access is an intrinsic property of objective biological ground truth rather than algorithm choice.

---

## 5. Strategic Alignment & Institutional Translation

Leading academic institutions in biostatistics and population health sciences spearhead comparative effectiveness research, algorithmic equity, and health disparity analytics. I am eager to contribute to collaborative investigations by combining econometric causal reasoning, complex survey variance estimation, and production-grade Python/R data engineering. 

HiddenCare demonstrates my commitment to extracting truthful signals from incomplete observational data, ensuring that clinical algorithms expand healthcare equity rather than entrench historical divides.
