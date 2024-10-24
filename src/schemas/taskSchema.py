from pydantic import BaseModel
from datetime import date

# Esquema para crear una tarea
class TaskCreate(BaseModel):
    fechaEstimada: date
    fechaRealizacion: date
    descripcion: str
    estadoId: int
    planeadaAutomaticamente: bool
    esMecanizable: bool
    cultivoId: int
    laborId: int
    insumoId: int
    manoObraId: int

    class Config:
        orm_mode = True

# Esquema para actualizar una tarea
class TaskUpdate(BaseModel):
    fechaEstimada: date
    fechaRealizacion: date
    descripcion: str
    estadoId: int
    planeadaAutomaticamente: bool
    esMecanizable: bool
    cultivoId: int
    laborId: int
    insumoId: int
    manoObraId: int

    class Config:
        orm_mode = True

# Esquema de respuesta
class TaskResponse(BaseModel):
    id: int
    fechaEstimada: date
    fechaRealizacion: date
    descripcion: str
    estadoId: int
    planeadaAutomaticamente: bool
    esMecanizable: bool
    cultivoId: int
    laborId: int
    insumoId: int
    manoObraId: int

    class Config:
        orm_mode = True
