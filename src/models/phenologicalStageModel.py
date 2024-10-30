# src/models/phenologicalStageModel.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class PhenologicalStage(Base):
    __tablename__ = 'etapa_fenologica'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    fase = Column(String(50), nullable=False)

    # Relación inversa hacia VarietyRiceStageModel
    varieties = relationship("VarietyRiceStageModel", back_populates="phenological_stage")
