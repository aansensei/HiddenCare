# kiem thu uoc luong phuong sai khao sat phuc hop
import pandas as pd
from hiddencare.survey_stats import compute_survey_ratio_variance, compute_paired_survey_difference


# kiem thu ham tinh ty le va sai so tuyen tinh hoa taylor
def test_compute_survey_ratio_variance():
    df_sample = pd.DataFrame({
        "num": [1, 0, 1, 0, 1, 0],
        "denom": [1, 1, 1, 1, 1, 1],
        "weight": [10.0, 10.0, 20.0, 20.0, 15.0, 15.0],
        "strata": [1, 1, 2, 2, 3, 3],
        "psu": [1, 2, 1, 2, 1, 2],
    })
    res = compute_survey_ratio_variance(df_sample, "num", "denom")
    assert 0.0 <= res["ratio"] <= 1.0
    assert res["se"] >= 0.0
    assert res["ci_lower"] <= res["ratio"] <= res["ci_upper"]
    assert res["df"] == 3


# kiem thu ham tinh sai so phuong sai bat cap cho hieu so hai mo hinh
def test_compute_paired_survey_difference():
    df_sample = pd.DataFrame({
        "sel_a": [1, 0, 1, 0, 1, 0],
        "sel_b": [1, 1, 1, 0, 0, 0],
        "potential_case": [1, 1, 1, 1, 1, 1],
        "weight": [10.0, 10.0, 20.0, 20.0, 15.0, 15.0],
        "strata": [1, 1, 2, 2, 3, 3],
        "psu": [1, 2, 1, 2, 1, 2],
    })
    res = compute_paired_survey_difference(df_sample, "sel_a", "sel_b")
    assert res["se"] >= 0.0
    assert res["ci_lower"] <= res["diff_ratio"] <= res["ci_upper"]
    assert res["df"] == 3

