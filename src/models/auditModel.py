from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP
from src.database.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)  # INSERT, UPDATE, DELETE
    record_id = Column(Integer, nullable=False)
    changed_data = Column(JSON, nullable=True)
    operation_timestamp = Column(TIMESTAMP, nullable=False)
