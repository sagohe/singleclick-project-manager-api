from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("", response_model=schemas.MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(payload: schemas.MemberCreate, db: Session = Depends(get_db)):
    if db.query(models.Member).filter(models.Member.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Ya existe un miembro con ese email")
    obj = models.Member(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=List[schemas.MemberOut])
def list_members(db: Session = Depends(get_db)):
    return db.query(models.Member).all()


@router.get("/{member_id}", response_model=schemas.MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Member, member_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return obj


@router.put("/{member_id}", response_model=schemas.MemberOut)
def update_member(member_id: int, payload: schemas.MemberUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Member, member_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Member, member_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    db.delete(obj)
    db.commit()
    return None
