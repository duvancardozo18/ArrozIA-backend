from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.models.agriculturalInputModel import AgriculturalInput
from src.schemas.agriculturalInputSchema import (AgriculturalInputCreate,
                                                 AgriculturalInputUpdate)


def createInput(insumo: AgriculturalInputCreate, session: Session = Depends(get_session)):
    newInsumo = AgriculturalInput(
        nombre=insumo.nombre,
        descripcion=insumo.descripcion,
        unidad_id=insumo.unidad_id,
        costo_unitario=insumo.costo_unitario
    )
    session.add(newInsumo)
    session.commit()
    session.refresh(newInsumo)
    
    return {"msg": "Insumo agrícola creado satisfactoriamente", "newInsumo": newInsumo}


def getAllInput(session: Session = Depends(get_session)):
    insumos = session.query(AgriculturalInput).all()
    return insumos


def getInputById(insumo_id: int, session: Session = Depends(get_session)):
    insumo = session.query(AgriculturalInput).filter(AgriculturalInput.id == insumo_id).first()
    if not insumo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insumo agrícola con id {insumo_id} no encontrado"
        )
    return insumo


def updateInput(insumo_id: int, insumo_data: AgriculturalInputUpdate, session: Session = Depends(get_session)):
    insumo = session.query(AgriculturalInput).filter(AgriculturalInput.id == insumo_id).first()
    if not insumo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insumo agrícola con id {insumo_id} no encontrado"
        )

    # Convertir insumo_data a un diccionario y excluir valores no enviados
    update_data = insumo_data.dict(exclude_unset=True)

    # Actualizar solo los campos que se han enviado
    for key, value in update_data.items():
        setattr(insumo, key, value)

    session.commit()
    session.refresh(insumo)

    return {"msg": "Insumo agrícola actualizado satisfactoriamente", "insumo":insumo}


def deleteInput(insumo_id: int, session: Session = Depends(get_session)):
    insumo = session.query(AgriculturalInput).filter(AgriculturalInput.id == insumo_id).first()
    if not insumo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insumo agrícola con id {insumo_id} no encontrado"
        )

    session.delete(insumo)
    session.commit()

    return {"msg": "Insumo agrícola eliminado satisfactoriamente"}
