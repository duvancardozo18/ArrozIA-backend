from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from src.models.taskModel import Task
from src.schemas.taskSchema import TaskCreate, TaskUpdate


def get_all_tasks(db: Session):
    """
    Obtiene todas las tareas sin cargar relaciones.
    """
    return db.query(Task).all()


def get_task_by_id(db: Session, task_id: int):
    """
    Obtiene una tarea por ID sin cargar relaciones.
    """
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate):
    """
    Crea una nueva tarea, incluyendo el nuevo campo precio_labor_cultural.
    """
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    """
    Actualiza una tarea existente. Si el estado cambia a 3,
    guarda la fecha y hora actual en el campo `fecha_realizacion`.
    """
    db_task = get_task_by_id(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            # Actualiza cada campo proporcionado
            setattr(db_task, key, value)
        
        # Verificar si el estado cambió a 3
        if task.estado_id == 3:
            db_task.fecha_realizacion = datetime.now()
        
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    """
    Elimina una tarea por ID.
    """
    db_task = get_task_by_id(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task


def get_tasks_by_crop_id(db: Session, crop_id: int):
    """
    Obtiene todas las tareas relacionadas con un cultivo específico por su ID.
    """
    return (
        db.query(Task)
        .filter(Task.cultivo_id == crop_id)
        .options(joinedload(Task.labor_cultural))  # Carga la relación
        .all()
    )


def update_task_state_and_date(db: Session, task_id: int, new_state: int):
    """
    Actualiza el estado de una tarea. Si el estado es 3, guarda la fecha y hora
    actual en el campo `fecha_realizacion`.
    """
    # Obtener la tarea
    db_task = get_task_by_id(db, task_id)

    if not db_task:
        return {"error": "Tarea no encontrada"}

    # Actualizar el estado
    db_task.estado_id = new_state

    # Si el estado es 3, asignar fecha_realizacion
    if new_state == 3:
        db_task.fecha_realizacion = datetime.now()

    # Guardar los cambios
    db.commit()
    db.refresh(db_task)

    return {
        "message": "Tarea actualizada correctamente",
        "tarea": {
            "id": db_task.id,
            "estado": db_task.estado_id,
            "fecha_realizacion": db_task.fecha_realizacion,
        },
    }
