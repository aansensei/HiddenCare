# Unit tests for cohort selection and exclusion criteria on synthetic test data.

import pandas as pd
import pytest
from hiddencare.cohort import build_cohort


def test_exclusion_criteria_on_synthetic_data():
    # Construct synthetic dataset with intentional violations of eligibility rules.
    synthetic_df = pd.DataFrame(
        {
            "seqn": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            # 1: Underage (<20) -> exclude
            # 2: Borderline diagnosis (dx=3) -> exclude
            # 3: Refused diagnosis (dx=7) -> exclude
            # 4: Don't know diagnosis (dx=9) -> exclude
            # 5: Missing HbA1c -> exclude
            # 6: Zero weight -> exclude
            # 7: Pregnant female (prg=1) -> exclude
            # 8: Non-pregnant tested female (prg=2) -> include
            # 9: Male with prg=NaN (not tested) -> include
            # 10: Older female with prg=NaN (not tested) -> include
            "age": [18, 45, 50, 55, 40, 35, 28, 30, 42, 68],
            "sex": [1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
            "dx": [2, 3, 7, 9, 2, 2, 2, 2, 2, 1],
            "a1c": [5.4, 6.2, 5.8, 6.0, None, 5.5, 5.3, 5.4, 5.6, 6.8],
            "weight": [100.0, 100.0, 100.0, 100.0, 100.0, 0.0, 100.0, 100.0, 100.0, 100.0],
            "prg": [None, None, None, None, None, None, 1.0, 2.0, None, None],
            "hiq": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "pir": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
        }
    )

    cohort = build_cohort(synthetic_df, min_age=20, a1c_threshold=6.5)

    retained_seqns = set(cohort["seqn"])
    expected_retained = {8, 9, 10}

    assert retained_seqns == expected_retained, (
        f"Expected retained SEQN {expected_retained}, but got {retained_seqns}"
    )


def test_no_male_or_untested_female_exclusion():
    # Explicitly test that participants not eligible for pregnancy test are retained.
    synthetic_df = pd.DataFrame(
        {
            "seqn": [10, 20],
            "age": [50, 70],
            "sex": [1, 2],
            "dx": [2, 2],
            "a1c": [5.5, 5.7],
            "weight": [500.0, 600.0],
            "prg": [None, None],
            "hiq": [1, 1],
            "pir": [3.0, 3.0],
        }
    )

    cohort = build_cohort(synthetic_df, min_age=20, a1c_threshold=6.5)
    assert len(cohort) == 2, "Untested participants (males and older adults) must not be dropped."
