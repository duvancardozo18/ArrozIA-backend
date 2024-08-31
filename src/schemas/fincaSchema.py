from decimal import Decimal

from pydantic import BaseModel


class FincaSchema(BaseModel):
    nombre: str
    ubicacion: str
    area_total: float
    latitud: Decimal
    longitud: Decimal