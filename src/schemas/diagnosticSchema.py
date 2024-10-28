from pydantic import BaseModel
from typing import Optional, Any

class DiagnosticBase(BaseModel):
    resultado_ia: Any
    tarea_labor_id: int
    online: bool
    sincronizado: Optional[bool] = False

class DiagnosticCreate(DiagnosticBase):
    pass

class DiagnosticUpdate(BaseModel):
    resultado_ia: Optional[Any] = None
    tarea_labor_id: Optional[int] = None
    online: Optional[bool] = None
    sincronizado: Optional[bool] = None


class DiagnosticResponse(DiagnosticBase):
    id: int

    class Config:
        from_attributes = True
