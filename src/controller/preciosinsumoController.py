from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from src.database.database import get_session
from src.models.taskModel import Task
from src.models.agriculturalInputModel import AgriculturalInput
from src.schemas.preciosinsumoSchema import AgriculturalInputWithTipoSchema


def get_inputs_by_crop(cultivo_id: int, session: Session = Depends(get_session)):
    # Consulta para obtener tareas con sus insumos agrícolas relacionados
    tasks_with_inputs = session.query(Task).options(
        joinedload(Task.insumo_agricola).joinedload(AgriculturalInput.tipo_insumo)  # Corregido
    ).filter(Task.cultivo_id == cultivo_id).all()

    # Construir la respuesta con los datos
    result = []
    for task in tasks_with_inputs:
        if task.insumo_agricola:  # Verifica que haya un insumo relacionado
            insumo_data = {
                "nombre": task.insumo_agricola.nombre,
                "descripcion": task.insumo_agricola.descripcion,
                "costo_unitario": task.insumo_agricola.costo_unitario,
                "precio_unitario_estimado": task.insumo_agricola.precio_unitario_estimado,
                "cantidad_insumo": task.cantidad_insumo,  # Desde Task
                "tipo_insumo": {
                    "id": task.insumo_agricola.tipo_insumo.id if task.insumo_agricola.tipo_insumo else None,
                    "nombre": task.insumo_agricola.tipo_insumo.nombre if task.insumo_agricola.tipo_insumo else None
                }
            }
            result.append(insumo_data)

    return result
