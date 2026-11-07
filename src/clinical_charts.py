# Interactive Plotly chart generation routines adhering to Clinical Light theme.

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from src.simulation_engine import LOOKUP_DF, HOLDOUT_DF, SWAP_DF, compute_decision_curve

CLINICAL_PLOTLY_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(family="Inter, sans-serif", color="#0f172a", size=12),
    title_font=dict(family="Source Serif 4, serif", color="#0f172a", size=15),
    margin=dict(l=54, r=28, t=50, b=46),
    xaxis=dict(
        gridcolor="#f1f5f9",
        linecolor="#cbd5e1",
        zerolinecolor="#e2e8f0",
        tickfont=dict(family="JetBrains Mono, monospace", size=11, color="#475569"),
    ),
    yaxis=dict(
        gridcolor="#f1f5f9",
        linecolor="#cbd5e1",
        zerolinecolor="#e2e8f0",
        tickfont=dict(family="JetBrains Mono, monospace", size=11, color="#475569"),
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(255,255,255,0.92)",
        bordercolor="#e2e8f0",
        borderwidth=1,
    ),
)


# Build cumulative case capture (gain) chart across screening capacities.
def build_capacity_gain_chart(selected_capacity_pct: int = 20) -> go.Figure:
    df_sub = LOOKUP_DF[(LOOKUP_DF["capacity_pct"] >= 5) & (LOOKUP_DF["capacity_pct"] <= 50)].copy()

    fig = go.Figure()

    # Random baseline
    fig.add_trace(
        go.Scatter(
            x=df_sub["capacity_pct"],
            y=df_sub["found_rand"],
            mode="lines",
            name="Random Baseline",
            line=dict(color="#94a3b8", dash="dash", width=1.8),
        )
    )

    # Model A
    fig.add_trace(
        go.Scatter(
            x=df_sub["capacity_pct"],
            y=df_sub["found_a"],
            mode="lines+markers",
            name="Model A (Diagnosis Only)",
            line=dict(color="#64748b", width=2.2),
            marker=dict(size=4),
        )
    )

    # Model B
    fig.add_trace(
        go.Scatter(
            x=df_sub["capacity_pct"],
            y=df_sub["found_b"],
            mode="lines+markers",
            name="Model B (Combined Biomarker)",
            line=dict(color="#0284c7", width=2.4),
            marker=dict(size=4),
        )
    )

    # Selected capacity indicator line
    fig.add_vline(
        x=selected_capacity_pct,
        line_width=1.5,
        line_dash="dot",
        line_color="#0369a1",
        annotation_text=f"Selected Budget: {selected_capacity_pct}%",
        annotation_position="top left",
    )

    fig.update_layout(**CLINICAL_PLOTLY_LAYOUT)
    fig.update_layout(
        title="Screening Capacity vs Potential Cases Detected (Holdout N = 4,698)",
        xaxis_title="Screening Capacity (% of Undiagnosed Population)",
        yaxis_title="Potential Undiagnosed Cases Detected (HbA1c >= 6.5%)",
        height=380,
    )
    return fig


# Build Number Needed to Screen (NNS) chart across budget capacities.
def build_nns_chart(selected_capacity_pct: int = 20) -> go.Figure:
    df_sub = LOOKUP_DF[(LOOKUP_DF["capacity_pct"] >= 5) & (LOOKUP_DF["capacity_pct"] <= 50)].copy()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_sub["capacity_pct"],
            y=df_sub["nns_rand"],
            mode="lines",
            name="Random Baseline (NNS = 40.5)",
            line=dict(color="#94a3b8", dash="dash", width=1.8),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_sub["capacity_pct"],
            y=df_sub["nns_a"],
            mode="lines",
            name="Model A (Diagnosis Only)",
            line=dict(color="#64748b", width=2.2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_sub["capacity_pct"],
            y=df_sub["nns_b"],
            mode="lines",
            name="Model B (Combined Biomarker)",
            line=dict(color="#0284c7", width=2.4),
        )
    )

    fig.add_vline(
        x=selected_capacity_pct,
        line_width=1.5,
        line_dash="dot",
        line_color="#0369a1",
        annotation_text=f"Current: {selected_capacity_pct}%",
        annotation_position="bottom right",
    )

    fig.update_layout(**CLINICAL_PLOTLY_LAYOUT)
    fig.update_layout(
        title="Number Needed to Screen (NNS) per Case Detected",
        xaxis_title="Screening Capacity (% of Population)",
        yaxis_title="Lab Tests Required per Case Found (Lower is Better)",
        height=380,
    )
    return fig


