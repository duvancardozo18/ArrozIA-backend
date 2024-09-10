from decimal import Decimal

from pydantic import BaseModel


class FarmSchema(BaseModel):
    nombre: str
    ubicacion: str
    area_total: float
    latitud: Decimal
    longitud: Decimal