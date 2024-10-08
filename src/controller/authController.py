from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.models.authModel import TokenTable
from src.models.userModel import User
from src.schemas.authShema import LoginRequest
from src.helpers.utils import (create_access_token, create_refresh_token, verify_password)
import re

def login(request: LoginRequest, db: Session = Depends(get_session)):
    # Validate email contains '@'
    if "@" not in request.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format. Email must contain '@'.")
    
    # Validate password contains at least one uppercase letter, one lowercase letter, one digit, and has at least 8 characters
    password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
    if not password_pattern.match(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, and a number."
        )
    
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    if user.primer_login:
        return JSONResponse(
            status_code=403,
            content={
                "message": "You need to change your password",
                "change_password_required": True,
                "access_token": create_access_token(subject=user.id),
                "refresh_token": create_refresh_token(subject=user.id)
            }
        )
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    tokenDb = TokenTable(
        user_id=user.id,
        access_toke=access_token,
        refresh_toke=refresh_token,
        status=True
    )
    db.add(tokenDb)
    db.commit()
    db.refresh(tokenDb)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def logout(user_id: int, db: Session = Depends(get_session)):
    token = db.query(TokenTable).filter(TokenTable.user_id == user_id, TokenTable.status == True).first()
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token not found or already logged out"
        )
    # Invalidar el token
    token.status = False
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Successfully logged out"}
    )