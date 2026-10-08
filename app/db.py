import os
import sqlite3
from contextlib import contextmanager

import pandas as pd

REQUIRED_COLUMNS = {"board_id", "test_date", "line", "attempt", "result", "defect_type"}


def db_path() -> str:
    return os.environ.get("QUALITY_DB", "quality.db")


@contextmanager
def connection():
    conn = sqlite3.connect(db_path())
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes : {', '.join(sorted(missing))}")
    df = df[sorted(REQUIRED_COLUMNS)].copy()
    df["result"] = df["result"].astype(str).str.strip().str.upper()
    if not df["result"].isin(["PASS", "FAIL"]).all():
        raise ValueError("La colonne 'result' doit contenir uniquement PASS ou FAIL")
    df["test_date"] = pd.to_datetime(df["test_date"], errors="raise")
    df["attempt"] = df["attempt"].astype(int)
    df["defect_type"] = df["defect_type"].fillna("").astype(str).str.strip()
    return df


def replace_data(df: pd.DataFrame) -> None:
    df = clean_and_validate(df)
    with connection() as conn:
        df.to_sql("tests", conn, if_exists="replace", index=False)


def read_data() -> pd.DataFrame:
    with connection() as conn:
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='tests'"
        ).fetchone()
        if not exists:
            return pd.DataFrame(columns=sorted(REQUIRED_COLUMNS))
        return pd.read_sql_query("SELECT * FROM tests", conn, parse_dates=["test_date"])
