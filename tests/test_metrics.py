# Unit tests for screening allocation, deterministic tie breaking, and metric calculations.

import numpy as np
import pandas as pd
import pytest
from hiddencare.metrics import allocate_screening, compute_screening_metrics
from hiddencare.models import assert_predictor_allowlist


def test_allocation_and_tie_breaking():
    # 5 participants with tied scores for two participants.
    scores = np.array([0.9, 0.7, 0.7, 0.4, 0.1])
    seqns = np.array([200, 300, 100, 400, 500])

    # Allocate top 40% (2 participants out of 5).
    # Highest is seqn 200 (score 0.9).
    # Tied at 0.7: seqn 100 vs seqn 300. Ascending tie breaking must pick 100.
    selected = allocate_screening(scores, seqns, capacity_frac=0.40)

    assert selected.sum() == 2
    assert selected[0] is True or selected[0] == 1  # seqn 200
    assert selected[2] is True or selected[2] == 1  # seqn 100
    assert selected[1] is False or selected[1] == 0  # seqn 300 was not selected due to tie break


def test_screening_metric_calculations():
    # Synthetic ground truth and selection.
    selected = np.array([True, True, True, False, False, False, False, False, False, False])
    true_cases = np.array([1, 1, 0, 1, 0, 0, 0, 0, 0, 0])
    weights = np.ones(10)

    # 10 evaluated, 3 picked, 3 true cases, 2 found, 1 missed.
    metrics = compute_screening_metrics(selected, true_cases, weights=weights)

    assert metrics["n_eval"] == 10
    assert metrics["n_pick"] == 3
    assert metrics["n_case"] == 3
    assert metrics["n_found"] == 2
    assert metrics["n_missed"] == 1
    assert pytest.approx(metrics["sensitivity"]) == 2 / 3
    assert pytest.approx(metrics["ppv"]) == 2 / 3
    assert pytest.approx(metrics["number_needed_to_screen"]) == 3 / 2


def test_forbidden_predictor_assertion():
    # Dataframe containing leaked target variable must raise an error.
    leaked_df = pd.DataFrame(
        {
            "age": [50],
            "sex": [1],
            "bmi": [28.0],
            "waist": [90.0],
            "a1c": [6.8],  # Leakage!
        }
    )

    with pytest.raises(ValueError, match="Target or survey leakage variable found"):
        assert_predictor_allowlist(leaked_df, ["age", "sex", "bmi", "waist"])
