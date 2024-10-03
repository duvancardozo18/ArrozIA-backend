from sqlalchemy.orm import Session
from src.models.userRoleModel import UserRole
from src.schemas.userRoleSchema import CreateUserRole, UpdateUserRole

# Register a new user role
def registerUserRole(user_role: CreateUserRole, db: Session):
    new_user_role = UserRole(usuario_id=user_role.usuario_id, rol_id=user_role.rol_id)
    db.add(new_user_role)
    db.commit()
    db.refresh(new_user_role)
    return new_user_role


# Get a user role by ID
def getUserRoleByUserId(user_id: int, db: Session):
    print(f"Looking for user role with user_id: {user_id}")
    user_role = db.query(UserRole).filter(UserRole.usuario_id == user_id).first()
    print(f"Found user role: {user_role}")
    if not user_role:
        return {"error": f"User role with user_id {user_id} not found"}, 404
    return user_role


# Update an existing user role
def updateUserRole(rol_id: int, user_role_update: UpdateUserRole, db: Session):
    user_role = db.query(UserRole).filter(UserRole.id == rol_id).first()
    if user_role:
        if user_role_update.rol_id is not None:
            user_role.rol_id = user_role_update.rol_id
        db.commit()
        db.refresh(user_role)
    return user_role

# Delete a user role
def deleteUserRole(rol_id: int, db: Session):
    user_role = db.query(UserRole).filter(UserRole.id == rol_id).first()
    if user_role:
        db.delete(user_role)
        db.commit()
    return {"message": "User role deleted successfully"}
