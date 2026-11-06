# Functions for downloading, validating, and merging NHANES data files.

from pathlib import Path
import urllib.request
import pandas as pd


# Download remote XPT file if missing and verify it is not an HTML error response.
def download_xpt(url: str, dest_path: Path) -> Path:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if not dest_path.exists():
        urllib.request.urlretrieve(url, dest_path)
    with open(dest_path, "rb") as f:
        head = f.read(80)
    if b"<!DOCTYPE" in head or b"<html" in head.lower():
        raise ValueError(f"Downloaded file {dest_path} is an HTML error page, not an XPT file.")
    return dest_path


# Download all required component files for a given cycle.
def download_cycle_files(urls_dict: dict, target_dir: Path) -> dict:
    local_paths = {}
    for comp_name, url in urls_dict.items():
        filename = Path(url).name
        dest = target_dir / filename
        local_paths[comp_name] = download_xpt(url, dest)
    return local_paths


# Load and merge component files for pre-pandemic release.
def load_pre_pandemic_data(raw_dir: Path) -> pd.DataFrame:
    demo_path = raw_dir / "P_DEMO.xpt"
    diq_path = raw_dir / "P_DIQ.xpt"
    ghb_path = raw_dir / "P_GHB.xpt"
    bmx_path = raw_dir / "P_BMX.xpt"
    hiq_path = raw_dir / "P_HIQ.xpt"

    demo = pd.read_sas(demo_path, format="xport")[
        ["SEQN", "RIDAGEYR", "RIAGENDR", "INDFMPIR", "SDMVPSU", "SDMVSTRA", "WTMECPRP", "RIDEXPRG"]
    ].rename(
        columns={
            "SEQN": "seqn",
            "RIDAGEYR": "age",
            "RIAGENDR": "sex",
            "INDFMPIR": "pir",
            "SDMVPSU": "psu",
            "SDMVSTRA": "strata",
            "WTMECPRP": "weight",
            "RIDEXPRG": "prg",
        }
    )

    diq = pd.read_sas(diq_path, format="xport")[["SEQN", "DIQ010"]].rename(
        columns={"SEQN": "seqn", "DIQ010": "dx"}
    )
    ghb = pd.read_sas(ghb_path, format="xport")[["SEQN", "LBXGH"]].rename(
        columns={"SEQN": "seqn", "LBXGH": "a1c"}
    )
    bmx = pd.read_sas(bmx_path, format="xport")[["SEQN", "BMXBMI", "BMXWAIST"]].rename(
        columns={"SEQN": "seqn", "BMXBMI": "bmi", "BMXWAIST": "waist"}
    )
    hiq = pd.read_sas(hiq_path, format="xport")[["SEQN", "HIQ011"]].rename(
        columns={"SEQN": "seqn", "HIQ011": "hiq"}
    )

    # Convert participant identifier to integer.
    for table in [demo, diq, ghb, bmx, hiq]:
        table["seqn"] = table["seqn"].astype(int)
        assert table["seqn"].is_unique, "Duplicate SEQN found within a component."

    # Merge components on participant identifier.
    merged = demo.merge(diq, on="seqn", how="inner")
    merged = merged.merge(ghb, on="seqn", how="left")
    merged = merged.merge(bmx, on="seqn", how="left")
    merged = merged.merge(hiq, on="seqn", how="left")

    assert merged["seqn"].is_unique, "Merged dataset contains duplicate participants."
    return merged


# Load and merge component files for post-pandemic release.
def load_post_pandemic_data(raw_dir: Path) -> pd.DataFrame:
    demo_path = raw_dir / "DEMO_L.xpt"
    diq_path = raw_dir / "DIQ_L.xpt"
    ghb_path = raw_dir / "GHB_L.xpt"
    bmx_path = raw_dir / "BMX_L.xpt"
    hiq_path = raw_dir / "HIQ_L.xpt"

    demo = pd.read_sas(demo_path, format="xport")[
        ["SEQN", "RIDAGEYR", "RIAGENDR", "INDFMPIR", "SDMVPSU", "SDMVSTRA", "RIDEXPRG"]
    ].rename(
        columns={
            "SEQN": "seqn",
            "RIDAGEYR": "age",
            "RIAGENDR": "sex",
            "INDFMPIR": "pir",
            "SDMVPSU": "psu",
            "SDMVSTRA": "strata",
            "RIDEXPRG": "prg",
        }
    )

    diq = pd.read_sas(diq_path, format="xport")[["SEQN", "DIQ010"]].rename(
        columns={"SEQN": "seqn", "DIQ010": "dx"}
    )
    ghb = pd.read_sas(ghb_path, format="xport")[["SEQN", "WTPH2YR", "LBXGH"]].rename(
        columns={"SEQN": "seqn", "WTPH2YR": "weight", "LBXGH": "a1c"}
    )
    bmx = pd.read_sas(bmx_path, format="xport")[["SEQN", "BMXBMI", "BMXWAIST"]].rename(
        columns={"SEQN": "seqn", "BMXBMI": "bmi", "BMXWAIST": "waist"}
    )
    hiq = pd.read_sas(hiq_path, format="xport")[["SEQN", "HIQ011"]].rename(
        columns={"SEQN": "seqn", "HIQ011": "hiq"}
    )

    # Convert participant identifier to integer.
    for table in [demo, diq, ghb, bmx, hiq]:
        table["seqn"] = table["seqn"].astype(int)
        assert table["seqn"].is_unique, "Duplicate SEQN found within a component."

    # Merge components on participant identifier.
    merged = demo.merge(diq, on="seqn", how="inner")
    merged = merged.merge(ghb, on="seqn", how="left")
    merged = merged.merge(bmx, on="seqn", how="left")
    merged = merged.merge(hiq, on="seqn", how="left")

    assert merged["seqn"].is_unique, "Merged dataset contains duplicate participants."
    return merged
