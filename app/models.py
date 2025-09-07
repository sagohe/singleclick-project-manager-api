from datetime import date
from sqlalchemy import String, Integer, Date, Enum, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from .database import Base


class ProjectStatus(str, PyEnum):
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


project_members = Table(
    "project_members",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("member_id", ForeignKey("members.id", ondelete="CASCADE"), primary_key=True),
)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.IN_PROGRESS)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)

    members: Mapped[list["Member"]] = relationship(
        "Member",
        secondary=project_members,
        back_populates="projects",
        lazy="selectin",
    )


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    role: Mapped[str | None] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)

    projects: Mapped[list[Project]] = relationship(
        "Project",
        secondary=project_members,
        back_populates="members",
        lazy="selectin",
    )
