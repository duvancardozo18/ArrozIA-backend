from sqlalchemy.orm import Session, joinedload
from src.models.costsModel import Costs
from src.models.taskModel import Task


def get_total_costs(db: Session, cultivo_id: int):
    """
    Obtiene:
    1. Costos (concepto y precio) de gastos asociados al cultivo.
    2. Precio total de insumos y labores culturales con conceptos "quemados".
    """
    # Obtener costos de la tabla 'gastos'
    costos = db.query(Costs).filter(Costs.cultivo_id == cultivo_id).all()
    costos_data = [{"concepto": costo.concepto, "total": costo.precio} for costo in costos]

    # Calcular el precio total de insumos
    tasks_with_inputs = db.query(Task).options(
        joinedload(Task.insumo_agricola)
    ).filter(Task.cultivo_id == cultivo_id).all()

    total_insumos = sum(
        (task.insumo_agricola.costo_unitario or 0) * (task.cantidad_insumo or 0)
        for task in tasks_with_inputs
        if task.insumo_agricola
    )

    # Calcular el precio total de labores culturales
    tasks_with_labors = db.query(Task).options(
        joinedload(Task.labor_cultural),
        joinedload(Task.maquinaria_agricola)
    ).filter(Task.cultivo_id == cultivo_id).all()

    total_labores = sum(
        ((task.labor_cultural.precio_hectaria or 0) if task.labor_cultural else 0) +
        ((task.maquinaria_agricola.costPerHour or 0) if task.maquinaria_agricola else 0)
        for task in tasks_with_labors
    )

    # Añadir los conceptos quemados para insumos y labores culturales
    costos_data.append({"concepto": "Insumos", "total": total_insumos})
    costos_data.append({"concepto": "Labores culturales", "total": total_labores})

    # Construir la respuesta
    response = {"costos": costos_data}
    return response

def get_overall_total_cost(db: Session, cultivo_id: int):
    """
    Calcula el total general de costos de un cultivo, sumando:
    1. Los costos de la tabla 'gastos'.
    2. El costo total de insumos.
    3. El costo total de labores culturales.
    """
    # Obtener costos de la tabla 'gastos'
    costos = db.query(Costs).filter(Costs.cultivo_id == cultivo_id).all()
    total_gastos = sum(costo.precio for costo in costos)

    # Calcular el precio total de insumos
    tasks_with_inputs = db.query(Task).options(
        joinedload(Task.insumo_agricola)
    ).filter(Task.cultivo_id == cultivo_id).all()

    total_insumos = sum(
        (task.insumo_agricola.costo_unitario or 0) * (task.cantidad_insumo or 0)
        for task in tasks_with_inputs
        if task.insumo_agricola
    )

    # Calcular el precio total de labores culturales
    tasks_with_labors = db.query(Task).options(
        joinedload(Task.labor_cultural),
        joinedload(Task.maquinaria_agricola)
    ).filter(Task.cultivo_id == cultivo_id).all()

    total_labores = sum(
        ((task.labor_cultural.precio_hectaria or 0) if task.labor_cultural else 0) +
        ((task.maquinaria_agricola.costPerHour or 0) if task.maquinaria_agricola else 0)
        for task in tasks_with_labors
    )

    # Calcular el total general
    total_general = total_gastos + total_insumos + total_labores

    return {"total_general": total_general}