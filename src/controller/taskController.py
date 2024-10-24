from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.taskModel import Task
from src.schemas.taskSchema import TaskCreate, TaskUpdate
from typing import List

def create_task(task: TaskCreate, session: Session):
    new_task = Task(**task.dict())
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

def get_all_tasks(session: Session) -> List[Task]:
    tasks = session.query(Task).all()
    return tasks

def get_task_by_id(task_id: int, session: Session):
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(task_id: int, task: TaskUpdate, session: Session):
    task_to_update = session.query(Task).filter(Task.id == task_id).first()
    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict().items():
        setattr(task_to_update, key, value)

    session.commit()
    session.refresh(task_to_update)
    return task_to_update

def delete_task(task_id: int, session: Session):
    task_to_delete = session.query(Task).filter(Task.id == task_id).first()
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task_to_delete)
    session.commit()
    return {"message": "Task deleted successfully"}
