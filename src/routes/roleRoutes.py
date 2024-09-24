from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.roleController import create_role, get_roles, get_role_by_id, update_role, delete_role
from src.database.database import get_session
from src.helpers.utils import  verify_permission
from src.schemas.roleShema import Role, RoleCreate, RoleUpdate

ROLE_ROUTES = APIRouter()

@ROLE_ROUTES.post("/roles", dependencies=[Depends(verify_permission("crear_rol"))], response_model=dict)
def create_role_route(role: RoleCreate, db: Session = Depends(get_session)):
    return create_role(role, db)

@ROLE_ROUTES.get("/roles", dependencies=[Depends(verify_permission("crear_rol"))], response_model=dict)
def get_roles_route(db: Session = Depends(get_session)):
    roles_data = get_roles(db)
    roles = [Role.from_orm(role) for role in roles_data["roles"] if role.descripcion is not None]
    return {"message": roles_data["message"], "roles": roles}

@ROLE_ROUTES.get("/roles/{role_id}", dependencies=[Depends(verify_permission("ver_rol"))], response_model=dict)
def get_role_by_id_route(role_id: int, db: Session = Depends(get_session)):
    return get_role_by_id(role_id, db)

@ROLE_ROUTES.put("/roles/{role_id}", dependencies=[Depends(verify_permission("actualizar_rol"))], response_model=dict)
def update_role_route(role_id: int, role: RoleUpdate, db: Session = Depends(get_session)):
    return update_role(role_id, role, db)

@ROLE_ROUTES.delete("/roles/{role_id}", dependencies=[Depends(verify_permission("eliminar_rol"))], response_model=dict)
def delete_role_route(role_id: int, db: Session = Depends(get_session)):
    return delete_role(role_id, db)
