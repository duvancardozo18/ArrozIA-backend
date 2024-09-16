from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.models.userFarmRoleModel import UserFarmRole  # Importa el modelo UserFarmRole
from src.schemas.userFarmRoleSchema import UserFarmRoleCreate, UserFarmRoleShema, UserFarmRoleUpdate  # Importa el esquema

# Función para crear un registro UserFarmRole
def create_user_farm(user_farm: UserFarmRoleCreate, db: Session):
    new_user_farm = UserFarmRole(
        usuario_id=user_farm.usuario_id, 
        finca_id=user_farm.finca_id, 
        rol_id=user_farm.rol_id
    )
    db.add(new_user_farm)
    db.commit()
    db.refresh(new_user_farm)
    return new_user_farm

# Función para obtener un rol de usuario por ID
def getUserFarmRolById(user_id: int, session: Session):
    farmUserRol = session.query(UserFarmRole).filter(UserFarmRole.usuario_id == user_id).first()
    if not farmUserRol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hay usuario con id {user_id}"
        )
    return farmUserRol

# Función para actualizar un registro UserFarmRole
def update_user_farm_role_by_id(user_id: int, updated_data: UserFarmRoleUpdate, session: Session):
    farmUserRol = session.query(UserFarmRole).filter(UserFarmRole.usuario_id == user_id).first()
    
    if not farmUserRol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hay usuario con id {user_id}"
        )
    
    # Actualizar los campos con la nueva información
    farmUserRol.rol_id = updated_data.rol_id
    farmUserRol.finca_id = updated_data.finca_id

    # Guardar los cambios en la base de datos
    session.commit()
    session.refresh(farmUserRol)

    return farmUserRol

# Función para obtener todos los registros de UserFarmRole
def get_all_user_farms(db: Session):
    return db.query(UserFarmRole).all()

# Función para eliminar un registro UserFarmRole
def delete_user_farm(usuario_id: int, finca_id: int, db: Session):
    user_farm = db.query(UserFarmRole).filter(
        UserFarmRole.usuario_id == usuario_id, 
        UserFarmRole.finca_id == finca_id
    ).first()
    
    if not user_farm:
        return None
    
    db.delete(user_farm)
    db.commit()
    return True
