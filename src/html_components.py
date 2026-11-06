# HTML and Jinja-style component renderers for HiddenCare interactive research platform.

from src.simulation_engine import evaluate_budget_capacity, compute_economic_nmb, SWAP_DF
from data.verified_constants import COHORT_METRICS


def render_masthead_html() -> str:
    return """
<div class="hc-masthead">
  <div class="hc-kicker">
    <span>CDC NHANES 2017–2023</span>
    <span>•</span>
    <span>Population Health Sciences</span>
    <span>•</span>
    <span>Weill Cornell Fellowship Portfolio</span>
  </div>
  <h1 class="hc-title">When Clinical History Masks Biological Reality</h1>
  <p class="hc-subtitle">
    How Training Label Definitions Reorder the Undiagnosed Screening Queue in Population Diabetes Detection: 
    An Empirical Investigation of Proxy Outcome Bias across N = 12,459 Adults.
  </p>
  <div class="hc-whisper-quote">
    "Where data whispers untold stories: investigating who gets left behind when healthcare algorithms train on access rather than need."
  </div>
</div>
"""


def render_hero_summary_cards() -> str:
    return """
<div class="hc-grid-3">
  <div class="hc-card hc-card--medical">
    <div class="hc-metric-label">Development Cohort (2017–Mar 2020)</div>
    <div class="hc-metric-value">N = 7,761</div>
    <div class="hc-metric-subtext">
      • Label A (Diagnosis Only): 1,257 cases (16.20%)<br>
      • Label B (Dx OR HbA1c &ge; 6.5%): 1,484 cases (19.12%)<br>
      <span class="hc-badge hc-badge--medical" style="margin-top: 6px;">
        Hidden Need: +227 Unrecognized Cases
      </span>
    </div>
  </div>

  <div class="hc-card hc-card--neutral">
    <div class="hc-metric-label">Undiagnosed Holdout (2021–2023)</div>
    <div class="hc-metric-value">N = 4,698</div>
    <div class="hc-metric-subtext">
      • Strictly previously undiagnosed adults at exam<br>
      • True Latent Cases (HbA1c &ge; 6.5%): <b>116 cases</b><br>
      <span class="hc-badge" style="background: #f1f5f9; color: #334155; margin-top: 6px;">
        Background Prevalence: 2.47%
      </span>
    </div>
  </div>

  <div class="hc-card hc-card--emerald">
    <div class="hc-metric-label">Primary 20% Budget Margin (K = 939)</div>
    <div class="hc-metric-value">61 Swapped</div>
    <div class="hc-metric-subtext">
      • Consensus Core: 878 shared (52 cases, 5.92% yield)<br>
      • Model A Unique: 1 / 61 cases (1.64% hit rate)<br>
      <span class="hc-badge hc-badge--emerald" style="margin-top: 6px;">
        Model B Unique: 3 / 61 cases (4.92% — 3.0x Yield!)
      </span>
    </div>
  </div>
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
<div class="hc-grid-3">
  <div class="hc-card hc-card--neutral">
    <div class="hc-metric-label">Random Allocation Baseline</div>
    <div class="hc-metric-value">{found_rand} <span style="font-size: 1rem; color: #64748b; font-weight: normal;">/ 116 cases</span></div>
    <div class="hc-metric-subtext">
      <b>Sensitivity:</b> {sens_rand}%<br>
      <b>PPV (Yield):</b> {ppv_rand}%<br>
      <b>Number Needed to Screen (NNS):</b> {nns_rand} tests/case<br>
      <b>Allocated Tests:</b> {k_screened:,} / 4,698
    </div>
  </div>

  <div class="hc-card hc-card--medical">
    <div class="hc-metric-label">Model A (Diagnosis Only Proxy)</div>
    <div class="hc-metric-value">{found_a} <span style="font-size: 1rem; color: #64748b; font-weight: normal;">/ 116 cases</span></div>
    <div class="hc-metric-subtext">
      <b>Sensitivity:</b> {sens_a}%<br>
      <b>PPV (Yield):</b> {ppv_a}%<br>
      <b>Number Needed to Screen (NNS):</b> {nns_a} tests/case<br>
      <b>ROC AUC:</b> 0.7300 | <b>PR AUC:</b> 0.0548
    </div>
  </div>

  <div class="hc-card hc-card--emerald">
    <div class="hc-metric-label">Model B (Combined Biomarker Augmented)</div>
    <div class="hc-metric-value" style="color: #059669;">
      {found_b} <span style="font-size: 1rem; color: #059669; font-weight: normal;">/ 116 cases</span>
      <span class="hc-badge hc-badge--emerald" style="font-size: 0.72rem; vertical-align: middle; margin-left: 6px;">{diff_cases_str} Cases</span>
    </div>
    <div class="hc-metric-subtext">
      <b>Sensitivity:</b> {sens_b}% <span class="hc-badge hc-badge--emerald">{diff_sens_str}</span><br>
      <b>PPV (Yield):</b> {ppv_b}%<br>
      <b>Number Needed to Screen (NNS):</b> {nns_b} tests/case<br>
      <b>ROC AUC:</b> 0.7410 | <b>PR AUC:</b> 0.0566
    </div>
  </div>
</div>
"""


