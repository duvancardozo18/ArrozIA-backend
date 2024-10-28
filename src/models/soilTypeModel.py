from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class SoilType(Base):
    __tablename__ = 'tipo_suelo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)

    # Relación inversa con SoilAnalysis
    soil_analyses = relationship("SoilAnalysis", back_populates="tipo_suelo")
