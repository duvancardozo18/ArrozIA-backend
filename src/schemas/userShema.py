from typing import Optional
from pydantic import BaseModel

class CrearUsuario(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str

class UpdateUser(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    primer_login: Optional[bool] = None