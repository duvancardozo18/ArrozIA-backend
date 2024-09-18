from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.rolModel import Rol
from src.models.permissionModel import RolPermiso  
from src.schemas.roleShema import RoleCreate, RoleUpdate, Role

# Crear un nuevo rol y asociar permisos
def create_role(role: RoleCreate, db: Session):
    # Crear el nuevo rol
    new_role = Rol(nombre=role.nombre, descripcion=role.descripcion)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)  
    # Asociar permisos al rol en la tabla de relación rol-permiso
    if role.permisos:  # Verificar si se proporcionaron permisos
        for permiso_id in role.permisos:
            role_permission = RolPermiso(rol_id=new_role.id, permiso_id=permiso_id)
            db.add(role_permission)
        db.commit()  # Hacer commit para guardar la relación
    return {"message": "Role created successfully", "role_id": new_role.id}  # Devolver también el ID del nuevo rol


# Obtener todos los roles
def get_roles(db: Session):
    roles = db.query(Rol).all()
    return {"message": f"{len(roles)} roles found", "roles": roles}


# Obtener un rol por ID
def get_role_by_id(role_id: int, db: Session):
    role = db.query(Rol).filter(Rol.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return {"message": "Role found", "role": Role.from_orm(role)}


# Actualizar un rol por ID
def update_role(role_id: int, role_update: RoleUpdate, db: Session):
    role = db.query(Rol).filter(Rol.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    role.nombre = role_update.nombre if role_update.nombre is not None else role.nombre
    role.descripcion = role_update.descripcion if role_update.descripcion is not None else role.descripcion
    db.commit()
    return {"message": "Role updated successfully"}


# Eliminar un rol por ID
def delete_role(role_id: int, db: Session):
    role = db.query(Rol).filter(Rol.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}