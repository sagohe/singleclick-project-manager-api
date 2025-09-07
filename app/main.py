from fastapi import FastAPI
from .database import Base, engine
from .routers import projects, members, reports

# Crear tablas (para demo). En producción usa migraciones (Alembic).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SingleClick – Project Manager API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(projects.router)
app.include_router(members.router)
app.include_router(reports.router)
