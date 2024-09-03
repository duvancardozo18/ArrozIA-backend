from pydantic import BaseModel
from typing import Optional

class VariedadArrozCreate(BaseModel):
    nombre: str
    numero_registro_productor_ica: int
    siembra: Optional[str] = None
    caracteristicas_variedad: Optional[str] = None
    susceptibilidad_herbicidas: Optional[str] = None
    manejo_fitosanitario: Optional[str] = None
    fertilizacion_nutricion: Optional[str] = None
    cosecha: Optional[str] = None
    oferta_ambiental: Optional[str] = None
    recomendaciones_generales: Optional[str] = None

class VariedadArrozResponse(VariedadArrozCreate):
    id: int

    class Config:
        from_attributes = True  