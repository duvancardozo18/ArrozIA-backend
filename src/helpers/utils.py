import os
import uuid
from datetime import datetime, timedelta
from typing import Union, Any
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.models.userModel import User
from src.models.rolModel import UsuarioFincaRol, Rol
from src.models.permissionModel import Permission, RolPermiso
from src.helpers.auth_bearer import JWTBearer
from src.helpers.config import (
    JWT_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
)

# Contraseñas
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return passwordContext.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return passwordContext.verify(password, hashed_pass)


# Actualización para generar token asociado a un usuario específico
def generate_password_reset_token(user_id: int) -> str:
    expiration = datetime.utcnow() + timedelta(hours=1)  # El token será válido por 1 hora
    token_data = {"user_id": user_id, "exp": expiration.timestamp()}
    return jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)

# Función para verificar el token de restablecimiento de contraseña
def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if user_id is None:
            return None
        
        expiration = payload.get("exp")
        if datetime.utcnow() > datetime.utcfromtimestamp(expiration):
            return None
        
        return payload  # Retorna los datos del token si es válido
    except JWTError:
        return None


def send_password_reset_email(email: str, token: str):
    print(f"Se ha enviado un correo electrónico a {email} con el token de restablecimiento de contraseña: {token}")


# Tokens
def create_access_token(subject: Union[str, Any], expiresDelta: int = None) -> str:
    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encodedJwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt


def create_refresh_token(subject: Union[str, Any], expiresDelta: int = None) -> str:
    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    toEncode = {"exp": expire, "sub": str(subject)}
    encodedJwt = jwt.encode(toEncode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt


# Obtiene el usuario actual autenticado utilizando el token JWT
def get_current_user(token: str = Depends(JWTBearer()), db: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )
    
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


# Permisos
def verify_permission(permission_name: str):
    # Verifica si el usuario actual tiene el permiso necesario.
    def verify(user: User = Depends(get_current_user), db: Session = Depends(get_session)):
        # Obtener todos los roles del usuario
        user_roles = db.query(UsuarioFincaRol).filter(UsuarioFincaRol.usuario_id == user.id).all()
        
        # Verificar si se encontraron roles para el usuario
        if not user_roles:
            print(f"Usuario {user.id} no tiene roles asociados.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have any roles")

        print(f"Roles encontrados para el usuario {user.id}: {user_roles}")

        # Iterar sobre cada rol del usuario
        for user_role in user_roles:
            # Obtener todos los permisos asociados al rol
            role_permissions = db.query(RolPermiso).filter(RolPermiso.rol_id == user_role.rol_id).all()
            print(f"Permisos encontrados para el rol {user_role.rol_id}: {role_permissions}")
            
            # Verificar cada permiso asociado con el rol
            for role_permission in role_permissions:
                permission = db.query(Permission).filter(Permission.id == role_permission.permiso_id).first()
                # Si se encuentra el permiso requerido, permitir el acceso
                if permission and permission.nombre == permission_name:
                    print(f"Permiso '{permission_name}' encontrado para el usuario {user.id}")
                    return
        
        # Si después de iterar no se encontró el permiso, denegar el acceso
        print(f"Permiso '{permission_name}' no encontrado para el usuario {user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return verify
