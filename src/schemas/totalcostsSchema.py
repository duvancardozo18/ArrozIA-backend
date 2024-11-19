from pydantic import BaseModel
from typing import List


class CostsData(BaseModel):
    concepto: str
    total: float


class TotalCostsResponse(BaseModel):
    costos: List[CostsData]



class OverallTotalResponse(BaseModel):
    total_general: float
