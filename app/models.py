from datetime import date
from sqlalchemy import String, Integer, Date, Enum, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from .database import Base

# 2 principales modelos de la API

class EstadoProyecto(str, PyEnum):
    EN_PROGRESO = "EN_PROGRESO"
    DONE = "DONE"

# Tabla intermedia Relacion(muchos - muchos)
proyectos_miembros = Table(
    "project_miembros",
    Base.metadata,
    Column("proyecto_id", ForeignKey("proyectos.id", ondelete="CASCADE"), primary_key=True),
    Column("miembro_id", ForeignKey("miembros.id", ondelete="CASCADE"), primary_key=True),
)

# Grupo
class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    estado: Mapped[EstadoProyecto] = mapped_column(Enum(EstadoProyecto), default=EstadoProyecto.EN_PROGRESO)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    
    # lazy="selectin" consulta adicional optimizada
    miembros: Mapped[list["Miembro"]] = relationship(
        "Miembro",
        secondary=proyectos_miembros,
        back_populates="proyectos",
        lazy="selectin",
    )

# Cada persona
class Miembro(Base):
    __tablename__ = "miembros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), index=True)
    rol: Mapped[str | None] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)

    proyectos: Mapped[list[Proyecto]] = relationship(
        "Proyecto",
        secondary=proyectos_miembros,
        back_populates="miembros",
        lazy="selectin",
    )
