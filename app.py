# Main interactive web application entrypoint for Hugging Face Spaces.

from pathlib import Path
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
    render_hero_summary_cards,
    render_simulator_kpi_cards,
    render_margin_table_html,
    render_equity_callout_html,
    render_economic_ledger_html,
)

PROJECT_ROOT = Path(__file__).resolve().parent
CSS_PATH = PROJECT_ROOT / "assets" / "clinical_theme.css"
CLINICAL_CSS = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.exists() else ""

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
    body_background_fill="#f8fafc",
    block_background_fill="#ffffff",
    block_border_color="#e2e8f0",
    body_text_color="#0f172a",
)

# Load data dictionary for methodology tab.
DICT_PATH = PROJECT_ROOT / "data" / "nhanes_dictionary.json"
dict_records = []
if DICT_PATH.exists():
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        dict_records = json.load(f)
dict_df = pd.DataFrame(dict_records)


def on_capacity_change(capacity_pct: int, cost_test: float, benefit_early: float):
    kpi_html = render_simulator_kpi_cards(capacity_pct)
    gain_fig = build_capacity_gain_chart(capacity_pct)
    nns_fig = build_nns_chart(capacity_pct)
    econ_html = render_economic_ledger_html(capacity_pct, cost_test, benefit_early)
    return kpi_html, gain_fig, nns_fig, econ_html


def on_margin_filter_change(filter_choice: str):
    return render_margin_table_html(filter_choice)


def on_economic_param_change(capacity_pct: int, cost_test: float, benefit_early: float):
    return render_economic_ledger_html(capacity_pct, cost_test, benefit_early)


with gr.Blocks(
    title="HiddenCare | Algorithmic Epidemiology & Diabetes Screening Lab",
) as demo:

    # Editorial Masthead & Summary Cards
    gr.HTML(render_masthead_html())
    gr.HTML(render_hero_summary_cards())

    # Analytical Tabs
    with gr.Tabs():

        # Tab 1: Capacity Simulator
        with gr.TabItem("01. Capacity Allocation Simulator"):
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
                    with gr.Row():
                        btn_10 = gr.Button("Preset: 10% Budget", size="sm")
                        btn_20 = gr.Button("Preset: 20% (Primary)", variant="primary", size="sm")
                        btn_30 = gr.Button("Preset: 30% Budget", size="sm")

            sim_kpi_html = gr.HTML(value=render_simulator_kpi_cards(20))

            with gr.Row():
                with gr.Column(scale=6):
                    plot_gain = gr.Plot(value=build_capacity_gain_chart(20))
                with gr.Column(scale=6):
                    plot_nns = gr.Plot(value=build_nns_chart(20))

        # Tab 2: The 61-Person Margin Inspector
        with gr.TabItem("02. The 61-Person Margin Inspector"):
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
        with gr.TabItem("03. Health Equity & Access Audit"):
            gr.HTML(render_equity_callout_html())
            with gr.Row():
                plot_equity = gr.Plot(value=build_equity_bar_chart())

        # Tab 4: Health Economics & Decision Curves
        with gr.TabItem("04. Health Economics & Decision Curves"):
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

        # Tab 5: Methodology & Dictionary
        with gr.TabItem("05. Methodology & NHANES Dictionary"):
            gr.Markdown(
                """
### Methodological Design & Epidemiological Guardrails

1. **Strict Temporal Split:** The model is trained on pre-pandemic continuous NHANES (2017 to March 2020; N = 7,761) and evaluated once on a locked holdout of previously undiagnosed adults from post-pandemic NHANES (August 2021 to August 2023; N = 4,698).
2. **Zero Target Leakage:** Only non-invasive demographic and anthropometric markers (Age, Sex, BMI, Waist Circumference) enter the feature matrix. Laboratory HbA1c is used strictly as the ground-truth outcome in evaluation.
3. **Screening Allocation vs Clinical Diagnosis:** Models output priority ranking scores to allocate laboratory screening kits; they do not claim to provide definitive clinical diagnoses.

#### Interactive CDC NHANES Variable Codebook
                """
            )
            if not dict_df.empty:
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
                    label="CDC NHANES Variables Used in HiddenCare",
                    interactive=False,
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

    demo.queue().launch(
        server_name=server_name,
        server_port=server_port,
        theme=clinical_theme,
        css=CLINICAL_CSS,
        js=FORCE_LIGHT_JS,
        ssr_mode=False,
    )
