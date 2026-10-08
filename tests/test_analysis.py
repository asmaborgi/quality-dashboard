import pandas as pd
import pytest

from app import analysis, db


def make_df():
    return pd.DataFrame(
        {
            "board_id": ["A", "B", "C", "C", "D"],
            "test_date": pd.to_datetime(["2026-09-01"] * 5),
            "line": ["L1", "L1", "L2", "L2", "L2"],
            "attempt": [1, 1, 1, 2, 1],
            "result": ["PASS", "PASS", "FAIL", "PASS", "FAIL"],
            "defect_type": ["", "", "Soudure froide", "", "Soudure froide"],
        }
    )


def test_kpis():
    k = analysis.compute_kpis(make_df())
    assert k["boards"] == 4
    assert k["tests"] == 5
    assert k["fpy"] == 50.0          # 2 cartes sur 4 OK au premier passage
    assert k["defect_rate"] == 40.0  # 2 échecs sur 5 tests


def test_pareto():
    p = analysis.compute_pareto(make_df())
    assert p == [{"defect_type": "Soudure froide", "count": 2, "cumulative_pct": 100.0}]


def test_empty_dataframe():
    k = analysis.compute_kpis(make_df().iloc[0:0])
    assert k["fpy"] is None


def test_validation_rejects_missing_columns():
    with pytest.raises(ValueError):
        db.clean_and_validate(pd.DataFrame({"board_id": ["A"]}))
