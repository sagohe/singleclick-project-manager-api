from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Literal

# Uso Pydantic por la organizacion y practica al usar una db

EstadoProyecto = Literal["EN_PROGRESO", "DONE"]

# Esquemas del miembro
class MiembroBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    rol: Optional[str] = Field(default=None, max_length=120)
    email: EmailStr


class CrearMiembro(MiembroBase):
    pass


class ActualizarMiembro(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=120)
    rol: Optional[str] = Field(default=None, max_length=120)
    email: Optional[EmailStr] = None


class SalidaMiembro(MiembroBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas del proyecto
class ProyectoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    estado: EstadoProyecto = "EN_PROGRESO"
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, values):
        start = values.get("start_date")
        if v and start and v < start:
            raise ValueError("end_date no puede ser anterior a start_date")
        return v


class CrearProyecto(ProyectoBase):
    pass


class ActualizarProyecto(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    estado: Optional[EstadoProyecto] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, values):
        start = values.get("start_date")
        if v and start and v < start:
            raise ValueError("end_date no puede ser anterior a start_date")
        return v


class SalidaProyecto(ProyectoBase):
    id: int
    miembros: List[SalidaMiembro] = []

    class Config:
        from_attributes = True


class AsignarMiembro(BaseModel):
    miembro_id: int


class Resumen(BaseModel):
    total_proyectos: int
    en_progreso: int
    done: int
    miembros_totales: int
