from pydantic import BaseModel
from datetime import date

class CropCycleRequest(BaseModel):
    sowingDate: date

class CropCycleStageResponse(BaseModel):
    stage: str
    startDate: date
    endDate: date
