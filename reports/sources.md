# Data Sources and Citations

## CDC NHANES Source Files

All data files were downloaded directly from the CDC National Center for Health Statistics (NCHS) public NHANES servers.

### Development Release: NHANES 2017 to March 2020 Pre-pandemic

1. Demographics (`P_DEMO.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DEMO.xpt
   - Description: Age, gender, pregnancy status, poverty income ratio, sampling design (PSU, strata), and pre-pandemic MEC examination sample weight (`WTMECPRP`).
   - Size: 3,614,720 bytes
   - SHA-256: 0ff1628d258cb88fc31d9ea4c40b54020c99a38eb7fa19c6e3b5e406aa843609

2. Diabetes Questionnaire (`P_DIQ.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DIQ.xpt
   - Description: Prior clinical diagnosis of diabetes (`DIQ010`).
   - Size: 3,361,520 bytes

3. Glycohemoglobin (`P_GHB.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_GHB.xpt
   - Description: Laboratory measurement of glycohemoglobin percentage (`LBXGH`).
   - Size: 167,600 bytes

4. Body Measures (`P_BMX.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_BMX.xpt
   - Description: Examination measurements of body mass index (`BMXBMI`) and waist circumference (`BMXWAIST`).
   - Size: 2,520,640 bytes

5. Health Insurance (`P_HIQ.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_HIQ.xpt
   - Description: Self-reported health insurance coverage (`HIQ011`).
   - Size: 1,745,440 bytes

### Evaluation Release: NHANES 2021 to 2023 Post-pandemic

1. Demographics (`DEMO_L.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.xpt
   - Description: Age, gender, pregnancy status, poverty income ratio, sampling design (PSU, strata), and 2-year examination weights.
   - Size: 2,582,160 bytes

2. Diabetes Questionnaire (`DIQ_L.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DIQ_L.xpt
   - Description: Prior clinical diagnosis of diabetes (`DIQ010`).
   - Size: 847,600 bytes

3. Glycohemoglobin (`GHB_L.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.xpt
   - Description: Laboratory measurement of glycohemoglobin percentage (`LBXGH`) and phlebotomy 2-year sample weight (`WTPH2YR`).
   - Size: 174,000 bytes

4. Body Measures (`BMX_L.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.xpt
   - Description: Examination measurements of body mass index (`BMXBMI`) and waist circumference (`BMXWAIST`).
   - Size: 1,563,200 bytes

5. Health Insurance (`HIQ_L.xpt`)
   - URL: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HIQ_L.xpt
   - Description: Self-reported health insurance coverage (`HIQ011`).
   - Size: 455,840 bytes

## Clinical Guidance and Diagnostic Cutoffs

1. National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)
   - The A1C Test and Diabetes
   - URL: https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test/
   - Guidance: An HbA1c level of 6.5 percent or higher on two separate tests indicates diabetes. In cross-sectional survey data like NHANES, a single measurement above 6.5 percent represents an elevated screening criterion rather than a confirmed clinical diagnosis.

## Academic References

1. Access to care affects electronic health record reliability and AI-driven disease prediction.
   - Journal: Nature Health, 2026.
   - Reference URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC13262972/

2. Hierarchical Bayesian models to mitigate systematic disparities in prediction with proxy outcomes.
   - Journal: Journal of the Royal Statistical Society Series A.
   - Reference URL: https://academic.oup.com/jrsssa/article/189/1/242/7932063

3. Explainable Machine Learning for Diabetes Screening Using NHANES 2021 to 2023 Data: A Leakage-Controlled Classification Study.
   - Journal: MDPI Healthcare, 2024.
   - Reference URL: https://www.mdpi.com/2297-8747/31/5/221
