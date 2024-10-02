from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


#Esquema de Listar
class UserFarmRoleShema(BaseModel):
    usuario_id: int
    finca_id: int
    # rol_id: int

    class Config:
        orm_mode = True

# Esquema de Crear
class UserFarmRoleCreate(BaseModel):
    usuario_id: int
    finca_id: int
    # rol_id: int

    class Config:
        orm_mode = True


# Esquema de Actualizar
class UserFarmRoleUpdate(BaseModel):
    usuario_id: Optional[int] = None  
    finca_id: Optional[int] = None    
    # rol_id: Optional[int] = None 

    class Config:
        orm_mode = True



