from sqlalchemy import (Boolean, Column, Date, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from src.models.cropModel import Crop

from src.database.database import \
    Base  # Asegúrate de importar tu base correctamente


class DiagnosticoFitosanitario(Base):
    __tablename__ = "diagnostico_fitosanitario"
    
    id = Column(Integer, primary_key=True, index=True)
    resultado_ia = Column(String, nullable=False)
    ruta = Column(String, nullable=False)
    cultivo_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)
    fecha_diagnostico = Column(Date, nullable=False)
    confianza_promedio = Column(Float, nullable=True)
    tipo_problema = Column(String, nullable=True)
    imagenes_analizadas = Column(Integer, nullable=True)
    exportado = Column(Boolean, default=False)
    comparacion_diagnostico = Column(String, nullable=True)

    # Relación con el modelo Crop para obtener datos del cultivo
    cultivo = relationship("Crop", back_populates="diagnosticos")