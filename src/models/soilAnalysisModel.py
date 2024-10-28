from sqlalchemy import Column, Integer, Date, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.soilTypeModel import SoilType
from src.models.landModel import Land  # Asegúrate de que el import sea correcto

class SoilAnalysis(Base):
    __tablename__ = 'analisis_edafologico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lote_id = Column(Integer, ForeignKey('lote.id'), nullable=False)
    fecha_analisis = Column(Date, nullable=False)
    tipo_suelo_id = Column(Integer, ForeignKey('tipo_suelo.id'), nullable=False)
    archivo_reporte = Column(LargeBinary, nullable=True)

    # Relación con el modelo SoilType
    tipo_suelo = relationship("SoilType", back_populates="soil_analyses")
    
    # Relación con el modelo Land (antes Lote)
    lote = relationship("Land", back_populates="analisis_edafologico")
