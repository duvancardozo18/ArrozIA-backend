from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.diagnosticModel import Diagnostic
from src.schemas.diagnosticSchema import DiagnosticCreate

def create_diagnostic(db: Session, diagnostic: DiagnosticCreate):
    db_diagnostic = Diagnostic(**diagnostic.dict())
    db.add(db_diagnostic)
    db.commit()
    db.refresh(db_diagnostic)
    return db_diagnostic

def get_diagnostics(db: Session):
    return db.query(Diagnostic).all()

def get_diagnostic(db: Session, diagnostic_id: int):
    diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if diagnostic is None:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    return diagnostic

def update_diagnostic(db: Session, diagnostic_id: int, diagnostic: DiagnosticCreate):
    db_diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if db_diagnostic is None:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    for key, value in diagnostic.dict().items():
        setattr(db_diagnostic, key, value)
    db.commit()
    db.refresh(db_diagnostic)
    return db_diagnostic

def delete_diagnostic(db: Session, diagnostic_id: int):
    diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if diagnostic is None:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    db.delete(diagnostic)
    db.commit()
    return {"detail": "Diagnóstico eliminado exitosamente"}
