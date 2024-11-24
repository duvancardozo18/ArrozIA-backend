from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.auditController import (
    get_all_audits,
    get_audits_by_table,
    get_audits_by_operation,
    get_audit_by_table_and_id,
)
from src.database.database import get_session

AUDIT_ROUTES = APIRouter()

@AUDIT_ROUTES.get("/audits/")
def list_all_audits(db: Session = Depends(get_session)):
    return get_all_audits(db)

@AUDIT_ROUTES.get("/audits/table/{table_name}")
def list_audits_by_table(table_name: str, db: Session = Depends(get_session)):
    return get_audits_by_table(db, table_name)

@AUDIT_ROUTES.get("/audits/operation/{operation_type}")
def list_audits_by_operation(operation_type: str, db: Session = Depends(get_session)):
    return get_audits_by_operation(db, operation_type)

@AUDIT_ROUTES.get("/audits/{table_name}/{record_id}")
def get_audit_details(table_name: str, record_id: int, db: Session = Depends(get_session)):
    return get_audit_by_table_and_id(db, table_name, record_id)
