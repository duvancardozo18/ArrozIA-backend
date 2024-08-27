import jwt
from jwt.exceptions import InvalidKeyTypeError
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models.userModel import TokenTable
from jose import jwt
from src.helpers.config import JWT_SECRET_KEY, ALGORITHM

def decodeJWT(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
    except Exception:
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except Exception:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

jwt_bearer = JWTBearer()