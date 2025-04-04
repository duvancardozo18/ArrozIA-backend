from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from src.database.database import get_session
from src.models.agriculturalInputModel import AgriculturalInput, UnidadInsumo, TipoInsumo
from src.schemas.agriculturalInputSchema import (AgriculturalInputCreate, AgriculturalInputUpdate, TipoInsumoSchema)

def createInput(insumo: AgriculturalInputCreate, session: Session = Depends(get_session)):
    newInsumo = AgriculturalInput(
        nombre=insumo.nombre,
        descripcion=insumo.descripcion,
        unidad_id=insumo.unidad_id,
        tipo_insumo_id=insumo.tipo_insumo_id,  # Nuevo campo agregado
        costo_unitario=insumo.costo_unitario,
        cantidad=insumo.cantidad
    )
    session.add(newInsumo)
    session.commit()
    session.refresh(newInsumo)
    
    return {"msg": "Insumo agrícola creado satisfactoriamente", "newInsumo": newInsumo}

def getAllInput(session: Session = Depends(get_session)):
    # Usar joinedload para cargar las relaciones `unidad` y `tipo_insumo`
    insumos = session.query(AgriculturalInput).options(
        joinedload(AgriculturalInput.unidad),
        joinedload(AgriculturalInput.tipo_insumo)  # Cargar la relación con tipo_insumo
    ).all()
    return insumos

def getInputById(insumo_id: int, session: Session = Depends(get_session)):
    # Cargar las relaciones `unidad` y `tipo_insumo`
    insumo = session.query(AgriculturalInput).options(
        joinedload(AgriculturalInput.unidad),
        joinedload(AgriculturalInput.tipo_insumo)
    ).filter(AgriculturalInput.id == insumo_id).first()
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

    return {"msg": "Insumo agrícola actualizado satisfactoriamente", "insumo": insumo}

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

def get_all_units(session: Session):
    return session.query(UnidadInsumo).all()

def get_all_input_types(session: Session):
    tipos = session.query(TipoInsumo).all()
    return [{"id": tipo.id, "nombre": tipo.nombre} for tipo in tipos]