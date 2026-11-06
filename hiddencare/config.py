# Central configuration parameters for HiddenCare analysis.

from pathlib import Path
import numpy as np

# Project root directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Random seed for all modeling and simulation.
SEED = 42

# Cohort filtering and clinical thresholds.
MIN_AGE = 20
A1C_THRESHOLD = 6.5
EXCLUDE_PREGNANCY_CODE = 1.0

# Screening capacity scenarios and primary comparison.
CAPACITIES = [0.10, 0.20, 0.30]
PRIMARY_CAPACITY = 0.20

# Feature allowlist and evaluation variables.
PREDICTORS = ["age", "sex", "bmi", "waist"]
AUDIT_VARS = ["insured", "pir_group"]
DESIGN_VARS = ["psu", "strata", "weight"]

# Hyperparameter search grid and cross-validation folds.
CV_FOLDS = 5
C_GRID = np.logspace(-4, 1, 10).tolist()

# Verified CDC source URLs for raw public XPT files.
URLS = {
    "pre_pandemic": {
        "demo": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DEMO.xpt",
        "diq": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DIQ.xpt",
        "ghb": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_GHB.xpt",
        "bmx": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_BMX.xpt",
        "hiq": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_HIQ.xpt",
    },
    "post_pandemic": {
        "demo": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.xpt",
        "diq": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DIQ_L.xpt",
        "ghb": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.xpt",
        "bmx": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.xpt",
        "hiq": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HIQ_L.xpt",
    },
}

# Directory paths for inputs, intermediates, outputs, and documentation.
PATHS = {
    "raw_pre": PROJECT_ROOT / "data" / "raw" / "pre_pandemic",
    "raw_post": PROJECT_ROOT / "data" / "raw" / "post_pandemic",
    "processed": PROJECT_ROOT / "data" / "processed",
    "tables": PROJECT_ROOT / "outputs" / "tables",
    "figures": PROJECT_ROOT / "outputs" / "figures",
    "models": PROJECT_ROOT / "outputs" / "models",
    "reports": PROJECT_ROOT / "reports",
}
