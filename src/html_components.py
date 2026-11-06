# HTML component renderers for HiddenCare interactive research platform.
# Styled according to the Macro Event Lab design system and anti-slop guidelines.

import base64
from pathlib import Path
from src.simulation_engine import evaluate_budget_capacity, compute_economic_nmb, SWAP_DF
from data.verified_constants import COHORT_METRICS

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def get_base64_image(filename: str, mime: str = "image/png") -> str:
    path = ASSETS_DIR / filename
    if path.exists():
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{encoded}"
    return ""


LOGO_URI = get_base64_image("favicon-96x96.png", "image/png")
AVATAR_URI = get_base64_image("avatar.jpg", "image/jpeg")


def render_masthead_html() -> str:
    logo_img = (
        f'<img src="{LOGO_URI}" alt="AanSensei Logo" class="hc-brand-logo" width="28" height="28" />'
        if LOGO_URI
        else ""
    )
    return f"""
<header class="hc-header">
  <div class="hc-header-meta">
    {logo_img}
    <span class="hc-brand">HIDDENCARE</span>
    <span class="hc-meta-bullet">•</span>
    <span class="hc-meta-tag">CDC NHANES 2017–2023</span>
    <span class="hc-meta-bullet">•</span>
    <span class="hc-meta-tag">Population Health Sciences</span>
    <span class="hc-meta-bullet">•</span>
    <span class="hc-meta-tag">Weill Cornell Fellowship Portfolio</span>
  </div>
  <h1 class="hc-header-title">When Clinical History Masks Biological Reality</h1>
  <p class="hc-header-lead">
    How training label definitions reorder the undiagnosed screening queue in population diabetes detection: 
    An empirical investigation of proxy outcome bias across N = 12,459 adults.
  </p>
</header>
"""


def render_site_guide_html() -> str:
    return """
<section class="hc-guide" aria-labelledby="guide-title">
  <div class="hc-guide-header">
    <span class="hc-section-kicker">Navigation & Workflow</span>
    <h2 class="hc-guide-heading" id="guide-title">How to explore this research platform</h2>
    <p class="hc-guide-subtext">
      This platform simulates public health triage under finite clinical resources. Follow the evidence step by step.
    </p>
  </div>
  <ol class="hc-guide-steps">
    <li>
      <span class="hc-guide-num" aria-hidden="true">01</span>
      <div class="hc-guide-step-body">
        <h4>Set screening capacity</h4>
        <p>Adjust the budget slider (5% to 50%) or click preset shortcuts (10%, 20%, 30%) to simulate community testing constraints.</p>
      </div>
    </li>
    <li>
      <span class="hc-guide-num" aria-hidden="true">02</span>
      <div class="hc-guide-step-body">
        <h4>Compare model yields</h4>
        <p>Observe how many hidden cases are detected by Model A (clinical history only) versus Model B (biomarker augmented).</p>
      </div>
    </li>
    <li>
      <span class="hc-guide-num" aria-hidden="true">03</span>
      <div class="hc-guide-step-body">
        <h4>Inspect the 61-person margin</h4>
        <p>Switch to Tab 2 to inspect the exact 61 discordant individuals at the 20% boundary cutoff and see why Label B yields 3.0x higher efficiency.</p>
      </div>
    </li>
    <li>
      <span class="hc-guide-num" aria-hidden="true">04</span>
      <div class="hc-guide-step-body">
        <h4>Audit health equity</h4>
        <p>Examine Tab 3 to audit sensitivity divides across health insurance status and poverty income ratios (PIR).</p>
      </div>
    </li>
  </ol>
</section>
"""


def render_hero_summary_cards() -> str:
    return """
<div class="hc-findings-grid">
  <article class="hc-finding-card">
    <div class="hc-finding-kicker">Development Cohort (2017–Mar 2020)</div>
    <div class="hc-finding-value num">N = 7,761</div>
    <div class="hc-finding-detail">
      <div>• Label A (Diagnosis Only): 1,257 cases (16.20%)</div>
      <div>• Label B (Dx OR HbA1c &ge; 6.5%): 1,484 cases (19.12%)</div>
    </div>
    <div class="hc-finding-badge hc-badge--cyan">
      Hidden Need: +227 Latent Cases
    </div>
  </article>

  <article class="hc-finding-card">
    <div class="hc-finding-kicker">Undiagnosed Holdout (2021–2023)</div>
    <div class="hc-finding-value num">N = 4,698</div>
    <div class="hc-finding-detail">
      <div>• Strictly previously undiagnosed adults at exam</div>
      <div>• True Latent Cases (HbA1c &ge; 6.5%): <b>116 cases</b></div>
    </div>
    <div class="hc-finding-badge hc-badge--neutral">
      Background Prevalence: 2.47%
    </div>
  </article>

  <article class="hc-finding-card hc-finding-card--highlight">
    <div class="hc-finding-kicker">The 20% Budget Margin (K = 939)</div>
    <div class="hc-finding-value num" style="color: var(--detected-emerald);">61 Swapped</div>
    <div class="hc-finding-detail">
      <div>• Consensus Core: 878 shared (52 cases, 5.92% yield)</div>
      <div>• Model A Unique: 1 / 61 cases (1.64% baseline rate)</div>
    </div>
    <div class="hc-finding-badge hc-badge--emerald">
      Model B Unique: 3 / 61 cases (4.92% — 3.0x Yield)
    </div>
  </article>
</div>
"""


