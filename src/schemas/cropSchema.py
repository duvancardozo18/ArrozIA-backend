from pydantic import BaseModel, Field
from datetime import date

class CropBase(BaseModel):
    cropName: str = Field(..., max_length=100)
    varietyId: int
    plotId: int
    plantingDate: date | None = None
    estimatedHarvestDate: date | None = None
   
  

    class Config:
        from_attributes = True

class CropCreate(CropBase): 
    pass

class CropUpdate(CropBase):
    pass

class CropOut(BaseModel):
    id: int
    cropName: str
    varietyId: int
    varietyName: str  # Asegúrate de incluir el nombre de la variedad de arroz
    plotId: int
    plotName: str      # Asegúrate de incluir el nombre del lote
    plantingDate: date | None = None
    estimatedHarvestDate: date | None = None

    class Config:
        orm_mode = True
