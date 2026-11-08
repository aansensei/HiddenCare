# lakehouse mo hinh hoa du lieu nhung voi duckdb va parquet
from pathlib import Path
import duckdb
import pandas as pd
from hiddencare.config import PATHS, MIN_AGE, A1C_THRESHOLD, EXCLUDE_PREGNANCY_CODE


# khoi tao ket noi duckdb toi tep co so du lieu cuc bo
def get_lakehouse_connection(db_path: Path | None = None) -> duckdb.DuckDBPyConnection:
    if db_path is None:
        db_path = PATHS["processed"].parent / "hiddencare.duckdb"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(db_path))


# nap cac thanh phan du lieu vao lakehouse
def ingest_raw_components_to_lakehouse(
    conn: duckdb.DuckDBPyConnection,
    raw_pre_dir: Path,
    raw_post_dir: Path,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    
    # danh sach cac thanh phan xpt can nap
    components = [
        ("pre_demo", raw_pre_dir / "P_DEMO.xpt"),
        ("pre_diq", raw_pre_dir / "P_DIQ.xpt"),
        ("pre_ghb", raw_pre_dir / "P_GHB.xpt"),
        ("pre_bmx", raw_pre_dir / "P_BMX.xpt"),
        ("pre_hiq", raw_pre_dir / "P_HIQ.xpt"),
        ("post_demo", raw_post_dir / "DEMO_L.xpt"),
        ("post_diq", raw_post_dir / "DIQ_L.xpt"),
        ("post_ghb", raw_post_dir / "GHB_L.xpt"),
        ("post_bmx", raw_post_dir / "BMX_L.xpt"),
        ("post_hiq", raw_post_dir / "HIQ_L.xpt"),
    ]
    
    for table_name, file_path in components:
        if not file_path.exists():
            continue
        df_comp = pd.read_sas(file_path, format="xport")
        df_comp.columns = [str(c).upper() for c in df_comp.columns]
        conn.register(f"temp_{table_name}", df_comp)
        conn.execute(f"CREATE OR REPLACE TABLE raw_{table_name} AS SELECT * FROM temp_{table_name}")
        row_cnt = conn.execute(f"SELECT count(*) FROM raw_{table_name}").fetchone()[0]
        counts[table_name] = row_cnt
        
    return counts


# tao bang staging va cohort tinh toan thuan bang sql trong duckdb
def build_lakehouse_cohorts(conn: duckdb.DuckDBPyConnection) -> dict[str, int]:
    # staging tien dai dich 2017 to 2020
    conn.execute("""
        CREATE OR REPLACE VIEW stg_pre_merged AS
        SELECT
            CAST(d.SEQN AS INTEGER) AS seqn,
            CAST(d.RIDAGEYR AS DOUBLE) AS age,
            CAST(d.RIAGENDR AS INTEGER) AS sex,
            CAST(d.INDFMPIR AS DOUBLE) AS pir,
            CAST(d.SDMVPSU AS INTEGER) AS psu,
            CAST(d.SDMVSTRA AS INTEGER) AS strata,
            CAST(d.WTMECPRP AS DOUBLE) AS weight,
            CAST(d.RIDEXPRG AS DOUBLE) AS prg,
            CAST(q.DIQ010 AS INTEGER) AS dx,
            CAST(g.LBXGH AS DOUBLE) AS a1c,
            CAST(b.BMXBMI AS DOUBLE) AS bmi,
            CAST(b.BMXWAIST AS DOUBLE) AS waist,
            CAST(h.HIQ011 AS INTEGER) AS hiq
        FROM raw_pre_demo d
        INNER JOIN raw_pre_diq q ON d.SEQN = q.SEQN
        LEFT JOIN raw_pre_ghb g ON d.SEQN = g.SEQN
        LEFT JOIN raw_pre_bmx b ON d.SEQN = b.SEQN
        LEFT JOIN raw_pre_hiq h ON d.SEQN = h.SEQN;
    """)

    # staging hau dai dich 2021 to 2023
    conn.execute("""
        CREATE OR REPLACE VIEW stg_post_merged AS
        SELECT
            CAST(d.SEQN AS INTEGER) AS seqn,
            CAST(d.RIDAGEYR AS DOUBLE) AS age,
            CAST(d.RIAGENDR AS INTEGER) AS sex,
            CAST(d.INDFMPIR AS DOUBLE) AS pir,
            CAST(d.SDMVPSU AS INTEGER) AS psu,
            CAST(d.SDMVSTRA AS INTEGER) AS strata,
            CAST(g.WTPH2YR AS DOUBLE) AS weight,
            CAST(d.RIDEXPRG AS DOUBLE) AS prg,
            CAST(q.DIQ010 AS INTEGER) AS dx,
            CAST(g.LBXGH AS DOUBLE) AS a1c,
            CAST(b.BMXBMI AS DOUBLE) AS bmi,
            CAST(b.BMXWAIST AS DOUBLE) AS waist,
            CAST(h.HIQ011 AS INTEGER) AS hiq
        FROM raw_post_demo d
        INNER JOIN raw_post_diq q ON d.SEQN = q.SEQN
        LEFT JOIN raw_post_ghb g ON d.SEQN = g.SEQN
        LEFT JOIN raw_post_bmx b ON d.SEQN = b.SEQN
        LEFT JOIN raw_post_hiq h ON d.SEQN = h.SEQN;
    """)

    # tao bang cohort huan luyen tien dai dich
    conn.execute(f"""
        CREATE OR REPLACE TABLE cohort_train AS
        SELECT
            seqn, age, sex, pir, psu, strata, weight, prg, dx, a1c, bmi, waist, hiq,
            CASE WHEN dx = 1 THEN 1 ELSE 0 END AS label_dx,
            CASE WHEN dx = 1 OR a1c >= {A1C_THRESHOLD} THEN 1 ELSE 0 END AS label_full,
            CASE
                WHEN hiq = 1 THEN 'insured'
                WHEN hiq = 2 THEN 'uninsured'
                ELSE 'unknown'
            END AS insured,
            CASE
                WHEN pir IS NULL THEN 'missing'
                WHEN pir < 1.30 THEN 'low'
                WHEN pir >= 1.30 AND pir <= 3.50 THEN 'middle'
                WHEN pir > 3.50 THEN 'high'
                ELSE 'missing'
            END AS pir_group
        FROM stg_pre_merged
        WHERE age >= {MIN_AGE}
          AND dx IN (1, 2)
          AND a1c IS NOT NULL
          AND weight > 0
          AND (prg IS NULL OR prg != {EXCLUDE_PREGNANCY_CODE});
    """)

    # tao bang cohort danh gia hau dai dich
    conn.execute(f"""
        CREATE OR REPLACE TABLE cohort_eval AS
        SELECT
            seqn, age, sex, pir, psu, strata, weight, prg, dx, a1c, bmi, waist, hiq,
            CASE WHEN dx = 1 THEN 1 ELSE 0 END AS label_dx,
            CASE WHEN dx = 1 OR a1c >= {A1C_THRESHOLD} THEN 1 ELSE 0 END AS label_full,
            CASE
                WHEN hiq = 1 THEN 'insured'
                WHEN hiq = 2 THEN 'uninsured'
                ELSE 'unknown'
            END AS insured,
            CASE
                WHEN pir IS NULL THEN 'missing'
                WHEN pir < 1.30 THEN 'low'
                WHEN pir >= 1.30 AND pir <= 3.50 THEN 'middle'
                WHEN pir > 3.50 THEN 'high'
                ELSE 'missing'
            END AS pir_group,
            CASE WHEN a1c >= {A1C_THRESHOLD} THEN 1 ELSE 0 END AS potential_case
        FROM stg_post_merged
        WHERE age >= {MIN_AGE}
          AND dx = 2
          AND a1c IS NOT NULL
          AND weight > 0
          AND (prg IS NULL OR prg != {EXCLUDE_PREGNANCY_CODE});
    """)

    train_cnt = conn.execute("SELECT count(*) FROM cohort_train").fetchone()[0]
    eval_cnt = conn.execute("SELECT count(*) FROM cohort_eval").fetchone()[0]
    return {"cohort_train": train_cnt, "eval_subset": eval_cnt}


# xuat du lieu tu duckdb ra cac tep parquet
def export_lakehouse_parquet(conn: duckdb.DuckDBPyConnection, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    train_path = output_dir / "lakehouse_cohort_train.parquet"
    eval_path = output_dir / "lakehouse_eval_subset.parquet"
    
    conn.execute(f"COPY cohort_train TO '{train_path.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    conn.execute(f"COPY cohort_eval TO '{eval_path.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    
    return {"cohort_train": train_path, "eval_subset": eval_path}


# thuc hien truy van phan tich truc tiep tren lakehouse
def query_lakehouse_equity_summary(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    query = """
        SELECT
            insured,
            count(*) AS total_count,
            sum(potential_case) AS total_cases,
            round(sum(potential_case) * 100.0 / count(*), 2) AS prevalence_pct,
            round(sum(weight * potential_case) / sum(weight) * 100.0, 2) AS weighted_prevalence_pct
        FROM cohort_eval
        GROUP BY insured
        ORDER BY insured;
    """
    return conn.execute(query).df()
