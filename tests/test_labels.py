# Unit tests for Label A and Label B definitions on synthetic test data.

import pandas as pd
import pytest
from hiddencare.cohort import build_cohort


def test_label_definitions_on_synthetic_data():
    # Construct synthetic participants covering all diagnostic combinations.
    synthetic_df = pd.DataFrame(
        {
            "seqn": [101, 102, 103, 104, 105],
            "age": [45, 50, 35, 60, 55],
            "sex": [1, 2, 1, 2, 1],
            "dx": [1, 1, 2, 2, 2],
            "a1c": [5.5, 8.2, 5.2, 6.5, 7.8],
            "weight": [1000.0, 1500.0, 2000.0, 1200.0, 1800.0],
            "prg": [None, 2.0, None, None, None],
            "hiq": [1, 1, 1, 2, 1],
            "pir": [2.5, 3.8, 1.1, 4.2, 1.8],
        }
    )

    cohort = build_cohort(synthetic_df, min_age=20, a1c_threshold=6.5)

    # Participant 101: Prior diagnosis with low HbA1c (treated). Positive under both labels.
    p101 = cohort.loc[cohort["seqn"] == 101].iloc[0]
    assert p101["label_dx"] == 1
    assert p101["label_full"] == 1

    # Participant 102: Prior diagnosis with elevated HbA1c. Positive under both labels.
    p102 = cohort.loc[cohort["seqn"] == 102].iloc[0]
    assert p102["label_dx"] == 1
    assert p102["label_full"] == 1

    # Participant 103: No prior diagnosis and normal HbA1c. Negative under both labels.
    p103 = cohort.loc[cohort["seqn"] == 103].iloc[0]
    assert p103["label_dx"] == 0
    assert p103["label_full"] == 0

    # Participant 104: No prior diagnosis and borderline/cutoff HbA1c exactly 6.5%.
    # Negative under Label A, positive under Label B.
    p104 = cohort.loc[cohort["seqn"] == 104].iloc[0]
    assert p104["label_dx"] == 0
    assert p104["label_full"] == 1

    # Participant 105: No prior diagnosis and high HbA1c 7.8% (hidden case).
    # Negative under Label A, positive under Label B.
    p105 = cohort.loc[cohort["seqn"] == 105].iloc[0]
    assert p105["label_dx"] == 0
    assert p105["label_full"] == 1
