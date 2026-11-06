# Publication style visualization functions using matplotlib.

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Plot screening capacity versus detected potential cases across models.
def plot_capacity_tradeoff(
    metrics_df: pd.DataFrame,
    random_df: pd.DataFrame,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

    # Filter to model performance across capacities.
    dx_rows = metrics_df[metrics_df["model"] == "Diagnosis Only (Label A)"].sort_values("capacity")
    full_rows = metrics_df[metrics_df["model"] == "Combined (Label B)"].sort_values("capacity")

    cap_pct = [c * 100 for c in dx_rows["capacity"]]

    ax.plot(
        cap_pct,
        dx_rows["n_found"],
        marker="o",
        linewidth=2,
        color="#2b5c8f",
        label="Diagnosis Only Model (Label A)",
    )
    ax.plot(
        cap_pct,
        full_rows["n_found"],
        marker="s",
        linewidth=2,
        color="#d95f02",
        label="Combined Model (Label B)",
    )

    if not random_df.empty:
        rand_sorted = random_df.sort_values("capacity")
        ax.plot(
            [c * 100 for c in rand_sorted["capacity"]],
            rand_sorted["expected_found"],
            linestyle="--",
            color="#7570b3",
            label="Random Allocation Baseline",
        )

    ax.set_xlabel("Screening Capacity (% of Evaluation Cohort)", fontsize=11)
    ax.set_ylabel("Potential Undiagnosed Cases Detected (HbA1c >= 6.5%)", fontsize=11)
    ax.set_title("Screening Capacity Tradeoff in Previously Undiagnosed Adults", fontsize=12, pad=12)
    ax.set_xticks(cap_pct)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(frameon=True, loc="upper left")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# Plot agreement and disagreement between paired policies under primary capacity.
def plot_paired_overlap(
    overlap_df: pd.DataFrame,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    labels = overlap_df["policy_group"].tolist()
    counts = overlap_df["n_participants"].tolist()
    cases = overlap_df["n_potential_cases"].tolist()

    x = np.arange(len(labels))
    width = 0.35

    rects1 = ax.bar(x - width / 2, counts, width, label="Total Screened", color="#4575b4")
    rects2 = ax.bar(x + width / 2, cases, width, label="Potential Cases Found", color="#d73027")

    ax.set_ylabel("Number of Participants", fontsize=11)
    ax.set_title("Paired Screening Policy Overlap at Primary 20% Capacity", fontsize=12, pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right", fontsize=9)
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    ax.legend(frameon=True)

    # Annotate bar values.
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(
            f"{int(height)}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(
            f"{int(height)}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# Plot missed potential cases by sociodemographic subgroup.
def plot_subgroup_audit(
    audit_df: pd.DataFrame,
    subgroup_name: str,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sub_data = audit_df[audit_df["subgroup"] == subgroup_name].copy()

    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    cats = sub_data["category"].tolist()
    found = sub_data["n_found"].tolist()
    missed = sub_data["n_missed"].tolist()

    x = np.arange(len(cats))
    width = 0.55

    ax.bar(x, found, width, label="Potential Cases Detected", color="#1b7837")
    ax.bar(x, missed, width, bottom=found, label="Potential Cases Missed", color="#e7298a")

    ax.set_ylabel("Number of Potential Cases", fontsize=11)
    ax.set_title(f"Potential Undiagnosed Cases by {subgroup_name.title()} at 20% Capacity", fontsize=12, pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=10)
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    ax.legend(frameon=True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
