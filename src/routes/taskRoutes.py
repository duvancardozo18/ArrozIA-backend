from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.controller.taskController import (
    get_all_tasks, get_task_by_id, create_task, update_task, delete_task, get_tasks_by_crop_id
)
from src.schemas.taskSchema import TaskCreate, TaskUpdate, TaskOut

TASK_ROUTES = APIRouter()

@TASK_ROUTES.get("/taskslist", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return get_all_tasks(db)

@TASK_ROUTES.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@TASK_ROUTES.post("/tasksCreate", response_model=TaskOut)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)

@TASK_ROUTES.put("/tasks/{task_id}", response_model=TaskOut)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@TASK_ROUTES.delete("/tasks/{task_id}", response_model=TaskOut)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# Nuevo endpoint para obtener tareas asociadas a un cultivo específico
@TASK_ROUTES.get("/crops/{crop_id}/tasks", response_model=list[TaskOut])
def get_tasks_for_crop(crop_id: int, db: Session = Depends(get_db)):
    tasks = get_tasks_by_crop_id(db, crop_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this crop")
    return tasks
