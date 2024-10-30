from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controller.monitoringController import (
    create_monitoring,
    get_monitorings,
    get_monitoring,
    update_monitoring,
    delete_monitoring
)
from src.schemas.monitoringSchema import (
    MonitoringCreate,
    MonitoringUpdate,
    MonitoringOut
)
from src.database.database import get_db

MONITORING_ROUTES = APIRouter()

@MONITORING_ROUTES.post("/monitoring/", response_model=MonitoringOut, status_code=status.HTTP_201_CREATED)
def create_monitoring_route(monitoring: MonitoringCreate, db: Session = Depends(get_db)):
    return create_monitoring(db, monitoring)

@MONITORING_ROUTES.get("/monitoring/", response_model=list[MonitoringOut])
def read_monitorings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_monitorings(db, skip, limit)

@MONITORING_ROUTES.get("/monitoring/{monitoring_id}", response_model=MonitoringOut)
def read_monitoring(monitoring_id: int, db: Session = Depends(get_db)):
    return get_monitoring(db, monitoring_id)

@MONITORING_ROUTES.put("/monitoring/{monitoring_id}", response_model=MonitoringOut)
def update_monitoring_route(monitoring_id: int, monitoring: MonitoringUpdate, db: Session = Depends(get_db)):
    updated_monitoring = update_monitoring(db, monitoring_id, monitoring)
    return updated_monitoring

@MONITORING_ROUTES.delete("/monitoring/{monitoring_id}", status_code=status.HTTP_200_OK)
def delete_monitoring_route(monitoring_id: int, db: Session = Depends(get_db)):
    return delete_monitoring(db, monitoring_id)
