from sqlalchemy import Boolean, Column, ForeignKey, Integer, JSON, String
from src.database.database import Base
from sqlalchemy.orm import relationship

class Diagnostic(Base):
    __tablename__ = "diagnostico_fitosanitario"

    id = Column(Integer, primary_key=True, index=True)
    resultado_ia = Column(JSON)
    tarea_labor_id = Column(Integer, ForeignKey('tarea_labor_cultural.id'))
    online = Column(Boolean, default=False)
    sincronizado = Column(Boolean, default=False)

    # Relación con la tarea
    #task = relationship("Task", back_populates="diagnostics")
