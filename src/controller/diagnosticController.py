from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.diagnosticModel import Diagnostic
from src.schemas.diagnosticSchema import DiagnosticCreate, DiagnosticUpdate

def create_diagnostic(db: Session, diagnostic: DiagnosticCreate):
    # Verificar si ya existe un diagnóstico para la tarea especificada
    existing_diagnostic = db.query(Diagnostic).filter(Diagnostic.tarea_labor_id == diagnostic.tarea_labor_id).first()
    if existing_diagnostic:
        raise HTTPException(status_code=400, detail="A diagnostic already exists for this task.")
    
    # Crear el nuevo diagnóstico si no existe uno previo para la tarea
    new_diagnostic = Diagnostic(**diagnostic.dict())
    db.add(new_diagnostic)
    db.commit()
    db.refresh(new_diagnostic)
    return new_diagnostic

def get_all_diagnostics(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Diagnostic).offset(skip).limit(limit).all()

def get_diagnostic_by_id(db: Session, diagnostic_id: int):
    diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")
    return diagnostic

def update_diagnostic(db: Session, diagnostic_id: int, diagnostic: DiagnosticUpdate):
    existing_diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if not existing_diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic not found for update.")
    
    print("Datos antes de la actualización:", existing_diagnostic.resultado_ia)
    print("Datos a actualizar:", diagnostic.resultado_ia)

    # Verificar duplicados solo si se proporciona un nuevo tarea_labor_id
    if diagnostic.tarea_labor_id is not None:
        duplicate_diagnostic = db.query(Diagnostic).filter(
            Diagnostic.tarea_labor_id == diagnostic.tarea_labor_id,
            Diagnostic.id != diagnostic_id
        ).first()
        if duplicate_diagnostic:
            raise HTTPException(
                status_code=400, 
                detail="Another diagnostic already exists for the specified task."
            )
    
    # Actualizar los campos
    if diagnostic.resultado_ia is not None:
        existing_diagnostic.resultado_ia = diagnostic.resultado_ia
    
    existing_diagnostic.tarea_labor_id = diagnostic.tarea_labor_id or existing_diagnostic.tarea_labor_id
    existing_diagnostic.online = diagnostic.online if diagnostic.online is not None else existing_diagnostic.online
    existing_diagnostic.sincronizado = diagnostic.sincronizado if diagnostic.sincronizado is not None else existing_diagnostic.sincronizado
    
    db.commit()
    
    # Verifica los valores después del commit
    print("Datos después de commit (antes de refresh):", existing_diagnostic.resultado_ia)
    db.refresh(existing_diagnostic)
    print("Datos después de refresh:", existing_diagnostic.resultado_ia)

    return existing_diagnostic

def delete_diagnostic(db: Session, diagnostic_id: int):
    diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic not found for deletion.")
    
    db.delete(diagnostic)
    db.commit()
    return {"message": "Diagnostic deleted successfully"}
