from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import src.models.userModel as userModel
import src.schemas.schemas as schemas
from src.database.database import Base, engine, get_session
from src.helpers.auth_bearer import JWTBearer
from src.helpers.utils import (create_access_token, create_refresh_token,
                               get_current_user, get_hashed_password,
                               verify_password)
from src.models.userModel import TokenTable, User
from src.schemas.schemas import LoginRequest


def registerUser(user: schemas.CrearUsuario, session: Session = Depends(get_session)):
    existingUser = session.query(userModel.User).filter_by(email=user.email).first()
    if existingUser:
        raise HTTPException(status_code=400, detail="Email already registered")

    encryptedPassword = get_hashed_password(user.password)

    newUser = userModel.User(
        nombre=user.nombre,
        apellido=user.apellido,
        email=user.email,
        password=encryptedPassword
    )
    
    session.add(newUser)
    session.commit()
    session.refresh(newUser)

    # Devolver el ID del usuario recién creado
    return {"id": newUser.id, "message": "user created successfully"}


def login(request: schemas.LoginRequest, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    if user.primer_login:
        # Responder con un mensaje de que se necesita cambiar la contraseña
        return JSONResponse(
            status_code=403,
            content={
                "message": "You need to change your password",
                "change_password_required": True,
                "access_token" : create_access_token(subject=user.id),
                "refresh_token" : create_refresh_token(subject=user.id)
            }
        )
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    tokenDb = TokenTable(
        user_id=user.id,
        access_toke=access_token,
        refresh_toke=refresh_token,
        status=True
    )
    db.add(tokenDb)
    db.commit()
    db.refresh(tokenDb)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def getUsers(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users

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
    user.primer_login = False
    db.commit()
    
    return {"message": "Password changed successfully"}