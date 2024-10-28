from pydantic import BaseModel

class Machinery(BaseModel):
    id: int
    name: str  # Incluir el nombre de la maquinaria

    class Config:
        orm_mode = True

class OpMechBase(BaseModel):
    taskId: int
    mechanizationName: str
    machineryId: int
    hoursUsed: float

class OpMechCreate(OpMechBase):
    pass

class OpMechUpdate(OpMechBase):
    pass

class OpMech(OpMechBase):
    id: int

    class Config:
        orm_mode = True


class OpMechResponse(BaseModel):
    id: int
    taskId: int
    mechanizationName: str
    machineryId: int
    hoursUsed: float
    machinery: Machinery  # Relación para obtener el name de la maquinaria

    class Config:
        orm_mode = True