def render_simulator_kpi_cards(capacity_pct: int) -> str:
    metrics = evaluate_budget_capacity(capacity_pct)
    k_screened = metrics["k_screened"]

    found_a = metrics["found_a"]
    sens_a = metrics["sens_a"]
    ppv_a = metrics["ppv_a"]
    nns_a = metrics["nns_a"]

    found_b = metrics["found_b"]
    sens_b = metrics["sens_b"]
    ppv_b = metrics["ppv_b"]
    nns_b = metrics["nns_b"]

    found_rand = metrics["found_rand"]
    sens_rand = metrics["sens_rand"]
    ppv_rand = metrics["ppv_rand"]
    nns_rand = metrics["nns_rand"]

    diff_cases = found_b - found_a
    diff_cases_str = f"+{diff_cases}" if diff_cases >= 0 else str(diff_cases)
    diff_sens = round(sens_b - sens_a, 2)
    diff_sens_str = f"+{diff_sens}%" if diff_sens >= 0 else f"{diff_sens}%"

    return f"""
<div class="hc-kpi-grid">
  <article class="hc-kpi-card hc-kpi-card--baseline">
    <div class="hc-kpi-kicker">Random Baseline ({capacity_pct}% Capacity)</div>
    <div class="hc-kpi-hero num">{found_rand} <span class="hc-kpi-denom">/ 116 cases</span></div>
    <div class="hc-kpi-rows">
      <div class="hc-kpi-row"><span>Sensitivity</span><span class="num">{sens_rand}%</span></div>
      <div class="hc-kpi-row"><span>PPV (Precision)</span><span class="num">{ppv_rand}%</span></div>
      <div class="hc-kpi-row"><span>Number Needed to Screen</span><span class="num">{nns_rand} tests</span></div>
      <div class="hc-kpi-row"><span>Screening Quota</span><span class="num">{k_screened:,} / 4,698</span></div>
    </div>
  </article>

  <article class="hc-kpi-card hc-kpi-card--model-a">
    <div class="hc-kpi-kicker">Model A (Diagnosis Only Label)</div>
    <div class="hc-kpi-hero num">{found_a} <span class="hc-kpi-denom">/ 116 cases</span></div>
    <div class="hc-kpi-rows">
      <div class="hc-kpi-row"><span>Sensitivity</span><span class="num">{sens_a}%</span></div>
      <div class="hc-kpi-row"><span>PPV (Precision)</span><span class="num">{ppv_a}%</span></div>
      <div class="hc-kpi-row"><span>Number Needed to Screen</span><span class="num">{nns_a} tests</span></div>
      <div class="hc-kpi-row"><span>Discrimination</span><span class="num">ROC AUC 0.7300</span></div>
    </div>
  </article>

  <article class="hc-kpi-card hc-kpi-card--model-b">
    <div class="hc-kpi-kicker">
      <span>Model B (Biomarker Augmented Label)</span>
      <span class="hc-badge hc-badge--emerald-sm">{diff_cases_str} Cases</span>
    </div>
    <div class="hc-kpi-hero num" style="color: var(--detected-emerald);">{found_b} <span class="hc-kpi-denom">/ 116 cases</span></div>
    <div class="hc-kpi-rows">
      <div class="hc-kpi-row"><span>Sensitivity</span><span class="num"><b>{sens_b}%</b> ({diff_sens_str})</span></div>
      <div class="hc-kpi-row"><span>PPV (Precision)</span><span class="num"><b>{ppv_b}%</b></span></div>
      <div class="hc-kpi-row"><span>Number Needed to Screen</span><span class="num"><b>{nns_b} tests</b></span></div>
      <div class="hc-kpi-row"><span>Discrimination</span><span class="num">ROC AUC 0.7410</span></div>
    </div>
  </article>
</div>
"""


