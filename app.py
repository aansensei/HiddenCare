# Main interactive web application entrypoint for Hugging Face Spaces.
# Styled according to the Macro Event Lab design system and anti-slop guidelines.

from pathlib import Path
import os
import json
import gradio as gr
import pandas as pd

from src.clinical_charts import (
    build_capacity_gain_chart,
    build_nns_chart,
    build_margin_swap_comparison_chart,
    build_joint_ranking_scatter,
    build_equity_bar_chart,
    build_decision_curve_plot,
)
from src.html_components import (
    render_masthead_html,
    render_site_guide_html,
    render_hero_summary_cards,
    render_simulator_kpi_cards,
    render_margin_table_html,
    render_equity_callout_html,
    render_economic_ledger_html,
    render_about_page_html,
)

PROJECT_ROOT = Path(__file__).resolve().parent
CSS_PATH = PROJECT_ROOT / "assets" / "clinical_theme.css"
CLINICAL_CSS = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.exists() else ""
FAVICON_PATH = PROJECT_ROOT / "assets" / "favicon.ico"

# JavaScript to enforce light theme and eliminate dark mode classes.
FORCE_LIGHT_JS = """
function() {
    if (typeof document !== 'undefined') {
        document.body.classList.remove('dark');
        if (document.documentElement) document.documentElement.classList.remove('dark');
        const container = document.querySelector('.gradio-container');
        if (container) container.classList.remove('dark');
    }
}
"""

clinical_theme = gr.themes.Base(
    primary_hue=gr.themes.colors.sky,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
).set(
    body_background_fill="#ffffff",
    block_background_fill="#ffffff",
    block_border_color="#dbe7ef",
    body_text_color="#062033",
)

# Load data dictionary for methodology tab.
DICT_PATH = PROJECT_ROOT / "data" / "nhanes_dictionary.json"
dict_records = []
if DICT_PATH.exists():
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        dict_records = json.load(f)
dict_df = pd.DataFrame(dict_records)


def on_capacity_change(capacity_pct, cost_test, benefit_early):
    kpi_html = render_simulator_kpi_cards(int(capacity_pct))
    plot_gain = build_capacity_gain_chart(int(capacity_pct))
    plot_nns = build_nns_chart(int(capacity_pct))
    econ_html = render_economic_ledger_html(
        int(capacity_pct), float(cost_test), float(benefit_early)
    )
    return kpi_html, plot_gain, plot_nns, econ_html


def on_margin_filter_change(filter_selection):
    return render_margin_table_html(filter_selection)


def on_economic_param_change(capacity_pct, cost_test, benefit_early):
    return render_economic_ledger_html(
        int(capacity_pct), float(cost_test), float(benefit_early)
    )


