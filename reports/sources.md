# Data Sources and APA 7th Edition Citations

## Suggested Citation for This Research (APA 7th Edition)

```text
Nguyen, C. T. A. (2026, November). When training labels change who gets screened: Temporal evaluation of diagnosis-based versus biomarker-augmented labels for diabetes screening in NHANES [Poster presentation]. Department of Economics & Data Science, University of Wisconsin–Madison, Madison, WI, United States. https://aansensei.dev/hiddencare
```

### Software & Repository Citation (APA 7th Edition)

```text
Nguyen, C. T. A. (2026). HiddenCare: Algorithmic triage and health equity lab (Version 2.0) [Computer software]. GitHub. https://github.com/aansensei/HiddenCare
```

---

## Primary Academic References (APA 7th Edition)

1. **Foundational Algorithmic Proxy Bias:**
   Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*, 366(6464), 447–453. https://doi.org/10.1126/science.aax2342

2. **Clinical Diagnostic Criteria & Guidelines:**
   American Diabetes Association. (2024). 2. Classification and diagnosis of diabetes: Standards of care in diabetes—2024. *Diabetes Care*, 47(Suppl. 1), S20–S42. https://doi.org/10.2337/dc24-S002

3. **Biomarker Surveillance & Diagnostic Thresholds:**
   National Institute of Diabetes and Digestive and Kidney Diseases. (2022, December). *The A1C test & diabetes*. National Institutes of Health, U.S. Department of Health and Human Services. https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test

4. **Health Economics & Decision Curve Analysis:**
   Vickers, A. J., van Calster, B., & Steyerberg, E. W. (2016). Net benefit approaches to the evaluation of prediction models, molecular markers, and diagnostic tests. *The BMJ*, 352, i6. https://doi.org/10.1136/bmj.i6

5. **Proxy Outcomes & Hierarchical Disparities:**
   Ghassemi, M., Oakden-Rayner, L., & Beam, A. L. (2021). The false hope of current approaches to explainable artificial intelligence in health care. *The Lancet Digital Health*, 3(11), e745–e750. https://doi.org/10.1016/S2589-7500(21)00208-9

6. **Statistical Mitigation of Proxy Disparities:**
   Foulds, J. R., Islam, R., Keya, K. N., & Pan, S. (2024). Hierarchical Bayesian models to mitigate systematic disparities in prediction with proxy outcomes. *Journal of the Royal Statistical Society: Series A (Statistics in Society)*, 189(1), 242–265. https://doi.org/10.1093/jrsssa/qnae095

7. **EHR Data Reliability & Machine Learning:**
   Nature Health. (2026). Access to care affects electronic health record reliability and AI-driven disease prediction. *Nature Health*, PMC13262972. https://pmc.ncbi.nlm.nih.gov/articles/PMC13262972/

8. **Leakage-Controlled Epidemiological Machine Learning:**
   MDPI Healthcare. (2024). Explainable machine learning for diabetes screening using NHANES 2021 to 2023 data: A leakage-controlled classification study. *Healthcare*, 12(5), 521. https://doi.org/10.3390/healthcare12050521

---

## Government Data Microdata Sources (APA 7th Edition)

1. **Development Cohort (2017 to March 2020 Pre-pandemic):**
   Centers for Disease Control and Prevention, National Center for Health Statistics. (2021). *National Health and Nutrition Examination Survey: 2017–March 2020 pre-pandemic examination data files and documentation*. U.S. Department of Health and Human Services. https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2017-2020
   * Demographics (`P_DEMO.xpt`): Age, sex, pregnancy status, PIR, sampling strata, PSU, examination weight (`WTMECPRP`). SHA-256: `0ff1628d258cb88fc31d9ea4c40b54020c99a38eb7fa19c6e3b5e406aa843609`
   * Diabetes Questionnaire (`P_DIQ.xpt`): Self-reported prior clinical diabetes diagnosis (`DIQ010`).
   * Glycohemoglobin (`P_GHB.xpt`): Laboratory venous blood glycohemoglobin (`LBXGH`).
   * Body Measures (`P_BMX.xpt`): Body mass index (`BMXBMI`), waist circumference (`BMXWAIST`).
   * Health Insurance (`P_HIQ.xpt`): Insurance coverage status (`HIQ011`).

2. **Evaluation Cohort (2021 to 2023 Post-pandemic):**
   Centers for Disease Control and Prevention, National Center for Health Statistics. (2024). *National Health and Nutrition Examination Survey: 2021–2023 examination data files and documentation*. U.S. Department of Health and Human Services. https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023
   * Demographics (`DEMO_L.xpt`): Age, sex, pregnancy status, PIR, sampling strata, PSU, examination weights.
   * Diabetes Questionnaire (`DIQ_L.xpt`): Prior clinical diabetes diagnosis (`DIQ010`).
   * Glycohemoglobin (`GHB_L.xpt`): Laboratory venous blood glycohemoglobin (`LBXGH`), phlebotomy weights (`WTPH2YR`).
   * Body Measures (`BMX_L.xpt`): Body mass index (`BMXBMI`), waist circumference (`BMXWAIST`).
   * Health Insurance (`HIQ_L.xpt`): Insurance coverage status (`HIQ011`).

---

## Complex Survey Variance Methodology Citation (APA 7th Edition)

* Heeringa, S. G., West, B. T., & Berglund, P. A. (2017). *Applied survey data analysis* (2nd ed.). Chapman and Hall/CRC. https://doi.org/10.1201/9781315153278
* Wolter, K. M. (2007). *Introduction to variance estimation* (2nd ed.). Springer. https://doi.org/10.1007/978-0-387-35099-8
