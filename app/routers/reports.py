from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary", response_model=schemas.SummaryReport)
def summary(db: Session = Depends(get_db)):
    total_projects = db.query(models.Project).count()
    in_progress = db.query(models.Project).filter(models.Project.status == models.ProjectStatus.IN_PROGRESS).count()
    done = db.query(models.Project).filter(models.Project.status == models.ProjectStatus.DONE).count()
    total_members = db.query(models.Member).count()
    return schemas.SummaryReport(
        total_projects=total_projects,
        in_progress=in_progress,
        done=done,
        total_members=total_members,
    )
