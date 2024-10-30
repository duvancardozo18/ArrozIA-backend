from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class VarietyRiceStageModel(Base):
    __tablename__ = "variedad_arroz_etapa_fenologica"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    etapa_fenologica_id = Column(Integer, ForeignKey("etapa_fenologica.id", ondelete="SET NULL"), nullable=True)
    dias_duracion = Column(Integer)
    variedad_arroz_id = Column(Integer, ForeignKey("variedad_arroz.id", ondelete="CASCADE"))

    # Relación con la tabla `variedad_arroz`
    variety = relationship("VarietyArrozModel", back_populates="stages")

    # Relación con la tabla `etapa_fenologica`
    phenological_stage = relationship("PhenologicalStage", back_populates="varieties")


    # Relación inversa con el modelo Monitoring
    monitoreos = relationship("Monitoring", back_populates="variedad_arroz_etapa_fenologica")
