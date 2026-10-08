import io
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from . import analysis, db

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_CSV = BASE_DIR.parent / "data" / "sample_tests.csv"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au premier lancement, charge les données d'exemple si la base est vide
    if db.read_data().empty and SAMPLE_CSV.exists():
        db.replace_data(pd.read_csv(SAMPLE_CSV))
    yield


app = FastAPI(title="Tableau de bord qualité", lifespan=lifespan)


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/kpis")
def kpis():
    return analysis.compute_kpis(db.read_data())


@app.get("/api/pareto")
def pareto():
    return analysis.compute_pareto(db.read_data())


@app.get("/api/trend")
def trend():
    return analysis.compute_fpy_trend(db.read_data())


@app.get("/api/lines")
def lines():
    return analysis.compute_by_line(db.read_data())


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Le fichier doit être un CSV")
    try:
        df = pd.read_csv(io.BytesIO(await file.read()))
        db.replace_data(df)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"status": "ok", "rows": len(df)}
