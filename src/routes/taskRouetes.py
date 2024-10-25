from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.schemas.taskSchema import TaskCreate, TaskUpdate, TaskResponse
from src.controller.taskController import (
    create_task, 
    get_all_tasks, 
    get_task_by_id, 
    update_task, 
    delete_task
)
from typing import List

TASK_ROUTES = APIRouter()

# Crear tarea
@TASK_ROUTES.post("/task", response_model=TaskResponse)
def create_task_route(task: TaskCreate, session: Session = Depends(get_session)):
    return create_task(task, session)

# Obtener todas las tareas
@TASK_ROUTES.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks_route(session: Session = Depends(get_session)):
    return get_all_tasks(session)

# Obtener tarea por ID
@TASK_ROUTES.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id_route(task_id: int, session: Session = Depends(get_session)):
    return get_task_by_id(task_id, session)

# Actualizar tarea
@TASK_ROUTES.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, task: TaskUpdate, session: Session = Depends(get_session)):
    return update_task(task_id, task, session)

# Eliminar tarea
@TASK_ROUTES.delete("/tasks/{task_id}")
def delete_task_route(task_id: int, session: Session = Depends(get_session)):
    return delete_task(task_id, session)
