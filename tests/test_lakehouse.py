# kiem thu he thong lakehouse duckdb
import duckdb
import pandas as pd
from hiddencare.lakehouse import get_lakehouse_connection, build_lakehouse_cohorts, query_lakehouse_equity_summary


# kiem thu ket noi va truy van duckdb
def test_lakehouse_memory_connection():
    conn = duckdb.connect(":memory:")
    df_test = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
    conn.register("df_test", df_test)
    res = conn.execute("SELECT sum(a), sum(b) FROM df_test").fetchone()
    assert res == (6, 60)
    conn.close()


# kiem thu phan tich tong hop cong bang y te tren duckdb
def test_lakehouse_equity_query_structure():
    conn = duckdb.connect(":memory:")
    sample_cohort = pd.DataFrame({
        "insured": ["insured", "insured", "uninsured", "uninsured"],
        "potential_case": [1, 0, 1, 0],
        "weight": [100.0, 100.0, 50.0, 50.0],
    })
    conn.register("cohort_eval", sample_cohort)
    conn.execute("CREATE TABLE cohort_eval AS SELECT * FROM cohort_eval")
    df_res = query_lakehouse_equity_summary(conn)
    assert len(df_res) == 2
    assert "prevalence_pct" in df_res.columns
    assert "weighted_prevalence_pct" in df_res.columns
    conn.close()
