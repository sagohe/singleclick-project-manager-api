from fastapi import FastAPI
from .database import Base, engine
from .routers import miembros, proyectos, reportes
from . import models
from fastapi.staticfiles import StaticFiles

# Crear tablas (para demo). 
Base.metadata.create_all(bind=engine)

# Programa hecho especialmente para SingleClick v1.0
app = FastAPI(title="SingleClick - DEMO Gestion de grupos", version="1.0.0")

app.mount("/web", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(proyectos.router)
app.include_router(miembros.router)
app.include_router(reportes.router)
