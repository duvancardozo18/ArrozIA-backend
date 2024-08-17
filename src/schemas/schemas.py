from pydantic import BaseModel 
import datetime

class CrearUsuario(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str

class requestdetails(BaseModel):
    email:str
    password:str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
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
    nombre: str
    apellido: str
    email: str

# Clases para permisos

class PermissionBase(BaseModel):
    name: str  # El nombre del permiso

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    role_id: int

    class Config:
        orm_mode = True

#Clases temporales para Rol -------------------------------------------------

        from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True
