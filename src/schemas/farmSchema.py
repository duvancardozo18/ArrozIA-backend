from decimal import Decimal, InvalidOperation
from typing import Optional, Union

from pydantic import BaseModel, Field, validator

class FarmSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID de la finca")
    nombre: str
    ubicacion: str
    area_total: float
    latitud: Optional[Union[float, Decimal]] = None
    longitud: Optional[Union[float, Decimal]] = None
    ciudad: Optional[str] = None
    departamento: Optional[str] = None
    pais: Optional[str] = None
    slug: Optional[str] = None  # Agregar este campo


    @validator('area_total', pre=True, always=True)
    def validate_area_total(cls, value):
        if isinstance(value, str) and value.strip() == "":
            raise ValueError('El campo "area_total" no puede estar vacío.')
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError('El campo "area_total" debe ser un número válido.')
        return value

    @validator('latitud', pre=True, always=True)
    def validate_latitud(cls, value):
        if value is None:
            return None  # Permitir None
        if isinstance(value, str) and value.strip() == "":
            raise ValueError('El campo "latitud" no puede estar vacío.')
        try:
            latitud = Decimal(str(value))
            if latitud < Decimal('-90') or latitud > Decimal('90'):
                raise ValueError('El campo "latitud" debe estar entre -90 y 90.')
            return latitud
        except (TypeError, ValueError, InvalidOperation):
            raise ValueError('El campo "latitud" debe ser un número decimal válido.')

    @validator('longitud', pre=True, always=True)
    def validate_longitud(cls, value):
        if value is None:
            return None  # Permitir None
        if isinstance(value, str) and value.strip() == "":
            raise ValueError('El campo "longitud" no puede estar vacío.')
        try:
            longitud = Decimal(str(value))
            if longitud < Decimal('-180') or longitud > Decimal('180'):
                raise ValueError('El campo "longitud" debe estar entre -180 y 180.')
            return longitud
        except (TypeError, ValueError, InvalidOperation):
            raise ValueError('El campo "longitud" debe ser un número decimal válido.')

class FincaResponseSchema(FarmSchema):
    id: Optional[int] = Field(None, description="ID de la finca")

class UpdateFarmSchema(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    area_total: Optional[float] = None
    latitud: Optional[Union[float, Decimal]] = None
    longitud: Optional[Union[float, Decimal]] = None
    ciudad: Optional[str] = None  # Nuevo campo
    departamento: Optional[str] = None  # Nuevo campo
    pais: Optional[str] = None  # Nuevo campo

    @validator('area_total', pre=True, always=True)
    def validate_area_total_update(cls, value):
        if isinstance(value, str) and value.strip() == "":
            raise ValueError('El campo "area_total" no puede estar vacío.')
        if value is not None:
            try:
                value = float(value)
            except ValueError:
                raise ValueError('El campo "area_total" debe ser un número válido.')
        return value

    @validator('latitud', pre=True, always=True)
    def validate_latitud_update(cls, value):
        if value is None:
            return None  # Permitir None
        if isinstance(value, str) and value.strip() == "":
            raise ValueError('El campo "latitud" no puede estar vacío.')
        try:
            latitud = Decimal(str(value))
            if latitud < Decimal('-90') or latitud > Decimal('90'):
                raise ValueError('El campo "latitud" debe estar entre -90 y 90.')
            return latitud
        except (TypeError, ValueError, InvalidOperation):
            raise ValueError('El campo "latitud" debe ser un número decimal válido.')

    @validator('longitud', pre=True, always=True)
    def validate_longitud_update(cls, value):
        if value is None:
            return None  # Permitir None
        if isinstance(value, str) and value.strip() == "":
            raise ValueError('El campo "longitud" no puede estar vacío.')
        try:
            longitud = Decimal(str(value))
            if longitud < Decimal('-180') or longitud > Decimal('180'):
                raise ValueError('El campo "longitud" debe estar entre -180 y 180.')
            return longitud
        except (TypeError, ValueError, InvalidOperation):
            raise ValueError('El campo "longitud" debe ser un número decimal válido.')
