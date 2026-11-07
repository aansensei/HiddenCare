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
    <span class="hc-meta-tag">Algorithmic Epidemiology Lab</span>
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
<div class="hc-bento-grid">
  <!-- Bento 1: Primary Discovery (Featured Highlight) -->
  <article class="hc-bento-card hc-bento-card--featured">
    <div>
      <span class="hc-section-kicker" style="color: var(--accent);">Primary Discovery • 20% Budget Constraint</span>
      <div class="hc-finding-value num" style="color: var(--accent); margin: 8px 0 4px 0;">61 Patients Swapped</div>
      <p style="margin: 0 0 16px 0; font-size: 0.90rem; color: var(--text-muted); line-height: 1.55;">
        At the 939-slot boundary (K = 20%), Model B rescues <strong>3 true cases</strong> missed by Model A, 
        delivering a <strong>3.0× higher marginal yield (4.92% vs 1.64%)</strong>.
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
      <span class="hc-section-kicker">Evaluation Cohort • Aug 2021–Aug 2023</span>
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
      <span class="hc-section-kicker">Training Benchmark • 2017–Mar 2020</span>
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
      <span class="hc-badge hc-badge--accent-sm">{diff_cases_str} Cases</span>
    </div>
    <div class="hc-kpi-hero num" style="color: var(--accent);">{found_b} <span class="hc-kpi-denom">/ 116 cases</span></div>
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
  <section class="about-section" aria-labelledby="about-author">
    <h3 class="t-h2" id="about-author" style="margin-bottom: 16px;">Author</h3>
    <div class="author-card" style="display: grid; grid-template-columns: 110px 1fr; gap: 28px; align-items: start; padding: 28px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; margin-top: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
      {avatar_html}
      <div class="author-body" style="display: flex; flex-direction: column;">
        <h4 class="author-name" style="font-size: 1.4rem; font-weight: 700; color: var(--text); margin: 0 0 4px 0; letter-spacing: -0.01em;">Cao Thien An Nguyen</h4>
        <p class="author-role" style="font-size: 0.95rem; font-weight: 600; color: var(--accent); margin: 0 0 12px 0;">Data Science & Economics, University of Wisconsin–Madison</p>
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
  <section class="disclaimer-callout" aria-labelledby="about-disclaimer">
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
        <strong>Data Attribution:</strong> This research utilizes public microdata from the continuous National Health and Nutrition Examination Survey (NHANES 2017–2023) administered by the National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC). This independent investigation is neither conducted, endorsed, nor certified by the CDC or NCHS.
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
<footer class="site-footer">
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
        <span>CDC NHANES Continuous Biomonitoring 2017–2023</span>
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
          <span class="footer-role">Continuous Cycles 2017–2023</span>
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
    <div>&copy; 2026 Cao Thien An Nguyen. Academic and policy research.</div>
    <div class="footer-legal">
      <p class="footer-disclaimer">
        Educational and epidemiological research only. An elevated HbA1c measurement in cross-sectional surveillance is a clinical screening surrogate, not an autonomous medical diagnosis. Models and simulation outputs are designed to examine algorithmic fairness under resource limits and must not guide clinical decision-making without qualified medical review.
      </p>
      <p>
        Microdata sourced from the National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC). This independent analysis is neither endorsed nor certified by the CDC or NCHS.
      </p>
    </div>
  </div>
</footer>
"""
