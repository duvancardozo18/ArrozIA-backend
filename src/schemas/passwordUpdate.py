from pydantic import BaseModel

class PasswordUpdate(BaseModel):
    new_password: str
