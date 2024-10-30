from pydantic import BaseModel
from datetime import date
from typing import Optional

class TaskBase(BaseModel):
    fecha_estimada: date
    fecha_realizacion: Optional[date] = None
    descripcion: Optional[str] = None
    estado_id: int
    es_mecanizable: bool
    cultivo_id: int
    labor_cultural_id: int
    insumo_agricola_id: Optional[int] = None
    usuario_id: int
    tiempo_hora: Optional[int] = None
    maquinaria_agricola_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
