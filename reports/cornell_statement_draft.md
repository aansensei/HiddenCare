# Weill Cornell Medicine Biostatistics Fellowship: Research Statement & Technical Defense Draft

**Candidate:** Cao Thien An Nguyen (AanSensei)  
**Institution:** University of Wisconsin, Madison (B.S. Economics & Data Science)  
**Target Program:** Department of Population Health Sciences, Division of Biostatistics Summer Internship  
**Project Portfolio:** HiddenCare (https://aansensei.dev/hiddencare/ | https://github.com/aansensei/HiddenCare)  
**Status:** Pre-submission draft prepared for An's review (February 2027 application cycle)  

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

Evaluating both policies under a realistic 20% clinic testing capacity (N = 939 slots for 4,698 adults):

* **The 61-Patient Proof:** While both models agree on 878 individuals, Model B swaps 61 marginal patients into the screening queue. Among these swapped individuals, Model B achieved a 4.92% diagnostic yield (3 cases detected) compared to 1.64% for Model A (1 case detected), delivering a **3.0x higher precision ratio** at zero incremental testing cost.
* **Decision Curve Analysis (DCA):** Decision curves demonstrated superior net clinical benefit for Model B across threshold probabilities from 1% to 15%, translating to a **+$25,500 net economic benefit per 10,000 screened individuals**.
* **Health Equity Dividend:** Traditional models penalized uninsured Americans, exhibiting an 8.6% sensitivity deficit. Augmenting training labels with objective laboratory biomarkers eliminated this gap. Across nonlinear architectures (Random Forest), biomarker augmentation yielded a **+15.38% sensitivity boost for uninsured adults** (46.15% vs 30.77%) without ever collecting insurance status as an input.

---

## 4. Scientific Humility & Methodological Limitations

True biostatistical scholarship requires documenting what empirical data cannot prove:

* **Observational Boundaries:** NHANES cross-sectional data establishes statistical disparities in priority triage queues, but cannot demonstrate a causal link between insurance status and biological diabetes onset.
* **Screening Surrogacy vs Clinical Confirmation:** A single elevated HbA1c (&ge; 6.5%) in a mobile survey is a population screening surrogate, not an authoritative clinical diagnosis, which requires repeat confirmatory testing.
* **Subgroup Sample Power:** The uninsured evaluation subset contained 422 individuals with 13 true cases. I explicitly disclose this sample limit to avoid inflating modest subgroup counts into sweeping fairness claims.

---

## 5. Alignment with Weill Cornell Medicine

The Division of Biostatistics at Weill Cornell Medicine leads international efforts in comparative effectiveness, cancer epidemiology, and health disparity analytics. I am eager to contribute to Cornell's ongoing investigations by combining econometric rigor, complex survey variance estimation, and production-grade Python/R data engineering. HiddenCare demonstrates my commitment to extracting truthful stories from incomplete observational data, ensuring that clinical algorithms expand healthcare equity rather than entrench historical divides.
