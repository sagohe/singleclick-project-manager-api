from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, List, Literal

# Uso Pydantic por la organizacion y practica al usar una db

EstadoProyecto = Literal["EN_PROGRESO", "DONE"]

# ----- Miembros -----
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

# ----- Proyectos -----
class ProyectoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=500)   # 👈 usa el mismo nombre que esperas en la API
    estado: EstadoProyecto = "EN_PROGRESO"
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def _check_dates(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValueError("end_date no puede ser anterior a start_date")
        return self

class CrearProyecto(ProyectoBase):
    pass

class ActualizarProyecto(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    estado: Optional[EstadoProyecto] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def _check_dates(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValueError("end_date no puede ser anterior a start_date")
        return self

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
