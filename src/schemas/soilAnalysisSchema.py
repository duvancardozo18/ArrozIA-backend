from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class SoilAnalysisBase(BaseModel):
    fecha_analisis: date
    lote_id: int
    tipo_suelo_id: int
    archivo_reporte: Optional[bytes] = None

class SoilAnalysisCreate(SoilAnalysisBase):
    pass

class SoilAnalysisUpdate(SoilAnalysisBase):
    pass

class SoilAnalysisOut(SoilAnalysisBase):
    id: int

    class Config:
        orm_mode = True
