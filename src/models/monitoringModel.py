from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class Monitoring(Base):
    __tablename__ = "monitoreos"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(100), nullable=False)
    variedad_arroz_etapa_fenologica_id = Column(Integer, ForeignKey("variedad_arroz_etapa_fenologica.id"), nullable=True)
    recomendacion = Column(Text)

    # Relación hacia la tabla variedad_arroz_etapa_fenologica
    variedad_arroz_etapa_fenologica = relationship("RiceVarStageModel", back_populates="monitoreos")
