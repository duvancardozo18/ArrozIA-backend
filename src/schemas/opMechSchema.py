from pydantic import BaseModel
from typing import Optional


class OpMechBase(BaseModel):
    taskId: int
    mechanizationName: str
    machineryId: int
    hoursUsed: float



class OpMechCreate(BaseModel):
    taskId: int
    mechanizationName: str
    machineryId: int
    hoursUsed: float


class OpMechUpdate(OpMechBase):
    pass


class OpMech(OpMechBase):
    id: int

    class Config:
        orm_mode = True
