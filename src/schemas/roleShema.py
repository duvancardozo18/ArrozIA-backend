from typing import Optional, List  # Importar List para manejar listas de permisos
from pydantic import BaseModel

class RoleBase(BaseModel):
    nombre: str
    descripcion: str

class Role(RoleBase):
    id: int
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class RoleCreate(RoleBase):
    permisos: List[int]  # Lista de IDs de permisos para asociar al rol

class RoleUpdate(RoleBase):
    nombre: str = None
    descripcion: str = None



