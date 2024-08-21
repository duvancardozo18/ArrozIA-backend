from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.schemas.schemas import PasswordResetRequest, PasswordResetVerify
from src.models.userModel import User
from src.models.passwordResetModel import PasswordReset
from src.helpers.utils import generate_password_reset_token, send_password_reset_email, get_hashed_password
from src.database.database import get_session

def requestPasswordReset(request: PasswordResetRequest, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email does not exist")
    
    # Generar un token de restablecimiento de contraseña
    token = generate_password_reset_token()
    
    # Crear un registro de restablecimiento de contraseña
    password_reset = PasswordReset(email=user.email, token=token)
    db.add(password_reset)
    db.commit()
    
    # Enviar un correo electrónico al usuario con el token de restablecimiento
    send_password_reset_email(user.email, token)
    
    return {"message": "Password reset email sent successfully"}

def verifyPasswordReset(request: PasswordResetVerify, db: Session = Depends(get_session)):
    password_reset = db.query(PasswordReset).filter(PasswordReset.email == request.email, PasswordReset.token == request.token).first()
    if not password_reset or password_reset.is_token_expired():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Actualizar la contraseña del usuario
    user.password = get_hashed_password(request.new_password)
    db.commit()
    
    # Eliminar el token de restablecimiento de contraseña
    db.delete(password_reset)
    db.commit()
    
    return {"message": "Password has been reset successfully"}
