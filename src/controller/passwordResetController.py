from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.schemas.schemas import PasswordResetRequest, PasswordResetVerify, PasswordUpdate
from src.models.userModel import User
from src.models.passwordResetModel import PasswordReset
from src.helpers.utils import generate_password_reset_token, get_hashed_password, verify_password_reset_token
from src.database.database import get_session
from src.helpers.email_helper import send_email  # Asegúrate de que esta importación sea correcta
from fastapi.responses import HTMLResponse, RedirectResponse  # Importar RedirectResponse

def requestPasswordReset(request: PasswordResetRequest, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email does not exist")
    
    # Generar un token de restablecimiento de contraseña asociado al user_id
    token = generate_password_reset_token(user.id)
    
    # Crear un registro de restablecimiento de contraseña
    password_reset = PasswordReset(email=user.email, token=token)
    db.add(password_reset)
    db.commit()
    
    # Enviar un correo electrónico al usuario con el token de restablecimiento
    reset_link = f"http://localhost:5173/Reset_Password/{token}"  # Aquí puedes redirigir al frontend si tienes uno
    send_email(
        recipient=user.email,
        token=token,
        user_name=user.nombre  # Asumiendo que tienes un campo 'nombre' en tu modelo User
    )
    
    return {"message": "Password reset email sent successfully"}

def verifyPasswordReset(request: PasswordResetVerify, db: Session = Depends(get_session)):
    # Verificar si el token es válido
    token_data = verify_password_reset_token(request.token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    # Buscar el registro de restablecimiento de contraseña
    password_reset = db.query(PasswordReset).filter(PasswordReset.token == request.token).first()
    if not password_reset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password reset request not found")
    
    # Buscar al usuario
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {"message": "Token is valid", "user": user}

def updatePassword(token: str, password_data: PasswordUpdate, db: Session = Depends(get_session)):
    # Verificar si el token es válido
    token_data = verify_password_reset_token(token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    # Buscar al usuario asociado al token
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Actualizar la contraseña del usuario
    user.password = get_hashed_password(password_data.new_password)
    db.commit()

    # Eliminar el registro de restablecimiento de contraseña
    password_reset = db.query(PasswordReset).filter(PasswordReset.token == token).first()
    db.delete(password_reset)
    db.commit()
    
    return {"message": "Password updated successfully"}

# Función para manejar la ruta "/Reset_Password/{token}" y devolver una página HTML
def showResetPasswordPage(token: str):
    # Verificar si el token es válido
    token_data = verify_password_reset_token(token)
    if not token_data:
        # Si el token es inválido o ha expirado, redirigir al login
        return RedirectResponse(url="/login")
    # Si el token es válido, redirigir al frontend donde está implementado ResetPasswordForm
    reset_link = f"http://localhost:5173/Reset_Password/{token}"
    return RedirectResponse(url=reset_link)

