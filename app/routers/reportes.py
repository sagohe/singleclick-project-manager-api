from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/informacion", response_model=schemas.Resumen)
def summary(db: Session = Depends(get_db)):
    total_projects = db.query(models.Proyecto).count()
    in_progress = db.query(models.Proyecto).filter(models.Proyecto.status == models.EstadoProyecto.EN_PROGRESO).count()
    done = db.query(models.Proyecto).filter(models.Proyecto.status == models.EstadoProyecto.DONE).count()
    total_miembros = db.query(models.Miembro).count()
    return schemas.Resumen(
        total_projects=total_projects,
        in_progress=in_progress,
        done=done,
        total_miembros=total_miembros,
    )
