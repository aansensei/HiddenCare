# HiddenCare: Research Brief on Proxy Outcome Bias in Algorithmic Diabetes Screening

Author: An Nguyen (AanSensei)  
Date: November 6, 2026  
Target Application: Weill Cornell Biostatistics Summer Internship 2027  
Repository: https://github.com/aansensei/HiddenCare.git  

## Executive Summary

Machine learning algorithms deployed for healthcare screening often rely on administrative diagnosis codes or self-reported medical history as training labels. These proxy outcomes inevitably confound biological disease risk with historic healthcare access. 

HiddenCare investigates this phenomenon through a controlled, leakage-free experiment on CDC NHANES data. We train two regularized logistic regression models using identical baseline predictors (age, gender, BMI, waist circumference) on a pre-pandemic cohort (2017 to March 2020; N = 7,761 adults). Model A is trained on self-reported clinical diagnosis (Label A), while Model B is trained on an expanded criterion combining clinical diagnosis with laboratory HbA1c of 6.5 percent or higher (Label B). Both models are evaluated on a locked, non-overlapping holdout of previously undiagnosed adults from the post-pandemic release (2021 to 2023; N = 4,698 adults, containing 116 potential undiagnosed cases).

Under the primary fixed screening budget of 20 percent capacity (939 participants screened):
1. Algorithmic screening significantly outperforms random allocation: Model A detects 53 potential cases (sensitivity 45.7%, PPV 5.64%) and Model B detects 55 potential cases (sensitivity 47.4%, PPV 5.86%), compared to an expected 23.2 cases under random allocation (95% simulation interval: 15 to 32 cases).
2. Label definition alters screening priority at the margin: While both policies agree on 878 participants (52 cases found, 5.92% yield), they diverge on 122 participants (61 participants prioritized exclusively by each model). Among participants prioritized only by Model B, the positivity yield is 4.92% (3 cases detected), whereas participants prioritized only by Model A exhibit a positivity yield of only 1.64% (1 case detected), roughly matching the background unscreened prevalence of 1.62%.
3. Disparities in screening yield by insurance and income: Among uninsured adults, sensitivity is substantially lower for both models (15.4% for Model A; 23.1% for Model B) compared to insured adults (50.0% for Model A; 51.0% for Model B). Model B recovers 1 additional case among the uninsured by screening 6 additional uninsured individuals. However, because the uninsured evaluation sample is small (N = 422, with only 13 cases), these subgroup differences reflect empirical screening yields rather than causal effects of insurance.

## Research Question and Motivation

When screening capacity is constrained, does training a model on self-reported prior clinical diagnoses versus a combined diagnosis and laboratory HbA1c criterion alter which previously undiagnosed adults are prioritized for screening? How are potentially missed cases distributed across insurance and income subgroups?

In clinical and population health, predictive models are frequently utilized to allocate finite screening capacity, such as mobile clinic outreach or subsidized diagnostic testing. If a model learns historical patterns of who received a diagnosis rather than who needs care, it risks systematically under-prioritizing populations with lower healthcare access. This study provides a rigorous, inspectable empirical demonstration of proxy outcome bias.

## Data Sources and Cohort Selection

We utilize two distinct cross-sectional cycles from the CDC National Health and Nutrition Examination Survey (NHANES):
1. Development Cohort: NHANES 2017 to March 2020 Pre-pandemic release (14,986 initial participants).
2. Evaluation Cohort: NHANES August 2021 to August 2023 Post-pandemic release (11,744 initial participants).

Component files (Demographics, Diabetes Questionnaire, Glycohemoglobin, Body Measures, and Health Insurance) were merged on participant sequence number (SEQN). Eligibility criteria were sequentially applied:
- Age 20 years or older: retained 9,232 pre-pandemic and 7,809 post-pandemic adults.
- Explicit diagnosis answer (DIQ010 is 1 or 2): excluded borderline, refused, and unknown responses (retained 8,965 pre-pandemic and 7,536 post-pandemic).
- Observed venous HbA1c laboratory measurement: retained 7,837 pre-pandemic and 5,554 post-pandemic.
- Strictly positive survey examination weight: retained 7,837 pre-pandemic and 5,554 post-pandemic.
- Non-pregnancy: In NHANES, urine pregnancy tests are administered only to females aged 20 to 44. Participants with known positive pregnancy (code 1) were excluded, while untested participants (all males and older females) were retained to prevent age-related attrition bias. This yielded 7,761 pre-pandemic adults and 5,517 post-pandemic adults.