def render_margin_table_html(filter_selection: str) -> str:
    df = SWAP_DF.copy()

    if "3 True Positive" in filter_selection:
        df = df[(df["potential_case"] == 1) & (df["swap_group"].str.contains("Model B"))]
    elif "All 61 Model B" in filter_selection:
        df = df[df["swap_group"].str.contains("Model B")]
    elif "61 Model A" in filter_selection:
        df = df[df["swap_group"].str.contains("Model A")]

    rows_html = []
    for _, row in df.head(15).iterrows():
        is_case = row["potential_case"] == 1
        row_class = "row-rescued" if is_case else ""
        gender = "Male" if row["sex"] == 1.0 else "Female"
        a1c_display = f"<b>{row['a1c']}%</b>" if is_case else f"{row['a1c']}%"
        status_badge = (
            '<span class="hc-badge hc-badge--emerald">Rescued Case (HbA1c &ge; 6.5%)</span>'
            if is_case
            else '<span class="hc-badge hc-badge--neutral">Normal</span>'
        )

        rows_html.append(f"""
<tr class="{row_class}">
  <td class="num"><b>#{int(row['seqn'])}</b></td>
  <td>{int(row['age'])}y / {gender}</td>
  <td class="num">BMI {row['bmi']:.1f} • Waist {row['waist']:.1f}cm</td>
  <td>{str(row['insured']).title()} • {str(row['pir_group']).title()} PIR</td>
  <td class="num">Rank A: #{row['rank_dx']} • Rank B: #{row['rank_full']}</td>
  <td class="num">{a1c_display}</td>
  <td>{status_badge}</td>
</tr>
""")

    table_body = "".join(rows_html)
    total_count = len(df)
    shown_text = f"Showing top {min(15, total_count)} of {total_count} matching profiles"

    return f"""
<div class="hc-table-container">
  <div class="hc-table-caption">
    {shown_text}
  </div>
  <table class="hc-table">
    <thead>
      <tr>
        <th>SEQN</th>
        <th>Demographics</th>
        <th>Anthropometry</th>
        <th>Access & Income</th>
        <th>Priority Ranking</th>
        <th>Observed HbA1c</th>
        <th>Clinical Status</th>
      </tr>
    </thead>
    <tbody>
      {table_body}
    </tbody>
  </table>
</div>
"""


def render_equity_callout_html() -> str:
    return """
<div class="hc-callout hc-callout--rose">
  <div class="hc-callout-title">
    Structural Access Disparity & Statistical Honesty Callout
  </div>
  <div class="hc-callout-body">
    <p><b>1. The 3x Insurance Sensitivity Divide:</b> At the primary 20% capacity budget, both models successfully detect ~50.0% of latent cases among insured individuals (51/102 cases for Model A, 52/102 for Model B). Conversely, screening sensitivity drops to <b>15.4% (Model A)</b> and <b>23.1% (Model B)</b> among uninsured individuals, leaving over 75% of uninsured cases undetected.</p>
    <p><b>2. Relative Biomarker Recovery:</b> Incorporating the laboratory biomarker (Model B) allocates 6 additional screening slots to uninsured participants and catches <b>+1 additional true case</b> (+50% relative increase in yield), demonstrating that biomarker augmentation partially corrects access bias.</p>
    <p><b>3. Small-Sample Integrity:</b> In the holdout cohort of previously undiagnosed adults, the uninsured subgroup holds N = 422 participants with exactly 13 latent positive cases. In accordance with biostatistical best practices, we report exact participant counts and avoid over-extrapolating small-sample estimates into sweeping algorithmic fairness claims.</p>
  </div>
</div>
"""


