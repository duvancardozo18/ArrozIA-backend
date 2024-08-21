from fastapi import APIRouter, Depends
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
