# Web Application Layer (`src/`)

This directory contains the interactive web application, simulation engine, and visual layout components powering the HiddenCare research platform. It connects the underlying analytical models with the user interface deployed on Hugging Face Spaces and embedded on the portfolio site.

## Architecture Overview

* **Separation of Concerns:** Heavy model training and cohort derivations are precomputed; this web layer focuses entirely on responsive, real-time user interaction.
* **Low Latency Simulation:** The simulation engine evaluates user-selected clinic screening budgets (5% to 50%) in milliseconds using sorted index lookups rather than re-running heavy models on the fly.
* **Responsive Visualizations:** Charting functions dynamically adapt to mobile phones, tablets, and widescreen desktop displays.

## File Summary

| File | Primary Responsibility | Role in HiddenCare |
| :--- | :--- | :--- |
| `simulation_engine.py` | Real-time policy triage and economic calculations | Evaluates cases detected, sensitivity, NNS, and Net Monetary Benefit as users adjust sliders |
| `clinical_charts.py` | Interactive Plotly visualization builders | Renders capacity trade-offs, margin swaps, equity divides, and decision curves |
| `html_components.py` | Editorial UI layout and responsive components | Renders the recruiter introduction, executive summaries, poster modal, and research codebook |

## Detailed File Guide

### `simulation_engine.py` (Real-Time Screening Engine)
* **What it does:** Calculates clinical and economic outcomes instantaneously whenever a user changes screening capacity or financial parameters.
* **Key functions:**
  * `simulate_screening(pct_budget)`: Determines how many undiagnosed individuals receive a test at a given clinic capacity, computing true positive cases, sensitivity, and Number Needed to Screen (NNS) for both Model A and Model B.
  * `compute_net_monetary_benefit(pct_budget, cost_test, benefit_early)`: Applies standard health economic decision formulas (`Net Benefit = (Cases Found * Early Intervention Benefit) minus Total Testing Cost`) to compare algorithmic screening against universal testing or no screening.
  * `compute_decision_curve_data()`: Evaluates clinical utility across a continuum of decision threshold probabilities (1% to 15%).
* **Design choice:** Pre-sorting holdout predictions allows the simulator to serve instantaneous updates in the browser without server lag.

### `clinical_charts.py` (Interactive Plotly Visualizations)
* **What it does:** Builds all interactive data visualizations using Plotly, unified around an editorial sapphire blue palette (`#0284c7`) and off-white cards.
* **Visualizations built:**
  * **Capacity Yield & Efficiency Curves:** Demonstrates how case detection and testing efficiency change as screening expands from 5% to 50%.
  * **61-Person Margin Swap:** Highlights the 61 patients who swap triage priority at the 20% budget mark, comparing precision rates between models (4.92% vs 1.64%).
  * **Joint Ranking Scatter Plot:** Compares individual patient priorities assigned by Model A versus Model B.
  * **Health Equity Audit:** Visualizes the sensitivity divide between insured and uninsured Americans.
  * **Decision Curve Analysis (DCA):** Quantifies net clinical benefit across clinical threshold probabilities.
* **Design choice:** Custom responsive styling ensures labels, axes, and tooltips remain fully readable on mobile screens without horizontal truncation.

### `html_components.py` (Editorial UI and Research Documentation)
* **What it does:** Assembles the editorial structure, responsive navigation, and research reference sections.
* **Key sections generated:**
  * **Header & Quick Summary:** A concise 20-second project explanation, "What I Built" technical quadrant, and direct action buttons.
  * **Executive Study Abstract:** A clean 3-column layout outlining the structural bias, the 61-patient proof, and health equity dividends.
  * **Academic Poster Viewer:** Embedded research poster with a direct 1-click vector PDF download button.
  * **Statistical Evidence Tables:** Formatted tables displaying CDC Taylor Series 95% Confidence Intervals and Multi-Architecture Robustness comparisons.
  * **Variable Codebook & Methodology:** Detailed CDC NHANES variable dictionary and author profile.
* **Design choice:** Enforces strict typography discipline (Newsreader serif for titles, Inter for body text) and touch targets of at least 44x44 CSS pixels for mobile usability.
