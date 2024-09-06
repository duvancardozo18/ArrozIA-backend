from pydantic import BaseModel 
import datetime
from typing import Optional

class CrearUsuario(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True

class ChangePassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime.datetime

class UpdateUser(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class CreatePermission(BaseModel):
    name: str
    description: str = None

class UpdatePermission(BaseModel):
    name: str = None
    description: str = None


class PermissionSchema(BaseModel):
    id: int
    name: str
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

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    nombre: str = None
    descripcion: str = None

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True