# HiddenCare Analysis Protocol

Protocol Version: 1.0  
Date: November 6, 2026  
Status: Pre-registered prior to model evaluation on the holdout release  
Principal Investigator: An Nguyen (AanSensei)  
Target Application: Weill Cornell Biostatistics Summer Internship 2027  

## 1. Research Question and Motivation

In healthcare machine learning, models are frequently trained on administrative or self-reported diagnostic codes that reflect who had access to care and received a diagnosis, rather than underlying biological need alone.

This study examines the following research question:
When screening capacity is constrained, does training a model on self-reported prior diabetes diagnoses versus a combined diagnosis and laboratory HbA1c screening criterion alter which previously undiagnosed adults are prioritized for screening? How are potentially missed cases distributed across insurance and income subgroups?

This investigation is designed as a student replication and methodological extension of proxy outcome bias research. It demonstrates rigorous epidemiological data hygiene, leakage prevention, fixed-budget evaluation, and health equity auditing. It does not claim to invent the concept of proxy outcome bias or prove causal relationships between access to care and disease prevalence.

## 2. Study Design and Data Sources

The study utilizes two distinct, non-overlapping survey cycles from the CDC National Health and Nutrition Examination Survey (NHANES):

1. Development Cohort: NHANES 2017 to March 2020 Pre-pandemic release. This 3.2 year cycle represents the development environment where feature engineering, cross-validation, and hyperparameter tuning take place.
2. Evaluation Cohort: NHANES August 2021 to August 2023 Post-pandemic release. This 2-year cycle serves as a locked holdout evaluation set. Participants in this cycle are entirely distinct individuals from the pre-pandemic cycle.

For each cycle, five component files are merged on the unique sequence identifier (SEQN):
- Demographics: age, gender, pregnancy status, poverty income ratio, sampling design, and survey weights.
- Diabetes Questionnaire: self-reported physician diagnosis of diabetes.
- Glycohemoglobin: venous blood laboratory measurement of HbA1c percentage.
- Body Measures: physical examination measurements of body mass index and waist circumference.
- Health Insurance: self-reported health insurance coverage status.

## 3. Cohort Eligibility and Exclusion Criteria

Both candidate models must be trained on the exact same participants to guarantee a fair and paired comparison. A participant is eligible for the primary cohort if all of the following criteria are met:

1. Age: At least 20 years of age at the time of screening exam (`RIDAGEYR >= 20`).
2. Explicit Diagnosis Response: Explicit affirmative or negative response to physician diagnosis of diabetes (`DIQ010 %in% c(1, 2)`). Responses of borderline (`3`), refused (`7`), or don't know (`9`) are excluded from the primary cohort.
3. Laboratory HbA1c: Valid observed glycohemoglobin measurement (`!is.na(LBXGH)`). No imputation is performed on the laboratory outcome.
4. Survey Weight: Strictly positive analysis weight (`WTMECPRP > 0` for pre-pandemic; `WTPH2YR > 0` for post-pandemic).
5. Known Pregnancy Exclusion: In NHANES, urine pregnancy testing is conducted exclusively on females aged 20 to 44 years participating in the exam (`RIDEXPRG`). Participants with a positive pregnancy result (`RIDEXPRG == 1`) are excluded. Participants with negative results (`RIDEXPRG == 2`), unknown results (`RIDEXPRG == 3`), or those not eligible for testing (all males and females aged 45 and older, where `RIDEXPRG` is missing) are retained. This rule prevents the inadvertent exclusion of older adults where diabetes prevalence is highest.

## 4. Target Label Definitions

Two distinct outcome labels are constructed within the training cohort:

- Label A (Diagnosis-only Proxy):  
  `label_dx = 1` if `DIQ010 == 1` (physician told participant they have diabetes).  
  `label_dx = 0` if `DIQ010 == 2` (no reported diagnosis).

- Label B (Combined Diagnosis and Laboratory Criterion):  
  `label_full = 1` if `DIQ010 == 1` OR `LBXGH >= 6.5%`.  
  `label_full = 0` if `DIQ010 == 2` AND `LBXGH < 6.5%`.

Key clinical note: Individuals with a confirmed prior diagnosis remain positive under Label B regardless of their current HbA1c level. Effective clinical management and pharmacological treatment may lower HbA1c below 6.5 percent in patients who nonetheless have diabetes.

## 5. Feature Allowlist and Leakage Prevention

The feature matrix is strictly restricted to four non-invasive demographic and anthropometric variables that are routinely available prior to diagnostic testing:
- Age in years (`age` from `RIDAGEYR`)
- Gender (`sex` from `RIAGENDR`, coded as binary factor)
- Body Mass Index (`bmi` from `BMXBMI`)
- Waist Circumference (`waist` from `BMXWAIST`)