Within the post-pandemic holdout, the primary evaluation subset consists of adults reporting no prior clinical diagnosis (DIQ010 == 2; N = 4,698). In this subset, 116 individuals exhibited an elevated HbA1c of 6.5 percent or higher, establishing a true background prevalence of 2.47%.

## Leakage-Controlled Preprocessing and Modeling Strategy

The predictor set is strictly restricted to four non-invasive demographic and anthropometric variables:
- Age (years)
- Gender (binary indicator)
- Body Mass Index (BMI, kg/m^2)
- Waist Circumference (cm)

All diagnostic questions, medications, laboratory measurements (HbA1c, glucose), participant identifiers, survey design weights, and audit variables (insurance, poverty income ratio) were strictly excluded from the feature matrix.

Within the pre-pandemic development release, an end-to-end scikit-learn Pipeline was implemented:
1. Imputation: Missing values in continuous predictors (BMI and waist circumference) were imputed using median values estimated strictly within training cross-validation splits.
2. Scaling: Numeric features were standardized (zero mean, unit variance) using training statistics.
3. Classifier: Logistic Regression with L2 regularization penalty C.
4. Tuning: Five-fold stratified cross-validation was used to optimize C over a grid of 10 values from 0.0001 to 10.0. The optimal hyperparameter for Model A was C = 0.0167 (CV ROC AUC = 0.7688), and for Model B was C = 0.0046 (CV ROC AUC = 0.7647).

Both final models were refitted on the complete pre-pandemic cohort and saved before inspecting post-pandemic holdout performance.

## Empirical Findings

### 1. Screening Performance Across Capacity Scenarios

We simulated three fixed public health screening capacity thresholds: 10 percent (469 screened), 20 percent (939 screened, primary benchmark), and 30 percent (1,409 screened).

At 10% capacity:
- Model A (Diagnosis Only): detects 31 cases (sensitivity 26.7%, PPV 6.61%, NNS 15.1).
- Model B (Combined): detects 36 cases (sensitivity 31.0%, PPV 7.68%, NNS 13.0).
- Random Baseline: detects an expected 11.6 cases (95% simulation interval: 6 to 18 cases).

At 20% capacity (Primary Pre-declared Comparison):
- Model A (Diagnosis Only): detects 53 cases (sensitivity 45.7%, PPV 5.64%, NNS 17.7).
- Model B (Combined): detects 55 cases (sensitivity 47.4%, PPV 5.86%, NNS 17.1).
- Random Baseline: detects an expected 23.2 cases (95% simulation interval: 15 to 32 cases).

At 30% capacity:
- Model A (Diagnosis Only): detects 70 cases (sensitivity 60.3%, PPV 4.97%, NNS 20.1).
- Model B (Combined): detects 75 cases (sensitivity 64.7%, PPV 5.32%, NNS 18.8).
- Random Baseline: detects an expected 34.8 cases (95% simulation interval: 25 to 44 cases).

Overall holdout discrimination:
- Model A: ROC AUC = 0.7300, Average Precision = 0.0548.
- Model B: ROC AUC = 0.7410, Average Precision = 0.0566.

### 2. Paired Policy Disagreement Analysis

At the primary 20% screening capacity (N = 939 screened):
- Both models agree on selecting 878 participants. Among these concordant selections, 52 potential cases are detected (positivity rate of 5.92%).
- Model A uniquely selects 61 participants who are excluded by Model B. Among these 61 participants, only 1 true case is found (positivity rate of 1.64%), which is indistinguishable from the background prevalence of unscreened individuals (1.62%).
- Model B uniquely selects 61 participants who are excluded by Model A. Among these 61 participants, 3 true cases are found (positivity rate of 4.92%), representing a threefold higher diagnostic yield.
- Both models agree on excluding 3,698 participants, leaving 60 potential cases undetected.

### 3. Sociodemographic Subgroup Audit

