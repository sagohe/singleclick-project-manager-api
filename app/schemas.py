from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Literal


ProjectStatus = Literal["IN_PROGRESS", "DONE"]


class MemberBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    role: Optional[str] = Field(default=None, max_length=120)
    email: EmailStr


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    role: Optional[str] = Field(default=None, max_length=120)
    email: Optional[EmailStr] = None


class MemberOut(MemberBase):
    id: int

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    status: ProjectStatus = "IN_PROGRESS"
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, values):
        start = values.get("start_date")
        if v and start and v < start:
            raise ValueError("end_date no puede ser anterior a start_date")
        return v


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, values):
        start = values.get("start_date")
        if v and start and v < start:
            raise ValueError("end_date no puede ser anterior a start_date")
        return v


class ProjectOut(ProjectBase):
    id: int
    members: List[MemberOut] = []

    class Config:
        from_attributes = True


class AssignMember(BaseModel):
    member_id: int


class SummaryReport(BaseModel):
    total_projects: int
    in_progress: int
    done: int
    total_members: int
