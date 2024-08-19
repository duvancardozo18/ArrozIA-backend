import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return passwordContext.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return passwordContext.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any], expiresDelta: int = None) -> str:
    if expiresDelta is not None:
        expiresDelta = datetime.utcnow() + expiresDelta
        
    else:
        expiresDelta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
         
    
    to_encode = {"exp": expiresDelta, "sub": str(subject)}
    encodedJwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
    return encodedJwt

def create_refresh_token(subject: Union[str, Any], expiresDelta: int = None) -> str:
    if expiresDelta is not None:
        expiresDelta = datetime.utcnow() + expiresDelta
    else:
        expiresDelta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    toEncode = {"exp": expiresDelta, "sub": str(subject)}
    encodedJwt = jwt.encode(toEncode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encodedJwt