from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.rolModel import UsuarioFincaRol, Rol
from src.models.permissionModel import Permiso, RolPermiso 

def check_permission(user_id: int, permission_name: str, db: Session):
    # Obtener los roles del usuario desde la tabla usuario_finca
    user_roles = db.query(UsuarioFincaRol).filter(UsuarioFincaRol.usuario_id == user_id).all()

    if not user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have any roles"
        )

    for user_role in user_roles:
        role = db.query(Rol).filter(Rol.id == user_role.rol_id).first()
        if not role:
            continue
        
        permission = db.query(Permiso).join(RolPermiso).filter(
            RolPermiso.rol_id == role.id,
            Permiso.nombre == permission_name
        ).first()

        if permission:
            return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions"
    )
