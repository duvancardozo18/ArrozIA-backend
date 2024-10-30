from sqlalchemy.orm import Session
from src.models.taskModel import Task
from src.schemas.taskSchema import TaskCreate, TaskUpdate

def get_all_tasks(db: Session):
    # Obtiene todas las tareas sin cargar relaciones
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: int):
    # Obtiene una tarea por ID sin cargar relaciones
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    # Crea una nueva tarea solo con los campos necesarios
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate):
    # Actualiza una tarea existente sin cargar relaciones
    db_task = get_task_by_id(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    # Elimina una tarea por ID sin cargar relaciones
    db_task = get_task_by_id(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
