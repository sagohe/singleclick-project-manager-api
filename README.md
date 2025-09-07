# SingleClick – Project Manager API (Demo)

Microservicio **FastAPI** para gestionar **proyectos** y **miembros** del equipo, con buenas prácticas de validación, pruebas y CI/CD.  
Pensado como demo técnico para prácticas en **SingleClick**.

## 🚀 Stack
- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy 2.x (SQLite por defecto)
- Pydantic v2
- Pytest (+ httpx TestClient)
- Ruff, Black, mypy
- Dockerfile + GitHub Actions

## 📦 Instalación local
```bash
python -m venv .venv && source .venv/bin/activate  # (en Windows: .venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
