from pydantic import BaseModel, Field
from datetime import date

class CropBase(BaseModel):
    cropName: str = Field(..., max_length=100)
    varietyId: int
    plotId: int
    plantingDate: date | None = None
    estimatedHarvestDate: date | None = None
    actualHarvestDate: date | None = None
    harvestedQuantity: float | None = None
    weightUnitId: int | None = None
    income: float | None = None

    class Config:
        from_attributes = True

class CropCreate(CropBase):
    pass

class CropUpdate(CropBase):
    pass

class CropOut(CropBase):
    id: int
