from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class AuditBase(BaseModel):
    table_name: str
    operation_type: str
    record_id: int
    changed_data: Optional[Any]
    operation_timestamp: datetime

class AuditOut(AuditBase):
    id: int

    class Config:
        orm_mode = True
