# Tableau de bord qualité – tests ICT

Application web qui calcule et affiche des indicateurs qualité à partir de journaux de tests de cartes électroniques :

- **FPY** (First Pass Yield) : part des cartes OK dès le premier passage
- **Taux de défauts** global
- **Diagramme de Pareto** des types de défauts (avec cumul en %)
- **Évolution du FPY** par jour et **FPY par ligne** de production

> Projet personnel inspiré d'un travail d'analyse de performance industrielle. Les données fournies sont **entièrement fictives**.

## Technologies

Python · FastAPI · pandas · SQLite · Chart.js · pytest

## Lancer le projet

```bash
git clone https://github.com/asmaborgi/quality-dashboard.git
cd quality-dashboard
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python data/generate_sample_data.py   # régénère les données d'exemple (optionnel)
uvicorn app.main:app --reload
```

Ouvrir ensuite http://127.0.0.1:8000

## Importer ses propres données

Via le bouton « Importer » de la page, avec un CSV contenant les colonnes :

| Colonne | Description |
|---|---|
| board_id | Identifiant de la carte |
| test_date | Date et heure du test |
| line | Ligne de production |
| attempt | 1 = premier passage, 2+ = re-test |
| result | PASS ou FAIL |
| defect_type | Type de défaut (vide si PASS) |

## API

| Route | Description |
|---|---|
| `GET /api/kpis` | FPY, taux de défauts, nombre de cartes et de tests |
| `GET /api/pareto` | Défauts triés avec cumul % |
| `GET /api/trend` | FPY par jour |
| `GET /api/lines` | FPY par ligne |
| `POST /api/upload` | Import d'un CSV |

La documentation interactive est disponible sur `/docs`.

## Tests

```bash
pytest
```

## Structure

```
app/            API FastAPI, calculs (analysis.py), accès base (db.py), page web
data/           générateur de données fictives + CSV d'exemple
tests/          tests unitaires
```

## Pistes d'amélioration

- Filtres par ligne et par période
- Authentification et plusieurs jeux de données
- Déploiement avec Docker

## Auteure

Asma Borgi – [LinkedIn](https://www.linkedin.com/in/borgi-asma)
