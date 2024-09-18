import datetime
from typing import Optional, List  # Importar List para manejar listas de permisos

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
 
class CreatePermission(BaseModel):
    name: str
    description: str = None

class UpdatePermission(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionSchema(BaseModel):
    id: int
    nombre: str
    description: str = None

    class Config:
        from_attributes = True



class RoleBase(BaseModel):
    nombre: str
    descripcion: str

# Esquema para crear un nuevo rol, incluyendo los permisos
class RoleCreate(RoleBase):
    permisos: List[int]  # Lista de IDs de permisos para asociar al rol

class RoleUpdate(RoleBase):
    nombre: str = None
    descripcion: str = None

class Role(RoleBase):
    id: int
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

