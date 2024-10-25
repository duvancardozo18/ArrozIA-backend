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
        from_attributes = True

class CropCreate(CropBase): 
    cropName: str = Field(..., max_length=100)
    varietyId: int
    plotId: int
    plantingDate: date | None = None
    estimatedHarvestDate: date | None = None
    slug: str | None = None


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
        orm_mode = True
