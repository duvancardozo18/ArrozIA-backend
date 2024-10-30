from sqlalchemy import Column, Integer, JSON, String
from src.database.database import Base

class Diagnostic(Base):
    __tablename__ = "diagnostico_fitosanitario"

    id = Column(Integer, primary_key=True, index=True)
    resultado_ia = Column(JSON, nullable=True)
    ruta = Column(String(255), nullable=True)
