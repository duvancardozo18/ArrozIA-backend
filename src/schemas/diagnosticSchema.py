from pydantic import BaseModel
from typing import Optional

class DiagnosticBase(BaseModel):
    resultado_ia: Optional[dict] = None
    ruta: Optional[str] = None

class DiagnosticCreate(DiagnosticBase):
    pass

class Diagnostic(DiagnosticBase):
    id: int

    class Config:
        orm_mode = True
