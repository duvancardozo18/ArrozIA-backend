from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import src.schemas.schemas as schemas
from src.controller.permissionController import get_all_permissions, createPermission, getPermission, updatePermission, deletePermission
from src.database.database import get_session

PERMISSION_ROUTES = APIRouter()

@PERMISSION_ROUTES.get("/permissions", response_model=dict)
def get_all_permissions_route(db: Session = Depends(get_session)):
    return get_all_permissions(db)


@PERMISSION_ROUTES.post("/permissions/create", response_model=schemas.PermissionSchema)
def createPermissionRoute(permission: schemas.CreatePermission, session: Session = Depends(get_session)):
    return createPermission(permission, session)

@PERMISSION_ROUTES.get("/permissions/{id}", response_model=schemas.PermissionSchema)
def getPermissionRoute(id: int, session: Session = Depends(get_session)):  # Cambia `permission_id` a `id` para coincidir con el parámetro
    return getPermission(id, session)

@PERMISSION_ROUTES.put("/permissions/update/{id}", response_model=schemas.PermissionSchema)
def updatePermissionRoute(id: int, permission: schemas.UpdatePermission, session: Session = Depends(get_session)):
    return updatePermission(id, permission, session)

@PERMISSION_ROUTES.delete("/permissions/delete/{id}")
def deletePermissionRoute(id: int, session: Session = Depends(get_session)):
    return deletePermission(id, session)
