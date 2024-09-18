from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.userShema import CrearUsuario, UpdateUser
from src.controller.userController import (deleteUser, getUser, registerUser, updateUser)
from src.database.database import get_session
from src.helpers.utils import get_current_user, verify_permission
from src.models.userModel import User

USER_ROUTES = APIRouter()

@USER_ROUTES.post("/users/register", dependencies=[Depends(verify_permission("crear_usuario"))])
def register(user: CrearUsuario, session: Session = Depends(get_session)):
    return registerUser(user, session)

@USER_ROUTES.get('/users/{user_id}', dependencies=[Depends(verify_permission("ver_usuario"))])
def getUserId(user_id: int, db: Session = Depends(get_session)):
    return getUser(user_id, db)

@USER_ROUTES.get("/users", dependencies=[Depends(verify_permission("ver_usuarios"))])
async def get_users(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users

@USER_ROUTES.put('/users/update/{user_id}', dependencies=[Depends(verify_permission("actualizar_usuario"))])
def modifyUser(user_id: int, user_update: UpdateUser, db: Session = Depends(get_session)):
    return updateUser(user_id, user_update, db)

@USER_ROUTES.delete('/users/delete/{user_id}', dependencies=[Depends(verify_permission("eliminar_usuario"))])
def removeUser(user_id: int, db: Session = Depends(get_session)):
    return deleteUser(user_id, db)