def render_economic_ledger_html(
    capacity_pct: int, cost_test: float, benefit_early: float
) -> str:
    econ = compute_economic_nmb(capacity_pct, cost_test, benefit_early)

    return f"""
<div class="hc-card" style="margin-top: 10px;">
  <div class="hc-metric-label">Economic & Clinical Impact Ledger (Budget: {capacity_pct}%)</div>
  <table class="hc-table" style="margin: 8px 0 14px 0;">
    <thead>
      <tr>
        <th>Allocation Policy</th>
        <th>Cases Found</th>
        <th>Total Testing Cost</th>
        <th>Cost per Case Detected</th>
        <th>Net Monetary Benefit (NMB)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Random Outreach</b></td>
        <td class="num">{econ['cost_per_case_rand']:.1f}</td>
        <td class="num">${econ['total_cost']:,.0f}</td>
        <td class="num">${econ['cost_per_case_rand']:,.0f}</td>
        <td class="num">${econ['nmb_rand']:,.0f}</td>
      </tr>
      <tr>
        <td><b>Model A (Diagnosis Only)</b></td>
        <td class="num">{evaluate_budget_capacity(capacity_pct)['found_a']}</td>
        <td class="num">${econ['total_cost']:,.0f}</td>
        <td class="num">${econ['cost_per_case_a']:,.0f}</td>
        <td class="num">${econ['nmb_a']:,.0f}</td>
      </tr>
      <tr class="row-rescued">
        <td><b>Model B (Combined Biomarker)</b></td>
        <td class="num"><b>{evaluate_budget_capacity(capacity_pct)['found_b']}</b></td>
        <td class="num">${econ['total_cost']:,.0f}</td>
        <td class="num"><b>${econ['cost_per_case_b']:,.0f}</b></td>
        <td class="num"><b>${econ['nmb_b']:,.0f}</b></td>
      </tr>
    </tbody>
  </table>

  <div class="hc-callout hc-callout--emerald">
    <div class="hc-callout-title" style="color: #047857;">
      Zero Marginal Cost Policy Improvement
    </div>
    <div class="hc-callout-body">
      Because both models use the exact same testing quota ({econ['k_screened']:,} tests; $\\Delta\\text{{Cost}} = \\$0$), shifting from Label A to Label B yields an 
      <b>Incremental Net Benefit of +${econ['incremental_nmb']:,.0f}</b> on this holdout cohort (or <b>+${econ['nmb_gain_10k']:,.0f} per 10,000 undiagnosed adults</b>) by identifying {econ['incremental_cases']} additional cases at zero additional laboratory expenditure.
    </div>
  </div>
</div>
"""


