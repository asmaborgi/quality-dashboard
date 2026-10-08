"""Calculs des indicateurs qualité à partir d'un DataFrame de tests."""
import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"boards": 0, "tests": 0, "fpy": None, "defect_rate": None}
    first_pass = df[df["attempt"] == 1]
    fpy = (first_pass["result"] == "PASS").mean() * 100  # First Pass Yield
    defect_rate = (df["result"] == "FAIL").mean() * 100
    return {
        "boards": int(df["board_id"].nunique()),
        "tests": int(len(df)),
        "fpy": round(float(fpy), 2),
        "defect_rate": round(float(defect_rate), 2),
    }


def compute_pareto(df: pd.DataFrame) -> list[dict]:
    fails = df[(df["result"] == "FAIL") & (df["defect_type"] != "")]
    counts = fails["defect_type"].value_counts()
    if counts.empty:
        return []
    cumulative = counts.cumsum() / counts.sum() * 100
    return [
        {"defect_type": name, "count": int(n), "cumulative_pct": round(float(c), 2)}
        for (name, n), c in zip(counts.items(), cumulative)
    ]


def compute_fpy_trend(df: pd.DataFrame) -> list[dict]:
    first_pass = df[df["attempt"] == 1].copy()
    if first_pass.empty:
        return []
    first_pass["day"] = first_pass["test_date"].dt.strftime("%Y-%m-%d")
    daily = first_pass.groupby("day")["result"].apply(lambda s: (s == "PASS").mean() * 100)
    return [{"day": d, "fpy": round(float(v), 2)} for d, v in daily.items()]


def compute_by_line(df: pd.DataFrame) -> list[dict]:
    first_pass = df[df["attempt"] == 1]
    if first_pass.empty:
        return []
    by_line = first_pass.groupby("line")["result"].apply(lambda s: (s == "PASS").mean() * 100)
    return [{"line": l, "fpy": round(float(v), 2)} for l, v in by_line.items()]