# Build 61-person margin swap bar comparison chart.
def build_margin_swap_comparison_chart() -> go.Figure:
    categories = [
        "Model A Exclusive<br>(n = 61 dropped by B)",
        "Uninformed Random<br>Baseline (N = 4,698)",
        "Model B Exclusive<br>(n = 61 rescued by B)",
        "Consensus Core<br>(n = 878 shared)",
    ]
    hit_rates = [1.64, 2.47, 4.92, 5.92]
    case_labels = [
        "1 / 61 cases (1.64%)<br>Below random chance!",
        "2.47% base prevalence",
        "3 / 61 cases (4.92%)<br>3.0x Model A yield",
        "52 / 878 cases (5.92%)",
    ]
    colors = ["#94a3b8", "#cbd5e1", "#0284c7", "#0369a1"]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=hit_rates,
                text=case_labels,
                textposition="outside",
                marker=dict(color=colors, line=dict(width=1, color="rgba(15, 23, 42, 0.15)")),
                width=0.52,
            )
        ]
    )

    fig.update_layout(**CLINICAL_PLOTLY_LAYOUT)
    fig.update_layout(
        title="The 61-Person Boundary Swap: Positive Predictive Value (PPV) by Queue Segment",
        yaxis_title="Positive Predictive Value / Hit Rate (%)",
        yaxis_range=[0, 7.5],
        height=390,
    )
    fig.add_hline(
        y=2.47,
        line_dash="dot",
        line_color="#64748b",
        annotation_text="Holdout Base Prevalence (2.47%)",
        annotation_position="top left",
    )
    return fig


# Build quadrant scatter plot of joint priority ranking.
def build_joint_ranking_scatter() -> go.Figure:
    fig = go.Figure()

    # Shared consensus (both <= 939)
    mask_both = (HOLDOUT_DF["rank_dx"] <= 939) & (HOLDOUT_DF["rank_full"] <= 939)
    both_df = HOLDOUT_DF[mask_both]
    fig.add_trace(
        go.Scatter(
            x=both_df["rank_full"],
            y=both_df["rank_dx"],
            mode="markers",
            name="Consensus Core (n = 878)",
            marker=dict(size=4, color="#cbd5e1", opacity=0.7),
        )
    )

    # Model A only
    mask_only_a = (HOLDOUT_DF["rank_dx"] <= 939) & (HOLDOUT_DF["rank_full"] > 939)
    only_a_df = HOLDOUT_DF[mask_only_a]
    fig.add_trace(
        go.Scatter(
            x=only_a_df["rank_full"],
            y=only_a_df["rank_dx"],
            mode="markers",
            name="Model A Exclusive (n = 61)",
            marker=dict(size=6, color="#94a3b8", symbol="diamond"),
        )
    )

    # Model B only
    mask_only_b = (HOLDOUT_DF["rank_full"] <= 939) & (HOLDOUT_DF["rank_dx"] > 939)
    only_b_df = HOLDOUT_DF[mask_only_b]
    fig.add_trace(
        go.Scatter(
            x=only_b_df["rank_full"],
            y=only_b_df["rank_dx"],
            mode="markers",
            name="Model B Exclusive (n = 61)",
            marker=dict(size=6, color="#0284c7", symbol="circle"),
        )
    )

    # 3 Rescued True Positives
    rescued_true = only_b_df[only_b_df["potential_case"] == 1]
    fig.add_trace(
        go.Scatter(
            x=rescued_true["rank_full"],
            y=rescued_true["rank_dx"],
            mode="markers+text",
            name="3 Rescued Cases (HbA1c >= 6.5%)",
            marker=dict(size=12, color="#0369a1", symbol="star", line=dict(color="#0f172a", width=1.5)),
            text=["Rescued Case", "Rescued Case", "Rescued Case"],
            textposition="top center",
            textfont=dict(family="JetBrains Mono", size=10, color="#0369a1"),
        )
    )

    fig.add_vline(x=939, line_width=1.5, line_dash="dash", line_color="#0f172a")
    fig.add_hline(y=939, line_width=1.5, line_dash="dash", line_color="#0f172a")

    fig.update_layout(**CLINICAL_PLOTLY_LAYOUT)
    fig.update_layout(
        title="Joint Priority Ranking (K = 939 Threshold)",
        xaxis_title="Model B Priority Rank (1 to 4,698)",
        yaxis_title="Model A Priority Rank (1 to 4,698)",
        height=430,
    )
    return fig


