import datetime
from typing import Optional, List  # Importar List para manejar listas de permisos

from pydantic import BaseModel


class CrearUsuario(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ChangePasswordResponse(BaseModel):
    message: str
    change_password_required: bool
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True

class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str

class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime

class UpdateUser(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
 
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

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetVerify(BaseModel):
    email: str
    token: str
    new_password: str

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

class PasswordUpdate(BaseModel):
    new_password: str