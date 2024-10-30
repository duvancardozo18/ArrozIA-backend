from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class VarietyArrozModel(Base):
    __tablename__ = 'variedad_arroz'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)  # Cambiado de 50 a 100
    numero_registro_productor_ica = Column(String(50), nullable=False)  # Cambiado a String
    caracteristicas_variedad = Column(Text, nullable=True)

    # Relación con la tabla de cultivos (crops)
    crops = relationship("Crop", order_by="Crop.id", back_populates="variety")

    # Relación inversa con VarietyRiceStageModel
    stages = relationship("VarietyRiceStageModel", back_populates="variety", cascade="all, delete-orphan")
