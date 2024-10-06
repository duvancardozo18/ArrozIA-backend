from typing import Optional
from pydantic import BaseModel

class PermissionSchema(BaseModel):
    id: int
    nombre: str
    description: str = None

    class Config:
        from_attributes = True

class CreatePermission(BaseModel):
    name: str
    description: str = None

class UpdatePermission(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


