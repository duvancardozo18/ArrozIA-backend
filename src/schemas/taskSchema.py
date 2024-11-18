from pydantic import BaseModel
from datetime import date
from typing import Optional
from datetime import datetime



class CulturalWorkOut(BaseModel):
    fecha_inicio: datetime
    fecha_culminacion: Optional[datetime] = None
    actividad: str
    maquinaria: Optional[str] = None  # Puede no aplicar
    operario: str
    descripcion: Optional[str] = None
    valor: float

    class Config:
        orm_mode = True

class CropOut(BaseModel):
    id: int
    cropName: str  # Campo del modelo de cultivo

    class Config:
        orm_mode = True


class LaborCulturalOut(BaseModel):
    id: int
    nombre: str  # Nombre de la labor cultural
    descripcion: Optional[str] = None  # Descripción de la labor cultural
    precio_hectaria: Optional[float] = None  # Precio por hectárea
    precio_hectaria_estimada: Optional[float] = None  # Precio estimado por hectárea

    class Config:
        orm_mode = True

class AgriculturalInputOut(BaseModel):
    id: int
    nombre: str  # Nombre del insumo agrícola
    descripcion: Optional[str] = None  # Descripción opcional
    costo_unitario: Optional[float] = None  # Costo unitario
    precio_unitario_estimado: Optional[float] = None  # Precio estimado

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    nombre: str  # Nombre del usuario
    email: str  # Correo del usuario
    rol: Optional[str] = None  # Rol del usuario (opcional)

    class Config:
        orm_mode = True

class MachineryOut(BaseModel):
    id: int
    name: str  # Nombre de la maquinaria
    description: Optional[str] = None  # Descripción opcional
    costPerHour: float  # Costo por hora real
    estimatedCostPerHour: Optional[float] = None  # Costo por hora estimado

    class Config:
        orm_mode = True

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
    cantidad_insumo: Optional[int] = None
    maquinaria_agricola_id: Optional[int] = None


class TaskCreate(TaskBase):
    cultivo_id: int  # Mantén cultivo_id en los esquemas de creación y actualización
    pass


class TaskUpdate(BaseModel):
    fecha_estimada: Optional[date] = None
    fecha_realizacion: Optional[date] = None
    descripcion: Optional[str] = None
    estado_id: Optional[int] = None
    es_mecanizable: Optional[bool] = None
    cultivo_id: Optional[int] = None
    labor_cultural_id: Optional[int] = None
    insumo_agricola_id: Optional[int] = None
    usuario_id: Optional[int] = None
    cantidad_insumo: Optional[int] = None
    maquinaria_agricola_id: Optional[int] = None


class TaskOut(TaskBase):
    id: int
    cultivo: CropOut  # Relación con CropOut
    labor_cultural: LaborCulturalOut  # Relación con LaborCulturalOut
    insumo_agricola: Optional[AgriculturalInputOut] = None  # Relación con AgriculturalInputOut
    usuario: UserOut  # Relación con UserOut
    maquinaria_agricola: Optional[MachineryOut] = None  # Relación con MachineryOut


    class Config:
        orm_mode = True
