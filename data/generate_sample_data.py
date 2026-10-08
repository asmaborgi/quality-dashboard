"""Génère des données fictives de tests ICT (carte électronique).

Chaque ligne = un passage d'une carte sur le banc de test.
attempt = 1 pour le premier passage, 2+ pour les re-tests après réparation.
"""
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)

DEFECTS = {
    "Soudure froide": 30,
    "Composant manquant": 22,
    "Court-circuit": 16,
    "Valeur hors tolérance": 12,
    "Pont de soudure": 10,
    "Autre": 5,
}
LINES = ["Ligne A", "Ligne B", "Ligne C"]


def generate(days: int = 30, boards_per_day: int = 60) -> pd.DataFrame:
    rows = []
    start = datetime(2026, 9, 1)
    board_id = 1000
    for d in range(days):
        day = start + timedelta(days=d)
        for _ in range(boards_per_day):
            board_id += 1
            line = random.choice(LINES)
            attempt = 1
            # le taux de défaut varie légèrement selon la ligne
            fail_prob = {"Ligne A": 0.08, "Ligne B": 0.12, "Ligne C": 0.17}[line]
            while True:
                ts = day + timedelta(minutes=random.randint(0, 1439))
                failed = random.random() < (fail_prob if attempt == 1 else 0.25)
                defect = ""
                if failed:
                    defect = random.choices(list(DEFECTS), weights=DEFECTS.values())[0]
                rows.append(
                    {
                        "board_id": f"PCB-{board_id}",
                        "test_date": ts.strftime("%Y-%m-%d %H:%M:%S"),
                        "line": line,
                        "attempt": attempt,
                        "result": "FAIL" if failed else "PASS",
                        "defect_type": defect,
                    }
                )
                if not failed or attempt >= 3:
                    break
                attempt += 1
    return pd.DataFrame(rows)


if __name__ == "__main__":
    out = Path(__file__).parent / "sample_tests.csv"
    df = generate()
    df.to_csv(out, index=False)
    print(f"{len(df)} tests écrits dans {out}")
