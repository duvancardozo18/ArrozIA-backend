from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.permissionController import remove_permission_from_role, add_permission_to_role
from src.database.database import get_session
from src.helpers.utils import  verify_permission
from src.models.rolModel import Rol  
from src.models.permissionModel import Permission 

ROL_PERMISSION_ROUTES = APIRouter()

# Ruta para consultar los permisos de un rol
@ROL_PERMISSION_ROUTES.get("/roles/{role_id}/permissions", dependencies=[Depends(verify_permission("ver_rol"))])
def get_role_permissions(role_id: int, db: Session = Depends(get_session)):
    role = db.query(Rol).filter(Rol.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = db.query(Permission).filter(Permission.roles.contains(role)).all()
    
    # Cambia role.name a role.nombre
    return {"role": role.nombre, "permissions": [permission.nombre for permission in permissions]}


# Ruta para eliminar un permiso de un rol
@ROL_PERMISSION_ROUTES.delete("/roles/{role_id}/permissions/{permission_id}", dependencies=[Depends(verify_permission("eliminar_rol"))])
def delete_role_permission(role_id: int, permission_id: int, db: Session = Depends(get_session)):
    return remove_permission_from_role(role_id, permission_id, db)


@ROL_PERMISSION_ROUTES.put("/roles/{role_id}/permissions/{permission_id}", dependencies=[Depends(verify_permission("actualizar_rol"))])
def update_role_permission(role_id: int, permission_id: int, db: Session = Depends(get_session)):
    role = db.query(Rol).filter(Rol.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    # Añadir el permiso al rol
    add_permission_to_role(role_id, permission_id, db)
    
    return {"message": f"Permission '{permission.nombre}' successfully added to role '{role.nombre}'"}