Insurance Coverage Audit:
- Insured adults (N = 4,268; 102 cases): Model A screens 916 and detects 51 cases (sensitivity 50.0%, PPV 5.57%). Model B screens 910 and detects 52 cases (sensitivity 51.0%, PPV 5.71%).
- Uninsured adults (N = 422; 13 cases): Model A screens 23 and detects 2 cases (sensitivity 15.4%, PPV 8.70%, 11 missed). Model B screens 29 and detects 3 cases (sensitivity 23.1%, PPV 10.34%, 10 missed).
- Unknown insurance status (N = 8; 1 case): Neither model selects any participant from this tiny subgroup (sensitivity 0.0%).

Income (Poverty Income Ratio) Audit:
- Low Income (PIR < 1.30; N = 821; 21 cases): Model A detects 4 cases (sensitivity 19.0%, PPV 3.57%). Model B detects 5 cases (sensitivity 23.8%, PPV 4.55%).
- Middle Income (1.30 <= PIR <= 3.50; N = 1,507; 55 cases): Model A detects 27 cases (sensitivity 49.1%, PPV 7.48%). Model B detects 27 cases (sensitivity 49.1%, PPV 7.38%).
- High Income (PIR > 3.50; N = 1,769; 26 cases): Model A detects 15 cases (sensitivity 57.7%, PPV 4.39%). Model B detects 15 cases (sensitivity 57.7%, PPV 4.48%).
- Missing Income (N = 601; 14 cases): Model A detects 7 cases (sensitivity 50.0%). Model B detects 8 cases (sensitivity 57.1%).

## Critical Biostatistical Interpretation

1. Modest Aggregate Shift, Meaningful Marginal Difference:
In aggregate metrics, Model B provides a modest improvement over Model A (+2 detected cases at 20% capacity, +5 detected cases at 10% and 30% capacities; +0.011 ROC AUC). However, inspecting the paired disagreement reveals that the individuals swapped into the screening pool by Model B have a 4.92% positivity rate compared to 1.64% for those prioritized only by Model A. Expanding the training label to include undiagnosed laboratory positives teaches the model to identify risk patterns that are less dependent on whether an individual historically accessed a clinic.

2. Lower Sensitivity Among Disadvantaged Groups:
Both models exhibit noticeably lower sensitivity in uninsured (15.4% to 23.1%) and low income (19.0% to 23.8%) participants than in insured (~50.0%) and high income (~57.7%) participants. This reflects the reality that risk factors such as age, BMI, and waist circumference interact differently with socioeconomic determinants of health. Incorporating laboratory positives in training yields marginal gains for uninsured (+1 case, +7.7% sensitivity) and low income (+1 case, +4.8% sensitivity) groups, but does not fully eliminate the disparity.

## Limitations and Causal Boundaries

1. Non-causal Observational Data: These findings describe statistical differences in priority rankings across proxy outcome definitions. They do not demonstrate that lacking insurance or having low income causally causes elevated HbA1c or missed screening.
2. Screening Criterion vs Clinical Diagnosis: A single elevated survey HbA1c measurement represents an epidemiological screening criterion. Clinical diagnostic guidelines require repeat confirmatory testing.
3. Subgroup Sample Constraints: The uninsured evaluation cohort contains only 13 potential cases out of 422 participants, and the unknown insurance group contains only 8 participants. These sample limits preclude broad claims regarding algorithmic fairness and must be reported transparently.
4. Survey Weights: Unweighted sample-level ML metrics serve as the primary reproducible algorithmic benchmark. Complex survey design calculations must account for masked PSU and strata to yield valid population inference.

## References

1. Access to care affects electronic health record reliability and AI-driven disease prediction. Nature Health, 2026.
2. Hierarchical Bayesian models to mitigate systematic disparities in prediction with proxy outcomes. Journal of the Royal Statistical Society Series A, 2024.
3. Explainable Machine Learning for Diabetes Screening Using NHANES 2021 to 2023 Data: A Leakage-Controlled Classification Study. MDPI Healthcare, 2024.
4. National Institute of Diabetes and Digestive and Kidney Diseases. The A1C Test and Diabetes. NIH Publication.
