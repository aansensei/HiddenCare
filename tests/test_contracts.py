# kiem thu hop dong du lieu pandera va cong kiem toan schema drift
import numpy as np
import pandas as pd
import pytest
import pandera.errors
from hiddencare.contracts import CohortSchema, calculate_psi, run_schema_drift_audit


# kiem thu hop dong du lieu voi ban ghi hop le
def test_cohort_schema_valid():
    valid_data = pd.DataFrame({
        "seqn": [10001, 10002],
        "age": [45.0, 60.0],
        "sex": [1, 2],
        "dx": [1, 2],
        "a1c": [5.8, 7.2],
        "weight": [1234.5, 5678.9],
        "bmi": [24.5, 31.2],
        "waist": [85.0, 102.0],
        "pir": [1.5, 3.8],
        "psu": [1, 2],
        "strata": [10, 10],
        "prg": [np.nan, 2.0],
        "label_dx": [1, 0],
        "label_full": [1, 1],
        "insured": ["insured", "uninsured"],
        "pir_group": ["middle", "high"],
    })
    validated = CohortSchema.validate(valid_data)
    assert len(validated) == 2


# kiem thu hop dong du lieu tu choi phu nu mang thai xac nhan
def test_cohort_schema_rejects_pregnancy():
    invalid_data = pd.DataFrame({
        "seqn": [99999],
        "age": [28.0],
        "sex": [2],
        "dx": [2],
        "a1c": [5.4],
        "weight": [1000.0],
        "bmi": [22.0],
        "waist": [75.0],
        "pir": [2.0],
        "psu": [1],
        "strata": [1],
        "prg": [1.0],
        "label_dx": [0],
        "label_full": [0],
        "insured": ["insured"],
        "pir_group": ["middle"],
    })
    with pytest.raises(pandera.errors.SchemaError):
        CohortSchema.validate(invalid_data)


# kiem thu ham tinh chi so on dinh quan the psi
def test_calculate_psi_identical_distributions():
    arr = np.random.normal(50, 10, 1000)
    psi = calculate_psi(arr, arr)
    assert psi == 0.0
