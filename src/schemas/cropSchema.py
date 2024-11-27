from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class CropBase(BaseModel):
    cropName: str = Field(..., max_length=100)
    varietyId: int
    plotId: int
    plantingDate: Optional[date] = None
    estimatedHarvestDate: Optional[date] = None
    slug: str

    class Config:
        from_attributes = True  # Utiliza from_attributes para Pydantic v2

class CropCreate(CropBase):
    slug: Optional[str] = None  # Slug opcional al crear

class CropUpdate(CropBase):
    pass

# Aquí agregamos varietyName a CropOut
class CropOut(BaseModel):
    id: int
    cropName: str
    varietyId: int
    varietyName: Optional[str] = None  # Agregamos el campo varietyName
    plotId: int
    plantingDate: Optional[date] = None
    estimatedHarvestDate: Optional[date] = None

    class Config:
        from_attributes = True  # Asegúrate de que esté alineado con Pydantic v2