# Build health equity sensitivity gap chart by insurance status.
def build_equity_bar_chart() -> go.Figure:
    groups = ["Insured (N = 4,268; 102 cases)", "Uninsured (N = 422; 13 cases)"]
    sens_a = [50.0, 15.4]
    sens_b = [51.0, 23.1]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=groups,
            x=sens_a,
            name="Model A (Diagnosis Only)",
            orientation="h",
            marker=dict(color="#64748b"),
            text=["50.0% (51 cases)", "15.4% (2 cases)"],
            textposition="inside",
        )
    )
    fig.add_trace(
        go.Bar(
            y=groups,
            x=sens_b,
            name="Model B (Combined Biomarker)",
            orientation="h",
            marker=dict(color="#0284c7"),
            text=["51.0% (52 cases)", "23.1% (3 cases, +1 rescued)"],
            textposition="inside",
        )
    )

    fig.update_layout(**CLINICAL_PLOTLY_LAYOUT)
    fig.update_layout(
        title="Disparity Audit: Screening Sensitivity by Health Insurance Coverage",
        xaxis_title="Sensitivity (% of Latent Cases Detected at 20% Budget)",
        xaxis_range=[0, 70],
        barmode="group",
        height=320,
    )
    return fig


# Build Decision Curve Analysis (DCA) Net Benefit chart.
def build_decision_curve_plot() -> go.Figure:
    dca = compute_decision_curve()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dca["thresholds"] * 100,
            y=dca["net_benefit_none"],
            mode="lines",
            name="Treat None (Net Benefit = 0)",
            line=dict(color="#cbd5e1", dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dca["thresholds"] * 100,
            y=dca["net_benefit_all"],
            mode="lines",
            name="Treat All",
            line=dict(color="#94a3b8", width=1.5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dca["thresholds"] * 100,
            y=dca["net_benefit_a"],
            mode="lines",
            name="Model A (Diagnosis Only)",
            line=dict(color="#64748b", width=2.2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dca["thresholds"] * 100,
            y=dca["net_benefit_b"],
            mode="lines",
            name="Model B (Combined Biomarker)",
            line=dict(color="#0284c7", width=2.4),
        )
    )

    fig.update_layout(**CLINICAL_PLOTLY_LAYOUT)
    fig.update_layout(
        title="Decision Curve Analysis (Net Monetary Benefit vs Risk Threshold)",
        xaxis_title="Risk Threshold Probability pt (%)",
        yaxis_title="Net Benefit (Standardized Units)",
        yaxis_range=[-0.005, 0.025],
        height=380,
    )
    return fig
