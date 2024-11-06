from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


#Esquema de Listar
class UserFarmRoleShema(BaseModel):
    usuario_id: int
    finca_id: int
    farm_name: Optional[str] = None
    

    class Config:
        orm_mode = True

# Esquema de Crear
class UserFarmRoleCreate(BaseModel):
    usuario_id: int
    finca_id: int
    
    class Config:
        orm_mode = True


# Esquema de Actualizar
class UserFarmRoleUpdate(BaseModel):
    usuario_id: Optional[int] = None  
    finca_id: Optional[int] = None    
   
    class Config:
        orm_mode = True



class AssignFarmRequest(BaseModel):
    farm_id: int

class FarmSchema(BaseModel):
    id: int
    nombre: str
    # Agrega otros campos de la finca si los necesitas

    class Config:
        orm_mode = True