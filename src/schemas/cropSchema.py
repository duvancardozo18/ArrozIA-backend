from pydantic import BaseModel, Field
from datetime import date

class CropBase(BaseModel):
    cropName: str = Field(..., max_length=100)
    varietyId: int
    plotId: int
    plantingDate: date | None = None
    estimatedHarvestDate: date | None = None
    slug: str

    class Config:
        from_attributes = True  # Utiliza from_attributes para Pydantic v2

class CropCreate(CropBase):
    slug: str | None = None  # Slug opcional al crear

class CropUpdate(CropBase):
    pass

class CropOut(BaseModel):
    id: int
    cropName: str
    varietyId: int
    plotId: int
    plantingDate: date | None = None
    estimatedHarvestDate: date | None = None

    class Config:
        from_attributes = True  # Asegúrate de que esté alineado con Pydantic v2
