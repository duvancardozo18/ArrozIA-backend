from sqlalchemy import DECIMAL, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class Land(Base):
    __tablename__ = 'lote'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    finca_id = Column(Integer, ForeignKey('finca.id'), nullable=False)
    area = Column(Float, nullable=False)
    latitud = Column(DECIMAL(10, 5), nullable=True)
    longitud = Column(DECIMAL(10, 5), nullable=True)
    slug = Column(String(255), nullable=False)  # Asegúrate de que el slug está definido
    arriendo_real = Column(Float, nullable=True)  # Nuevo campo agregado

    # Relaciones
    finca = relationship("Farm", back_populates="lotes")   
    crops = relationship("Crop", back_populates="lotes") 
    soil_analysis = relationship("SoilAnalysisModel", back_populates="lote")

    def __repr__(self):
        return f"<Land(id={self.id}, nombre={self.nombre}, slug={self.slug}, arriendo_real={self.arriendo_real})>"
