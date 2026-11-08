# Research Reports, Academic Publications & APA 7th Citations (`reports/`)

This directory contains the formal epidemiological research protocol, executive briefing, data provenance records, schema drift audit logs, academic research poster assets, and APA 7th edition citation standards.

---

## Suggested Citations (APA 7th Edition)

### How to Cite This Research Poster (APA 7th Edition)

```text
Nguyen, C. T. A. (2026, November). When training labels change who gets screened: Temporal evaluation of diagnosis-based versus biomarker-augmented labels for diabetes screening in NHANES [Poster presentation]. Department of Economics & Data Science, University of Wisconsin–Madison, Madison, WI, United States. https://aansensei.dev/hiddencare
```

### How to Cite This Open-Source Software & Repository (APA 7th Edition)

```text
Nguyen, C. T. A. (2026). HiddenCare: Algorithmic triage and health equity lab (Version 2.0) [Computer software]. GitHub. https://github.com/aansensei/HiddenCare
```

---

## Directory Overview

* **Open Science Standards:** Adheres to pre-specified observational study protocols, documenting hypotheses and analytical plans before model evaluation.
* **Complete Data Provenance:** Cryptographically documents CDC NHANES data sources across 10 SAS transport (.XPT) files with direct URLs and SHA-256 hashes.
* **Publication Deliverables:** Includes a print-ready 36 × 24-inch academic conference poster (HTML, vector PDF, high-res PNG) and automated schema drift audit logs.
* **Interactive Lightbox Zoom:** Supported in web runtime with keyboard accessibility (Escape), backdrop dismiss, and mobile touch safeguards.

---

## File Summary

| File | Document Type | Purpose |
| :--- | :--- | :--- |
| `poster.html` | Academic Poster (HTML) | 36 × 24-inch physical conference poster markup with scalable typography |
| `poster.pdf` | Vector Print PDF | Verified single-page 36.00 × 24.00-inch PDF export (2592 × 1728 pt) |
| `poster.png` | High-Resolution Image | 3456 × 2304 px (96 dpi) raster export for digital presentations and web previews |
| `protocol.md` | Research Protocol | Formal epidemiological study design, inclusion rules, and statistical endpoints |
| `brief.md` | Executive Summary | High-level synthesis of clinical results, equity metrics, and economic utility |
| `sources.md` | Data Sources & Citations | Exact CDC NHANES download URLs, cycle descriptions, and full APA 7th reference list |
| `data_dictionary.csv` | Semantic Data Dictionary | Machine-readable crosswalk from CDC raw codes to clean analytical variables |
| `schema_drift_audit.json` / `.md` | Data Quality Audit Logs | Pandera drift metrics, KS test p-values, and PSI statistics across survey eras |
| `fellowship_statement_draft.md` | Fellowship Statement | Technical research defense and application statement for graduate fellowships |

---

## Academic Poster Specifications (`poster.html`, `poster.pdf`, `poster.png`)

### Physical Print Dimensions
* **Width × Height:** Exactly 36.00 × 24.00 inches (landscape aspect ratio 3:2).
* **PDF Points:** Exactly 2592.0 pt × 1728.0 pt. Verified via `pypdf` as a strict single page with 0.0 in margins.
* **Raster Output:** 3456 × 2304 px at 96 dpi.

### Typography Hierarchy (Targeted for Conference Readability)
* **Poster Title:** 64 pt (Newsreader Serif, bold, line height 1.1).
* **Subtitle:** 26 pt (Inter Sans-serif, medium, line height 1.35).
* **Section Headings:** 22 pt (Inter, bold, uppercase, letter-spacing 0.05em).
* **Body / Prose:** 20.5 pt (Inter, line height 1.48).
* **Table & Metric Data:** 18.5 pt with 700-weight headers.
* **Figure Labels & Footnotes:** 16.5 pt (Inter, regular/italic).

### Core Verified Empirical Results Displayed
* **Cohorts:** Development cohort $N = 7,761$ adults (2017 to March 2020); evaluation cohort $N = 4,698$ undiagnosed adults with 116 potential cases (venous blood $\text{HbA1c} \ge 6.5\%$).
* **Screening Capacity ($K = 20\%$):** 939 fixed test slots for each model.
* **Shared Selection:** Both models concordantly prioritize 878 shared individuals, yielding 52 cases (5.92% yield).
* **Boundary Swap:** Each model selects 61 exclusive individuals at the margin:
  * Model A Exclusive (Diagnosis Only): 1 case (1.64% yield).
  * Model B Exclusive (Biomarker Augmented): 3 cases (4.92% yield).
* **Overall Queue Yield:** Model A identifies 53 potential cases vs Model B identifies 55 potential cases (+2 potential cases, +1.72 pp unweighted sensitivity, +2.38 pp survey-weighted sensitivity).
* **Health Equity Audit:** Insured detection: 51/102 (50.0%) vs 52/102 (51.0%). Uninsured detection: 2/13 (15.4%) vs 3/13 (23.1%). Documented with a prominent small denominator note ($N = 13$ latent cases).
* **Non-invasive Predictors:** Strictly restricted to non-invasive anthropometrics: age, sex, BMI, and waist circumference. Poverty Income Ratio (PIR) and insurance coverage were strictly excluded from model inputs and reserved solely for equity audits.

---

## Interactive Lightbox Feature (Web Application)

The web application (`src/html_components.py` and `app.py`) includes a custom lightbox modal for the poster:
* **Trigger:** Clicking or pressing Enter/Space on the poster preview expands the poster into a full-screen lightbox.
* **Close Options:**
  1. Prominent close button (`X`) with a touch target $\ge 44 \times 44\text{ px}$.
  2. Clicking outside the image on the semi-transparent backdrop.
  3. Pressing the `Escape` key (`Esc`).
* **UX Safeguards:** Prevents page scrolling (`document.body.style.overflow = 'hidden'`) while open; contains smooth opacity transitions; supports high-DPI displays; safe layout on mobile screens ($\le 640\text{ px}$).

---

## Primary Literature Citations (APA 7th Edition)

1. American Diabetes Association. (2024). 2. Classification and diagnosis of diabetes: Standards of care in diabetes—2024. *Diabetes Care*, 47(Suppl. 1), S20–S42. https://doi.org/10.2337/dc24-S002
2. Centers for Disease Control and Prevention, National Center for Health Statistics. (2021). *National Health and Nutrition Examination Survey: 2017–March 2020 pre-pandemic examination data files and documentation*. U.S. Department of Health and Human Services. https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2017-2020
3. Centers for Disease Control and Prevention, National Center for Health Statistics. (2024). *National Health and Nutrition Examination Survey: 2021–2023 examination data files and documentation*. U.S. Department of Health and Human Services. https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023
4. Foulds, J. R., Islam, R., Keya, K. N., & Pan, S. (2024). Hierarchical Bayesian models to mitigate systematic disparities in prediction with proxy outcomes. *Journal of the Royal Statistical Society: Series A (Statistics in Society)*, 189(1), 242–265. https://doi.org/10.1093/jrsssa/qnae095
5. National Institute of Diabetes and Digestive and Kidney Diseases. (2022, December). *The A1C test & diabetes*. National Institutes of Health, U.S. Department of Health and Human Services. https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test
6. Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*, 366(6464), 447–453. https://doi.org/10.1126/science.aax2342
7. Vickers, A. J., van Calster, B., & Steyerberg, E. W. (2016). Net benefit approaches to the evaluation of prediction models, molecular markers, and diagnostic tests. *The BMJ*, 352, i6. https://doi.org/10.1136/bmj.i6
