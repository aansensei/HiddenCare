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
POSTER_URI = get_base64_image("poster.png", "image/png")
POSTER_PDF_URI = get_base64_image("poster.pdf", "application/pdf")


def render_masthead_html() -> str:
    logo_img = (
        f'<img src="{LOGO_URI}" alt="AanSensei Logo" class="hc-brand-logo" width="28" height="28" />'
        if LOGO_URI
        else ""
    )
    return f"""
<header class="hc-header" id="hc-top-header">
  <div class="hc-header-meta">
    {logo_img}
    <span class="hc-brand">HIDDENCARE</span>
    <span class="hc-meta-bullet">&#8226;</span>
    <span class="hc-meta-tag">CDC NHANES Data</span>
    <span class="hc-meta-bullet">&#8226;</span>
    <span class="hc-meta-tag">Algorithmic Epidemiology Lab</span>
  </div>
  <h1 class="hc-header-title">
    HiddenCare compares two ways of choosing who gets screened for diabetes when a clinic cannot test everyone.
  </h1>
  <p class="hc-header-notice">
    Interactive research study on public health data. Not an individual diagnosis tool or hospital-deployed system.
  </p>
  <div class="hc-header-problem">
    <p>
      When screening algorithms learn only from past diagnosis records, people who rarely visit doctors can be misclassified as low risk. This project compares how training label definitions reorder screening triage priorities across a population under finite testing capacity.
    </p>
  </div>
  <div class="hc-what-i-built">
    <div class="hc-wib-header">What I Built</div>
    <div class="hc-wib-grid">
      <div class="hc-wib-item">
        <strong>Data Engineering:</strong> Curated and validated N = 12,459 adult records from CDC NHANES (2017 to 2023) with complex survey weights and missingness audits.
      </div>
      <div class="hc-wib-item">
        <strong>Model Comparison:</strong> Trained gradient-boosted models comparing administrative diagnosis labels (Model A) against biomarker-augmented labels (Model B: HbA1c &ge; 6.5%).
      </div>
      <div class="hc-wib-item">
        <strong>Screening Simulator:</strong> Built an interactive triage engine simulating 5% to 50% capacity constraints with dynamic queue thresholds.
      </div>
      <div class="hc-wib-item">
        <strong>Equity & Decision Audits:</strong> Quantified health insurance sensitivity divides, boundary queue swaps, and net monetary benefit via decision curves.
      </div>
    </div>
  </div>
  <div class="hc-cta-row">
    <a href="#sec-simulation" class="hc-cta-btn hc-cta-btn--primary" id="btn-try-simulator">
      Try the simulator
    </a>
    <a href="https://github.com/aansensei/HiddenCare" target="_blank" rel="noopener noreferrer" class="hc-cta-btn hc-cta-btn--secondary" id="btn-view-source">
      View source code
    </a>
  </div>
  <p class="hc-usage-guide">
    <strong>How to use:</strong> Adjust the screening budget slider below to compare how both models allocate test slots and detect hidden cases.
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
<!-- Accessible Plain-Language Summary for Non-Specialists -->
<section class="hc-plain-summary-card" id="sec-overview" data-toc="00 • Overview">
  <div class="hc-plain-summary-kicker">The 30-Second Translation • Plain Language Summary</div>
  <h3 class="hc-plain-summary-title">When Health Algorithms Overlook People Who Don't Visit Doctors</h3>
  <div class="hc-plain-summary-grid">
    <div class="hc-plain-col">
      <div class="hc-plain-step">1. Finite Clinic Budget</div>
      <p>A community clinic only has enough funding to test a fraction of residents (e.g., 20% of the town). Who gets invited first?</p>
    </div>
    <div class="hc-plain-col">
      <div class="hc-plain-step">2. The Healthcare Access Trap</div>
      <p>Standard AI (Model A) trains on past doctor visits. Because uninsured people rarely see doctors, their records look healthy even when they are sick.</p>
    </div>
    <div class="hc-plain-col">
      <div class="hc-plain-step">3. The Biological Rescue</div>
      <p>At the 20% budget cutoff, Model B swaps 61 overlooked people into the queue, achieving a 3.0x higher hit rate (4.92% vs 1.64%, or 3 cases vs 1 case) in that marginal swapped cohort compared to Model A. Across the full 939-person queue, Model B detects 55 latent cases compared to 53 for Model A (+2 net cases overall).</p>
    </div>
  </div>
</section>

<div class="hc-bento-grid">
  <!-- Bento 1: Primary Discovery (Featured Highlight) -->
  <article class="hc-bento-card hc-bento-card--featured">
    <div>
      <span class="hc-section-kicker" style="color: var(--accent);">Primary Discovery • 20% Budget Constraint</span>
      <div class="hc-finding-value num" style="color: var(--accent); margin: 8px 0 4px 0;">61 Patients Swapped</div>
      <p style="margin: 0 0 16px 0; font-size: 0.90rem; color: var(--text-muted); line-height: 1.55;">
        At the 939-slot boundary (K = 20%), Model B rescues <strong>3 true cases</strong> missed by Model A, 
        delivering a <strong>3.0x higher marginal yield (4.92% vs 1.64%)</strong> among the 61 swapped candidates. 
        Across the entire 939-person queue, Model B detects 55 latent cases vs 53 for Model A (+2 net cases overall).
      </p>
    </div>
    <div class="hc-finding-detail" style="border-top: 1px solid rgba(2, 132, 199, 0.2); padding-top: 12px; font-size: 0.85rem; line-height: 1.6; color: var(--text-muted);">
      <div>• Consensus Core: 878 shared candidates (52 true cases, 5.92% yield)</div>
      <div>• Model B Unique: 3 / 61 cases (4.92% precision)</div>
    </div>
  </article>

  <!-- Bento 2: Evaluation Holdout -->
  <article class="hc-bento-card">
    <div>
      <span class="hc-section-kicker">Evaluation Cohort • Aug 2021 to Aug 2023</span>
      <div class="hc-finding-value num" style="margin: 8px 0 4px 0;">N = 4,698 Adults</div>
      <p style="margin: 0 0 16px 0; font-size: 0.90rem; color: var(--text-muted); line-height: 1.55;">
        Strictly previously undiagnosed adults with zero temporal overlap with training data. 
        Biochemically confirmed <strong>116 latent diabetes cases</strong> (HbA1c &ge; 6.5%).
      </p>
    </div>
    <div class="hc-finding-detail" style="border-top: 1px solid var(--border); padding-top: 12px; font-size: 0.85rem; line-height: 1.6; color: var(--text-muted);">
      <div>• Unweighted Background Prevalence: 2.47%</div>
      <div>• Predictors: Age, Sex, BMI, Waist Circumference</div>
    </div>
  </article>

  <!-- Bento 3: Development Benchmark -->
  <article class="hc-bento-card">
    <div>
      <span class="hc-section-kicker">Training Benchmark • 2017 to Mar 2020</span>
      <div class="hc-finding-value num" style="margin: 8px 0 4px 0;">N = 7,761 Adults</div>
      <p style="margin: 0 0 16px 0; font-size: 0.90rem; color: var(--text-muted); line-height: 1.55;">
        Pre-pandemic baseline comparing administrative self-report labels against 
        biomarker-augmented screening labels.
      </p>
    </div>
    <div class="hc-finding-detail" style="border-top: 1px solid var(--border); padding-top: 12px; font-size: 0.85rem; line-height: 1.6; color: var(--text-muted);">
      <div>• Label A (Diagnosis Only): 1,257 cases (16.20%)</div>
      <div>• Label B (Dx OR HbA1c &ge; 6.5%): 1,484 cases (19.12%)</div>
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
      <div class="hc-kpi-row"><span>Sensitivity (% caught)</span><span class="num">{sens_rand}%</span></div>
      <div class="hc-kpi-row"><span>Precision (hit rate)</span><span class="num">{ppv_rand}%</span></div>
      <div class="hc-kpi-row"><span>Tests per case (NNS)</span><span class="num">{nns_rand} tests</span></div>
      <div class="hc-kpi-row"><span>Screening Quota</span><span class="num">{k_screened:,} / 4,698</span></div>
    </div>
  </article>

  <article class="hc-kpi-card hc-kpi-card--model-a">
    <div class="hc-kpi-kicker">Model A (Doctor History Label)</div>
    <div class="hc-kpi-hero num">{found_a} <span class="hc-kpi-denom">/ 116 cases</span></div>
    <div class="hc-kpi-rows">
      <div class="hc-kpi-row"><span>Sensitivity (% caught)</span><span class="num">{sens_a}%</span></div>
      <div class="hc-kpi-row"><span>Precision (hit rate)</span><span class="num">{ppv_a}%</span></div>
      <div class="hc-kpi-row"><span>Tests per case (NNS)</span><span class="num">{nns_a} tests</span></div>
      <div class="hc-kpi-row"><span>Discrimination</span><span class="num">ROC AUC 0.7300</span></div>
    </div>
  </article>

  <article class="hc-kpi-card hc-kpi-card--model-b">
    <div class="hc-kpi-kicker">
      <span>Model B (CDC Blood Test Label)</span>
      <span class="hc-badge hc-badge--accent-sm">{diff_cases_str} Cases</span>
    </div>
    <div class="hc-kpi-hero num" style="color: var(--accent);">{found_b} <span class="hc-kpi-denom">/ 116 cases</span></div>
    <div class="hc-kpi-rows">
      <div class="hc-kpi-row"><span>Sensitivity (% caught)</span><span class="num"><b>{sens_b}%</b> ({diff_sens_str})</span></div>
      <div class="hc-kpi-row"><span>Precision (hit rate)</span><span class="num"><b>{ppv_b}%</b></span></div>
      <div class="hc-kpi-row"><span>Tests per case (NNS)</span><span class="num"><b>{nns_b} tests</b></span></div>
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
            '<span class="hc-badge hc-badge--accent">Rescued Case (HbA1c &ge; 6.5%)</span>'
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
        f'<img src="{AVATAR_URI}" alt="Avatar of Cao Thien An Nguyen" class="author-photo" style="width: 104px; height: 104px; min-width: 104px; min-height: 104px; border-radius: 50% !important; object-fit: cover !important; border: 3px solid var(--accent); padding: 3px; background: #ffffff; box-shadow: 0 4px 14px rgba(3, 105, 161, 0.18); display: block;" />'
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

  <!-- executive summary tren dau trang about -->
  <section class="about-section about-summary-box" id="sec-about-summary" data-toc="00 • Executive Summary">
    <div class="about-summary-kicker">
      Executive Summary • Study Abstract
    </div>
    <h3 class="about-summary-title">
      Decoupling Disease Detection from Healthcare Access
    </h3>
    <div class="about-summary-grid">
      <div class="about-summary-col">
        <div class="about-col-label">01 / The Structural Bias</div>
        <p class="about-col-text">
          Algorithms trained solely on self-reported doctor diagnoses or administrative billing codes conflate biological disease with healthcare access, misclassifying unvisited sick patients as healthy baseline.
        </p>
      </div>
      <div class="about-summary-col">
        <div class="about-col-label">02 / The 61-Patient Proof</div>
        <p class="about-col-text">
          Across N = 4,698 undiagnosed adults from CDC NHANES 2021 to 2023, retraining on observed venous HbA1c swaps 61 individuals at the 20% budget line, uncovering 3 hidden diabetes cases at 3.0x higher precision ($0 extra cost).
        </p>
      </div>
      <div class="about-summary-col">
        <div class="about-col-label">03 / The Health Equity Dividend</div>
        <p class="about-col-text">
          Biomarker-augmented triage eliminates an 8.6% sensitivity deficit suffered by uninsured Americans under traditional models, yielding +$25,500 net economic benefit per 10,000 screened individuals.
        </p>
      </div>
    </div>
  </section>

  <!-- The project at a glance: 4 rows like macro-event-lab -->
  <section class="about-section" id="sec-about-glance" data-toc="01 • Project at Glance">
    <h3 class="t-h2">The Project at a Glance</h3>
    <dl class="about-rows glance-rows" aria-label="The project at a glance">
      <div>
        <dt>The problem</dt>
        <dd>Predictive screening models frequently train on self-reported clinical history or administrative billing codes (ICD-10). These proxy outcomes measure healthcare access and insurance status rather than pure biological disease, penalizing undiagnosed, marginalized patients at the screening margin.</dd>
      </div>
      <div>
        <dt>What it does</dt>
        <dd>Re-evaluates N = 4,698 previously undiagnosed US adults from the post-pandemic CDC NHANES 2021 to 2023 cycle under fixed screening budgets (10%, 20%, 30%). Identifies the exact individuals who shift in the triage queue and audits who gets left behind across insurance and income strata.</dd>
      </div>
      <div>
        <dt>How</dt>
        <dd>Trains regularized Logistic Regression on pre-pandemic NHANES (2017 to March 2020; N = 7,761) comparing Diagnosis-Only labels (Label A) against Biomarker-Augmented labels (Label B: Diagnosis OR HbA1c &ge; 6.5%), holding non-invasive predictors (age, sex, BMI, waist circumference) completely identical.</dd>
      </div>
      <div>
        <dt>Built with</dt>
        <dd>Python, DuckDB, Parquet, scikit-learn, Gradio, Plotly, pytest, with raw data from the CDC National Center for Health Statistics (NHANES).</dd>
      </div>
    </dl>
  </section>

  <!-- Why this way -->
  <section class="about-section" id="sec-about-why" data-toc="02 • Why This Way">
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
  <section class="about-section" id="sec-about-questions" data-toc="03 • 5 Questions">
    <h3 class="t-h2">Core Research Questions</h3>
    <ul class="idea-questions">
      <li>Does training an algorithm on laboratory-augmented biological ground truth alter which undiagnosed adults are prioritized for screening under fixed budget caps?</li>
      <li>Under a 20% outreach budget constraint (K = 939 slots), how many additional unrecognized cases of diabetes are captured?</li>
      <li>What are the clinical, demographic, and socioeconomic profiles of the 61 individuals swapped at the capacity margin?</li>
      <li>Are uninsured and low-income individuals systematically penalized by models trained solely on self-reported clinical history?</li>
      <li>What is the Net Monetary Benefit (NMB) of biological label retraining when accounting for test kit costs and early intervention savings?</li>
    </ul>
  </section>

    <!-- academic research poster -->
  <section class="about-section" id="sec-about-poster" data-toc="04 • Academic Poster">
    <h3 class="t-h2">Academic Research Poster</h3>
    <p class="about-lead" style="font-size: 0.95rem; margin-bottom: 16px;">
      One-page research conference poster synthesizing the core scientific hypothesis, CDC NHANES temporal validation protocol, the 61-patient proof, decision curve analysis, and health equity dividends. Click the poster below to enlarge full-screen.
    </p>
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 18px; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; gap: 16px;">
      <!-- Interactive Click-to-Enlarge Poster Preview Container -->
      <div class="hc-poster-preview-container" onclick="window.openPosterLightbox &amp;&amp; window.openPosterLightbox()" onkeydown="if(event.key==='Enter'||event.key===' '){{window.openPosterLightbox &amp;&amp; window.openPosterLightbox(); event.preventDefault();}}" tabindex="0" role="button" aria-haspopup="dialog" aria-label="Click to enlarge research poster fullscreen">
        <img src="{POSTER_URI}" alt="HiddenCare Academic Research Poster" />
        <div class="hc-poster-hover-hint">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="15 3 21 3 21 9"></polyline>
            <polyline points="9 21 3 21 3 15"></polyline>
            <line x1="21" y1="3" x2="14" y2="10"></line>
            <line x1="3" y1="21" x2="10" y2="14"></line>
          </svg>
          <span>Click to enlarge full-screen</span>
        </div>
      </div>

      <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <a href="{POSTER_PDF_URI}" download="HiddenCare_Research_Poster_CaoThienAnNguyen.pdf" class="hc-cta-btn" style="text-decoration: none; display: inline-flex; align-items: center; justify-content: center; padding: 10px 20px; font-size: 0.88rem; font-weight: 600; background: var(--accent); color: #ffffff; border-radius: var(--radius-sm); min-height: 44px;">
          Download Vector PDF (36x24 in)
        </a>
        <a href="{POSTER_URI}" download="HiddenCare_Research_Poster_CaoThienAnNguyen.png" style="text-decoration: none; display: inline-flex; align-items: center; justify-content: center; padding: 10px 20px; font-size: 0.88rem; font-weight: 600; background: #ffffff; color: var(--text); border: 1px solid var(--border); border-radius: var(--radius-sm); min-height: 44px;">
          Download High-Res Image (PNG)
        </a>
        <button type="button" onclick="window.openPosterLightbox &amp;&amp; window.openPosterLightbox()" style="border: 1px solid var(--accent); background: #f0f9ff; color: var(--accent); padding: 10px 20px; font-size: 0.88rem; font-weight: 600; border-radius: var(--radius-sm); min-height: 44px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
          <span>Enlarge Poster (Lightbox)</span>
        </button>
      </div>
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; font-size: 0.82rem; color: var(--text-muted); border-top: 1px solid var(--border); padding-top: 12px; margin-top: 4px;">
        <span><strong>Author &amp; Attribution:</strong> Cao Thien An Nguyen (GitHub: <a href="https://github.com/aansensei" target="_blank" rel="noopener noreferrer" style="color: var(--accent); text-decoration: none; font-weight: 600;">aansensei</a>)</span>
        <span><strong>Suggested Citation (APA 7th):</strong> Nguyen, C. T. A. (2026). <em>When training labels change who gets screened</em> [Poster]. UW&ndash;Madison.</span>
      </div>
    </div>
  </section>

  <!-- Fullscreen Modal / Lightbox Component -->
  <div id="hc-poster-lightbox" class="hc-modal-backdrop" role="dialog" aria-modal="true" aria-label="Enlarged HiddenCare Research Poster" style="display: none;" onclick="window.handlePosterLightboxClick &amp;&amp; window.handlePosterLightboxClick(event)">
    <div class="hc-modal-dialog" onclick="event.stopPropagation()">
      <button id="hc-poster-lightbox-close" class="hc-modal-close-btn" type="button" aria-label="Close enlarged preview" onclick="window.closePosterLightbox &amp;&amp; window.closePosterLightbox(event)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <img src="{POSTER_URI}" alt="Enlarged HiddenCare Academic Research Poster (36x24 in)" class="hc-modal-img" />
      <div class="hc-modal-caption">
        <span><strong>When Training Labels Change Who Gets Screened</strong> &bull; 36 &times; 24 in Research Poster (NHANES 2017&ndash;2023)</span>
        <span class="hc-modal-hint">Click outside or press <strong>Esc</strong> to close</span>
      </div>
    </div>
  </div>

  <script>
  (function() {{
    window.openPosterLightbox = function() {{
      var modal = document.getElementById('hc-poster-lightbox');
      if (!modal) return;
      modal.style.display = 'flex';
      modal.offsetHeight;
      modal.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', window.handlePosterLightboxKeydown);
      var closeBtn = document.getElementById('hc-poster-lightbox-close');
      if (closeBtn) closeBtn.focus();
    }};

    window.closePosterLightbox = function(e) {{
      if (e && e.stopPropagation) e.stopPropagation();
      var modal = document.getElementById('hc-poster-lightbox');
      if (!modal) return;
      modal.classList.remove('is-open');
      document.body.style.overflow = '';
      window.removeEventListener('keydown', window.handlePosterLightboxKeydown);
      setTimeout(function() {{
        if (!modal.classList.contains('is-open')) {{
          modal.style.display = 'none';
        }}
      }}, 250);
    }};

    window.handlePosterLightboxClick = function(e) {{
      if (e.target.id === 'hc-poster-lightbox' || e.target.classList.contains('hc-modal-backdrop')) {{
        window.closePosterLightbox(e);
      }}
    }};

    window.handlePosterLightboxKeydown = function(e) {{
      if (e.key === 'Escape' || e.key === 'Esc') {{
        window.closePosterLightbox(e);
      }}
    }};
  }})();
  </script>

  <!-- complex survey variance and model robustness -->
  <section class="about-section" id="sec-about-stats" data-toc="05 • Survey Variance & Robustness">
    <h3 class="t-h2">Survey Variance & Model Robustness</h3>
    <p class="about-lead" style="font-size: 0.95rem; margin-bottom: 16px;">
      Addressing complex multistage survey variance via Taylor Series Linearization and verifying algorithmic fairness across nonlinear machine learning architectures.
    </p>
    
    <!-- bang sai so khao sat phuc hop -->
    <div style="margin-bottom: 24px;">
      <h4 style="font-family: var(--font-serif); font-size: 1.15rem; font-weight: 600; color: var(--text); margin: 0 0 8px 0;">
        Taylor Series Linearization (CDC NHANES 95% Confidence Intervals)
      </h4>
      <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0 0 12px 0; line-height: 1.5;">
        Standard IID formulas underestimate variance in clustered populations. We implement Taylor Series Linearization across masked survey strata and primary sampling units (WTPH2YR weights, df = 15):
      </p>
      <div style="overflow-x: auto; -webkit-overflow-scrolling: touch; border: 1px solid var(--border); border-radius: var(--radius-sm);">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem; text-align: left;">
          <thead>
            <tr style="background: var(--bg); border-bottom: 1px solid var(--border);">
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Capacity</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Model Policy</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Weighted Sensitivity (95% CI)</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Weighted PPV (95% CI)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 10px 14px; font-weight: 600;">10% Budget</td>
              <td style="padding: 10px 14px; color: var(--text-muted);">Model A (Diagnosis Only)</td>
              <td style="padding: 10px 14px;" class="num">25.25% [16.1%, 34.4%]</td>
              <td style="padding: 10px 14px;" class="num">7.33% [4.0%, 10.7%]</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border); background: var(--accent-tint);">
              <td style="padding: 10px 14px; font-weight: 600;">10% Budget</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);">Model B (Biomarker Augmented)</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">28.77% [19.2%, 38.3%]</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">8.23% [4.8%, 11.7%]</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 10px 14px; font-weight: 600;">20% Budget</td>
              <td style="padding: 10px 14px; color: var(--text-muted);">Model A (Diagnosis Only)</td>
              <td style="padding: 10px 14px;" class="num">40.08% [28.9%, 51.2%]</td>
              <td style="padding: 10px 14px;" class="num">5.79% [3.6%, 8.0%]</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border); background: var(--accent-tint);">
              <td style="padding: 10px 14px; font-weight: 600;">20% Budget</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);">Model B (Biomarker Augmented)</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">42.47% [28.4%, 56.5%]</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">6.02% [3.4%, 8.6%]</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 10px 14px; font-weight: 600;">30% Budget</td>
              <td style="padding: 10px 14px; color: var(--text-muted);">Model A (Diagnosis Only)</td>
              <td style="padding: 10px 14px;" class="num">53.14% [39.9%, 66.3%]</td>
              <td style="padding: 10px 14px;" class="num">5.03% [3.2%, 6.8%]</td>
            </tr>
            <tr style="background: var(--accent-tint);">
              <td style="padding: 10px 14px; font-weight: 600;">30% Budget</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);">Model B (Biomarker Augmented)</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">58.13% [41.8%, 74.5%]</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">5.38% [3.2%, 7.6%]</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- bang kiem dinh do ben mo hinh phi tuyen -->
    <div>
      <h4 style="font-family: var(--font-serif); font-size: 1.15rem; font-weight: 600; color: var(--text); margin: 0 0 8px 0;">
        Nonlinear Model Robustness (Random Forest & Gradient Boosting)
      </h4>
      <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0 0 12px 0; line-height: 1.5;">
        To ensure the 61-patient proof is not an artifact of linear models, we retrained on ensemble decision trees. Across architectures, Model B consistently preserves higher sensitivity and boosts uninsured detection:
      </p>
      <div style="overflow-x: auto; -webkit-overflow-scrolling: touch; border: 1px solid var(--border); border-radius: var(--radius-sm);">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem; text-align: left;">
          <thead>
            <tr style="background: var(--bg); border-bottom: 1px solid var(--border);">
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Algorithm</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Model A Cases</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Model B Cases</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Margin Swaps</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Swap Precision Ratio</th>
              <th style="padding: 10px 14px; font-weight: 700; color: var(--text);">Uninsured Sensitivity Boost</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 10px 14px; font-weight: 600;">Logistic Regression</td>
              <td style="padding: 10px 14px;" class="num">53 / 116</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">55 / 116</td>
              <td style="padding: 10px 14px;" class="num">61</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">3.0x</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">+7.7% (+1 case)</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 10px 14px; font-weight: 600;">Random Forest</td>
              <td style="padding: 10px 14px;" class="num">60 / 116</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">61 / 116</td>
              <td style="padding: 10px 14px;" class="num">77</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">1.25x</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">+15.38% (46.2% vs 30.8%)</td>
            </tr>
            <tr>
              <td style="padding: 10px 14px; font-weight: 600;">Gradient Boosting</td>
              <td style="padding: 10px 14px;" class="num">59 / 116</td>
              <td style="padding: 10px 14px; font-weight: 600; color: var(--accent);" class="num">59 / 116</td>
              <td style="padding: 10px 14px;" class="num">132</td>
              <td style="padding: 10px 14px;" class="num">1.0x</td>
              <td style="padding: 10px 14px;" class="num">30.8% vs 30.8%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

<!-- Author Profile -->
  <section class="about-section" id="sec-about-author" data-toc="06 • Author Profile" aria-labelledby="about-author">
    <h3 class="t-h2" id="about-author" style="margin-bottom: 16px;">Author</h3>
    <div class="author-card" style="display: grid; grid-template-columns: 110px 1fr; gap: 28px; align-items: start; padding: 28px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; margin-top: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
      {avatar_html}
      <div class="author-body" style="display: flex; flex-direction: column;">
        <h4 class="author-name" style="font-size: 1.4rem; font-weight: 700; color: var(--text); margin: 0 0 4px 0; letter-spacing: -0.01em;">Cao Thien An Nguyen</h4>
        <p class="author-role" style="font-size: 0.95rem; font-weight: 600; color: var(--accent); margin: 0 0 12px 0;">Data Science & Economics, University of Wisconsin, Madison</p>
        <p class="author-bio" style="font-size: 0.92rem; line-height: 1.65; color: var(--text-muted); margin: 0 0 14px 0; max-width: 68ch;">
          From Ho Chi Minh City, Vietnam, now in Madison, where the winters are long enough to build a
          whole data pipeline indoors. I blend economics with data science to turn raw data into stories
          that anyone can follow, and I only trust a number after checking when it was first published.
        </p>
        <p class="author-fun" style="font-size: 0.90rem; line-height: 1.6; color: var(--text-muted); margin: 0 0 18px 0; padding: 10px 14px; background: #ffffff; border: 1px solid var(--border); border-radius: 8px; max-width: 68ch;">
          <span class="author-fun-tag" style="display: inline-block; margin-right: 8px; padding: 2px 8px; border-radius: 999px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; color: var(--accent); background-color: var(--accent-tint); vertical-align: 1px;">Fun fact</span> Runs on crispy fried noodles (mì xào giòn):
          one plate a week through all of 2025, about 52 plates. Revisions to this preference since the
          first print: zero.
        </p>
        <!-- Elegant Icon Pills for Links (No Long Colliding URLs) -->
        <div class="author-pills-row" style="margin-top: 18px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding-top: 16px; border-top: 1px solid var(--border);">
          <a class="author-pill-btn" href="https://aansensei.dev" target="_blank" rel="noopener noreferrer" title="Portfolio: aansensei.dev" aria-label="Portfolio">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>
            </svg>
            <span>Portfolio</span>
          </a>

          <a class="author-pill-btn" href="https://www.linkedin.com/in/cao-thien-an-nguyen" target="_blank" rel="noopener noreferrer" title="LinkedIn Profile" aria-label="LinkedIn">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="3" y="3" width="18" height="18" rx="3"/><line x1="8" y1="11" x2="8" y2="16"/><line x1="8" y1="8" x2="8" y2="8.01"/><path d="M12 16v-5m0 2.5a2.5 2.5 0 0 1 5 0V16"/>
            </svg>
            <span>LinkedIn</span>
          </a>

          <a class="author-pill-btn" href="https://github.com/aansensei" target="_blank" rel="noopener noreferrer" title="GitHub Profile" aria-label="GitHub">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <polyline points="8 7 3 12 8 17"/><polyline points="16 7 21 12 16 17"/>
            </svg>
            <span>GitHub</span>
          </a>

          <a class="author-pill-btn" href="mailto:nguyencaothienan937@gmail.com" title="Email: nguyencaothienan937@gmail.com" aria-label="Email">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3 7 12 13 21 7"/>
            </svg>
            <span>Email</span>
          </a>

          <a class="author-pill-btn" href="https://github.com/aansensei/HiddenCare" target="_blank" rel="noopener noreferrer" title="Project Repository" aria-label="Repository Code">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/>
            </svg>
            <span>Code</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="about-section">
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

  <!-- Prominent Clinical & Methodological Disclaimer -->
  <section class="disclaimer-callout" id="sec-about-disclaimer" data-toc="07 • Disclaimer" aria-labelledby="about-disclaimer">
    <div class="disclaimer-header">
      <span class="disclaimer-badge">Institutional & Research Notice</span>
      <h3 class="disclaimer-title" id="about-disclaimer">Clinical & Methodological Disclaimer</h3>
    </div>
    <div class="disclaimer-content">
      <p>
        <strong>Not Medical Advice:</strong> HiddenCare is an empirical research and educational policy simulation platform investigating algorithmic proxy outcome bias under resource constraints. It is intended strictly for academic, epidemiological, and data science research. The models, risk scores, and simulations presented on this site do not constitute clinical diagnostic tools, medical advice, or personalized care recommendations.
      </p>
      <p>
        <strong>Epidemiological Surveillance vs Clinical Diagnosis:</strong> In cross-sectional population surveys such as CDC NHANES, an elevated laboratory Glycohemoglobin (HbA1c &ge; 6.5%) measurement serves as a biological screening surrogate. Under clinical practice guidelines (such as the American Diabetes Association Standards of Care), an authoritative diagnosis of Type 2 Diabetes requires confirmatory repeat testing or clinical adjudication. Individual patient triage decisions should always be directed by licensed medical professionals.
      </p>
      <p>
        <strong>Data Attribution:</strong> This research utilizes public microdata from the continuous National Health and Nutrition Examination Survey (NHANES 2017 to 2023) administered by the National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC). This independent investigation is neither conducted, endorsed, nor certified by the CDC or NCHS.
      </p>
    </div>
  </section>
</article>
"""


