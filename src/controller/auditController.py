from sqlalchemy.orm import Session
from src.models.auditModel import AuditLog

def get_all_audits(db: Session):
    return db.query(AuditLog).all()

def get_audits_by_table(db: Session, table_name: str):
    return db.query(AuditLog).filter(AuditLog.table_name == table_name).all()

def get_audits_by_operation(db: Session, operation_type: str):
    return db.query(AuditLog).filter(AuditLog.operation_type == operation_type).all()

def get_audit_by_table_and_id(db: Session, table_name: str, record_id: int):
    return (
        db.query(AuditLog)
        .filter(AuditLog.table_name == table_name, AuditLog.record_id == record_id)
        .all()
    )
