from pydantic import BaseModel

class FarmLotSchema(BaseModel):
    id: int
    nombre: str
    area: float
    latitud: float
    longitud: float

    class Config:
        orm_mode = True
