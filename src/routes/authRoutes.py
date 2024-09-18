from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.authShema import LoginRequest, TokenSchema
from src.controller.authController import login, logout
from src.database.database import get_session

AUTH_ROUTES = APIRouter()

@AUTH_ROUTES.post('/login', response_model=TokenSchema)
def loginRoute(request: LoginRequest, db: Session = Depends(get_session)):
    return login(request, db)

@AUTH_ROUTES.post('/logout')
def logoutRoute(user_id: int, db: Session = Depends(get_session)):
    return logout(user_id, db)