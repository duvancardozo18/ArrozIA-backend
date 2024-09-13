from pydantic import BaseModel


class UserFarmRolSchema(BaseModel):
    usuario_id: int
    rol_id: int
    finca_id: int

    class Config:
        orm_mode = True
