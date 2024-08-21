from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.permissionController import check_permission
from src.database.database import get_session 

ROL_PERMISSION_ROUTES = APIRouter()

@ROL_PERMISSION_ROUTES.get("/view-secure-data")
def view_secure_data(user_id: int, db: Session = Depends(get_session)):
    permission_name = "view_secure_data"
    check_permission(user_id, permission_name, db)
    return {"message": "You have access to view secure data"}

@ROL_PERMISSION_ROUTES.get("/edit-secure-data")
def edit_secure_data(user_id: int, db: Session = Depends(get_session)):
    permission_name = "edit_secure_data"
    check_permission(user_id, permission_name, db)
    return {"message": "You have access to edit secure data"}
