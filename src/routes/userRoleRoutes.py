from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.userRoleSchema import CreateUserRole, UpdateUserRole
from src.controller.userRoleController import (deleteUserRole, getUserRoleByUserId, registerUserRole, updateUserRole)
from src.database.database import get_session
from src.helpers.utils import get_current_user, verify_permission
from src.models.userRoleModel import UserRole

USER_ROLE_ROUTES = APIRouter()

@USER_ROLE_ROUTES.post("/user-roles/register", dependencies=[Depends(verify_permission("crear_usuario"))])
def register_user_role(user_role: CreateUserRole, session: Session = Depends(get_session)):
    return registerUserRole(user_role, session)

@USER_ROLE_ROUTES.get('/user-roles/user/{user_id}')
def get_user_role_by_user_id(user_id: int, db: Session = Depends(get_session)):
    return getUserRoleByUserId(user_id, db)


@USER_ROLE_ROUTES.get("/user-roles", dependencies=[Depends(verify_permission("crear_usuario"))])
async def get_user_roles(db: Session = Depends(get_session), current_user: UserRole = Depends(get_current_user)):
    roles = db.query(UserRole).all()
    return roles

@USER_ROLE_ROUTES.put('/user-roles/update/{role_id}', dependencies=[Depends(verify_permission("actualizar_usuario"))])
def modify_user_role(role_id: int, user_role_update: UpdateUserRole, db: Session = Depends(get_session)):
    return updateUserRole(role_id, user_role_update, db)

@USER_ROLE_ROUTES.delete('/user-roles/delete/{role_id}', dependencies=[Depends(verify_permission("eliminar_usuario"))])
def remove_user_role(role_id: int, db: Session = Depends(get_session)):
    return deleteUserRole(role_id, db)