def render_margin_table_html(filter_choice: str) -> str:
    df = SWAP_DF.copy()

    if "3 True Positive" in filter_choice:
        df = df[(df["swap_group"].str.contains("Model B Exclusive")) & (df["potential_case"] == 1)]
    elif "All 61 Model B" in filter_choice:
        df = df[df["swap_group"].str.contains("Model B Exclusive")]
    else:
        df = df[df["swap_group"].str.contains("Model A Exclusive")]

    rows_html = []
    for _, row in df.head(15).iterrows():
        is_case = row["potential_case"] == 1
        row_class = "row-rescued" if is_case else ""
        gender = "Male" if row["sex"] == 1.0 else "Female"
        a1c_display = f"<b>{row['a1c']}%</b>" if is_case else f"{row['a1c']}%"
        status_badge = (
            '<span class="hc-badge hc-badge--emerald">Rescued Case (HbA1c &ge; 6.5%)</span>'
            if is_case
            else '<span class="hc-badge" style="background:#f1f5f9; color:#475569;">Normal</span>'
        )

        rows_html.append(f"""
<tr class="{row_class}">
  <td><b>#{int(row['seqn'])}</b></td>
  <td>{int(row['age'])}y / {gender}</td>
  <td>BMI: {row['bmi']:.1f}<br>Waist: {row['waist']:.1f}cm</td>
  <td>Insurance: {row['insured'].title()}<br>PIR: {row['pir_group'].title()}</td>
  <td>Rank A: #{row['rank_dx']}<br>Rank B: #{row['rank_full']}</td>
  <td>{a1c_display}</td>
  <td>{status_badge}</td>
</tr>
""")

    table_body = "".join(rows_html)
    total_count = len(df)
    shown_text = f"Showing top {min(15, total_count)} of {total_count} matching profiles"

    return f"""
<div style="margin-top: 10px;">
  <div style="font-family: var(--font-mono); font-size: 0.75rem; color: #64748b; margin-bottom: 6px;">
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
  <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.8rem; text-transform: uppercase; color: #be123c; margin-bottom: 6px;">
    Structural Access Disparity & Statistical Honesty Callout
  </div>
  <div style="font-size: 0.94rem; line-height: 1.55; color: #0f172a;">
    <p><b>1. The 3x Insurance Sensitivity Divide:</b> At the primary 20% capacity budget, both models successfully detect ~50.0% of latent cases among insured individuals (51/102 cases for Model A, 52/102 for Model B). Conversely, screening sensitivity drops to <b>15.4% (Model A)</b> and <b>23.1% (Model B)</b> among uninsured individuals, leaving over 75% of uninsured cases undetected.</p>
    <p style="margin-top: 8px;"><b>2. Relative Biomarker Recovery:</b> Incorporating the laboratory biomarker (Model B) allocates 6 additional screening slots to uninsured participants and catches <b>+1 additional true case</b> (+50% relative increase in yield), demonstrating that biomarker augmentation partially corrects access bias.</p>
    <p style="margin-top: 8px;"><b>3. Small-Sample Integrity:</b> In the holdout cohort of previously undiagnosed adults, the uninsured subgroup holds N = 422 participants with exactly 13 latent positive cases. In accordance with biostatistical best practices, we report exact participant counts and avoid over-extrapolating small-sample estimates into sweeping algorithmic fairness claims.</p>
  </div>
</div>
"""


def render_economic_ledger_html(
    capacity_pct: int, cost_test: float, benefit_early: float
) -> str:
    econ = compute_economic_nmb(capacity_pct, cost_test, benefit_early)

    return f"""
<div class="hc-card hc-card--medical" style="margin-top: 10px;">
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
        <td>{econ['cost_per_case_rand']:.1f}</td>
        <td>${econ['total_cost']:,.0f}</td>
        <td>${econ['cost_per_case_rand']:,.0f}</td>
        <td>${econ['nmb_rand']:,.0f}</td>
      </tr>
      <tr>
        <td><b>Model A (Diagnosis Only)</b></td>
        <td>{evaluate_budget_capacity(capacity_pct)['found_a']}</td>
        <td>${econ['total_cost']:,.0f}</td>
        <td>${econ['cost_per_case_a']:,.0f}</td>
        <td>${econ['nmb_a']:,.0f}</td>
      </tr>
      <tr class="row-rescued">
        <td><b>Model B (Combined Biomarker)</b></td>
        <td>{evaluate_budget_capacity(capacity_pct)['found_b']}</td>
        <td>${econ['total_cost']:,.0f}</td>
        <td><b>${econ['cost_per_case_b']:,.0f}</b></td>
        <td><b>${econ['nmb_b']:,.0f}</b></td>
      </tr>
    </tbody>
  </table>

  <div class="hc-callout hc-callout--emerald" style="margin: 0; padding: 14px 18px;">
    <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.78rem; text-transform: uppercase; color: #047857; margin-bottom: 4px;">
      Zero Marginal Cost Policy Improvement
    </div>
    <div style="font-size: 0.88rem; color: #0f172a; line-height: 1.5;">
      Because both models use the exact same testing quota ({econ['k_screened']:,} tests; $\Delta\text{{Cost}} = \$0$), shifting from Label A to Label B yields an 
      <b>Incremental Net Benefit of +${econ['incremental_nmb']:,.0f}</b> on this holdout cohort (or <b>+${econ['nmb_gain_10k']:,.0f} per 10,000 undiagnosed adults</b>) by identifying {econ['incremental_cases']} additional cases at zero additional laboratory expenditure.
    </div>
  </div>
</div>
"""
