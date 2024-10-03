from pydantic import BaseModel
from typing import Optional


class CreateUserRole(BaseModel):
    usuario_id: int
    rol_id: int

    class Config:
        orm_mode = True


class UpdateUserRole(BaseModel):
    rol_id: Optional[int]

    class Config:
        orm_mode = True