def render_about_page_html() -> str:
    avatar_html = (
        f'<img src="{AVATAR_URI}" alt="An Nguyen" class="author-photo" width="96" height="96" />'
        if AVATAR_URI
        else ""
    )
    return f"""
<article class="hc-about-page">
  <div class="hc-about-header">
    <h2 class="t-h1">About HiddenCare</h2>
    <p class="about-lead">
      HiddenCare investigates how proxy labeling in algorithmic healthcare triage alters who is prioritized for preventive screening under real-world resource constraints.
    </p>
  </div>

  <!-- The project at a glance: 4 rows like macro-event-lab -->
  <section class="about-section">
    <h3 class="t-h2">The Project at a Glance</h3>
    <dl class="about-rows glance-rows" aria-label="The project at a glance">
      <div>
        <dt>The problem</dt>
        <dd>Predictive screening models frequently train on self-reported clinical history or administrative billing codes (ICD-10). These proxy outcomes measure healthcare access and insurance status rather than pure biological disease, penalizing undiagnosed, marginalized patients at the screening margin.</dd>
      </div>
      <div>
        <dt>What it does</dt>
        <dd>Re-evaluates N = 4,698 previously undiagnosed US adults from the post-pandemic CDC NHANES 2021–2023 cycle under fixed screening budgets (10%, 20%, 30%). Identifies the exact individuals who shift in the triage queue and audits who gets left behind across insurance and income strata.</dd>
      </div>
      <div>
        <dt>How</dt>
        <dd>Trains regularized Logistic Regression on pre-pandemic NHANES (2017–March 2020; N = 7,761) comparing Diagnosis-Only labels (Label A) against Biomarker-Augmented labels (Label B: Diagnosis OR HbA1c &ge; 6.5%), holding non-invasive predictors (age, sex, BMI, waist circumference) completely identical.</dd>
      </div>
      <div>
        <dt>Built with</dt>
        <dd>Python, DuckDB, Parquet, scikit-learn, Gradio, Plotly, pytest, with raw data from the CDC National Center for Health Statistics (NHANES).</dd>
      </div>
    </dl>
  </section>

  <!-- Why this way -->
  <section class="about-section">
    <h3 class="t-h2">Why This Way</h3>
    <dl class="about-rows">
      <div>
        <dt>Biological reality over administrative proxies</dt>
        <dd>Receiving a diabetes diagnosis requires visiting a doctor, having insurance, and affording lab tests. Having elevated blood sugar requires none of those. By training on observed laboratory HbA1c, we decouple biological pathology from socioeconomic access.</dd>
      </div>
      <div>
        <dt>The whole capacity curve</dt>
        <dd>Public health outreach operates under finite testing capacity (e.g., funding for 1,000 HbA1c kits), not theoretical 0.5 probability thresholds. We evaluate models across continuous budget allocations from 5% to 50% of the population.</dd>
      </div>
      <div>
        <dt>Checked, not just shown</dt>
        <dd>Every model prediction is validated against observed venous blood laboratory HbA1c from CDC mobile examination centers. Disagreements are verified patient-by-patient at the individual level.</dd>
      </div>
      <div>
        <dt>Readable without an epidemiology degree</dt>
        <dd>The interface translates complex statistical trade-offs into plain language, interactive capacity curves, and explicit demographic ledgers.</dd>
      </div>
      <div>
        <dt>Honest about sample bounds</dt>
        <dd>The uninsured evaluation cohort contains N = 422 adults with 13 true cases. We report exact participant counts and avoid overbroad claims regarding algorithmic fairness.</dd>
      </div>
      <div>
        <dt>An engineering project</dt>
        <dd>Behind this site is an automated, verified data pipeline: binary SAS XPT headers validation, survey weight mapping across cycles, zero target leakage assertion, and pre-computed columnar Parquet lookup tables.</dd>
      </div>
    </dl>
  </section>

  <!-- The 5 Research Questions -->
  <section class="about-section">
    <h3 class="t-h2">Core Research Questions</h3>
    <ul class="idea-questions">
      <li>Does training an algorithm on laboratory-augmented biological ground truth alter which undiagnosed adults are prioritized for screening under fixed budget caps?</li>
      <li>Under a 20% outreach budget constraint (K = 939 slots), how many additional unrecognized cases of diabetes are captured?</li>
      <li>What are the clinical, demographic, and socioeconomic profiles of the 61 individuals swapped at the capacity margin?</li>
      <li>Are uninsured and low-income individuals systematically penalized by models trained solely on self-reported clinical history?</li>
      <li>What is the Net Monetary Benefit (NMB) of biological label retraining when accounting for test kit costs and early intervention savings?</li>
    </ul>
  </section>

  <!-- Author Profile -->
  <section class="about-section">
    <h3 class="t-h2">Author & Institutional Target</h3>
    <div class="author-card">
      {avatar_html}
      <div class="author-info">
        <h4 style="margin: 0 0 4px 0; font-size: 1.15rem; color: var(--text);">An Nguyen (AanSensei)</h4>
        <p style="margin: 0 0 10px 0; color: var(--accent); font-weight: 500; font-size: 0.95rem;">
          University of Wisconsin–Madison • B.S. Economics & Data Science
        </p>
        <p style="margin: 0 0 12px 0; color: var(--text-muted); line-height: 1.6; font-size: 0.92rem;">
          Flagship biostatistics portfolio project for application to the <b>Weill Cornell Medicine Biostatistics Summer Internship 2027</b> (Department of Population Health Sciences, Division of Biostatistics).
        </p>
        <div style="font-size: 0.88rem; color: var(--text-muted);">
          <b>Email:</b> nguyencaothienan937@gmail.com • <b>Website:</b> <a href="https://aansensei.github.io" target="_blank" style="color: var(--accent); text-decoration: underline;">aansensei.github.io</a> • <b>GitHub:</b> <a href="https://github.com/aansensei/HiddenCare" target="_blank" style="color: var(--accent); text-decoration: underline;">github.com/aansensei/HiddenCare</a>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="about-section" style="margin-bottom: 40px;">
    <h3 class="t-h2">Frequently Asked Questions</h3>
    <dl class="about-rows">
      <div>
        <dt>What is "proxy outcome bias"?</dt>
        <dd>When an algorithm is trained to predict an observable administrative label (such as a billing code or self-reported diagnosis) rather than the true underlying condition. Because receiving a diagnosis requires healthcare access, the model learns predictors of healthcare utilization rather than biological risk.</dd>
      </div>
      <div>
        <dt>Why only 4 non-invasive predictors?</dt>
        <dd>High-dimensional clinical models requiring laboratory panels cannot be deployed in resource-limited community outreach because they require the very clinical visit we are trying to triage. Non-invasive markers (age, sex, BMI, waist circumference) allow zero-cost community screening.</dd>
      </div>
      <div>
        <dt>Is an elevated HbA1c a definitive diagnosis?</dt>
        <dd>No. In cross-sectional population surveys like NHANES, a single HbA1c measurement above 6.5% serves as an epidemiological screening criterion. Clinical diagnostic confirmation requires repeat laboratory testing.</dd>
      </div>
      <div>
        <dt>Can I reproduce this entire study?</dt>
        <dd>Yes. All raw CDC SAS transport files, preprocessing pipelines, model checkpoints, unit tests, and pre-computed Parquet tables are fully open-source and reproducible with a single command: <code>python run.py</code>.</dd>
      </div>
    </dl>
  </section>
</article>
"""
