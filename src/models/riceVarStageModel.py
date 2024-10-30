from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class RiceVarStageModel(Base):
    __tablename__ = "variedad_arroz_etapa_fenologica"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    etapa_fenologica_id = Column(Integer)  # Columna para la etapa fenológica
    dias_duracion = Column(Integer)
    variedad_arroz_id = Column(Integer)
    labor_cultural_id = Column(Integer)

    # Relación inversa con el modelo Monitoring
    monitoreos = relationship("Monitoring", back_populates="variedad_arroz_etapa_fenologica")