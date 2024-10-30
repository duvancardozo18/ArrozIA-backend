from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.diagnosticController import (
    create_diagnostic, get_diagnostic, get_diagnostics, update_diagnostic, delete_diagnostic
)
from src.schemas.diagnosticSchema import Diagnostic, DiagnosticCreate
from src.database.database import get_db

DIAGNOSTIC_ROUTES = APIRouter()

# Crear un nuevo diagnóstico fitosanitario
@DIAGNOSTIC_ROUTES.post("/diagnostics/", response_model=Diagnostic)
def create_diagnostic_route(diagnostic: DiagnosticCreate, db: Session = Depends(get_db)):
    return create_diagnostic(db, diagnostic)

# Obtener un diagnóstico fitosanitario por ID
@DIAGNOSTIC_ROUTES.get("/diagnostics/{diagnostic_id}", response_model=Diagnostic)
def read_diagnostic(diagnostic_id: int, db: Session = Depends(get_db)):
    return get_diagnostic(db, diagnostic_id)

# Obtener todos los diagnósticos fitosanitarios
@DIAGNOSTIC_ROUTES.get("/diagnostics/", response_model=list[Diagnostic])
def read_all_diagnostics(db: Session = Depends(get_db)):
    return get_diagnostics(db)

# Actualizar un diagnóstico fitosanitario
@DIAGNOSTIC_ROUTES.put("/diagnostics/{diagnostic_id}", response_model=Diagnostic)
def update_diagnostic_route(diagnostic_id: int, diagnostic: DiagnosticCreate, db: Session = Depends(get_db)):
    return update_diagnostic(db, diagnostic_id, diagnostic)

# Eliminar un diagnóstico fitosanitario
@DIAGNOSTIC_ROUTES.delete("/diagnostics/{diagnostic_id}", response_model=dict)
def delete_diagnostic_route(diagnostic_id: int, db: Session = Depends(get_db)):
    return delete_diagnostic(db, diagnostic_id)
