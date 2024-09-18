from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from src.controller.passwordResetController import changePassword, requestPasswordReset, updatePassword, showResetPasswordPage
from src.schemas.passwordShema import ChangePassword, PasswordResetRequest, PasswordUpdate
from src.database.database import get_session
from src.helpers.utils import verify_password_reset_token

PASSWORD_RESET_ROUTES = APIRouter()

# Cambio de contraseña
@PASSWORD_RESET_ROUTES.post('/change-password')
def changeUserPassword(request: ChangePassword, db: Session = Depends(get_session)):
    return changePassword(request, db)

# RECUPERACION
# Enviar token de recuperacion al email
@PASSWORD_RESET_ROUTES.post("/password-reset/request")
def requestPasswordResetRoute(request: PasswordResetRequest, session: Session = Depends(get_session)):
    return requestPasswordReset(request, session)

# Valida el token de recuperacion existente
@PASSWORD_RESET_ROUTES.get("/Reset_Password/{token}", response_class=HTMLResponse)
def reset_password_page_route(token: str):
    # Verificamos el token antes de mostrar la página
    token_data = verify_password_reset_token(token)
    if token_data is None:
        # Si el token no es válido o ha expirado, lanzamos una excepción
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    # Si el token es válido, mostramos la página de restablecimiento
    return showResetPasswordPage(token)

# Actulizar contraseña
@PASSWORD_RESET_ROUTES.post("/password-reset/update")
def updatePasswordRoute(token: str = Form(...), new_password: str = Form(...), session: Session = Depends(get_session)):
    return updatePassword(token, PasswordUpdate(new_password=new_password), session)