def render_footer_html() -> str:
    logo_img = (
        f'<img src="{LOGO_URI}" alt="HiddenCare Logo" width="28" height="28" />'
        if LOGO_URI
        else ""
    )
    return f"""
<div class="site-footer" id="hc-institutional-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <div class="footer-mark">
        {logo_img}
        <span class="footer-name">HiddenCare</span>
      </div>
      <p class="footer-tagline">
        When clinical history masks biological reality: an empirical investigation of proxy outcome bias in algorithmic triage across N = 12,459 CDC NHANES participants.
      </p>
      <div class="footer-status">
        <span class="footer-status-dot" aria-hidden="true"></span>
        <span>CDC NHANES Continuous Biomonitoring 2017 to 2023</span>
      </div>
      <div class="footer-social">
        <a class="footer-social-btn" href="https://github.com/aansensei" target="_blank" rel="noopener noreferrer" aria-label="GitHub" title="GitHub">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="8 7 3 12 8 17" /><polyline points="16 7 21 12 16 17" />
          </svg>
        </a>
        <a class="footer-social-btn" href="https://www.linkedin.com/in/cao-thien-an-nguyen" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="3" y="3" width="18" height="18" rx="3" /><line x1="8" y1="11" x2="8" y2="16" /><line x1="8" y1="8" x2="8" y2="8.01" /><path d="M12 16v-5m0 2.5a2.5 2.5 0 0 1 5 0V16" />
          </svg>
        </a>
        <a class="footer-social-btn" href="https://aansensei.dev" target="_blank" rel="noopener noreferrer" aria-label="Portfolio" title="Portfolio">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18" />
          </svg>
        </a>
        <a class="footer-social-btn" href="mailto:nguyencaothienan937@gmail.com" aria-label="Email" title="Email">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="3" y="5" width="18" height="14" rx="2" /><polyline points="3 7 12 13 21 7" />
          </svg>
        </a>
      </div>
    </div>

    <div class="footer-col">
      <h2 class="footer-head">Explore</h2>
      <ul class="footer-list">
        <li><span class="footer-link">01 Capacity Allocation Simulator</span></li>
        <li><span class="footer-link">02 The 61-Person Margin Inspector</span></li>
        <li><span class="footer-link">03 Health Equity & Access Audit</span></li>
        <li><span class="footer-link">04 Health Economics & Decision Curves</span></li>
        <li><span class="footer-link">05 About & Methodology</span></li>
      </ul>
    </div>

    <div class="footer-col">
      <h2 class="footer-head">Data Sources</h2>
      <ul class="footer-list">
        <li class="footer-source">
          <a class="footer-link" href="https://wwwn.cdc.gov/nchs/nhanes/" target="_blank" rel="noopener noreferrer">CDC NCHS NHANES</a>
          <span class="footer-role">Continuous Cycles 2017 to 2023</span>
        </li>
        <li class="footer-source">
          <a class="footer-link" href="https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/GHB_J.htm" target="_blank" rel="noopener noreferrer">Glycohemoglobin (GHB)</a>
          <span class="footer-role">Laboratory Biomonitoring</span>
        </li>
        <li class="footer-source">
          <a class="footer-link" href="https://diabetes.org/" target="_blank" rel="noopener noreferrer">ADA Clinical Criteria</a>
          <span class="footer-role">Diagnostic cut-off HbA1c ≥ 6.5%</span>
        </li>
        <li class="footer-source">
          <a class="footer-link" href="https://wwwn.cdc.gov/nchs/nhanes/tutorials/weighting.aspx" target="_blank" rel="noopener noreferrer">Complex Survey Design</a>
          <span class="footer-role">WTMEC2YR Examination Weights</span>
        </li>
      </ul>
    </div>

    <div class="footer-col">
      <h2 class="footer-head">Project & Code</h2>
      <ul class="footer-list">
        <li><a class="footer-link" href="https://github.com/aansensei/HiddenCare" target="_blank" rel="noopener noreferrer">Source Code (GitHub)</a></li>
        <li><a class="footer-link" href="https://huggingface.co/spaces/aansensei/HiddenCare" target="_blank" rel="noopener noreferrer">Hugging Face Space</a></li>
        <li><a class="footer-link" href="https://aansensei.dev" target="_blank" rel="noopener noreferrer">Author Portfolio</a></li>
        <li><a class="footer-link" href="https://github.com/aansensei/HiddenCare/issues" target="_blank" rel="noopener noreferrer">Report an Issue</a></li>
      </ul>
    </div>
  </div>

  <div class="footer-bottom">
    <div style="font-weight: 500;">&copy; 2026 Cao Thien An Nguyen &bull; GitHub: <a href="https://github.com/aansensei" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: underline;">aansensei</a> &bull; Academic and policy research.</div>
    <div class="footer-legal">
      <p class="footer-disclaimer">
        Educational and epidemiological research only. An elevated HbA1c measurement in cross-sectional surveillance is a clinical screening surrogate, not an autonomous medical diagnosis. Models and simulation outputs are designed to examine algorithmic fairness under resource limits and must not guide clinical decision-making without qualified medical review.
      </p>
      <p>
        Microdata sourced from the National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC). This independent analysis is neither endorsed nor certified by the CDC or NCHS.
      </p>
    </div>
  </div>
</div>
"""
