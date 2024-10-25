from pydantic import BaseModel

class LaborCulturalBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class LaborCulturalCreate(LaborCulturalBase):
    pass

class LaborCulturalResponse(LaborCulturalBase):
    id: int  # Incluir el ID en la respuesta

    class Config:
        from_attributes = True

class LaborCulturalUpdate(LaborCulturalBase):
    pass
