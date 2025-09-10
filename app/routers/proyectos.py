from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

# Rutas de funciones del modelo proyecto

@router.post("", response_model=schemas.SalidaProyecto, status_code=status.HTTP_201_CREATED)
def crear_proyecto(payload: schemas.CrearProyecto, db: Session = Depends(get_db)):
    if db.query(models.Proyecto).filter(models.Proyecto.nombre == payload.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe un proyecto con ese nombre")
    obj = models.Proyecto(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=List[schemas.SalidaProyecto])
def lista_proyectos(db: Session = Depends(get_db)):
    return db.query(models.Proyecto).all()


@router.get("/{proyecto_id}", response_model=schemas.SalidaProyecto)
def get_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Proyecto, proyecto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return obj


@router.put("/{proyecto_id}", response_model=schemas.SalidaProyecto)
def actualizar_proyecto(proyecto_id: int, payload: schemas.ActualizarProyecto, db: Session = Depends(get_db)):
    obj = db.get(models.Proyecto, proyecto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Proyecto, proyecto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(obj)
    db.commit()
    return None


@router.post("/{proyecto_id}/asignar", response_model=schemas.SalidaProyecto)
def asignar_miembro(proyecto_id: int, payload: schemas.AsignarMiembro, db: Session = Depends(get_db)):
    proyecto = db.get(models.Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    miembro = db.get(models.Miembro, payload.miembro_id)
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    if miembro not in proyecto.miembros:
        proyecto.miembros.append(miembro)
        db.add(proyecto)
        db.commit()
        db.refresh(proyecto)
    return proyecto
