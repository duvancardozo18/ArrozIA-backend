from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from src.controller.passwordResetController import requestPasswordReset, verifyPasswordReset, updatePassword, showResetPasswordPage
from src.schemas.schemas import PasswordResetRequest, PasswordResetVerify, PasswordUpdate
from src.database.database import get_session


PASSWORD_RESET_ROUTES = APIRouter()

@PASSWORD_RESET_ROUTES.post("/password-reset/request")
def requestPasswordResetRoute(request: PasswordResetRequest, session: Session = Depends(get_session)):
    return requestPasswordReset(request, session)

@PASSWORD_RESET_ROUTES.post("/password-reset/verify")
def verifyPasswordResetRoute(request: PasswordResetVerify, session: Session = Depends(get_session)):
    return verifyPasswordReset(request, session)

@PASSWORD_RESET_ROUTES.post("/password-reset/update")
def updatePasswordRoute(token: str = Form(...), new_password: str = Form(...), session: Session = Depends(get_session)):
    return updatePassword(token, PasswordUpdate(new_password=new_password), session)

# La ruta que se maneja cuando el usuario hace clic en el enlace del correo
@PASSWORD_RESET_ROUTES.get("/Reset_Password/{token}", response_class=HTMLResponse)
def resetPasswordPageRoute(token: str):
    return showResetPasswordPage(token)
