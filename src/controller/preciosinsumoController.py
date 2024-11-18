from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Dict
from src.database.database import get_session
from src.models.taskModel import Task
from src.models.agriculturalInputModel import AgriculturalInput
from src.schemas.preciosinsumoSchema import AgriculturalInputWithTipoSchema


def get_inputs_by_crop(cultivo_id: int, session: Session = Depends(get_session)) -> List[AgriculturalInputWithTipoSchema]:
    """
    Obtiene todos los insumos agrícolas relacionados con un cultivo.
    """
    tasks_with_inputs = session.query(Task).options(
        joinedload(Task.insumo_agricola).joinedload(AgriculturalInput.tipo_insumo)
    ).filter(Task.cultivo_id == cultivo_id).all()

    result = []
    for task in tasks_with_inputs:
        if task.insumo_agricola:
            valor_unitario = task.insumo_agricola.costo_unitario or 0
            cantidad = task.cantidad_insumo or 0
            valor_total = valor_unitario * cantidad

            insumo_data = AgriculturalInputWithTipoSchema(
                concepto=task.insumo_agricola.nombre,
                descripcion=task.insumo_agricola.descripcion,
                valor_unitario=valor_unitario,
                cantidad=cantidad,
                valor_total=valor_total,
                tipo_insumo={
                    "id": task.insumo_agricola.tipo_insumo.id if task.insumo_agricola.tipo_insumo else None,
                    "nombre": task.insumo_agricola.tipo_insumo.nombre if task.insumo_agricola.tipo_insumo else None
                }
            )
            result.append(insumo_data)
    return result


def get_total_input_cost_by_crop(cultivo_id: int, session: Session = Depends(get_session)) -> Dict[str, float]:
    """
    Calcula el costo total de todos los insumos agrícolas relacionados con un cultivo.
    """
    tasks_with_inputs = session.query(Task).options(
        joinedload(Task.insumo_agricola)
    ).filter(Task.cultivo_id == cultivo_id).all()

    total_cost = 0
    for task in tasks_with_inputs:
        if task.insumo_agricola:
            valor_unitario = task.insumo_agricola.costo_unitario or 0
            cantidad = task.cantidad_insumo or 0
            total_cost += valor_unitario * cantidad  # Suma al total

    return {"cultivo_id": cultivo_id, "total_cost": total_cost}


def get_inputs_by_crop_and_partial_name(
    cultivo_id: int, concepto: str, session: Session = Depends(get_session)
) -> List[AgriculturalInputWithTipoSchema]:
    """
    Obtiene los insumos agrícolas relacionados con un cultivo filtrados por un concepto parcial.
    """
    # Normalizar el concepto
    concepto = concepto.strip().lower()

    tasks_with_inputs = session.query(Task).options(
        joinedload(Task.insumo_agricola).joinedload(AgriculturalInput.tipo_insumo)
    ).filter(
        Task.cultivo_id == cultivo_id,
        Task.insumo_agricola.has(func.lower(AgriculturalInput.nombre).ilike(f"{concepto}%"))  # Búsqueda parcial por prefijo
    ).all()

    result = []
    for task in tasks_with_inputs:
        if task.insumo_agricola:
            valor_unitario = task.insumo_agricola.costo_unitario or 0
            cantidad = task.cantidad_insumo or 0
            valor_total = valor_unitario * cantidad

            insumo_data = AgriculturalInputWithTipoSchema(
                concepto=task.insumo_agricola.nombre,
                descripcion=task.insumo_agricola.descripcion,
                valor_unitario=valor_unitario,
                cantidad=cantidad,
                valor_total=valor_total,
                tipo_insumo={
                    "id": task.insumo_agricola.tipo_insumo.id if task.insumo_agricola.tipo_insumo else None,
                    "nombre": task.insumo_agricola.tipo_insumo.nombre if task.insumo_agricola.tipo_insumo else None
                }
            )
            result.append(insumo_data)

    return result
