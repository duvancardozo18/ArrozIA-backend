from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from src.models.taskModel import Task
from datetime import datetime


def get_cultural_works_by_crop(db: Session, cultivo_id: int):
    tasks = db.query(Task).options(
        joinedload(Task.labor_cultural),
        joinedload(Task.maquinaria_agricola),
        joinedload(Task.usuario)
    ).filter(Task.cultivo_id == cultivo_id).all()

    return _build_cultural_work_list(tasks)


def get_total_cultural_works_value(db: Session, cultivo_id: int):
    """
    Calcula el valor total de todas las actividades culturales relacionadas con un cultivo.
    """
    tasks = db.query(Task).options(
        joinedload(Task.labor_cultural),
        joinedload(Task.maquinaria_agricola)
    ).filter(Task.cultivo_id == cultivo_id).all()

    total_value_sum = sum(
        ((task.labor_cultural.precio_hectaria or 0) if task.labor_cultural else 0) +
        ((task.maquinaria_agricola.costPerHour or 0) if task.maquinaria_agricola else 0)
        for task in tasks
    )

    return {"total_value": total_value_sum}


def filter_by_activity(cultivo_id: int, activity_name: str, db: Session):
    tasks = db.query(Task).options(
        joinedload(Task.labor_cultural)
    ).filter(
        Task.cultivo_id == cultivo_id,
        Task.labor_cultural.has(func.lower(Task.labor_cultural.property.mapper.class_.nombre).like(f"%{activity_name.lower()}%"))
    ).all()

    return _build_cultural_work_list(tasks)


def filter_by_machinery(cultivo_id: int, machinery_name: str, db: Session):
    tasks = db.query(Task).options(
        joinedload(Task.maquinaria_agricola)
    ).filter(
        Task.cultivo_id == cultivo_id,
        Task.maquinaria_agricola.has(func.lower(Task.maquinaria_agricola.property.mapper.class_.name).like(f"%{machinery_name.lower()}%"))
    ).all()

    return _build_cultural_work_list(tasks)


def filter_by_operator(cultivo_id: int, operator_name: str, db: Session):
    tasks = db.query(Task).options(
        joinedload(Task.usuario)
    ).filter(
        Task.cultivo_id == cultivo_id,
        Task.usuario.has(func.lower(Task.usuario.property.mapper.class_.nombre).like(f"%{operator_name.lower()}%"))
    ).all()

    return _build_cultural_work_list(tasks)


def filter_by_date_range(cultivo_id: int, start_date: datetime, end_date: datetime, db: Session):
    tasks = db.query(Task).options(
        joinedload(Task.labor_cultural),
        joinedload(Task.maquinaria_agricola),
        joinedload(Task.usuario)
    ).filter(
        Task.cultivo_id == cultivo_id,
        and_(
            Task.fecha_realizacion >= start_date,
            Task.fecha_realizacion <= end_date
        )
    ).all()

    return _build_cultural_work_list(tasks)


def _build_cultural_work_list(tasks):
    cultural_works = []
    for task in tasks:
        labor = task.labor_cultural
        maquinaria = task.maquinaria_agricola
        usuario = task.usuario

        labor_cost = labor.precio_hectaria if labor else 0
        machinery_cost = maquinaria.costPerHour if maquinaria else 0
        total_value = (labor_cost or 0) + (machinery_cost or 0)

        cultural_works.append({
            "fecha_inicio": task.fecha_realizacion or datetime.now(),
            "fecha_culminacion": task.fecha_realizacion or datetime.now(),
            "actividad": labor.nombre if labor else "No definida",
            "maquinaria": maquinaria.name if maquinaria else "No aplica",
            "operario": usuario.nombre if usuario else "No definido",
            "descripcion": task.descripcion,
            "valor": total_value
        })

    return cultural_works
