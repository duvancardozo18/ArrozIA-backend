from sqlalchemy.orm import Session
from src.models.userFarmRoleModel import UserFarmRole  # Importa el modelo UserFarmRole
from src.schemas.userFarmRoleSchema import UserFarmRoleCreate, UserFarmRoleShema  # Importa el esquema de creación

# Función para crear un registro UserFarmRole
def create_user_farm(user_farm: UserFarmRoleCreate, db: Session):
    new_user_farm = UserFarmRole(usuario_id=user_farm.usuario_id, finca_id=user_farm.finca_id, rol_id=user_farm.rol_id)
    db.add(new_user_farm)
    db.commit()
    db.refresh(new_user_farm)
    return new_user_farm

# Función para obtener todos los registros de UserFarmRole
def get_all_user_farms(db: Session):
    return db.query(UserFarmRole).all()

# Función para obtener un registro específico por user_id y finca_id
def get_user_farm(user_id: int, finca_id: int, db: Session):
    return db.query(UserFarmRole).filter(UserFarmRole.usuario_id == user_id, UserFarmRole.finca_id == finca_id).first()
# Función para actualizar un registro UserFarmRole
def update_user_farm(usuario_id: int, finca_id: int, rol_id: int, db: Session):
    try:
        user_farm = db.query(UserFarmRole).filter(UserFarmRole.usuario_id == usuario_id, UserFarmRole.finca_id == finca_id).first()
        if not user_farm:
            return None  
        user_farm.rol_id = rol_id
        db.commit()
        db.refresh(user_farm)  
        return user_farm  
    except Exception as e:
        db.rollback()  
        raise e  


# Función para eliminar un registro UserFarmRole
def delete_user_farm(usuario_id: int, finca_id: int, db: Session):
    user_farm = db.query(UserFarmRole).filter(UserFarmRole.usuario_id == usuario_id, UserFarmRole.finca_id == finca_id).first()
    if not user_farm:
        return None
    db.delete(user_farm)
    db.commit()
    return True
