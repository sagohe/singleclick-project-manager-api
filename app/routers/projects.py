from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    if db.query(models.Project).filter(models.Project.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Ya existe un proyecto con ese nombre")
    obj = models.Project(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Project, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return obj


@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Project, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Project, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(obj)
    db.commit()
    return None


@router.post("/{project_id}/assign", response_model=schemas.ProjectOut)
def assign_member(project_id: int, payload: schemas.AssignMember, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    member = db.get(models.Member, payload.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    if member not in project.members:
        project.members.append(member)
        db.add(project)
        db.commit()
        db.refresh(project)
    return project
