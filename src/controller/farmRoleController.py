from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.models.farmRoleModel import UserFarmRol


def getUserFarmRol(session: Session = Depends(get_session)):
    userFarmRol = session.query(UserFarmRol).all()
    return userFarmRol

def getUserFarmRolById(user_id: int, session: Session = Depends(get_session)):
    farmUserRol = session.query(UserFarmRol).filter(UserFarmRol.usuario_id == user_id).first()
    if not farmUserRol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no hay usuario con id {user_id} "
        )
    return farmUserRol