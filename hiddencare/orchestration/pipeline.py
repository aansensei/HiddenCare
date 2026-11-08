# he thong dieu phoi du lieu dua tren tai san theo nguyen ly dagster va dbt
from typing import Callable, Any
from pathlib import Path
import time
import pandas as pd
from hiddencare.config import PATHS, URLS, PREDICTORS, PRIMARY_CAPACITY
from hiddencare.data import download_cycle_files, load_pre_pandemic_data, load_post_pandemic_data
from hiddencare.cohort import build_cohort
from hiddencare.lakehouse import get_lakehouse_connection, ingest_raw_components_to_lakehouse, build_lakehouse_cohorts, export_lakehouse_parquet
from hiddencare.contracts import CohortSchema, run_schema_drift_audit
from hiddencare.survey_stats import evaluate_survey_variance_summary
from hiddencare.robustness import run_architecture_robustness_check
import joblib


# lop dai dien cho mot tai san du lieu trong he thong
class DataAsset:
    def __init__(
        self,
        name: str,
        depends_on: list[str],
        fn: Callable[..., Any],
        description: str = "",
    ):
        self.name = name
        self.depends_on = depends_on
        self.fn = fn
        self.description = description
        self.metadata: dict[str, Any] = {}


# he thong dang ky va thuc thi cac tai san theo do thi co huong dag
class AssetOrchestrator:
    def __init__(self):
        self.assets: dict[str, DataAsset] = {}
        
    def register(self, name: str, depends_on: list[str], description: str = ""):
        def decorator(fn: Callable[..., Any]):
            asset = DataAsset(name, depends_on, fn, description)
            self.assets[name] = asset
            return fn
        return decorator

    def execute_all(self) -> dict[str, dict[str, Any]]:
        # sap xep thu tu thuc thi dua tren phu thuoc dag
        execution_order = []
        visited = set()
        
        def visit(node: str):
            if node in visited:
                return
            for dep in self.assets[node].depends_on:
                if dep in self.assets:
                    visit(dep)
            visited.add(node)
            execution_order.append(node)
            
        for asset_name in self.assets:
            visit(asset_name)
            
        manifest = {}
        
        # thuc thi tung tai san theo thu tu tuyen tinh
        for name in execution_order:
            asset = self.assets[name]
            t0 = time.time()
            result = asset.fn()
            t_elapsed = round(time.time() - t0, 3)
            
            meta = {
                "asset": name,
                "description": asset.description,
                "dependencies": asset.depends_on,
                "duration_seconds": t_elapsed,
                "status": "MATERIALIZED",
            }
            if isinstance(result, pd.DataFrame):
                meta["record_count"] = len(result)
            elif isinstance(result, dict) and "record_count" in result:
                meta["record_count"] = result["record_count"]
                
            asset.metadata = meta
            manifest[name] = meta
            
        return manifest


# khoi tao bo dieu phoi toan cuc
orchestrator = AssetOrchestrator()


# 1. tai san nap du lieu tho tu cdc
@orchestrator.register("raw_nhanes_assets", depends_on=[], description="Tai va xac thuc 10 tep XPT tu may chu CDC")
def materialize_raw_nhanes_assets():
    download_cycle_files(URLS["pre_pandemic"], PATHS["raw_pre"])
    download_cycle_files(URLS["post_pandemic"], PATHS["raw_post"])
    return {"status": "SUCCESS"}


# 2. tai san ho du lieu nhung duckdb
@orchestrator.register("duckdb_lakehouse_assets", depends_on=["raw_nhanes_assets"], description="Nap vao co so du lieu DuckDB va tao view staging")
def materialize_duckdb_lakehouse_assets():
    conn = get_lakehouse_connection()
    ingest_raw_components_to_lakehouse(conn, PATHS["raw_pre"], PATHS["raw_post"])
    res = build_lakehouse_cohorts(conn)
    export_lakehouse_parquet(conn, PATHS["processed"])
    conn.close()
    return {"status": "SUCCESS", "record_count": res["cohort_train"] + res["eval_subset"]}


# 3. tai san hop dong du lieu va kiem toan bien dong pandera
@orchestrator.register("pandera_contract_assets", depends_on=["duckdb_lakehouse_assets"], description="Xac thuc hop dong du lieu va kiem toan schema drift")
def materialize_pandera_contract_assets():
    df_train = pd.read_parquet(PATHS["processed"] / "cohort_train.parquet")
    df_eval = pd.read_parquet(PATHS["processed"] / "eval_subset.parquet")
    CohortSchema.validate(df_train)
    CohortSchema.validate(df_eval)
    drift = run_schema_drift_audit(df_train, df_eval, PATHS["reports"])
    return {"status": drift["status"], "record_count": len(df_train)}


# 4. tai san uoc luong phuong sai khao sat phuc hop
@orchestrator.register("survey_variance_assets", depends_on=["pandera_contract_assets"], description="Uoc luong sai so khao sat phuc hop bang chuoi Taylor")
def materialize_survey_variance_assets():
    model_a = joblib.load(PATHS["models"] / "model_dx.joblib")
    model_b = joblib.load(PATHS["models"] / "model_full.joblib")
    df_eval = pd.read_parquet(PATHS["processed"] / "eval_subset.parquet")
    scores_a = model_a.predict_proba(df_eval[PREDICTORS])[:, 1]
    scores_b = model_b.predict_proba(df_eval[PREDICTORS])[:, 1]
    df_res = evaluate_survey_variance_summary(df_eval, scores_a, scores_b)
    df_res.to_csv(PATHS["tables"] / "survey_variance_summary.csv", index=False)
    return df_res


# 5. tai san kiem dinh do ben mo hinh qua cac kien truc phi tuyen
@orchestrator.register("robustness_check_assets", depends_on=["pandera_contract_assets"], description="Kiem dinh do ben voi Random Forest va Gradient Boosting")
def materialize_robustness_check_assets():
    df_train = pd.read_parquet(PATHS["processed"] / "cohort_train.parquet")
    df_eval = pd.read_parquet(PATHS["processed"] / "eval_subset.parquet")
    df_res = run_architecture_robustness_check(df_train, df_eval, PATHS["tables"], PATHS["figures"])
    return df_res


# ham thuc thi toan bo pipeline qua bo dieu phoi tai san
def run_asset_pipeline():
    return orchestrator.execute_all()


if __name__ == "__main__":
    print("Running Asset-Based Pipeline Orchestration...")
    manifest = run_asset_pipeline()
    for asset_name, meta in manifest.items():
        print(f"  [{meta['status']}] {asset_name} ({meta['duration_seconds']}s): {meta['description']}")
    print("Pipeline execution completed successfully!")
