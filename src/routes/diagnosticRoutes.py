from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controller.diagnosticController import (
    create_diagnostic, get_all_diagnostics, get_diagnostic_by_id, update_diagnostic, delete_diagnostic
)
from src.schemas.diagnosticSchema import (
    DiagnosticCreate, DiagnosticUpdate, DiagnosticResponse
)
from src.database.database import get_db

DIAGNOSTIC_ROUTES = APIRouter()

@DIAGNOSTIC_ROUTES.post("/diagnostics/", response_model=DiagnosticResponse, status_code=status.HTTP_201_CREATED)
def create_diagnosis(diagnostic: DiagnosticCreate, db: Session = Depends(get_db)):
    return create_diagnostic(db, diagnostic)

@DIAGNOSTIC_ROUTES.get("/diagnostics/", response_model=list[DiagnosticResponse])
def read_diagnostics(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_diagnostics(db, skip, limit)

@DIAGNOSTIC_ROUTES.get("/diagnostics/{diagnostic_id}", response_model=DiagnosticResponse)
def read_diagnosis(diagnostic_id: int, db: Session = Depends(get_db)):
    return get_diagnostic_by_id(db, diagnostic_id)

@DIAGNOSTIC_ROUTES.put("/diagnostics/{diagnostic_id}", response_model=DiagnosticResponse)
def update_diagnosis(diagnostic_id: int, diagnostic: DiagnosticUpdate, db: Session = Depends(get_db)):
    updated_diagnostic = update_diagnostic(db, diagnostic_id, diagnostic)
    return DiagnosticResponse.from_orm(updated_diagnostic)

@DIAGNOSTIC_ROUTES.delete("/diagnostics/{diagnostic_id}", status_code=status.HTTP_200_OK)
def delete_diagnosis(diagnostic_id: int, db: Session = Depends(get_db)):
    return delete_diagnostic(db, diagnostic_id)

