from pydantic import BaseModel

class PasswordUpdate(BaseModel):
    new_password: str
    
class ChangePasswordResponse(BaseModel):
    message: str
    change_password_required: bool
        
class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str

class PasswordResetRequest(BaseModel):
    email: str




