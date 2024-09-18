from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_session
import src.models.userModel as userModel
from src.models.userModel import User
from src.schemas.userShema import CrearUsuario, UpdateUser
from src.helpers.utils import (get_current_user, get_hashed_password)

def registerUser(user: CrearUsuario, session: Session = Depends(get_session)):
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


def getUsers(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users


def getUser(user_id: int, db: Session = Depends(get_session)):
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def updateUser(user_id: int, user_update: UpdateUser, db: Session = Depends(get_session)):
    user = db.query(userModel.User).filter(userModel.User.id == user_id).first()  # Cambiado userModel a userModel.User
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Actualizar solo los campos que se pasen en el body
    if user_update.nombre is not None:
        user.nombre = user_update.nombre
    if user_update.apellido is not None:
        user.apellido = user_update.apellido
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = get_hashed_password(user_update.password)  # Asegúrate de hash la contraseña
    if user_update.primer_login is not None:
        user.primer_login = user_update.primer_login
    # Guardar los cambios en la base de datos
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

