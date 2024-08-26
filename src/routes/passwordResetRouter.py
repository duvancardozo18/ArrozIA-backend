from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.passwordResetController import requestPasswordReset, verifyPasswordReset
from src.schemas.schemas import PasswordResetRequest, PasswordResetVerify
from src.database.database import get_session

PASSWORD_RESET_ROUTES = APIRouter()

@PASSWORD_RESET_ROUTES.post("/password-reset/request")
def requestPasswordResetRoute(request: PasswordResetRequest, session: Session = Depends(get_session)):
    return requestPasswordReset(request, session)

@PASSWORD_RESET_ROUTES.post("/password-reset/verify")
def verifyPasswordResetRoute(request: PasswordResetVerify, session: Session = Depends(get_session)):
    return verifyPasswordReset(request, session)

@PASSWORD_RESET_ROUTES.get("/Reset_Password/{token}")
def reset_password(token: str):
    # Aquí simplemente puedes devolver un JSON indicando que el token se recibió
    return {"message": "Token received", "token": token}
