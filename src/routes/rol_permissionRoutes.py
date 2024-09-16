from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.permissionController import check_permission
from src.database.database import get_session 
from src.models.rolModel import Rol  # Asumiendo que tienes un modelo para Roles
from src.models.permissionModel import Permission  # Asumiendo que tienes un modelo para Permisos

ROL_PERMISSION_ROUTES = APIRouter()

# Ruta para consultar los permisos de un rol
@ROL_PERMISSION_ROUTES.get("/roles/{role_id}/permissions")
def get_role_permissions(role_id: int, db: Session = Depends(get_session)):
    role = db.query(Rol).filter(Rol.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = db.query(Permission).filter(Permission.roles.contains(role)).all()
    
    # Cambia role.name a role.nombre
    return {"role": role.nombre, "permissions": [permission.nombre for permission in permissions]}

