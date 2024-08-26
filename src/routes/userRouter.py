from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
import  src.schemas.schemas as schemas
from src.controller.userController import registerUser, changePassword, deleteUser, getUser, getUsers, login, updateUser, updatePassword
from src.database.database import get_session
#from src.helpers.auth_bearer import JWTBearer


USER_ROUTES = APIRouter()


@USER_ROUTES.post("/register")
def register(user: schemas.CrearUsuario, session: Session = Depends(get_session)):
    return registerUser(user, session)

@USER_ROUTES.post('/login' ,response_model=schemas.TokenSchema)
def loginRoute(request: schemas.RequestDetails, db: Session = Depends(get_session)):
    return login(request, db)



@USER_ROUTES.get('/users/getusers',)
#def listUsers(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
def listUsers( session: Session = Depends(get_session)):
    return getUsers(session)

@USER_ROUTES.get('/users/{user_id}', )
#def getUserId(user_id: int, dependencies=[Depends(JWTBearer())], db: Session = Depends(get_session)):
def getUserId(user_id: int, db: Session = Depends(get_session)):
    return getUser(user_id, db)



@USER_ROUTES.put('/users/update/{user_id}')
def modifyUser(user_id: int, user_update: schemas.UpdateUser, db: Session = Depends(get_session)):
    return updateUser(user_id, user_update, db)


@USER_ROUTES.delete('/users/delete/{user_id}')
def removeUser(user_id: int, db: Session = Depends(get_session)):
    return deleteUser(user_id, db)


@USER_ROUTES.post('/change-password/')
def changeUserPassword(request: schemas.ChangePassword, db: Session = Depends(get_session)):
    return changePassword(request, db)

@USER_ROUTES.put("/update_password/{user_id}")
def update_password(user_id: int, password_data: schemas.UpdatePassword, db: Session = Depends(get_session)):
   return updatePassword(user_id, password_data, db)