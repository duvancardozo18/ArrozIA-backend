from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from src.database.database import Base

# Asegúrate de importar las clases relacionadas
from src.models.variedadArrozModel import VariedadArroz  
from src.models.loteModel import Lote
from src.models.unidadPesoModel import UnidadPeso

class Cultivo(Base):
    __tablename__ = 'cultivo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cultivo = Column(String(100), nullable=False)
    variedad_id = Column(Integer, ForeignKey('variedad_arroz.id'), nullable=False)
    lote_id = Column(Integer, ForeignKey('lote.id'), nullable=False)
    fecha_siembra = Column(Date, nullable=True)
    fecha_estimada_cosecha = Column(Date, nullable=True)
    fecha_real_cosecha = Column(Date, nullable=True)
    cantidad_cosechada = Column(Float, nullable=True)
    unidad_peso_id = Column(Integer, ForeignKey('unidad_peso.id'), nullable=True)
    ingresos = Column(Float, nullable=True)

    # Relaciones
    variedad = relationship("VariedadArroz", back_populates="cultivos")
    lote = relationship("Lote", back_populates="cultivos")
    unidad_peso = relationship("UnidadPeso", back_populates="cultivos")