Strictly Excluded Variables:
- Laboratory HbA1c (`LBXGH`) and plasma glucose
- Diabetes questionnaire responses (`DIQ010`) and diabetes medications
- Participant identifier (`SEQN`)
- Survey design variables (`SDMVPSU`, `SDMVSTRA`) and survey weights
- Audit variables: Health insurance (`HIQ011`) and Poverty Income Ratio (`INDFMPIR`) are preserved exclusively for downstream audit and are never supplied to the predictive models.

## 6. Preprocessing, Cross-Validation, and Model Fitting

Preprocessing is encapsulated in a reproducible workflow to prevent data leakage:
1. Imputation: Missing values in numeric predictors (`bmi`, `waist`) are imputed using the median calculated strictly within the analysis split of each training fold.
2. Standardization: Continuous predictors are centered and scaled based on training fold statistics.
3. Categorical Encoding: The binary sex variable is converted to indicator dummy variables.

Model Architecture:
- Regularized Logistic Regression using scikit-learn LogisticRegression with an L2 penalty parameter C.
- Hyperparameter tuning optimizes the inverse regularization strength C over a pre-declared grid of 10 log-spaced values from 0.0001 to 10.0.
- Five-fold cross-validation is performed on the pre-pandemic development cohort, using stratified resampling to preserve positive class prevalence.
- The workflow with the highest area under the ROC curve on cross-validation is selected and refitted on the complete pre-pandemic cohort.
- All model artifacts, configurations, and tuning summaries are saved prior to evaluating the holdout dataset.

## 7. Holdout Evaluation Protocol

The primary evaluation cohort consists of previously undiagnosed adults in the post-pandemic release:
- Inclusion: Post-pandemic cohort participants who reported no prior diabetes diagnosis (`DIQ010 == 2`).
- Ground Truth Outcome: Elevated HbA1c of 6.5 percent or higher (`LBXGH >= 6.5%`), representing potential undiagnosed diabetes or elevated glycemic risk requiring clinical confirmation.

Screening Capacity Allocation:
- Both trained models assign a predicted probability to every individual in the evaluation cohort.
- Screening capacity scenarios simulate fixed public health testing resources: top 10 percent, top 20 percent, and top 30 percent.
- The 20 percent capacity scenario is designated as the primary benchmark before inspecting results.
- Ranking and Tie-breaking Rule: Participants are ranked in descending order of predicted score. Any tied scores are broken deterministically by ascending sequence number (`SEQN`).

Reported Performance Metrics:
- Number evaluated (`n_eval`), number selected (`n_pick`), potential cases present (`n_case`), potential cases detected (`n_found`), and potential cases missed (`n_missed`).
- Sensitivity (Recall): proportion of potential cases detected (`n_found / n_case`).
- Positive Predictive Value (PPV / Precision): proportion of screened participants who are true potential cases (`n_found / n_pick`).
- Number Needed to Screen (NNS): `n_pick / n_found`.
- Area under the ROC Curve (ROC AUC) and Average Precision (PR AUC).
- Random Selection Baseline: Mathematical expectation (`n_pick * prevalence`) and fixed-seed simulation for identical capacity.

## 8. Equity and Disparity Audit

To assess how proxy outcome choice influences care access:
- Paired Concordance Analysis: We quantify the exact overlap between individuals selected by Model A and Model B under the 20 percent capacity budget. We calculate who is selected by both models, who is prioritized exclusively by Model A, who is prioritized exclusively by Model B, and the number of true potential cases in each partition.
- Insurance Audit: Performance is stratified by insurance status (`insured`, `uninsured`, `unknown`).
- Income Audit: Performance is stratified by Poverty Income Ratio categories:
  - Low income: `PIR < 1.30`
  - Middle income: `1.30 <= PIR <= 3.50`
  - High income: `PIR > 3.50`
  - Missing income: `is.na(PIR)`
- Fairness Rule: Subgroup metrics must report sample counts (`N`) and positive case counts (`cases`). Small subgroups are not used to make generalized claims about systemic disparities.

## 9. Scientific Limitations and Causal Boundaries

1. Cross-sectional Observation: NHANES captures cross-sectional snapshots. Differences in prioritization between models describe shifts in proxy learning, not prospective clinical trajectories.
2. Non-causal Interpretation: Differences in missed cases across insurance or income groups do not establish that health insurance or income causally produces diabetes or missed screening.
3. Laboratory Cutoff vs Clinical Diagnosis: An elevated HbA1c level from a single survey blood draw meets epidemiological screening criteria but requires repeat laboratory testing for clinical diagnosis.
4. Survey Weights: Unweighted sample-level ML metrics serve as the primary reproducible algorithmic benchmark. Complex survey design analyses are conducted separately with appropriate design degrees of freedom.
