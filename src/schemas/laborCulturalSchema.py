from pydantic import BaseModel, condecimal
from typing import Optional

class LaborCulturalBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_hora_real: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    precio_hora_estimado: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    id_etapa_fenologica: Optional[int] = None  # Relación con otra tabla, puede ser None

class LaborCulturalCreate(LaborCulturalBase):
    pass  # Aquí puedes dejarlo así si todos los campos son opcionales en la creación

class LaborCulturalResponse(LaborCulturalBase):
    id: int  # Incluye el ID en la respuesta

    class Config:
        orm_mode = True  # Permite que Pydantic lea datos desde un modelo ORM

class LaborCulturalUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    precio_hora_real: Optional[float]
    precio_hora_estimado: Optional[float]
    id_etapa_fenologica: Optional[int]

    class Config:
        orm_mode = True