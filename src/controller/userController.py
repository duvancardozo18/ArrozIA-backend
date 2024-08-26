from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import src.schemas.schemas as schemas
import src.models.userModel as userModel
from src.helpers.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password
from src.database.database import Base, get_session, engine
from src.models.userModel import User, TokenTable
#from src.helpers.auth_bearer import JWTBearer

def registerUser(user: schemas.CrearUsuario, session: Session = Depends(get_session)):
    existingUser = session.query(userModel.User).filter_by(email=user.email).first()
    if existingUser:
        raise HTTPException(status_code=400, detail="Email already registered")

    encryptedPassword = get_hashed_password(user.password)

    newUser = userModel.User(nombre=user.nombre, apellido=user.apellido, email=user.email, password=encryptedPassword )
    

    session.add(newUser)
    session.commit()
    session.refresh(newUser)

    return {"message":"user created successfully"}

def login(request: schemas.RequestDetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashedPass = user.password
    if not verify_password(request.password, hashedPass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    if user.primer_login:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Please update your password", 
                     "redirect": "/update_password",
                     "usuario_id": user.id}
        )
    
    
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    tokenDb = userModel.TokenTable(user_id=user.id,  access_toke=access,  refresh_toke=refresh, status=True)
    db.add(tokenDb)
    db.commit()
    db.refresh(tokenDb)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }
#def getUsers( dependencies=Depends(JWTBearer()),session: Session = Depends(get_session)):
def getUsers(session: Session = Depends(get_session)):
    user = session.query(userModel.User).all()
    return user

def getUser(user_id: int, db: Session = Depends(get_session)):
#def getUser(user_id: int, dependencies=[Depends(JWTBearer())], db: Session = Depends(get_session)):
    # Buscar el usuario en la base de datos
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



def updateUser(user_id: int, user_update: schemas.UpdateUser, db: Session = Depends(get_session)):
    # Buscar el usuario en la base de datos
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Actualizar la información del usuario solo si se proporciona un nuevo valor
    if user_update.nombre is not None:
        user.nombre = user_update.nombre
    if user_update.apellido is not None:
        user.apellido = user_update.apellido
    if user_update.email is not None:
        # Verificar si el nuevo email ya está registrado
        existing_user = db.query(userModel.User).filter(userModel.User.email == user_update.email).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user.email = user_update.email  

    if user_update.password is not None:
        user.password = get_hashed_password(user_update.password)
    
    db.commit()
    db.refresh(user)
    
    return {"message": "User updated successfully", "user": user}

def deleteUser(user_id: int, db: Session = Depends(get_session)):
    # Buscar el usuario en la base de datos
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Eliminar el usuario de la base de datos
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully", "status": status.HTTP_200_OK}


def changePassword(request: schemas.ChangePassword, db: Session = Depends(get_session)):
    user = db.query(userModel.User).filter(userModel.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encryptedPassword = get_hashed_password(request.new_password)
    user.password = encryptedPassword
    db.commit()
    
    return {"message": "Password changed successfully"}


def updatePassword(user_id: int, password_data: schemas.UpdatePassword, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail='las contraseñas no coinciden')

    if user.primer_login:
        print(password_data.new_password)
        user.password = get_hashed_password(password_data.new_password)
        user.primer_login = False
        db.commit()
        db.refresh(user)
        return {"message": "Password updated successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password update not allowed")

# if user.primer_login:
#         temporalToken = create_access_token(data = {'sub': user.email, "primer_login": True})
#         return { 'access_token': temporalToken, 'token_type': 'bearer', 'redirect_to': '/update-password'  }