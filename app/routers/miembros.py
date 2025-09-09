from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/miembros", tags=["Miembros"])


@router.post("", response_model=schemas.SalidaMiembro, status_code=status.HTTP_201_CREATED)
def crear_miembro(payload: schemas.CrearMiembro, db: Session = Depends(get_db)):
    if db.query(models.Miembro).filter(models.Miembro.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Ya existe un miembro con ese email")
    obj = models.Miembro(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=List[schemas.SalidaMiembro])
def lista_miembros(db: Session = Depends(get_db)):
    return db.query(models.Miembro).all()


@router.get("/{miembro_id}", response_model=schemas.SalidaMiembro)
def get_miembro(miembro_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Miembro, miembro_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return obj


@router.put("/{miembro_id}", response_model=schemas.SalidaMiembro)
def actualizar_miembro(miembro_id: int, payload: schemas.ActualizarMiembro, db: Session = Depends(get_db)):
    obj = db.get(models.Miembro, miembro_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{miembro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_miembro(miembro_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Miembro, miembro_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    db.delete(obj)
    db.commit()
    return None
