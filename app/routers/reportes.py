from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/reportes", tags=["Reportes"])

# Ruta de  informacion general creada en la API

@router.get("/informacion", response_model=schemas.Resumen)
def informacion(db: Session = Depends(get_db)):
    total_proyectos = db.query(models.Proyecto).count()
    en_progreso = db.query(models.Proyecto).filter(models.Proyecto.estado == models.EstadoProyecto.EN_PROGRESO).count()
    done = db.query(models.Proyecto).filter(models.Proyecto.estado == models.EstadoProyecto.DONE).count()
    miembros_totales = db.query(models.Miembro).count()
    return schemas.Resumen(
        total_proyectos=total_proyectos,
        en_progreso=en_progreso,
        done=done,
        miembros_totales=miembros_totales,
    )
