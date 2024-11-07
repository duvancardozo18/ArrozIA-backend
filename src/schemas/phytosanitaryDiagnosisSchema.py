from datetime import date
from typing import Optional

from pydantic import BaseModel


class DiagnosticoFitosanitarioBase(BaseModel):
    resultado_ia: str
    ruta: str
    cultivo_id: int
    fecha_diagnostico: date
    confianza_promedio: Optional[float] = None
    tipo_problema: Optional[str] = None
    imagenes_analizadas: Optional[int] = None
    exportado: Optional[bool] = False
    comparacion_diagnostico: Optional[str] = None

class DiagnosticoFitosanitarioCreate(DiagnosticoFitosanitarioBase):
    pass

class DiagnosticoFitosanitarioUpdate(DiagnosticoFitosanitarioBase):
    pass

class CultivoInfo(BaseModel):
    id: int
    cropName: str  # Nombre del cultivo en el esquema de salida

    class Config:
        orm_mode = True

class DiagnosticoFitosanitarioOut(BaseModel):
    id: int
    resultado_ia: str
    ruta: str
    cultivo_id: int
    fecha_diagnostico: date
    confianza_promedio: Optional[float] = None
    tipo_problema: Optional[str] = None
    imagenes_analizadas: Optional[int] = None
    exportado: Optional[bool] = False
    comparacion_diagnostico: Optional[str] = None
    cultivo: CultivoInfo  # Incluye datos de la relación con el cultivo

    class Config:
        orm_mode = True