# Build the Gradio Application Blocks Layout
with gr.Blocks(
    theme=clinical_theme,
    css=CLINICAL_CSS,
    js=FORCE_LIGHT_JS,
    title="HiddenCare | Algorithmic Epidemiology & Diabetes Screening Lab",
) as demo:

    # Header with AanSensei logo, title, and lead (no cheesy quote)
    gr.HTML(render_masthead_html())

    # Analytical Tabs matching Macro Event Lab
    with gr.Tabs():

        # Tab 1: Overview & Capacity Simulator
        with gr.TabItem("Overview & Simulator"):
            gr.HTML(render_site_guide_html())
            gr.HTML(render_hero_summary_cards())

            with gr.Row():
                with gr.Column(scale=8):
                    capacity_slider = gr.Slider(
                        minimum=5,
                        maximum=50,
                        value=20,
                        step=1,
                        label="Screening Budget Capacity (% of Undiagnosed Holdout Cohort, N = 4,698)",
                    )
                with gr.Column(scale=4):
                    gr.Markdown("**Quick Budget Presets:**")
                    with gr.Row():
                        btn_10 = gr.Button("10% Budget", size="sm", elem_classes=["preset-btn"])
                        btn_20 = gr.Button("20% (Primary)", variant="primary", size="sm", elem_classes=["preset-btn", "preset-btn--primary"])
                        btn_30 = gr.Button("30% Budget", size="sm", elem_classes=["preset-btn"])

            sim_kpi_html = gr.HTML(value=render_simulator_kpi_cards(20))

            with gr.Row():
                with gr.Column(scale=6):
                    plot_gain = gr.Plot(value=build_capacity_gain_chart(20))
                with gr.Column(scale=6):
                    plot_nns = gr.Plot(value=build_nns_chart(20))

        # Tab 2: The 61-Person Margin Inspector
        with gr.TabItem("The 61-Person Margin"):
            with gr.Row():
                with gr.Column(scale=6):
                    plot_swap_bar = gr.Plot(value=build_margin_swap_comparison_chart())
                with gr.Column(scale=6):
                    plot_scatter = gr.Plot(value=build_joint_ranking_scatter())

            with gr.Row():
                margin_filter = gr.Radio(
                    choices=[
                        "3 True Positive Cases Rescued by Label B",
                        "All 61 Model B Exclusive (Rescued Queue)",
                        "61 Model A Exclusive (Dropped by Label B)",
                    ],
                    value="3 True Positive Cases Rescued by Label B",
                    label="Inspect Marginal Patient Clinical Profiles (At K = 939 Boundary Cutoff)",
                )

            margin_table_display = gr.HTML(
                value=render_margin_table_html("3 True Positive Cases Rescued by Label B")
            )

        # Tab 3: Health Equity Audit
        with gr.TabItem("Equity & Access Audit"):
            gr.HTML(render_equity_callout_html())
            with gr.Row():
                plot_equity = gr.Plot(value=build_equity_bar_chart())

        # Tab 4: Health Economics & Decision Curves
        with gr.TabItem("Health Economics & DCA"):
            with gr.Row():
                with gr.Column(scale=6):
                    cost_input = gr.Number(
                        value=25.0, label="Point-of-Care HbA1c Test Cost ($ USD)"
                    )
                with gr.Column(scale=6):
                    benefit_input = gr.Number(
                        value=8500.0,
                        label="Present Value of Early Intervention / Avoided Complication ($ USD)",
                    )

            with gr.Row():
                with gr.Column(scale=6):
                    plot_dca = gr.Plot(value=build_decision_curve_plot())
                with gr.Column(scale=6):
                    econ_summary_display = gr.HTML(
                        value=render_economic_ledger_html(20, 25.0, 8500.0)
                    )

        # Tab 5: About & How It Is Built (Full Macro Event Lab Style)
        with gr.TabItem("About & Methodology"):
            gr.HTML(render_about_page_html())
            if not dict_df.empty:
                gr.Markdown("### Interactive CDC NHANES Variable Codebook")
                gr.DataFrame(
                    value=dict_df[
                        [
                            "original_name",
                            "variable_name",
                            "release",
                            "file_source",
                            "unit",
                            "role",
                            "description",
                        ]
                    ],
                    headers=[
                        "Original Code",
                        "Clean Variable",
                        "Cycle",
                        "File Source",
                        "Unit",
                        "Analytical Role",
                        "Description",
                    ],
                    datatype=["str", "str", "str", "str", "str", "str", "str"],
                    interactive=False,
                    wrap=True,
                )

    # Event Listeners
    capacity_slider.change(
        fn=on_capacity_change,
        inputs=[capacity_slider, cost_input, benefit_input],
        outputs=[sim_kpi_html, plot_gain, plot_nns, econ_summary_display],
    )

    btn_10.click(fn=lambda: 10, outputs=capacity_slider)
    btn_20.click(fn=lambda: 20, outputs=capacity_slider)
    btn_30.click(fn=lambda: 30, outputs=capacity_slider)

    margin_filter.change(
        fn=on_margin_filter_change,
        inputs=[margin_filter],
        outputs=[margin_table_display],
    )

    cost_input.change(
        fn=on_economic_param_change,
        inputs=[capacity_slider, cost_input, benefit_input],
        outputs=[econ_summary_display],
    )

    benefit_input.change(
        fn=on_economic_param_change,
        inputs=[capacity_slider, cost_input, benefit_input],
        outputs=[econ_summary_display],
    )


if __name__ == "__main__":
    in_space = bool(os.environ.get("SPACE_ID"))
    server_port = 7860 if in_space else int(os.environ.get("PORT", 3000))
    server_name = "0.0.0.0" if in_space else "127.0.0.1"

    fav = str(FAVICON_PATH) if FAVICON_PATH.exists() else None

    demo.queue().launch(
        server_name=server_name,
        server_port=server_port,
        favicon_path=fav,
        ssr=False,
    )
