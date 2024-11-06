from pydantic import BaseModel
from typing import Optional

class CreateUserRole(BaseModel):
    usuario_id: int
    rol_id: int

    class Config:
        orm_mode = True

class UpdateUserRole(BaseModel):
    usuario_id: int
    rol_id: int

    class Config:
        orm_mode = True

class AdminStatus(BaseModel):
    is_admin: bool
