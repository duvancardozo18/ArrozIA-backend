from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_session
import src.models.userModel as userModel
from src.models.userModel import User
from src.schemas.userShema import CrearUsuario, UpdateUser
from src.helpers.utils import (get_current_user, get_hashed_password)
import re

def registerUser(user: CrearUsuario, session: Session = Depends(get_session)):
    # Validate that required fields are not empty or only spaces
    if not user.nombre.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty or only spaces.")
    if not user.apellido.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name cannot be empty or only spaces.")
    if not user.email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email cannot be empty or only spaces.")
    if not user.password.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password cannot be empty or only spaces.")
    
    # Validate length constraints
    if len(user.nombre) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name must be at most 50 characters.")
    if len(user.apellido) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name must be at most 50 characters.")
    if len(user.email) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be at most 50 characters.")
    if len(user.password) > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at most 100 characters.")
    
    # Validate email contains '@'
    if "@" not in user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format. Email must contain '@'.")
    
    # Validate password contains at least one uppercase letter, one lowercase letter, one digit, and has at least 8 characters
    password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
    if not password_pattern.match(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, and a number."
        )
    
    # Validate that 'nombre' and 'apellido' do not contain special characters
    if not user.nombre.isalpha() or not user.apellido.isalpha():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name and last name must only contain letters."
        )
    
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
    # Validate that 'nombre' and 'apellido' contain only letters and spaces
    if user_update.nombre is not None:
        if not user_update.nombre.replace(" ", "").isalpha():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name must only contain letters and spaces.")
    if user_update.apellido is not None:
        if not user_update.apellido.replace(" ", "").isalpha():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name must only contain letters and spaces.")
    
    # Apply restrictions if user_update.nombre is provided
    if user_update.nombre is not None:
        user_update.nombre = user_update.nombre.strip()
        if len(user_update.nombre) == 0:
            user_update.nombre = None  # Treat as empty if only spaces
        if user_update.nombre is not None and len(user_update.nombre) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name must be at most 50 characters.")
    
    # Apply restrictions if user_update.apellido is provided
    if user_update.apellido is not None:
        user_update.apellido = user_update.apellido.strip()
        if len(user_update.apellido) == 0:
            user_update.apellido = None  # Treat as empty if only spaces
        if user_update.apellido is not None and len(user_update.apellido) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name must be at most 50 characters.")
    
    # Apply restrictions if user_update.email is provided
    if user_update.email is not None:
        user_update.email = user_update.email.strip()
        if len(user_update.email) == 0:
            user_update.email = None  # Treat as empty if only spaces
        if user_update.email is not None and len(user_update.email) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be at most 50 characters.")
        if "@" not in user_update.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must contain '@'.")

    # Validate password contains at least one uppercase letter, one lowercase letter, one digit, and has at least 8 characters
    if user_update.password is not None:
        password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
        if not password_pattern.match(user_update.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, and a number."
            )

        # Validate password length is at most 100 characters
        if len(user_update.password) > 100:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at most 100 characters.")


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

