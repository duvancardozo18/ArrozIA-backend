from pydantic import BaseModel


class UnidadAreaSchema(BaseModel):
    id: int
    unidad: str